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
- **Prompt compression / final render prompt**: user has a long analysis prompt or seven-layer draft and needs the clean prompt to actually paste into a model. Output priority stack, compressed prompt, and dropped/compressed details.
- **Revision prompt from failure**: user describes a failed image output. Output failure type, preserve/change plan, and a copy-ready repair prompt.
- **Reference image role planning**: user has one or more reference images. Output what each reference controls, what it must not control, and a prompt with reference roles.

For exact schemas, read `references/output-contract.md`.

## Mode Precedence

If multiple modes apply:

1. Choose **Revision prompt from failure** first when the user describes a generated image failure or asks how to fix a bad output.
2. Choose **Reference image role planning** first when reference images must control identity, product geometry, pose, composition, palette, or style.
3. Choose **Critique** when the user provides an existing prompt and asks what is wrong.
4. Choose **Model port** when source and target models are named.
5. Choose **Series bible** when multiple images or continuity are required.
6. Choose **Prompt compression / final render prompt** when the user asks for the final paste-ready prompt, a shorter model prompt, or cleaner GPT Image output from a long draft.
7. Choose **Standard build** for structured creation or rewrite.
8. Choose **Quick prompt** only when the user asks for speed or gives a simple one-off request.

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
- For GPT Image-like models, is the final render prompt short enough, prioritized, and clean enough to avoid dirty texture/noise overload?

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
