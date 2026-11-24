# Coverage manifest — @iiiinvest

**Packaged:** 2026-11-24 20:40:23 GMT+8 (Asia/Shanghai, GMT+8).

This account folder is **not** a complete public history. Profile `post_count` is a platform lifetime figure, not proof that a remainder still exists or is retrievable.

## Stored corpus (deduplicated by string id)

- Unique posts stored: **3856**
- Profile `post_count` at first lookup (24 Nov 2026): 4858
- Span (UTC): `2022-11-22T08:48:28.000Z` → `2026-11-24T09:50:06.000Z`
- Span (Asia/Shanghai, GMT+8): 2022-11-22 16:48:28 GMT+8 → 2026-11-24 17:50:06 GMT+8
- Types: original 1272, reply 2027, quote 517, repost 40
- Earliest stored: [1594976093844303872](https://x.com/iiiinvest/status/1594976093844303872)
- Latest stored: [2125165053078839443](https://x.com/iiiinvest/status/2125165053078839443)

### Posts by UTC year

| Year | Stored |
|---|---:|
| 2022 | 408 |
| 2023 | 37 |
| 2024 | 21 |
| 2025 | 69 |
| 2026 | 3321 |

## Expand-pass window status

Status counts: `exhausted` 30, `open` 5, `pagination_stalled` 1, `pending` 14

Expand pass used fresh monthly `search_posts_all` windows (`from:<handle>`, `sort_order=recency`, `max_results=25`). Later pages store query, window bounds, input token, and output `next_token`. If an output token equals the input token on a duplicate page, the window is marked `pagination_stalled` and is not reused; the earlier remainder is opened as a subwindow.

### Open, stalled, or not-proven-exhausted windows (resumable)

| Label | Status | start_time | end_time | pages | added | next_token | last_input_token |
|---|---|---|---|---:|---:|---|---|
| 2024-03 | open | `2024-03-01T00:00:00Z` | `2024-04-01T00:00:00Z` | 1 | 0 | `b26v89c19zqg8o3fr5tf2y6kfl1s6lgrfqcyi0z6if98d` | `—` |
| 2024-04 | open | `2024-04-01T00:00:00Z` | `2024-05-01T00:00:00Z` | 1 | 0 | `b26v89c19zqg8o3fr5wef9q8hje9y7cyy9d1dap71fhq5` | `—` |
| 2026-07 | open | `2026-07-01T00:00:00Z` | `2026-08-01T00:00:00Z` | 19 | 475 | `b26v89c19zqg8o3juetiu3pwrn98hk6kkpu00ab83qovx` | `b26v89c19zqg8o3juetiu7y62ole97sq17ogsvvxq8fwd` |
| 2026-08 | pagination_stalled | `2026-08-01T00:00:00Z` | `2026-09-01T00:00:00Z` | 4 | 75 | `b26v89c19zqg8o3juezgoudctnrq3quemi6wf56f1d5dp` | `b26v89c19zqg8o3juezgoudctnrq3quemi6wf56f1d5dp` |
| 2026-09 | open | `2026-09-01T00:00:00Z` | `2026-10-01T00:00:00Z` | 19 | 449 | `b26v89c19zqg8o3juzivs5t2k3bz55ue17d4hte5b44u5` | `b26v89c19zqg8o3juzivsa2ixs2t0itdp9o8ow7ixlrp9` |
| 2026-08-01to27 | open | `2026-08-01T00:00:00Z` | `2026-08-27T16:04:47Z` | 15 | 375 | `b26v89c19zqg8o3juewilr7wkp0qkm532sa2x4awgmid9` | `b26v89c19zqg8o3juewilvhcttgtfqziivluiht955xtp` |

### Pending first pages (14 windows, not yet opened in the expand pass)

2024-06, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2024-12, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-06, 2025-07

### Exhausted monthly (or sub) windows

2022-11, 2022-12, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11, 2023-12, 2024-01, 2024-02, 2024-05, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-06, 2026-10, 2026-11

## Coverage caveats

- 2022-11 was walked deeply and is exhausted. Several 2023–2025 months (including 2025-09 through 2025-12, and 2025-08 whose first page was empty) are exhausted or empty; 2025-01 through 2025-07 remain pending.
- 2026-11, 2026-10, 2026-06, 2026-05, 2026-04, 2026-03, 2026-02, and 2026-01 are exhausted. 2026-07 and 2026-09 remain open with next_tokens. Parent `2026-08` is pagination_stalled; continue only via subwindow `2026-08-01to27`, which is still open.
- 2024-03 and 2024-04 remain open (first pages were largely first-pass duplicates but still returned a next_token). 2026 is now the deepest year in the store; earlier years are not comparably deep.

- First-pass year-end samples remain in the JSONL and can make unopened years look like they have ~25 posts clustered at the end of the year.
- Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.
- Collection was paused to prioritize analysis and packaging; the daily read budget was not exhausted.

Do **not** claim this folder contains all tweets.
