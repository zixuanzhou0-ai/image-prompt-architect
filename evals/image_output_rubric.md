# Image Output Rubric

Score each generated image 0-2 per dimension.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Text accuracy | Required text is absent or wrong | Partially correct text | Exact required text with acceptable placement |
| Subject fidelity | Main subject differs from prompt | Subject mostly matches with drift | Subject clearly matches |
| Edit preservation | Important preserved areas changed | Some drift in preserved areas | Preserve/change split followed |
| Composition match | Framing ignores prompt | Some requested composition appears | Framing, lens feel, and layout match |
| Style coherence | Style conflicts or is generic | Partial style match | Style anchors are coherent and visible |
| Constraint handling | Must-avoid items appear | Minor constraint issues | Constraints are respected |
| Model-specific fit | Output shows syntax/policy mismatch | Minor model-fit issues | Output reflects model-native prompt strategy |
| Revision usefulness | Failures are unclear | Some revision path exists | Observed failure leads to clear repair prompt |
| Identity continuity | Character/product identity changes across a series | Some repeated anchors remain but identity drifts | Identity anchors stay stable across frames |
| Product geometry/material fidelity | Product shape or material differs from prompt/reference | Product mostly matches with visible drift | Geometry, material, and finish match prompt/reference |
| Text/layout legibility | Text/layout is unreadable or chaotic | Text/layout is partially legible | Text/layout is readable and placed as requested |
| Iteration improvement | Revision does not address observed failure | Revision addresses one failure partially | Revision directly targets visible failures |

Suggested gate for v1.0 image-output evidence: at least 18/24 when all dimensions apply, or at least 75% of applicable points when some dimensions are marked `not_applicable`.

## Task-Specific Gates

Apply these gates in addition to the general score.

- **Text rendering:** Text accuracy and text/layout legibility must both be greater than 0.
- **Image editing:** Edit preservation must be greater than 0.
- **Series / visual bible:** Identity continuity and constraint handling must both be greater than 0.
- **Product photography:** Product geometry/material fidelity and subject fidelity must both be greater than 0.
- **Model-port eval:** Model-specific fit must be greater than 0.

If a dimension is irrelevant to a task, mark it `not_applicable` in the record notes instead of forcing a numeric score.
