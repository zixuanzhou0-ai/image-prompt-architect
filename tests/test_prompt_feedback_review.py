import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CREATE_SCRIPT = ROOT / "scripts" / "create_prompt_feedback_review.py"
REVISION_SCRIPT = ROOT / "scripts" / "make_feedback_revision.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


create_prompt_feedback_review = load_module("create_prompt_feedback_review", CREATE_SCRIPT)
make_feedback_revision = load_module("make_feedback_revision", REVISION_SCRIPT)


def write_prompt(tmp_path: Path) -> Path:
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text(
        "Create a clean product image of a glass bottle with exact text \"ROSE HOUR\", "
        "reference image 1 for product geometry, reference image 2 for palette.",
        encoding="utf-8",
    )
    return prompt_file


def test_create_prompt_feedback_review_schema(tmp_path):
    prompt_file = write_prompt(tmp_path)
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake image")

    review = create_prompt_feedback_review.build_review_template(
        prompt_file=prompt_file,
        model="gpt-image",
        case_id="demo-case",
        image_path=image_path,
    )

    assert review["review_schema_version"] == "prompt-feedback-review-v0.1"
    assert review["case_id"] == "demo-case"
    assert review["target_model"] == "gpt-image"
    assert "text_accuracy" in review["scores"]
    assert "reference_role_confusion" in review["allowed_failure_labels"]
    assert review["prompt_text"].startswith("Create a clean product image")


def write_review(tmp_path: Path, failures: list[str]) -> Path:
    prompt_file = write_prompt(tmp_path)
    review = create_prompt_feedback_review.build_review_template(
        prompt_file=prompt_file,
        model="gpt-image",
        case_id="revision-case",
    )
    review["failures"] = failures
    review["observed_cause"] = "visible output feedback from the generated image"
    review_path = tmp_path / "prompt_feedback_review.json"
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return review_path


def test_make_feedback_revision_repairs_dirty_edges_and_text(tmp_path):
    review_path = write_review(
        tmp_path,
        ["texture_noise_overload", "edge_contamination", "text_accuracy_failure"],
    )

    result = make_feedback_revision.generate_feedback_revision(review_path)
    updated = json.loads(review_path.read_text(encoding="utf-8"))
    revision = updated["revision_prompt"]

    assert result["status"] == "success"
    assert (tmp_path / "revision_prompt.txt").exists()
    assert "Reduce heavy grain" in revision
    assert "Clean up subject edges" in revision
    assert "Render only the exact quoted text" in revision
    assert "remove stacked grain" in revision
    assert updated["next_check"].startswith("Check that these failures are fixed")


def test_reference_role_confusion_repair_mentions_unwanted_background_text_logo(tmp_path):
    review_path = write_review(tmp_path, ["reference_role_confusion"])

    make_feedback_revision.generate_feedback_revision(review_path)
    revision = json.loads(review_path.read_text(encoding="utf-8"))["revision_prompt"]

    assert "Use reference images only for their assigned roles" in revision
    assert "background, text, logos" in revision


def test_product_geometry_drift_repair_locks_geometry(tmp_path):
    review_path = write_review(tmp_path, ["product_geometry_drift"])

    make_feedback_revision.generate_feedback_revision(review_path)
    revision = json.loads(review_path.read_text(encoding="utf-8"))["revision_prompt"]

    assert "Lock product geometry" in revision
    assert "silhouette" in revision
    assert "label placement" in revision
