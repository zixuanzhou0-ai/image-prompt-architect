# Multi-System Modular Prompt Template

Use this framework for cinematic series, consistent visual grammar, style bibles, and image sets that should feel like they belong to the same world.

## Core Idea

The seven-layer framework decomposes one image by visible elements. The multi-system template decomposes a visual world by control systems.

- Seven-layer structure: "What parts make up this picture?"
- System template: "What rules govern this world?"

## Core Systems

1. **Premise System**
   - State format, genre, era, subject theme, and intended continuity.

2. **Spatial System**
   - Define geography, recurring locations, scale, and how space participates in story.

3. **Character System**
   - Define identity rules, clothing, behavior, gestures, facial affect, and forbidden pose language.

4. **Color System**
   - Define color science, palette, saturation, highlight and shadow behavior.

5. **Medium System**
   - Define film stock, grain, scan, lens artifacts, broadcast texture, analog flaws, or rendering medium.

6. **Composition System**
   - Define recurring framing, camera distance, lens grammar, subject scale, negative space, and dividers.

7. **Lighting and Atmosphere System**
   - Define weather, time of day, light sources, diffusion, haze, and emotional weather.

8. **Narrative and Emotion System**
   - Define unspoken story, emotional temperature, symbolic motifs, and what the images should imply.

9. **Quality and Exclusion System**
   - Define output gate and common failure exclusions.
   - This is not a world system; it is a production filter.

## Series Controls

### Continuity System

List what must stay fixed across all images:

- era and cultural context;
- medium and color science;
- character identity and costume rules;
- recurring locations or object motifs;
- lens grammar and composition habits;
- emotional temperature;
- visual motifs.

### Identity Lock

State what must never drift:

- character facial constants;
- body type, age, hair, costume, and prop invariants;
- product geometry and brand-shape invariants;
- recurring prop invariants;
- forbidden identity drift.

### Continuity Anchor Budget

Repeat only 3-5 core anchors across the series. Avoid repeating the entire prompt unchanged; repeat the identity, medium, palette, motif, and camera grammar anchors that truly matter.

### Variation Budget

List what may change per image:

- location;
- weather;
- time of day;
- camera distance;
- character action;
- emotional beat.

Limit each frame to 2-3 major changes. Too much variation breaks series identity.

### Shot Slot Template

```text
Frame:
subject action:
location:
camera:
lighting:
emotional beat:
identity lock:
required continuity anchors:
per-frame delta:
failure watch item:
copy-ready prompt:
```

## Blank Template

```text
[Premise System]
A series of [era/genre/medium] image stills about [relationship/story theme], set in [season] across [location set]. The images should feel like [core aesthetic premise].

[Continuity System]
Must remain fixed: [era], [medium], [palette], [characters], [lens grammar], [motifs], [emotional temperature].

[Identity Lock]
Must never drift: [face/body/costume/product geometry/recurring prop].

[Continuity Anchor Budget]
Repeat only: [3-5 core anchors].

[Variation Budget]
May change per frame: [location], [weather], [time of day], [camera distance], [action], [emotional beat]. Limit each image to 2-3 major changes.

[Spatial System]
...

[Character System]
...

[Color System]
...

[Medium System]
...

[Composition System]
...

[Lighting and Atmosphere System]
...

[Narrative and Emotion System]
...

[Quality and Exclusion System]
...

[Shot Slots]
Frame 01 ...
Frame 02 ...
Frame 03 ...
```

## When It Beats Seven Layers

- The user wants multiple images with one visual language.
- The style is more important than a single subject.
- The output should feel like stills from the same film.
- The prompt needs world rules, not just object description.

## Common Failure Modes

- System shell without content: all headings, no specific visual law.
- Weak continuity: each image looks good but unrelated.
- No variation budget: the series drifts too far or repeats too much.
- Conflicting media cues: VHS, IMAX, watercolor, and 3D render compete.
- Location becomes wallpaper: spatial system does not affect story or composition.
