# Prompt Eval Report

Generated from `evals/prompt_cases.yml` using structural prompt lint only.
Image-output scoring still requires `evals/image_output_protocol.md`.

| Case | Model | Mode | Source | Rewrite | Delta | Critical | Warnings | Expected Risks |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `generic_city_girl` | `gpt-image` | `critique` | 0 | 4 | 4 | 1 | 1 | generic filler; missing lighting source; missing camera/composition |
| `flux_negative` | `flux` | `model-port` | 0 | 10 | 10 | 3 | 1 | negative prompt unsupported; needs positive replacements |
| `midjourney_params` | `midjourney` | `critique` | 0 | 7 | 7 | 2 | 1 | parameters not at end |
| `gpt_image_text_rendering` | `gpt-image` | `standard` | 0 | 9 | 9 | 1 | 2 | exact text not quoted; layout underspecified |
| `gpt_image_edit_preserve_change` | `gpt-image` | `critique` | 4 | 10 | 6 | 0 | 2 | missing preserve/change split; product geometry drift |
| `midjourney_no_phrase` | `midjourney` | `critique` | 4 | 7 | 3 | 0 | 2 | ambiguous multiword --no phrase; needs positive period-costume anchors |
| `midjourney_oref_style_ref` | `midjourney` | `model-port` | 1 | 7 | 6 | 1 | 1 | reference role unclear; missing lighting/composition controls |
| `flux_plain_negation` | `flux` | `critique` | 0 | 5 | 5 | 2 | 1 | plain negation should become positive replacement; lighting intent unclear |
| `flux_structured_brand_color` | `flux` | `standard` | 0 | 5 | 5 | 1 | 1 | brand color lacks hex code; product material and lighting underspecified |
| `dreamina_bilingual_cultural_scene` | `dreamina` | `standard` | 5 | 10 | 5 | 0 | 1 | too little concrete cultural detail; generic quality filler |
| `grok_reference_image_generation` | `grok` | `standard` | 1 | 10 | 9 | 1 | 1 | reference role unclear; missing model settings outside prose |
| `series_identity_drift` | `gpt-image` | `series` | 0 | 6 | 6 | 2 | 1 | identity lock missing; variation budget missing; shot slots missing |
| `product_photo_constraints` | `flux` | `model-port` | 0 | 6 | 6 | 2 | 1 | negative language needs positive replacement; material and geometry constraints underspecified |
