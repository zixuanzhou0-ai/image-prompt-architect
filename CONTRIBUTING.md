# Contributing

Contributions should improve prompt architecture quality, model-specific accuracy, or test coverage.

## Rules

- Prefer primary model documentation over community folklore.
- Mark unverified model behavior as a heuristic.
- Add examples when changing a framework.
- Add tests when changing `prompt_lint.py`.
- Do not invent metadata for imported image assets. Use `unknown` when the source prompt, model, or seed is not reliable.

## Local Checks

```bash
python -m pytest
python skills/image-prompt-architect/scripts/prompt_lint.py tests/fixtures/good_seven_layer.txt --architecture seven-layer
```

