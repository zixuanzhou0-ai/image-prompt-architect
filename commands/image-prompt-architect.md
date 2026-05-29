---
description: "Design, rewrite, critique, or port AI image prompt text"
argument-hint: "[prompt or request]"
---

# Image Prompt Architect

Treat this command as an explicit request to use the `image-prompt-architect` skill. If the plugin-prefixed skill name is available, use `image-prompt-architect:image-prompt-architect`.

If `$ARGUMENTS` is empty, ask the user for the prompt text or image-prompt task they want handled.

If `$ARGUMENTS` is provided:

1. Use the `image-prompt-architect` skill workflow.
2. Select the right mode from the request:
   - quick prompt
   - standard build
   - critique
   - model port
   - series bible
3. Follow target-model syntax when the user names GPT Image, Midjourney, FLUX, Grok, Dreamina/Seedream, or Stable Diffusion.
4. Return copy-ready prompt text when the user asks for a prompt.
5. Do not generate or edit images unless the user separately asks for image generation or image editing.

User request:

```text
$ARGUMENTS
```
