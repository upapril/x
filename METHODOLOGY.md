# METHODOLOGY — day3 package

**26 Nov 2026, Asia/Shanghai (GMT+8).** Explicitly partial five-account public-post archive. This file describes how the corpus was collected, checked and packaged. It is not a completeness proof and not investment advice.

## Scope and identity

Handles only: `silverfang88`, `iiiinvest`, `alexandr_wang`, `taresky`, `thankUcrypto`. Public collection is authorized. No private legal-name inference. @alexandr_wang is treated as an operator, not a presumed trader. Significant Meta facts are limited to literal sourced wording already captured in `public_sources_wang.md` plus stored X text; no Meta/Scale/Reuters page was fetched or re-fetched on day3. Do not conflate Meta leadership HTML with packaging-note wording.

## Collection recipe (unchanged)

Public shared X MCP tool `search_posts_all` only. Query `from:<handle>`. `sort_order=recency`. `max_results=25`. Fields: `created_at,public_metrics,note_post,entities,attachments,lang,conversation_id`. Expansions: `author_id,referenced_posts,in_reply_to_user_id`. Always `write_to_file: true`, then disk ingest with `python3 _tools/checkpoint_batch.py`. Rate limits: 30 reads/minute, 1,000/day. A 75-read daily reserve is a hard stop: collection ends when remaining would drop to 75 or below (landing at 75 / usable 0 is the intended stop).

JSONL is split on the literal newline byte, not `str.splitlines()`. Canonical records use `created_at_utc` / `created_at_shanghai` (not an empty `created_at`). Author IDs checked on every top-level post: Wang `615818451`, III `1589763597705437184`, SF `1435990322702520320`, taresky `368245720`, thankUcrypto `705564530936418304`.

Terminal status is derived from ingest: empty `result_count` 0 with no `next_token`. Short nonempty pages that still return a `next_token` are followed, including 1–24 result pages. 255/256-byte responses with `result_count` 0 and no `next_token` are true terminals. Unusual small sizes and 6.6KB/9-line Full-text pointer pages are ingested (pointers are followed), not assumed terminal.

Never reuse stalled or exhausted parent tokens: SF 2023-09, SF 2026-07 parent, III 2026-08 parents. Never open SF 2026-11. Wang 2012–2014 remains not_proven_exhausted; do not blindly reuse a lost historical empty-page input token. Defer overlapping taresky / thankUcrypto timeline-recent cursors rather than rewalking finished months.

`_tools/checkpoint_batch.py` uses `BASE_CALLS_BEFORE_DATA_CHUNK = 1816`. Day3 `calls_this_pass` at reserve close is 2,741 (= 1,816 + 925 ingested day3 calls). Packaged unique baseline from day2 is 34,913; day1 close was 15,370.

## Day3 stop

Collection stopped at the **true 75-read reserve** on **26 Nov 2026 09:31:16 GMT+8 Asia/Shanghai**. Authoritative footer:

`X reads left for this user: 29 of 30 this minute (resets at 2026-11-26T01:32:00.000Z), 75 of 1000 today (resets at 2026-11-27T00:00:00.000Z).`

Daily remaining 75; usable 0; reset **2026-11-27 08:00 Asia/Shanghai** (2026-11-27T00:00:00.000Z). This packaging pass collected **no new X posts** and did not call X search/timeline tools. No pending fetched pages were left uningested at reserve close.

## Counts

53,706 unique posts: SF 19,848; III 4,850; Wang 3,625; taresky 17,532; thankUcrypto 7,851. +18,793 versus day2 34,913; +38,336 versus day1 15,370.

UTC year indexes are in each account `coverage_manifest.md` and `archives/<year>.md`. Notable day3 fill-ins: SF 2024/2025/2026; taresky 2023 and 2024; Wang 2024–2026 (2026-09 still open); thankUcrypto 2023; iiiinvest 2025.

## Validation

- Fast ID / author-attribution / day2-ID-retention checks passed at reserve close and were re-run in the full audit.
- Full raw-text / provenance audit: every post’s `collection.page_file` resolves; raw page contains the post id; stored `full_text` or `text` matches a raw candidate text field. JSONL SHA256 recorded. Control characters other than TAB/LF/CR are rejected. U+2028 on SF `2110119596435054716` is retained. Three pinned-post `collection.page_file` values remain `../_raw/pinned_posts_get_posts_by_ids.json`.
- After rebuild: `posts_lite.jsonl` is equivalent on id / timestamps / display text; year archives contain headings and literal post text; citation ledger excerpts exist in the store.
- Prior immutable ZIP SHA256 values were rehashed and left unchanged (see `logs/day3_package_validation.json` and the package artifacts JSON).

Day2 validation files (`logs/day2_validation_checkpoint.json`, `logs/day2_package_validation.json`, `logs/day2_citation_ledger.json`, `logs/remaining_jobs_day2.json`, `logs/DAY2_FINAL_REMAINING_JOBS.json`) were not overwritten.

Rebuild used `_tools/rebuild_day3_artifacts.py` (literal newline split; dynamic backtick fences). Day2 rebuild/package/analysis scripts were not run as-is.

## Remaining work after the 27 Nov 2026 08:00 Asia/Shanghai reset

Recorded in `logs/remaining_jobs_day3.json` and `collection_summary.json`; not walked in this pass:

1. Open dated: Wang 2026-09 p23 +536, next_token `b26v89c19zqg8o3juezidpc17rh8q611r4x6m7qlzhd31`, window 2026-09-01T00:00:00Z–2026-10-01T00:00:00Z, still open after a 25-result Full-text pointer page.
2. Unstarted incremental: 2026-11-25T00:35:00Z–2026-11-25T23:59:00Z. Prior increment through 2026-11-25T00:35:00Z stays terminal for all five.
3. Deferred: taresky and thankUcrypto timeline-recent cursors.
4. Blocked: SF 2026-11. Stalled/unproven: SF 2023-09, SF 2026-07 parent, III 2026-08 parents, Wang 2012–2014 not_proven_exhausted.
5. Job-count summary: 1 open dated; 2 deferred timeline-recent; 0 actionable pending; 1 blocked SF 2026-11; 360 exhausted; 3 pagination_stalled; 210 no-job calendar windows; 17 excluded pre-creation Wang placeholders.

Next collection log after reset: `logs/day3_batch111.txt` (do not create via collection now).

## Packaging

NEW artifact stem `/workspace/x-research-day3-final`. If split, independently extractable numbered ZIPs are each below 25,000,000 bytes. Extract all parts to the same destination. Every ZIP is CRC-tested and every packaged file is SHA256-compared to disk. Exclude `*.bak*`, `__pycache__`, `.pyc`. Prior ZIPs remain outside this tree and are not modified. File hashes: `FILE_SHA256SUMS.json`. Manifest: `PACKAGE_README.md`. Validation: `logs/day3_package_validation.json`. Citation ledger: `logs/day3_citation_ledger.json`.

## Integration boundary

No GitHub writes from this work. PR1 and PR2 are already merged into main (PR2 merge `e21cbe0c18d98b2d2fe460a838ed643833e086ef`). Later parent opens a **NEW PR from current main**. No merge authorization is granted here. Upstream finance skills were not executed.
