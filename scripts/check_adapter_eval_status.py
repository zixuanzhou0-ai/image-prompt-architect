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
    scored_models = sorted(
        {
            str(record.get("target_model"))
            for record in records.get("records", [])
            if record.get("image_score") is not None
        }
    )

    warnings: list[str] = []
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
