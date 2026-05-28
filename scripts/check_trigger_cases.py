#!/usr/bin/env python3
"""Heuristic smoke test for trigger-case fixtures.

This does not simulate Codex skill routing. It only catches obvious drift where
`should_not_trigger` examples start using explicit prompt-text trigger language.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "trigger_cases.yml"

PROMPT_TEXT_TERMS = re.compile(
    r"\b(prompt|rewrite|port|model adaptation|seven-layer|visual bible|style bible|prompt text)\b",
    re.I,
)


def load_list(name: str, text: str) -> list[str]:
    in_block = False
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith(f"{name}:"):
            in_block = True
            continue
        if in_block and re.match(r"^[A-Za-z_]+:", line):
            break
        if in_block and line.strip().startswith("-"):
            item = line.split("-", 1)[1].strip().strip('"')
            items.append(item)
    return items


def main() -> int:
    text = CASES.read_text(encoding="utf-8")
    should_trigger = load_list("should_trigger", text)
    should_not_trigger = load_list("should_not_trigger", text)
    errors = []

    if not should_trigger or not should_not_trigger:
        errors.append("trigger_cases.yml must define both should_trigger and should_not_trigger lists.")

    for item in should_trigger:
        if not PROMPT_TEXT_TERMS.search(item):
            errors.append(f"should_trigger case lacks explicit prompt-text intent: {item}")

    for item in should_not_trigger:
        if PROMPT_TEXT_TERMS.search(item):
            errors.append(f"should_not_trigger case contains prompt-text trigger language: {item}")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"Trigger smoke check passed: {len(should_trigger)} trigger, {len(should_not_trigger)} non-trigger cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
