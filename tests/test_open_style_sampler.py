import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "open_style_sampler.py"

spec = importlib.util.spec_from_file_location("open_style_sampler", SCRIPT)
open_style_sampler = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["open_style_sampler"] = open_style_sampler
spec.loader.exec_module(open_style_sampler)


def load_inputs():
    return (
        open_style_sampler.read_json(open_style_sampler.POOL_PATH),
        open_style_sampler.load_style_library(open_style_sampler.STYLE_LIBRARY_PATH),
    )


def write_sample_batch(tmp_path, *, seed=42, count=3, style_family=None, history=None):
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
        style_strength="style-forward",
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
        )
        for item in manifest["prompts"]
    ]


def test_seeded_batch_is_stable_and_parseable(tmp_path):
    first_dir, first = write_sample_batch(tmp_path / "first", seed=42)
    second_dir, second = write_sample_batch(tmp_path / "second", seed=42)

    assert first["prompt_contract_version"] == "open-style-v0.15"
    assert first["style_library_version"] == "1.1"
    assert first["history_dedupe"] == {"enabled": False, "runs_scanned": 0}
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
        assert selection["style_strength"] == "style-forward"
        assert selection["history_dedupe"]["enabled"] is False


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
        "subjects": Counter({pool["subjects"][0]: 3}),
        "lighting": Counter({pool["lighting"][0]: 2}),
        "style_ids": Counter({sid: 4}),
    }

    assert no_history["enabled"] is False
    assert no_history["runs_scanned"] == 0
    assert open_style_sampler.style_weight(style, "high", with_history["style_ids"]) < open_style_sampler.style_weight(
        style,
        "high",
        Counter(),
    )
