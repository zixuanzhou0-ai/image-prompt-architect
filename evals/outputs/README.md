# Output Images

Store real image-output eval artifacts here only after a model run has happened.

Each output should be referenced from `evals/image_output_records.json` with:

- model and model version
- prompt before and rewritten prompt
- generation parameters
- output image path
- human rater and image score
- observed failures and revision prompt

Do not invent output files or metadata. Use `unknown` or `null` until a real generation has been captured.
