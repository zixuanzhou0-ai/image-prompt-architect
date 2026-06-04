#!/usr/bin/env python3
"""Generate revision prompts from Open Style Atlas review failure labels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FAILURE_REPAIR_RULES = {
    "texture_noise_overload": "Reduce heavy grain, scan noise, dirty speckles, and compression artifacts; keep only light texture in the background.",
    "muddy_materials": "Clarify primary materials, separate glass/metal/fabric with clean highlights, and avoid muddy mixed textures.",
    "over_detailed_background": "Simplify the background, remove dense small props, lower background contrast, and keep one readable environment.",
    "style_overpowering_subject": "Preserve subject identity and action first; let style influence color, surface, lighting, and composition only.",
    "media_defect_too_strong": "Keep media artifacts very subtle, limited to background and shadows; do not degrade the subject or edges.",
    "low_subject_readability": "Make the subject occupy 35-60% of the frame, improve edge separation, and reduce background contrast.",
    "weak_style_visibility": "Make the main style visible through 2-3 clear anchors: palette, material treatment, and composition language.",
    "random_text_or_symbols": "Remove random text, fake letters, logos, and symbol clutter; keep labels blank unless exact quoted text is requested.",
    "edge_contamination": "Clean up subject edges, prevent texture or background patterns from bleeding over the outline, and add subtle separation light.",
}


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prompts_by_index(manifest: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(prompt["index"]): prompt for prompt in manifest.get("prompts", [])}


def style_name(prompt: dict[str, Any], key: str) -> str:
    style = ((prompt.get("style_selection") or {}).get(key) or {})
    sid = style.get("style_id") or ""
    name = style.get("name") or ""
    return f"{sid} {name}".strip()


def repair_text_for_failures(failures: list[str]) -> str:
    repairs = [FAILURE_REPAIR_RULES[failure] for failure in failures if failure in FAILURE_REPAIR_RULES]
    return " ".join(repairs)


def build_revision_prompt(review: dict[str, Any], prompt: dict[str, Any]) -> str:
    failures = [failure for failure in review.get("failures", []) if failure in FAILURE_REPAIR_RULES]
    repair_text = repair_text_for_failures(failures)
    main_style = style_name(prompt, "main_style")
    auxiliary_style = style_name(prompt, "auxiliary_style")
    style_phrase = f"main style {main_style}"
    if auxiliary_style:
        style_phrase += f", auxiliary style {auxiliary_style}"
    aspect_ratio = prompt.get("aspect_ratio", "same aspect ratio")
    return (
        "Revise the image while preserving the same subject, action, composition, "
        f"{style_phrase}, and aspect ratio {aspect_ratio}. "
        f"{repair_text} "
        "Keep the result clean, readable, and faithful to the original prompt intent."
    ).strip()


def generate_revision_prompts(run_dir: Path) -> dict[str, Any]:
    manifest = read_json(run_dir / "manifest.json")
    review_path = run_dir / "generated_review.json"
    review = read_json(review_path)
    prompt_lookup = prompts_by_index(manifest)
    revisions_dir = run_dir / "revisions"
    revisions_dir.mkdir(exist_ok=True)

    generated = []
    for item in review.get("reviews", []):
        failures = [failure for failure in item.get("failures", []) if failure in FAILURE_REPAIR_RULES]
        if not failures:
            continue
        index = int(item["index"])
        prompt = prompt_lookup[index]
        revision_prompt = item.get("revision_prompt") or build_revision_prompt(item, prompt)
        item["revision_prompt"] = revision_prompt
        path = revisions_dir / f"{index:02d}_revision.txt"
        path.write_text(revision_prompt + "\n", encoding="utf-8")
        generated.append({"index": index, "revision_file": str(path.relative_to(run_dir)), "failures": failures})

    write_json(review_path, review)
    return {"status": "success", "generated": generated}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate revision prompts from generated_review.json.")
    parser.add_argument("run_folder", type=Path)
    args = parser.parse_args()
    result = generate_revision_prompts(args.run_folder.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
