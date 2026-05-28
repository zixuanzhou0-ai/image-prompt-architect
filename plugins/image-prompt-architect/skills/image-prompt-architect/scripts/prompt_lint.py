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
    "subject": [r"person", r"character", r"product", r"object", r"woman", r"man", r"人物", r"一位", r"产品"],
    "environment": [r"location", r"street", r"room", r"landscape", r"background", r"club", r"kitchen", r"forest", r"city", r"老街", r"房间"],
    "lighting": [r"sunlight", r"moonlight", r"neon", r"volumetric", r"backlit", r"softbox", r"rim light", r"overcast", r"光线", r"逆光"],
    "material": [r"texture", r"silk", r"metal", r"glass", r"stone", r"grain", r"reflection", r"ceramic", r"brass", r"材质", r"纹理"],
    "composition": [r"camera", r"lens", r"shot", r"framing", r"depth of field", r"bokeh", r"35mm", r"50mm", r"构图", r"镜头"],
    "style": [r"cinematic", r"film", r"illustration", r"render", r"editorial", r"noir", r"documentary", r"电影感", r"胶片"],
    "context_tone": [r"emotion", r"narrative", r"nostalgia", r"melancholy", r"loneliness", r"restrained", r"情绪", r"叙事", r"克制"],
    "output_constraints": [r"aspect ratio", r"avoid / replacement", r"must include", r"exactly", r"--ar", r"分辨率", r"比例", r"避免"],
}

SEVEN_SECTION_ALIASES = {
    "subject": [r"subject", r"主体", r"人物", r"对象"],
    "environment": [r"environment", r"setting", r"spatial", r"环境", r"空间", r"场景"],
    "lighting": [r"lighting", r"atmosphere", r"光影", r"氛围"],
    "material": [r"material", r"texture", r"材质", r"纹理"],
    "composition": [r"composition", r"camera", r"构图", r"镜头"],
    "style": [r"style", r"medium", r"风格", r"介质"],
    "context_tone": [r"context", r"intent", r"tone", r"语感", r"内涵", r"情绪"],
    "output_constraints": [r"output constraints", r"constraints", r"输出", r"限制", r"约束"],
}

SYSTEM_REQUIRED = {
    "premise": [r"series of", r"a set of", r"film stills", r"visual bible", r"系列", r"套图"],
    "identity_lock": [r"must never change", r"same face", r"same costume", r"identity drift", r"身份锁定", r"不漂移"],
    "continuity": [r"must remain fixed", r"continuity", r"fixed anchors", r"保持一致", r"连续性"],
    "variation_budget": [r"may change", r"limit each frame", r"variation", r"变化预算", r"每帧"],
    "spatial": [r"reservoir", r"street", r"school", r"bus", r"village", r"landscape", r"空间", r"地点"],
    "character": [r"student", r"character", r"gesture", r"costume", r"人物", r"表情", r"动作"],
    "color": [r"cobalt", r"cyan", r"palette", r"color", r"shadow", r"色彩", r"调色"],
    "medium": [r"35mm", r"film", r"telecine", r"grain", r"scan", r"介质", r"胶片"],
    "composition": [r"wide", r"frame", r"lens", r"negative space", r"composition", r"构图", r"镜头"],
    "lighting": [r"overcast", r"sunset", r"reflection", r"haze", r"light", r"光影", r"氛围"],
    "narrative": [r"narrative", r"emotion", r"confession", r"hesitation", r"叙事", r"情绪"],
    "quality_exclusion": [r"no modern", r"avoid", r"exclusion", r"forbidden", r"禁止", r"排除"],
    "shot_slots": [r"frame 01", r"frame 02", r"per-shot", r"shot", r"分镜"],
}

SYSTEM_SECTION_ALIASES = {
    "premise": [r"premise", r"前提"],
    "identity_lock": [r"identity lock", r"身份锁定"],
    "continuity": [r"continuity", r"连续性"],
    "variation_budget": [r"variation budget", r"变化预算"],
    "spatial": [r"spatial", r"空间"],
    "character": [r"character", r"人物"],
    "color": [r"color", r"palette", r"色彩"],
    "medium": [r"medium", r"介质"],
    "composition": [r"composition", r"构图"],
    "lighting": [r"lighting", r"atmosphere", r"光影", r"氛围"],
    "narrative": [r"narrative", r"emotion", r"叙事", r"情绪"],
    "quality_exclusion": [r"quality", r"exclusion", r"avoid", r"质量", r"排除"],
    "shot_slots": [r"shot slots?", r"frame", r"分镜"],
}

COMPACT_REQUIRED = {
    "subject": [r"subject", r"person", r"character", r"product", r"singer", r"object", r"人物", r"一位", r"男人", r"女人", r"老板", r"产品", r"护肤品", r"玻璃瓶", r"海报"],
    "setting": [r"setting", r"club", r"room", r"street", r"landscape", r"studio", r"background", r"老街", r"江南", r"雨后", r"木门", r"城市", r"街角", r"台面", r"背景", r"工作室"],
    "visual_style": [r"style", r"cinematic", r"film", r"noir", r"editorial", r"photo", r"illustration", r"电影感", r"人像", r"复古", r"产品摄影", r"极简"],
    "camera_or_composition": [r"camera", r"lens", r"shot", r"composition", r"35mm", r"50mm", r"85mm", r"foreground", r"portrait", r"构图", r"版式", r"居中", r"网格"],
    "lighting_or_mood": [r"light", r"lamp", r"shadow", r"mood", r"melancholy", r"atmosphere", r"smoky", r"overcast", r"克制", r"光", r"柔光", r"柔光箱", r"窗光", r"橱窗光"],
}

COMPACT_SECTION_ALIASES = {
    "subject": [r"subject", r"主体", r"人物"],
    "setting": [r"setting", r"environment", r"场景", r"环境"],
    "visual_style": [r"visual style", r"style", r"风格"],
    "camera_or_composition": [r"camera", r"composition", r"构图", r"镜头"],
    "lighting_or_mood": [r"lighting", r"mood", r"atmosphere", r"光影", r"情绪", r"氛围"],
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
    "高级感",
    "电影感",
    "大片",
    "好看",
    "漂亮",
    "精美",
    "大师作品",
    "质感",
    "高级",
    "氛围感",
    "神图",
    "超清",
    "细节丰富",
    "商业大片",
    "高端大气",
    "视觉冲击",
    "爆款",
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
    "书店",
    "老街",
    "青石板",
    "旧书",
    "木门",
    "棉麻",
    "长衫",
    "雨",
    "窗",
    "石板",
    "手表",
    "表盘",
    "海报",
    "标题",
    "产品",
    "玻璃瓶",
    "泵头",
    "纸张",
    "列车",
    "站台",
    "窗户",
    "雨巷",
    "香水瓶",
    "金属盖",
    "包装盒",
    "货架",
    "霓虹灯",
    "飞船",
    "舱门",
    "机器人",
    "绘本",
    "蜡笔",
    "屋顶",
    "楼梯",
    "海报纸",
    "字体",
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
    "--bs",
    "--chaos",
    "--c",
    "--end",
    "--iw",
    "--motion",
    "--oref",
    "--profile",
    "--p",
    "--quality",
    "--q",
    "--repeat",
    "--r",
    "--seed",
    "--sref",
    "--stylize",
    "--s",
    "--sv",
    "--sw",
    "--weird",
    "--w",
    "--v",
    "--version",
}
MJ_LEGACY_VALUE_PARAMS = {"--cref", "--cw", "--style"}
MJ_FLAG_PARAMS = {
    "--raw",
    "--turbo",
    "--fast",
    "--relax",
    "--niji",
    "--stealth",
    "--tile",
    "--public",
    "--draft",
    "--loop",
    "--video",
}
FLUX_NEGATION_RE = re.compile(r"\b(?:no|without|not|avoid)\s+[^,.;\n]+", re.I)
FLUX_SOFT_NEGATION_RE = re.compile(r"\b(?:not|no)\s+(?:overly|too|excessively)\s+[^,.;\n]+", re.I)


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
    heading_re = re.compile(
        r"^\s*(?:(?:#+\s*)?(?:\[|【)([^]\】\n]+)(?:\]|】)|#{1,6}\s+([^:\n]+?)\s*$|([^:\n]{0,80}?(?:Layer|System|层|系统|Constraints|Prompt|主体|环境|光影|材质|构图|风格|语感|内涵|输出|约束|限制))\s*[:：]\s*)$",
        re.M,
    )
    matches = list(heading_re.finditer(text))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        heading = next(group for group in match.groups() if group)
        sections[canonical_heading(heading)] = text[start:end].strip()
    return sections


def has_any(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.I) for pattern in patterns)


def concrete_noun_count(text: str) -> int:
    haystack = normalize(text)
    return sum(1 for noun in CONCRETE_NOUNS if re.search(rf"\b{re.escape(noun)}\b", haystack))


def generic_filler_hits(text: str) -> list[str]:
    haystack = normalize(text)
    return sorted(term for term in GENERIC_FILLER if term in haystack)


def content_units(text: str) -> int:
    latin_tokens = re.findall(r"[A-Za-z0-9#:/.-]+", text)
    cjk_chars = re.findall(r"[\u4e00-\u9fff]", text)
    return len(latin_tokens) + (len(cjk_chars) // 2)


def section_is_valid(content: str) -> SectionQuality:
    units = content_units(content)
    if PLACEHOLDER_RE.match(content):
        return SectionQuality(True, False, units, "empty or placeholder content")
    if units < 4:
        return SectionQuality(True, False, units, "section is too short")
    filler_hits = generic_filler_hits(content)
    if len(filler_hits) >= 3 and concrete_noun_count(content) == 0:
        return SectionQuality(True, False, units, "filler-only section")
    return SectionQuality(True, True, units, "")


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


def section_aliases_for(architecture: str) -> dict[str, list[str]]:
    if architecture == "seven-layer":
        return SEVEN_SECTION_ALIASES
    if architecture == "system":
        return SYSTEM_SECTION_ALIASES
    return COMPACT_SECTION_ALIASES


def coverage_for(text: str, architecture: str) -> tuple[dict[str, bool], dict[str, SectionQuality]]:
    haystack = normalize(text)
    sections = parse_sections(text)
    required = requirements_for(architecture)
    aliases = section_aliases_for(architecture)
    coverage: dict[str, bool] = {}
    section_quality: dict[str, SectionQuality] = {}

    for key, patterns in required.items():
        section_name, section_content = section_for_key(sections, key, aliases.get(key, patterns))
        if section_name is not None and section_content is not None:
            quality = section_is_valid(section_content)
            section_quality[key] = quality
            coverage[key] = quality.valid
        else:
            section_quality[key] = SectionQuality(False, False, 0, "no matching section")
            if architecture in {"seven-layer", "system"} and not sections:
                coverage[key] = has_any(haystack, patterns)
            elif architecture == "compact":
                coverage[key] = has_any(haystack, patterns)
            else:
                coverage[key] = False

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


def parse_midjourney_params(text: str, strict_model_params: bool = False) -> MidjourneyParse:
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

        if param in MJ_VALUE_PARAMS or param in MJ_LEGACY_VALUE_PARAMS:
            if param in MJ_LEGACY_VALUE_PARAMS:
                warnings.append(f"Legacy or deprecated Midjourney parameter: {param}")
            idx += 1
            if idx >= len(tokens) or tokens[idx].startswith("--"):
                critical.append(f"Midjourney parameter {param} is missing a value.")
            else:
                value = tokens[idx]
                if value != value.rstrip(".,;:"):
                    critical.append(f"Midjourney parameter {param} value has trailing punctuation.")
                idx += 1
            continue

        if param in MJ_FLAG_PARAMS:
            idx += 1
            continue

        message = f"Unknown Midjourney parameter: {param}"
        if strict_model_params:
            critical.append(message)
        else:
            warnings.append(message)
        idx += 1
        if idx < len(tokens) and not tokens[idx].startswith("--"):
            idx += 1

    if trailing:
        critical.append("Midjourney parameters must be a contiguous block at the end; trailing prose found after parameters.")

    return MidjourneyParse(prompt_text=prompt_text, params=params, trailing_text=" ".join(trailing), critical=critical, warnings=warnings)


def malformed_hex_codes(text: str) -> list[str]:
    return [code for code in re.findall(r"#[0-9A-Za-z]+", text) if not re.fullmatch(r"#[0-9a-fA-F]{6}", code)]


def gpt_image_needs_quoted_text(text: str) -> bool:
    haystack = normalize(text)
    if any(term in haystack for term in ("空白标签", "无字标签", "未标记包装")):
        return False
    if any(term in haystack for term in ("招牌写着", "标题", "文字", "字样", "logo写着", "标签写着")):
        return True
    label_or_logo = re.search(r"\b(label|logo)\b", haystack)
    label_text_cue = re.search(r"\b(read|reads|says|with the words|exactly)\b", haystack)
    if label_or_logo and label_text_cue:
        return True
    if any(term in haystack for term in ("headline", "sign", "text", "typography", "wording", "copy")):
        return True
    if any(term in haystack for term in ("blank label", "white label", "unmarked label")):
        return False
    return False


def check_model_policy(text: str, model: str, strict_model_params: bool = False) -> tuple[list[str], list[str], dict[str, object]]:
    haystack = normalize(text)
    critical: list[str] = []
    warnings: list[str] = []
    policy: dict[str, object] = {}
    has_negative_block = "negative prompt" in haystack or re.search(r"^\s*(negative|avoid)\s*:", text, flags=re.I | re.M)

    if model == "midjourney":
        parsed = parse_midjourney_params(text, strict_model_params)
        policy["midjourney_params"] = parsed.params
        policy["trailing_after_params"] = parsed.trailing_text
        critical.extend(parsed.critical)
        warnings.extend(parsed.warnings)
        if has_negative_block:
            critical.append("Midjourney should use --no at the end instead of a separate Negative Prompt block.")
    elif model == "flux":
        bad_hex = malformed_hex_codes(text)
        negation_hits = FLUX_NEGATION_RE.findall(text)
        soft_negation_hits = FLUX_SOFT_NEGATION_RE.findall(text)
        object_negation_hits = [hit for hit in negation_hits if hit not in soft_negation_hits]
        policy["malformed_hex_codes"] = bad_hex
        policy["plain_negation_phrases"] = negation_hits
        policy["soft_negation_phrases"] = soft_negation_hits
        policy["object_negation_phrases"] = object_negation_hits
        if has_negative_block or "--no" in haystack:
            critical.append("FLUX: prefer positive replacement language; most FLUX models do not support negative prompts.")
        if len(object_negation_hits) >= 2:
            critical.append(f"FLUX prompt uses multiple object-exclusion negation phrases; rewrite as positive replacements: {', '.join(object_negation_hits)}.")
        elif object_negation_hits:
            warnings.append(f"FLUX prompt uses plain negation; prefer a positive replacement: {', '.join(object_negation_hits)}.")
        if soft_negation_hits:
            warnings.append(f"FLUX prompt uses soft modifier negation; positive wording is still safer: {', '.join(soft_negation_hits)}.")
        if bad_hex:
            critical.append(f"FLUX color steering has malformed hex code(s): {', '.join(bad_hex)}.")
    elif model == "gpt-image":
        filler_hits = generic_filler_hits(text)
        policy["generic_filler_hits"] = filler_hits
        if len(filler_hits) >= 5:
            warnings.append("GPT Image: reduce keyword pile and express priorities in natural language.")
        if any(term in haystack for term in ("edit", "replace", "remove", "change")) and not any(term in haystack for term in ("preserve", "keep", "only", "unchanged")):
            warnings.append("GPT Image edit prompts should separate preserve/change instructions.")
        if gpt_image_needs_quoted_text(text) and not re.search(r'"[^"]+"|“[^”]+”', text):
            warnings.append("GPT Image text-rendering prompts should quote exact text.")
        if "pixel-perfect" in haystack or "guarantee exact reproduction" in haystack:
            warnings.append("GPT Image prompts should not promise pixel-perfect or guaranteed exact reproduction.")
        if "reference image" in haystack and not any(term in haystack for term in ("controls", "for identity", "for style", "for composition", "for palette")):
            warnings.append("GPT Image reference-image prompts should assign each reference image a role.")
    elif model == "grok":
        if "reference image" in haystack and not any(term in haystack for term in ("for identity", "for style", "for composition", "for palette")):
            warnings.append("Grok reference-image prompts should assign whether the reference controls identity, style, composition, or palette.")
    elif model == "stable-diffusion":
        if "--no" in haystack:
            warnings.append("Stable Diffusion wrappers usually use a negative prompt field, not Midjourney --no.")
    return critical, warnings, policy


def score_result(coverage: dict[str, bool], critical: list[str], warnings: list[str]) -> int:
    base = round(10 * sum(coverage.values()) / max(1, len(coverage)))
    penalty = min(6, (2 * len(critical)) + len(warnings))
    return max(0, base - penalty)


def lint(text: str, architecture: str, model: str, strict_model_params: bool = False) -> LintResult:
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
    model_critical, model_warnings, model_policy = check_model_policy(text, model, strict_model_params)
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
    parser.add_argument(
        "--strict-model-params",
        action="store_true",
        help="Treat unknown model-specific parameters as critical failures where supported.",
    )
    args = parser.parse_args()

    text = args.prompt_file.read_text(encoding="utf-8")
    result = lint(text, args.architecture, args.model, args.strict_model_params)

    if args.format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print_text(result)

    if args.strict and result.critical:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
