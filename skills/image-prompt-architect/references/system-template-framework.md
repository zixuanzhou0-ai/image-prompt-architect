# Multi-System Modular Prompt Template

Use this framework for cinematic series, consistent visual grammar, story-world prompts, and sets of images that must feel like they belong to the same film, campaign, or visual universe.

## Core Idea

The seven-layer framework decomposes an image by visible elements. The multi-system template decomposes an image by functional control systems.

- Seven-layer structure: "What parts make up this picture?"
- System template: "What visual systems govern this world?"

The system template is powerful because it repeats a few key anchors across multiple systems: period, medium, color science, emotional tone, spatial logic, and character behavior.

## Core Systems

1. **Premise System**
   - State the series format, genre, era, subject theme, and intended continuity.
   - Example: "a set of early Heisei 80s/90s Japanese youth drama film stills..."

2. **Spatial System**
   - Define the world geography, recurring locations, scale, and environmental narrative role.
   - Make space functional: the location shapes the story, emotion, and composition.
   - Include ratios such as character-to-environment scale when useful.

3. **Character System**
   - Define people, clothing, body language, facial affect, actions, and what to avoid.
   - For cinematic work, restrained actions often outperform dramatic poses.
   - Include behavioral vocabulary: withheld emotion, misaligned gaze, adolescent hesitation, emotional ellipsis.

4. **Color System**
   - Define color science, palette, saturation, highlight and shadow behavior.
   - Good prompts name color relationships, not only colors.
   - Example: cobalt sky, cyan-green shadow cast, warm orange sun, slight magenta highlight shift.

5. **Medium System**
   - Define film stock, grain, scan, lens artifacts, broadcast texture, analog flaws, and image materiality.
   - This is often the difference between "AI picture" and "found film still."

6. **Composition System**
   - Define recurring framing strategies, camera distance, subject scale, negative space, frames within frames, and landscape ratio.
   - This system keeps a series visually consistent.

7. **Lighting and Atmosphere System**
   - Define weather, light sources, diffusion, haze, time of day, and emotional weather.
   - Keep it tied to the premise, not pasted from a generic cinematic keyword list.

8. **Narrative and Emotion System**
   - Define the unspoken story, emotional temperature, symbolic motifs, and what the image should feel like before it says anything.
   - Use this to prevent beautiful but empty images.

9. **Quality and Exclusion System**
   - Define technical target and common failure exclusions.
   - Avoid broad "masterpiece" piles unless the target model benefits from them.

## Blank Template

```text
A series of [era/genre/medium] image stills about [relationship/story theme], set in [season] at [location set]. The images should feel like [core aesthetic premise].

[Spatial System] ...

[Character System] ...

[Color System] ...

[Medium System] ...

[Composition System] ...

[Lighting and Atmosphere System] ...

[Narrative and Emotion System] ...

[Quality and Exclusion System] ...
```

## When It Beats Seven Layers

- The user wants multiple images with one visual language.
- The style is more important than a single subject.
- The output should feel like stills from the same movie.
- The prompt needs world rules, not just an object description.

## Common Failure Modes

- **System shell without content**: all headings, no specific visual law.
- **Weak anchor repetition**: the core style appears once and disappears.
- **Conflicting media cues**: VHS, IMAX, watercolor, and 3D render all fight.
- **Character treated as fashion model**: cinematic restraint is lost.
- **Location becomes wallpaper**: spatial system does not affect story or composition.

