import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "open_style_sampler.py"
REVIEW_SCRIPT = ROOT / "scripts" / "review_generated_images.py"
REVISION_SCRIPT = ROOT / "scripts" / "make_revision_prompts.py"

spec = importlib.util.spec_from_file_location("open_style_sampler", SCRIPT)
open_style_sampler = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["open_style_sampler"] = open_style_sampler
spec.loader.exec_module(open_style_sampler)

review_spec = importlib.util.spec_from_file_location("review_generated_images", REVIEW_SCRIPT)
review_generated_images = importlib.util.module_from_spec(review_spec)
assert review_spec.loader is not None
sys.modules["review_generated_images"] = review_generated_images
review_spec.loader.exec_module(review_generated_images)

revision_spec = importlib.util.spec_from_file_location("make_revision_prompts", REVISION_SCRIPT)
make_revision_prompts = importlib.util.module_from_spec(revision_spec)
assert revision_spec.loader is not None
sys.modules["make_revision_prompts"] = make_revision_prompts
revision_spec.loader.exec_module(make_revision_prompts)


def load_inputs():
    return (
        open_style_sampler.read_json(open_style_sampler.POOL_PATH),
        open_style_sampler.load_style_library(open_style_sampler.STYLE_LIBRARY_PATH),
    )


def write_sample_batch(tmp_path, *, seed=42, count=3, style_family=None, history=None, render_profile="clean"):
    pool, style_library = load_inputs()
    out_dir = tmp_path / "batch"
    open_style_sampler.write_batch(
        out_dir=out_dir,
        count=count,
        pool=pool,
        style_library=style_library,
        seed=seed,
        eagle_folder="AI风格探索",
        min_lint_score=10,
        max_attempts=8,
        style_family=style_family,
        freshness="high",
        style_strength="balanced",
        render_profile=render_profile,
        background_complexity=2,
        defect_strength=0.15,
        max_aux_styles=1,
        history=history or open_style_sampler.load_history(False),
    )
    return out_dir, json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))


def stable_manifest_bits(manifest):
    return [
        (
            item["title"],
            item["aspect_ratio"],
            item["layers"],
            item["style_selection"]["main_style"]["style_id"],
            (item["style_selection"]["auxiliary_style"] or {}).get("style_id"),
            item["lint_score"],
            item["render_prompt_chars"],
            item["internal_prompt_chars"],
        )
        for item in manifest["prompts"]
    ]


def test_seeded_batch_is_stable_and_parseable(tmp_path):
    first_dir, first = write_sample_batch(tmp_path / "first", seed=42)
    second_dir, second = write_sample_batch(tmp_path / "second", seed=42)

    assert first["prompt_contract_version"] == "open-style-v0.16"
    assert first["style_library_version"] == "1.1"
    assert first["history_dedupe"] == {"enabled": False, "runs_scanned": 0, "reviews_scanned": 0}
    assert stable_manifest_bits(first) == stable_manifest_bits(second)
    assert (first_dir / first["prompts"][0]["prompt_file"]).read_text(encoding="utf-8") == (
        second_dir / second["prompts"][0]["prompt_file"]
    ).read_text(encoding="utf-8")


def test_every_prompt_records_rare_style_and_lint_score(tmp_path):
    out_dir, manifest = write_sample_batch(tmp_path, seed=42)

    assert len(list((out_dir / "prompts").glob("*.txt"))) == 3
    for item in manifest["prompts"]:
        selection = item["style_selection"]
        main = selection["main_style"]
        assert item["lint_score"] >= 10
        assert main["style_id"]
        assert main["name"]
        assert main["category"]
        assert "risk" in main
        assert "fix" in main
        assert selection["selection_mode"] == "mixed"
        assert selection["style_strength"] == "balanced"
        assert selection["render_profile"] == "clean"
        assert selection["history_dedupe"]["enabled"] is False


def test_clean_profile_outputs_render_and_internal_prompts(tmp_path):
    out_dir, manifest = write_sample_batch(tmp_path, seed=42)
    first = manifest["prompts"][0]
    render_prompt = (out_dir / first["render_prompt_file"]).read_text(encoding="utf-8")
    internal_prompt = (out_dir / first["internal_prompt_file"]).read_text(encoding="utf-8")

    assert manifest["render_profile"] == "clean"
    assert manifest["style_strength"] == "balanced"
    assert first["render_prompt_chars"] < first["internal_prompt_chars"]
    assert "Clean render" in render_prompt
    assert "crisp subject silhouette" in render_prompt
    assert "[Subject]" not in render_prompt
    assert "[Subject]" in internal_prompt


def test_defect_style_gets_clean_constraints():
    _, style_library = load_inputs()
    defect_style = next(style for style in style_library["styles"] if open_style_sampler.is_defect_style(style))
    selection = {"main_style": open_style_sampler.style_record(defect_style), "auxiliary_style": None}
    layers = {
        "subject": "a glass fish on a workbench",
        "environment": "a quiet workshop",
        "lighting": "soft window light",
        "material": "glass, brass, old paper tickets, scratched metal",
        "composition_camera": "medium close-up, 50mm lens",
        "style": "rare style",
        "expression": "still product pose",
        "tone": "clean visual study",
    }

    prompt = open_style_sampler.compress_prompt_for_render(layers, selection, "1:1", "clean", 2, 0.15)

    assert "Media defect strength stays below 0.15" in prompt
    assert "not damaged" in prompt


def test_style_family_limits_main_style_category(tmp_path):
    _, manifest = write_sample_batch(tmp_path, seed=7, count=2, style_family="graphic")

    assert manifest["style_family"] == "graphic"
    for item in manifest["prompts"]:
        assert item["style_selection"]["selection_mode"] == "style-family:graphic"
        assert item["style_selection"]["main_style"]["category"] == "平面设计、印刷与海报亚种"


def test_history_can_be_disabled_and_style_history_lowers_weight():
    pool, style_library = load_inputs()
    style = style_library["styles"][0]
    sid = style["style_id"]
    no_history = open_style_sampler.load_history(False)
    with_history = {
        "enabled": True,
        "runs_scanned": 1,
        "reviews_scanned": 1,
        "subjects": Counter({pool["subjects"][0]: 3}),
        "lighting": Counter({pool["lighting"][0]: 2}),
        "style_ids": Counter({sid: 4}),
        "style_failures": Counter({f"{sid}:texture_noise_overload": 2}),
        "failure_types": Counter({"texture_noise_overload": 2}),
    }

    assert no_history["enabled"] is False
    assert no_history["runs_scanned"] == 0
    assert open_style_sampler.style_weight(style, "high", with_history["style_ids"]) < open_style_sampler.style_weight(
        style,
        "high",
        Counter(),
    )
    assert open_style_sampler.style_weight(style, "high", Counter(), with_history["style_failures"], "clean") < open_style_sampler.style_weight(
        style,
        "high",
        Counter(),
    )


def test_review_template_and_revision_prompt_generation(tmp_path):
    out_dir, manifest = write_sample_batch(tmp_path, seed=42, count=1)
    images_dir = out_dir / "images"
    images_dir.mkdir(exist_ok=True)
    (images_dir / "01_sample.png").write_bytes(b"fake png")

    review = review_generated_images.build_review_template(out_dir)
    review_path = out_dir / "generated_review.json"
    review["reviews"][0]["failures"] = ["texture_noise_overload", "low_subject_readability"]
    review_generated_images.write_json(review_path, review)
    result = make_revision_prompts.generate_revision_prompts(out_dir)
    updated = json.loads(review_path.read_text(encoding="utf-8"))
    revision_file = out_dir / result["generated"][0]["revision_file"]

    assert review["reviews"][0]["image_path"] == "images\\01_sample.png"
    assert updated["reviews"][0]["revision_prompt"]
    assert revision_file.exists()
    assert manifest["prompts"][0]["style_selection"]["main_style"]["style_id"] in revision_file.read_text(encoding="utf-8")
