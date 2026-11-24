# X public-post research package (expanded)

Research folder for three public X accounts, packaged on **2026-11-24 19:44:01 GMT+8** (Asia/Shanghai). This is an **incomplete** archive plus evidence-grounded analysis. It does **not** contain all tweets.

Accounts:

| Handle | Folder | Unique posts stored | Span (Asia/Shanghai, GMT+8) |
|---|---|---:|---|
| [@alexandr_wang](https://x.com/alexandr_wang) | `alexandr_wang/` | 788 | 2012-06-23 10:48:05 → 2026-11-23 12:21:30 |
| [@iiiinvest](https://x.com/iiiinvest) | `iiiinvest/` | 736 | 2022-11-22 16:48:28 → 2026-11-24 17:50:06 |
| [@silverfang88](https://x.com/silverfang88) | `silverfang88/` | 6576 | 2021-09-13 14:35:07 → 2026-11-24 17:58:30 |

Start here:

- **[INSIGHTS.md](INSIGHTS.md)** — synthesis, differences, and a practical trader study/checklist grounded in the stored posts.
- **`analysis.md` in each account folder** — chronological evidence, core operating model, explicit rules vs interpretation vs practical tests, contradictions, monetization and performance caveats.
- **`coverage_manifest.md`** in each folder — what was actually retrieved, what is still open, and what must not be claimed.
- **[METHODOLOGY.md](METHODOLOGY.md)** — tools, provenance, analysis rules, citation corrections.
- **[public_sources_wang.md](public_sources_wang.md)** — what re-read public pages actually say about Wang, and which Reuters URLs were not re-read.
- **[FINANCE_SKILLS_COMPARISON.md](FINANCE_SKILLS_COMPARISON.md)** — how the stored posts relate to the vendored finance-skills docs, including the SEPA “never average down” vs @iiiinvest “越跌越买” conflict.

Per-account files:

- `profile.json` — first-lookup public profile
- `normalized/posts.jsonl` — full normalized records, deduped by string id
- `normalized/posts_lite.jsonl` — compact fields + full text
- `archives/YYYY.md` — full original-language text, chronological, one file per UTC year
- `chronological_archive.md` — year index plus a compact one-line index of every stored post
- `raw/` — API page payloads and `_page_index.json`
- `coverage_manifest.md` / `.json`

Root also has `profiles.json`, `collection_summary.json`, and `logs/` (including `expand_jobs.json` and resumable `RESUME_OPEN_JOBS.json`).

**Still not a complete history.** Profile counts at first lookup were 3,762 / 4,858 / 19,982. Stored shares are about 20.9% / 15.1% / 32.9%, and those percentages are not a missing-post census. Key windows still open or never started:

- **@alexandr_wang:** 2012–2014 is not proven exhausted (one stored post). Open monthly windows: 2016-12, 2017-02, 2017-03, 2017-04. **115 pending months, 2017-05 through 2026-11**, were never opened. Years that still show exactly 25 posts are first-pass year-end samples.
- **@iiiinvest:** 2022-11 through 2024-02 and 2024-05 are marked exhausted. **2024-03 and 2024-04 are still open.** **30 pending months, 2024-06 through 2026-11**, were never opened.
- **@silverfang88:** 2021-09 through 2023-12 is largely exhausted, except **2023-09 pagination_stalled** (later duplicate token; earlier subwindow exhausted). Open: 2024-03, 2024-05 through 2024-09, and 2026-11-01to08. **26 pending windows from 2024-10 through 2026-11** were never opened. **2025 has 25 stored posts**, a thin year-end sample, not a quiet year.

[`vendor/finance-skills/`](vendor/finance-skills/) is the MIT copy of [himself65/finance-skills](https://github.com/himself65/finance-skills) at `a0850786e72aa23b92862f9f1635b0de506fe206`. Provenance: [`vendor/finance-skills.PROVENANCE.md`](vendor/finance-skills.PROVENANCE.md). Those files are stored only.

The first-pass zip SHA256 is `455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976`. The zip is not in this repository. Those 1,232 ids remain inside this expanded store.

```bash
python3 _tools/validate_archive.py
python3 -m unittest discover -s tests -v
```
