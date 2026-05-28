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

Suggested gate for v1.0 image-output evidence: at least 12/16 per case, with no 0 in subject fidelity, constraint handling, or edit preservation when editing is the task.
