# Project Context

This project was created from a long image-prompting discussion about turning reusable prompt methodology into a Codex skill and plugin.

## Core Insight

The original conversation compared two prompt architectures:

1. **Seven-layer structure**
   - Best for precise single-image control.
   - Layers: subject, environment, lighting/atmosphere, material/texture, composition/camera, style, era/artistic tone.

2. **Multi-system modular template**
   - Best for cinematic series, consistent visual grammar, and image sets.
   - Systems: premise, spatial, character, color, medium, composition, lighting/atmosphere, narrative/emotion, quality/exclusion.

The most important conclusion was not "templates make images good." The conclusion was:

> Structure is only the scaffold. Quality comes from concrete visual detail, strong anchors, model adaptation, and iteration.

## Design Decisions

- `SKILL.md` stays concise and tells Codex how to choose the right workflow.
- Detailed methods live in `references/` so Codex can load only what is needed.
- `model-adapters.md` avoids treating model behavior as permanent truth.
- `prompt_lint.py` gives a small deterministic check for missing image-prompt controls.
- `GPT_PRO_REVIEW_PROMPT.md` is included so a second model can critique the repository.

## Planned Review Loop

1. Publish this repository to GitHub.
2. Ask GPT Pro to review it with `GPT_PRO_REVIEW_PROMPT.md`.
3. Convert GPT Pro feedback into a second commit.
4. Add more examples and evaluation prompts if the review identifies gaps.

