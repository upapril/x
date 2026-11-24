# Coverage manifest: @iiiinvest

- Collection pass completed: 2026-11-24 19:09:28 GMT+8 (Asia/Shanghai) / 2026-11-24T11:09:28Z UTC
- User id: `1589763597705437184`
- Profile: https://x.com/iiiinvest
- Account created: 2022-11-07T23:36:06.000Z UTC
- Protected: False
- Profile `post_count` at lookup: **4858**
- Unique posts retrieved this pass: **366** (7.53% of the reported count)
- Completeness claim: **no** — this is a bounded first pass
- Retrieved span (UTC): 2022-11-27T13:36:12.000Z → 2026-11-24T09:50:06.000Z
- Types: {'original': 129, 'reply': 162, 'quote': 46, 'repost': 29}
- API pages stored: 15 (`{'get_users_posts': 3, 'search_posts_all': 12}`)

## End conditions

- get_users_posts was only advanced 3 pages (still had next_token); recent November 2026 is the dense timeline sample, not a complete timeline.
- search_posts_all year/quarter windows generally still have next_token; stopped after 1-2 pages per window.
- No posts retrieved between account creation 2022-11-07 and 2022-11-27 in this pass (window 2022-11-07 to 2022-12-07 still had next_token after one page ending 2022-11-27).

## Counts by year

| Year | Retrieved posts |
|---|---:|
| 2022 | 50 |
| 2023 | 25 |
| 2024 | 21 |
| 2025 | 69 |
| 2026 | 201 |

## Counts by year-month (retrieved only)

| Year-month | n |
|---|---:|
| 2022-11 | 13 |
| 2022-12 | 37 |
| 2023-06 | 3 |
| 2023-08 | 13 |
| 2023-09 | 3 |
| 2023-10 | 4 |
| 2023-11 | 2 |
| 2024-03 | 1 |
| 2024-04 | 3 |
| 2024-06 | 1 |
| 2024-07 | 1 |
| 2024-11 | 14 |
| 2024-12 | 1 |
| 2025-03 | 25 |
| 2025-05 | 20 |
| 2025-06 | 5 |
| 2025-07 | 13 |
| 2025-09 | 6 |
| 2026-03 | 25 |
| 2026-06 | 25 |
| 2026-09 | 25 |
| 2026-10 | 1 |
| 2026-11 | 125 |

## Months in the account lifetime with **zero** retrieved posts this pass

26 months. This includes both months that may truly have had no posts and months not sampled or not fully paged.

2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-07, 2023-12, 2024-01, 2024-02, 2024-05, 2024-08, 2024-09, 2024-10, 2025-01, 2025-02, 2025-04, 2025-08, 2025-10, 2025-11, 2025-12, 2026-01, 2026-02, 2026-04, 2026-05, 2026-07, 2026-08

## Open pagination tokens still to follow

15 stored pages still show a `next_token`. Full tokens are in `coverage_manifest.json`. This is not a deduplicated count of unfinished windows. Input tokens were not stored.


Pinned post: expansion 404, then `get_posts_by_ids` succeeded for `2110022220131226106`.

