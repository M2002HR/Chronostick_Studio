# Episode 004 three-seed generation queue

The 2026-09-29 02:00 cron entry was removed when the operator changed the instruction to immediate chaining. The persistent user service `chronostick-episode-004-three-seed-queue.service` waits for r002 to finish and then runs three full 13-clip batches sequentially: r003, r004, r005. All three retain the common r003 episode direction and 39 distinct fixed seeds. After r003 Clip 01 visibly turned seven islands into people, variants r004 and r005 received a revised single-scene seven-tile reference and prompt for Clip 01 before submission. They also use an anchored-overlook prompt for Clip 02 after r003 produced near-photographic sea, and a simplified two-shot CTA prompt for Clip 13 because r002 placed the button late. The other 10 clips use identical prompt text and references across all three seed variants. The media/job revisions remain distinct. Each job samples with 14 steps and creates immutable 5-second raw and editorial media. No automatic selection, assembly or approval occurs.

Live queue state: `automation/retries/r003/queue-state.json`. Batch IDs for each submitted variant are recorded there and in `automation/retries/<revision>/batch-id.txt`.

To monitor:

```bash
systemctl --user status chronostick-episode-004-three-seed-queue.service
cat episodes/004-smallest-empire-in-history/automation/retries/r003/queue-state.json
tail -n 30 episodes/004-smallest-empire-in-history/automation/retries/r003/queue.log
```

For the active revision, run from `/home/mhr/AI/comfy-video-automation`:

```bash
uv run comfy-video status --service-url http://127.0.0.1:8091 --batch <batch_id> --watch
```

Do not resubmit a revision whose `submitted.marker` exists without first checking its persisted batch ID and service state. The queue was preflighted with repository validation and all three 13-job dry-runs. Generation success only means files were rendered; inspect frames and listen to audio before selecting a final cut. In particular, r002 Clip 05 had user-reported background music and the r002 CTA appeared late.
