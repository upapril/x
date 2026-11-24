# Methodology (day-1 close, explicitly partial)

## What this package is

A 24 Nov 2026 public-X research archive for five accounts — originally [@alexandr_wang](https://x.com/alexandr_wang), [@iiiinvest](https://x.com/iiiinvest), [@silverfang88](https://x.com/silverfang88), with [@taresky](https://x.com/taresky) and [@thankUcrypto](https://x.com/thankUcrypto) added late on day 1. Stored under `/workspace/x-research`. **This is not a complete tweet archive for any handle.**

Unique posts at day-1 close, validated with `json.loads` on every `normalized/posts.jsonl` line (bad lines = 0, duplicate ids = 0, `author_username` matches folder):

| Handle | Unique posts stored | Profile `post_count` at lookup | Day-1 collection depth |
|---|---:|---:|---|
| silverfang88 | 9,239 | 19,982 (first lookup) | Deep 2021–2023 and much of 2025–2026; parts of 2024 and early 2025 remain |
| iiiinvest | 3,856 | 4,858 (first lookup) | Deep 2026; 2023–2025 still thin |
| alexandr_wang | 1,873 | 3,762 (first lookup) | 2018–2023 much improved; 2012–2014 unproven; 2024–2026 monthly jobs mostly unopened |
| taresky | 224 | 34,003 (24 Nov 2026 20:31 GMT+8) | Initial sample only |
| thankUcrypto | 178 | 8,097 (24 Nov 2026 20:31 GMT+8) | Initial sample only |
| **Total** | **15,370** | | |

Profile `post_count` is **not** a missing-count proof.

## Tools and constraints

Built-in first-party-adjacent `x` MCP **public** reads only: `get_users_by_usernames`, `get_users_posts`, `search_posts_all` (`query=from:handle`, `sort_order=recency`, `max_results=25` because the connector caps ~25), `get_posts_by_ids`. Large responses were written to disk (`write_to_file`) and ingested without pasting raw payloads into the model context. No browser X login, no user-X session, no `api.x.com` bearer tokens, no GitHub writes from this box.

Pagination: later pages store query, window, and input token. If `next_token` equals the input token on a duplicate page, the window is `pagination_stalled` and that token is never reused; an earlier remainder may be opened with `end_time` = oldest timestamp of the duplicate page. Empty `result_count: 0` with no `next_token` marks a window exhausted. 503s do not advance a window (they may still decrement the daily footer).

IDs are stored as strings. Post types from `referenced_tweets` / `referenced_posts` and `in_reply_to_user_id`. Timestamps: API `created_at` UTC; human summaries Asia/Shanghai (GMT+8). Original-language text is preserved. Canonical URLs are `https://x.com/{handle}/status/{id}`. Collection time and source file are in each post’s `collection` object and in `raw/`.

JSONL control characters: raw newlines inside JSON strings are escaped losslessly (`_repair_json_strings` / hardened `load_jsonl`). Two silverfang88 records were repaired this way earlier in the day; a third split (`1928748987865080287`) was repaired at day-1 close — text was escaped, not rewritten. Backup copies of the pre-repair files were left on disk and **excluded from the zip**.

## Day-1 budget footer (authoritative)

After the last ingested X call (pinned-post `get_posts_by_ids` for the two new accounts):

```
X reads left for this user: 23 of 30 this minute (resets at 2026-11-24T12:33:00.000Z), 61 of 1000 today (resets at 2026-11-25T00:00:00.000Z).
```

- Daily reset: `2026-11-25T00:00:00.000Z` = **2026-11-25 08:00:00 GMT+8 (Asia/Shanghai)**.
- The original ~75 reserve was relaxed at the end of the day so that **22** public reads could be spent on the two new handles (1 combined profile lookup, 2 recent timeline first pages, 18 representative dated first pages, 1 pinned-ids lookup). Collection then **stopped**, leaving **61** daily remaining (above a ~40 floor for other tasks).
- 30 reads/minute and 1,000/day limits still apply tomorrow.

## Exact remaining work for a routine at 08:00 Asia/Shanghai on 25 Nov 2026

The reproducible job list is:

- `logs/remaining_jobs_day1.json` — open windows with `next_token`, stalled tokens never to reuse, pending labels, and calendar months that still have **no job at all** (especially @taresky 131 months and @thankUcrypto 79 months).
- `logs/RESUME_OPEN_JOBS.json` and `logs/expand_jobs.json` — live job state.
- Each account’s `coverage_manifest.json`.

High-value open windows to continue first (tokens in the JSON, not repeated at length here): @silverfang88 `2025-07`, `2025-06`, `2025-05`; @iiiinvest `2026-07`, `2026-09`, `2026-08-01to27`; then the still-open first pages for @taresky and @thankUcrypto; then remaining Wang 2018 open months; then lower-priority mid-2024 @silverfang88 and 2016–17 Wang leftovers.

**Do not reopen** exhausted windows. **Do not reuse** stalled tokens:

- silverfang88 `2023-09` `b26v89c19zqg8o3fr5beqknfiduf3z8svkzzdfjkf2ttp`
- silverfang88 `2026-07` `b26v89c19zqg8o3juewg2tl5lpfe021lawn2fn8ar26pp` (continue only via already-exhausted `2026-07-01to26`; 26–31 Jul 2026 was not opened as its own subwindow)
- iiiinvest parent `2026-08` tokens `b26v89c19zqg8o3juezgoudctnrq3quemi6wf56f1d5dp` and `b26v89c19zqg8o3juezgp0sqjwdnag097te7ltdd0hzlp` (continue only via open `2026-08-01to27`)
- alexandr_wang `2012-2014` is `not_proven_exhausted` (empty-page input token not saved)

Do not open silverfang88 pending label `2026-11` (overlaps exhausted `2026-11-01to08` and `2026-11-08to25`).

Year-end first pages are recency-biased (~25 newest posts). First-page empty months (e.g. thankUcrypto 2018-12, iiiinvest 2025-08) prove only that the query returned no posts in that window, not that the account was silent all year.

## Significant Meta facts

Only text this repository has actually captured is treated as a source fact. Scale’s 12 Jun 2025 announcement was re-read and does not say “Chief AI Officer.” Wang’s 1 Jul 2025 post does. Meta’s leadership URL was fetched twice during integration; the captured HTML supports the title and a short vision sentence, and does not contain “first-ever,” “June 2025,” or “Meta Superintelligence Labs.” The day-1 packaging note attributes that longer sentence to the same URL. Both versions are in `public_sources_wang.md`. They are not combined. Both Reuters URLs returned HTTP 401 and were not re-read.

## Prior packages

Packaging notes record these zip SHA256 values. The zip files are not stored in this repository. The post ids from the commits on this branch before this close remain inside the JSONL.

- first pass `455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976` (git `7c43efc`, 1,232 posts)
- expanded package, as recorded: `d601957063b3610067d2dafd6cab0a6effb63e771bd642df57233b5e44fee6c7`
- 9,435-post package, as recorded: `1ab3fc4aaee8667c42d833543a85f86f54ff9dabe165f6305d56769aed4d8e58` (packaged 2026-11-24 20:01 GMT+8)
- the 8,100-post tree on this branch is git `5e939e9`

## File layout

See `README.md`. Analyses distinguish fact (quoted dated posts), interpretation, and practical tests. No fabricated returns or backtests.
