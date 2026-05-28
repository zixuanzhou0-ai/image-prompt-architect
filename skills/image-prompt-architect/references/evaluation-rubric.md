# Evaluation Rubric

Score each dimension 0-2. A production-ready prompt should score at least 16/20 and have no 0 in model fit or constraint handling.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Subject specificity | Generic subject | Some attributes | Concrete identity, pose, action, visual details |
| Environment | Background label only | Place/time present | Space shapes story and composition |
| Lighting | Vague "cinematic" | Some light cues | Source, direction, color, contrast, atmosphere |
| Materiality | No tactile cues | Some textures | Surfaces, reflection, wear, medium-specific detail |
| Composition | No camera grammar | Basic shot or angle | Lens, framing, scale, depth, hierarchy |
| Style coherence | Many competing styles | Mostly coherent | Few strong, compatible anchors |
| Context and tone | Empty mood words | Some emotion | Cultural context, symbolic intent, viewer response |
| Output constraints | Buried or absent | Some constraints | Aspect/text/must-have/must-avoid clearly separated |
| Model fit | Wrong syntax or assumptions | Mostly compatible | Native prompt shape, parameters, negative handling |
| Iteration readiness | No knobs | Generic knobs | Specific high-leverage next edits |

## Release Gate

- 18-20: strong prompt.
- 16-17: usable, needs targeted polishing.
- 12-15: draft quality.
- Below 12: rewrite architecture or gather more user intent.

