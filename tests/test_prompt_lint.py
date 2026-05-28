from pathlib import Path
import importlib.util
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "image-prompt-architect" / "scripts" / "prompt_lint.py"

spec = importlib.util.spec_from_file_location("prompt_lint", SCRIPT)
prompt_lint = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["prompt_lint"] = prompt_lint
spec.loader.exec_module(prompt_lint)


def fixture(name: str) -> str:
    return (ROOT / "tests" / "fixtures" / name).read_text(encoding="utf-8")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def test_good_seven_layer_has_full_coverage():
    result = prompt_lint.lint(fixture("good_seven_layer.txt"), "seven-layer", "generic")
    assert result.score >= 8
    assert not result.missing
    assert not result.critical


def test_bad_template_shell_is_critical_in_strict_terms():
    result = prompt_lint.lint(fixture("bad_template_shell.txt"), "seven-layer", "generic")
    assert result.critical
    assert "material" in result.missing
    assert any("generic filler" in warning.lower() for warning in result.warnings)


def test_empty_heading_skeleton_is_critical():
    result = prompt_lint.lint(fixture("bad_empty_heading_skeleton.txt"), "seven-layer", "generic")
    assert result.critical
    assert all(not quality["valid"] for quality in result.section_quality.values())


def test_keyword_stuffing_without_sections_does_not_count_as_coverage():
    result = prompt_lint.lint(fixture("bad_keyword_stuffing_no_sections.txt"), "seven-layer", "generic")
    assert result.critical
    assert sum(result.coverage.values()) <= 1
    assert "subject" in result.missing


def test_markdown_heading_skeleton_is_parsed_and_rejected():
    result = prompt_lint.lint(fixture("bad_markdown_heading_skeleton.txt"), "seven-layer", "generic")
    assert result.critical
    assert result.section_quality["subject"]["present"]
    assert not result.section_quality["subject"]["valid"]


def test_colon_heading_skeleton_is_parsed_and_rejected():
    result = prompt_lint.lint(fixture("bad_label_colon_skeleton.txt"), "seven-layer", "generic")
    assert result.critical
    assert result.section_quality["composition"]["present"]
    assert not result.section_quality["composition"]["valid"]


def test_good_system_series_has_series_controls():
    result = prompt_lint.lint(fixture("good_system_series.txt"), "system", "generic")
    assert result.score >= 8
    assert not result.critical
    assert result.coverage["continuity"]
    assert result.coverage["variation_budget"]
    assert result.coverage["shot_slots"]


def test_system_without_continuity_is_critical():
    result = prompt_lint.lint(fixture("bad_system_no_continuity.txt"), "system", "generic")
    assert result.critical
    assert "continuity" in result.missing
    assert "variation_budget" in result.missing
    assert "shot_slots" in result.missing


def test_midjourney_good_prompt_auto_infers_compact():
    result = prompt_lint.lint(fixture("good_midjourney.txt"), "auto", "midjourney")
    assert result.architecture == "compact"
    assert not result.critical


def test_midjourney_negative_block_is_critical():
    result = prompt_lint.lint(fixture("bad_midjourney_negative_block.txt"), "auto", "midjourney")
    assert any("Negative Prompt" in item for item in result.critical)


def test_midjourney_params_middle_is_critical():
    result = prompt_lint.lint(fixture("bad_midjourney_params_middle.txt"), "auto", "midjourney")
    assert any("trailing prose" in item for item in result.critical)


def test_midjourney_current_reference_params_pass():
    result = prompt_lint.lint(fixture("good_midjourney_oref_profile.txt"), "auto", "midjourney")
    assert not result.critical
    assert "--oref" in result.model_policy["midjourney_params"]
    assert "--profile" in result.model_policy["midjourney_params"]


def test_midjourney_chaos_alias_passes():
    result = prompt_lint.lint(fixture("good_midjourney_chaos_alias.txt"), "auto", "midjourney")
    assert not result.critical
    assert "--c" in result.model_policy["midjourney_params"]


def test_midjourney_video_and_loop_params_pass():
    result = prompt_lint.lint(fixture("good_midjourney_video.txt"), "compact", "midjourney")
    assert not result.critical
    assert "--video" in result.model_policy["midjourney_params"]
    assert "--loop" in result.model_policy["midjourney_params"]


def test_midjourney_loop_is_flag_like():
    result = prompt_lint.lint(fixture("good_midjourney_loop.txt"), "compact", "midjourney")
    assert not result.critical
    assert "--loop" in result.model_policy["midjourney_params"]


def test_midjourney_value_punctuation_is_critical():
    result = prompt_lint.lint(fixture("bad_midjourney_value_punctuation.txt"), "auto", "midjourney")
    assert any("value has trailing punctuation" in item for item in result.critical)


def test_midjourney_legacy_cw_warns():
    result = prompt_lint.lint(fixture("warn_midjourney_legacy_cw.txt"), "compact", "midjourney")
    assert not result.critical
    assert any("Legacy or deprecated" in warning for warning in result.warnings)


def test_midjourney_legacy_style_warns():
    result = prompt_lint.lint(fixture("warn_midjourney_legacy_style.txt"), "compact", "midjourney")
    assert not result.critical
    assert any("Legacy or deprecated" in warning for warning in result.warnings)


def test_midjourney_unknown_param_warns_by_default():
    result = prompt_lint.lint(fixture("warn_midjourney_unknown_future_param.txt"), "compact", "midjourney")
    assert not result.critical
    assert any("Unknown Midjourney parameter" in warning for warning in result.warnings)


def test_midjourney_unknown_param_can_be_strict_model_critical():
    result = prompt_lint.lint(
        fixture("warn_midjourney_unknown_future_param.txt"),
        "compact",
        "midjourney",
        strict_model_params=True,
    )
    assert any("Unknown Midjourney parameter" in item for item in result.critical)


def test_midjourney_unknown_param_strict_model_cli_fails():
    completed = run_cli(
        "tests/fixtures/bad_midjourney_unknown_param_strict_model_params.txt",
        "--architecture",
        "compact",
        "--model",
        "midjourney",
        "--strict",
        "--strict-model-params",
    )
    assert completed.returncode != 0


def test_flux_negative_prompt_is_critical():
    result = prompt_lint.lint(fixture("bad_flux_negative.txt"), "auto", "flux")
    assert any("FLUX" in item for item in result.critical)


def test_flux_plain_negation_is_detected_and_escalated():
    result = prompt_lint.lint(fixture("bad_flux_plain_negation.txt"), "auto", "flux")
    assert result.model_policy["plain_negation_phrases"]
    assert any("object-exclusion negation" in item for item in result.critical)


def test_flux_single_plain_negation_warns_but_does_not_fail():
    result = prompt_lint.lint(fixture("warn_flux_single_plain_negation_phrase.txt"), "compact", "flux")
    assert result.model_policy["plain_negation_phrases"] == ["no background distractions"]
    assert not result.critical
    assert any("plain negation" in warning for warning in result.warnings)


def test_flux_multiple_plain_negations_are_critical():
    result = prompt_lint.lint(fixture("bad_flux_multiple_plain_negation_phrases.txt"), "compact", "flux")
    assert len(result.model_policy["object_negation_phrases"]) >= 2
    assert any("multiple object-exclusion negation" in item for item in result.critical)


def test_flux_soft_modifier_negations_warn_only():
    result = prompt_lint.lint(fixture("warn_flux_soft_modifier_negation.txt"), "compact", "flux")
    assert result.model_policy["soft_negation_phrases"]
    assert not result.model_policy["object_negation_phrases"]
    assert not result.critical
    assert any("soft modifier negation" in warning for warning in result.warnings)


def test_flux_object_exclusion_negations_are_critical():
    result = prompt_lint.lint(fixture("bad_flux_object_exclusion_negations.txt"), "compact", "flux")
    assert len(result.model_policy["object_negation_phrases"]) >= 2
    assert any("object-exclusion" in item for item in result.critical)


def test_flux_invalid_hex_is_critical():
    result = prompt_lint.lint(fixture("bad_flux_invalid_hex.txt"), "auto", "flux")
    assert any("malformed hex" in item for item in result.critical)


def test_good_flux_structured_has_no_critical_errors():
    result = prompt_lint.lint(fixture("good_flux_structured.txt"), "compact", "flux")
    assert not result.critical


def test_good_flux_positive_replacements_have_no_negation_warning():
    result = prompt_lint.lint(fixture("good_flux_positive_replacements.txt"), "compact", "flux")
    assert not result.critical
    assert not result.model_policy["plain_negation_phrases"]


def test_good_flux_positive_replacements_extended_have_no_negation_warning():
    result = prompt_lint.lint(fixture("good_flux_positive_replacements_extended.txt"), "compact", "flux")
    assert not result.critical
    assert not result.model_policy["plain_negation_phrases"]


def test_gpt_image_keyword_pile_warns():
    result = prompt_lint.lint(fixture("bad_gpt_image_keyword_pile.txt"), "auto", "gpt-image")
    assert any("keyword pile" in warning.lower() for warning in result.warnings)


def test_gpt_image_edit_without_preserve_warns():
    result = prompt_lint.lint(fixture("warn_gpt_image_edit_no_preserve.txt"), "compact", "gpt-image")
    assert not result.critical
    assert any("preserve/change" in warning for warning in result.warnings)


def test_gpt_image_text_without_quotes_warns():
    result = prompt_lint.lint(fixture("warn_gpt_image_unquoted_text.txt"), "compact", "gpt-image")
    assert not result.critical
    assert any("quote exact text" in warning for warning in result.warnings)


def test_gpt_image_pixel_perfect_claim_warns():
    result = prompt_lint.lint(fixture("warn_gpt_image_pixel_perfect_claim.txt"), "compact", "gpt-image")
    assert not result.critical
    assert any("pixel-perfect" in warning for warning in result.warnings)


def test_gpt_image_reference_without_role_warns():
    result = prompt_lint.lint(fixture("warn_gpt_image_reference_without_role.txt"), "compact", "gpt-image")
    assert not result.critical
    assert any("reference-image" in warning for warning in result.warnings)


def test_good_gpt_image_edit_preserve_change_has_no_policy_warning():
    result = prompt_lint.lint(fixture("good_gpt_image_edit_preserve_change.txt"), "compact", "gpt-image")
    assert not result.critical
    assert not any("preserve/change" in warning for warning in result.warnings)


def test_good_gpt_image_quoted_text_has_no_text_warning():
    result = prompt_lint.lint(fixture("good_gpt_image_text_quoted.txt"), "compact", "gpt-image")
    assert not result.critical
    assert not any("quote exact text" in warning for warning in result.warnings)


def test_good_gpt_image_blank_label_has_no_text_warning():
    result = prompt_lint.lint(fixture("good_gpt_image_blank_label.txt"), "compact", "gpt-image")
    assert not result.critical
    assert not any("quote exact text" in warning for warning in result.warnings)


def test_gpt_image_label_reads_unquoted_words_warns():
    result = prompt_lint.lint(fixture("warn_gpt_image_label_with_unquoted_words.txt"), "compact", "gpt-image")
    assert not result.critical
    assert any("quote exact text" in warning for warning in result.warnings)


def test_chinese_dreamina_prompt_runs():
    result = prompt_lint.lint(fixture("good_chinese_dreamina.txt"), "compact", "dreamina")
    assert result.score >= 6


def test_chinese_seven_layer_headings_are_supported():
    result = prompt_lint.lint(fixture("good_chinese_seven_layer.txt"), "seven-layer", "dreamina")
    assert not result.critical
    assert not result.missing


def test_chinese_short_labels_are_supported():
    result = prompt_lint.lint(fixture("good_chinese_short_labels.txt"), "seven-layer", "dreamina")
    assert not result.critical
    assert not result.missing


def test_chinese_short_label_skeleton_is_rejected():
    result = prompt_lint.lint(fixture("bad_chinese_short_label_skeleton.txt"), "seven-layer", "dreamina")
    assert result.critical
    assert result.section_quality["subject"]["present"]
    assert not result.section_quality["subject"]["valid"]


def test_chinese_no_spaces_sections_are_supported():
    result = prompt_lint.lint(fixture("good_chinese_no_spaces.txt"), "seven-layer", "dreamina")
    assert not result.critical
    assert not result.missing


def test_chinese_product_no_spaces_sections_are_supported():
    result = prompt_lint.lint(fixture("good_chinese_product_no_spaces.txt"), "seven-layer", "dreamina")
    assert not result.critical
    assert not result.missing


def test_chinese_poster_no_spaces_sections_are_supported():
    result = prompt_lint.lint(fixture("good_chinese_poster_no_spaces.txt"), "seven-layer", "dreamina")
    assert not result.critical
    assert not result.missing


def test_chinese_system_series_is_supported():
    result = prompt_lint.lint(fixture("good_chinese_series_system.txt"), "system", "dreamina")
    assert not result.critical
    assert result.coverage["identity_lock"]
    assert result.coverage["shot_slots"]


def test_chinese_filler_only_sections_are_rejected():
    result = prompt_lint.lint(fixture("bad_chinese_filler_only.txt"), "seven-layer", "dreamina")
    assert result.critical
    assert any("filler-only" in item for item in result.critical)


def test_chinese_generic_praise_only_sections_are_rejected():
    result = prompt_lint.lint(fixture("bad_chinese_generic_praise_only.txt"), "seven-layer", "dreamina")
    assert result.critical
    assert any("filler-only" in item for item in result.critical)


def test_chinese_too_short_sections_are_rejected():
    result = prompt_lint.lint(fixture("bad_chinese_too_short.txt"), "seven-layer", "dreamina")
    assert result.critical
    assert any("too short" in item for item in result.critical)


def test_bilingual_model_port_prompt_runs_as_compact():
    result = prompt_lint.lint(fixture("good_bilingual_model_port.txt"), "compact", "dreamina")
    assert result.score >= 6


def test_contradictions_warn():
    result = prompt_lint.lint(fixture("bad_contradictions.txt"), "auto", "generic")
    joined = " ".join(result.warnings)
    assert "1930s" in joined
    assert "macro" in joined


def test_json_output_contains_severity_fields():
    completed = run_cli(
        "tests/fixtures/bad_flux_negative.txt",
        "--model",
        "flux",
        "--format",
        "json",
    )
    assert completed.returncode == 0
    data = json.loads(completed.stdout)
    assert "critical" in data
    assert "warnings" in data
    assert "suggestions" in data
    assert "section_quality" in data
    assert "model_policy" in data


def test_strict_bad_fixture_returns_nonzero():
    completed = run_cli("tests/fixtures/bad_flux_negative.txt", "--model", "flux", "--strict")
    assert completed.returncode != 0


def test_strict_good_fixture_returns_zero():
    completed = run_cli("tests/fixtures/good_seven_layer.txt", "--architecture", "seven-layer", "--strict")
    assert completed.returncode == 0
