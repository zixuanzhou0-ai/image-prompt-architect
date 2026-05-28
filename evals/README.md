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

