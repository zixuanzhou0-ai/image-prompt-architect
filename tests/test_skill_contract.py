from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "image-prompt-architect" / "SKILL.md"
OUTPUT_CONTRACT = ROOT / "skills" / "image-prompt-architect" / "references" / "output-contract.md"
SEVEN_LAYER = ROOT / "skills" / "image-prompt-architect" / "references" / "seven-layer-framework.md"
MODEL_ADAPTERS = ROOT / "skills" / "image-prompt-architect" / "references" / "model-adapters.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_mode_precedence_includes_quality_loop_modes():
    text = read(SKILL)
    assert "Revision prompt from failure" in text
    assert "Reference image role planning" in text
    assert "Prompt compression / final render prompt" in text
    assert text.index("Choose **Revision prompt from failure** first") < text.index("Choose **Critique**")


def test_output_contract_has_compression_revision_and_reference_schemas():
    text = read(OUTPUT_CONTRACT)
    assert "## Prompt Compression / Final Render Prompt" in text
    assert "**Priority Stack**" in text
    assert "**Dropped / Compressed**" in text
    assert "## Revision Prompt From Failure" in text
    assert "**Preserve**" in text
    assert "**Change**" in text
    assert "## Reference Image Role Planning" in text
    assert "product geometry" in text


def test_seven_layer_framework_defines_internal_and_final_prompt_split():
    text = read(SEVEN_LAYER)
    assert "Internal Analysis Draft" in text
    assert "Final Render Prompt" in text
    assert "80-160 words" in text
    assert "Priority 1: subject readability" in text


def test_model_adapters_document_clean_render_and_wrapper_boundaries():
    text = read(MODEL_ADAPTERS)
    assert "Clean render strategy" in text
    assert "GPT Image / GPT Image 2-style final render prompts" in text
    assert "Render strategy" in text
    assert "Boundary strategy" in text
    assert "Dreamina/Jimeng UI-style work" in text
