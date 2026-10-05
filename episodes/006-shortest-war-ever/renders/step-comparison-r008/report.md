# Episode006: same-prompt, same-seed12→20step experiment

Reviewed: 2026-10-04T19:30:43.745240+00:00

All40generation jobs succeeded. Effective prompt text, actual seed, approved reference hashes, sampler/scheduler and all generation parameters other than step count were verified against the original r00612step sidecars. Test outputs are immutable r008. Settings remain res_multistep/beta, Lightning off,1024×576,24fps.

| Observed visual result | Clips | Share |
| --- | ---: | ---: |
| Original major defect removed; candidate still requires complete QC |6|15%|
| Partial improvement; remains failed |8|20%|
| No material repair or regression |24|60%|
| Input/criterion conflict; requires reassessment |2|5%|

Mean end-to-end service execution:12steps=411.5s;20steps=647.8s. Total execution4.572h versus7.198h: **57.4% more time**. Queue waiting is excluded. GPU/CPU/VRAM/energy details remain in the immutable run sidecars and [metrics report](metrics-and-controls.json).

**Limits:** This is a selected set of previously failed12step clips, not a random first-pass comparison.6/40is a rate of removing the originally recorded major visual defect, not a full approval rate or a global20step success estimate. Audio is not reviewed in this comparison. No final-selected clip or approved picture master is created.

All40pairs were inspected in side-by-side actual-frame/reference sheets at0/1/2/3/4/4.958seconds. All120frames of the six apparent major-defect removals were checked;082has a separate dense placard review with09:00stable/visible throughout.

## Individual results

| Clip |12step defect →20step observation | Result |
| --- | --- | --- |
|002|Blue palette and major limb rendering improve; new broad white vignette masks the scene, and shoe inventory still needs repair.|partial_improvement_still_failed|
|004|Opening fog is removed and intact palace is visible; second half changes to orange late-day light and altered scene geometry.|partial_improvement_still_failed|
|007|Approaching giant bow remains; fixed fleet/world positions are still violated.|no_material_repair_or_regression|
|010|Invented person remains at the bow and sinks in open water; unsupported small boat also appears.|no_material_repair_or_regression|
|012|Opening now resembles the anchor and officer/instrument are clearer; opposite-side second viewpoint and invented close ship remain.|partial_improvement_still_failed|
|013|Moored dhow still travels/grows and changes orientation in the second half.|no_material_repair_or_regression|
|015|The two invented foreground people disappear; only the original cream-clad worker remains. All120frames checked for the original count defect. Initial composition is still a close crop rather than literal full reference.|original_major_defect_removed|
|017|Transition is cleaner, but exactly two closed dispatches still become unfolded sheets and another roll.|no_material_repair_or_regression|
|019|Large invented group remains in the empty throne room.|no_material_repair_or_regression|
|022|Unlisted crowd remains in harbour foreground/open water.|no_material_repair_or_regression|
|025|Two invented foreground people remain in the zero-person fleet scene.|no_material_repair_or_regression|
|031|Giant unsupported hands/scrolls remain and the scroll opens.|no_material_repair_or_regression|
|032|Premature red flare disappears; invented close deck crew/view remains.|partial_improvement_still_failed|
|033|Unlisted chalk-like hull drawing disappears; hull stays unmarked in all120frames. Remaining shot/camera/audio approval is separate.|original_major_defect_removed|
|034|Unlisted crowd remains, with additional foreground heads compared with12steps.|no_material_repair_or_regression|
|035|Unlisted group remains beside the empty throne.|no_material_repair_or_regression|
|036|Khalid remains visible from the opening and keeps a closed roll; unsupported hand/open-scroll defect removed. All120frames checked. Cut occurs earlier than planned, so this is not final approval.|original_major_defect_removed|
|037|Extra guard and reference-world rearrangement remain.|no_material_repair_or_regression|
|045|Duplicate Hamoud remains while another Hamoud is still visible in the original throne scene.|no_material_repair_or_regression|
|047|Unlisted cloth wiping disappears; replaced by another unlisted action, sitting down on the throne.|partial_improvement_still_failed|
|058|Unsupported initial close crop and detailed fingered hands remain.|no_material_repair_or_regression|
|062|Initial two invented foreground people disappear; second half still invents a large close deck crowd.|partial_improvement_still_failed|
|063|Close crew and new gun still occupy the specified hull/funnel crop.|no_material_repair_or_regression|
|067|Invented foreground residents disappear; one original worker retained through all120frames. Motion/audio contract approval is separate.|original_major_defect_removed|
|070|Premature muzzle flash remains; new sail/deck crew view also appears.|no_material_repair_or_regression|
|072|Opening clears and haze is shorter/weaker, but an unlisted bright veil/dissolve still appears.|partial_improvement_still_failed|
|073|Extra navy gunner remains in the opening section.|no_material_repair_or_regression|
|077|Excluded deck view still appears with an even larger invented crowd.|no_material_repair_or_regression|
|078|Premature burning/exploding fleet persists and extends to more ships.|no_material_repair_or_regression|
|080|Khalid remains visible throughout instead of exiting/disappearing. All120frames inspected; framing/pose still changes and final approval is separate.|original_major_defect_removed|
|081|Palace/shore still dissolves into largely empty background in the second half.|no_material_repair_or_regression|
|082|Required09:00 placard remains fully visible and correct in all120frames; Khalid no longer covers it. Existing visible distant flame and complete sound contract still require review.|original_major_defect_removed|
|093|Invented crowd still stands and sinks in the water around the Glasgow.|no_material_repair_or_regression|
|094|Daylight still changes into orange sunset.|no_material_repair_or_regression|
|095|Correction: reference shows retreating bent-forward defenders; prompt also calls them crouching. Earlier crouch-based mismatch judgement is withdrawn pending contract reassessment.|input_conflict_reassessment_required|
|097|Correction: reference shows retreating defenders; crouching requirement conflicts with that source. Pose-based failure attribution requires reassessment.|input_conflict_reassessment_required|
|103|Opening characters are now visible and the main smoke obstruction is much weaker; unlisted haze/dissolve remains.|partial_improvement_still_failed|
|105|Large black side panels persist and appear even earlier.|no_material_repair_or_regression|
|110|Invented foreground civilians remain and more people are introduced.|no_material_repair_or_regression|
|126|Dispatches now stay rolled rather than open, but approximately four closed rolls replace the required two; prop count remains broken.|no_material_repair_or_regression|

## Subsequent input audit

[Actual reference/prompt audit](input-audit.md) establishes contradictory inputs in010,095,097 and110, unnecessary human conditioning in empty019/035, and genuine output deviations despite adequate reference inventories in017/073/126.095/097 are separated from the earlier26-case failure category; that earlier pose judgement misread the full references. No causal percentages or final approvals follow from this audit.

## Production recommendation

Do not raise every episode clip to20–30steps on the strength of this experiment.20steps can help selected reference/detail failures, but eight more steps left most semantic/count/time-of-day failures intact. Keep the present production default until a representative first-pass test establishes a better cost per fully acceptable clip.

A more useful first-pass experiment would compare16/20/25steps on a small balanced set of empty architecture, fixed fleet, closed dispatches, character/prop interaction, battle chronology and exact clock text.16and25are proposals, not tested outcomes here. Freeze the revised prompt, reference, seed, sampler and scheduler for each comparison. Measure complete pass rate and execution time; do not count sharper but incorrect outputs as passes.

First reduce conditioning ambiguity: empty-room prompts such as019/035 also describe heads, eyes, limbs, hands and period clothing. Those generic style descriptions conflict with their empty-world inventory. Replace them with architectural style direction specific to the actual scene. This is a plausible cause inferred from the repeated defect; no causal prompt-ablation experiment has yet been run.

Use scene-specific positive descriptions, concise physical actions, explicit reference retention and complete sound fields. Avoid mechanically repeating absent people, explosions, drowning or writing. For particularly strict scene inventories, test a genuinely anchored first-frame I2V path or timed frame guides rather than expecting a full-scene R2V reference to become a literal first frame solely through prose. The current automation template only exposes h3_ref2va; these control modes would require separate workflow support and testing.

Single continuous shots and action-specific references are a proposed route to better first-pass consistency, not a guarantee. Preserve approved editorial pace and use a planned edit when a new framing is necessary, instead of asking the generator to invent an unsupported viewpoint.

## External technical context

[ComfyUI step-count guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3#step-count) recommends20base steps for close reference adherence and25if drift persists; simple content may work at12–16and high-frequency detail can improve at higher counts. Our fixed beta-scheduler test does not establish the behavior of every documented workflow.

[ComfyUI prompt guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide) explains the single-conditioning BasicGuider and recommends writing bans positively and reference-retention roles explicitly. [Native I2V workflow](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native) provides actual first/last-frame inputs. These primary sources support proposed follow-up tests; the measured counts above come from our local media, not documentation.
