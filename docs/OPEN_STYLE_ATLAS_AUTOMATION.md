# Open Style Atlas Automation

This workflow keeps generating varied images with the seven-layer standard.
Version `open-style-v0.16` adds a clean render profile, separates internal
seven-layer specs from model-facing render prompts, and introduces structured
image review/revision scaffolding. Image Prompt Architect `v0.18` moves the
failure labels and repair rules into a shared feedback taxonomy used by both
batch review and single-prompt feedback review.

## What It Does

1. Samples subject, environment, lighting, material, camera, expression acting, and tone from `automation/open_style_source_pool.json`.
2. Samples one main rare style and up to one auxiliary style from `automation/rare_style_library.json`.
3. Writes a compressed render prompt in `prompts/` and a full seven-layer internal prompt in `prompts_internal/`.
4. Records style metadata, lint scores, render profile settings, history dedupe status, and prompt paths in `manifest.json`.
5. Lets Codex generate images from the render prompts and save them under `images/`.
6. Creates `generated_review.json` for image scoring and failure labels.
7. Generates revision prompts from review failures and imports finished images into Eagle.

## Prepare A Clean Batch

```powershell
python scripts\open_style_sampler.py --count 3 --min-lint-score 10 --eagle-folder "AI风格探索"
```

Defaults:

- `--render-profile clean`
- `--style-strength balanced`
- `--background-complexity 2`
- `--defect-strength 0.15`
- `--max-aux-styles 1`

The command prints the run folder path. Inside it:

- `prompts/`: compressed model-facing render prompts.
- `prompts_internal/`: full seven-layer internal specs for lint/review.
- `images/`: save generated images here.
- `manifest.json`: batch metadata.
- `generation_queue.md`: what to generate.
- `import_to_eagle.ps1`: import command.

## Exploration Options

```powershell
python scripts\open_style_sampler.py `
  --count 3 `
  --style-family graphic `
  --freshness high `
  --render-profile explore `
  --style-strength style-forward `
  --min-lint-score 10
```

Key options:

- `--style-library`: rare style JSON path. Default: `automation/rare_style_library.json`.
- `--style-family`: limit the main style pool. Choices: `film`, `product`, `photography`, `illustration`, `graphic`, `craft`, `digital`, `space`, `material`, `fashion`.
- `--freshness`: `high` biases toward newer, more specific style entries; `normal` is flatter.
- `--render-profile`: `clean`, `explore`, or `raw`.
- `--style-strength`: `subject-first`, `balanced`, or `style-forward`. If omitted, `clean` defaults to `balanced`.
- `--background-complexity`: `1`, `2`, or `3`.
- `--defect-strength`: `0.0` to `0.5`; clean batches should stay near `0.15`.
- `--max-aux-styles`: `0` or `1`.
- `--no-history`: disable reading recent manifests and reviews for repeat/failure lowering.

## Manifest Fields

Every v0.16 manifest includes:

- `prompt_contract_version: "open-style-v0.16"`
- `style_library_version`
- `style_family`, `freshness`, `style_strength`, and `render_profile`
- `background_complexity`, `defect_strength`, and `max_aux_styles`
- `history_dedupe.enabled`, `runs_scanned`, and `reviews_scanned`

Each prompt record includes:

- `prompt_file` / `render_prompt_file`: compressed render prompt.
- `internal_prompt_file`: full seven-layer spec.
- `render_prompt_chars` and `internal_prompt_chars`.
- `style_selection`: main/auxiliary style IDs, names, categories, risk, and fix.
- `style_budget`: style strength, defect strength, texture density, and background complexity.

The Eagle import still uses one batch annotation file. Per-image metadata lives in
the manifest so Eagle can preserve the full prompt record without changing the
import API path.

## Review And Revision Loop

After images are saved under `images/`, create a review template:

```powershell
python scripts\review_generated_images.py "<run folder>"
```

Fill `generated_review.json` with 0/1/2 scores, failure labels, notes, and keep decisions.
Supported failure labels come from `scripts/feedback_taxonomy.py` and include:

- `texture_noise_overload`
- `muddy_materials`
- `over_detailed_background`
- `style_overpowering_subject`
- `media_defect_too_strong`
- `low_subject_readability`
- `weak_style_visibility`
- `random_text_or_symbols`
- `edge_contamination`
- `text_accuracy_failure`
- `identity_drift`
- `product_geometry_drift`
- `reference_role_confusion`
- `composition_drift`
- `prompt_too_long`
- `style_overload`

Generate repair prompts from the failure labels:

```powershell
python scripts\make_revision_prompts.py "<run folder>"
```

The script writes `revisions/<index>_revision.txt` and backfills empty
`revision_prompt` fields in `generated_review.json`.

For a single non-batch prompt, use:

```powershell
python scripts\create_prompt_feedback_review.py --prompt-file "<prompt.txt>" --model gpt-image --case-id "<case id>" --image-path "<image.png>"
python scripts\make_feedback_revision.py "<prompt_feedback_review.json>"
```

## Import A Finished Batch

```powershell
python scripts\open_style_sampler.py --import-images --out "<run folder>" --eagle-folder "AI风格探索"
```

or run the generated:

```powershell
.\import_to_eagle.ps1
```

## Automation Prompt

Use this as the Codex App heartbeat prompt:

```text
Continue the Open Style Atlas image exploration in E:\七层提示词\image-prompt-architect.

Workflow:
1. Run `python scripts\open_style_sampler.py --count 3 --min-lint-score 10 --render-profile clean --eagle-folder "AI风格探索"`.
2. Read `generation_queue.md`, `manifest.json`, and the render prompts in `prompts/`.
3. Generate one image per render prompt. Honor aspect ratio when possible, but prioritize clean subject readability.
4. Save each image into `images/` with matching numeric prefixes.
5. Run `python scripts\review_generated_images.py "<run folder>"`.
6. Inspect each image and fill `generated_review.json` with scores, failure labels, notes, and keep decisions.
7. Run `python scripts\make_revision_prompts.py "<run folder>"` for any failed images.
8. Regenerate only the images that need repair, then update the review.
9. Run `python scripts\open_style_sampler.py --import-images --out "<run folder>" --eagle-folder "AI风格探索"`.

Creative direction:
- Explore rare sub-styles, but keep the subject clean and readable.
- In clean mode, the final render prompt should be shorter than the internal seven-layer spec.
- Media defects must remain subtle; avoid dirty scan marks, muddy materials, and texture bleeding over subject edges.
- Do not copy exact protected characters, living artists, living actors, logos, or readable copyrighted text.
- Record failures honestly; sampler history uses review data to lower risky style weights later.
```
