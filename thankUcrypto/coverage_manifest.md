# Coverage manifest — @thankUcrypto

**Packaged:** 2026-11-24 20:40:23 GMT+8 (Asia/Shanghai, GMT+8).

This account folder is **not** a complete public history. Profile `post_count` is a platform lifetime figure, not proof that a remainder still exists or is retrievable.

## Stored corpus (deduplicated by string id)

- Unique posts stored: **178**
- Profile `post_count` at first lookup (24 Nov 2026): 8097
- Span (UTC): `2022-12-30T09:55:07.000Z` → `2026-11-24T11:05:18.000Z`
- Span (Asia/Shanghai, GMT+8): 2022-12-30 17:55:07 GMT+8 → 2026-11-24 19:05:18 GMT+8
- Types: original 82, reply 74, quote 21, repost 1
- Earliest stored: [1608763604010176512](https://x.com/thankUcrypto/status/1608763604010176512)
- Latest stored: [2125183975757119963](https://x.com/thankUcrypto/status/2125183975757119963)

### Posts by UTC year

| Year | Stored |
|---|---:|
| 2022 | 2 |
| 2023 | 25 |
| 2024 | 25 |
| 2025 | 50 |
| 2026 | 76 |

## Expand-pass window status

Status counts: `exhausted` 2, `open` 9, `pending` 40

Expand pass used fresh monthly `search_posts_all` windows (`from:<handle>`, `sort_order=recency`, `max_results=25`). Later pages store query, window bounds, input token, and output `next_token`. If an output token equals the input token on a duplicate page, the window is marked `pagination_stalled` and is not reused; the earlier remainder is opened as a subwindow.

### Open, stalled, or not-proven-exhausted windows (resumable)

| Label | Status | start_time | end_time | pages | added | next_token | last_input_token |
|---|---|---|---|---:|---:|---|---|
| timeline-recent | open | `None` | `None` | 1 | 24 | `7140dibdnow9c7btwp0gm9i8sjoq8m9keuzhjjx1ftyr8` | `—` |
| 2026-11 | open | `2026-11-01T00:00:00Z` | `2026-11-25T00:00:00Z` | 1 | 1 | `b26v89c19zqg8o3juzowlxwfcjef8gbd5vc978vr2uhrx` | `—` |
| 2026-10 | open | `2026-10-01T00:00:00Z` | `2026-11-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3juzlxod10t2jlubd1szxp6x1j4v7nh` | `—` |
| 2026-06 | open | `2026-06-01T00:00:00Z` | `2026-07-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3jueqimn5399wglj1wvbhph7sa5jvy5` | `—` |
| 2025-12 | open | `2025-12-01T00:00:00Z` | `2026-01-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3jue8hvvok54byopd5y3jn9t8jlcqyl` | `—` |
| 2025-06 | open | `2025-06-01T00:00:00Z` | `2025-07-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3fsc598rfej8hgc3qq162stvnzamxdp` | `—` |
| 2024-12 | open | `2024-12-01T00:00:00Z` | `2025-01-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3frr6rx3qiy6cxsmrxr487bij5l1ksd` | `—` |
| 2023-12 | open | `2023-12-01T00:00:00Z` | `2024-01-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3fr5kh0qyam3np3rae1pvqp2qhzxxtp` | `—` |
| 2022-12 | open | `2022-12-01T00:00:00Z` | `2023-01-01T00:00:00Z` | 1 | 2 | `b26v89c19zqg8o3fqk12y2l83isxjg0sb9ofufluiyjjx` | `—` |

### Pending first pages (40 windows, not yet opened in the expand pass)

2026-09, 2026-08, 2026-07, 2026-05, 2026-04, 2026-03, 2026-02, 2026-01, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2024-01, 2024-02, 2024-03, 2024-04, 2024-05, 2024-06, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11

### Exhausted monthly (or sub) windows

pinned, 2018-12

## Coverage caveats

- Day-1 collection is an initial sample only: public profile, one recent get_users_posts page, first pages of representative dated windows (2026-11, 2026-10, 2026-06, 2025-12, 2025-06, 2024-12, 2023-12, 2022-12, 2018-12), and the pinned post via get_posts_by_ids after an expansion 404. 178 unique posts stored versus profile post_count 8,097 at lookup. Explicitly partial.
- 2018-12 first page was empty with no next_token (exhausted for that month only — not proof the account was inactive in 2018). 2022-12 returned 2 posts but still has a next_token (open). A 2025-06 post says the author shared on Weibo from 2022-24 and '25年才转的推'; that is self-description, not a coverage proof. Pre-2025 X months remain mostly unsampled.
- Self-reported P&L, livestream-challenge totals, and copy-trading figures in posts are unverified. Do not infer a legal name from the display name 'allincrypto 熬鹰资本'.

- First-pass year-end samples remain in the JSONL and can make unopened years look like they have ~25 posts clustered at the end of the year.
- Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.
- Collection was paused to prioritize analysis and packaging; the daily read budget was not exhausted.

Do **not** claim this folder contains all tweets.
