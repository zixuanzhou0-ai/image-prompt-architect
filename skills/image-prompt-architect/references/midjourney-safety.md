# MidJourney Safety and Art-Preservation Preflight

This reference is for adapting prompts to MidJourney while preserving artistic intent under MidJourney's official PG-13/SFW rules. It is not a jailbreak guide and must not be used to evade moderation.

## Official Sources

- MidJourney Community Guidelines: https://docs.midjourney.com/docs/community-guidelines
- MidJourney Terms of Service: https://docs.midjourney.com/docs/terms-of-service
- MidJourney Prompt Basics: https://docs.midjourney.com/docs/prompts
- MidJourney Parameter List: https://docs.midjourney.com/docs/parameter-list

## Default Behavior

When a user asks for a MidJourney prompt, produce an `MJ Safe Prompt` by default:

1. Preserve art anchors: subject identity, cultural period, narrative mood, environment, lighting, color palette, camera distance/angle, fabric/material cues, and foreground/background relationships.
2. Rewrite ambiguous or sexualized wording into PG-13 visual language.
3. Keep parameters at the end of the prompt.
4. Use `--no` only for ordinary visual exclusions such as text, watermark, logo, modern cars, modern clothing, extra fingers.
5. Do not put prohibited or highly suggestive terms in `--no`.

If the original request cannot be made compliant without changing the core subject, refuse the unsafe version and offer a safe alternative direction.

## Hard-Block Categories

Treat these as critical failures for MidJourney prompt output:

- Adult content: nudity, genitals, sexual acts, pornographic framing, explicit fetish content, or intentionally sexualized imagery.
- Child safety: any sexualized minor, child, teen, schoolgirl/schoolboy, or underage-coded subject.
- Gore and graphic violence: dismemberment, mutilation, detached body parts, cannibalism, excessive blood, shootings, bombings, or shock imagery.
- Hate, harassment, or abuse: content that attacks, dehumanizes, threatens, or humiliates a person or protected group.
- Deception or misinformation: political campaign imagery, election influence, forged news, fraud, impersonation, or images meant to mislead viewers.
- Real-person harm: sexualized, defamatory, humiliating, or misleading depictions of a real person or public figure.

## Borderline-Risk Rewriting

Borderline wording should be rewritten into safe descriptive language while preserving the visual story.

| Risky wording | Safer MidJourney wording |
| --- | --- |
| young beauty, young girl, 少女, 年轻美女 | adult woman, young adult woman, adult Chinese woman |
| semi-transparent, transparent fabric, 半透明披帛 | lightweight silk shawl layered over modest clothing |
| strapless bodice, 抹胸贴合肩颈线 | structured ivory bodice under layered Tang-style Hanfu |
| seductive gaze, sensual look, 迷离眼神 | serene lowered gaze, introspective classical mood |
| body-focused chest/neck/skin language | wardrobe construction, fabric layering, posture, silhouette |
| low-res mobile portrait plus suggestive wardrobe | casual mobile-photo texture, separated from modest wardrobe cues |

## Art-Preservation Strategy

Do not reduce a prompt to bland safety language. Move intensity into safe art channels:

- Lighting: warm backlight, bloom, rim light, low-contrast shadow, haze, sunset color.
- Camera: medium shot, high angle, mobile-photo texture, shallow depth of field, foreground framing.
- Materials: silk, brocade, stone, water reflection, peony petals, metal earrings, fan surface.
- Narrative: court-lady story mood, introspection, restrained gesture, classical stillness.
- Environment: lake edge, stone bank, tree shade, calm reflection, color-separated foreground/background.

## Output Pattern

For MidJourney model-port or rewrite tasks:

```text
**MJ Safe Prompt**
<copy-ready prompt with parameters at the end>

**Art Preservation Notes**
- <what narrative, lighting, camera, materials, and cultural cues were preserved>

**Risk Tradeoffs**
- <which risky phrases were rewritten and why>
```

Only include an `Art Forward Variant` when the user explicitly asks for it. Mark it as higher moderation risk and keep it PG-13.

## Linting Expectations

`prompt_lint.py --model midjourney --mj-safety strict` should:

- Report hard-block categories as critical failures.
- Report borderline wording as warnings with safe rewrite suggestions.
- Warn when unsafe terms are placed in `--no`.
- Keep existing MidJourney parameter checks intact.
- Avoid claiming that any prompt is guaranteed to pass MidJourney's black-box moderation.
