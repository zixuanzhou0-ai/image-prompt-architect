from pathlib import Path
import importlib.util
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


def test_good_seven_layer_has_full_coverage():
    result = prompt_lint.lint(fixture("good_seven_layer.txt"), "seven-layer", "generic")
    assert result.score >= 8
    assert not result.missing


def test_bad_template_shell_is_critical_in_strict_terms():
    result = prompt_lint.lint(fixture("bad_template_shell.txt"), "seven-layer", "generic")
    assert result.critical_failures
    assert "material" in result.missing
    assert any("generic filler" in warning.lower() for warning in result.warnings)


def test_midjourney_no_negative_block_warning_for_good_prompt():
    result = prompt_lint.lint(fixture("good_midjourney.txt"), "auto", "midjourney")
    assert not any("Negative Prompt" in warning for warning in result.warnings)
    assert any("Midjourney" in suggestion for suggestion in result.suggestions)


def test_flux_negative_prompt_warns():
    result = prompt_lint.lint(fixture("bad_flux_negative.txt"), "auto", "flux")
    assert any("FLUX" in warning for warning in result.warnings)
