#!/usr/bin/env python3
"""Create seven-layer prompts for Open Style Atlas exploration.

This script prepares prompt batches and Eagle import commands. It does not call
Codex image generation directly; the Codex thread/automation should generate
images from the prompt files, save them under the batch images folder, then run
the import command written by this script.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar


ROOT = Path(__file__).resolve().parents[1]
POOL_PATH = ROOT / "automation" / "open_style_source_pool.json"
STYLE_LIBRARY_PATH = ROOT / "automation" / "rare_style_library.json"
EAGLE_IMPORT = ROOT / "scripts" / "eagle_import.py"
PROMPT_LINT = ROOT / "skills" / "image-prompt-architect" / "scripts" / "prompt_lint.py"
PROMPT_CONTRACT_VERSION = "open-style-v0.15"


BASE_CATEGORIES = {
    "电影、电视与影像类型",
    "动画、漫画与插画亚种",
    "摄影工艺与影像缺陷",
    "工艺、地域视觉与历史媒介",
    "数字、游戏、UI与计算机视觉",
}
SURFACE_CATEGORIES = {"材质与表面质感"}
FORMAT_CATEGORIES = {
    "平面设计、印刷与海报亚种",
    "玩具、产品与收藏品呈现",
}
SPACE_CATEGORIES = {"建筑、空间与场景气质"}
FASHION_CATEGORIES = {"时装、亚文化与人物造型"}
STYLE_FAMILIES = {
    "film": {"电影、电视与影像类型"},
    "fashion": {"时装、亚文化与人物造型"},
    "product": {"玩具、产品与收藏品呈现", "材质与表面质感"},
    "photography": {"摄影工艺与影像缺陷"},
    "illustration": {"动画、漫画与插画亚种"},
    "graphic": {"平面设计、印刷与海报亚种"},
    "craft": {"工艺、地域视觉与历史媒介"},
    "digital": {"数字、游戏、UI与计算机视觉"},
    "space": {"建筑、空间与场景气质"},
    "material": {"材质与表面质感"},
}
DEFECT_HINTS = ("缺陷", "复印", "扫描", "CRT", "VHS", "胶片", "噪点", "压缩", "印刷")
LIGHT_HINTS = ("光", "lighting", "light", "灯", "色彩", "霓虹", "horror lighting")
GENERIC_WORDS = {
    "a",
    "and",
    "art",
    "cinema",
    "cinematic",
    "color",
    "colored",
    "design",
    "editorial",
    "film",
    "glossy",
    "high",
    "illustration",
    "light",
    "lighting",
    "low",
    "modern",
    "old",
    "photo",
    "photography",
    "poster",
    "render",
    "retro",
    "soft",
    "style",
    "surreal",
    "the",
    "vintage",
    "with",
}
SUPPORT_PROBABILITY = {
    "subject-first": 0.35,
    "balanced": 0.75,
    "style-forward": 1.0,
}
T = TypeVar("T")


def slugify(text: str, limit: int = 52) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    text = text.strip("-")
    return text[:limit].strip("-") or "open-style"


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def style_category(style: dict[str, Any]) -> str:
    return str(style.get("类别", "")).strip()


def style_id(style: dict[str, Any]) -> str:
    return str(style.get("style_id", "")).strip()


def style_name(style: dict[str, Any]) -> str:
    return str(style.get("中文风格名", "")).strip()


def style_tokens(style: dict[str, Any]) -> str:
    return str(style.get("English prompt tokens", "")).strip()


def style_dna(style: dict[str, Any]) -> str:
    return str(style.get("视觉DNA / 关键词", "")).strip()


def style_light_material(style: dict[str, Any]) -> str:
    return str(style.get("材质/色彩/光线", "")).strip()


def unique_parts(parts: list[str]) -> list[str]:
    result = []
    seen = set()
    for part in parts:
        value = part.strip()
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result


def style_phrase(style: dict[str, Any] | None) -> str:
    if not style:
        return ""
    return "，".join(unique_parts([style_name(style), style_dna(style), style_light_material(style)]))


def style_record(style: dict[str, Any] | None) -> dict[str, Any] | None:
    if not style:
        return None
    return {
        "style_id": style_id(style),
        "name": style_name(style),
        "category": style_category(style),
        "tokens": style_tokens(style),
        "visual_dna": style_dna(style),
        "material_color_light": style_light_material(style),
        "recommended_strength": style.get("建议强度", ""),
        "role": style.get("组合角色", ""),
        "suitable_subjects": style.get("适合主体", ""),
        "risk": style.get("容易翻车", ""),
        "fix": style.get("补救提示", ""),
        "source_batch": style.get("来源批次", ""),
    }


def has_any(text: str, hints: tuple[str, ...]) -> bool:
    lower = text.lower()
    return any(hint.lower() in lower for hint in hints)


def meaningful_terms(style: dict[str, Any]) -> set[str]:
    words = re.findall(r"[a-z0-9]+", style_tokens(style).lower())
    return {word for word in words if len(word) > 2 and word not in GENERIC_WORDS}


def too_similar(style: dict[str, Any], seen_term_sets: list[set[str]]) -> bool:
    terms = meaningful_terms(style)
    if not terms:
        return False
    for seen in seen_term_sets:
        shared = terms & seen
        if len(shared) >= 2 and len(shared) / max(1, min(len(terms), len(seen))) >= 0.5:
            return True
    return False


def style_weight(
    style: dict[str, Any],
    freshness: str,
    style_history: Counter[str],
    avoid_generic: bool = True,
) -> float:
    weight = 1.0
    terms = meaningful_terms(style)
    if freshness == "high":
        if style.get("来源批次"):
            weight *= 3.0
        if len(terms) >= 4:
            weight *= 1.4
    if avoid_generic:
        token_count = max(1, len(re.findall(r"[a-z0-9]+", style_tokens(style).lower())))
        specificity = len(terms) / token_count
        if len(terms) <= 1 or specificity < 0.35:
            weight *= 0.25
    used_count = style_history.get(style_id(style), 0)
    if used_count:
        weight /= 1 + (0.85 * used_count)
    return max(weight, 0.01)


def weighted_pick(rng: random.Random, items: list[T], weights: list[float]) -> T | None:
    if not items:
        return None
    total = sum(weights)
    if total <= 0:
        return rng.choice(items)
    threshold = rng.random() * total
    current = 0.0
    for item, weight in zip(items, weights):
        current += weight
        if current >= threshold:
            return item
    return items[-1]


def pick_text(rng: random.Random, items: list[str], history: Counter[str] | None = None) -> str:
    weights = [1 / (1 + 0.7 * (history or Counter()).get(item, 0)) for item in items]
    picked = weighted_pick(rng, items, weights)
    if picked is None:
        raise ValueError("Cannot pick from an empty source pool.")
    return picked


def pick_unique_style(
    rng: random.Random,
    items: list[dict[str, Any]],
    state: dict[str, Any],
    freshness: str,
    style_history: Counter[str],
) -> dict[str, Any] | None:
    if not items:
        return None

    def eligible(relax_category: bool = False, relax_similarity: bool = False, relax_used: bool = False) -> list[dict[str, Any]]:
        result = []
        for style in items:
            sid = style_id(style)
            if not relax_used and sid in state["used_style_ids"]:
                continue
            if not relax_category and state["last_category"] == style_category(style):
                continue
            if not relax_similarity and too_similar(style, state["term_sets"]):
                continue
            result.append(style)
        return result

    candidates = eligible()
    if not candidates:
        candidates = eligible(relax_category=True)
    if not candidates:
        candidates = eligible(relax_category=True, relax_similarity=True)
    if not candidates:
        candidates = eligible(relax_category=True, relax_similarity=True, relax_used=True)

    weights = [style_weight(style, freshness, style_history) for style in candidates]
    picked = weighted_pick(rng, candidates, weights)
    if picked:
        state["used_style_ids"].add(style_id(picked))
        terms = meaningful_terms(picked)
        if terms:
            state["term_sets"].append(terms)
        state["last_category"] = style_category(picked)
    return picked


def load_style_library(path: Path) -> dict[str, Any]:
    data = read_json(path)
    styles = data.get("styles", [])
    if not isinstance(styles, list) or not styles:
        raise ValueError(f"Style library has no styles: {path}")
    return data


def style_pools(styles: list[dict[str, Any]], style_family: str | None) -> dict[str, list[dict[str, Any]]]:
    family_categories = STYLE_FAMILIES.get(style_family or "", set())
    base_categories = family_categories or BASE_CATEGORIES
    base = [style for style in styles if style_category(style) in base_categories]
    if not base:
        base = [style for style in styles if style_category(style) in BASE_CATEGORIES]

    surface = [style for style in styles if style_category(style) in SURFACE_CATEGORIES]
    fmt = [style for style in styles if style_category(style) in FORMAT_CATEGORIES]
    space = [style for style in styles if style_category(style) in SPACE_CATEGORIES]
    fashion = [style for style in styles if style_category(style) in FASHION_CATEGORIES]
    defect = [
        style
        for style in styles
        if has_any(" ".join([style_category(style), style_name(style), style_tokens(style), str(style.get("组合角色", ""))]), DEFECT_HINTS)
    ]
    light = [
        style
        for style in styles
        if has_any(" ".join([style_name(style), style_tokens(style), style_light_material(style)]), LIGHT_HINTS)
        and style_category(style) not in SURFACE_CATEGORIES
    ]
    return {
        "base": base,
        "auxiliary": surface + fmt + space + fashion + defect + light,
    }


def load_history(enabled: bool) -> dict[str, Any]:
    history = {
        "enabled": enabled,
        "runs_scanned": 0,
        "subjects": Counter(),
        "lighting": Counter(),
        "style_ids": Counter(),
    }
    if not enabled:
        return history

    manifest_paths = sorted((ROOT / "runs").glob("*/manifest.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for manifest_path in manifest_paths[:120]:
        try:
            manifest = read_json(manifest_path)
        except (OSError, json.JSONDecodeError):
            continue
        history["runs_scanned"] += 1
        for item in manifest.get("prompts", []):
            layers = item.get("layers") or {}
            if layers.get("subject"):
                history["subjects"][layers["subject"]] += 1
            if layers.get("lighting"):
                history["lighting"][layers["lighting"]] += 1
            selection = item.get("style_selection") or {}
            for key in ("main_style", "auxiliary_style"):
                sid = ((selection.get(key) or {}).get("style_id") or "").strip()
                if sid:
                    history["style_ids"][sid] += 1
    return history


def select_styles(
    styles: list[dict[str, Any]],
    pool: dict[str, Any],
    rng: random.Random,
    style_state: dict[str, Any],
    history: dict[str, Any],
    subject: str,
    lighting: str,
    style_family: str | None,
    freshness: str,
    style_strength: str,
) -> dict[str, Any]:
    if not styles:
        fallback = pick_text(rng, pool.get("style_languages", ["original visual style"]))
        return {
            "selection_mode": "fallback-source-pool",
            "style_strength": style_strength,
            "freshness": freshness,
            "main_style": {
                "style_id": "fallback-style-language",
                "name": fallback,
                "category": "source_pool",
                "tokens": "",
                "visual_dna": fallback,
                "material_color_light": "",
                "recommended_strength": "",
                "role": "主风格",
                "suitable_subjects": "",
                "risk": "",
                "fix": "Install automation/rare_style_library.json for rare-style metadata.",
                "source_batch": "",
            },
            "auxiliary_style": None,
            "history_dedupe": {
                "enabled": history["enabled"],
                "runs_scanned": history["runs_scanned"],
                "subject_recent_count": history["subjects"].get(subject, 0),
                "lighting_recent_count": history["lighting"].get(lighting, 0),
                "main_style_recent_count": 0,
                "auxiliary_style_recent_count": 0,
            },
        }

    pools = style_pools(styles, style_family)
    main = pick_unique_style(rng, pools["base"], style_state, freshness, history["style_ids"])
    auxiliary = None
    if rng.random() <= SUPPORT_PROBABILITY[style_strength]:
        auxiliary_candidates = [style for style in pools["auxiliary"] if style_id(style) != style_id(main or {})]
        auxiliary = pick_unique_style(rng, auxiliary_candidates, style_state, freshness, history["style_ids"])

    main_record = style_record(main)
    auxiliary_record = style_record(auxiliary)
    return {
        "selection_mode": f"style-family:{style_family}" if style_family else "mixed",
        "style_strength": style_strength,
        "freshness": freshness,
        "main_style": main_record,
        "auxiliary_style": auxiliary_record,
        "history_dedupe": {
            "enabled": history["enabled"],
            "runs_scanned": history["runs_scanned"],
            "subject_recent_count": history["subjects"].get(subject, 0),
            "lighting_recent_count": history["lighting"].get(lighting, 0),
            "main_style_recent_count": history["style_ids"].get((main_record or {}).get("style_id", ""), 0),
            "auxiliary_style_recent_count": history["style_ids"].get((auxiliary_record or {}).get("style_id", ""), 0),
        },
    }


def format_style_layer(selection: dict[str, Any], style_strength: str) -> str:
    main = selection.get("main_style") or {}
    auxiliary = selection.get("auxiliary_style")
    main_phrase = "，".join(unique_parts([main.get("name", ""), main.get("visual_dna", ""), main.get("material_color_light", "")]))
    aux_phrase = ""
    if auxiliary:
        aux_phrase = "；辅助风格只作为弱层：" + "，".join(
            unique_parts([auxiliary.get("name", ""), auxiliary.get("visual_dna", ""), auxiliary.get("material_color_light", "")])
        )
    if style_strength == "subject-first":
        priority = "主体身份和动作优先，风格只作用于色彩、材质和构图语言"
    elif style_strength == "balanced":
        priority = "主体可读性和风格显性并重"
    else:
        priority = "主风格必须清晰可见，避免坍缩成泛化电影写实"
    return f"{main_phrase}{aux_phrase}；{priority}"


def build_prompt(
    pool: dict[str, Any],
    styles: list[dict[str, Any]],
    index: int,
    rng: random.Random,
    style_state: dict[str, Any],
    history: dict[str, Any],
    style_family: str | None,
    freshness: str,
    style_strength: str,
) -> dict[str, Any]:
    subject = pick_text(rng, pool["subjects"], history["subjects"] if history["enabled"] else None)
    environment = pick_text(rng, pool["environments"])
    lighting = pick_text(rng, pool["lighting"], history["lighting"] if history["enabled"] else None)
    material = pick_text(rng, pool["materials"])
    composition = pick_text(rng, pool["composition_camera"])
    expression = pick_text(rng, pool["expression_acting"])
    tone = pick_text(rng, pool["tone_goals"])
    ratio = pick_text(rng, pool["aspect_ratios"])
    avoid = ", ".join(pool["avoid"])
    style_selection = select_styles(
        styles,
        pool,
        rng,
        style_state,
        history,
        subject,
        lighting,
        style_family,
        freshness,
        style_strength,
    )
    style_layer = format_style_layer(style_selection, style_strength)

    title = f"{index:02d}_{slugify(subject)}"
    prompt = f"""Open Style Atlas image {index:02d}. {tone}.

[Subject]
{subject}. Acting and expression: {expression}.

[Environment]
{environment}; the space must shape the story and remain readable.

[Lighting and Atmosphere]
{lighting}.

[Material and Texture]
{material}.

[Composition and Camera]
{composition}.

[Style]
{style_layer}.

[Context, Intent, and Tone]
{tone}; make it feel like one original frame from an unknown visual world.

[Output Constraints]
Aspect ratio {ratio}. Must include the subject, the chosen environment, and visible rare-style DNA. Avoid {avoid}.
"""

    return {
        "index": index,
        "title": title,
        "aspect_ratio": ratio,
        "layers": {
            "subject": subject,
            "environment": environment,
            "lighting": lighting,
            "material": material,
            "composition_camera": composition,
            "style": style_layer,
            "expression": expression,
            "tone": tone,
        },
        "style_selection": style_selection,
        "prompt": prompt,
    }


def lint_score(prompt_text: str, tmp_file: Path) -> int:
    tmp_file.write_text(prompt_text, encoding="utf-8")
    result = subprocess.run(
        [
            "python",
            str(PROMPT_LINT),
            str(tmp_file),
            "--architecture",
            "seven-layer",
            "--model",
            "dreamina",
        ],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    match = re.search(r"Score:\s*(\d+)/10", result.stdout)
    return int(match.group(1)) if match else 0


def build_prompt_with_gate(
    pool: dict[str, Any],
    styles: list[dict[str, Any]],
    index: int,
    tmp_dir: Path,
    min_score: int,
    max_attempts: int,
    rng: random.Random,
    style_state: dict[str, Any],
    history: dict[str, Any],
    style_family: str | None,
    freshness: str,
    style_strength: str,
) -> dict[str, Any]:
    last_item = None
    tmp_file = tmp_dir / f"_lint_{index:02d}.txt"
    for _ in range(max_attempts):
        item = build_prompt(pool, styles, index, rng, style_state, history, style_family, freshness, style_strength)
        item["lint_score"] = lint_score(item["prompt"], tmp_file)
        last_item = item
        if item["lint_score"] >= min_score:
            return item
    last_score = (last_item or {}).get("lint_score", 0)
    raise RuntimeError(f"Could not build prompt {index:02d} at lint score {min_score}/10 after {max_attempts} attempts; last score was {last_score}/10.")


def relative_to_run(path: Path, out_dir: Path) -> str:
    return str(path.relative_to(out_dir))


def write_batch(
    out_dir: Path,
    count: int,
    pool: dict[str, Any],
    style_library: dict[str, Any],
    seed: int | None,
    eagle_folder: str,
    min_lint_score: int,
    max_attempts: int,
    style_family: str | None,
    freshness: str,
    style_strength: str,
    history: dict[str, Any],
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir = out_dir / "prompts"
    images_dir = out_dir / "images"
    prompts_dir.mkdir(exist_ok=True)
    images_dir.mkdir(exist_ok=True)
    for stale_prompt in prompts_dir.glob("*.txt"):
        stale_prompt.unlink()

    rng = random.Random(seed)
    style_state: dict[str, Any] = {"used_style_ids": set(), "term_sets": [], "last_category": None}
    styles = style_library.get("styles", [])
    prompts = [
        build_prompt_with_gate(
            pool,
            styles,
            i,
            out_dir,
            min_lint_score,
            max_attempts,
            rng,
            style_state,
            history,
            style_family,
            freshness,
            style_strength,
        )
        for i in range(1, count + 1)
    ]
    for tmp in out_dir.glob("_lint_*.txt"):
        tmp.unlink(missing_ok=True)
    for item in prompts:
        (prompts_dir / f"{item['title']}.txt").write_text(item["prompt"], encoding="utf-8")

    manifest = {
        "batch_id": out_dir.name,
        "prompt_contract_version": PROMPT_CONTRACT_VERSION,
        "created_at_local": datetime.now().astimezone().isoformat(),
        "seed": seed,
        "count": count,
        "eagle_folder": eagle_folder,
        "image_generation_status": "pending",
        "style_library_version": style_library.get("version", "unknown"),
        "style_family": style_family,
        "freshness": freshness,
        "style_strength": style_strength,
        "history_dedupe": {
            "enabled": history["enabled"],
            "runs_scanned": history["runs_scanned"],
        },
        "prompts": [
            {
                "index": item["index"],
                "title": item["title"],
                "aspect_ratio": item["aspect_ratio"],
                "lint_score": item.get("lint_score"),
                "prompt_file": relative_to_run(prompts_dir / f"{item['title']}.txt", out_dir),
                "layers": item["layers"],
                "style_selection": item["style_selection"],
            }
            for item in prompts
        ],
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    queue_lines = [
        "# Generation Queue",
        "",
        "Generate one image for each prompt file below. Save outputs in `images/` with matching numeric prefixes.",
        "",
    ]
    for item in prompts:
        main_style = (item["style_selection"].get("main_style") or {}).get("name", "fallback style")
        prompt_filename = f"{item['title']}.txt"
        queue_lines.append(
            f"- `{item['index']:02d}` `{(prompts_dir / prompt_filename).name}` "
            f"ratio `{item['aspect_ratio']}` style `{main_style}`"
        )
    (out_dir / "generation_queue.md").write_text("\n".join(queue_lines) + "\n", encoding="utf-8")

    import_cmd = (
        f'python "{EAGLE_IMPORT}" "{images_dir}\\*.png" "{images_dir}\\*.jpg" '
        f'--folder-name "{eagle_folder}" '
        f'--tag "Codex Image,AI generated,Open Style Atlas,seven-layer,rare-style,v0.15" '
        f'--annotation-file "{out_dir / "manifest.json"}"'
    )
    (out_dir / "import_to_eagle.ps1").write_text(import_cmd + "\n", encoding="utf-8")


def import_images(batch_dir: Path, eagle_folder: str) -> int:
    images_dir = batch_dir / "images"
    paths = sorted([*images_dir.glob("*.png"), *images_dir.glob("*.jpg"), *images_dir.glob("*.jpeg")])
    if not paths:
        raise SystemExit(f"No images found in {images_dir}")
    cmd = [
        "python",
        str(EAGLE_IMPORT),
        *[str(p) for p in paths],
        "--folder-name",
        eagle_folder,
        "--tag",
        "Codex Image,AI generated,Open Style Atlas,seven-layer,rare-style,v0.15",
        "--annotation-file",
        str(batch_dir / "manifest.json"),
    ]
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare Open Style Atlas v0.15 prompt batches.")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--pool", type=Path, default=POOL_PATH)
    parser.add_argument("--style-library", type=Path, default=STYLE_LIBRARY_PATH)
    parser.add_argument("--style-family", choices=sorted(STYLE_FAMILIES))
    parser.add_argument("--freshness", choices=["normal", "high"], default="high")
    parser.add_argument("--style-strength", choices=sorted(SUPPORT_PROBABILITY), default="style-forward")
    parser.add_argument("--no-history", action="store_true")
    parser.add_argument("--eagle-folder", default="AI风格探索")
    parser.add_argument("--min-lint-score", type=int, default=8)
    parser.add_argument("--max-attempts", type=int, default=8)
    parser.add_argument("--import-images", action="store_true")
    args = parser.parse_args()

    if args.import_images:
        batch_dir = args.out or Path.cwd()
        raise SystemExit(import_images(batch_dir.resolve(), args.eagle_folder))

    pool = read_json(args.pool)
    style_library = load_style_library(args.style_library)
    history = load_history(not args.no_history)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out or ROOT / "runs" / f"{stamp}-open-style-auto"
    write_batch(
        out_dir.resolve(),
        args.count,
        pool,
        style_library,
        args.seed,
        args.eagle_folder,
        args.min_lint_score,
        args.max_attempts,
        args.style_family,
        args.freshness,
        args.style_strength,
        history,
    )
    print(out_dir.resolve())


if __name__ == "__main__":
    main()
