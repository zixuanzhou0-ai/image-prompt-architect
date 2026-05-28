# Image Output Protocol

Use this protocol when model access exists and a prompt-level eval can be extended into a real output eval.

Score generated images with `image_output_rubric.md`, including the task-specific gates for text rendering, editing, series, product photography, and model-port evals.

## Required Fields

- `case_id`
- `target_model`
- `model_version`
- `adapter_version`
- `prompt_before`
- `rewritten_prompt`
- `skill_output_source`
- `skill_output_date`
- `skill_output_notes`
- `expected_mode`
- `expected_risks`
- `task_type`
- `source_score`
- `rewritten_score`
- `generation_params`
- `output_image_path`
- `image_score`
- `task_gate_results`
- `human_rater`
- `observed_failures`
- `revision_prompt`
- `final_score`

## Steps

1. Score the source prompt with `skills/image-prompt-architect/references/evaluation-rubric.md`.
2. Run the skill in the expected mode and record the rewritten prompt.
3. Record whether the rewritten prompt came from a manual capture, a Codex run, or a golden reference.
4. Score the rewritten prompt before generation.
5. Generate the image with model version, seed, aspect ratio, reference images, and other parameters recorded.
6. Score the image against the original intent and rewritten prompt.
7. Apply the task-specific gate in `image_output_rubric.md`.
8. Record visible failures and write a revision prompt.
9. Regenerate only when the eval explicitly tracks iteration quality.
