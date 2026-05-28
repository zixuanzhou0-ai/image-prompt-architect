# Model Adapters

Model behavior changes. Treat this file as a dated heuristic matrix, not permanent truth. Prefer official docs and local tests over inherited prompt lore.

## Adapter Schema

Each adapter tracks:

- **Last verified**
- **Source basis**
- **Best prompt shape**
- **Language strategy**
- **Length strategy**
- **Negative prompt strategy**
- **Parameter/API strategy**
- **Reference image strategy**
- **Do not claim**
- **Copy-ready output format**

## GPT Image / OpenAI Image Models

**Last verified:** 2026-05-28

**Source basis:**

- OpenAI image generation docs distinguish Responses API and Image API. Responses API is suited to conversational and multi-turn image generation/editing; Image API is suited to direct image operations.
- When using the image generation tool in Responses API, the mainline model may revise prompts for performance and expose `revised_prompt`.

**Best prompt shape:**

- Clear natural language with explicit priorities.
- Use sections when preserving/changing/editing instructions need clarity.
- For text rendering, quote exact text and specify placement, typography, layout, and what must remain unchanged.

**Language strategy:**

- Use the language that carries the user's intent best.
- English can help with production art-direction terms; Chinese can be appropriate for Chinese text rendering and culturally specific content.

**Length strategy:**

- Prefer concise, prioritized natural language over huge keyword piles.

**Negative prompt strategy:**

- Use "avoid" or "do not change" instructions in ordinary language.
- For editing, state both preservation and change constraints.

**Parameter/API strategy:**

- Note whether the workflow is Responses API or Image API if the user is coding.
- Mention `revised_prompt` only for Responses image generation tool behavior.

**Reference image strategy:**

- State what each reference image controls: identity, style, composition, product shape, or palette.

**Do not claim:**

- Do not claim exact reproducibility from prompt text alone.
- Do not claim English is always better.

**Copy-ready output format:**

```text
Create an image of ... Preserve ... Change ... Render the exact text "...". Avoid ...
```

## Grok / Grok Imagine

**Last verified:** 2026-05-28

**Source basis:**

- xAI Imagine docs state Grok Imagine models generate images from text prompts and expose settings such as output count, aspect ratio, resolution, and response format.

**Best prompt shape:**

- Structured English prompts often work well in practice, but treat this as a heuristic unless the user has test results.
- Seven-layer and system prompts are useful when the user wants explicit control.

**Language strategy:**

- Use English for technical art-direction terms when precision matters.
- Keep Chinese cultural terms when they are semantically important.

**Length strategy:**

- Medium to long prompts are acceptable when each part is concrete.

**Negative prompt strategy:**

- Use concise avoid statements. Do not overstuff exclusions.

**Parameter/API strategy:**

- If coding, expose aspect ratio, resolution, output count, and response format separately from prompt prose.

**Reference image strategy:**

- If references are available, name which reference controls style, subject, or composition.

**Do not claim:**

- Do not claim official proof that Grok is uniquely optimized for long cinematic prompts.

**Copy-ready output format:**

```text
[seven-layer or system prompt], avoid [specific failure modes]. Aspect ratio: ...
```

## Dreamina / Seedream / Jimeng

**Last verified:** 2026-05-28

**Source basis:**

- Project-local AGENTS rules may override this public adapter.
- Public model reports describe Seedream as a multimodal image generation/editing family, but public skill defaults should not hard-code a private "always use 4.5" rule.

**Best prompt shape:**

- Combine natural-language intent with structured aesthetic keywords when useful.
- Follow local prompt libraries, checklist, and model notes if present.

**Language strategy:**

- Chinese is often useful for culturally specific scenes.
- English is useful for common technical visual terms.

**Length strategy:**

- Use medium-length prompts with clear subject, scene, style, camera, and constraints.

**Negative prompt strategy:**

- Keep avoid lists short and model-specific.

**Parameter/API strategy:**

- Do not set a model default unless the user's local instructions require it.

**Reference image strategy:**

- State whether references control identity, pose, style, or layout.

**Do not claim:**

- Do not claim a public universal default model version.

**Copy-ready output format:**

```text
自然语言概念段落 + 三段式美学关键词 + 简短避免项
```

## Midjourney

**Last verified:** 2026-05-28

**Source basis:**

- Midjourney docs state parameters belong at the end of the prompt.
- The `--no` parameter is the native way to tell Midjourney what to exclude.

**Best prompt shape:**

- Compact image-forward prompt: subject, setting, style, camera, lighting, mood.

**Language strategy:**

- English compact prompts are conventional; keep culturally specific terms if needed.

**Length strategy:**

- Short to medium. Avoid long explanatory prose.

**Negative prompt strategy:**

- Convert negative block to `--no item, item`.
- Avoid ambiguous multiword exclusions that can be parsed independently; specify desired alternatives in the positive prompt.

**Parameter/API strategy:**

- Put parameters at the end with spaces before dashes and no punctuation after parameters.
- Common parameters: `--ar`, `--chaos`, `--quality`, `--seed`, `--raw`, `--stylize`, `--sref`, `--weird`, `--niji`, `--no`.

**Reference image strategy:**

- If using style references, keep them separate from prose when the UI supports it.

**Do not claim:**

- Do not output a Stable Diffusion-style `Negative Prompt:` block for Midjourney.

**Copy-ready output format:**

```text
[Prompt]
subject, setting, visual style, camera, lighting, mood

[Parameters]
--ar 16:9 --stylize 150 --chaos 8 --seed 1234 --raw --no text, watermark, modern cars
```

## FLUX.2 / BFL API

**Last verified:** 2026-05-28

**Source basis:**

- BFL docs recommend natural-language specificity and working without negative prompts for most FLUX models.
- FLUX.2 docs describe hex-code color steering and JSON-structured prompts for precise production control.

**Best prompt shape:**

- Natural-language descriptive prompts.
- JSON-structured prompts for production workflows and automation.

**Language strategy:**

- Use direct descriptive language. Quote exact text when text rendering matters.

**Length strategy:**

- Medium to long is acceptable, but more words do not automatically improve output. Remove filler.

**Negative prompt strategy:**

- Prefer positive replacements: "empty pathway" instead of "no crowds."
- Only include a negative field if the specific wrapper/model supports it.

**Parameter/API strategy:**

- Put aspect ratio, width, height, and seed/API fields outside prompt prose when coding.
- Use hex codes for exact brand colors.

**Reference image strategy:**

- Define each reference's role: composition, character, style, palette, product.

**Do not claim:**

- Do not assume negative prompts are supported.
- Do not merge FLUX guidance with Stable Diffusion local-wrapper habits.

**Copy-ready output format:**

```json
{
  "subject": "...",
  "background": "...",
  "lighting": "...",
  "style": "...",
  "camera_angle": "...",
  "composition": "...",
  "constraints": "positive replacements for unwanted elements"
}
```

## Stable Diffusion Local Wrappers

**Last verified:** 2026-05-28

**Source basis:** local wrapper behavior varies.

**Best prompt shape:**

- Positive prompt plus negative prompt only if the interface supports it.
- Use LoRA, ControlNet, weights, and sampler terms only when the user names that workflow.

**Do not claim:**

- Do not apply Stable Diffusion syntax to FLUX or Midjourney.

