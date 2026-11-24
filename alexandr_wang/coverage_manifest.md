# Coverage manifest: @alexandr_wang

- Collection pass completed: 2026-11-24 19:09:28 GMT+8 (Asia/Shanghai) / 2026-11-24T11:09:28Z UTC
- User id: `615818451`
- Profile: https://x.com/alexandr_wang
- Account created: 2012-06-23T02:46:22.000Z UTC
- Protected: False
- Profile `post_count` at lookup: **3762**
- Unique posts retrieved this pass: **512** (13.61% of the reported count)
- Completeness claim: **no** — this is a bounded first pass
- Retrieved span (UTC): 2012-06-23T02:48:05.000Z → 2026-11-23T04:21:30.000Z
- Types: {'original': 160, 'quote': 109, 'reply': 192, 'repost': 51}
- API pages stored: 26 (`{'get_users_posts': 3, 'search_posts_all': 23}`)

## End conditions

- Two non-empty `get_users_posts` pages are stored (49 posts, UTC 2026-11-08 through 2026-11-23). Both still have `next_token` values listed in `open_pagination_tokens`. `page_0004_get_users_posts.json` has `result_count` 0 and no `next_token`. Its `previous_token` does not equal page 2's `next_token`, and the request token was not stored, so the file does not by itself prove that the empty page closed the timeline. Collector notes say the timeline stopped there. This is not a complete user-timeline crawl.
- `page_0016_search_posts_all.json` returned the single 2012-06-23 post and still has a `next_token`. `page_0023_search_posts_all.json` is empty (`result_count` 0, no `next_token`). Collector notes treat that empty page as the follow-up for a 2012-06-23 to 2015-01-01 search. The raw payload does not store the query or input token, so 2012–2014 retrieval is not proven exhausted. No other 2012–2014 post is in this archive.
- Most year/quarter `search_posts_all` pages still have `next_token` and were stopped after 1–3 pages (bounded first pass). `open_pagination_tokens` lists every stored page that returned a `next_token` (24). That count is not a deduplicated set of unfinished windows, because continuations cannot be reconstructed without input tokens.

## Counts by year

| Year | Retrieved posts |
|---|---:|
| 2012 | 1 |
| 2015 | 25 |
| 2016 | 25 |
| 2017 | 25 |
| 2018 | 25 |
| 2019 | 25 |
| 2020 | 25 |
| 2021 | 25 |
| 2022 | 25 |
| 2023 | 25 |
| 2024 | 50 |
| 2025 | 75 |
| 2026 | 161 |

## Counts by year-month (retrieved only)

| Year-month | n |
|---|---:|
| 2012-06 | 1 |
| 2015-07 | 7 |
| 2015-09 | 6 |
| 2015-10 | 4 |
| 2015-11 | 6 |
| 2015-12 | 2 |
| 2016-12 | 25 |
| 2017-10 | 7 |
| 2017-11 | 8 |
| 2017-12 | 10 |
| 2018-10 | 1 |
| 2018-11 | 8 |
| 2018-12 | 16 |
| 2019-12 | 25 |
| 2020-12 | 25 |
| 2021-11 | 11 |
| 2021-12 | 14 |
| 2022-12 | 25 |
| 2023-11 | 11 |
| 2023-12 | 14 |
| 2024-06 | 25 |
| 2024-11 | 3 |
| 2024-12 | 22 |
| 2025-04 | 15 |
| 2025-05 | 9 |
| 2025-06 | 3 |
| 2025-07 | 7 |
| 2025-08 | 9 |
| 2025-09 | 13 |
| 2025-10 | 2 |
| 2025-11 | 8 |
| 2025-12 | 9 |
| 2026-01 | 3 |
| 2026-02 | 4 |
| 2026-03 | 4 |
| 2026-04 | 8 |
| 2026-05 | 13 |
| 2026-06 | 4 |
| 2026-08 | 25 |
| 2026-09 | 26 |
| 2026-10 | 24 |
| 2026-11 | 50 |

## Months in the account lifetime with **zero** retrieved posts this pass

132 months. This includes both months that may truly have had no posts and months not sampled or not fully paged.

2012-07, 2012-08, 2012-09, 2012-10, 2012-11, 2012-12, 2013-01, 2013-02, 2013-03, 2013-04, 2013-05, 2013-06, 2013-07, 2013-08, 2013-09, 2013-10, 2013-11, 2013-12, 2014-01, 2014-02, 2014-03, 2014-04, 2014-05, 2014-06, 2014-07, 2014-08, 2014-09, 2014-10, 2014-11, 2014-12, 2015-01, 2015-02, 2015-03, 2015-04, 2015-05, 2015-06, 2015-08, 2016-01, 2016-02, 2016-03, … (92 more) … , 2024-10, 2025-01, 2025-02, 2025-03, 2026-07

## Open pagination tokens still to follow

24 stored pages still show a `next_token`. Full tokens are in `coverage_manifest.json`. This is not a deduplicated count of unfinished windows.


Pinned post: expansion 404, then `get_posts_by_ids` succeeded for `2103551714536439951`.

