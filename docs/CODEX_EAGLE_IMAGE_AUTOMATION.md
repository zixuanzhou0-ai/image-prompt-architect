# Codex + Image Prompt Architect + Rare Style Explorer + Eagle Automation

This document defines a practical Codex App automation pattern for generating images with two local skills and importing the outputs into Eagle.

Verified local Eagle state on this machine:

- Eagle process: `F:\Eagle\Eagle\Eagle.exe`
- Eagle API: `http://localhost:41595`
- Eagle version: `4.0.0`
- Current library: `F:\Eagle\Mypic\MyPic.library`

## Cooperation Model

Use the two skills in a fixed order:

1. `$rare-style-explorer`
   - explores rare visual sub-style directions;
   - avoids generic style words;
   - produces several style candidates and anti-drift constraints.

2. `$image-prompt-architect`
   - turns the chosen style candidates into model-specific prompts;
   - handles GPT Image / Grok / Midjourney / FLUX syntax;
   - adds composition, reference-image role, constraints, and iteration knobs.

3. Image generation tool
   - generates images from the final prompt;
   - saves generated files locally.

4. `scripts/eagle_import.py`
   - imports generated PNG/JPG files into Eagle through the local API;
   - adds tags and annotation with prompt metadata.

## Recommended Automation Prompt

Paste this into a Codex App automation when you want a scheduled or repeatable image-generation batch.

```text
You are an automated AI image generation curator for this workspace.

Goal:
Generate a small batch of high-quality AI images, using both local skills:
- $rare-style-explorer for rare visual style exploration;
- $image-prompt-architect for model-specific prompt architecture.

Workspace:
E:\七层提示词\image-prompt-architect

Inputs:
- Subject: <replace with the subject>
- Target model: GPT Image unless the run request says otherwise.
- Batch size: 4 images unless the run request says otherwise.
- Eagle folder: import to Eagle through the local API. If no folder is specified, import unfiled with clear tags.
- Output folder: runs/<YYYYMMDD-HHMM>-<short-subject>/

Workflow:
1. Use $rare-style-explorer to generate 6 rare style directions for the subject.
   - Use the correct mode:
     - character for people, avatars, IP, portraits;
     - product for product or packaging;
     - poster for covers, social graphics, editorial visuals;
     - scene for narrative environments;
     - material-series for the same subject across surfaces.
   - Prefer freshness high.
   - Remove style candidates that conflict with the subject or platform.

2. Choose 2 strongest style directions.
   - Prefer styles that add concrete visual DNA rather than broad labels.
   - Keep a note of style IDs/names if available.

3. Use $image-prompt-architect to build final image prompts.
   - If a reference image is provided, set its role explicitly:
     preserve composition, palette, pose, layout density, material texture, and visual rhythm;
     do not preserve exact readable text, logos, real names, or copyrighted identity.
   - If target model is GPT Image, use natural-language prompt with clear subject, environment, light, composition, style, and constraints.
   - If target model is Grok, keep generation settings outside the prompt and make reference-image role explicit.
   - If target model is Midjourney, put parameters at the end and convert exclusions to --no.
   - If target model is FLUX, rewrite negative ideas as positive replacements.

4. Generate images.
   - Generate the requested batch size.
   - Save each output image into the run folder.
   - Keep a manifest file named manifest.json with:
     subject, target model, style direction, final prompt, generation time, output path, and notes.

5. Import generated images into Eagle.
   - Use:
     python scripts/eagle_import.py <image paths> --tag "Codex Image,AI generated,image-prompt-architect,rare-style-explorer,<target model>" --annotation-file <manifest or prompt note file>
   - If an Eagle folder is specified, pass --folder-name or --folder-id.
   - Do not delete the original generated files after importing.

6. Final report:
   - List imported images.
   - List Eagle import result.
   - Include the final prompts.
   - Include failed imports or model-generation problems if any.

Safety and quality:
- Do not claim image-output eval unless real images were inspected.
- Do not invent Eagle imports; verify API success.
- Do not copy real character names, logos, or readable copyrighted text unless the user explicitly asks for that and it is allowed.
- Prefer original fictional identities when imitating a style or layout.
```

## Eagle Import Commands

List Eagle folders:

```bash
python scripts/eagle_import.py --list-folders
```

Dry-run an import:

```bash
python scripts/eagle_import.py "C:\path\to\image.png" --tag "Codex Image,AI generated" --dry-run
```

Import to Eagle unfiled:

```bash
python scripts/eagle_import.py "C:\path\to\image.png" --tag "Codex Image,AI generated,image-prompt-architect,rare-style-explorer"
```

Import to a named Eagle folder:

```bash
python scripts/eagle_import.py "C:\path\to\image.png" --folder-name "Girl" --tag "Codex Image,AI generated"
```

Import with a metadata annotation:

```bash
python scripts/eagle_import.py "C:\path\to\image.png" --annotation-file "runs\batch\prompt.md" --tag "Codex Image,GPT Image"
```

## On-Demand Version

For manual runs inside Codex Desktop, use this compact prompt:

```text
Use $rare-style-explorer first to explore 6 rare style directions for this subject, then use $image-prompt-architect to turn the best 2 directions into GPT Image prompts. Generate 4 images with the built-in image generation tool. Save the images locally, then import them into Eagle with scripts/eagle_import.py. Add tags: Codex Image, AI generated, rare-style-explorer, image-prompt-architect, GPT Image. Subject: <your subject>
```

