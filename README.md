# Image Prompt Architect

Image Prompt Architect is a Codex plugin for designing, rewriting, critiquing, and porting AI image-generation prompts.

It is not an image generator. It is a prompt architecture workflow for users who want better prompt text, model-specific adaptation, cinematic series bibles, or prompt diagnosis.

## What It Does

- Builds single-image prompts with a seven-layer structure.
- Builds cinematic series and style bibles with a multi-system template.
- Ports prompts between model families such as GPT Image, Grok, Midjourney, FLUX, Dreamina/Seedream, and Stable Diffusion wrappers.
- Critiques weak prompts and rewrites them.
- Runs a small lint script to catch missing controls, model-syntax issues, generic filler, and contradictions.

## What It Does Not Do

- It does not directly generate images.
- It does not edit images.
- It does not guarantee exact reproducibility across image models.
- It does not treat model-specific folklore as fact; model adapters are dated heuristics.

## Project Layout

```text
image-prompt-architect/
  .codex-plugin/plugin.json
  skills/image-prompt-architect/SKILL.md
  skills/image-prompt-architect/references/
  skills/image-prompt-architect/scripts/prompt_lint.py
  assets/examples/manifest.json
  tests/
```

## Install Locally

### Option A: Use As A Local Plugin Project

Clone the repository:

```bash
git clone https://github.com/zixuanzhou0-ai/image-prompt-architect.git
```

Then install or link it using the Codex plugin workflow available in your Codex app/CLI environment. The plugin follows the standard Codex layout: `.codex-plugin/plugin.json` at the root and bundled skills under `./skills/`.

### Option B: Use The Skill Directly

Copy or link `skills/image-prompt-architect/` into your Codex skills directory, then invoke it explicitly:

```text
$image-prompt-architect Rewrite this image prompt for Midjourney.
```

## Usage Examples

Quick prompt:

```text
Use Image Prompt Architect to write one FLUX prompt for a premium skincare product photo.
```

Critique:

```text
Use Image Prompt Architect to diagnose why this prompt feels generic, then rewrite it:
"beautiful girl, cinematic, masterpiece, city at night"
```

Model port:

```text
Use Image Prompt Architect to port this Grok prompt to Midjourney and convert the negatives to --no.
```

Series bible:

```text
Use Image Prompt Architect to create a 6-shot visual bible for an early-90s rural youth drama.
```

## Validate

Run from the repository root:

```bash
python skills/image-prompt-architect/scripts/prompt_lint.py tests/fixtures/good_seven_layer.txt --architecture seven-layer --model generic
python skills/image-prompt-architect/scripts/prompt_lint.py tests/fixtures/bad_flux_negative.txt --model flux --format json
python -m pytest
```

If you have the Codex creator/validator tools available locally, also run the skill and plugin validators from your installed Codex skill/plugin tooling.

## Evaluation

Use `skills/image-prompt-architect/references/evaluation-rubric.md`. A prompt should score at least 16/20 before being treated as strong, and model fit should not be 0.

## Review Loop

`GPT_PRO_REVIEW_PROMPT.md` contains a detailed prompt for asking another model to critique this repository. The intended workflow is:

1. Review the repo.
2. Convert critique into a patch plan.
3. Improve the skill and examples.
4. Run tests and validators.

