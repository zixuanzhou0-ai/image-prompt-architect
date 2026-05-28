# Install

This repository is a Codex plugin project. It uses the standard root layout:

```text
.codex-plugin/plugin.json
skills/image-prompt-architect/SKILL.md
```

## Marketplace-Style Install

If your Codex CLI supports plugin marketplace sources:

```bash
codex plugin marketplace add zixuanzhou0-ai/image-prompt-architect --ref main
codex plugin marketplace list
codex plugin marketplace upgrade
```

This repository is a plugin project root. If your CLI expects a marketplace index rather than a plugin root, use direct skill installation instead.

## Direct Skill Use

Copy `skills/image-prompt-architect` into a Codex skills directory and invoke:

```text
$image-prompt-architect Build a series bible for a three-image product campaign.
```

## Smoke Test

```text
Use Image Prompt Architect to rewrite this prompt for Midjourney: "beautiful girl, city, cinematic".
```

## Troubleshooting

- Plugin not appearing: verify your Codex app/CLI supports local plugin projects.
- Skill not triggering: invoke `$image-prompt-architect` explicitly.
- Tests failing: run `python -m pip install pytest` and retry `python -m pytest`.
- Strict lint unexpectedly passes a bad prompt: add a fixture and expected critical failure.

