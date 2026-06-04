# Image Feedback Loop

Use this reference when a generated image failed and the user needs a revision prompt.

## Review Shape

For a single image, use `scripts/create_prompt_feedback_review.py` to create `prompt_feedback_review.json`.
For Open Style Atlas batches, use `scripts/review_generated_images.py` to create `generated_review.json`.
Both paths use the shared taxonomy in `scripts/feedback_taxonomy.py`.

Required review decisions:

- Assign 0/1/2 scores where possible.
- Add one or more failure labels.
- Write the observed cause in concrete visual terms.
- Fill preserve/change only when the default would be wrong.
- Generate the revision with `scripts/make_feedback_revision.py` or `scripts/make_revision_prompts.py`.

## Failure Labels

- `texture_noise_overload`: grain, scan noise, dirty speckles, or compression artifacts dominate.
- `muddy_materials`: materials merge into unclear surfaces.
- `over_detailed_background`: background props or contrast compete with the subject.
- `style_overpowering_subject`: style hides identity, action, or product shape.
- `media_defect_too_strong`: VHS/CRT/halftone/photocopy defects damage the subject.
- `low_subject_readability`: subject is too small, blurred, low contrast, or visually ambiguous.
- `weak_style_visibility`: intended style is not visible enough.
- `random_text_or_symbols`: fake letters, logos, symbols, or labels appear.
- `edge_contamination`: texture or background patterns bleed over subject edges.
- `text_accuracy_failure`: exact requested text is wrong, missing, warped, or duplicated.
- `identity_drift`: face, character, age, pose, clothing, or identity anchor changed.
- `product_geometry_drift`: product silhouette, proportions, cap/pump, label, or camera angle changed.
- `reference_role_confusion`: a reference controlled the wrong thing or preserved unwanted background/text/logo.
- `composition_drift`: framing, subject scale, hierarchy, or aspect ratio drifted.
- `prompt_too_long`: prompt length likely diluted priorities.
- `style_overload`: too many medium/style anchors competed.

## Revision Rules

- Preserve first, then change.
- Repair observed failures before adding new creative details.
- For GPT Image-like models, keep the revision short and natural.
- For dirty render, remove stacked grain/scan/VHS/CRT/halftone/photocopy language or reduce it to one subtle artifact.
- For text failures, quote exact text and remove all extra words or random symbols.
- For reference failures, name what each reference controls and what it must not preserve.
- For product failures, lock silhouette, proportions, label placement, cap/pump shape, edges, and camera angle.
- For identity failures, lock face structure, pose, clothing, age, expression, and distinctive accessories.

## When To Ask For More Feedback

Ask one concise question only when the failure cannot be inferred from the review, for example:

- The user says "bad result" but gives no visible failure.
- A reference image has multiple possible roles and the prompt does not assign one.
- The user asks to preserve something that conflicts with the requested repair.

Otherwise, generate a narrow revision prompt and include the next check.
