# Changelog

## 0.11.0 - 2026-05-29

- Hardened `evals/check_image_output_records.py` so real scored records with object/list fields validate cleanly instead of triggering type errors.
- Added image-output record validator tests for placeholder mode, `--require-real-records`, dict/list scored records, missing fields, failed task gates, missing output paths, score thresholds, invalid score values, and final-score consistency.
- Added stricter v1.0 scored-record checks for `image_score` values, task-gate-to-score consistency, `skill_output_date` format, required case coverage, and revision-loop evidence.
- Updated `scripts/check_adapter_eval_status.py` to use type-safe missing-value detection.
- Kept image-output records placeholder-only; v1.0 remains blocked until real model outputs are captured and scored.

## 0.10.0 - 2026-05-29

- Added `evals/check_image_output_records.py` for v1.0-style scored record validation.
- Added CI coverage for image-output record validation.
- Made prompt eval fail when `skill_output_prompt` lacks source/date/notes provenance.
- Added `docs/V1_RELEASE_GATE.md` with release gates and an example scored image-output record.
- Kept image-output records placeholder-only; v1.0 remains blocked until real model outputs are captured and scored.

## 0.9.0 - 2026-05-29

- Added skill-output provenance fields to prompt eval cases.
- Updated prompt eval reporting with a `Skill Source` column.
- Strengthened future image-output record validation for scored records, including task gates and required output fields.
- Added Chinese GPT Image text-rendering warnings for signs, titles, logos, labels, and exact wording cues.
- Added Chinese GPT Image blank-label and quoted-text fixtures to reduce false positives.
- Added Grok prompt-level fixtures for reference-image role assignment and generation settings.
- Expanded image-output rubric task examples for text rendering, editing, series, product photography, and model-port evals.
- Kept image-output records placeholder-only; real prompt-to-image evidence remains the v1.0 blocker.

## 0.8.0 - 2026-05-29

- Added `skill_output_prompt` fields directly to prompt eval cases.
- Updated prompt eval reporting with missing expected feature visibility.
- Added task-specific image-output rubric gates for text rendering, editing, series, product photography, and model-port evals.
- Strengthened adapter/image-output eval status checks for future scored records.
- Expanded GPT Image warning fixtures around unmarked logos and label/logo text.
- Expanded trigger smoke cases from 40 to 50 with more Chinese ambiguity pairs.
- Added broader Chinese filler and concrete visual terms.
- Kept image-output records placeholder-only; no model outputs were invented.

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
