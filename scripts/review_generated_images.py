#!/usr/bin/env python3
"""Create a structured review template for generated Open Style Atlas images."""

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


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_image_for_index(images_dir: Path, index: int) -> str | None:
    prefix = f"{index:02d}"
    for pattern in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        for path in sorted(images_dir.glob(pattern)):
            if path.name.startswith(prefix):
                return str(path.relative_to(images_dir.parent))
    return None


def style_ids_for_prompt(prompt: dict[str, Any]) -> list[str]:
    selection = prompt.get("style_selection") or {}
    result = []
    for key in ("main_style", "auxiliary_style"):
        sid = ((selection.get(key) or {}).get("style_id") or "").strip()
        if sid:
            result.append(sid)
    return result


def build_review_template(run_dir: Path) -> dict[str, Any]:
    manifest = read_json(run_dir / "manifest.json")
    images_dir = run_dir / "images"
    reviews = []
    for prompt in manifest.get("prompts", []):
        index = int(prompt["index"])
        reviews.append(
            {
                "index": index,
                "image_path": find_image_for_index(images_dir, index),
                "prompt_file": prompt.get("prompt_file"),
                "internal_prompt_file": prompt.get("internal_prompt_file"),
                "main_style_id": ((prompt.get("style_selection") or {}).get("main_style") or {}).get("style_id"),
                "auxiliary_style_id": ((prompt.get("style_selection") or {}).get("auxiliary_style") or {}).get("style_id"),
                "style_ids": style_ids_for_prompt(prompt),
                "overall_score": None,
                "scores": {key: None for key in SCORE_KEYS},
                "failures": [],
                "revision_prompt": "",
                "keep": None,
                "notes": "",
            }
        )
    return {
        "batch_id": manifest.get("batch_id", run_dir.name),
        "prompt_contract_version": manifest.get("prompt_contract_version"),
        "review_schema_version": "open-style-review-v0.2",
        "score_scale": "0=fail, 1=partial, 2=good",
        "allowed_failure_labels": FAILURE_LABELS,
        "reviews": reviews,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create generated_review.json for an Open Style Atlas run.")
    parser.add_argument("run_folder", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    run_dir = args.run_folder.resolve()
    output_path = run_dir / "generated_review.json"
    if output_path.exists() and not args.overwrite:
        raise SystemExit(f"{output_path} already exists; pass --overwrite to replace it.")
    review = build_review_template(run_dir)
    write_json(output_path, review)
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
