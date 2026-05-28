# Seven-Layer Image Prompt Framework

Use this framework when the user wants a single image or a tightly controlled image concept.

## The Seven Layers

1. **Subject Layer**
   - Controls the core person, object, creature, product, or scene focus.
   - Include identity, age or type, posture, expression, action, clothing, key accessories, and relationship to the frame.
   - Weak: "a beautiful girl in the rain"
   - Strong: "a young Chinese woman in her early 20s, porcelain-like skin, long side-swept black curls, wearing a vintage emerald qipao with gold phoenix embroidery, holding a red oil-paper umbrella, half-turned with a restrained mysterious smile"

2. **Environment Layer**
   - Controls time, place, weather, background objects, and spatial context.
   - Make the environment participate in the image, not merely sit behind the subject.
   - Include time period, location, weather, architecture, background elements, foreground depth cues, and scale.

3. **Lighting and Atmosphere Layer**
   - Controls light source, light direction, contrast, color temperature, haze, rain, fog, dust, bloom, and emotional mood.
   - This is often the highest-impact layer for "premium" results.
   - Use concrete light relationships: warm neon against cold moonlight, backlit rain streaks, soft window light, hard rim light, volumetric beams.

4. **Material and Texture Layer**
   - Controls surfaces and tactile realism.
   - Include fabric, skin, metal, glass, water, stone, wood, paper, grain, reflection, translucency, roughness, and wear.
   - This prevents generic plastic-looking output.

5. **Composition and Camera Layer**
   - Controls frame, lens, distance, angle, depth of field, and visual hierarchy.
   - Include shot type, lens feel, camera angle, subject scale, rule of thirds, negative space, leading lines, foreground framing, and bokeh.

6. **Style Layer**
   - Controls visual language.
   - Include medium, genre, film stock, art movement, color grade, renderer, painterly language, or cinematographic reference.
   - Keep style anchors few and coherent. Too many unrelated references dilute the output.

7. **Era and Artistic Tone Layer**
   - Controls cultural time, narrative feeling, symbolism, and deeper emotional interpretation.
   - Include period mood, nostalgia, alienation, mono no aware, noir fatalism, post-bubble suburbia, folk ritual quality, or editorial elegance.

## Recommended Sentence Structure

```text
[Subject: core object + attributes + posture + action],
in [Environment: time + place + spatial elements],
with [Lighting and atmosphere: source + direction + color + mood],
featuring [Material and texture: surfaces + reflections + tactile details],
captured through [Composition and camera: shot + lens + angle + framing],
in [Style: medium + visual language + color grade],
evoking [Era and artistic tone: cultural mood + narrative meaning],
[quality and technical constraints].
```

## How to Use It Well

- Put the subject early. Most models treat early content as more central.
- Make each layer specific. A layer title alone does nothing.
- Let the environment and lighting support the emotion.
- Put camera language after the scene is clear.
- Use repeated anchors only for the most important style concepts.
- Add negative constraints only when they prevent common failure modes.

## Common Failure Modes

- **Template-only prompt**: layers exist, but details are generic.
- **Style overload**: five unrelated style references compete.
- **Lighting omitted**: output looks flat even with a good subject.
- **No material cues**: output becomes glossy, plastic, or vague.
- **No camera layer**: composition becomes default portrait framing.

