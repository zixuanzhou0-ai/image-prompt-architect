# Evals

This folder defines a lightweight prompt-evaluation protocol.

## Protocol

1. Score the source prompt with `references/evaluation-rubric.md`.
2. Run Image Prompt Architect in the expected mode.
3. Score the rewritten prompt.
4. Generate an image only if model access exists.
5. Score the output image against prompt intent.
6. Record observed failures and revision prompt.

The current evals are prompt-level only. Image-output evaluation is not yet automated.

For image-output scoring fields and manual capture format, see `image_output_protocol.md`.

`image_output_records.json` currently contains placeholder records only. Do not treat them as evidence of model output quality until `output_image_path`, `image_score`, and `human_rater` are filled from real runs.
