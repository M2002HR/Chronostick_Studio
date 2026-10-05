# Episode 006 — latest-candidate review and incremental repair queue

Updated: 2026-10-03T19:36:03.368880+00:00

All **131 initial latest candidates** were frozen by path and SHA-256 before review: 103 r004 and 28 r005. Reference comparisons and sampled motion frames cover all slots. This is not an all-frame motion/audio approval. See [the review ledger](../renders/review-evidence-r006/review-ledger.json) and [the frozen baseline](../renders/review-evidence-r006/baseline.json).

**76 distinct slots / 81 immutable generation requests** are persisted in the production service. Requests are enqueued as review proceeds; the shared GPU processes them sequentially. All requests passed service dry-run, preserve approved reference hashes, use 12 steps without Lightning, and retain 1024×576 at 24fps. Automatic assembly/upscale is disabled.

Live progress: [status.json](../automation/retries/review-r006/status.json). The detached evidence monitor checks all review revisions every 30 seconds and prepares contact sheets for completed replacements. It never approves outputs. Closing the conversation does not cancel submitted jobs.

## Replacement review

| Clip | Reviewed revision | Result |
| --- | --- | --- |
| 002 | r006 | Warm reference floor, light and fabric palette changed to cold flat blue. Status: failed_r007_queued. |
| 004 | r006 | Added foreground haze obscures intact palace; reference geometry changes. Status: failed_r007_queued. |
| 006 | r006 | Empty throne and identity restored; early cut and continuing pan need full-motion decision. Status: visual_improved_motion_and_audio_pending. |
| 007 | r006 | Additional moving bow overlay violates fixed five-ship inventory. Status: failed_r007_queued. |
| 009 | r006 | Khalid, scroll, clothing and guard preserved; cut occurs about 2.08s rather than 2.30s. Status: sampled_visual_pass_audio_pending. |
| 010 | r006 | Invented large person beside bow chain enters water and disappears; replace risky bow closeup with modest wide crop. Status: failed_r007_queued. |
| 012 | r006 | Officer changes from screen right to screen left; invented close vessel and altered flag. Preserve original layout and distant fleet. Status: failed_r007_queued. |

## Exact text

All 120 editorial frames of 008, 060, 075, 090, 124 and 125 were inspected in dense placard panels. 008/075/090/125 preserve the exact listed text; 060/124 require replacements for clipping/framing. 059 fails costume identity and 082 obscures its clock with smoke. Every replacement of a text-event slot requires another all-frame text review. Existing controlled maps014/118 retain their previously recorded 120-frame reviews and verified silent PCM.

## Audio evidence

Native full-video model observations were contaminated by narration supplied as context; those audio claims must not be used as review truth. Independent audio-only observations exist for all 131 baseline files. Their flags are not automatic failures: the provider described a faint squeak for a digitally silent control, and its initial speech claim for003 was contradicted by a second check. Clip119 produced consistent unwanted instrument and intelligible male speech in two context-free checks and has a silent-timeline replacement queued. Other suspect audio remains pending independent confirmation; upstream 5xx/403 interrupted further checks.

## Immutable requests

| Clip | Revision | Reviewed defect / repair |
| --- | --- | --- |
| 002 | r006 | At 2.25–4.96s the loose shoe is stacked above the worn shoe while a second foot is already shod; intended bare foot/held empty shoe relation is lost. |
| 004 | r006 | Whole clip performs continuous camera drift instead of the planned two locked shots; transient unmotivated pale haze and drifting dhow change the peaceful fixed harbour state; camera never resolves. |
| 006 | r006 | From frame 0 the empty-throne scene contains five invented foreground council figures; zero-person contract fails throughout. |
| 007 | r006 | At 1.50s the fleet view cuts to an unsupported occupied deck with numerous invented figures including giant heads; nearest-bow crop was not followed. |
| 009 | r006 | Close-up at 2.25s changes the secondary clean-shaven guard to a second black-bearded identity, partially averaging Khalid identity into the guard. |
| 010 | r006 | Frame0 invents an occupied foreground bow instead of five distant vessels, then drifts continuously; crew scale not controlled by anchor. |
| 012 | r006 | Frame0 shows darkened battle sky, smoke and fiery descending objects; by2.5s explosions destroy intact shore before the battle chronology. Negative future-event wording activated the forbidden event. |
| 013 | r006 | Continuous zoom replaces hard cut and keeps moving through final frame; planned locked harbour is unresolved. |
| 015 | r006 | At1.50s a second disconnected sail/bow-shaped triangle emerges beside existing moored dhow and persists, corrupting single rigid vessel geometry. |
| 016 | r006 | Continuous zoom drifts through all five seconds, removes worker and ends without resolved camera hold; no planned hard cut. |
| 017 | r006 | At1.00s the desk has three dispatches and a disconnected extra arm; required exactly two sealed dispatches fails. |
| 019 | r006 | Frame0 contains six invented council figures; later an unattached hand touches throne; empty unoccupied-room contract fails throughout. |
| 021 | r006 | At1.00s the prebattle quiet cannon fires a prolonged flame and smoke plume despite planned hand-rest action; chronology fails. |
| 022 | r006 | Second shot invents a ship full of foreground people with giant heads, violating nearest-bow-only reference coverage. |
| 023 | r006 | Close-up invents a gigantic green fruit that changes shape and scale and occupies the entire basket, instead of holding original small fruit. |
| 024 | r006 | Close-up changes hands to dark realistic glove silhouettes and starts lifting/pulling rope during final hold, violating fixed crate/rope state. |
| 025 | r006 | Frame0 introduces an approaching giant crew-filled hull, with numerous invented foreground people; intended fixed distant fleet is lost. |
| 026 | r006 | At1.75–4.96s a new close view invents rope handling and continues moving through the final hold, rather than head turn and settled crate/rope. |
| 027 | r006 | At2.00s the second shot swaps navy shopper and woman, invents shared oversized basket and extra fruit-transfer action during the intended pause. |
| 028 | r006 | At0.50s navy sleeve changes to purple, then continuous zoom drifts through final frame with no settled hold. |
| 030 | r006 | At1.50–2.00s officials overlap/morph into one hybrid body while desk geometry and dispatch positions change; later continuous drift persists. |
| 031 | r006 | At2.375s extreme chest crop cuts the cream scroll almost completely out of frame; held-message action becomes unreadable. |
| 032 | r006 | Continuous zoom invents close deck coverage and foreground residents, displacing initial fleet view and drifting to final frame. |
| 033 | r006 | Initial shot replaces full panorama with unsupported enlarged deck and crew; continuous drift replaces planned cut and final hold. |
| 034 | r006 | Frame0 introduces a large invented crowd that crosses the empty-throne room, violating zero-person contract. |
| 035 | r006 | Frame0 contains an invented crowd and at1.75s a new smiling teal-clothed figure sits on throne; succession chronology fails. |
| 036 | r006 | At1.00s closed scroll unrolls; at2.75s extreme view slides protagonist off screen, losing planned grip/action and resolved end. |
| 037 | r006 | Continuous zoom toward right-facing face replaces declared turn toward throne and drifts through final frame. |
| 043 | r006 | Atframe0 two invented people occupy throne view; later another figure and giant blank board enter scene, violating zero-person contract. |
| 044 | r006 | Atframe0 numerous invented figures are gathered beside throne, including a fallen/sitting figure; intended death conveyed by empty seat becomes an invented ceremony. |
| 045 | r006 | Frame0 changes standing identity comparison to crouching at throne, then invents an extra maroon-sleeved arm pulling sash from another person; fixed single-person sash/pose fails. |
| 047 | r006 | Frame0 giant cream cloth covers almost entire composition; second shot cuts face off and adds wrapping cloth, destroying clean fixed identity comparison. |
| 051 | r006 | Camera drifts and removes messenger through ending. |
| 053 | r006 | 3.25–4.25s turban becomes a long ribbon across face. |
| 055 | r006 | 4.0s premature flame across harbour. |
| 058 | r006 | Duplicate Rawson from frame zero; invented haze and paper marks. |
| 059 | r006 | Khalid robe is teal green instead of maroon. |
| 060 | r006 | Continuous camera drift changes mandatory placard placement; clock progressively leaves frame. |
| 062 | r006 | From 1.0s invented foreground crew and new huge occupied bow. |
| 063 | r006 | 2.75s adds giant foreground gunners and cannon not present in reference. |
| 067 | r006 | Dhow crosses harbour and grows continuously through final frame. |
| 068 | r006 | 2.0s duplicate giant foreground Khalid persists to end. |
| 069 | r006 | 2.75s extreme crop invents realistic fingered hands and cuts away head. |
| 070 | r006 | 1.25s premature muzzle flashes and shore blast; giant crew and invented deck close-up at 2.75s. |
| 072 | r006 | 1.25s scroll unfurls horizontally across face; turban and face cut away. |
| 073 | r006 | 4.0–4.35s premature firing while this is a waiting beat. |
| 076 | r006 | 1.5s onward large premature harbour explosions and smoke. |
| 077 | r006 | 1.5s cut invents three foreground crew holding a maroon banner. |
| 078 | r006 | 2.75s onward two British ships burn during prebattle observation. |
| 079 | r006 | 2.0s invents new opposite viewpoint, large crowd, seated messenger and open paper. |
| 080 | r006 | Frame zero omits Khalid, then he walks in; blank placard turns black. |
| 081 | r006 | Continuous drift and dhow motion through final frame; no resolved hold. |
| 082 | r006 | 0.00–3.0s smoke covers entire scene and mandatory 09:00 text. |
| 084 | r006 | 2.375s duplicate foreground pair appears while original pair remains behind. |
| 088 | r006 | 0.25–1.5s invented glowing projectile travels out of palace toward water; close-up open mouths. |
| 093 | r006 | Frame zero invents a large crowd standing in water; dozens appear to sink through whole clip. |
| 094 | r006 | Frame zero onward invented large crowd obscures wreck; bodies morph and new people arrive. |
| 095 | r006 | 0.5s adds third giant foreground defender with backpack while original pair stays behind. |
| 096 | r006 | Entire clip invents many civilians standing in water in front of wreck. |
| 097 | r006 | 1.0s new explosive projectile and damage; invented large blue backpack in close-up. |
| 100 | r006 | 4.0s close-up changes into a white blurred vignette instead of full-frame drawn scene. |
| 103 | r006 | 3.5s closed scroll disappears from Khalid’s hand. |
| 105 | r006 | Frame zero invents huge foreground flag bearer, hiding damaged masonry; reference contains no flag bearer. |
| 107 | r006 | Invented hand touches temple; turban develops long loose ribbon across shoulder; continuous ending drift. |
| 108 | r006 | Ending zoom continues into oversized faces with right head cut off. |
| 110 | r006 | Frame zero adds two unsupported foreground women while original two remain. |
| 113 | r006 | 1.5s onward giant tsunami wave rises behind residents and overtops quay. |
| 114 | r006 | Invented giant anchor and third woman standing waist-deep in water. |
| 115 | r006 | Frame zero adds crowd; smoke floods empty clock room. |
| 117 | r006 | 2.75s changes cream robe into entirely green costume; head and turban cut off. |
| 119 | r006 | Independent audio-only observations and a second context-free check both identify a plucked instrumental melody and intelligible unwanted male speech; use an explicit silent audio timeline. |
| 123 | r006 | Held shoe disappears at 0.5s; foot remains barefoot until replacement shoe pops on at 1.5s. |
| 124 | r006 | Continuous camera drift changes mandatory placard placement; clock progressively leaves frame. |
| 126 | r006 | 0.75s onward third dispatch appears beside right official; final crop shows three. |
| 130 | r006 | Reviewed latest baseline: fully shod searcher lifts an invented loose third shoe; preserve two worn shoes and empty hands. |
| 131 | r006 | Starts outside then walks in; 3.25s loose shoes fly in and land in hand despite fully shod still ending. |
| 002 | r007 | Reviewed latest r006: warm floor/lighting become flat blue; restore literal anchor palette and shoe inventory. |
| 004 | r007 | Reviewed latest r006: foreground haze obscures the intact palace and geometry changes; retain clean fixed anchor geometry. |
| 007 | r007 | Reviewed latest r006: overlay introduces another moving hull; retain five fixed separated ships in both compositions. |
| 010 | r007 | Latest r006 adds a giant person at the bow chain and lowers him into the sea; replace risky waterline closeup with a fixed wide crop of the same five ships. |
| 012 | r007 | Latest r006 reverses the officer from screen right to screen left and invents a large nearby vessel with an altered flag; keep original officer position and distant fleet in a modest centered crop. |

## Remaining work

Review each newly generated latest revision against its approved anchor and shot contract, including motion and native audio; add only necessary immutable repairs. Recheck all listed exact-text frames. Resolve pending audio evidence before approval. Select one actually approved artifact per slot before assembly.

For045/047/093, r006 requests are seed retries of their frozen original prompts, recorded as `retry`; later active prompt refinements are not present in those submitted requests. The active093 refinement was corrected to describe an empty deck; any further repair must freeze a new request. Slot024 reference mitten colour needs explicit comparison when r006 arrives.
