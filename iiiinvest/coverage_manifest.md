# Coverage manifest — @iiiinvest

**Packaged:** 2026-11-24 19:44:01 GMT+8 (Asia/Shanghai, GMT+8).

This account folder is **not** a complete public history. Profile `post_count` is a platform lifetime figure, not proof that a remainder still exists or is retrievable.

## Stored corpus (deduplicated by string id)

- Unique posts stored: **736**
- Profile `post_count` at first lookup (24 Nov 2026): 4858
- Span (UTC): `2022-11-22T08:48:28.000Z` → `2026-11-24T09:50:06.000Z`
- Span (Asia/Shanghai, GMT+8): 2022-11-22 16:48:28 GMT+8 → 2026-11-24 17:50:06 GMT+8
- Types: original 172, reply 480, quote 48, repost 36
- Earliest stored: [1594976093844303872](https://x.com/iiiinvest/status/1594976093844303872)
- Latest stored: [2125165053078839443](https://x.com/iiiinvest/status/2125165053078839443)

### Posts by UTC year

| Year | Stored |
|---|---:|
| 2022 | 408 |
| 2023 | 37 |
| 2024 | 21 |
| 2025 | 69 |
| 2026 | 201 |

## Expand-pass window status

Status counts: `exhausted` 17, `open` 2, `pending` 30

Expand pass used fresh monthly `search_posts_all` windows (`from:<handle>`, `sort_order=recency`, `max_results=25`). Later pages store query, window bounds, input token, and output `next_token`. If an output token equals the input token on a duplicate page, the window is marked `pagination_stalled` and is not reused; the earlier remainder is opened as a subwindow.

### Open, stalled, or not-proven-exhausted windows (resumable)

| Label | Status | start_time | end_time | pages | added | next_token | last_input_token |
|---|---|---|---|---:|---:|---|---|
| 2024-03 | open | `2024-03-01T00:00:00Z` | `2024-04-01T00:00:00Z` | 1 | 0 | `b26v89c19zqg8o3fr5tf2y6kfl1s6lgrfqcyi0z6if98d` | `—` |
| 2024-04 | open | `2024-04-01T00:00:00Z` | `2024-05-01T00:00:00Z` | 1 | 0 | `b26v89c19zqg8o3fr5wef9q8hje9y7cyy9d1dap71fhq5` | `—` |

### Pending first pages (30 windows, not yet opened in the expand pass)

2024-06, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2024-12, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06, 2026-07, 2026-08, 2026-09, 2026-10, 2026-11

### Exhausted monthly (or sub) windows

2022-11, 2022-12, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11, 2023-12, 2024-01, 2024-02, 2024-05

## Coverage caveats

- 2022-11 was walked deeply (many pages) and is exhausted with stored later-page provenance. 2022-12 and 2023-01 through 2024-02 plus 2024-05 were exhausted; many of those later months added 0–few new posts because first-pass year-end samples already contained the only hits those first pages returned.
- 2024-03 and 2024-04 are open: first pages were first-pass duplicates (`posts_added=0`) but still returned a next_token.
- 2024-06 onward (including most of 2025–2026) remains pending. 2025–2026 posts in the store are mostly first-pass / recent-timeline samples, not monthly-exhausted coverage.

- First-pass year-end samples remain in the JSONL and can make unopened years look like they have ~25 posts clustered at the end of the year.
- Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.
- Collection was paused to prioritize analysis and packaging; the daily read budget was not exhausted.

Do **not** claim this folder contains all tweets.
