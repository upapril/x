# Methodology — day2 reserve close, explicitly partial

## Scope and evidentiary boundary

Five public accounts: @silverfang88, @iiiinvest, @alexandr_wang, @taresky, @thankUcrypto. Day2 is25 Nov2026, Asia/Shanghai (GMT+8), continuing the immutable15,370-ID day1 baseline. **34,913 unique IDs** are now stored; **19,543 added**. No account is claimed complete. Profile lifetime `post_count` figures are day1 lookups, not fresh day2 metrics and not proof a computable missing remainder exists.

A captured post supports the literal text/attribution in the captured response, not every underlying market fact, performance claim, legal assertion or accusation. Analyses are selective evidence-led synthesis, not a manual reread of all34,913 posts. “New” means added versus day1 ZIP, not necessarily recently authored. Distinct IDs with identical text remain distinct. Reposts, replies and expanded referenced writers retain separate attribution. No private legal-name inference.

## Tools and collection recipe

Only shared public `x` tools. Day2 collection used `x.search_posts_all`, `write_to_file:true`, followed by disk ingestion. No browser, user-X session, bearer token, alternative scrape, messages, purchases or GitHub writes. No profile recheck or Meta web refetch was spent onday2.

- Query: `from:<handle>`.
- Each existing job's exact `start_time`, `end_time`, `next_token` is reused unchanged; pending first pages omit token.
- `max_results:25`, `sort_order:recency`.
- `post.fields`: `created_at,public_metrics,note_post,entities,attachments,lang,conversation_id`.
- `expansions`: `author_id,referenced_posts,in_reply_to_user_id`.
- At most30reads/minute,1,000/day; live footers, not arithmetic from stale snapshots, control the stop. Across parallel batches the lowest daily remainder is authoritative.
- `python3 _tools/checkpoint_batch.py handle:ASSET_FILENAME.txt:window_label ...` ingests downloaded responses and advances only their corresponding jobs. It follows saved Full-text pointers for truncated tool-output wrappers. Every fetched response was ingested before finalization; none remain pending.
- Follow a new token even after a small nonempty page; do not assume fewer than25 is terminal. A no-token terminal result ends that saved window. Same-token duplicate stalls are recorded and never retried. Errors do not establish exhaustion. Parent stalls and exhausted children are not reopened.

## Exact day2 stop and budget

Collection reached the real75-read reserve at **25 Nov2026 09:36:46 Asia/Shanghai** (last verified footer; no subsequent X reads in finalization). **924 day2 collection calls ingested**, in addition to the earlier probe that left999. No claim of all-window exhaustion.

```
X reads left for this user: 22 of 30 this minute (resets at 2026-11-25T01:37:00.000Z), 75 of 1000 today (resets at 2026-11-26T00:00:00.000Z).
```

Footer minute reset: **25 Nov2026 09:37 Asia/Shanghai**. Daily reset: **26 Nov2026 08:00 Asia/Shanghai**. Remaining75, usable to reserve0. This is a budget stop, not a context checkpoint. Other tasks may share the quota; the next run must read live authority rather than assume these historical75 remain. No new routine was created here; the prior routine fired/deleted itself.

## Day1 footer retained exactly (historical, not current authority)

```
X reads left for this user: 23 of 30 this minute (resets at 2026-11-24T12:33:00.000Z), 61 of 1000 today (resets at 2026-11-25T00:00:00.000Z).
```

Minute reset:24 Nov2026 **20:33 Asia/Shanghai**; daily reset:25 Nov2026 **08:00 Asia/Shanghai**. Day1 relaxed its reserve for22 initial reads covering the two added accounts and stopped at61. Those61 are not carried into day2's fresh1,000-read day.

## Reproducible unfinished-job manifest for26 Nov2026 08:00 Asia/Shanghai

**Frozen package authority:** `logs/DAY2_FINAL_REMAINING_JOBS.json`. It contains every exact open query/bound/token, pending first-page window, terminal job, blocked parent token, and calendar month with no job. **Live continuation authority:** `logs/remaining_jobs_day2.json` + `logs/expand_jobs.json`; `RESUME_OPEN_JOBS.json` is a convenience copy, `NEXT_FIRE.json` is not a scheduled routine. The day1 manifest is historical only.

Counts:11 open dated windows plus2 overlapping recent-timeline cursors (defer);93 actionable pending jobs;210 no-job calendar months (TA131,THANK79). Three stalled parents and one unprovenWang2012–2014 bucket are not safe token-resume jobs. A94th pending label,SF2026-Nov, overlaps terminal children and is blocked.17 inherited pre-creationWang calendar placeholders were moved into `excluded_precreation_calendar_windows`; no post was removed and no extra read is warranted there.

### Open dated windows (UTC bounds are exact API arguments)

| Handle | Label | start_time UTC | end_time UTC | Exact next_token |
|---|---|---|---|---|
| silverfang88 | 2024-03 | `2024-03-01T00:00:00Z` | `2024-04-01T00:00:00Z` | `b26v89c19zqg8o3fr5tenupng9quli5mpc13gghztaid9` |
| silverfang88 | 2024-06 | `2024-06-01T00:00:00Z` | `2024-07-01T00:00:00Z` | `b26v89c19zqg8o3fr62eek5f4qrff1ul9ltd7re7e1u9p` |
| silverfang88 | 2024-07 | `2024-07-01T00:00:00Z` | `2024-08-01T00:00:00Z` | `b26v89c19zqg8o3frqlvljape4hxiaccagk4pjjh0wu4d` |
| silverfang88 | 2024-08 | `2024-08-01T00:00:00Z` | `2024-09-01T00:00:00Z` | `b26v89c19zqg8o3frqrrrru86cwk00i1t1o3gbb3xtnjx` |
| silverfang88 | 2024-09 | `2024-09-01T00:00:00Z` | `2024-10-01T00:00:00Z` | `b26v89c19zqg8o3frqut8grgysui3mzlnxqnlyzly9da5` |
| taresky | 2024-09 | `2024-09-01T00:00:00Z` | `2024-10-01T00:00:00Z` | `b26v89c19zqg8o3frqut8rdwre6omn2yqnku6qzsio9rx` |
| taresky | 2024-10 | `2024-10-01T00:00:00Z` | `2024-11-01T00:00:00Z` | `b26v89c19zqg8o3frqxtuwhnof5dyuwak0sfs5h3drs71` |
| taresky | 2024-11 | `2024-11-01T00:00:00Z` | `2024-12-01T00:00:00Z` | `b26v89c19zqg8o3frr0rxtbbubn41jahj0tbk73i5x56l` |
| thankUcrypto | 2025-03 | `2025-03-01T00:00:00Z` | `2025-04-01T00:00:00Z` | `b26v89c19zqg8o3frrct5kdpolkj1rt23tb7zodjxpy7x` |
| thankUcrypto | 2024-04 | `2024-04-01T00:00:00Z` | `2024-05-01T00:00:00Z` | `b26v89c19zqg8o3fr5wef7lsykbep4ns28qkoya4wln5p` |
| thankUcrypto | 2024-07 | `2024-07-01T00:00:00Z` | `2024-08-01T00:00:00Z` | `b26v89c19zqg8o3frqos08le9855ejt2s6c935r547rst` |

After reset, first finish thankUcrypto2025-March and current new-account historical cursors; finish short SFJune/August tails and other savedSF2024 cursors; then pending recent months and all remaining calendar gaps by value. Wang2016Dec/2017 and original2018Jan–Oct/2019Aug priority tails are terminal. SF2025May–July andIII2026July/September/Aug01–27 are terminal. Do not spend reads rechecking stored profiles or rewalking overlapping timeline-recent tokens. Never reuse a stalled parent or exhausted window.

A separate **unstarted proposed incremental** window is recorded for each handle: `2026-11-25T00:35:00Z` → `2026-11-25T23:59:00Z`, i.e.25 Nov08:35 →26 Nov07:59 Asia/Shanghai. It has a60s buffer before08:00 and is **not captured yet**. Use the fixed endpoint as the next high-water mark if collected; no silent gap. The preceding fixed incremental `2026-11-24T12:00:00Z` → `2026-11-25T00:35:00Z` is terminal for all five: TA/THANK final tails batch44; SF final tail batch77; III/Wang earlier. Do not reopen it. Every unstarted job remains explicitly unstarted until a response is ingested.

## Text preservation, JSONL and archives

Canonical full records are `*/normalized/posts.jsonl`; IDs are strings. Full/liteJSONL are emitted with `ensure_ascii=True`, escaping controls and Unicode losslessly. Records are split on literalLF (`'\n'`), **not** `splitlines()`; U+2028 inside text is legal content and must not become a record delimiter. `json.loads` validates each physical line. Original `text`, long-form `full_text`, expanded references and raw pages are retained; linked articles/media are not claimed fully retrieved.

Each post's `collection` gives its raw response provenance. All cited top-level author IDs match their folder; a quoted writer is not relabeled. Each account has a day1 profile snapshot and provenance file; the two added profiles' named raw lookup response is included where available. The original-three normalized profile captures are retained; no missing original lookup response is invented.

Yearly Markdown uses dynamic backtick fences long enough to preserve embedded fences **without altering the post's literal text**. UTC year partitions are labeled; human times include Asia/Shanghai. Full archives, compact chronological indexes, liteJSONL, per-account manifests and root counts were rebuilt atday2 close. JSONL/raw files remain the authoritative machine-readable text if a Markdown renderer treats content differently.

### Audited inherited corrections only

`logs/day2_literal_corrections.json` documents:
- SFpost `2110119596435054716`: restore captured literalU+2028 in `text` where the inherited day1 normalized record hadLF; no wording change.
- Three inherited pinned-post relative provenance paths: `../../_raw/...` → `../_raw/...`.

Every day1 ID is retained; all other inherited record fields remain semantically unchanged. Prior ZIPs were not edited. Day1 control-character repair history remains in historical methodology; current validation compares decoded text to captured raw and the immutable baseline, allowing only these audited corrections.

## Validation and reproducibility

- `python3 _tools/validate_data_checkpoint.py`: strict JSONL, string-ID dedup, author checks, literal raw text/provenance, baseline ID retention and audited delta check.
- `python3 _tools/write_day2_analysis.py`: writes five analyses with literal substring assertions and source/author/date ledger.
- `python3 _tools/rebuild_day2_artifacts.py`: rebuilds archives/year indexes/liteJSONL/manifests from canonical records and live job state. It requires the saved75-read reserve state and performs no network reads.
- `logs/day2_package_validation.json`: global/per-account ID counts, lite/full equivalence, archives, citation URLs/text and immutable priorZIP hashes; exact on-disk file hashes in `FILE_SHA256SUMS.json`.
- NEW artifact stem `/workspace/x-research-day2-final`; if split, independently extractable numbered ZIPs are each below25,000,000bytes. Extract all to the same destination. EveryZIP is CRC-tested and every packaged file is SHA256-compared to disk. Exclude `*.bak*`, `__pycache__`, `.pyc`; priorZIPs remain outside this tree.

## Significant Meta facts and unresolved audit

Only the literal sourced wording already captured in `public_sources_wang.md` and the actual stored X records is used. No Meta-page read, signatory-list check, compute-allocation audit or product-launch audit occurred onday2. The inherited Meta leadership-page note is explicitly attributed and dated, not a newly validated fact. Do not derive “first-ever” or aJune start from the1Jul2025 title tweet or the12JunScale announcement. Cloud audit of the original captured source remains outstanding. Quoting a leadership claim proves attribution, not implementation.

## Prior immutable artifacts / integration boundary

`x-research-day1-final.zip` SHA256 `537597c2d1c295f18773fb2099d751338f78a354be982b65a26aaf7367efea37`; three olderZIP hashes remain inREADME and the validation report. Day1 historical narratives are preserved but not current coverage authority.

No GitHub writes from this work. Parent already mergedPR1 into main `fb75058962f33f1c176f0297e47eb4cfde74d929`; future integration requires a **NEW PR from main**, not updates to the mergedPR and not an authorized future merge.
