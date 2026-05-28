# Output Contract

Choose the smallest output mode that satisfies the user.

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

