# Coverage manifest: @silverfang88

- Collection pass completed: 2026-11-24 19:09:28 GMT+8 (Asia/Shanghai) / 2026-11-24T11:09:28Z UTC
- User id: `1435990322702520320`
- Profile: https://x.com/silverfang88
- Account created: 2021-09-09T15:36:07.000Z UTC
- Protected: False
- Profile `post_count` at lookup: **19982**
- Unique posts retrieved this pass: **354** (1.77% of the reported count)
- Completeness claim: **no** — this is a bounded first pass
- Retrieved span (UTC): 2021-09-25T04:43:03.000Z → 2026-11-24T09:58:30.000Z
- Types: {'reply': 98, 'original': 210, 'quote': 35, 'repost': 11}
- API pages stored: 15 (`{'get_users_posts': 3, 'search_posts_all': 12}`)

## End conditions

- get_users_posts was only advanced 3 pages (still had next_token).
- search_posts_all year/quarter windows generally still have next_token; stopped after 1-2 pages per window. Late-window bias is severe for 2021-2025 (often only the last days of December or of a sampled month).
- Earliest retrieved post is 2021-09-25T04:43:03.000Z (2021-09-25 12:43:03 GMT+8, id `1441624264130453510`), not account creation 2021-09-09. Posts from 2021-09-28 are also in the sample. Early September 2021 was not fully paged.

## Counts by year

| Year | Retrieved posts |
|---|---:|
| 2021 | 49 |
| 2022 | 25 |
| 2023 | 25 |
| 2024 | 50 |
| 2025 | 25 |
| 2026 | 180 |

## Counts by year-month (retrieved only)

| Year-month | n |
|---|---:|
| 2021-09 | 6 |
| 2021-10 | 15 |
| 2021-11 | 4 |
| 2021-12 | 24 |
| 2022-12 | 25 |
| 2023-12 | 25 |
| 2024-06 | 25 |
| 2024-12 | 25 |
| 2025-12 | 25 |
| 2026-03 | 25 |
| 2026-06 | 25 |
| 2026-09 | 23 |
| 2026-10 | 1 |
| 2026-11 | 106 |

## Months in the account lifetime with **zero** retrieved posts this pass

49 months. This includes both months that may truly have had no posts and months not sampled or not fully paged.

2022-01, 2022-02, 2022-03, 2022-04, 2022-05, 2022-06, 2022-07, 2022-08, 2022-09, 2022-10, 2022-11, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09, 2023-10, 2023-11, 2024-01, 2024-02, 2024-03, 2024-04, 2024-05, 2024-07, 2024-08, 2024-09, 2024-10, 2024-11, 2025-01, 2025-02, 2025-03, 2025-04, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2026-01, 2026-02, 2026-04, 2026-05, 2026-07, 2026-08

## Open pagination tokens still to follow

15 stored pages still show a `next_token`. Full tokens are in `coverage_manifest.json`. This is not a deduplicated count of unfinished windows. Input tokens were not stored.


Pinned post: expansion 404, then `get_posts_by_ids` succeeded for `2109440726865985560`.

