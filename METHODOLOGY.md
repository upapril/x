# Methodology (expanded collection and insight analysis)

**Packaged:** 2026-11-24 19:44:01 GMT+8 (box-local Asia/Shanghai) / 2026-11-24T11:44:01Z UTC.

This folder is an **expanded but still incomplete** public-post archive plus evidence-grounded analysis for three X accounts. It was produced on the box at `/workspace/x-research` for later attachment into GitHub repository `x` by the parent agent / CloudAgent. This work did **not** check out or write to any GitHub repository and did not create a Page.

The first-pass zip’s SHA256 is `455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976`. That file is not stored in this repository. The first-pass tree is git commit `7c43efc9646ebe174a1e5d43c669865d982909ba` (512 / 366 / 354 posts). This expanded JSONL is a superset of those ids. Analyses and manifests here supersede the first-pass narrative files.

## Research question

For the public X accounts [@alexandr_wang](https://x.com/alexandr_wang), [@iiiinvest](https://x.com/iiiinvest), and [@silverfang88](https://x.com/silverfang88):

1. Recover as much retrievable public posting history as is practical under API limits, with honest coverage and provenance.
2. Describe, in chronological order and grounded in retrieved posts, each account's public identity, recurring arguments, evolution, tensions, and uncertainty.
3. Go beyond persona labels: identify **operating and decision frameworks** actually present in posts — especially, for the two trading accounts, trader edge, signal vs noise, thesis vs timing, entries/exits, position sizing/leverage, loss limits, invalidation, and discipline/journaling/review.
4. For each important lesson, distinguish **explicit rules the account stated**, **the analyst's interpretation**, and a **recommended practical test**. Cite dated post URLs. Note chronological shifts and contradictory examples.
5. Do not fabricate returns, backtests, or proof of edge. Do not invent numerical risk thresholds or sizing rules and attribute them to the accounts. Treat self-reported performance, ranks, and account sizes as claims. Include failure modes, monetization, and survivorship caveats.
6. Treat @alexandr_wang as a **business / AI operator, not a trader**. Transferable ideas are analogies or inferences, not trading evidence.
7. Add a root `INSIGHTS.md` synthesizing similarities/differences and a practical, evidence-grounded trader study/checklist.

## Tools and provenance

- Public reads used Grok Bot's built-in `x` MCP tools only. No direct `api.x.com` calls, no bearer tokens, and no browser login to X.
- Profile lookup: `x.get_users_by_usernames`.
- Recent timeline: `x.get_users_posts` (numeric user id, `max_results=25`, paginated with `pagination_token`).
- Historical coverage: `x.search_posts_all` with `query=from:<handle>` (the parameter name is `query`, not `q`), `sort_order=recency`, `start_time`/`end_time` windows, `max_results=25`, paginated with `next_token`.
- Pinned posts: `pinned_post_id` expansion on the profile lookup returned `resource-not-found`; the same ids were then retrieved successfully with `x.get_posts_by_ids`.
- Requested post fields (when accepted): `created_at`, `public_metrics`, `author_id`, `lang`, `conversation_id`, `text`, `attachments`, `entities`, plus `note_post`/`note_tweet` when returned, `source`, etc.
- Expansions: `author_id`, `referenced_posts`, `attachments.media_keys`, `in_reply_to_user_id`.
- Some requested user fields were unauthorized (`parody`, `verified_followers_count`) and were dropped.
- Each raw API page is stored under `<handle>/raw/` with collection timestamps and the tool name. After a provenance patch, later pages also store **query, window bounds, input token, and output next_token**. Normalized posts are in `<handle>/normalized/posts.jsonl` (deduplicated by string id).
- Rate limits observed: **30 reads/minute** and **1000/day**. Daily reset is `2026-11-25T00:00:00.000Z` = **2026-11-25 08:00:00 GMT+8** (Asia/Shanghai). A reserve of about 75 daily reads was left unused by pausing collection.
- The connector advertises `max_results` up to 500, but pages effectively cap around 25; this pass used `max_results=25`.

## Why this is still not a complete history

Platform `public_metrics.post_count` at first profile lookup on 24 Nov 2026:

| Handle | Reported post_count | Unique posts stored in this package | Share of reported count (indicative only) |
|---|---:|---:|---:|
| alexandr_wang | 3762 | 788 | ~20.9% |
| iiiinvest | 4858 | 736 | ~15.1% |
| silverfang88 | 19982 | 6576 | ~32.9% |

`post_count` is a platform-reported lifetime figure. It is **not** proof that all of those posts still exist or are retrievable, and the percentages above are **not** a precise “missing count.” Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.

Additional limits:

1. **`get_users_posts` was shallow.** Historical coverage depended on `search_posts_all`.
2. **~25 results per call.** Completing a ~20,000-post account in one day is not feasible under the 1000/day cap, even if every post were still retrievable.
3. **First-pass sampling bias still present in unopened years.** The first pass used year/quarter windows and only a few pages per window, sorted by recency, so many later years in the store are still **biased toward the end of the window**. The expand pass opened **fresh monthly windows** and paginated them, but many months (especially silverfang 2024-10 through most of 2025–2026, iiiinvest 2024-06+, and Wang 2017-05 through much of 2018–2026) were never opened because collection was paused for packaging.
4. **2012–2014 for Wang** is `not_proven_exhausted`: only one stored post from that span (`216361960667754498`), and the input token for a later empty page was not saved.
5. **Pagination stall.** silverfang 2023-09 looped (output token = input token on a duplicate page). The token was not reused; an earlier subwindow was exhausted separately. Combined September 2023 coverage is therefore stalled-later plus exhausted-earlier, not a clean monthly exhaustion.
6. **Weaker early exhaustions.** Some 2021-09/10/11 silverfang exhaustions happened before input-token provenance was stored.
7. **Expansion errors.** Some referenced tweets or mentioned users were not found or were suspended. Posts in `data` were still kept.
8. **503s** on `search_posts_all` occurred; failed pages were not marked progressed. Some 503s may have counted against the daily cap.

## Deduplication, types, and identifiers

- IDs are stored and cited as **strings**.
- Dedup key is the post `id`.
- Post types are classified from `referenced_tweets` / `referenced_posts` and `in_reply_to_user_id`:
  - `original` — no reply/quote/repost reference
  - `reply` — `replied_to` or `in_reply_to_user_id`
  - `quote` — `quoted`
  - `repost` — `retweeted`/`reposted`, or text starting `RT @` with no other type
- Canonical URLs are the API-provided `url` when present, otherwise `https://x.com/<handle>/status/<id>`.
- Timestamps are stored in UTC as returned (`created_at_utc`) and converted for human summaries to **Asia/Shanghai (GMT+8)** as `created_at_shanghai`.

## Analysis rules

- Analyses are in **English**. Quoted post text is kept in the **original language**.
- Viewpoints were assessed only after reading retrieved posts (and, for public-figure identity of Alexandr Wang, a small set of official/public pages and later news corroboration of specific late-2026 claims). Representative dated posts are cited for each major argument or change.
- Three layers are kept distinct:
  - **Explicit:** wording the account actually posted, with date and URL.
  - **Interpretation:** the analyst's compression of a pattern, labeled as such.
  - **Practical test:** what a reader could try in order to *use* the idea; these are not the account's rules and are not presented as proven edge.
- Public identity is taken from the public profile, retrieved posts, and (for Wang only) corroborating official or major-news pages. **No legal-name or private-life inference** is made for `@iiiinvest` or `@silverfang88` beyond their public display names and self-descriptions.
- Self-reported trading performance, rankings, and account sizes are treated as **claims**, not verified facts. No returns are fabricated or backtested.
- Numerical risk or sizing figures are quoted only when the account itself posted them, as dated statements, not as a verified system and not as a recommendation.
- Inaccessible, deleted, or unretrieved history is marked as unknown. This package does **not** claim to have “all tweets.”

## Citation corrections carried forward

These first-pass errors were checked against the expanded JSONL and must not be reintroduced:

- Slack 200-users post is [`809663723006611456`](https://x.com/alexandr_wang/status/809663723006611456) (2016-12-16 15:37:29 GMT+8). Id `809675263590961152` is **absent**.
- Authenticity post [`1334171701844746240`](https://x.com/alexandr_wang/status/1334171701844746240) (2020-12-03 00:24:56 GMT+8) is a **reply** to `1334171701001678848`, not a stand-alone tactics essay.
- Intern open house is [`624051679432937472`](https://x.com/alexandr_wang/status/624051679432937472). Wealthfront list post is [`1073470437139439617`](https://x.com/alexandr_wang/status/1073470437139439617).
- Wang 2012–2014: only one stored post, [`216361960667754498`](https://x.com/alexandr_wang/status/216361960667754498) (2012-06-23 10:48:05 GMT+8).
- silverfang earliest *in this expanded store* is [`1437303812616720389`](https://x.com/silverfang88/status/1437303812616720389) (2021-09-13 14:35:07 GMT+8), a repost of @GoGalaGames — earlier than the first-pass earliest [`1441624264130453510`](https://x.com/silverfang88/status/1441624264130453510) (2021-09-25 12:43:03 GMT+8), which is still present.
- NFT bull line: [`1443403746990440455`](https://x.com/silverfang88/status/1443403746990440455) (2021-09-30 10:34:05 GMT+8).
- 31 Dec 2022 note root [`1609058637267492865`](https://x.com/silverfang88/status/1609058637267492865) ends “起点的热门小说我基本都看完了”; it is the first post of a thread, not the end of the thread. A later post in the same thread, [`1609058652547338240`](https://x.com/silverfang88/status/1609058652547338240), quotes Xu Xiake / “按照自己的方式，去度过人生.”
- On integration, Meta’s leadership-page HTML was re-read. It supports the Chief AI Officer title only. It does not contain “June 2025”, “first Chief AI Officer”, “Meta Superintelligence Labs”, or a 2016 founding year. Scale’s 12 Jun 2025 page was re-read and supports the investment, the move onto Meta’s AI work, the board seat, and the interim CEO. Both Reuters URLs returned HTTP 401 and were not re-read.

## Stopping and resume

Collection stopped to prioritize insight writing and packaging, not because pages were exhausted or the daily cap was hit. Open tokens and pending window labels are in `logs/RESUME_OPEN_JOBS.json`, `logs/expand_jobs.json`, and each `coverage_manifest.json`.

## File layout

See `README.md`.
