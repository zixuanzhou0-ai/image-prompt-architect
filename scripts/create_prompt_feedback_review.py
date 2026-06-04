#!/usr/bin/env python3
"""Create a structured single-prompt image feedback review template."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from feedback_taxonomy import FAILURE_LABELS, SCORE_KEYS  # noqa: E402


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_review_template(
    *,
    prompt_file: Path,
    model: str,
    case_id: str,
    image_path: Path | None = None,
) -> dict[str, Any]:
    prompt_file = prompt_file.resolve()
    image_value = str(image_path.resolve()) if image_path else None
    return {
        "review_schema_version": "prompt-feedback-review-v0.1",
        "case_id": case_id,
        "target_model": model,
        "prompt_file": str(prompt_file),
        "image_path": image_value,
        "prompt_text": read_text(prompt_file),
        "score_scale": "0=fail, 1=partial, 2=good",
        "allowed_failure_labels": FAILURE_LABELS,
        "scores": {key: None for key in SCORE_KEYS},
        "failures": [],
        "observed_cause": "",
        "preserve": "",
        "change": "",
        "revision_prompt": "",
        "next_check": "",
        "notes": "",
    }


def default_output_path(prompt_file: Path) -> Path:
    return prompt_file.resolve().parent / "prompt_feedback_review.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create prompt_feedback_review.json for one generated image.")
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--image-path", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    out_path = args.out.resolve() if args.out else default_output_path(args.prompt_file)
    if out_path.exists() and not args.overwrite:
        raise SystemExit(f"{out_path} already exists; pass --overwrite to replace it.")
    review = build_review_template(
        prompt_file=args.prompt_file,
        model=args.model,
        case_id=args.case_id,
        image_path=args.image_path,
    )
    write_json(out_path, review)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
