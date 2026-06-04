#!/usr/bin/env python3
"""Generate a single-image revision prompt from prompt_feedback_review.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from feedback_taxonomy import build_revision_prompt, default_next_check, known_failures  # noqa: E402


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def output_prompt_path(review_path: Path, explicit: Path | None = None) -> Path:
    return explicit.resolve() if explicit else review_path.resolve().parent / "revision_prompt.txt"


def generate_feedback_revision(review_path: Path, out_prompt: Path | None = None) -> dict[str, Any]:
    review_path = review_path.resolve()
    review = read_json(review_path)
    failures = known_failures(review.get("failures", []))
    revision_prompt = review.get("revision_prompt") or build_revision_prompt(
        model=str(review.get("target_model") or "generic"),
        failures=failures,
        preserve=review.get("preserve"),
        change=review.get("change"),
        observed_cause=review.get("observed_cause"),
    )
    next_check = review.get("next_check") or default_next_check(failures)
    review["failures"] = failures
    review["revision_prompt"] = revision_prompt
    review["next_check"] = next_check
    write_json(review_path, review)

    prompt_path = output_prompt_path(review_path, out_prompt)
    prompt_path.write_text(revision_prompt + "\n", encoding="utf-8")
    return {
        "status": "success",
        "review_file": str(review_path),
        "revision_file": str(prompt_path),
        "failures": failures,
        "next_check": next_check,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a revision_prompt.txt from prompt_feedback_review.json.")
    parser.add_argument("review_file", type=Path)
    parser.add_argument("--out-prompt", type=Path)
    args = parser.parse_args()

    result = generate_feedback_revision(args.review_file, args.out_prompt)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
