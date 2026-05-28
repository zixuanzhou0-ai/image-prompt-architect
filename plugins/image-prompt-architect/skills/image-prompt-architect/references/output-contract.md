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
