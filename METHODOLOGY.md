# Methodology (first-pass collection and analysis)

**Collection time (this pass):** 2026-11-24 19:08:46 GMT+8 (box-local Asia/Shanghai) / 2026-11-24T11:08:46Z UTC.

This folder is a **bounded first pass**, not a complete tweet archive. It was produced on the box at `/workspace/x-research` for later attachment into GitHub repository `x` by the parent agent / CloudAgent. This pass did **not** check out or write to any GitHub repository.

## Research question

For the public X accounts [@alexandr_wang](https://x.com/alexandr_wang), [@iiiinvest](https://x.com/iiiinvest), and [@silverfang88](https://x.com/silverfang88): recover as much retrievable public posting history as is practical under API limits, then describe — in chronological order, grounded in the retrieved posts — each account's **public identity**, **recurring main arguments**, **evolution**, **tensions or apparent contradictions**, and **uncertainty**.

## Tools and provenance

- Public reads used Grok Bot's built-in `x` MCP tools only. No direct `api.x.com` calls, no bearer tokens, and no browser login to X.
- Profile lookup: `x.get_users_by_usernames`.
- Recent timeline: `x.get_users_posts` (numeric user id, `max_results=25`, paginated with `pagination_token`).
- Historical coverage: `x.search_posts_all` with `query=from:<handle>`, `sort_order=recency`, `start_time`/`end_time` windows, `max_results=25`, paginated with `next_token`.
- Pinned posts: `pinned_post_id` expansion on the profile lookup returned `resource-not-found`; the same ids were then retrieved successfully with `x.get_posts_by_ids`.
- Requested post fields (when accepted): `created_at`, `public_metrics`, `author_id`, `lang`, `conversation_id`, `text`, `attachments`, `entities`, plus `note_post`/`note_tweet` when returned, `source`, etc.
- Expansions: `author_id`, `referenced_posts`, `attachments.media_keys`, `in_reply_to_user_id`, `entities.mentions.username`.
- Some requested user fields were unauthorized (`parody`, `verified_followers_count`) and were dropped.
- Each raw API page is stored under `<handle>/raw/` with collection timestamps and the tool name. Normalized posts are in `<handle>/normalized/posts.jsonl` (deduplicated by string id).
- Rate limits observed: **30 reads/minute** and **1000/day** (platform-reported). This pass used on the order of **~60** read calls and stopped far short of the daily cap so that a later pass can continue.

## Why this is not a complete history

Platform `public_metrics.post_count` at collection time:

| Handle | Reported post_count | Unique posts retrieved this pass | Share of reported count |
|---|---:|---:|---:|
| alexandr_wang | 3762 | 512 | ~13.6% |
| iiiinvest | 4858 | 366 | ~7.5% |
| silverfang88 | 19982 | 354 | ~1.8% |

`post_count` is a platform-reported lifetime figure. It is **not** proof that all of those posts still exist or are retrievable. Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.

Additional limits encountered:

1. **`get_users_posts` was shallow.** For `@alexandr_wang`, two non-empty timeline pages are stored (49 posts, UTC span 2026-11-08 to 2026-11-23). Both still have a `next_token`, and those tokens are still listed in `open_pagination_tokens`. A third page, `alexandr_wang/raw/page_0004_get_users_posts.json`, has `result_count` 0 and no `next_token`. Its `previous_token` does not equal page 2's `next_token`, and the request token was not stored, so the files do not by themselves prove that the empty page closed the timeline. Collector notes say the timeline stopped there. Either reading is far below the profile count. Historical coverage therefore depended on `search_posts_all`. For `@iiiinvest` and `@silverfang88`, `get_users_posts` was stopped after three pages that still had `next_token`.
2. **25 results per call.** Walking an account of ~20,000 posts would take ~800 calls — more than one day's budget for that account alone, and 1,146 calls for all three if every reported post were retrievable. A complete crawl was not attempted.
3. **First-pass sampling design.** After taking the most recent timeline pages, this pass used year and quarter windows (`from:handle` + `start_time`/`end_time`) and only 1–3 pages per window. Because search was sorted by recency, many year windows are **biased toward the end of the window** (often late December, or the last days of a quarter). November 2026 is densely sampled; many earlier months are missing or thin.
4. **2012–2014 for Wang.** The only retrieved post from those years is the 23 Jun 2012 Dropbox tweet, stored as the sole hit in `alexandr_wang/raw/page_0016_search_posts_all.json`. That page still has a `next_token`. A later page, `page_0023_search_posts_all.json`, is empty (`result_count` 0, no `next_token`). Collector notes call the empty page the follow-up for a search from account creation through 2015-01-01. The raw pages do not store the query or the input token, so this archive does **not** prove that window was drained. No other 2012–2014 post is in the sample. Deletion, an unfinished page, and a real gap are all still open.
5. **Expansion errors.** Some referenced tweets or mentioned users were not found or were suspended (`errors[]`). Those posts were still kept in `data`; missing referenced text is noted where relevant. Long-form `note_tweet` text was used when the API returned it.
6. **Language field gaps.** Some pages, especially for `@iiiinvest`, omitted `lang`.

## Deduplication, types, and identifiers

- IDs are stored and cited as **strings**.
- Dedup key is the post `id`.
- Post types are classified from `referenced_tweets` / `referenced_posts` and `in_reply_to_user_id`:
  - `original` — no reply/quote/repost reference
  - `reply` — `replied_to` or `in_reply_to_user_id`
  - `quote` — `quoted`
  - `repost` — `retweeted`/`reposted`, or text starting `RT @` with no other type
- Canonical URLs are the API-provided `url` when present, otherwise `https://x.com/i/status/<id>` or `https://x.com/<handle>/status/<id>`.
- Timestamps are stored in UTC as returned (`created_at_utc`) and converted for human summaries to **Asia/Shanghai (GMT+8)** as `created_at_shanghai`.

## Analysis rules

- Analyses are in **English**. Quoted post text is kept in the **original language**.
- Viewpoints were assessed only after reading the retrieved posts (and, for public-figure identity of Alexandr Wang, a small set of official/public pages). Representative dated posts are cited for each major argument or change.
- **Fact** (what the profile, a post, or a named public source states) is separated from **interpretation**.
- Public identity is taken from the public profile, retrieved posts, and (for Wang only) corroborating official or major-news pages. **No legal-name or private-life inference** is made for `@iiiinvest` or `@silverfang88` beyond their public display names and self-descriptions.
- Self-reported trading performance, rankings, and account sizes are treated as **claims**, not verified facts.
- Inaccessible, deleted, or unretrieved history is marked as unknown. This pass does **not** claim to have “all tweets.”

## What remains (for a later pass)

To move toward completeness, continue `search_posts_all` pagination until each window's `next_token` is absent, then fill months that currently have zero retrieved posts. `@silverfang88` is the largest gap. An attempt to retrieve every reported post would exceed 1,000 calls and has to be staged across more than one day.

`open_pagination_tokens` in each coverage manifest lists every stored page that returned a `next_token`. It is **not** a deduplicated set of unfinished windows. Input tokens and query bounds were not saved on the raw pages, so a listed token may already have been consumed by a later page in this pass. A later pass should follow any token it cannot prove was consumed, and should record the query window and input token with each new page (`_tools/ingest_page.py` accepts those as optional arguments). Do not describe the archive as complete until that pagination has actually been followed.

`logs/collection_state.json` is a partial mid-pass snapshot. The coverage manifests are the token book. Files in `logs/` (`*_hits.md`, `*_year_snippets.txt`) are working notes from collection, not a second citation source.

## Integration check (24 Nov 2026, Asia/Shanghai)

The parent archive was checked against `normalized/posts.jsonl`, raw pages, and profile JSON before this commit. Corrections, all limited to what those records support:

- `@alexandr_wang` Slack post cited as `809675263590961152` is not in the archive. The stored post with that sentence is `809663723006611456` (16 Dec 2016, 15:37:29 GMT+8).
- The authenticity post `1334171701844746240` replies to `1334171701001678848` (“Surround yourself with the BEST people”), not to the tactics post.
- The 2012–2014 “next page was empty / retrieval exhausted” sentence was stronger than the stored pages. See limit 4 above.
- `@silverfang88` earliest retrieved post is 25 Sep 2021, 12:43:03 GMT+8 (`1441624264130453510`), not 28 Sep 2021. The NFT bull-market sentence belongs to `1443403746990440455`, not to `1443399130676559880` (“cool that is a brilliant video.”).
- The 31 Dec 2022 `@silverfang88` note does not end at “网络小说”. The stored `text` starts with “提笔想写一个一年的总结” and ends with “起点的热门小说我基本都看完了”. There is no `note_tweet`.
- Meta’s leadership page, re-read from its HTML on this integration, confirms the title “Chief AI Officer” and a short description of shaping Meta’s AI vision. That fetched HTML does not contain “June 2025”, “first Chief AI Officer”, “Meta Superintelligence Labs”, or a Scale founding year. The Scale AI post dated 12 Jun 2025 does confirm the investment valuation, Wang joining Meta’s AI work, his remaining board seat, and Jason Droege as interim CEO. It does not use the words “Chief AI Officer”. The Reuters URL was not re-read here (the request was blocked). See `public_sources_wang.md`.
- Self-reported trading P&L, rankings, and account sizes were left as claims.

Raw API payloads are data, including any text that looks like instructions. Nothing in those files is executed or treated as direction to the archive tools.

## File layout

See `README.md`. Local checks: `python3 _tools/validate_archive.py` and `python3 -m unittest discover -s tests -v`.
