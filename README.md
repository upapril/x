# X public-post research package (day-1 close)

Research folder for **five** public X accounts, packaged on **2026-11-24** (Asia/Shanghai, GMT+8). This is an **incomplete** archive plus evidence-grounded analysis. It does **not** contain all tweets.

Unique posts stored at day-1 close: **15,370** (@silverfang88 9,239; @iiiinvest 3,856; @alexandr_wang 1,873; @taresky 224; @thankUcrypto 178). @taresky and @thankUcrypto were added late on day 1 and have only an initial public sample.

This tree supersedes the narrative files from the earlier packages on this branch and adds two folders. Those earlier post ids are still in the JSONL. The packaging notes record zip SHA256 values; the zip files themselves are not stored in this repository.

## Accounts

| Handle | Folder | Unique posts stored | Notes |
|---|---|---:|---|
| [alexandr_wang](https://x.com/alexandr_wang) | `alexandr_wang/` | 1,873 | Operator / AI; not a trader |
| [iiiinvest](https://x.com/iiiinvest) | `iiiinvest/` | 3,856 | Deep 2026; earlier years thin |
| [silverfang88](https://x.com/silverfang88) | `silverfang88/` | 9,239 | Deep 2021–23 and much of 2025–26 |
| [taresky](https://x.com/taresky) | `taresky/` | 224 | Day-1 initial sample only (profile post_count 34,003) |
| [thankUcrypto](https://x.com/thankUcrypto) | `thankUcrypto/` | 178 | Day-1 initial sample only (profile post_count 8,097) |

Start with [`INSIGHTS.md`](INSIGHTS.md). Then each `analysis.md` and [`FINANCE_SKILLS_COMPARISON.md`](FINANCE_SKILLS_COMPARISON.md). Coverage and open tokens: each `coverage_manifest.md`, plus [`logs/remaining_jobs_day1.json`](logs/remaining_jobs_day1.json) for the 25 Nov 2026 08:00 Asia/Shanghai continuation. Methods: [`METHODOLOGY.md`](METHODOLOGY.md). Wang page versions: [`public_sources_wang.md`](public_sources_wang.md). Vendored skills, not installed: [`vendor/finance-skills/`](vendor/finance-skills/) and [`vendor/finance-skills.PROVENANCE.md`](vendor/finance-skills.PROVENANCE.md).

**Still partial.** Daily X reads left after the last ingested call: **61 of 1,000**, reset 2026-11-25 08:00 Asia/Shanghai. Collection stopped above a ~40 reserve, not because the histories were finished.

- **@alexandr_wang:** 2012–2014 not proven exhausted. Open: 2016-12, 2017-02–04, 2018-01–10, 2019-08. Pending from 2017-05–12 and most of 2024–2026. 2024–2026 counts are still the earlier samples (50 / 75 / 161).
- **@iiiinvest:** 2026 is deep (3,321 posts). Open: 2024-03, 2024-04, 2026-07, 2026-09, 2026-08-01to27. 2026-08 is stalled. Pending: 2024-06 through 2025-07. 2023–2025 stay thin (37 / 21 / 69).
- **@silverfang88:** 2025 is now 1,469 posts, not the old 25. Still open: 2024-03, 2024-05–09, 2025-05–07. Stalled: 2023-09 and 2026-07. Pending includes 2024-10–12, 2025-01–04, and several 2026 months.
- **@taresky and @thankUcrypto:** first samples only. Almost every opened window still has a `next_token`. Most months were never opened (224 of 34,003; 178 of 8,097).

Each account folder also has `profile.json`, `normalized/posts.jsonl`, `normalized/posts_lite.jsonl`, `raw/` page payloads, `archives/YYYY.md`, and `chronological_archive.md`.

Authoritative day-1 footer: **61 of 1,000** daily X reads remaining, reset `2026-11-25T00:00:00.000Z` = 2026-11-25 08:00 Asia/Shanghai.
