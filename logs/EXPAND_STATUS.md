# Expand + packaging status

**Written:** 2026-11-24 19:44:01 GMT+8 (Asia/Shanghai, GMT+8).

## Stopping reason

Collection was **paused**, not completed. The user follow-up asked for operating/decision frameworks and useful trader insight, and the parent instruction was: if budget/time is tight, prioritize rigorous insight and packaging over endless crawl. Daily X-read budget was **not** exhausted. A later pass can resume from `logs/RESUME_OPEN_JOBS.json` and `logs/expand_jobs.json`.

Do **not** claim all tweets were retrieved. Profile `post_count` is not a missing-count proof.

## Unique posts stored (deduped by id)

| Handle | Stored | Span (Asia/Shanghai, GMT+8) | original / reply / quote / repost |
|---|---:|---|---|
| @alexandr_wang | 788 | 2012-06-23 10:48:05 GMT+8 → 2026-11-23 12:21:30 GMT+8 | 259 / 296 / 118 / 115 |
| @iiiinvest | 736 | 2022-11-22 16:48:28 GMT+8 → 2026-11-24 17:50:06 GMT+8 | 172 / 480 / 48 / 36 |
| @silverfang88 | 6576 | 2021-09-13 14:35:07 GMT+8 → 2026-11-24 17:58:30 GMT+8 | 2692 / 2685 / 598 / 601 |

Year breakdowns and open tokens are in each account's `coverage_manifest.md` / `.json`.

## Budget

- Expand-pass calls recorded in `expand_jobs.json`: 403
- Daily remaining at the expand probe (early in the pass): 941 of 1000
- Daily reset: `2026-11-25T00:00:00.000Z` = **2026-11-25 08:00:00 GMT+8** (Asia/Shanghai)
- Intended reserve: 75 reads
- Exact remaining at packaging time was **not** re-probed; use the next live tool footer.

## Immutable first-pass zip

`/workspace/x-research-firstpass.zip` SHA256 `455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976` — do not modify.
