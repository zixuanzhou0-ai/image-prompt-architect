# Changelog

## 0.7.0 - 2026-05-29

- Added skill-output prompt captures and skill/candidate delta reporting.
- Added image-output rubric and linked it from the image-output protocol.
- Expanded Chinese no-space fixtures for product, poster, and series prompts.
- Added Chinese generic-praise-only rejection coverage.
- Refined FLUX negation severity into object-exclusion vs soft modifier warnings.
- Added Midjourney legacy `--style` fixture coverage.
- Expanded trigger smoke cases with Chinese examples.
- Added output artifact storage guidance for future real image-output evals.
- Added adapter/eval metadata status check for future real image-output records.

## 0.6.0 - 2026-05-29

- Added CJK-aware section content validation for continuous Chinese prompt text.
- Added Chinese no-space, filler-only, and too-short fixtures.
- Moved Midjourney `--cw` and `--style` to legacy warning handling.
- Added `--strict-model-params` to make unknown model parameters critical when desired.
- Refined GPT Image text-rendering warnings to avoid blank-label false positives.
- Expanded trigger smoke cases to 30 review examples.
- Added rewrite-aware prompt eval fields and source/rewrite delta reporting.
- Added CI freshness check for generated `evals/report.md`.

## 0.5.0 - 2026-05-28

- Added Midjourney `--c` and `--video` support, and corrected `--loop` as flag-like based on current docs.
- Split warning-only fixtures into `warn_*.txt` and updated CI to enforce good/bad/warn fixture policy.
- Added short Chinese label fixtures for `主体：` / `环境：` / `输出约束：` style headings.
- Expanded FLUX plain-negation phrase capture and added single-warning vs multiple-critical fixtures.
- Added GPT Image pixel-perfect, reference-role, quoted-text, and preserve/change fixtures.
- Added prompt-level eval runner and generated report support.
- Added CI badge and v0.5 tag-based install commands.

## 0.4.0 - 2026-05-28

- Blocked framework-label keyword stuffing from counting as seven-layer/system coverage.
- Added Markdown, colon-label, and Chinese heading parsing for prompt sections.
- Expanded Midjourney parameter parsing and parameter-value punctuation checks.
- Added FLUX plain-negation detection with escalation for repeated negation phrases.
- Added GPT Image edit, text-rendering, reproducibility, and reference-role warnings.
- Expanded lint fixtures and tests from 17 to 27 test cases.
- Updated CI to strict-lint every `good_*.txt` and `bad_*.txt` fixture.
- Added tag-based install commands and adapter update/fixture naming policies.
- Expanded eval scaffolding and image-output protocol documentation.

## 0.3.0 - 2026-05-28

- Made strict lint mode fail on critical model-policy and section-quality errors.
- Added section parser for empty heading skeletons.
- Added expanded prompt lint fixtures and tests.
- Added trigger regression fixture.
- Added model adapter confidence, primary docs, local coverage, and applies-to fields.
- Added mode precedence and stricter copy-ready contract.
- Added Identity Lock and Continuity Anchor Budget to series framework.
- Added install commands, troubleshooting, and known limitations.
- Added evaluation protocol scaffolding.

## 0.2.0 - 2026-05-28

- Tightened skill trigger description and boundary.
- Added mode-based output contracts.
- Rewrote model adapters as a versioned heuristic matrix.
- Added continuity, variation budget, and shot slots for series prompts.
- Renamed the seventh layer to Context, Intent, and Tone.
- Added output constraints outside the seven creative layers.
- Expanded examples and evaluation rubric.
- Rewrote prompt lint script with architecture/model options, JSON output, strict mode, contradictions, generic filler, and model policy warnings.
- Added compact prompt detection for parameterized prompt styles such as Midjourney.
- Added tests and fixtures.

## 0.1.0 - 2026-05-28

- Initial plugin and skill scaffold.
