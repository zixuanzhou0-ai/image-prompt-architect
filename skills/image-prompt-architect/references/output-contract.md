# Output Contract

Choose the smallest output mode that satisfies the user.

## Copy-Ready Definition

Copy-ready means the final prompt contains no teaching labels, Markdown headings, bracketed placeholders, or explanation inside the prompt text.

Exceptions:

- target-native structured JSON when the target adapter recommends it;
- API request wrappers when the user explicitly asks for code/API use;
- separate parameter fields when the target interface requires fields.

## Quick Prompt

Use when the user asks for one prompt quickly.

Output:

```markdown
**Prompt**
<copy-ready prompt>

**Knobs**
- <2-3 concrete iteration controls>
```

Do not include long explanations unless the user asks to learn the structure.
Omit model notes in quick mode unless model syntax matters.

## Prompt Compression / Final Render Prompt

Use when the user already has a long prompt, seven-layer draft, style bible note, or analysis block and needs the shortest clean prompt that should be pasted into the target model.

Output:

```markdown
**Priority Stack**
1. <subject/readability priority>
2. <composition/light priority>
3. <main style priority>
4. <constraints/edit priority>

**Final Render Prompt**
<copy-ready prompt, usually 80-160 words for GPT Image-like models, with no headings inside the prompt>

**Dropped / Compressed**
- <redundant style anchor, weak texture detail, duplicate background prop, or low-priority artifact removed>
```

Rules:

- Keep one main style anchor and at most one weak modifier for GPT Image-like models.
- If the source uses grain, scan, VHS, CRT, halftone, photocopy, dust, or compression artifacts, keep only the artifact that matters and mark it subtle unless the user explicitly wants a dirty image.
- Preserve hard constraints such as exact text, product geometry, identity, aspect ratio, and must-include elements.

## Standard Build

Use when the user asks to create or rewrite a prompt with structure.

Output:

```markdown
**Architecture**
<seven-layer | system | hybrid | compact natural language, with one-sentence reason>

**Tagged Prompt**
<labeled layers or systems>

**Copy-Ready Prompt**
<clean prompt without teaching labels>

**Model Notes**
<language, length, parameters, reference-image, and negative handling>

**Knobs**
- <specific edit 1>
- <specific edit 2>
- <specific edit 3>
```

## Critique

Use when the user provides an existing prompt or asks why an image failed.

Output:

```markdown
**Diagnosis**
| Severity | Issue | Why It Matters | Fix |
| --- | --- | --- | --- |

**Missing Controls**
<subject/environment/light/material/camera/style/constraint gaps>

**Contradictions**
<media, era, camera, lighting, or model syntax conflicts>

**Rewrite**
<copy-ready corrected prompt>

**Iteration Plan**
<2-4 edits to try after the next image>
```

## Revision Prompt From Failure

Use when the user describes a failed generated image or gives image-output feedback such as dirty texture, weak style, wrong text, subject drift, background clutter, or style overpowering the subject.

Output:

```markdown
**Failure Type**
<dirty render / text error / subject drift / overstyle / weak style / background clutter / low subject readability>

**Observed Cause**
<what the generated image visibly did wrong, without adding new creative goals>

**Preserve**
<what should stay unchanged from the previous prompt or image>

**Change**
<what must be corrected, reduced, emphasized, or replaced>

**Revision Prompt**
<copy-ready repair prompt>

**Next Check**
<one sentence naming what to inspect after regeneration>
```

Revision prompts should be narrow. Fix the failure before adding new creative ideas.
When the user gives concrete image-output feedback, use the failure labels and repair rules in `image-feedback-loop.md`.

## Reference Image Role Planning

Use when one or more reference images are part of the workflow.

Output:

```markdown
**Reference Role Plan**
| Reference | Controls | Must Not Control |
| --- | --- | --- |
| ref 1 | <identity / product geometry / pose / composition / palette / style> | <text / background / logo / unwanted artifacts> |

**Prompt**
<copy-ready prompt that names each reference role in plain language>
```

When product shape or identity matters, make that role explicit before style or palette. If a reference image contains unwanted text, logo, background clutter, or lighting, say not to preserve it.

## Model Port

Use when translating a prompt from one model to another.

Output:

```markdown
**Port Target**
<source model -> target model>

**Risks**
<what will break if copied directly>

**Converted Prompt**
<target-native prompt>

**Parameter / Negative Handling**
<e.g. Midjourney --no, FLUX positive replacement, GPT Image preserve/change instructions>

**What Changed**
<short list of changes>
```

## Target-Native Copy-Ready Examples

Midjourney:

```text
handmade celadon ceramic tea set on a dark walnut table, thin steam, morning window light, linen napkin, subtle glaze crackle, calm minimal still life, 80mm product photography, shallow depth of field --ar 4:3 --stylize 80 --quality 1 --seed 2204 --no text, watermark, plastic shine
```

FLUX natural language:

```text
Premium glass skincare bottle with matte white pump on a warm gray stone surface, large diffused softbox from upper left, subtle rim light on the glass edge, centered minimal luxury product composition, clean unmarked background, solitary product, uncluttered stone surface, label color #F8F6F0 with accent line #B76E79.
```

FLUX structured prompt content:

```json
{
  "subject": "premium glass skincare bottle with matte white pump",
  "background": "warm gray stone surface with soft shadow gradient",
  "lighting": "large diffused softbox from upper left, subtle rim light on glass edge",
  "constraints": "clean unmarked background, solitary product, uncluttered stone surface"
}
```

BFL API wrapper example:

```json
{
  "prompt": "<natural-language prompt or stringified structured prompt>",
  "width": 1024,
  "height": 1024
}
```

GPT Image editing:

```text
Replace only the background with a softly lit bookstore interior. Preserve the person's face, pose, clothing, and camera angle. Add a window sign that reads exactly "NIGHT SHELF" in warm cream serif letters. Avoid extra text or warped letters.
```

## Series Bible

Use for multiple images, cinematic stills, style-consistent sets, or visual worlds.

Output:

```markdown
**Series Premise**
<one paragraph>

**Continuity Rules**
- <must remain fixed>

**Variation Budget**
- <what may change>
- Limit each frame to 2-3 major changes.

**Style Bible**
<spatial, character, color, medium, composition, lighting, narrative systems>

**Shot Slots**
| Frame | Subject Action | Location | Camera | Lighting | Emotional Beat | Required Anchors | Allowed Variation |
| --- | --- | --- | --- | --- | --- | --- | --- |

**Per-Shot Prompts**
<copy-ready prompts for each frame>
```
