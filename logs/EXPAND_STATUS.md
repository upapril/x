# Expand + packaging status

**Written:** 2026-11-24 20:40:23 GMT+8 (Asia/Shanghai, GMT+8).

## Stopping reason

Day-1 collection was **stopped with remaining budget**, not completed. Authoritative footer after the last ingested X call: **61 of 1000 today**, reset `2026-11-25T00:00:00.000Z` = **2026-11-25 08:00:00 GMT+8**. Two accounts (@taresky, @thankUcrypto) were added late on day 1 and have only an initial public sample. Resume from `logs/remaining_jobs_day1.json`, `logs/RESUME_OPEN_JOBS.json`, and `logs/expand_jobs.json`. Do not reopen exhausted or stalled-parent windows.

Do **not** claim all tweets were retrieved. Profile `post_count` is not a missing-count proof.

## Unique posts stored (deduped by id)

| Handle | Stored | Span (Asia/Shanghai, GMT+8) | original / reply / quote / repost |
|---|---:|---|---|
| @alexandr_wang | 1873 | 2012-06-23 10:48:05 GMT+8 → 2026-11-23 12:21:30 GMT+8 | 719 / 640 / 231 / 283 |
| @iiiinvest | 3856 | 2022-11-22 16:48:28 GMT+8 → 2026-11-24 17:50:06 GMT+8 | 1272 / 2027 / 517 / 40 |
| @silverfang88 | 9239 | 2021-09-13 14:35:07 GMT+8 → 2026-11-24 17:58:30 GMT+8 | 4168 / 3561 / 874 / 636 |
| @taresky | 224 | 2016-12-15 08:47:22 GMT+8 → 2026-11-24 17:10:31 GMT+8 | 53 / 138 / 22 / 11 |
| @thankUcrypto | 178 | 2022-12-30 17:55:07 GMT+8 → 2026-11-24 19:05:18 GMT+8 | 82 / 74 / 21 / 1 |

Year breakdowns and open tokens are in each account's `coverage_manifest.md` / `.json`.

## Budget

- Expand-pass calls recorded in `expand_jobs.json`: 892
- Daily remaining at the expand probe (early in the pass): 941 of 1000
- Daily reset: `2026-11-25T00:00:00.000Z` = **2026-11-25 08:00:00 GMT+8** (Asia/Shanghai)
- Intended reserve: 75 reads
- Authoritative day-1 footer (last ingested X call): 23 of 30 this minute (resets at 2026-11-24T12:33:00.000Z), **61 of 1000 today** (resets at 2026-11-25T00:00:00.000Z).
- Remaining 61 was left above a ~40 floor for other tasks after 22 reads for the two new handles.

## Immutable prior zips (do not modify)

- `/workspace/x-research-firstpass.zip` SHA256 `455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976`
- `/workspace/x-research-expanded.zip` SHA256 `d601957063b3610067d2dafd6cab0a6effb63e771bd642df57233b5e44fee6c7`
- `/workspace/x-research-latest.zip` SHA256 `1ab3fc4aaee8667c42d833543a85f86f54ff9dabe165f6305d56769aed4d8e58` (8.75 MB, 9,435 posts, packaged 2026-11-24 20:01 GMT+8)

