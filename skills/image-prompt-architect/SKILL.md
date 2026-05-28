---
name: image-prompt-architect
description: Create, adapt, critique, and iterate image-generation prompts using seven-layer image structure, multi-system modular prompt templates, and model-specific adapters for Grok, Dreamina/Seedream, GPT Image, Midjourney, Flux, and similar tools. Use when the user asks for image prompts, prompt engineering for AI images, cinematic/series prompt templates, prompt diagnosis, model adaptation, prompt libraries, or reusable visual style systems.
---

# Image Prompt Architect

## Core Principle

Treat prompt structure as a scaffold, not the art itself. A strong image prompt needs both:

- **Architecture**: a chosen structure that tells the model how to parse the image.
- **Substance**: specific scene details, style anchors, emotional intent, medium cues, and constraints.

Avoid merely filling a template with generic words. If a layer is vague, ask for or infer concrete visual details.

## Workflow

1. Identify the target model, output type, and purpose.
   - If the user names a model, adapt to it.
   - If no model is named, ask only when the choice changes the result materially; otherwise choose a conservative general prompt and state the assumption.
   - For Dreamina/Seedream image work in a workspace with project instructions, follow the local Dreamina rules first.

2. Choose the prompt architecture.
   - Use **seven-layer structure** for one-off images that need precise control over subject, lighting, materials, composition, and style. Read `references/seven-layer-framework.md` when needed.
   - Use **multi-system modular template** for series, cinematic stills, consistent visual grammar, narrative worlds, or sets of images. Read `references/system-template-framework.md` when needed.
   - Use **hybrid architecture** when the user needs both precise details and strong style continuity across a series.
   - Use **compact natural-language architecture** for models that revise or reason over prompts well, especially GPT Image-style systems. Read `references/model-adapters.md` before making model-specific claims.

3. Draft in a learning-friendly form first.
   - Provide labeled sections so the user can see what each layer or system controls.
   - Keep repeated style anchors intentional. Repeat only the few concepts that must dominate the output.
   - Separate positive prompt, negative constraints, and model notes.

4. Produce a clean copy version.
   - After the labeled version, provide a direct copy-ready prompt without explanations.
   - Match the language strategy to the model: English for maximum control on English-dominant models; Chinese or bilingual when cultural specificity or text rendering benefits from it.

5. Run a prompt self-check.
   - Use `references/checklist.md`.
   - For longer prompts, optionally run `scripts/prompt_lint.py` on a saved prompt file to detect missing layers, weak anchors, and overlong sections.

6. Suggest targeted iteration knobs.
   - Name the 2-4 highest-leverage edits: subject specificity, light source, camera distance, color system, material cues, style anchor, negative constraints, or model adapter.
   - Do not rewrite everything when one layer is the likely failure point.

## Output Contract

When creating or rewriting a prompt, default to this structure:

1. **Architecture Choice**: why this framework fits.
2. **Tagged Prompt**: labeled layers or systems.
3. **Copy-Ready Prompt**: clean final prompt.
4. **Negative / Avoid**: what to suppress.
5. **Model Notes**: language, length, and adaptation guidance.
6. **Iteration Knobs**: what to adjust after seeing the image.

For quick user requests, compress the explanation but still include a copy-ready prompt.

## References

- `references/seven-layer-framework.md`: seven-layer prompt structure.
- `references/system-template-framework.md`: multi-system modular template for cinematic series and unified visual worlds.
- `references/model-adapters.md`: model-specific prompt strategy.
- `references/checklist.md`: prompt quality gate and debugging checklist.
- `references/examples.md`: worked examples and reusable skeletons.

