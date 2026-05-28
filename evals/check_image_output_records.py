#!/usr/bin/env python3
"""Validate image-output eval records.

Placeholder records are allowed for developer-preview releases. Once a record
has `image_score`, this script treats it as real evidence and enforces the
v1.0-style required fields, task gates, output-path validity, and score gate.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RECORDS_FILE = ROOT / "evals" / "image_output_records.json"
DEFAULT_MAX_SCORE = 24
DEFAULT_MIN_SCORE = 18
ALLOWED_SKILL_OUTPUT_SOURCES = {"manual_capture", "codex_run", "golden_reference"}
PLACEHOLDER_STRINGS = {"", "unknown", "not_recorded"}

REQUIRED_REAL_CASES = {
    "gpt_image_text_rendering",
    "gpt_image_edit_preserve_change",
    "midjourney_no_phrase",
    "flux_plain_negation",
    "series_identity_drift",
}

REQUIRED_SCORED_FIELDS = [
    "case_id",
    "target_model",
    "model_version",
    "adapter_version",
    "prompt_before",
    "rewritten_prompt",
    "skill_output_source",
    "skill_output_date",
    "skill_output_notes",
    "task_type",
    "generation_params",
    "output_image_path",
    "image_score",
    "task_gate_results",
    "human_rater",
    "observed_failures",
    "revision_prompt",
    "final_score",
]

TASK_REQUIRED_GATES = {
    "text_rendering": ["text_accuracy", "text_layout_legibility"],
    "editing": ["edit_preservation"],
    "series": ["identity_continuity", "constraint_handling"],
    "product_photography": ["product_geometry_material_fidelity", "subject_fidelity"],
    "model_port": ["model_specific_fit"],
}


def missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().lower() in PLACEHOLDER_STRINGS
    if isinstance(value, dict):
        return len(value) == 0
    return False


def missing_list(value: Any) -> bool:
    return value is None or not isinstance(value, list)


def output_path_exists(value: str) -> bool:
    if re.match(r"^https?://", value):
        return True
    return (ROOT / value).resolve().exists()


def numeric_score_values(image_score: dict[str, Any]) -> list[int]:
    return [value for value in image_score.values() if isinstance(value, int) and not isinstance(value, bool)]


def validate_image_score(record: dict[str, Any]) -> list[str]:
    case_id = str(record.get("case_id", "unknown"))
    errors: list[str] = []
    image_score = record.get("image_score")
    final_score = record.get("final_score")

    if not isinstance(image_score, dict):
        return [f"{case_id}: image_score must be an object"]
    if not image_score:
        return [f"{case_id}: image_score must not be empty for scored records"]

    for dimension, value in image_score.items():
        valid_numeric = isinstance(value, int) and not isinstance(value, bool) and value in (0, 1, 2)
        valid_na = value == "not_applicable"
        if not (valid_numeric or valid_na):
            errors.append(f"{case_id}: image_score `{dimension}` must be 0, 1, 2, or not_applicable")

    numeric_values = numeric_score_values(image_score)
    computed_score = sum(numeric_values)
    if isinstance(final_score, (int, float)) and final_score != computed_score:
        errors.append(f"{case_id}: final_score {final_score} must equal numeric image_score sum {computed_score}")

    return errors


def validate_record(record: dict[str, Any]) -> list[str]:
    case_id = str(record.get("case_id", "unknown"))
    errors: list[str] = []

    for field in REQUIRED_SCORED_FIELDS:
        if field == "observed_failures":
            if missing_list(record.get(field)):
                errors.append(f"{case_id}: missing `{field}`")
        elif missing(record.get(field)):
            errors.append(f"{case_id}: missing `{field}`")

    source = record.get("skill_output_source")
    if source and source not in ALLOWED_SKILL_OUTPUT_SOURCES:
        errors.append(f"{case_id}: skill_output_source must be one of {sorted(ALLOWED_SKILL_OUTPUT_SOURCES)}")

    date = record.get("skill_output_date")
    if isinstance(date, str) and not missing(date) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        errors.append(f"{case_id}: skill_output_date must use YYYY-MM-DD")

    output_path = record.get("output_image_path")
    if isinstance(output_path, str) and not missing(output_path) and not output_path_exists(output_path):
        errors.append(f"{case_id}: output_image_path does not exist or use http(s): {output_path}")

    errors.extend(validate_image_score(record))

    final_score = record.get("final_score")
    if not isinstance(final_score, (int, float)):
        errors.append(f"{case_id}: final_score must be numeric")
    else:
        image_score = record.get("image_score")
        computed_max_score = 2 * len(numeric_score_values(image_score)) if isinstance(image_score, dict) else DEFAULT_MAX_SCORE
        max_score = record.get("max_score", computed_max_score or DEFAULT_MAX_SCORE)
        if not isinstance(max_score, (int, float)) or max_score <= 0:
            errors.append(f"{case_id}: max_score must be a positive number when provided")
        elif final_score > max_score:
            errors.append(f"{case_id}: final_score {final_score} cannot exceed max_score {max_score}")
        else:
            min_score = min(DEFAULT_MIN_SCORE, 0.75 * max_score)
            if final_score < min_score:
                errors.append(f"{case_id}: final_score {final_score} is below gate {min_score:g}")

    task_type = str(record.get("task_type", ""))
    gate_results = record.get("task_gate_results")
    required_gates = TASK_REQUIRED_GATES.get(task_type, [])
    if not isinstance(gate_results, dict):
        errors.append(f"{case_id}: task_gate_results must be an object")
    else:
        for gate in required_gates:
            if gate_results.get(gate) is not True:
                errors.append(f"{case_id}: task gate `{gate}` must be true for `{task_type}`")
            image_score = record.get("image_score")
            if isinstance(image_score, dict):
                gate_score = image_score.get(gate)
                if gate_score is None or gate_score == 0 or gate_score == "not_applicable":
                    errors.append(f"{case_id}: task gate `{gate}` must correspond to a positive image_score value")

    if not isinstance(record.get("generation_params"), dict):
        errors.append(f"{case_id}: generation_params must be an object")
    if not isinstance(record.get("observed_failures"), list):
        errors.append(f"{case_id}: observed_failures must be a list")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate image-output eval records.")
    parser.add_argument("--records", type=Path, default=RECORDS_FILE, help="Path to image_output_records.json.")
    parser.add_argument("--require-real-records", action="store_true", help="Fail when no scored records exist.")
    args = parser.parse_args()

    data = json.loads(args.records.read_text(encoding="utf-8"))
    records = data.get("records", [])
    scored_records = [record for record in records if record.get("image_score") is not None]

    errors: list[str] = []
    if args.require_real_records and not scored_records:
        errors.append("No scored image-output records exist.")
    if args.require_real_records:
        scored_case_ids = {str(record.get("case_id", "")) for record in scored_records}
        missing_cases = sorted(REQUIRED_REAL_CASES - scored_case_ids)
        if missing_cases:
            errors.append(f"Missing required scored image-output cases: {', '.join(missing_cases)}")
        revision_records = [
            record
            for record in scored_records
            if isinstance(record.get("observed_failures"), list)
            and record.get("observed_failures")
            and not missing(record.get("revision_prompt"))
        ]
        if len(revision_records) < 2:
            errors.append("At least two scored records must include observed failures and revision prompts.")

    for record in scored_records:
        errors.extend(validate_record(record))

    if errors:
        print("Image-output record validation failed:")
        print("\n".join(errors))
        return 1

    if scored_records:
        print(f"Image-output record validation passed for {len(scored_records)} scored record(s).")
    else:
        print("Image-output record validation passed: no scored records yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
