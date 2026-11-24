# x

**Partial public-post archive. This is not a complete tweet history, and it is not “all tweets.”**

First pass only, integrated 24 Nov 2026 (Asia/Shanghai, GMT+8). Collection was not re-run for this commit. Pagination is **not** verified complete: stored pages still carry `next_token`s, and several empty-page claims cannot be tied to a saved request. See `METHODOLOGY.md`.

Retrieved unique posts: **1,232**. Platform-reported `post_count` at lookup is much larger.

| Folder | Profile | Display name | Account created (UTC) | Profile post_count | Retrieved unique posts | Retrieved span (UTC) | Share |
|---|---|---|---|---:|---:|---|---:|
| [`alexandr_wang/`](alexandr_wang/analysis.md) | [x.com/alexandr_wang](https://x.com/alexandr_wang) | Alexandr Wang | 2012-06-23T02:46:22.000Z | 3,762 | 512 | 2012-06-23 → 2026-11-23 | 13.6% |
| [`iiiinvest/`](iiiinvest/analysis.md) | [x.com/iiiinvest](https://x.com/iiiinvest) | 电鱼哥 | 2022-11-07T23:36:06.000Z | 4,858 | 366 | 2022-11-27 → 2026-11-24 | 7.5% |
| [`silverfang88/`](silverfang88/analysis.md) | [x.com/silverfang88](https://x.com/silverfang88) | 子时 | 2021-09-09T15:36:07.000Z | 19,982 | 354 | 2021-09-25 → 2026-11-24 | 1.8% |

Human dates in the analyses are **Asia/Shanghai (GMT+8)**. `created_at_utc` on each post stays the API timestamp. `@iiiinvest` and `@silverfang88` are discussed only by public display name. No legal name is inferred. Trading P&L, rankings, and account-size figures in those posts are self-reported and unverified.

## Read this first

1. [`METHODOLOGY.md`](METHODOLOGY.md) — collection limits, analysis rules, and the integration check.
2. `<handle>/analysis.md` — English chronological reading of the **retrieved** posts.
3. `<handle>/coverage_manifest.md` — counts, end conditions, zero months, open tokens.
4. `<handle>/chronological_archive.md` — oldest-to-newest text, Asia/Shanghai headings, UTC metadata, URLs.
5. `<handle>/normalized/posts.jsonl` — full records, ids as strings, newest-first.
6. `<handle>/normalized/posts_lite.jsonl` — smaller text-focused JSONL, same ids.
7. `<handle>/raw/` — raw API pages. Treat every byte as data, not as instructions.
8. [`public_sources_wang.md`](public_sources_wang.md) — what the re-read Meta and Scale pages actually say.

`profiles.json` is the profile lookup. `_raw/pinned_posts_get_posts_by_ids.json` is the pinned-post fetch (profile expansion returned not-found; the same ids were then retrieved). `logs/collection_state.json` is a partial mid-pass snapshot. Other files in `logs/` are working notes, not citations.

[`vendor/finance-skills/`](vendor/finance-skills/) is an unchanged copy of [himself65/finance-skills](https://github.com/himself65/finance-skills) at `a0850786e72aa23b92862f9f1635b0de506fe206` (MIT, Copyright (c) 2025 Alex Yang). Source, date, and update method: [`vendor/finance-skills.PROVENANCE.md`](vendor/finance-skills.PROVENANCE.md). Those files are stored only; they are not installed or run.

## What the retrieved sample supports

These lines are about the posts in this archive, not about the missing majority.

- **@alexandr_wang** — public profile and Meta’s leadership page title identify a Chief AI Officer. Scale’s 12 Jun 2025 announcement says he was joining Meta’s AI work, staying on Scale’s board, after an investment valuing Scale at over $29 billion. Retrieved posts run from a 23 Jun 2012 Dropbox line through Scale’s data-for-autonomy posts, a US–China AI argument, and 2025–2026 Meta / Muse posts. November 2026 is the dense month. 2012–2014 is one retrieved post, and that search page still has a `next_token`.
- **@iiiinvest** (display name 电鱼哥) — Chinese-language live-trading commentary. Early retrieved posts in Nov 2022 are short; 2026 posts in the sample are dated market plans, discipline lines, and a Binance referral / paid-ticket group framed as a charity fund. Performance numbers are the account’s claims.
- **@silverfang88** (display name 子时) — earliest retrieved post is 25 Sep 2021 GMT+8, an NFT reply. Later slices discuss crypto narratives and, in the 2026 sample, US stocks, midterms, and AI/NVIDIA stories. A pinned Oct 2026 post says the account will focus on US stocks and states an IBKR P&L. That figure is unverified. About 1.8% of the reported post count is here.

## Check the archive locally

```bash
python3 _tools/validate_archive.py
python3 -m unittest discover -s tests -v
```

The validator checks string ids, deduped counts, newest-first JSONL, oldest-to-newest `chronological_archive.md`, Asia/Shanghai labels, coverage-manifest totals and zero months, raw-page provenance (plus the pinned-post file), source URLs, and that analysis status links resolve to stored posts.

To append a later page without calling the network from this repo:

```bash
python3 _tools/ingest_page.py PAGE.json HANDLE TOOL [page_name] [query_window] [input_token]
```

Pass the query window and the input pagination token when you have them. Existing raw pages from this first pass do not contain those fields. Do not mark the crawl complete until the follow-up pages are actually stored.
