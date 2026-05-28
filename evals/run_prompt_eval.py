#!/usr/bin/env python3
"""Generate a lightweight prompt-level eval report.

This intentionally avoids a YAML dependency and only parses the simple
`evals/prompt_cases.yml` structure used by this repository.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_FILE = ROOT / "evals" / "prompt_cases.yml"
REPORT_FILE = ROOT / "evals" / "report.md"
LINTER_FILE = ROOT / "skills" / "image-prompt-architect" / "scripts" / "prompt_lint.py"


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


def make_report(cases: list[dict[str, object]]) -> str:
    linter = load_linter()
    lines = [
        "# Prompt Eval Report",
        "",
        "Generated from `evals/prompt_cases.yml` using structural prompt lint only.",
        "Image-output scoring still requires `evals/image_output_protocol.md`.",
        "",
        "| Case | Model | Mode | Lint Score | Critical | Warnings | Expected Risks |",
        "| --- | --- | --- | ---: | ---: | ---: | --- |",
    ]

    for case in cases:
        case_id = str(case["id"])
        target_model = str(case.get("target_model", "generic"))
        expected_mode = str(case.get("expected_mode", "unknown"))
        source_prompt = str(case.get("source_prompt", ""))
        architecture = model_to_architecture(case_id, target_model)
        result = linter.lint(source_prompt, architecture, target_model)
        risks = case.get("expected_risks", [])
        risk_text = "; ".join(risks) if isinstance(risks, list) else str(risks)
        risk_text = re.sub(r"\|", "/", risk_text)
        lines.append(
            f"| `{case_id}` | `{target_model}` | `{expected_mode}` | {result.score} | "
            f"{len(result.critical)} | {len(result.warnings)} | {risk_text} |"
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
