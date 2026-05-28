#!/usr/bin/env python3
"""Check adapter metadata against image-output eval records.

This is intentionally light-touch for developer-preview releases. It does not
require image-output evals to exist. It only flags stale adapter metadata after
real image scores have been recorded.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDS_FILE = ROOT / "evals" / "image_output_records.json"
ADAPTERS_FILE = ROOT / "skills" / "image-prompt-architect" / "references" / "model-adapters.md"

MODEL_ADAPTER_HEADINGS = {
    "gpt-image": "GPT Image",
    "flux": "FLUX",
    "midjourney": "Midjourney",
    "dreamina": "Dreamina",
    "grok": "Grok",
}

REQUIRED_SCORED_FIELDS = [
    "model_version",
    "adapter_version",
    "rewritten_prompt",
    "task_type",
    "output_image_path",
    "image_score",
    "task_gate_results",
    "human_rater",
    "final_score",
]

TASK_REQUIRED_GATES = {
    "text_rendering": ["text_accuracy", "text_layout_legibility"],
    "editing": ["edit_preservation"],
    "series": ["identity_continuity", "constraint_handling"],
    "product_photography": ["product_geometry_material_fidelity", "subject_fidelity"],
    "model_port": ["model_specific_fit"],
}


def adapter_block(markdown: str, heading_hint: str) -> str:
    pattern = re.compile(rf"^## .*{re.escape(heading_hint)}.*$", re.I | re.M)
    match = pattern.search(markdown)
    if not match:
        return ""
    next_heading = re.search(r"^## ", markdown[match.end() :], re.M)
    if next_heading:
        return markdown[match.start() : match.end() + next_heading.start()]
    return markdown[match.start() :]


def main() -> int:
    records = json.loads(RECORDS_FILE.read_text(encoding="utf-8"))
    adapters = ADAPTERS_FILE.read_text(encoding="utf-8")
    scored_records = [record for record in records.get("records", []) if record.get("image_score") is not None]
    scored_models = sorted({str(record.get("target_model")) for record in scored_records})

    warnings: list[str] = []
    for record in scored_records:
        case_id = str(record.get("case_id", "unknown"))
        for field in REQUIRED_SCORED_FIELDS:
            value = record.get(field)
            if value in {None, "", "unknown"} or value == {}:
                warnings.append(f"{case_id}: scored image-output record has missing `{field}`")
        if "prompt_before" not in record or record.get("prompt_before") in {None, "", "unknown"}:
            warnings.append(f"{case_id}: scored image-output record has missing `prompt_before`")
        output_path = record.get("output_image_path")
        if isinstance(output_path, str) and output_path not in {"", "unknown"} and not re.match(r"^https?://", output_path):
            path = (ROOT / output_path).resolve()
            if not path.exists():
                warnings.append(f"{case_id}: output_image_path does not exist: {output_path}")
        final_score = record.get("final_score")
        if final_score is not None and not isinstance(final_score, (int, float)):
            warnings.append(f"{case_id}: final_score must be numeric when present")
        task_type = str(record.get("task_type", ""))
        gate_results = record.get("task_gate_results")
        required_gates = TASK_REQUIRED_GATES.get(task_type, [])
        if required_gates and isinstance(gate_results, dict):
            for gate in required_gates:
                value = gate_results.get(gate)
                if value is not True:
                    warnings.append(f"{case_id}: task gate `{gate}` must be true for task_type `{task_type}`")
        elif task_type:
            warnings.append(f"{case_id}: task_gate_results must be an object with task-specific gates")

    for model in scored_models:
        heading = MODEL_ADAPTER_HEADINGS.get(model, model)
        block = adapter_block(adapters, heading)
        if not block:
            warnings.append(f"{model}: adapter block not found")
            continue
        if re.search(r"\*\*Image-output eval last run:\*\*\s*none\b", block, re.I):
            warnings.append(f"{model}: image-output records exist but adapter still says eval last run is none")

    if warnings:
        print("Adapter eval status warnings:")
        print("\n".join(warnings))
        return 1

    if scored_models:
        print(f"Adapter eval status check passed for scored models: {', '.join(scored_models)}")
    else:
        print("Adapter eval status check passed: no real image-output scores recorded yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
