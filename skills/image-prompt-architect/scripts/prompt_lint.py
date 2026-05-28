#!/usr/bin/env python3
"""Small lint helper for image-prompt-architect prompts.

It detects whether a prompt appears to include the core seven-layer or
multi-system controls and prints concise improvement hints.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


SEVEN_LAYER_PATTERNS = {
    "subject": r"subject|主体|person|woman|man|character|object|creature|product",
    "environment": r"environment|环境|street|room|forest|city|landscape|background|location",
    "lighting": r"lighting|光影|light|neon|moonlight|sunlight|backlit|volumetric|atmosphere|氛围",
    "material": r"material|材质|texture|silk|metal|glass|stone|wood|reflection|grain",
    "composition": r"composition|构图|camera|lens|shot|angle|framing|depth of field|bokeh",
    "style": r"style|风格|cinematic|film|anime|oil painting|noir|editorial",
    "tone": r"tone|语感|artistic|emotion|nostalgia|melancholy|narrative|内涵",
}

SYSTEM_PATTERNS = {
    "spatial system": r"spatial system|空间系统",
    "character system": r"character system|人物系统",
    "color system": r"color system|色彩系统",
    "medium system": r"medium system|介质系统",
    "composition system": r"composition system|构图系统",
    "lighting system": r"lighting|光影",
    "narrative system": r"narrative|emotion|叙事|情绪",
}

ANCHOR_TERMS = [
    "cinematic",
    "film still",
    "35mm",
    "telecine",
    "noir",
    "mono no aware",
    "nostalgic",
    "volumetric",
    "shallow depth of field",
]


def count_matches(text: str, patterns: dict[str, str]) -> list[str]:
    found = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(name)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint an image prompt for structural coverage.")
    parser.add_argument("prompt_file", type=Path, help="Text file containing a prompt")
    args = parser.parse_args()

    text = args.prompt_file.read_text(encoding="utf-8")
    words = re.findall(r"\S+", text)
    seven = count_matches(text, SEVEN_LAYER_PATTERNS)
    systems = count_matches(text, SYSTEM_PATTERNS)
    anchors = [term for term in ANCHOR_TERMS if term.lower() in text.lower()]

    print(f"Prompt length: {len(words)} tokens/words approx.")
    print(f"Seven-layer coverage: {len(seven)}/7 ({', '.join(seven) or 'none'})")
    print(f"System-template coverage: {len(systems)}/7 ({', '.join(systems) or 'none'})")
    print(f"Detected style anchors: {', '.join(anchors) or 'none'}")

    missing = [name for name in SEVEN_LAYER_PATTERNS if name not in seven]
    if missing and len(systems) < 5:
        print("Hints:")
        for name in missing:
            print(f"- Add or clarify {name}.")
    if len(words) > 450:
        print("- Consider shortening or moving the most important constraints earlier for models that ignore late details.")
    if len(anchors) == 0:
        print("- Add 1-3 strong style anchors if visual consistency matters.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

