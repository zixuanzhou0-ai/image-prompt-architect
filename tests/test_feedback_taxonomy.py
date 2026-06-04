import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_SCRIPT = ROOT / "scripts" / "feedback_taxonomy.py"
REVIEW_SCRIPT = ROOT / "scripts" / "review_generated_images.py"
REVISION_SCRIPT = ROOT / "scripts" / "make_revision_prompts.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


feedback_taxonomy = load_module("feedback_taxonomy", TAXONOMY_SCRIPT)
review_generated_images = load_module("review_generated_images_for_taxonomy", REVIEW_SCRIPT)
make_revision_prompts = load_module("make_revision_prompts_for_taxonomy", REVISION_SCRIPT)


def test_every_failure_label_has_repair_rule():
    missing = [label for label in feedback_taxonomy.FAILURE_LABELS if label not in feedback_taxonomy.FAILURE_REPAIR_RULES]
    assert not missing


def test_open_style_review_uses_shared_taxonomy():
    assert review_generated_images.FAILURE_LABELS == feedback_taxonomy.FAILURE_LABELS
    assert review_generated_images.SCORE_KEYS == feedback_taxonomy.SCORE_KEYS
    assert make_revision_prompts.FAILURE_REPAIR_RULES == feedback_taxonomy.FAILURE_REPAIR_RULES


def test_gpt_image_repair_profile_reduces_defect_language():
    profile = feedback_taxonomy.model_repair_profile("gpt-image")
    assert profile["max_words"] <= 140
    assert "remove stacked grain" in profile["defect_policy"]
    assert "subtle artifact" in profile["defect_policy"]


def test_unknown_failures_are_filtered():
    assert feedback_taxonomy.known_failures(["texture_noise_overload", "unknown_failure"]) == ["texture_noise_overload"]
