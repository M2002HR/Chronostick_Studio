# Episode 005 corrective generation direction — r003 and r004

The user reviewed the first two complete 11-clip rounds and requested two new complete rounds. The failure report has three parts: generated music in most candidates, pistols sometimes pointing up rather than toward the opposing duelist, and opponents standing too close, especially in duels without a final handshake. This direction supersedes the affected details of the original shot plan for r003 and r004. The original prompts, references, renders, and approvals remain historical records.

## Revised visual contract

- Four newly reviewed, immutable wide duel anchors are used: S01, S04, S06, and S09 `r002`. Their subjects stand at opposing frame edges with a clear central corridor and level pistols pointed toward each other.
- In every duel wide shot, preserve at least 45 percent clear frame width between the duelists' front bodies. Neither person crosses sides or approaches while weapons are raised.
- When a weapon is raised, its barrel is horizontal and aimed directly at the opposing person's central chest. This holds through the Jackson, French-officer, and Uruguay trigger pulls. No skyward or outward aiming.
- In the deliberate-miss/reconciliation sequence of Clip 03, begin with both barrels directly opposed. Each makes only a small horizontal adjustment toward empty dirt beside the opponent at the last moment, then fires. The men approach only after both weapons lower. This preserves the narrated intentional misses without a skyward pose.
- In the French sequence, change Clip 07 Shot 5 from outward firing to directly opposed horizontal firing. The men never approach or reconcile; the ownerless gear remains the visual outcome.
- In the Uruguay sequence, Clip 09 ends with the politicians at distant opposing marks and pistols aimed directly at each other. Clip 10 raises and fires both level pistols in that same direction. The story's survival outcome remains non-graphic. Clip 11 begins at that wide spacing, places both weapons down, then compresses the walk to the handshake through hard cuts.

## Revised audio contract

Every r003/r004 prompt and every job's `audio.prompt_suffix` specifies only short, dry, literal Foley tied to visible actions. Each cue is at most 0.35 seconds; silence separates cues. Continuous ambience, tonal beds, music of any kind, speech, and vocalization are forbidden. If the model cannot produce a short literal effect, silence is preferred. The exact required no-music policy sentence appears once in each prompt file. `audio.music` is false in every job.

## Reference review

| Scene | Selected retry path | SHA-256 | Review decision |
| --- | --- | --- | --- |
| S01 | `assets/episodes/005-why-risk-a-duel/references/s01-dawn-duel-field-r002.png` | `fa85b445a55f0f5db40588d4b1848ea1f3cebf3a3d191442cf62436022a22370` | Assistant-reviewed: complete separated figures and horizontal opposing aim. |
| S04 | `assets/episodes/005-why-risk-a-duel/references/s04-jackson-duel-field-r002.png` | `90258760520eec7c51b9534054729283e09e1e0c5d426421335467962361b99a` | Assistant-reviewed: Jackson and opponent at opposite edges, horizontal opposing aim. |
| S06 | `assets/episodes/005-why-risk-a-duel/references/s06-french-officer-duel-courtyard-r002.png` | `079f2c5b91c7147ccb05df6d8f2ea01b76bc700171ae44cfc60ca175698b62ad` | Assistant-reviewed: two separated officers, horizontal opposing aim, ownerless gear. |
| S09 | `assets/episodes/005-why-risk-a-duel/references/s09-uruguay-political-duel-r002.png` | `4d9788285ea707e457643dbb70c23698147f17b77f62de94cfda20740eb43059` | Assistant-reviewed: distant politicians, opposing horizontal pistols, two witnesses, tripod. |

The four images were visually inspected at their displayed full vertical compositions during this continuation. This review approves their use as retry anchors; it does not approve generated video.
