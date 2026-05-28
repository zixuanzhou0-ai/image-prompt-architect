# Examples

These examples emphasize architecture and model fit. Do not copy them blindly; adapt the concrete nouns, light, medium, camera, and constraints.

## 1. Quick Prompt

User: "Give me a prompt for a moody jazz club poster."

```text
A 1950s New Orleans basement jazz club poster, solitary singer in an ivory satin suit holding a chrome microphone, red leather booths, rain on the street-level window, low amber table lamps and blue rim light, tarnished brass trumpet in foreground, scratched lacquer piano, smoky noir atmosphere, bold cream serif title space at top, Kodak Vision3 color, soft film grain, 2:3 poster composition.
```

Knobs: make it more noir; add exact title text; switch poster ratio.

## 2. Standard Seven-Layer Prompt

User idea: "1930s rainy Shanghai Bund qipao woman."

```text
[Subject Layer]
A young Chinese woman in her early 20s, porcelain-like skin, long side-swept black curls, wearing a vintage emerald qipao with delicate gold phoenix embroidery, holding a red oil-paper umbrella, half-turned with a restrained mysterious smile.

[Environment Layer]
Wet cobblestone streets of 1930s Shanghai Bund at night during heavy rain, European-style facades, soft neon signs, distant vintage cars, Huangpu River reflections.

[Lighting and Atmosphere Layer]
Warm golden neon glow contrasts with cold blue moonlight, backlit rain streaks, volumetric light beams, thin river fog, glossy reflections.

[Material and Texture Layer]
Silk qipao sheen, embroidered thread relief, translucent oiled paper umbrella, mirror-like puddles, wet stone texture.

[Composition and Camera Layer]
Low-angle cinematic medium shot, 50mm lens feel, shallow depth of field, rule-of-thirds placement, foreground rain blur.

[Style Layer]
Old Shanghai noir romance, teal-gold palette, restrained cinematic color grade, film still.

[Context, Intent, and Tone Layer]
Lonely glamour, pre-war Shanghai nostalgia, restrained longing.

[Output Constraints]
16:9, no modern cars, no LED billboards, no smartphone-era details.
```

## 3. Critique Example

Bad prompt:

```text
beautiful girl in city, cinematic, masterpiece, high quality, aesthetic, neon
```

Diagnosis:

- Subject is generic.
- City has no time, scale, or spatial role.
- Lighting says "cinematic" but does not define source or contrast.
- No material, camera, context, or output constraints.
- Style anchors are vague filler.

Rewrite:

```text
A 24-year-old courier in a rain-dark nylon jacket, wet short hair tucked behind one ear, holding a cracked transparent umbrella at a crosswalk in late-night Taipei, scooter headlights streaking through monsoon rain, green convenience-store glow reflecting on slick asphalt, close medium shot from across the street, 85mm lens compression, shallow depth of field, damp fabric texture, water beads on umbrella ribs, restrained neo-noir realism, lonely after-work exhaustion, 16:9, avoid fashion-pose glamour and cyberpunk neon overload.
```

## 4. Model Port: Generic Prompt to Midjourney

Source idea: "A quiet product photo of a ceramic tea set."

Midjourney output:

```text
handmade celadon ceramic tea set on a dark walnut table, thin steam rising from one cup, morning window light, linen napkin, subtle glaze crackle, calm minimal still life, 80mm product photography, shallow depth of field, soft shadows, restrained editorial composition --ar 4:3 --stylize 80 --quality 1 --seed 2204 --no text, watermark, plastic shine
```

Notes:

- Parameters are at the end.
- Avoid list is converted to `--no`.

## 5. GPT Image / OpenAI Image Model

```text
Create a clean editorial image of a small independent bookstore window on a rainy evening. Preserve a realistic street-level perspective. The window sign should read exactly "NIGHT SHELF" in warm cream serif letters centered on the glass. Inside, show stacked books, a brass reading lamp, and a small handwritten staff-pick card. Use soft amber interior light against cool blue rain outside. Avoid extra text, distorted letters, or modern neon signage.
```

## 6. FLUX.2 Structured Prompt

```json
{
  "subject": "premium glass skincare bottle with matte white pump",
  "background": "warm gray stone surface with soft shadow gradient",
  "lighting": "large diffused softbox from upper left, subtle rim light on glass edge",
  "style": "minimal luxury product photography",
  "camera_angle": "eye-level three-quarter view",
  "composition": "centered product, negative space above for headline",
  "colors": "label color #F8F6F0, accent line #B76E79",
  "constraints": "clean unmarked background, solitary product, no clutter"
}
```

Notes:

- Uses positive replacements instead of "no clutter" as a negative field.
- Uses hex colors for brand precision.

## 7. Dreamina / Seedream / Jimeng Bilingual Style

```text
一张电影感人像：雨后的江南老街，青石板反光，一位穿深蓝色棉麻长衫的年轻书店老板站在木门旁，手里拿着旧书，神情安静克制。soft overcast light, wet stone texture, muted teal-gray palette, 50mm documentary portrait, shallow depth of field, subtle film grain, restrained literary mood. 避免网红摆拍、过度磨皮、现代霓虹招牌。
```

## 8. Product Photography

```text
[Subject Layer] A matte black pour-over coffee kettle with a narrow gooseneck spout, tiny condensation beads near the lid, placed beside a ceramic dripper.
[Environment Layer] Minimal morning kitchen counter, pale limestone surface, blurred linen curtain in background.
[Lighting and Atmosphere Layer] Soft side window light from left, delicate steam, calm early morning atmosphere.
[Material and Texture Layer] Powder-coated metal, ceramic glaze, limestone pores, warm paper coffee filter.
[Composition and Camera Layer] 3:2 product editorial shot, 80mm lens feel, product on lower right third, negative space for copy.
[Style Layer] Scandinavian editorial product photography, warm neutral palette.
[Context, Intent, and Tone Layer] Quiet ritual, premium but unpretentious home brewing.
[Output Constraints] no logo, no hands, no text, no plastic props.
```

## 9. Typography / Poster

```text
Create a vertical concert poster for an imaginary ambient piano performance. Exact headline text: "AFTER RAIN". Subtext: "solo piano / 9pm / hall b". Large centered typography, black ink on wet translucent vellum, rain droplets catching soft silver light, minimal monochrome palette, generous margins, editorial Swiss grid, high legibility. Avoid extra words, warped letters, ornate fonts, and busy background.
```

## 10. Series Shot List

```text
[Continuity Rules]
Early Heisei rural youth drama, Fuji color negative feeling, two high-school students, restrained gestures, blue-green shadows, warm late-summer highlights, landscapes larger than characters.

[Variation Budget]
Each frame may change location, weather, or emotional beat. Keep costume, medium, palette, and body language fixed.

[Shot Slots]
Frame 01: Two students waiting under a rural bus shelter, wide 16:9, overcast afternoon, emotional beat: almost speaking.
Frame 02: One student seen through rain-streaked bus glass, medium shot, evening sodium light, emotional beat: separation.
Frame 03: Both students standing far apart on a reservoir levee, wide shot, pale sunset, emotional beat: unsent confession.
```

## 11. Failure -> Revision Loops

### Midjourney `--no` Phrase Issue

Initial:

```text
rural 1990s student portrait, film still --ar 16:9 --no modern clothing
```

Observed risk: Midjourney may parse "modern" and "clothing" separately instead of as one precise phrase.

Revision:

```text
rural 1990s student portrait, early-Heisei school uniform, white shirt, navy sailor collar, dark pleated skirt, canvas school bag, film still, muted summer light --ar 16:9 --no smartphone, hoodie, logo, streetwear
```

### FLUX Negative Replacement

Initial:

```text
Negative Prompt: no crowds, no cars, no signs. Peaceful village lane.
```

Revision:

```text
Peaceful empty village lane at dawn, closed wooden shutters, quiet stone path, solitary bicycle leaning by a wall, soft mist, no visible traffic implied by a pedestrian-only alley and calm rural stillness.
```

### GPT Image Exact Text Repair

Observed failure: poster text came out as "AFTR RAIN".

Repair:

```text
Regenerate the poster while preserving the monochrome wet-vellum design. The headline must read exactly "AFTER RAIN" with all letters present, centered at the top in a clean bold serif font. Keep the subtext exactly "solo piano / 9pm / hall b". Remove any extra words.
```

### Series Identity Drift Repair

Observed failure: frame 2 changes the student uniforms and face shape.

Repair:

```text
Keep the same two high-school students from frame 1: same face shape, same dark hair length, same white shirt and navy sailor collar, same canvas school bags. Change only the location to a rainy bus interior and the emotional beat to separation. Preserve Fuji color negative, blue-green shadows, restrained gestures, and 1990s rural youth drama tone.
```
