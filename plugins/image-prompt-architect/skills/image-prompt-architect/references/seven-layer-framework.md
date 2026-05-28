# Seven-Layer Image Prompt Framework

Use this framework for one image that needs precise control.

## The Seven Layers

1. **Subject Layer**
   - Controls the core person, object, creature, product, or scene focus.
   - Include identity, type, posture, expression, action, clothing, accessories, and relationship to the frame.

2. **Environment Layer**
   - Controls time, place, weather, background objects, scale, and spatial context.
   - The environment should shape the image, not merely decorate it.

3. **Lighting and Atmosphere Layer**
   - Controls light source, direction, contrast, color temperature, haze, rain, fog, dust, bloom, and mood.
   - This is often the highest-impact layer for perceived quality.

4. **Material and Texture Layer**
   - Controls surfaces and tactile realism: fabric, skin, metal, glass, water, stone, wood, paper, grain, reflection, translucency, roughness, and wear.

5. **Composition and Camera Layer**
   - Controls frame, lens, distance, angle, depth of field, visual hierarchy, negative space, leading lines, and foreground/background staging.

6. **Style Layer**
   - Controls visual language: medium, genre, film stock, art movement, color grade, rendering style, or cinematographic reference.
   - Keep style anchors coherent. Too many unrelated references dilute the output.

7. **Context, Intent, and Tone Layer**
   - Controls period context, cultural cues, symbolic meaning, emotional temperature, and intended viewer response.
   - This replaces the narrower "era and artistic tone" label.

## Output Constraints Block

Keep this outside the seven creative layers:

```text
[Output Constraints]
aspect ratio:
resolution or target surface:
text to render exactly:
must include:
avoid / replacement strategy:
brand/safety/platform constraints:
```

Do not bury these constraints inside style words. They are production requirements.

Model-native handling:

- Midjourney: convert avoid items to `--no`.
- FLUX: rewrite avoid items as positive replacements.
- GPT Image: use natural-language avoid/preserve instructions.

## Recommended Sentence Structure

```text
[Subject: core object + attributes + posture + action],
in [Environment: time + place + spatial elements],
with [Lighting and atmosphere: source + direction + color + mood],
featuring [Material and texture: surfaces + reflections + tactile details],
captured through [Composition and camera: shot + lens + angle + framing],
in [Style: medium + visual language + color grade],
evoking [Context, intent, and tone: cultural context + emotional meaning].

[Output Constraints: aspect ratio + exact text + must-have + avoid/replacement strategy]
```

## Bad to Good

Weak template fill:

```text
[Subject] beautiful woman
[Environment] city at night
[Lighting] cinematic lighting
[Material] high quality details
[Composition] good composition
[Style] artistic
[Tone] nostalgic
```

Why it fails: every layer exists, but none gives the model drawable specifics.

Concrete fill:

```text
[Subject] A 32-year-old jazz singer in a tailored ivory satin suit, one hand resting on a chrome microphone stand, eyes lowered as if holding back a confession.
[Environment] A narrow 1950s basement club in New Orleans after midnight, red leather booths, cigarette haze, brass instruments stacked near a small stage, rain visible through a street-level window.
[Lighting] Low amber table lamps, a single cool blue rim light from the stairwell, smoky volumetric beams crossing the stage.
[Material] Satin lapels with soft highlights, tarnished brass trumpet, damp black-and-white tile floor, scratched lacquer piano.
[Composition] Medium-wide 35mm film still, singer placed left third, microphone silhouette in foreground, deep background bokeh.
[Style] Kodak Vision3-style color, restrained noir musical drama, soft film grain.
[Context, Intent, and Tone] Late-night loneliness, postwar glamour wearing thin, intimate performance before an almost-empty room.
[Output Constraints] 16:9, no modern microphones, no LED panels, no smartphone-era details.
```

Exact text constraint example:

```text
[Output Constraints]
Vertical 2:3 poster. Render the headline exactly as "AFTER RAIN" and the subtext exactly as "solo piano / 9pm / hall b". Keep typography legible, centered, and free of extra words.
```

## Common Failure Modes

- Template-only prompt: headings exist, details are generic.
- Style overload: unrelated references compete.
- Lighting omitted: output looks flat.
- No material cues: output becomes glossy or plastic.
- No camera layer: composition defaults to centered portrait.
- Constraints buried in prose: platform or text requirements are ignored.
