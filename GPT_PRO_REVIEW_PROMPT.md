# Prompt for GPT Pro Review

You are reviewing a Codex plugin repository named `image-prompt-architect`.

I want you to act as a senior prompt-engineering researcher, image-generation workflow designer, and Codex skill/plugin architect. Please review the repository in extreme detail and give actionable suggestions.

Before criticizing model-specific claims, verify current official documentation where possible. Flag any adapter statement that is not supported by current primary sources or by explicit local testing.

Repository goal:

- Turn an image-prompt methodology into a reusable Codex skill/plugin.
- Support two core prompt architectures:
  - Seven-layer structure: subject, environment, lighting/atmosphere, material/texture, composition/camera, style, era/artistic tone.
  - Multi-system modular template: premise, spatial system, character system, color system, medium system, composition system, lighting/atmosphere system, narrative/emotion system, quality/exclusion system.
- Help users create, adapt, critique, and iterate AI image prompts for Grok, Dreamina/Seedream/Jimeng, GPT Image/OpenAI image models, Midjourney, Flux, and similar systems.
- Preserve the key insight that templates are only scaffolds; high quality comes from concrete visual details, strong style anchors, model adaptation, and iteration.

Please inspect these files especially:

- `.codex-plugin/plugin.json`
- `README.md`
- `skills/image-prompt-architect/SKILL.md`
- `skills/image-prompt-architect/references/seven-layer-framework.md`
- `skills/image-prompt-architect/references/system-template-framework.md`
- `skills/image-prompt-architect/references/model-adapters.md`
- `skills/image-prompt-architect/references/checklist.md`
- `skills/image-prompt-architect/references/examples.md`
- `skills/image-prompt-architect/scripts/prompt_lint.py`

Please evaluate:

1. Skill trigger quality
   - Is the `description` in `SKILL.md` clear enough to trigger at the right time?
   - Is it too broad or too narrow?
   - What exact wording would you improve?

2. Progressive disclosure
   - Is `SKILL.md` concise enough?
   - Are references split correctly?
   - Should anything move from `SKILL.md` to references or from references back into `SKILL.md`?

3. Prompt-framework quality
   - Are the seven layers correct and useful?
   - Are any layers missing, redundant, or named poorly?
   - Is the multi-system modular framework useful for cinematic series and consistent visual worlds?
   - Are there better names for either framework?

4. Model adaptation accuracy
   - Review the model-adapter guidance for Grok, Dreamina/Seedream/Jimeng, GPT Image/OpenAI image models, Midjourney, and Flux.
   - Identify claims that are too strong, outdated, unverifiable, or should be softened.
   - Suggest model-specific prompt strategies that are more accurate.

5. Output contract
   - Does the skill produce outputs that are useful for learning and copying?
   - Should the skill always produce tagged prompts, copy-ready prompts, negative prompts, model notes, and iteration knobs?
   - What should change for quick requests?

6. Practicality
   - Would an agent using this skill actually create better image prompts?
   - Where might it still produce generic template-filled results?
   - What guardrails should be added to force specificity?

7. `prompt_lint.py`
   - Is this script useful?
   - What additional checks should it perform?
   - Should it detect style-anchor repetition, prompt length by model, negative prompt quality, or contradiction between systems?

8. Missing repository pieces
   - Should this plugin include more examples?
   - Should it include test prompts?
   - Should it include an evaluation rubric?
   - Should it include example outputs or image assets?

9. Installation and distribution
   - Is the plugin structure valid and understandable?
   - What should be added before sharing publicly?

10. Give me a concrete patch plan
   - List the exact files to change.
   - For each file, say what to add, remove, or rewrite.
   - Prioritize changes as P0, P1, P2.

Important review style:

- Be direct and critical.
- Do not just praise the project.
- Find weak points.
- Make suggestions that can be implemented in a follow-up commit.
- If you think any idea is wrong, say so clearly and explain why.
- Give improved wording where possible.

Deliver your response in this format:

```markdown
## Executive Verdict

## P0 Issues

## P1 Improvements

## P2 Nice-to-Haves

## File-by-File Notes

## Suggested Rewrites

## Evaluation Rubric

## Final Recommendation
```
