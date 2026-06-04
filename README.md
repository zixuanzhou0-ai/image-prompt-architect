# Image Prompt Architect

[![test](https://github.com/zixuanzhou0-ai/image-prompt-architect/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/zixuanzhou0-ai/image-prompt-architect/actions/workflows/test.yml)

Image Prompt Architect is a Codex plugin for designing, rewriting, critiquing, and porting AI image-generation prompts.

It is not an image generator. It is a prompt architecture workflow for users who want better prompt text, model-specific adaptation, cinematic series bibles, or prompt diagnosis.

Current development version: `0.18.0` developer preview.
Latest tagged install target: `v0.14.0`.
Open Style Atlas prompt contract: `open-style-v0.16`.

## What It Does

- Builds single-image prompts with a seven-layer structure.
- Builds cinematic series and style bibles with a multi-system template.
- Ports prompts between model families such as GPT Image, Grok, Midjourney, FLUX, Dreamina/Seedream, and Stable Diffusion wrappers.
- Critiques weak prompts and rewrites them.
- Compresses long seven-layer drafts into cleaner final render prompts for GPT Image-like models.
- Creates narrow revision prompts from failed image-output feedback.
- Plans reference image roles for identity, product geometry, pose, composition, palette, and style.
- Runs a small lint script to catch missing controls, model-syntax issues, generic filler, contradictions, dirty-render risk, style overload, and defect overload.
- Creates single-image feedback review files and revision prompts from observed output failures.
- Generates Open Style Atlas prompt batches with rare style metadata, clean render prompts, and review-loop scaffolding.

## What It Does Not Do

- It does not directly generate images.
- It does not edit images.
- It does not guarantee exact reproducibility across image models.
- It does not treat model-specific folklore as fact; model adapters are dated heuristics.

## Project Layout

```text
image-prompt-architect/
  .agents/plugins/marketplace.json
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json
  commands/image-prompt-architect.md
  plugins/image-prompt-architect/
  skills/image-prompt-architect/SKILL.md
  skills/image-prompt-architect/references/
  skills/image-prompt-architect/scripts/prompt_lint.py
  assets/examples/manifest.json
  tests/
```

## Install

### Option A: Install From GitHub

Add this repository as a Codex plugin marketplace source, then install the plugin:

```bash
codex plugin marketplace add zixuanzhou0-ai/image-prompt-architect --ref v0.14.0
codex plugin add image-prompt-architect@image-prompt-architect
```

Verify:

```bash
codex plugin list --marketplace image-prompt-architect
```

For unreleased development snapshots, replace `v0.14.0` with `main`.

### Option B: Inspect Or Install Directly

Clone the exact developer-preview files:

```bash
git clone --branch v0.14.0 https://github.com/zixuanzhou0-ai/image-prompt-architect.git
```

If your Codex CLI does not support plugin marketplaces, copy or link `skills/image-prompt-architect/` into your Codex skills directory.

## Invoke The Skill

For a visual Chinese walkthrough, open [`docs/USAGE.html`](docs/USAGE.html) in a browser. It covers install commands, slash-menu usage, examples, model-specific phrasing, and troubleshooting.

For a Codex App image-generation workflow that combines Image Prompt Architect, Rare Style Explorer, and Eagle import, see [`docs/CODEX_EAGLE_IMAGE_AUTOMATION.md`](docs/CODEX_EAGLE_IMAGE_AUTOMATION.md).

Invoke it explicitly with either the slash command or the skill name:

```text
/image-prompt-architect Rewrite this image prompt for Midjourney:
beautiful girl, city at night, cinematic, masterpiece
```

```text
$image-prompt-architect Rewrite this image prompt for Midjourney.
```

`/image-prompt-architect` is a plugin command wrapper. `$image-prompt-architect` is the direct skill invocation. Both are supported after installation.

Version `v0.14.0` includes both `.codex-plugin` and `.claude-plugin` manifests so Codex Desktop command indexing can discover the slash-command wrapper as well as the skill. The `main` branch adds Open Style Atlas `open-style-v0.16` development features and Image Prompt Architect `v0.18.0` feedback-bridge tooling.

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

Prompt compression:

```text
Use Image Prompt Architect to compress this seven-layer draft into a clean GPT Image final render prompt.
```

Revision prompt:

```text
Use Image Prompt Architect to write a revision prompt. The output looked dirty and the scan texture covered the subject's face.
```

Reference roles:

```text
Use Image Prompt Architect to plan reference image roles: ref 1 is product geometry, ref 2 is palette, ref 3 is composition.
```

Feedback review:

```text
Use Image Prompt Architect to turn this failed image feedback into a revision prompt: the subject edges are dirty, the label text is wrong, and the reference background leaked into the output.
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
python scripts/create_prompt_feedback_review.py --prompt-file tests/fixtures/good_gpt_image_compressed_render_prompt.txt --model gpt-image --case-id demo --out runs/demo_prompt_feedback_review.json --overwrite
python scripts/make_feedback_revision.py runs/demo_prompt_feedback_review.json
python -m pytest
python evals/run_prompt_eval.py
python evals/check_image_output_records.py
```

If you have the Codex creator/validator tools available locally, also run the skill and plugin validators from your installed Codex skill/plugin tooling.

## Known Limitations

- This plugin does not generate images.
- It cannot guarantee exact reproducibility across image models.
- Model adapters are dated heuristics with source links, not permanent laws.
- The linter is structural and syntax-oriented; it does not replace image-output evaluation.
- Feedback review scripts standardize human/visual review notes; they do not inspect images automatically.

## Troubleshooting

- Plugin not appearing: confirm your Codex environment supports local plugin projects or marketplace sources.
- Skill not triggering: invoke it explicitly with `$image-prompt-architect`.
- `pytest` missing: install it with `python -m pip install pytest`.
- A bad fixture passes strict mode: file an issue with the fixture and expected failure.

## Evaluation

Use `skills/image-prompt-architect/references/evaluation-rubric.md`. A prompt should score at least 16/20 before being treated as strong, and model fit should not be 0.

`evals/run_prompt_eval.py` generates a prompt-level source/candidate/skill-output report at `evals/report.md`. Image-output evals still require manual model runs and the fields in `evals/image_output_protocol.md`.

CI evidence:

- Main badge: see the badge at the top of this README.
- Fixed release tag CI: check the [GitHub Actions workflow](https://github.com/zixuanzhou0-ai/image-prompt-architect/actions/workflows/test.yml) filtered to `v0.14.0`.
- Prompt-level report: [`evals/report.md`](evals/report.md).
- Image-output records: [`evals/image_output_records.json`](evals/image_output_records.json) is still placeholder-only until real model outputs are captured; v0.14 improves slash command indexing compatibility but does not invent output evidence.
- Image-output rubric: [`evals/image_output_rubric.md`](evals/image_output_rubric.md) defines task-specific gates for future real output evals.
- v1.0 gate: [`docs/V1_RELEASE_GATE.md`](docs/V1_RELEASE_GATE.md) defines the release checklist and example scored record shape.

Open Style Atlas evidence:

- Sampler: [`scripts/open_style_sampler.py`](scripts/open_style_sampler.py).
- Review template: [`scripts/review_generated_images.py`](scripts/review_generated_images.py).
- Revision prompts: [`scripts/make_revision_prompts.py`](scripts/make_revision_prompts.py).
- Single-prompt feedback review: [`scripts/create_prompt_feedback_review.py`](scripts/create_prompt_feedback_review.py).
- Single-prompt feedback revision: [`scripts/make_feedback_revision.py`](scripts/make_feedback_revision.py).
- Automation docs: [`docs/OPEN_STYLE_ATLAS_AUTOMATION.md`](docs/OPEN_STYLE_ATLAS_AUTOMATION.md).

## Review Loop

`GPT_PRO_REVIEW_PROMPT.md` contains a detailed prompt for asking another model to critique this repository. The intended workflow is:

1. Review the repo.
2. Convert critique into a patch plan.
3. Improve the skill and examples.
4. Run tests and validators.
