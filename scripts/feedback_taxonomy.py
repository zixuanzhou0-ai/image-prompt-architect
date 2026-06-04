#!/usr/bin/env python3
"""Shared image-feedback labels, score keys, and deterministic repair rules."""

from __future__ import annotations


SCORE_KEYS = [
    "subject_readability",
    "style_visibility",
    "clean_render",
    "composition",
    "material_clarity",
    "background_control",
    "text_accuracy",
    "reference_adherence",
    "identity_consistency",
    "product_geometry",
]

FAILURE_LABELS = [
    "texture_noise_overload",
    "muddy_materials",
    "over_detailed_background",
    "style_overpowering_subject",
    "media_defect_too_strong",
    "low_subject_readability",
    "weak_style_visibility",
    "random_text_or_symbols",
    "edge_contamination",
    "text_accuracy_failure",
    "identity_drift",
    "product_geometry_drift",
    "reference_role_confusion",
    "composition_drift",
    "prompt_too_long",
    "style_overload",
]

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
    "text_accuracy_failure": "Render only the exact quoted text requested; remove all extra letters, symbols, fake words, and unquoted typography.",
    "identity_drift": "Restore the original identity anchors: face structure, pose, clothing, age, expression, and distinctive accessories.",
    "product_geometry_drift": "Lock product geometry: silhouette, proportions, cap/pump shape, label placement, edges, and camera angle.",
    "reference_role_confusion": "Use reference images only for their assigned roles; do not preserve unwanted background, text, logos, lighting, or artifacts.",
    "composition_drift": "Return to the intended framing, camera distance, visual hierarchy, subject scale, and aspect ratio.",
    "prompt_too_long": "Compress the revision to subject, preserve/change instructions, one main style, and hard constraints.",
    "style_overload": "Keep one main style anchor and at most one weak modifier; remove competing media and genre references.",
}

MODEL_REPAIR_PROFILES = {
    "generic": {
        "max_words": 180,
        "style": "natural revision prompt",
        "priority": "preserve the original intent, then repair only the observed failures",
        "defect_policy": "keep media defects subtle and away from the subject",
    },
    "gpt-image": {
        "max_words": 140,
        "style": "short natural-language revision prompt",
        "priority": "subject readability, clean edges, exact text, product geometry, and reference roles before style texture",
        "defect_policy": "remove stacked grain, scan, VHS, CRT, halftone, dirty photocopy, and heavy noise language; keep at most one subtle artifact",
    },
    "dreamina": {
        "max_words": 160,
        "style": "short Chinese-first concept plus compact visual terms",
        "priority": "clear subject, simple scene, visible style, and short avoid list",
        "defect_policy": "avoid long negative blocks and keep texture defects light",
    },
    "midjourney": {
        "max_words": 90,
        "style": "compact phrase revision with parameters at the end",
        "priority": "subject, setting, one style phrase, camera, light, and concise --no terms",
        "defect_policy": "avoid stacked defect phrases; use --no only for concrete exclusions",
    },
    "flux": {
        "max_words": 160,
        "style": "positive-replacement revision prompt",
        "priority": "positive replacements, exact materials, clear lighting, and API fields outside prompt prose",
        "defect_policy": "rewrite unwanted dirty effects as clean surfaces, empty backgrounds, and controlled texture",
    },
}


def known_failures(failures: list[str]) -> list[str]:
    """Return valid failure labels in input order."""

    allowed = set(FAILURE_LABELS)
    return [failure for failure in failures if failure in allowed]


def repair_text_for_failures(failures: list[str]) -> str:
    """Join deterministic repair rules for valid failure labels."""

    return " ".join(FAILURE_REPAIR_RULES[failure] for failure in known_failures(failures))


def model_repair_profile(model: str) -> dict[str, object]:
    """Return the closest repair profile for a model name."""

    normalized = model.lower().strip()
    if normalized in MODEL_REPAIR_PROFILES:
        return MODEL_REPAIR_PROFILES[normalized]
    if normalized in {"openai", "chatgpt-image", "chatgpt image", "gpt-image-2", "gpt image"}:
        return MODEL_REPAIR_PROFILES["gpt-image"]
    if normalized in {"jimeng", "seedream", "dreamina/jimeng"}:
        return MODEL_REPAIR_PROFILES["dreamina"]
    if normalized in {"bfl", "flux.2", "flux2"}:
        return MODEL_REPAIR_PROFILES["flux"]
    return MODEL_REPAIR_PROFILES["generic"]


def default_preserve_text() -> str:
    return "the original subject, core action, composition intent, exact quoted text, product geometry, and assigned reference roles"


def default_next_check(failures: list[str]) -> str:
    valid = known_failures(failures)
    if not valid:
        return "Confirm the repaired image matches the original intent without adding new creative changes."
    return "Check that these failures are fixed: " + ", ".join(valid) + "."


def build_revision_prompt(
    *,
    model: str,
    failures: list[str],
    preserve: str | None = None,
    change: str | None = None,
    observed_cause: str | None = None,
    extra_context: str | None = None,
) -> str:
    """Build a copy-ready revision prompt from review fields."""

    valid_failures = known_failures(failures)
    profile = model_repair_profile(model)
    preserve_text = (preserve or "").strip() or default_preserve_text()
    repair_text = (change or "").strip() or repair_text_for_failures(valid_failures)
    cause_text = (observed_cause or "").strip()
    context_text = (extra_context or "").strip()

    parts = [
        "Revise the previous image.",
        f"Preserve {preserve_text}.",
    ]
    if cause_text:
        parts.append(f"Observed failure: {cause_text}.")
    if repair_text:
        parts.append(f"Change only the failed areas: {repair_text}")
    parts.append(str(profile["defect_policy"]) + ".")
    if context_text:
        parts.append(context_text)
    parts.append("Do not introduce new subjects, new layout ideas, or unrelated style changes.")
    return " ".join(part.strip() for part in parts if part).strip()
