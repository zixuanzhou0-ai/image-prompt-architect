# Image Prompt Architect

Image Prompt Architect is a Codex plugin project for building reusable AI image-prompt workflows.

It packages one skill:

- `image-prompt-architect`: creates, adapts, critiques, and iterates image prompts using a seven-layer framework, a multi-system modular template, and model-specific adapters.

## Why This Exists

The project came from a practical prompt-design insight:

Prompt structure helps, but structure alone is not enough. A good image prompt needs a strong architecture and highly specific visual content.

This skill helps choose the right architecture:

- Seven-layer structure for precise single-image control.
- Multi-system modular template for consistent cinematic series.
- Hybrid structure when both precision and visual continuity matter.
- Compact natural-language prompts for models that automatically reason over or revise prompts.

## Project Layout

```text
image-prompt-architect/
  .codex-plugin/plugin.json
  skills/image-prompt-architect/SKILL.md
  skills/image-prompt-architect/references/
  skills/image-prompt-architect/scripts/prompt_lint.py
  assets/examples/
```

## Validation

```bash
python C:/Users/Administrator/.codex/skills/.system/skill-creator/scripts/quick_validate.py E:/七层提示词/image-prompt-architect/skills/image-prompt-architect
python C:/Users/Administrator/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py E:/七层提示词/image-prompt-architect
```

## GPT Pro Review

Use `GPT_PRO_REVIEW_PROMPT.md` as the review prompt. It asks GPT Pro to review the plugin as a skill design, prompt-engineering framework, and practical image-generation workflow.

