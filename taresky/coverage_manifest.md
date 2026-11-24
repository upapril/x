# Coverage manifest — @taresky

**Packaged:** 2026-11-24 20:40:23 GMT+8 (Asia/Shanghai, GMT+8).

This account folder is **not** a complete public history. Profile `post_count` is a platform lifetime figure, not proof that a remainder still exists or is retrievable.

## Stored corpus (deduplicated by string id)

- Unique posts stored: **224**
- Profile `post_count` at first lookup (24 Nov 2026): 34003
- Span (UTC): `2016-12-15T00:47:22.000Z` → `2026-11-24T09:10:31.000Z`
- Span (Asia/Shanghai, GMT+8): 2016-12-15 08:47:22 GMT+8 → 2026-11-24 17:10:31 GMT+8
- Types: original 53, reply 138, quote 22, repost 11
- Earliest stored: [809198127789969409](https://x.com/taresky/status/809198127789969409)
- Latest stored: [2125155090130731098](https://x.com/taresky/status/2125155090130731098)

### Posts by UTC year

| Year | Stored |
|---|---:|
| 2016 | 25 |
| 2021 | 25 |
| 2022 | 25 |
| 2023 | 1 |
| 2024 | 25 |
| 2025 | 50 |
| 2026 | 73 |

## Expand-pass window status

Status counts: `exhausted` 1, `open` 10, `pending` 40

Expand pass used fresh monthly `search_posts_all` windows (`from:<handle>`, `sort_order=recency`, `max_results=25`). Later pages store query, window bounds, input token, and output `next_token`. If an output token equals the input token on a duplicate page, the window is marked `pagination_stalled` and is not reused; the earlier remainder is opened as a subwindow.

### Open, stalled, or not-proven-exhausted windows (resumable)

| Label | Status | start_time | end_time | pages | added | next_token | last_input_token |
|---|---|---|---|---:|---:|---|---|
| timeline-recent | open | `None` | `None` | 1 | 25 | `7140dibdnow9c7btwp0gm9gqgrurrob7n4a5eytlynzg0` | `—` |
| 2026-11 | open | `2026-11-01T00:00:00Z` | `2026-11-25T00:00:00Z` | 1 | 0 | `b26v89c19zqg8o3juzowln63mmdar00jvz60l8hp0a1dp` | `—` |
| 2026-10 | open | `2026-10-01T00:00:00Z` | `2026-11-01T00:00:00Z` | 1 | 23 | `b26v89c19zqg8o3juzlxod0q3o7foj3kl2vh3a9t75u2l` | `—` |
| 2026-06 | open | `2026-06-01T00:00:00Z` | `2026-07-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3juetgavebt9yov3dwq2lcd83sww8e5` | `—` |
| 2025-12 | open | `2025-12-01T00:00:00Z` | `2026-01-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3jue8j4zpqh0ulagerz9w1fngl493st` | `—` |
| 2025-06 | open | `2025-06-01T00:00:00Z` | `2025-07-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3fsc5996chnmiu8k80o5is81hndxoxp` | `—` |
| 2024-12 | open | `2024-12-01T00:00:00Z` | `2025-01-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3frr6rwzj66j4eq6bt70sn51ijbkpdp` | `—` |
| 2022-12 | open | `2022-12-01T00:00:00Z` | `2023-01-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3fqk12iwydq5frlwh39wmfq8h9udc3h` | `—` |
| 2021-01 | open | `2021-01-01T00:00:00Z` | `2021-02-01T00:00:00Z` | 1 | 25 | `b26v89c19zqg8o3foskt5god0ueh1goua2qzbpfrvo6f1` | `—` |
| 2016-12 | open | `2016-12-01T00:00:00Z` | `2017-01-01T00:00:00Z` | 1 | 25 | `1jzu9lk96gu5npw3iy4bo3bin9qtacqjskhen8rrf0ql` | `—` |

### Pending first pages (40 windows, not yet opened in the expand pass)

2026-09, 2026-08, 2026-07, 2026-05, 2026-04, 2026-03, 2026-02, 2026-01, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2024-01, 2024-02, 2024-03, 2024-04, 2024-05, 2024-06, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11

### Exhausted monthly (or sub) windows

pinned

## Coverage caveats

- Day-1 collection is an initial sample only: public profile, one recent get_users_posts page, first pages of representative dated windows (2026-11, 2026-10, 2026-06, 2025-12, 2025-06, 2024-12, 2022-12, 2021-01, 2016-12), and the pinned post via get_posts_by_ids after an expansion 404. 224 unique posts stored versus profile post_count 34,003 at lookup. This is not a complete history and is recency/year-end biased in unpaged months.
- Every dated window opened on day 1 still has a next_token (status=open) except the single-id pinned fetch (exhausted). 2018-12 was not searched. Unstarted years include 2011-09 (account creation) through 2015, most of 2016–2020, and most months of 2021–2026 not listed above.
- Do not treat year counts of 25 as low activity. Do not infer a legal name. Bio text '套利 1~100x | 2021~2025.6' is profile wording, not a verified track record.

- First-pass year-end samples remain in the JSONL and can make unopened years look like they have ~25 posts clustered at the end of the year.
- Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.
- Collection was paused to prioritize analysis and packaging; the daily read budget was not exhausted.

Do **not** claim this folder contains all tweets.
