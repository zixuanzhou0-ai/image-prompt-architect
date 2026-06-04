# Prompt Eval Report

Generated from `evals/prompt_cases.yml` using structural prompt lint only.
`Skill` columns use `skill_output_prompt` fields, with `evals/skill_outputs.json` as a fallback; this is not a Codex router simulator.
`Skill Source` records whether the prompt was a manual capture, Codex run, or golden reference.
Image-output scoring still requires `evals/image_output_protocol.md`.

| Case | Model | Mode | Skill Source | Source | Candidate | Candidate Delta | Skill | Skill Delta | Features | Missing Features | Expected Risks |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `generic_city_girl` | `gpt-image` | `critique` | `manual_capture` | 0 | 5 | 5 | 5 | 5 | 5/5 | - | generic filler; missing lighting source; missing camera/composition |
| `flux_negative` | `flux` | `model-port` | `manual_capture` | 0 | 10 | 10 | 7 | 7 | 3/3 | - | negative prompt unsupported; needs positive replacements |
| `midjourney_params` | `midjourney` | `critique` | `manual_capture` | 0 | 7 | 7 | 7 | 7 | 4/4 | - | parameters not at end |
| `gpt_image_text_rendering` | `gpt-image` | `standard` | `manual_capture` | 0 | 9 | 9 | 6 | 6 | 4/4 | - | exact text not quoted; layout underspecified |
| `gpt_image_edit_preserve_change` | `gpt-image` | `critique` | `manual_capture` | 4 | 10 | 6 | 10 | 6 | 3/3 | - | missing preserve/change split; product geometry drift |
| `midjourney_no_phrase` | `midjourney` | `critique` | `manual_capture` | 4 | 7 | 3 | 7 | 3 | 3/3 | - | ambiguous multiword --no phrase; needs positive period-costume anchors |
| `midjourney_oref_style_ref` | `midjourney` | `model-port` | `manual_capture` | 1 | 7 | 6 | 7 | 6 | 2/2 | - | reference role unclear; missing lighting/composition controls |
| `flux_plain_negation` | `flux` | `critique` | `manual_capture` | 0 | 5 | 5 | 5 | 5 | 3/3 | - | plain negation should become positive replacement; lighting intent unclear |
| `flux_structured_brand_color` | `flux` | `standard` | `manual_capture` | 0 | 5 | 5 | 5 | 5 | 4/4 | - | brand color lacks hex code; product material and lighting underspecified |
| `dreamina_bilingual_cultural_scene` | `dreamina` | `standard` | `manual_capture` | 5 | 10 | 5 | 10 | 5 | 4/4 | - | too little concrete cultural detail; generic quality filler |
| `grok_reference_image_generation` | `grok` | `standard` | `manual_capture` | 0 | 10 | 10 | 10 | 10 | 4/4 | - | reference role unclear; missing model settings outside prose |
| `series_identity_drift` | `gpt-image` | `series` | `manual_capture` | 0 | 6 | 6 | 7 | 7 | 4/4 | - | identity lock missing; variation budget missing; shot slots missing |
| `product_photo_constraints` | `flux` | `model-port` | `manual_capture` | 0 | 6 | 6 | 7 | 7 | 3/3 | - | negative language needs positive replacement; material and geometry constraints underspecified |
| `prompt_compression_gpt_image_long_seven_layer` | `gpt-image` | `prompt-compression` | `manual_capture` | 7 | 9 | 2 | 9 | 2 | 3/3 | - | long seven-layer draft should become final render prompt; needs priority stack |
| `dirty_render_style_overload` | `gpt-image` | `critique` | `manual_capture` | 0 | 10 | 10 | 10 | 10 | 3/3 | - | style overload; dirty render risk |
| `reference_image_role_plan_product_geometry` | `gpt-image` | `reference-role-plan` | `manual_capture` | 0 | 9 | 9 | 9 | 9 | 3/3 | - | reference roles unclear; product geometry may drift |
| `revision_from_failure_texture_noise` | `gpt-image` | `revision` | `manual_capture` | 0 | 10 | 10 | 10 | 10 | 3/3 | - | texture noise overload; low subject readability |
| `revision_from_failure_text_error` | `gpt-image` | `revision` | `manual_capture` | 0 | 1 | 1 | 1 | 1 | 3/3 | - | text error; random text |
| `model_port_midjourney_to_gpt_image` | `gpt-image` | `model-port` | `manual_capture` | 0 | 9 | 9 | 9 | 9 | 3/3 | - | Midjourney parameters must be removed; avoid language should become natural |
| `standard_build_should_not_over_explain` | `gpt-image` | `standard` | `manual_capture` | 1 | 6 | 5 | 6 | 5 | 3/3 | - | user wants prompt only; avoid explanatory headings in final prompt |
| `stable_diffusion_wrapper_boundary` | `stable-diffusion` | `model-port` | `manual_capture` | 0 | 2 | 2 | 2 | 2 | 3/3 | - | wrapper not named; local syntax boundary unclear |
