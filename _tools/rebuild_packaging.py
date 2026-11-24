#!/usr/bin/env python3
"""Rebuild manifests, chronological archives, collection summary, resume files."""
from __future__ import annotations

import json
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDLES = ["alexandr_wang", "iiiinvest", "silverfang88"]
PROFILE_COUNTS = {
    "alexandr_wang": {"user_id": "615818451", "post_count_at_lookup": 3762, "display": "Alexandr Wang"},
    "iiiinvest": {"user_id": "1589763597705437184", "post_count_at_lookup": 4858, "display": "电鱼哥"},
    "silverfang88": {"user_id": "1435990322702520320", "post_count_at_lookup": 19982, "display": "子时"},
}
SH = timezone(timedelta(hours=8))


def now_sh():
    return datetime.now(SH)


def load_posts(handle: str):
    path = ROOT / handle / "normalized" / "posts.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    rows.sort(key=lambda r: (r.get("created_at_utc") or "", r.get("id") or ""))
    return rows


def text_of(r):
    t = r.get("full_text") or r.get("text") or ""
    return t


def url_of(r, handle):
    return r.get("canonical_url") or f"https://x.com/{handle}/status/{r['id']}"


def metrics_line(r):
    m = r.get("public_metrics") or {}
    parts = []
    for k in ("like_count", "retweet_count", "repost_count", "reply_count", "quote_count", "impression_count", "bookmark_count"):
        if k in m and m[k] is not None:
            parts.append(f"{k.replace('_count','')}={m[k]}")
    return ", ".join(parts)


def load_jobs():
    return json.loads((ROOT / "logs" / "expand_jobs.json").read_text())


def job_table(jobs, handle):
    rows = [j for j in jobs if j["handle"] == handle]
    return rows


def md_escape_fence(s: str) -> str:
    return s.replace("```", "``\u200b`")


def write_archives(handle: str, posts: list):
    outdir = ROOT / handle / "archives"
    outdir.mkdir(exist_ok=True)
    # remove stale year files
    for p in outdir.glob("*.md"):
        p.unlink()
    by_year = defaultdict(list)
    for r in posts:
        y = (r.get("created_at_utc") or "unknown")[:4]
        by_year[y].append(r)
    year_index = []
    for y in sorted(by_year):
        ys = by_year[y]
        fpath = outdir / f"{y}.md"
        lines = [
            f"# @{handle} chronological archive — {y}",
            "",
            f"{len(ys)} stored posts in this year (deduplicated by id). Times are Asia/Shanghai (GMT+8) plus the API UTC timestamp. Full original-language text.",
            "",
        ]
        for r in ys:
            typ = r.get("post_type") or "unknown"
            lines.append(f"## {r.get('created_at_shanghai') or r.get('created_at_utc')} | {typ} | `{r['id']}`")
            lines.append(f"- UTC: `{r.get('created_at_utc')}`")
            lines.append(f"- URL: {url_of(r, handle)}")
            ml = metrics_line(r)
            if ml:
                lines.append(f"- Public metrics: {ml}")
            if r.get("conversation_id") and str(r.get("conversation_id")) != str(r["id"]):
                lines.append(f"- conversation_id: `{r.get('conversation_id')}`")
            lines.append("")
            lines.append("```")
            lines.append(md_escape_fence(text_of(r)))
            lines.append("```")
            lines.append("")
        fpath.write_text("\n".join(lines), encoding="utf-8")
        year_index.append((y, len(ys), str(fpath.relative_to(ROOT / handle))))
    # compact master archive: year stats + first/last + pointer
    types = Counter(r.get("post_type") or "unknown" for r in posts)
    years = Counter((r.get("created_at_utc") or "")[:4] for r in posts)
    first, last = posts[0], posts[-1]
    lines = [
        f"# @{handle} chronological archive",
        "",
        "This file is an **index**. Full original-language text for every stored post is in the yearly files under `archives/YYYY.md`.",
        "",
        f"- Unique posts stored (deduped by id): **{len(posts)}**",
        f"- Span (API UTC): `{first.get('created_at_utc')}` → `{last.get('created_at_utc')}`",
        f"- Span (Asia/Shanghai, GMT+8): {first.get('created_at_shanghai')} → {last.get('created_at_shanghai')}",
        f"- Types: " + ", ".join(f"{k} {types[k]}" for k in ["original", "reply", "quote", "repost"] if k in types),
        f"- Earliest stored: [{first['id']}]({url_of(first, handle)}) — {first.get('created_at_shanghai')}",
        f"- Latest stored: [{last['id']}]({url_of(last, handle)}) — {last.get('created_at_shanghai')}",
        "",
        "This is **not** a complete account history. See `coverage_manifest.md`.",
        "",
        "## Posts per calendar year (UTC year of created_at)",
        "",
        "| Year | Stored posts | Full-text file |",
        "|---|---:|---|",
    ]
    for y, n, rel in year_index:
        lines.append(f"| {y} | {n} | `{rel}` |")
    lines += [
        "",
        "## Compact chronological index (id, time, type, URL, first line)",
        "",
    ]
    for r in posts:
        first_line = (text_of(r).splitlines() or [""])[0][:180].replace("|", "\\|")
        lines.append(
            f"- `{r['id']}` | {r.get('created_at_shanghai')} | {r.get('post_type')} | {url_of(r, handle)} | {first_line}"
        )
    (ROOT / handle / "chronological_archive.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # lite jsonl already exists; refresh a compact lite
    lite_path = ROOT / handle / "normalized" / "posts_lite.jsonl"
    with lite_path.open("w", encoding="utf-8") as f:
        for r in posts:
            rec = {
                "id": r["id"],
                "created_at_utc": r.get("created_at_utc"),
                "created_at_shanghai": r.get("created_at_shanghai"),
                "post_type": r.get("post_type"),
                "lang": r.get("lang"),
                "canonical_url": url_of(r, handle),
                "conversation_id": r.get("conversation_id"),
                "public_metrics": r.get("public_metrics"),
                "text": text_of(r),
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return {
        "unique_posts": len(posts),
        "types": dict(types),
        "years": dict(sorted(years.items())),
        "first_id": first["id"],
        "first_utc": first.get("created_at_utc"),
        "first_shanghai": first.get("created_at_shanghai"),
        "first_url": url_of(first, handle),
        "last_id": last["id"],
        "last_utc": last.get("created_at_utc"),
        "last_shanghai": last.get("created_at_shanghai"),
        "last_url": url_of(last, handle),
    }


def write_manifest(handle, posts, stats, jobdoc, packed_at):
    jobs = job_table(jobdoc["jobs"], handle)
    by_status = Counter(j["status"] for j in jobs)
    open_jobs = [j for j in jobs if j["status"] in ("open", "pagination_stalled", "not_proven_exhausted")]
    exhausted = [j for j in jobs if j["status"] == "exhausted"]
    pending = [j for j in jobs if j["status"] == "pending"]

    notes = {
        "alexandr_wang": [
            "2012–2014 is `not_proven_exhausted`: a first-pass search from account creation through 2015-01-01 returned one post, and a later empty page was treated as exhausted, but the input token for that empty page was not saved. Do not treat this as proven silence or proven complete retrieval.",
            "2015-01 through 2016-11 and 2017-01 monthly windows were exhausted in the expand pass (many early-2015 months were empty or first-pass duplicates, with stored input tokens on later pages). 2016-12 and 2017-02/03/04 remain open with next_tokens.",
            "Most of 2017-05 through late 2026 monthly windows were never opened in the expand pass. Posts in those years often come from first-pass recency-biased year/quarter windows (typically ~25 posts near a year-end) plus recent timeline pages. Year counts that sit near 25 are a sampling artifact, not proof of low activity.",
        ],
        "iiiinvest": [
            "2022-11 was walked deeply (many pages) and is exhausted with stored later-page provenance. 2022-12 and 2023-01 through 2024-02 plus 2024-05 were exhausted; many of those later months added 0–few new posts because first-pass year-end samples already contained the only hits those first pages returned.",
            "2024-03 and 2024-04 are open: first pages were first-pass duplicates (`posts_added=0`) but still returned a next_token.",
            "2024-06 onward (including most of 2025–2026) remains pending. 2025–2026 posts in the store are mostly first-pass / recent-timeline samples, not monthly-exhausted coverage.",
        ],
        "silverfang88": [
            "2021-09 through 2023-12 is largely exhausted at monthly granularity, with one exception: original 2023-09 `pagination_stalled` (output token identical to input `b26v89c19zqg8o3fr5beqknfiduf3z8svkzzdfjkf2ttp` on a duplicate page spanning 2023-09-14T03:35:08Z–2023-09-15T05:50:57Z). The token was not reused. The earlier remainder was opened as `2023-09-01to14` (`end_time=2023-09-14T03:35:08Z`) and exhausted with stored provenance. Combined September 2023 coverage is therefore: stalled later segment plus exhausted earlier subwindow — not a clean monthly exhaustion.",
            "Some early 2021-09/10/11 exhaustions occurred before input-token provenance was added to the ingest path, so those exhaustions are weaker than later ones.",
            "2024-01, 2024-02, and 2024-04 are exhausted. 2024-03 and 2024-05 through 2024-09 remain open with next_tokens (2024-03 is the deepest open window, 10 pages / +248).",
            "2024-10 through most of 2025 and 2026 monthly windows were never opened, except an open slice `2026-11-01to08`. The stored 2025 count is only a thin first-pass year-end sample; do not interpret 2025 as a quiet year.",
        ],
    }

    manifest = {
        "handle": handle,
        "user_id": PROFILE_COUNTS[handle]["user_id"],
        "packaged_at_shanghai": packed_at,
        "unique_posts_stored": stats["unique_posts"],
        "profile_post_count_at_first_lookup": PROFILE_COUNTS[handle]["post_count_at_lookup"],
        "post_count_is_not_a_missing_count_proof": True,
        "span_utc": [stats["first_utc"], stats["last_utc"]],
        "span_shanghai": [stats["first_shanghai"], stats["last_shanghai"]],
        "types": stats["types"],
        "years_utc": stats["years"],
        "earliest": {"id": stats["first_id"], "utc": stats["first_utc"], "shanghai": stats["first_shanghai"], "url": stats["first_url"]},
        "latest": {"id": stats["last_id"], "utc": stats["last_utc"], "shanghai": stats["last_shanghai"], "url": stats["last_url"]},
        "expand_job_status_counts": dict(by_status),
        "windows": [
            {
                "label": j["label"],
                "query": j.get("query"),
                "start_time": j.get("start_time"),
                "end_time": j.get("end_time"),
                "status": j.get("status"),
                "pages_fetched": j.get("pages_fetched"),
                "posts_returned": j.get("posts_returned"),
                "posts_added": j.get("posts_added"),
                "next_token": j.get("next_token"),
                "last_input_token": j.get("last_input_token"),
                "last_span": j.get("last_span"),
            }
            for j in jobs
        ],
        "open_or_blocked_windows": [
            {
                "label": j["label"],
                "status": j["status"],
                "start_time": j.get("start_time"),
                "end_time": j.get("end_time"),
                "pages_fetched": j.get("pages_fetched"),
                "posts_added": j.get("posts_added"),
                "next_token": j.get("next_token"),
                "last_input_token": j.get("last_input_token"),
            }
            for j in open_jobs
        ],
        "pending_window_labels": [j["label"] for j in pending],
        "exhausted_window_labels": [j["label"] for j in exhausted],
        "coverage_notes": notes[handle],
        "stopping_reason": "Collection paused to prioritize evidence-grounded analysis and packaging. Daily X-read budget was not exhausted. Open and pending windows remain. This package is not a complete tweet archive.",
        "claim_all_tweets": False,
    }
    (ROOT / handle / "coverage_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def tok(t):
        return t if t else "—"

    md = [
        f"# Coverage manifest — @{handle}",
        "",
        f"**Packaged:** {packed_at} (Asia/Shanghai, GMT+8).",
        "",
        "This account folder is **not** a complete public history. Profile `post_count` is a platform lifetime figure, not proof that a remainder still exists or is retrievable.",
        "",
        "## Stored corpus (deduplicated by string id)",
        "",
        f"- Unique posts stored: **{stats['unique_posts']}**",
        f"- Profile `post_count` at first lookup (24 Nov 2026): {PROFILE_COUNTS[handle]['post_count_at_lookup']}",
        f"- Span (UTC): `{stats['first_utc']}` → `{stats['last_utc']}`",
        f"- Span (Asia/Shanghai, GMT+8): {stats['first_shanghai']} → {stats['last_shanghai']}",
        f"- Types: " + ", ".join(f"{k} {stats['types'].get(k,0)}" for k in ["original","reply","quote","repost"]),
        f"- Earliest stored: [{stats['first_id']}]({stats['first_url']})",
        f"- Latest stored: [{stats['last_id']}]({stats['last_url']})",
        "",
        "### Posts by UTC year",
        "",
        "| Year | Stored |",
        "|---|---:|",
    ]
    for y, n in stats["years"].items():
        md.append(f"| {y} | {n} |")
    md += [
        "",
        "## Expand-pass window status",
        "",
        f"Status counts: " + ", ".join(f"`{k}` {v}" for k, v in sorted(by_status.items())),
        "",
        "Expand pass used fresh monthly `search_posts_all` windows (`from:<handle>`, `sort_order=recency`, `max_results=25`). Later pages store query, window bounds, input token, and output `next_token`. If an output token equals the input token on a duplicate page, the window is marked `pagination_stalled` and is not reused; the earlier remainder is opened as a subwindow.",
        "",
        "### Open, stalled, or not-proven-exhausted windows (resumable)",
        "",
        "| Label | Status | start_time | end_time | pages | added | next_token | last_input_token |",
        "|---|---|---|---|---:|---:|---|---|",
    ]
    for j in open_jobs:
        md.append(
            f"| {j['label']} | {j['status']} | `{j.get('start_time')}` | `{j.get('end_time')}` | {j.get('pages_fetched')} | {j.get('posts_added')} | `{tok(j.get('next_token'))}` | `{tok(j.get('last_input_token'))}` |"
        )
    if pending:
        md += [
            "",
            f"### Pending first pages ({len(pending)} windows, not yet opened in the expand pass)",
            "",
            ", ".join(j["label"] for j in pending),
        ]
    md += [
        "",
        "### Exhausted monthly (or sub) windows",
        "",
        ", ".join(j["label"] for j in exhausted) or "(none)",
        "",
        "## Coverage caveats",
        "",
    ]
    for n in notes[handle]:
        md.append(f"- {n}")
    md += [
        "",
        "- First-pass year-end samples remain in the JSONL and can make unopened years look like they have ~25 posts clustered at the end of the year.",
        "- Deleted, withheld, protected, or otherwise inaccessible posts cannot be recovered.",
        "- Collection was paused to prioritize analysis and packaging; the daily read budget was not exhausted.",
        "",
        "Do **not** claim this folder contains all tweets.",
        "",
    ]
    (ROOT / handle / "coverage_manifest.md").write_text("\n".join(md), encoding="utf-8")
    return manifest


def main():
    packed_at = now_sh().strftime("%Y-%m-%d %H:%M:%S GMT+8")
    jobdoc = load_jobs()
    summary_accounts = {}
    all_stats = {}
    for handle in HANDLES:
        posts = load_posts(handle)
        stats = write_archives(handle, posts)
        all_stats[handle] = stats
        man = write_manifest(handle, posts, stats, jobdoc, packed_at)
        summary_accounts[handle] = {
            "unique_posts_stored": stats["unique_posts"],
            "types": stats["types"],
            "years_utc": stats["years"],
            "span_utc": [stats["first_utc"], stats["last_utc"]],
            "span_shanghai": [stats["first_shanghai"], stats["last_shanghai"]],
            "earliest": man["earliest"],
            "latest": man["latest"],
            "expand_job_status_counts": man["expand_job_status_counts"],
            "open_or_blocked_windows": man["open_or_blocked_windows"],
            "pending_window_count": len(man["pending_window_labels"]),
            "profile_post_count_at_first_lookup": man["profile_post_count_at_first_lookup"],
        }
        print(handle, stats["unique_posts"], stats["years"], stats["types"])

    resume = {
        "written_at_shanghai": packed_at,
        "daily_reset_utc": jobdoc.get("daily_reset_utc"),
        "daily_reset_shanghai": "2026-11-25 08:00:00 GMT+8",
        "reserve_target": jobdoc.get("reserve", 75),
        "expand_calls_this_pass": jobdoc.get("calls_this_pass"),
        "daily_reads_remaining_at_expand_probe": jobdoc.get("daily_reads_remaining_at_probe"),
        "remaining_budget_note": "Exact remaining daily reads must be read from the next live search_posts_all footer. Expand pass recorded 403 calls after a probe that showed 941 remaining of 1000. First-pass used on the order of ~58 reads, plus some 503s that may have counted. Collection was paused with a substantial unused remainder and a 75-call reserve still intended. Do not treat 941-403 as an exact remaining figure.",
        "open_jobs": [
            {
                "handle": j["handle"],
                "label": j["label"],
                "query": j.get("query"),
                "start_time": j.get("start_time"),
                "end_time": j.get("end_time"),
                "status": j["status"],
                "pages_fetched": j.get("pages_fetched"),
                "posts_added": j.get("posts_added"),
                "next_token": j.get("next_token"),
                "last_input_token": j.get("last_input_token"),
            }
            for j in jobdoc["jobs"]
            if j["status"] in ("open", "pagination_stalled", "not_proven_exhausted")
        ],
        "pending_by_handle": {
            h: [j["label"] for j in jobdoc["jobs"] if j["handle"] == h and j["status"] == "pending"]
            for h in HANDLES
        },
        "stall_note": "silverfang88 2023-09 pagination_stalled on token b26v89c19zqg8o3fr5beqknfiduf3z8svkzzdfjkf2ttp; do not reuse that token. Earlier subwindow 2023-09-01to14 is exhausted.",
    }
    (ROOT / "logs" / "RESUME_OPEN_JOBS.json").write_text(
        json.dumps(resume, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    summary = {
        "packaged_at_shanghai": packed_at,
        "pass": "expanded-plus-insights",
        "claim_complete_retrieval": False,
        "stopping_reason": "Parent/user instruction to prioritize rigorous insight and packaging over further crawl while time was tight. Daily X-read budget was not exhausted; open and pending windows remain in logs/RESUME_OPEN_JOBS.json and each coverage_manifest.",
        "tools": "Built-in x MCP public reads only (get_users_by_usernames, get_users_posts, search_posts_all, get_posts_by_ids).",
        "firstpass_zip": {
            "path": "/workspace/x-research-firstpass.zip",
            "sha256": "455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976",
            "immutable": True,
        },
        "accounts": summary_accounts,
        "expand_calls_this_pass": jobdoc.get("calls_this_pass"),
        "daily_reset_utc": jobdoc.get("daily_reset_utc"),
        "daily_reset_shanghai": "2026-11-25 08:00:00 GMT+8",
    }
    (ROOT / "collection_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    status = f"""# Expand + packaging status

**Written:** {packed_at} (Asia/Shanghai, GMT+8).

## Stopping reason

Collection was **paused**, not completed. The user follow-up asked for operating/decision frameworks and useful trader insight, and the parent instruction was: if budget/time is tight, prioritize rigorous insight and packaging over endless crawl. Daily X-read budget was **not** exhausted. A later pass can resume from `logs/RESUME_OPEN_JOBS.json` and `logs/expand_jobs.json`.

Do **not** claim all tweets were retrieved. Profile `post_count` is not a missing-count proof.

## Unique posts stored (deduped by id)

| Handle | Stored | Span (Asia/Shanghai, GMT+8) | original / reply / quote / repost |
|---|---:|---|---|
"""
    for h in HANDLES:
        s = all_stats[h]
        t = s["types"]
        status += (
            f"| @{h} | {s['unique_posts']} | {s['first_shanghai']} → {s['last_shanghai']} | "
            f"{t.get('original',0)} / {t.get('reply',0)} / {t.get('quote',0)} / {t.get('repost',0)} |\n"
        )
    status += f"""
Year breakdowns and open tokens are in each account's `coverage_manifest.md` / `.json`.

## Budget

- Expand-pass calls recorded in `expand_jobs.json`: {jobdoc.get('calls_this_pass')}
- Daily remaining at the expand probe (early in the pass): {jobdoc.get('daily_reads_remaining_at_probe')} of 1000
- Daily reset: `2026-11-25T00:00:00.000Z` = **2026-11-25 08:00:00 GMT+8** (Asia/Shanghai)
- Intended reserve: 75 reads
- Exact remaining at packaging time was **not** re-probed; use the next live tool footer.

## Immutable first-pass zip

`/workspace/x-research-firstpass.zip` SHA256 `455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976` — do not modify.
"""
    (ROOT / "logs" / "EXPAND_STATUS.md").write_text(status, encoding="utf-8")
    print("packaged_at", packed_at)


if __name__ == "__main__":
    main()
