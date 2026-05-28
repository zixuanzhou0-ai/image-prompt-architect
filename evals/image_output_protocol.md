# Image Output Protocol

Use this protocol when model access exists and a prompt-level eval can be extended into a real output eval.

Score generated images with `image_output_rubric.md`.

## Required Fields

- `case_id`
- `target_model`
- `model_version`
- `adapter_version`
- `prompt_before`
- `rewritten_prompt`
- `expected_mode`
- `expected_risks`
- `source_score`
- `rewritten_score`
- `generation_params`
- `output_image_path`
- `image_score`
- `human_rater`
- `observed_failures`
- `revision_prompt`
- `final_score`

## Steps

1. Score the source prompt with `skills/image-prompt-architect/references/evaluation-rubric.md`.
2. Run the skill in the expected mode and record the rewritten prompt.
3. Score the rewritten prompt before generation.
4. Generate the image with model version, seed, aspect ratio, reference images, and other parameters recorded.
5. Score the image against the original intent and rewritten prompt.
6. Record visible failures and write a revision prompt.
7. Regenerate only when the eval explicitly tracks iteration quality.
