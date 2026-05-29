# Install

This repository is a Codex plugin project. It uses the standard root layout:

```text
.codex-plugin/plugin.json
.claude-plugin/plugin.json
skills/image-prompt-architect/SKILL.md
```

## Marketplace-Style Install

If your Codex CLI supports plugin marketplace sources, add this repository and install the plugin:

```bash
codex plugin marketplace add zixuanzhou0-ai/image-prompt-architect --ref v0.14.0
codex plugin add image-prompt-architect@image-prompt-architect
codex plugin list --marketplace image-prompt-architect
```

To inspect the exact developer-preview files locally:

```bash
git clone --branch v0.14.0 https://github.com/zixuanzhou0-ai/image-prompt-architect.git
```

Use `--ref main` only when you intentionally want the latest unreleased state.

## Direct Skill Use

Copy `skills/image-prompt-architect` into a Codex skills directory and invoke:

```text
$image-prompt-architect Build a series bible for a three-image product campaign.
```

After plugin installation, you can also use the slash command:

```text
/image-prompt-architect Build a series bible for a three-image product campaign.
```

`v0.14.0` includes a Claude-compatible plugin manifest beside the Codex manifest so Codex Desktop can index `commands/image-prompt-architect.md` for the slash menu.

## Smoke Test

```text
Use Image Prompt Architect to rewrite this prompt for Midjourney: "beautiful girl, city, cinematic".
```

## Troubleshooting

- Plugin not appearing: verify your Codex app/CLI supports local plugin projects.
- Skill not triggering: invoke `$image-prompt-architect` explicitly.
- Tests failing: run `python -m pip install pytest` and retry `python -m pytest`.
- Strict lint unexpectedly passes a bad prompt: add a fixture and expected critical failure.
