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


def test_flux_negative_prompt_is_critical():
    result = prompt_lint.lint(fixture("bad_flux_negative.txt"), "auto", "flux")
    assert any("FLUX" in item for item in result.critical)


def test_flux_invalid_hex_is_critical():
    result = prompt_lint.lint(fixture("bad_flux_invalid_hex.txt"), "auto", "flux")
    assert any("malformed hex" in item for item in result.critical)


def test_good_flux_structured_has_no_critical_errors():
    result = prompt_lint.lint(fixture("good_flux_structured.txt"), "compact", "flux")
    assert not result.critical


def test_gpt_image_keyword_pile_warns():
    result = prompt_lint.lint(fixture("bad_gpt_image_keyword_pile.txt"), "auto", "gpt-image")
    assert any("keyword pile" in warning.lower() for warning in result.warnings)


def test_chinese_dreamina_prompt_runs():
    result = prompt_lint.lint(fixture("good_chinese_dreamina.txt"), "compact", "dreamina")
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

