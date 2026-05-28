---
name: image-prompt-architect
description: Create and improve prompt text for AI image models. Use for image prompt rewriting, critique, model-porting, prompt linting, cinematic series bibles, and reusable visual style systems. Do not trigger for ordinary image generation, image editing, or visual analysis unless the user explicitly asks for prompt text, prompt structure, or model adaptation.
---

# Image Prompt Architect

## Core Principle

Treat prompt structure as a scaffold, not the art itself. Strong image prompts need concrete visual substance: specific subjects, spatial logic, light, materiality, camera grammar, style anchors, constraints, and iteration knobs.

Never fill a template with vague praise words alone. If a layer is generic, infer concrete details from the user's intent or ask one concise question when guessing would change the output.

## Mode Selection

Choose one mode before drafting.

- **Quick prompt**: user wants one prompt fast. Output a copy-ready prompt plus 2-3 iteration knobs.
- **Standard build**: user wants a new or rewritten prompt. Output architecture choice, tagged prompt, copy-ready prompt, model notes, and iteration knobs.
- **Critique**: user provides an existing prompt. Output diagnosis, severity, missing controls, contradictions, and a rewritten prompt.
- **Model port**: user wants a prompt adapted from one model to another. Output target-model risks, converted prompt, parameter/negative handling, and what changed.
- **Series bible**: user wants multiple images, cinematic stills, a set, or a consistent visual world. Output continuity rules, variation budget, shot slots, and per-shot prompts.

For exact schemas, read `references/output-contract.md`.

## Mode Precedence

If multiple modes apply:

1. Choose **Critique** first when the user provides an existing prompt and asks what is wrong.
2. Choose **Model port** first when source and target models are named.
3. Choose **Series bible** first when multiple images or continuity are required.
4. Choose **Standard build** for structured creation or rewrite.
5. Choose **Quick prompt** only when the user asks for speed or gives a simple one-off request.

Quick mode must still follow model-native syntax when a target model is named.

## Architecture Choice

- Use **seven-layer structure** for a single image that needs precise control. Read `references/seven-layer-framework.md`.
- Use **multi-system modular template** for cinematic series, style bibles, and visual worlds. Read `references/system-template-framework.md`.
- Use **hybrid architecture** when the user needs both precise single-frame control and continuity across a set.
- Use **compact natural-language architecture** when the target model reasons over or revises prompts well. Check `references/model-adapters.md` before making model claims.

## Model Adaptation

Read `references/model-adapters.md` when:

- the user names a model or platform;
- the prompt must be ported between models;
- negative prompts, parameters, reference images, text rendering, or API fields matter.

Do not overclaim model behavior. If a model behavior is not documented or not locally tested, present it as a heuristic.

## Quality Gate

Before finalizing, apply `references/checklist.md` or `references/evaluation-rubric.md`:

- Is the subject drawable and specific?
- Does the environment shape the image?
- Are lighting, material, camera, style, and constraints explicit?
- Is the prompt shaped for the target model?
- Are avoid/negative instructions handled in the model's native way?

For file-based prompts, optionally run:

```bash
python skills/image-prompt-architect/scripts/prompt_lint.py prompt.txt --architecture auto --model generic
```

## Reference Map

- `references/output-contract.md`: response modes and schemas.
- `references/seven-layer-framework.md`: single-image structure.
- `references/system-template-framework.md`: cinematic series and continuity systems.
- `references/model-adapters.md`: versioned model adapter matrix.
- `references/checklist.md`: quick quality gate.
- `references/evaluation-rubric.md`: scoring rubric.
- `references/examples.md`: worked examples and reusable skeletons.
