# Contributing

Contributions should improve prompt architecture quality, model-specific accuracy, or test coverage.

## Rules

- Prefer primary model documentation over community folklore.
- Mark unverified model behavior as a heuristic.
- Add examples when changing a framework.
- Add tests when changing `prompt_lint.py`.
- Do not invent metadata for imported image assets. Use `unknown` when the source prompt, model, or seed is not reliable.

## Adapter Update Policy

When updating `references/model-adapters.md`:

- Link primary docs or state that only local/project evidence exists.
- Update `Last verified`, `Confidence`, `Applies to`, and `Local test coverage`.
- Add or update fixtures when syntax or policy behavior changes.
- Add tests when a linter rule changes.
- Add an eval case when a creative heuristic changes.

## Fixture Naming

- `good_*.txt` must pass `prompt_lint.py --strict`.
- `bad_*.txt` must fail `prompt_lint.py --strict`.
- `warn_*.txt` is reserved for warning-only examples that should pass strict mode.

## Local Checks

```bash
python -m pytest
python skills/image-prompt-architect/scripts/prompt_lint.py tests/fixtures/good_seven_layer.txt --architecture seven-layer
```
