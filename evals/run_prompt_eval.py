#!/usr/bin/env python3
"""Generate a lightweight prompt-level eval report.

This intentionally avoids a YAML dependency and only parses the simple
`evals/prompt_cases.yml` structure used by this repository.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_FILE = ROOT / "evals" / "prompt_cases.yml"
REPORT_FILE = ROOT / "evals" / "report.md"
SKILL_OUTPUTS_FILE = ROOT / "evals" / "skill_outputs.json"
LINTER_FILE = ROOT / "skills" / "image-prompt-architect" / "scripts" / "prompt_lint.py"

FEATURE_SYNONYMS = {
    "specific subject": ["24-year-old", "woman", "hiker", "product", "bottle", "watch", "书店老板"],
    "lighting source": ["light", "glow", "sunlight", "softbox", "lamp", "window", "柔光"],
    "concrete lighting": ["light", "glow", "sunlight", "softbox", "lamp", "window", "柔光"],
    "lighting": ["light", "glow", "sunlight", "softbox", "lamp", "window", "柔光"],
    "lighting constraints": ["light", "polarizing", "reflection", "softbox", "rim"],
    "camera": ["camera", "lens", "35mm", "50mm", "80mm", "portrait", "人像"],
    "mood": ["mood", "melancholy", "calm", "restrained", "loneliness", "克制", "安静"],
    "concrete setting": ["street", "landscape", "studio", "mountain", "club", "江南", "老街"],
    "concrete material": ["ceramic", "walnut", "glass", "steel", "stone", "paper", "棉麻"],
    "material": ["ceramic", "walnut", "glass", "steel", "stone", "paper", "棉麻"],
    "material geometry": ["steel", "glass", "case", "sapphire", "stone", "dial"],
    "positive replacements": ["empty", "vehicle-free", "peaceful", "solitary", "uncluttered", "unmarked", "clean"],
    "positive replacements for negation": ["empty", "vehicle-free", "peaceful", "solitary", "uncluttered", "unmarked", "clean"],
    "valid hex color": ["#"],
    "hex color": ["#"],
    "typography": ["headline", "footer", "layout", "poster"],
    "layout": ["layout", "grid", "centered", "composition", "margins"],
    "palette": ["palette", "navy", "ivory", "teal", "amber"],
    "reference role remains parameterized": ["--oref", "--profile", "--iw"],
    "lighting/composition added": ["light", "lens", "composition", "centered"],
    "specific cultural setting": ["江南", "老街", "书店", "青石板"],
    "reference role assignment": ["identity only", "reference image"],
    "setting": ["street", "landscape", "studio", "mountain", "club", "江南", "老街"],
    "continuity anchors": ["continuity", "anchors", "train-window"],
}


def load_linter():
    spec = importlib.util.spec_from_file_location("prompt_lint", LINTER_FILE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules["prompt_lint"] = module
    spec.loader.exec_module(module)
    return module


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_cases(text: str) -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_list: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip() == "cases:":
            continue
        if raw_line.startswith("  - id:"):
            if current:
                cases.append(current)
            current = {"id": strip_quotes(raw_line.split(":", 1)[1])}
            current_list = None
            continue
        if current is None:
            continue
        if raw_line.startswith("    ") and ":" in raw_line and not raw_line.lstrip().startswith("-"):
            key, value = raw_line.strip().split(":", 1)
            value = value.strip()
            if value:
                current[key] = int(value) if value.isdigit() else strip_quotes(value)
                current_list = None
            else:
                current[key] = []
                current_list = key
            continue
        if raw_line.startswith("      -") and current_list:
            item = strip_quotes(raw_line.split("-", 1)[1])
            assert isinstance(current[current_list], list)
            current[current_list].append(item)

    if current:
        cases.append(current)
    return cases


def model_to_architecture(case_id: str, target_model: str) -> str:
    if "series" in case_id:
        return "system"
    if target_model in {"midjourney", "flux", "gpt-image", "dreamina", "grok"}:
        return "compact"
    return "auto"


def load_skill_outputs() -> dict[str, str]:
    if not SKILL_OUTPUTS_FILE.exists():
        return {}
    data = json.loads(SKILL_OUTPUTS_FILE.read_text(encoding="utf-8"))
    outputs: dict[str, str] = {}
    for record in data.get("records", []):
        case_id = record.get("case_id")
        prompt = record.get("skill_output_prompt")
        if case_id and prompt:
            outputs[str(case_id)] = str(prompt)
    return outputs


def feature_hits(prompt: str, features: str) -> tuple[int, int, list[str]]:
    if not features:
        return 0, 0, []
    parts = [part.strip().lower() for part in re.split(r"[,;]", features) if part.strip()]
    haystack = prompt.lower()
    hits = 0
    missing: list[str] = []
    for part in parts:
        if part == "no negative prompt block":
            if "negative prompt" not in haystack and "--no" not in haystack:
                hits += 1
            else:
                missing.append(part)
            continue
        if part == "parameters at end":
            last_param = haystack.rfind("--")
            if last_param >= 0 and last_param > max(0, len(haystack) - 90):
                hits += 1
            else:
                missing.append(part)
            continue
        synonym_terms = FEATURE_SYNONYMS.get(part)
        if synonym_terms:
            if any(term.lower() in haystack for term in synonym_terms):
                hits += 1
            else:
                missing.append(part)
            continue
        tokens = re.findall(r"[a-zA-Z0-9#]+", part)
        if not tokens:
            continue
        required = tokens[:2] if len(tokens) > 1 else tokens
        if any(token in haystack for token in required):
            hits += 1
        else:
            missing.append(part)
    return hits, len(parts), missing


def lint_score(linter, prompt: str, architecture: str, target_model: str):
    if not prompt:
        return None
    return linter.lint(prompt, architecture, target_model)


def make_report(cases: list[dict[str, object]]) -> str:
    linter = load_linter()
    skill_outputs = load_skill_outputs()
    lines = [
        "# Prompt Eval Report",
        "",
        "Generated from `evals/prompt_cases.yml` using structural prompt lint only.",
        "`Skill` columns use `skill_output_prompt` fields, with `evals/skill_outputs.json` as a fallback; this is not a Codex router simulator.",
        "Image-output scoring still requires `evals/image_output_protocol.md`.",
        "",
        "| Case | Model | Mode | Source | Candidate | Candidate Delta | Skill | Skill Delta | Features | Missing Features | Expected Risks |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]

    for case in cases:
        case_id = str(case["id"])
        target_model = str(case.get("target_model", "generic"))
        expected_mode = str(case.get("expected_mode", "unknown"))
        source_prompt = str(case.get("source_prompt", ""))
        rewritten_prompt = str(case.get("rewritten_prompt_candidate", ""))
        skill_prompt = str(case.get("skill_output_prompt", "")) or skill_outputs.get(case_id, "")
        expected_features = str(case.get("expected_rewrite_features", ""))
        architecture = model_to_architecture(case_id, target_model)
        source_result = lint_score(linter, source_prompt, architecture, target_model)
        rewritten_result = lint_score(linter, rewritten_prompt, architecture, target_model)
        skill_result = lint_score(linter, skill_prompt, architecture, target_model)
        risks = case.get("expected_risks", [])
        risk_text = "; ".join(risks) if isinstance(risks, list) else str(risks)
        risk_text = re.sub(r"\|", "/", risk_text)
        source_score = source_result.score if source_result else ""
        rewrite_score = rewritten_result.score if rewritten_result else ""
        rewrite_delta = rewritten_result.score - source_result.score if source_result and rewritten_result else ""
        skill_score = skill_result.score if skill_result else ""
        skill_delta = skill_result.score - source_result.score if source_result and skill_result else ""
        hits, total, missing = feature_hits(skill_prompt or rewritten_prompt, expected_features)
        feature_text = f"{hits}/{total}" if total else ""
        missing_text = ", ".join(missing) if missing else "-"
        lines.append(
            f"| `{case_id}` | `{target_model}` | `{expected_mode}` | {source_score} | "
            f"{rewrite_score} | {rewrite_delta} | {skill_score} | {skill_delta} | {feature_text} | {missing_text} | {risk_text} |"
        )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    cases = parse_cases(CASES_FILE.read_text(encoding="utf-8"))
    report = make_report(cases)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_FILE.relative_to(ROOT)} with {len(cases)} cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
