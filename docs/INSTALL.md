# Install

This repository is a Codex plugin project. It uses the standard root layout:

```text
.codex-plugin/plugin.json
skills/image-prompt-architect/SKILL.md
```

## Local Plugin Use

1. Clone the repository.
2. Add or link it through the Codex plugin workflow available in your Codex app/CLI environment.
3. Confirm the plugin appears as `image-prompt-architect`.
4. Test it with:

```text
Use Image Prompt Architect to rewrite this prompt for Midjourney: "beautiful girl, city, cinematic".
```

## Direct Skill Use

Copy `skills/image-prompt-architect` into a Codex skills directory and invoke:

```text
$image-prompt-architect Build a series bible for a three-image product campaign.
```

