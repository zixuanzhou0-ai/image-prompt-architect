# Output Images

Store real image-output eval artifacts here only after a model run has happened.

Each output should be referenced from `evals/image_output_records.json` with:

- model and model version
- prompt before and rewritten prompt
- generation parameters
- output image path
- task-specific gate results from `evals/image_output_rubric.md`
- human rater and image score
- observed failures and revision prompt

Do not invent output files or metadata. Use `unknown` or `null` until a real generation has been captured.

## Storage Policy

- Use committed images only when the output is safe to share publicly.
- Use stable HTTPS URLs for private or externally hosted outputs.
- Redact or omit images that contain private people, proprietary brand assets, or restricted references.
- Record whether an artifact is `public`, `private`, or `redacted` in the corresponding eval notes.
- Keep enough generation metadata for review, but do not publish API keys, private reference images, or account-specific URLs.
