# Open Style Atlas Automation

This workflow keeps generating varied images with the seven-layer standard.
Version `open-style-v0.15` uses the built-in rare style library at
`automation/rare_style_library.json` as the primary style source.

## What It Does

1. Samples subject, environment, lighting, material, camera, expression acting, and tone from `automation/open_style_source_pool.json`.
2. Samples one main rare style and up to one auxiliary style from the 620-entry rare style library.
3. Writes copy-ready prompt files in a run folder.
4. Records style metadata, lint scores, history dedupe status, and prompt paths in `manifest.json`.
5. Codex generates images from those prompt files.
6. Images are saved under the run folder and imported into Eagle under `AI风格探索`.

## Prepare A Batch

```powershell
python scripts\open_style_sampler.py --count 3 --min-lint-score 10 --eagle-folder "AI风格探索"
```

The command prints the run folder path. Inside it:

- `prompts/`: one prompt per image.
- `images/`: save generated images here.
- `manifest.json`: batch metadata.
- `generation_queue.md`: what to generate.
- `import_to_eagle.ps1`: import command.

By default, each prompt is checked with the local seven-layer linter and must
score at least `8/10`. For stricter batches, use `--min-lint-score 10`.

## v0.15 Options

```powershell
python scripts\open_style_sampler.py `
  --count 3 `
  --style-family graphic `
  --freshness high `
  --style-strength style-forward `
  --min-lint-score 10
```

Key options:

- `--style-library`: rare style JSON path. Default: `automation/rare_style_library.json`.
- `--style-family`: limit the main style pool. Choices: `film`, `product`, `photography`, `illustration`, `graphic`, `craft`, `digital`, `space`, `material`, `fashion`.
- `--freshness`: `high` biases toward newer, more specific style entries; `normal` is flatter.
- `--style-strength`: `subject-first`, `balanced`, or `style-forward`. Default: `style-forward`.
- `--no-history`: disable reading recent `runs/*/manifest.json` files for repeat lowering.

## Manifest Fields

Every v0.15 manifest includes:

- `prompt_contract_version: "open-style-v0.15"`
- `style_library_version`
- `style_family`, `freshness`, and `style_strength`
- `history_dedupe.enabled` and `history_dedupe.runs_scanned`

Each prompt record includes `style_selection` with:

- `main_style`: `style_id`, name, category, prompt tokens, visual DNA, risk, and fix.
- `auxiliary_style`: same shape, or `null`.
- `selection_mode`, `freshness`, `style_strength`.
- `history_dedupe`: recent subject, lighting, main-style, and auxiliary-style counts.

The Eagle import still uses one batch annotation file. Per-image metadata lives in
the manifest so Eagle can preserve the full prompt record without changing the
import API path.

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
1. Run `python scripts\open_style_sampler.py --count 3 --min-lint-score 10 --freshness high --style-strength style-forward --eagle-folder "AI风格探索"`.
2. Read the generated `generation_queue.md`, `manifest.json`, and prompt files.
3. For each prompt, generate one image with the image generation tool. Honor the requested aspect ratio when possible, but prefer expressive quality over rigid format.
4. Copy each generated image into the run folder's `images/` directory, matching numeric prefixes.
5. Inspect each image briefly. If the main style is invisible, the subject is lost, or the image is broken, generate one replacement.
6. Run `python scripts\open_style_sampler.py --import-images --out "<run folder>" --eagle-folder "AI风格探索"`.
7. Append a short `generated_review.md` with image paths, style IDs, what worked, visible failures, and what to push next.

Creative direction:
- Explore wildly through rare sub-styles, public-domain visual history, world craft, camera grammar, actorly expressions, impossible rooms, strange objects, and material experiments.
- Every image must follow the seven-layer prompt standard.
- The main rare style must be visible; avoid collapsing into generic cinematic photorealism.
- Do not copy exact protected characters, living artists, living actors, logos, or readable copyrighted text.
- Make each image feel like the strongest possible single frame from an unknown visual world.
```
