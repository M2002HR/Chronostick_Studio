# Episode006: reference/prompt/output input audit

This targeted audit corrects causal interpretation of the frozen12→20step experiment. It is not a new generation or final clip approval. Inspecting an input contradiction proves that contradiction; it does not prove how much of a render failure it caused.

## Findings

| Clip | Diagnosis | Evidence |
| --- | --- | --- |
|010|confirmed_reference_prompt_conflict|Reference visibly includes deck crew and a large foreground vessel; prompt requires exactly five distant ships with zero visible crew. The unsupported person sinking in foreground water is still a real output deviation.|
|019|prompt_conditioning_ambiguity|Reference is genuinely an empty throne room. Prompt simultaneously requires no people and describes heads, eyes, limbs, hands and period clothing. Added crowd is absent from reference; contribution of the human vocabulary requires an ablation to prove.|
|035|prompt_conditioning_ambiguity|Empty-room reference is adequate for the inventory. Generic human anatomy/costume vocabulary is unnecessary conditioning. Added crowd is a real output deviation, with an avoidable prompt ambiguity.|
|095|confirmed_reference_prompt_conflict_and_review_correction|Full-resolution reference shows two bent-forward retreating defenders with lifted/stepping legs, not an unambiguous stationary crouch. Prompt itself calls them retreating and also requires original crouching poses. Withdraw the earlier reference-mismatch diagnosis based solely on standing/running pose. Motion, transition and inventory still require their own checks; this is not approval.|
|097|confirmed_reference_prompt_conflict_and_review_correction|Full-resolution reference likewise shows two retreating bent-forward defenders. Prompt describes retreating defenders and original crouching poses simultaneously. Earlier crouch-based failure attribution is disputed. Existing battle flashes also make a residual-smoke-only interpretation ambiguous; not final approval.|
|110|confirmed_reference_prompt_scale_conflict|Reference has two foreground civilians of substantial visible size; prompt calls those original people small and distant while retaining the original composition. Output nevertheless adds separate foreground civilians absent from the reference, a real count deviation.|
|017|clear_output_deviation_with_adequate_inventory_reference|Reference clearly contains two closed sealed cream rolls and two officers. Output opening/adding rolls departs from that concrete inventory. This does not establish whether model dynamics or prompt wording causes the deviation.|
|126|clear_output_deviation_with_adequate_inventory_reference|Reference shows two closed rolls; 20-step output close shot contains roughly four. The requested count is consistent with the source image. Close-shot adherence remains a generation/control problem, not a reference count defect.|
|073|clear_output_deviation_with_adequate_inventory_reference|Reference shows two foreground sailors, matching the prompt. A third foreground gunner is a genuine addition.|
|094|clear_output_deviation_with_adequate_state_reference|Reference is blue-sky daylight and prompt requests a fixed anchor view with only one ripple. Both outputs turn orange/dusk. Source image does not require that change.|
|105|clear_output_deviation_and_framing_control_gap|Reference is full landscape without black side panels. Both outputs introduce pillarboxing, a real composition deviation. Tight lower-wall opening and reveal are specified in words but no explicit start-crop frame is supplied; missing framing control is a plausible contributor, not proved cause.|
|012|unsupported_framing_or_viewpoint_inference|Reference covers the original over-shoulder view. Requested closer framing is described without a separate crop anchor. Opposite-side view and new close ship exceed a literal crop of the source. Reference is useful for the original view; it does not validate an invented reverse angle.|
|058|clear_output_deviation_and_framing_control_gap|Reference uses simple mitten hands and the original over-shoulder composition. Detailed fingered hands and an initial unsupported close composition are real deviations. Prompt-only literal-first-frame wording does not constitute an actual supplied I2V first-frame control.|
|093|clear_output_deviation_and_prompt_conditioning_ambiguity|Reference has no foreground crowd in water. Output invents one. Prompt nevertheless contains human anatomy styling and repeated crew/drowning/falling-people concepts in prohibitions. Their causal role is plausible but untested.|

## Correction to previous review

095 and097 must be removed from the undifferentiated model/reference-failure category pending reassessment. The previous crouch-only judgement misread the reference poses. Their 20step close frames retain the same two retreating identities and therefore are not proof of ignoring a crouched source image. Other motion/cut contracts remain independently reviewable. No clip is approved by this correction.

The revised accounting is6 original recorded major defects removed,8 partial improvements,24 no material repairs/regressions, and2 disputed input/criterion cases. Generation duration measurements and the same-prompt/seed controls are unchanged. Neither this count nor the earlier count estimates a clean-input first-pass success rate.

## Production implication

Fix incompatible inventories, poses and scale instructions before testing more steps. Keep references that already represent the intended scene; crop or replace references only when their visible contents cannot meet the intended shot. Remove irrelevant human descriptions from empty architectural/ship shots. Supply an explicit crop or a tested actual first-frame control for strict opening geometry. Then compare the same corrected inputs at fixed seed/settings to isolate step count. A separate fixed-step, fixed-seed input ablation is required to estimate prompt versus reference contribution.
