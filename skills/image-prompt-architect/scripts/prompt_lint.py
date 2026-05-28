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
    "output_constraints": [r"output constraints", r"aspect ratio", r"must avoid", r"must include", r"分辨率", r"比例"],
}

SYSTEM_REQUIRED = {
    "premise": [r"premise system", r"前提系统", r"series of", r"a set of"],
    "spatial": [r"spatial system", r"空间系统"],
    "character": [r"character system", r"人物系统"],
    "color": [r"color system", r"色彩系统"],
    "medium": [r"medium system", r"介质系统"],
    "composition": [r"composition system", r"构图系统"],
    "lighting": [r"lighting", r"atmosphere", r"光影"],
    "narrative": [r"narrative", r"emotion", r"叙事", r"情绪"],
    "quality_exclusion": [r"quality", r"exclusion", r"avoid", r"禁止", r"排除"],
    "continuity": [r"continuity", r"连续性", r"must remain fixed"],
    "variation_budget": [r"variation budget", r"变化预算", r"may change"],
    "shot_slots": [r"shot slot", r"frame 01", r"per-shot", r"分镜"],
}

COMPACT_REQUIRED = {
    "subject": [r"subject", r"person", r"character", r"product", r"singer", r"object"],
    "setting": [r"setting", r"club", r"room", r"street", r"landscape", r"studio", r"background"],
    "visual_style": [r"style", r"cinematic", r"film", r"noir", r"editorial", r"photo", r"illustration"],
    "camera_or_composition": [r"camera", r"lens", r"shot", r"composition", r"35mm", r"85mm", r"foreground"],
    "lighting_or_mood": [r"light", r"lamp", r"shadow", r"mood", r"melancholy", r"atmosphere", r"smoky"],
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


@dataclass
class LintResult:
    architecture: str
    model: str
    word_count: int
    score: int
    coverage: dict[str, bool]
    missing: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    @property
    def critical_failures(self) -> list[str]:
        return [w for w in self.warnings if w.startswith("CRITICAL:")]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def parse_headings(text: str) -> set[str]:
    headings = set()
    for match in re.finditer(r"^\s*(?:#+\s*)?(?:\[|【)?([A-Za-z0-9 _/&-]+|[\u4e00-\u9fffA-Za-z0-9 _/&-]+)(?:\]|】)?\s*$", text, flags=re.M):
        value = normalize(match.group(1))
        if len(value) <= 80:
            headings.add(value)
    return headings


def has_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def coverage_for(text: str, architecture: str) -> dict[str, bool]:
    haystack = normalize(text)
    headings = parse_headings(text)
    if architecture == "seven-layer":
        required = SEVEN_REQUIRED
    elif architecture == "system":
        required = SYSTEM_REQUIRED
    else:
        required = COMPACT_REQUIRED
    coverage = {}
    for key, patterns in required.items():
        heading_hit = any(key.replace("_", " ") in h or any(re.search(p, h, flags=re.I) for p in patterns) for h in headings)
        coverage[key] = heading_hit or has_any(haystack, patterns)
    return coverage


def infer_architecture(text: str) -> str:
    if re.search(r"--(?:ar|stylize|chaos|seed|raw|quality|no)\b", text, flags=re.I):
        return "compact"
    seven = coverage_for(text, "seven-layer")
    system = coverage_for(text, "system")
    return "system" if sum(system.values()) > sum(seven.values()) else "seven-layer"


def check_generic_filler(text: str) -> list[str]:
    haystack = normalize(text)
    hits = [term for term in GENERIC_FILLER if term in haystack]
    concrete_nouns = re.findall(
        r"\b(?:silk|brass|chrome|cobblestone|rain|window|lens|shadow|neon|paper|wood|stone|cotton|glass|street|room|product|label|poster|book|train|school|river)\b",
        haystack,
    )
    if len(hits) >= 4 and len(concrete_nouns) < 4:
        return [f"Too much generic filler ({', '.join(sorted(hits))}) without enough concrete visual nouns."]
    return []


def check_conflicts(text: str) -> list[str]:
    haystack = normalize(text)
    warnings = []
    for left, right, message in STYLE_CONFLICTS + ERA_CONFLICTS + CAMERA_CONFLICTS:
        if left in haystack and right in haystack:
            warnings.append(message)
    return warnings


def check_model_policy(text: str, model: str) -> list[str]:
    haystack = normalize(text)
    warnings = []
    has_negative_block = "negative prompt" in haystack or re.search(r"^\s*(negative|avoid)\s*:", text, flags=re.I | re.M)

    if model == "midjourney":
        params = list(re.finditer(r"--[a-zA-Z]+", text))
        if params:
            last_param_start = params[0].start()
            after = text[last_param_start:]
            if re.search(r"--[a-zA-Z]+[^\\n]*(?:,|\.)\s*$", after):
                warnings.append("Midjourney parameters should not end with punctuation.")
        if has_negative_block:
            warnings.append("Midjourney should use --no at the end instead of a separate Negative Prompt block.")
        if "--no" in haystack and re.search(r"--no\s+\w+\s+\w+", haystack) and "," not in haystack.split("--no", 1)[1]:
            warnings.append("Midjourney --no parses terms independently; comma-separate exclusions and prefer positive alternatives for phrases.")
    elif model == "flux":
        if has_negative_block or "--no" in haystack:
            warnings.append("FLUX: prefer positive replacement language; most FLUX models do not support negative prompts.")
        if "#" in text and not re.search(r"#[0-9a-fA-F]{6}\b", text):
            warnings.append("FLUX color steering should use valid six-digit hex colors.")
    elif model == "gpt-image":
        filler_hits = [term for term in GENERIC_FILLER if term in haystack]
        if len(filler_hits) >= 5:
            warnings.append("GPT Image: reduce keyword pile and express priorities in natural language.")
    elif model == "stable-diffusion":
        if "--no" in haystack:
            warnings.append("Stable Diffusion wrappers usually use a negative prompt field, not Midjourney --no.")
    return warnings


def score_result(coverage: dict[str, bool], warnings: list[str]) -> int:
    base = round(10 * sum(coverage.values()) / max(1, len(coverage)))
    penalty = min(4, len(warnings))
    return max(0, base - penalty)


def lint(text: str, architecture: str, model: str) -> LintResult:
    if architecture == "auto":
        architecture = infer_architecture(text)

    coverage = coverage_for(text, architecture)
    missing = [key for key, present in coverage.items() if not present]
    warnings: list[str] = []
    suggestions: list[str] = []
    word_count = len(re.findall(r"\S+", text))

    if missing:
        warnings.append(f"Missing controls: {', '.join(missing)}")
        suggestions.extend([f"Add concrete {item.replace('_', ' ')} control." for item in missing[:5]])

    warnings.extend(check_generic_filler(text))
    warnings.extend(check_conflicts(text))
    warnings.extend(check_model_policy(text, model))

    if architecture == "seven-layer" and not coverage.get("output_constraints", False):
        suggestions.append("Add a separate Output Constraints block for aspect ratio, exact text, and must-avoid items.")
    if architecture == "system":
        for item in ("continuity", "variation_budget", "shot_slots"):
            if item in missing:
                suggestions.append(f"Series prompts need {item.replace('_', ' ')}.")
    if model == "midjourney":
        suggestions.append("Place Midjourney parameters at the end and convert exclusions to --no.")
    if model == "flux":
        suggestions.append("Rewrite avoid/negative ideas as positive replacements for FLUX.")

    critical_missing = len(missing) >= (4 if architecture == "seven-layer" else 6 if architecture == "system" else 3)
    if critical_missing:
        warnings.insert(0, "CRITICAL: Too many required controls are missing.")

    return LintResult(
        architecture=architecture,
        model=model,
        word_count=word_count,
        score=score_result(coverage, warnings),
        coverage=coverage,
        missing=missing,
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

    if args.strict and result.critical_failures:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
