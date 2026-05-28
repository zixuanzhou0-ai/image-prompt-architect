# Model Adapters

Model behavior changes. Treat this file as a dated heuristic matrix, not permanent truth. Prefer official docs and local tests over inherited prompt lore.

## Adapter Schema

Each adapter tracks:

- **Docs last checked**
- **Fixture coverage last updated**
- **Image-output eval last run**
- **Confidence**
- **Primary docs**
- **Local test coverage**
- **Applies to**
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

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-28
**Image-output eval last run:** none
**Confidence:** high for API behavior; medium for creative prompt heuristics
**Primary docs:** https://platform.openai.com/docs/guides/image-generation
**Local test coverage:** `tests/fixtures/bad_gpt_image_keyword_pile.txt`, `tests/fixtures/warn_gpt_image_edit_no_preserve.txt`, `tests/fixtures/warn_gpt_image_unquoted_text.txt`, `tests/fixtures/warn_gpt_image_pixel_perfect_claim.txt`, `tests/fixtures/warn_gpt_image_reference_without_role.txt`, `tests/fixtures/warn_gpt_image_label_with_unquoted_words.txt`, `tests/fixtures/good_gpt_image_edit_preserve_change.txt`, `tests/fixtures/good_gpt_image_text_quoted.txt`, `tests/fixtures/good_gpt_image_blank_label.txt`; no image-output eval
**Applies to:** API and ChatGPT-like image workflows

**Source basis:**

- OpenAI image generation docs distinguish Responses API and Image API.
- Responses API is suited to conversational and multi-turn image generation/editing; Image API is suited to direct image operations.
- The Responses image generation tool may revise prompts for performance and expose `revised_prompt`.
- Mask editing is prompt-guided and should not be treated as pixel-perfect geometry control.

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
- Do not promise exact text/layout reproduction from prompt alone.
- Do not claim masks are followed with pixel-perfect precision.
- Do not claim English is always better.

**Copy-ready output format:**

```text
Create an image of ... Preserve ... Change ... Render the exact text "...". Avoid ...
```

## Grok Imagine - Image Generation

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-29
**Image-output eval last run:** none
**Confidence:** medium
**Primary docs:** https://docs.x.ai/docs/guides/image-generation
**Local test coverage:** examples only; no controlled image-output eval
**Applies to:** API and Grok Imagine-style image generation

**Source basis:**

- xAI Imagine docs state Grok Imagine models generate images from text prompts and expose settings such as output count, aspect ratio, resolution, and response format.

**Best prompt shape:**

- Structured English prompts often work well in practice, but treat this as a heuristic unless the user has test results.
- Seven-layer and system prompts are useful when the user wants explicit control.

**Language strategy:** Use English for technical art-direction terms; keep Chinese cultural terms when semantically important.

**Length strategy:** Medium to long prompts are acceptable when each part is concrete.

**Negative prompt strategy:** Use concise avoid statements. Do not overstuff exclusions.

**Parameter/API strategy:** Keep aspect ratio, resolution, output count, and response format outside prompt prose when coding.

**Reference image strategy:** Name whether references control style, subject, or composition.

**Do not claim:** Do not claim official proof that Grok is uniquely optimized for long cinematic prompts.

**Copy-ready output format:**

```text
<seven-layer or system prompt>, avoid <specific failure modes>. Aspect ratio: ...
```

## Grok Imagine - Image Editing

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-28
**Image-output eval last run:** none
**Confidence:** medium
**Primary docs:** https://docs.x.ai/docs/guides/image-generation
**Local test coverage:** none
**Applies to:** API/editing workflows

**Best prompt shape:** State what to preserve, what to change, and which reference controls style or identity.

**Do not claim:** Do not treat editing strategy as the same as text-to-image generation.

## Grok Imagine - Video / Image-to-Video

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-28
**Image-output eval last run:** none
**Confidence:** low
**Primary docs:** https://docs.x.ai/docs/guides/image-generation
**Local test coverage:** none
**Applies to:** video/image-to-video workflows

**Best prompt shape:** Use motion, temporal continuity, camera movement, and first/last-frame intent. This skill is prompt-text oriented; for video generation, defer to a video-specific skill when available.

## Dreamina / Seedream / Jimeng

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-28
**Image-output eval last run:** none
**Confidence:** low for Dreamina/Jimeng UI-specific behavior; medium for broad bilingual prompt heuristics
**Primary docs:** local project rules when present; Seedream technical reports are model-family evidence, not Dreamina/Jimeng UI evidence
**Local test coverage:** `tests/fixtures/good_chinese_dreamina.txt`, `tests/fixtures/good_chinese_seven_layer.txt`, `tests/fixtures/good_chinese_short_labels.txt`, `tests/fixtures/good_chinese_no_spaces.txt`, `tests/fixtures/bad_chinese_filler_only.txt`, `tests/fixtures/bad_chinese_too_short.txt`, `tests/fixtures/good_bilingual_model_port.txt`; no image-output eval
**Applies to:** mixed/unknown UI and local workflows

**Source basis:**

- Project-local AGENTS rules may override this public adapter.
- Seedream technical reports describe a model family; they do not prove Dreamina/Jimeng UI prompt best practices.

**Best prompt shape:**

- Combine natural-language intent with structured aesthetic keywords when useful.
- Follow local prompt libraries, checklist, and model notes if present.

**Language strategy:** Chinese is useful for culturally specific scenes; English is useful for common technical visual terms.

**Length strategy:** Use medium-length prompts with clear subject, scene, style, camera, and constraints.

**Negative prompt strategy:** Keep avoid lists short and model-specific.

**Parameter/API strategy:** Do not set a public universal model default unless local instructions require it.

**Reference image strategy:** State whether references control identity, pose, style, or layout.

**Do not claim:**

- Do not claim a public universal default model version.
- Do not imply Seedream technical report behavior, Dreamina UI behavior, and Jimeng UI behavior are identical.

**Copy-ready output format:**

```text
自然语言概念段落 + 三段式美学关键词 + 简短避免项
```

## Midjourney

**Docs last checked:** 2026-05-29
**Fixture coverage last updated:** 2026-05-29
**Image-output eval last run:** none
**Confidence:** high for parameter syntax; medium for creative heuristics
**Primary docs:** https://docs.midjourney.com/docs/parameter-list and https://docs.midjourney.com/docs/no
**Local test coverage:** `tests/fixtures/good_midjourney.txt`, `tests/fixtures/good_midjourney_oref_profile.txt`, `tests/fixtures/good_midjourney_chaos_alias.txt`, `tests/fixtures/good_midjourney_video.txt`, `tests/fixtures/good_midjourney_loop.txt`, `tests/fixtures/bad_midjourney_negative_block.txt`, `tests/fixtures/bad_midjourney_params_middle.txt`, `tests/fixtures/bad_midjourney_value_punctuation.txt`, `tests/fixtures/warn_midjourney_legacy_cw.txt`, `tests/fixtures/warn_midjourney_unknown_future_param.txt`, `tests/fixtures/bad_midjourney_unknown_param_strict_model_params.txt`; no image-output eval
**Applies to:** Midjourney prompt UI

**Source basis:**

- Midjourney docs state parameters belong at the end of the prompt.
- The `--no` parameter is the native way to tell Midjourney what to exclude.

**Best prompt shape:** Compact image-forward prompt: subject, setting, style, camera, lighting, mood.

**Language strategy:** English compact prompts are conventional; keep culturally specific terms if needed.

**Length strategy:** Short to medium. Avoid long explanatory prose.

**Negative prompt strategy:**

- Convert negative block to `--no item, item`.
- Avoid ambiguous multiword exclusions that can be parsed independently; specify desired alternatives in the positive prompt.

**Parameter/API strategy:**

- Put parameters at the end with spaces before dashes and no punctuation after parameters.
- Current parser-covered parameters include: `--ar`, `--aspect`, `--chaos`, `--c`, `--quality`, `--q`, `--seed`, `--raw`, `--stylize`, `--s`, `--sref`, `--sw`, `--sv`, `--oref`, `--profile`, `--p`, `--iw`, `--weird`, `--w`, `--niji`, `--no`, `--repeat`, `--r`, `--tile`, `--stealth`, `--public`, `--draft`, `--motion`, `--loop`, `--end`, `--bs`, and `--video`.
- Treat `--loop` and `--video` as flag-like. Treat `--motion`, `--end`, and `--bs` as value parameters.
- Legacy/deprecated parser-covered parameters: `--cref`, `--cw`, `--style`. Treat legacy parameters as warnings until confirmed against the current UI.
- Unknown parameters are warnings by default; `prompt_lint.py --strict-model-params` upgrades unknown Midjourney parameters to critical failures.

**Reference image strategy:** If using style references, keep them separate from prose when the UI supports it.

**Do not claim:** Do not output a Stable Diffusion-style `Negative Prompt:` block for Midjourney.

**Explanatory output format:**

```text
Prompt: subject, setting, visual style, camera, lighting, mood
Parameters: --ar 16:9 --stylize 150 --chaos 8 --seed 1234 --raw --no text, watermark, modern cars
```

**Copy-ready output format:**

```text
subject, setting, visual style, camera, lighting, mood --ar 16:9 --stylize 150 --chaos 8 --seed 1234 --raw --no text, watermark, modern cars
```

## FLUX.2 / BFL API

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-28
**Image-output eval last run:** none
**Confidence:** high for negative-prompt and API-field guidance; medium for creative heuristics
**Primary docs:** https://docs.bfl.ai/guides/prompting_unified_technical and https://docs.bfl.ai/flux_2/flux2_text_to_image
**Local test coverage:** `tests/fixtures/good_flux_structured.txt`, `tests/fixtures/good_flux_positive_replacements.txt`, `tests/fixtures/bad_flux_negative.txt`, `tests/fixtures/bad_flux_invalid_hex.txt`, `tests/fixtures/bad_flux_plain_negation.txt`, `tests/fixtures/bad_flux_multiple_plain_negation_phrases.txt`, `tests/fixtures/warn_flux_single_plain_negation_phrase.txt`; no image-output eval
**Applies to:** BFL API / FLUX.2 workflows

**Source basis:**

- BFL docs recommend natural-language specificity and working without negative prompts for most FLUX models.
- FLUX.2 docs describe hex-code color steering and JSON-structured prompt content for precise production control.

**Best prompt shape:**

- Natural-language descriptive prompts.
- Structured prompt content for production workflows and automation.

**Language strategy:** Use direct descriptive language. Quote exact text when text rendering matters.

**Length strategy:** Medium to long is acceptable, but more words do not automatically improve output. Remove filler.

**Negative prompt strategy:**

- Prefer positive replacements: "empty pathway" instead of "no crowds."
- Only include a negative field if the specific wrapper/model supports it.

**Parameter/API strategy:**

- Put aspect ratio, width, height, and seed/API fields outside prompt prose when coding.
- Use hex codes for exact brand colors.

**Reference image strategy:** Define each reference's role: composition, character, style, palette, product.

**Do not claim:**

- Do not assume negative prompts are supported.
- Do not merge FLUX guidance with Stable Diffusion local-wrapper habits.

**Natural-language output format:**

```text
Premium glass skincare bottle with matte white pump on a warm gray stone surface, large diffused softbox from upper left, subtle rim light on the glass edge, centered minimal luxury product composition, clean unmarked background, solitary product, uncluttered stone surface, label color #F8F6F0 with accent line #B76E79.
```

**Structured prompt content:**

```json
{
  "subject": "...",
  "background": "...",
  "lighting": "...",
  "style": "...",
  "constraints": "positive replacements for unwanted elements"
}
```

**BFL API wrapper:**

```json
{
  "prompt": "<natural-language prompt or stringified structured prompt>",
  "width": 1024,
  "height": 1024
}
```

## Stable Diffusion Local Wrappers

**Docs last checked:** 2026-05-28
**Fixture coverage last updated:** 2026-05-28
**Image-output eval last run:** none
**Confidence:** medium
**Primary docs:** local wrapper documentation varies
**Local test coverage:** none
**Applies to:** local wrapper / UI workflows

**Best prompt shape:**

- Positive prompt plus negative prompt only if the interface supports it.
- Use LoRA, ControlNet, weights, and sampler terms only when the user names that workflow.

**Do not claim:** Do not apply Stable Diffusion syntax to FLUX or Midjourney.
