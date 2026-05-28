# Model Adapters

Use this file to adapt prompt length, language, and structure to common image models. Model behavior changes over time, so treat these as working heuristics rather than permanent laws.

## Grok / Grok Imagine

Recommended style:

- Use English for maximum precision, especially for long structured prompts.
- Use explicit seven-layer or system templates.
- Keep visual concepts concrete and repeated when they must dominate.
- Name lighting, camera, and material details directly.

Good for:

- Long, structured, cinematic prompts.
- Specific film language and detailed visual grammar.

Risk:

- Chinese prompts may lose fine detail in complex structure.
- Generic templates produce generic images.

## Dreamina / Seedream / Jimeng

Recommended style:

- Follow the local project rules when present.
- For high quality image generation, default to model 4.5 unless the user asks otherwise or project rules specify another choice.
- Use mixed prompting when effective: natural-language concept plus structured aesthetic keywords.
- Use Chinese for culturally specific concepts and English for established visual-technical terms when useful.

Good for:

- Aesthetic images, model-specific prompt libraries, and style modifiers.

Risk:

- Overly abstract prompts can drift unless anchored by subject, scene, style, and constraints.

## GPT Image / ChatGPT Images / OpenAI Image Models

Recommended style:

- Use clear natural language with enough structure to express priorities.
- Avoid unnecessarily huge keyword piles when the model can reason over intent.
- Give composition, text rendering, and editing instructions explicitly.
- For API image generation tools, remember the mainline model may revise prompts for performance and expose `revised_prompt` in tool output.

Useful current facts:

- `gpt-image-2` is documented as a state-of-the-art image generation and editing model with text and image input and image output.
- OpenAI's image generation tool documentation states it uses GPT Image models and automatically optimizes text inputs for improved performance.
- ChatGPT Images 2.0 system-card material describes enhanced instruction following, detail generation, and a thinking mode that can turn a basic prompt into a more thought-through final image.

Language strategy:

- Chinese is often usable for direct conceptual prompts and Chinese text rendering.
- English can still be useful for precise technical art direction, complex lighting, lens, and production terminology.
- Prefer bilingual prompts only when each language carries a real advantage.

## Midjourney

Recommended style:

- Use compact, image-forward prompts.
- Put subject, environment, style, camera, and mood in a concise order.
- Use parameters separately when the user provides them or asks for Midjourney output.

Risk:

- Over-explaining can dilute the prompt.

## Flux / Stable Diffusion

Recommended style:

- Use concrete English visual terms.
- Separate positive and negative prompts if the interface supports it.
- Keep token weighting syntax only when the target interface supports it.

Risk:

- Long narrative prose can be less effective than dense visual phrases for some workflows.

## General Adapter Decision

- If the model is literal and prompt-sensitive: use seven-layer or system structure.
- If the model reasons and rewrites prompts: use clear natural language plus essential constraints.
- If the output is a series: use system template or hybrid.
- If the output is one hero image: use seven-layer.
- If the user is learning: always include the tagged version before the copy-ready version.

