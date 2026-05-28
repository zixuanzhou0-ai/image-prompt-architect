#!/usr/bin/env python3
"""Lint image prompts for structure, model fit, and common failure modes."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


SEVEN_REQUIRED = {
    "subject": [r"subject", r"主体", r"person", r"character", r"product", r"object"],
    "environment": [r"environment", r"环境", r"location", r"street", r"room", r"landscape", r"background"],
    "lighting": [r"lighting", r"atmosphere", r"光影", r"氛围", r"sunlight", r"moonlight", r"neon", r"volumetric", r"backlit"],
    "material": [r"material", r"texture", r"材质", r"silk", r"metal", r"glass", r"stone", r"grain", r"reflection"],
    "composition": [r"composition", r"camera", r"构图", r"lens", r"shot", r"framing", r"depth of field", r"bokeh"],
    "style": [r"style", r"风格", r"cinematic", r"film", r"illustration", r"render", r"editorial"],
    "context_tone": [r"context", r"intent", r"tone", r"语感", r"内涵", r"emotion", r"narrative", r"nostalgia"],
    "output_constraints": [r"output constraints", r"aspect ratio", r"avoid / replacement", r"must include", r"分辨率", r"比例"],
}

SYSTEM_REQUIRED = {
    "premise": [r"premise system", r"前提系统", r"series of", r"a set of"],
    "identity_lock": [r"identity lock", r"身份锁定", r"must never change"],
    "continuity": [r"continuity", r"连续性", r"must remain fixed"],
    "variation_budget": [r"variation budget", r"变化预算", r"may change"],
    "spatial": [r"spatial system", r"空间系统"],
    "character": [r"character system", r"人物系统"],
    "color": [r"color system", r"色彩系统"],
    "medium": [r"medium system", r"介质系统"],
    "composition": [r"composition system", r"构图系统"],
    "lighting": [r"lighting", r"atmosphere", r"光影"],
    "narrative": [r"narrative", r"emotion", r"叙事", r"情绪"],
    "quality_exclusion": [r"quality", r"exclusion", r"avoid", r"禁止", r"排除"],
    "shot_slots": [r"shot slot", r"frame 01", r"per-shot", r"分镜"],
}

COMPACT_REQUIRED = {
    "subject": [r"subject", r"person", r"character", r"product", r"singer", r"object", r"人物", r"一位", r"男人", r"女人", r"老板"],
    "setting": [r"setting", r"club", r"room", r"street", r"landscape", r"studio", r"background", r"老街", r"江南", r"雨后", r"木门"],
    "visual_style": [r"style", r"cinematic", r"film", r"noir", r"editorial", r"photo", r"illustration", r"电影感", r"人像"],
    "camera_or_composition": [r"camera", r"lens", r"shot", r"composition", r"35mm", r"50mm", r"85mm", r"foreground", r"portrait"],
    "lighting_or_mood": [r"light", r"lamp", r"shadow", r"mood", r"melancholy", r"atmosphere", r"smoky", r"overcast", r"克制"],
}

GENERIC_FILLER = {
    "beautiful",
    "stunning",
    "amazing",
    "aesthetic",
    "high quality",
    "best quality",
    "masterpiece",
    "cinematic",
    "ultra detailed",
    "professional",
}

CONCRETE_NOUNS = {
    "silk",
    "brass",
    "chrome",
    "cobblestone",
    "rain",
    "window",
    "lens",
    "shadow",
    "neon",
    "paper",
    "wood",
    "stone",
    "cotton",
    "glass",
    "street",
    "room",
    "product",
    "label",
    "poster",
    "book",
    "train",
    "school",
    "river",
    "lamp",
    "tile",
    "floor",
    "microphone",
    "jacket",
    "umbrella",
    "bottle",
    "ceramic",
}

PLACEHOLDER_RE = re.compile(r"^\s*(?:\.\.\.|tbd|todo|\[.*?\]|<.*?>|-)?\s*$", re.I)

STYLE_CONFLICTS = [
    ("watercolor", "photorealistic product photo", "watercolor conflicts with photorealistic product-photo intent"),
    ("vhs", "8k ultra sharp", "VHS softness conflicts with 8K ultra-sharp language"),
    ("oil painting", "3d render", "oil painting and 3D render are competing medium anchors"),
]

ERA_CONFLICTS = [
    ("1930", "smartphone", "1930s setting conflicts with smartphone-era detail"),
    ("1990", "iphone", "1990s setting conflicts with iPhone detail"),
    ("medieval", "neon billboard", "medieval setting conflicts with neon billboard unless intentionally anachronistic"),
]

CAMERA_CONFLICTS = [
    ("macro close-up", "wide establishing shot", "macro close-up conflicts with wide establishing shot"),
    ("extreme close-up", "full body wide shot", "extreme close-up conflicts with full-body wide shot"),
]

MJ_VALUE_PARAMS = {
    "--ar",
    "--aspect",
    "--chaos",
    "--quality",
    "--q",
    "--seed",
    "--stylize",
    "--s",
    "--weird",
    "--w",
    "--style",
    "--v",
    "--version",
    "--sref",
    "--cref",
    "--cw",
}
MJ_FLAG_PARAMS = {"--raw", "--turbo", "--fast", "--relax", "--niji"}


@dataclass
class SectionQuality:
    present: bool
    valid: bool
    word_count: int = 0
    reason: str = ""


@dataclass
class MidjourneyParse:
    prompt_text: str
    params: list[str]
    trailing_text: str
    critical: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class LintResult:
    architecture: str
    model: str
    word_count: int
    score: int
    coverage: dict[str, bool]
    section_quality: dict[str, dict[str, object]] = field(default_factory=dict)
    model_policy: dict[str, object] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    critical: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    @property
    def critical_failures(self) -> list[str]:
        return self.critical


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def canonical_heading(raw: str) -> str:
    value = normalize(raw)
    value = re.sub(r"\b(layer|system|block|层|系统)\b", "", value).strip()
    return value.replace("&", "and")


def parse_sections(text: str) -> dict[str, str]:
    heading_re = re.compile(r"^\s*(?:#+\s*)?(?:\[|【)([^]\】\n]+)(?:\]|】)\s*$", re.M)
    matches = list(heading_re.finditer(text))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[canonical_heading(match.group(1))] = text[start:end].strip()
    return sections


def has_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def concrete_noun_count(text: str) -> int:
    haystack = normalize(text)
    return sum(1 for noun in CONCRETE_NOUNS if re.search(rf"\b{re.escape(noun)}\b", haystack))


def generic_filler_hits(text: str) -> list[str]:
    haystack = normalize(text)
    return sorted(term for term in GENERIC_FILLER if term in haystack)


def section_is_valid(content: str) -> SectionQuality:
    words = re.findall(r"\S+", content)
    if PLACEHOLDER_RE.match(content):
        return SectionQuality(True, False, len(words), "empty or placeholder content")
    if len(words) < 4:
        return SectionQuality(True, False, len(words), "section is too short")
    filler_hits = generic_filler_hits(content)
    if len(filler_hits) >= 3 and concrete_noun_count(content) == 0:
        return SectionQuality(True, False, len(words), "filler-only section")
    return SectionQuality(True, True, len(words), "")


def section_for_key(sections: dict[str, str], key: str, patterns: Iterable[str]) -> tuple[str | None, str | None]:
    for name, content in sections.items():
        key_terms = [key.replace("_", " "), *patterns]
        if any(re.search(pattern, name, flags=re.I) for pattern in key_terms):
            return name, content
    return None, None


def requirements_for(architecture: str) -> dict[str, list[str]]:
    if architecture == "seven-layer":
        return SEVEN_REQUIRED
    if architecture == "system":
        return SYSTEM_REQUIRED
    return COMPACT_REQUIRED


def coverage_for(text: str, architecture: str) -> tuple[dict[str, bool], dict[str, SectionQuality]]:
    haystack = normalize(text)
    sections = parse_sections(text)
    required = requirements_for(architecture)
    coverage: dict[str, bool] = {}
    section_quality: dict[str, SectionQuality] = {}

    for key, patterns in required.items():
        section_name, section_content = section_for_key(sections, key, patterns)
        if section_name is not None and section_content is not None:
            quality = section_is_valid(section_content)
            section_quality[key] = quality
            coverage[key] = quality.valid
        else:
            section_quality[key] = SectionQuality(False, False, 0, "no matching section")
            coverage[key] = has_any(haystack, patterns)

    return coverage, section_quality


def infer_architecture(text: str) -> str:
    if re.search(r"--(?:ar|stylize|chaos|seed|raw|quality|no)\b", text, flags=re.I):
        return "compact"
    seven, _ = coverage_for(text, "seven-layer")
    system, _ = coverage_for(text, "system")
    return "system" if sum(system.values()) > sum(seven.values()) else "seven-layer"


def check_generic_filler(text: str) -> list[str]:
    hits = generic_filler_hits(text)
    if len(hits) >= 4 and concrete_noun_count(text) < 4:
        return [f"Too much generic filler ({', '.join(hits)}) without enough concrete visual nouns."]
    return []


def check_conflicts(text: str) -> list[str]:
    haystack = normalize(text)
    warnings = []
    for left, right, message in STYLE_CONFLICTS + ERA_CONFLICTS + CAMERA_CONFLICTS:
        if left in haystack and right in haystack:
            warnings.append(message)
    return warnings


def parse_midjourney_params(text: str) -> MidjourneyParse:
    tokens = re.findall(r"\S+", text)
    first_param_idx = next((i for i, token in enumerate(tokens) if token.startswith("--")), None)
    if first_param_idx is None:
        return MidjourneyParse(prompt_text=text.strip(), params=[], trailing_text="")

    critical: list[str] = []
    warnings: list[str] = []
    prompt_text = " ".join(tokens[:first_param_idx])
    params: list[str] = []
    trailing: list[str] = []
    idx = first_param_idx

    while idx < len(tokens):
        token = tokens[idx]
        if not token.startswith("--"):
            trailing = tokens[idx:]
            break
        param = token.rstrip(".,;:")
        params.append(param)
        if token != param:
            critical.append(f"Midjourney parameter {param} has trailing punctuation.")

        if param == "--no":
            values = []
            idx += 1
            while idx < len(tokens) and not tokens[idx].startswith("--"):
                values.append(tokens[idx])
                idx += 1
            if not values:
                critical.append("Midjourney --no is missing exclusion values.")
            elif len(values) >= 2 and "," not in " ".join(values):
                warnings.append("Midjourney --no multiword exclusions should be comma-separated or expressed positively.")
            continue

        if param in MJ_VALUE_PARAMS:
            idx += 1
            if idx >= len(tokens) or tokens[idx].startswith("--"):
                critical.append(f"Midjourney parameter {param} is missing a value.")
            else:
                idx += 1
            continue

        if param in MJ_FLAG_PARAMS:
            idx += 1
            continue

        warnings.append(f"Unknown Midjourney parameter: {param}")
        idx += 1

    if trailing:
        critical.append("Midjourney parameters must be a contiguous block at the end; trailing prose found after parameters.")

    return MidjourneyParse(prompt_text=prompt_text, params=params, trailing_text=" ".join(trailing), critical=critical, warnings=warnings)


def malformed_hex_codes(text: str) -> list[str]:
    return [code for code in re.findall(r"#[0-9A-Za-z]+", text) if not re.fullmatch(r"#[0-9a-fA-F]{6}", code)]


def check_model_policy(text: str, model: str) -> tuple[list[str], list[str], dict[str, object]]:
    haystack = normalize(text)
    critical: list[str] = []
    warnings: list[str] = []
    policy: dict[str, object] = {}
    has_negative_block = "negative prompt" in haystack or re.search(r"^\s*(negative|avoid)\s*:", text, flags=re.I | re.M)

    if model == "midjourney":
        parsed = parse_midjourney_params(text)
        policy["midjourney_params"] = parsed.params
        policy["trailing_after_params"] = parsed.trailing_text
        critical.extend(parsed.critical)
        warnings.extend(parsed.warnings)
        if has_negative_block:
            critical.append("Midjourney should use --no at the end instead of a separate Negative Prompt block.")
    elif model == "flux":
        bad_hex = malformed_hex_codes(text)
        policy["malformed_hex_codes"] = bad_hex
        if has_negative_block or "--no" in haystack:
            critical.append("FLUX: prefer positive replacement language; most FLUX models do not support negative prompts.")
        if bad_hex:
            critical.append(f"FLUX color steering has malformed hex code(s): {', '.join(bad_hex)}.")
    elif model == "gpt-image":
        filler_hits = generic_filler_hits(text)
        policy["generic_filler_hits"] = filler_hits
        if len(filler_hits) >= 5:
            warnings.append("GPT Image: reduce keyword pile and express priorities in natural language.")
    elif model == "stable-diffusion":
        if "--no" in haystack:
            warnings.append("Stable Diffusion wrappers usually use a negative prompt field, not Midjourney --no.")
    return critical, warnings, policy


def score_result(coverage: dict[str, bool], critical: list[str], warnings: list[str]) -> int:
    base = round(10 * sum(coverage.values()) / max(1, len(coverage)))
    penalty = min(6, (2 * len(critical)) + len(warnings))
    return max(0, base - penalty)


def lint(text: str, architecture: str, model: str) -> LintResult:
    if architecture == "auto":
        architecture = infer_architecture(text)

    coverage, section_quality_raw = coverage_for(text, architecture)
    section_quality = {key: asdict(value) for key, value in section_quality_raw.items()}
    missing = [key for key, present in coverage.items() if not present]
    critical: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []
    word_count = len(re.findall(r"\S+", text))

    if missing:
        warnings.append(f"Missing controls: {', '.join(missing)}")
        suggestions.extend([f"Add concrete {item.replace('_', ' ')} control." for item in missing[:5]])

    invalid_sections = [
        f"{key}: {quality.reason}"
        for key, quality in section_quality_raw.items()
        if quality.present and not quality.valid
    ]
    if invalid_sections:
        critical.append(f"Section content is empty, placeholder, or too weak: {'; '.join(invalid_sections)}")

    if architecture == "system":
        missing_series_controls = [item for item in ("continuity", "variation_budget", "shot_slots") if item in missing]
        if missing_series_controls:
            critical.append(f"System prompts must include series controls: {', '.join(missing_series_controls)}")
    if architecture == "seven-layer" and "output_constraints" in missing:
        suggestions.append("Add a separate Output Constraints block for aspect ratio, exact text, and avoid/replacement strategy.")

    warnings.extend(check_generic_filler(text))
    warnings.extend(check_conflicts(text))
    model_critical, model_warnings, model_policy = check_model_policy(text, model)
    critical.extend(model_critical)
    warnings.extend(model_warnings)

    if model == "midjourney":
        suggestions.append("Place Midjourney parameters at the end and convert exclusions to --no.")
    if model == "flux":
        suggestions.append("Rewrite avoid/negative ideas as positive replacements for FLUX.")

    critical_missing = len(missing) >= (4 if architecture == "seven-layer" else 6 if architecture == "system" else 3)
    if critical_missing:
        critical.insert(0, "Too many required controls are missing.")

    return LintResult(
        architecture=architecture,
        model=model,
        word_count=word_count,
        score=score_result(coverage, critical, warnings),
        coverage=coverage,
        section_quality=section_quality,
        model_policy=model_policy,
        missing=missing,
        critical=critical,
        warnings=warnings,
        suggestions=sorted(set(suggestions)),
    )


def print_text(result: LintResult) -> None:
    print(f"Architecture: {result.architecture}")
    print(f"Model: {result.model}")
    print(f"Approx words/tokens: {result.word_count}")
    print(f"Score: {result.score}/10")
    present = [key for key, value in result.coverage.items() if value]
    print(f"Coverage: {len(present)}/{len(result.coverage)} ({', '.join(present) or 'none'})")
    if result.missing:
        print(f"Missing: {', '.join(result.missing)}")
    if result.critical:
        print("Critical:")
        for item in result.critical:
            print(f"- {item}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"- {warning}")
    if result.suggestions:
        print("Suggestions:")
        for suggestion in result.suggestions:
            print(f"- {suggestion}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint an image prompt for structure and model fit.")
    parser.add_argument("prompt_file", type=Path, help="Text file containing a prompt")
    parser.add_argument("--architecture", choices=["auto", "seven-layer", "system", "compact"], default="auto")
    parser.add_argument(
        "--model",
        choices=["generic", "gpt-image", "midjourney", "flux", "grok", "dreamina", "stable-diffusion"],
        default="generic",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--strict", action="store_true", help="Return nonzero for critical failures.")
    args = parser.parse_args()

    text = args.prompt_file.read_text(encoding="utf-8")
    result = lint(text, args.architecture, args.model)

    if args.format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_text(result)

    if args.strict and result.critical:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
