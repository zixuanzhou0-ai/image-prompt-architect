# Style Mode Gate

Use this reference when a user asks for an image prompt and the request could be either plain or stylized.

The goal is not to maintain a fixed style-name library. The goal is to ask the right questions, search when needed, translate references into visible traits, and place those traits in the right prompt layer.

## Default Gate

If the user has not clearly chosen a style direction, ask once:

```text
Do you want a plain prompt or a stylized prompt?
```

- **Plain prompt**: build the prompt from the user's stated subject, setting, camera, lighting, material, and constraints. Do not add extra style anchors.
- **Stylized prompt**: ask for optional references before drafting.
- **Fast request exception**: if the user asks for speed or "just give me the prompt," default to a plain prompt and mention that a stylized variant can be made next.

## Stylized Prompt Intake

When the user chooses stylized mode, ask whether they have preferred references for any of these optional slots:

- Narrative / cinema / director / film / literary mood.
- Camera / film stock / lens / digital or mobile imaging texture.
- Fashion / styling / designer / garment silhouette.
- Artist / art movement / medium.
- Material / craft / surface texture.
- Color science / palette / grade.
- Reference images, style references, image prompts, or model-native reference tools.

Use only the slots that matter to the image. Keep the rest empty.

## Web Recommendation Rule

If the user chooses stylized mode but has no references:

1. Search the web for current or historically relevant references that fit the prompt's subject, audience, medium, and target model.
2. Recommend 2-4 style directions, not a hardcoded name list.
3. Present recommendations as visual directions such as "restrained winter cinema + muted film color" or "sculptural avant-garde couture + hard studio flash."
4. After the user picks a direction, translate it into visible traits before writing the final prompt.

Do not recommend from local memory, prior chat context, or a fixed in-skill library when the user explicitly needs fresh or open-ended style discovery.

## Cross-Domain Style Anchors

Style anchors can come from multiple domains:

- Cinema and literature often control story mood, pacing, gesture, composition, and emotional temperature.
- Camera, film, and lens anchors control color, grain, sharpness, dynamic range, depth of field, and framing.
- Fashion anchors control silhouette, tailoring, fabric, volume, accessories, and posture.
- Art movements and media control mark-making, rendering language, abstraction level, and surface treatment.
- Architecture and craft anchors control spatial logic, geometry, material systems, and ornament.

This cross-domain approach is inspired by prompt workflows that treat well-known creative references as compressed visual anchors. Keep it as a method, not as a fixed list of names.

## Translation Rule

Names and titles must not stand alone. Pair each anchor with visible traits.

Good patterns:

```text
designer/reference + silhouette + fabric/material + construction detail
camera/film + lens/focal behavior + color traits + grain/sharpness
director/film/literary mood + emotional beat + light + composition
artist/movement + medium + mark-making + palette + surface
```

Weak patterns:

```text
in the style of <name>
<name>, <name>, <name>, beautiful cinematic
exact scene from <film>
official <brand> campaign
```

## Anchor Budget

Use at most 2-3 primary style anchors in one prompt unless the user explicitly wants a collage or comparison test.

If more anchors are present, group them by role and remove weak or redundant ones. Prioritize visible controls over name stacking.

## Placement

- Subject layer: styling, garment identity, pose, expression, accessories.
- Material layer: fabric, metal, skin, paper, grain, surface wear, craft.
- Camera/composition layer: camera body, lens, focal length, shot scale, angle, depth of field.
- Style layer: film stock, color grade, art medium, movement, rendering language.
- Context/tone layer: cinema, director, film, literature, symbolic mood, era, viewer response.

For model-specific handling, apply `references/model-adapters.md` after this reference.

## Output Notes

For stylized outputs, include a short `Style Anchors Used` block outside the copy-ready prompt:

```text
Style Anchors Used:
- Narrative anchor: <reference or direction> -> <visible traits>
- Camera/color anchor: <reference or direction> -> <visible traits>
- Fashion/material anchor: <reference or direction> -> <visible traits>
```

For plain outputs, do not include this block unless useful for explaining why no extra style was added.
