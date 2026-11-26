#!/usr/bin/env python3
"""Rebuild day3 archives, lite JSONL, coverage manifests, and collection_summary.

Uses literal '\\n' JSONL splits (not str.splitlines). Does not write day2
remaining-job or day2 validation files. Does not modify prior ZIP paths.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path("/workspace/x-research")
HANDLES = [
    "alexandr_wang",
    "iiiinvest",
    "silverfang88",
    "taresky",
    "thankUcrypto",
]
AUTHOR_IDS = {
    "alexandr_wang": "615818451",
    "iiiinvest": "1589763597705437184",
    "silverfang88": "1435990322702520320",
    "taresky": "368245720",
    "thankUcrypto": "705564530936418304",
}
SH = timezone(timedelta(hours=8))
PROFILE_COUNTS = {
    "alexandr_wang": 3762,
    "iiiinvest": 4858,
    "silverfang88": 19982,
    "taresky": 34003,
    "thankUcrypto": 8097,
}


def now_shanghai() -> str:
    return datetime.now(SH).isoformat()


def load_jsonl(path: Path) -> list[dict]:
    raw = path.read_bytes()
    parts = raw.split(b"\n")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [json.loads(x) for x in parts]


def post_text(p: dict) -> str:
    return p.get("full_text") or p.get("text") or ""


def _fence(text: str) -> str:
    if text is None:
        text = ""
    longest = 0
    run = 0
    for ch in text:
        if ch == "`":
            run += 1
            if run > longest:
                longest = run
        else:
            run = 0
    n = max(3, longest + 1)
    ticks = "`" * n
    return f"{ticks}\n{text}\n{ticks}"


def write_year_archive(handle: str, year: str, posts: list[dict]) -> Path:
    dest = ROOT / handle / "archives" / f"{year}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# @{handle} — {year} (UTC year)",
        "",
        f"{len(posts)} captured posts in this UTC year. Text is the stored `full_text` or `text`. This file is a reading copy, not an audited performance record.",
        "",
    ]
    for p in posts:
        pid = p.get("id")
        when = p.get("created_at_shanghai") or p.get("created_at_utc")
        url = p.get("canonical_url") or f"https://x.com/{handle}/status/{pid}"
        text = post_text(p)
        lines.append(f"## {pid}")
        lines.append("")
        lines.append(f"- time: {when}")
        lines.append(f"- url: {url}")
        lines.append(f"- type: {p.get('post_type')}")
        lines.append(f"- lang: {p.get('lang')}")
        lines.append("")
        lines.append(_fence(text))
        lines.append("")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dest


def write_chrono_index(handle: str, posts: list[dict]) -> Path:
    dest = ROOT / handle / "chronological_archive.md"
    lines = [
        f"# @{handle} chronological index",
        "",
        f"{len(posts)} captured posts, newest first by `created_at_utc`. Full text lives in `archives/<year>.md`.",
        "",
    ]
    for p in posts:
        pid = p.get("id")
        when = p.get("created_at_shanghai") or p.get("created_at_utc")
        url = p.get("canonical_url") or f"https://x.com/{handle}/status/{pid}"
        snippet = post_text(p).replace("\n", " ")[:160]
        lines.append(
            f"- `{pid}` | {when} | {p.get('post_type')} | {url} | {snippet}"
        )
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return dest


def write_lite(handle: str, posts: list[dict]) -> Path:
    dest = ROOT / handle / "normalized" / "posts_lite.jsonl"
    keys = [
        "id",
        "created_at_utc",
        "created_at_shanghai",
        "post_type",
        "lang",
        "canonical_url",
        "conversation_id",
        "public_metrics",
        "text",
    ]
    lines = []
    for p in posts:
        row = {k: p.get(k) for k in keys}
        row["text"] = post_text(p)
        lines.append(json.dumps(row, ensure_ascii=True, separators=(",", ":")))
    dest.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    return dest


def rebuild() -> dict:
    jobs = json.loads((ROOT / "logs" / "remaining_jobs_day3.json").read_text(encoding="utf-8"))
    packaged_at = now_shanghai()
    footer = jobs.get("authoritative_last_collection_footer")
    accounts_out = {}
    types_all = Counter()
    all_posts = {}
    year_tables = {}

    for handle in HANDLES:
        posts = load_jsonl(ROOT / handle / "normalized" / "posts.jsonl")
        posts.sort(key=lambda p: (p.get("created_at_utc") or "", p.get("id") or ""), reverse=True)
        all_posts[handle] = posts
        years = defaultdict(list)
        types = Counter()
        for p in posts:
            y = (p.get("created_at_utc") or "")[:4] or "unknown"
            years[y].append(p)
            types[p.get("post_type") or "unknown"] += 1
        types_all.update(types)
        year_tables[handle] = {y: len(years[y]) for y in sorted(years)}

        # drop stale year files then rewrite
        arch = ROOT / handle / "archives"
        arch.mkdir(parents=True, exist_ok=True)
        for old in arch.glob("*.md"):
            old.unlink()
        for y in sorted(years):
            write_year_archive(handle, y, years[y])
        write_chrono_index(handle, posts)
        write_lite(handle, posts)

        h_jobs = [j for j in jobs.get("all_jobs_snapshot", []) if j.get("handle") == handle]
        status_counts = Counter(j.get("status") for j in h_jobs)
        open_or_blocked = [
            j
            for j in (
                jobs.get("open_windows", [])
                + jobs.get("pending_windows", [])
                + jobs.get("do_not_start_overlapping_pending", [])
                + jobs.get("pagination_stalled_or_unproven", [])
                + jobs.get("deferred_overlapping_timeline_cursors", [])
                + jobs.get("next_priority_open_jobs", [])
            )
            if j.get("handle") == handle
        ]
        # unique by handle+label
        seen = set()
        uniq_ob = []
        for j in open_or_blocked:
            key = (j.get("handle"), j.get("label"), j.get("status"), j.get("next_token"))
            if key in seen:
                continue
            seen.add(key)
            uniq_ob.append(j)
        open_or_blocked = uniq_ob
        pending_labels = [
            j.get("label")
            for j in jobs.get("pending_windows", [])
            if j.get("handle") == handle
        ]
        cal = jobs.get("calendar_windows_with_no_job_yet", {}).get(handle) or []
        earliest = posts[-1] if posts else {}
        latest = posts[0] if posts else {}

        notes = [
            "Explicitly partial. Day3 collection stopped at the true 75-read daily reserve (usable 0). Not window exhaustion.",
            "Profile lookup lifetime counts are not missing-count proofs. Profiles were not refreshed on day3.",
            "Archives and this manifest were rebuilt from canonical normalized/posts.jsonl at day3 packaging.",
        ]
        if handle == "alexandr_wang":
            notes.append(
                "34 of 35 monthly jobs for 2024-01..2026-11 are exhausted. 2026-09 remains open after a 25-result Full-text pointer page (follow the saved next_token; do not treat as terminal). 2012-2014 remains not_proven_exhausted. 17 pre-creation placeholders are excluded, not missing posts. 2026-11 monthly bound ends 2026-11-25T00:00:00Z."
            )
        elif handle == "silverfang88":
            notes.append(
                "Never reuse stalled parents 2023-09 or 2026-07. Never open the blocked pending 2026-11 window. Other previously pending 2024–2026 monthly jobs walked on day3 are now exhausted as listed in remaining_jobs_day3.json."
            )
        elif handle == "iiiinvest":
            notes.append(
                "Never reuse stalled 2026-08 parent tokens. Previously pending 2024-06..12 and 2025-01..07 monthly jobs remain exhausted."
            )
        elif handle == "taresky":
            notes.append(
                "All 2023 and 2024 monthly jobs are exhausted. The timeline-recent cursor stays deferred (do not rewalk finished months). 131 calendar windows still have no job. Incremental 2026-11-25T00:35:00Z–2026-11-25T23:59:00Z is unstarted for all handles."
            )
        elif handle == "thankUcrypto":
            notes.append(
                "All 2023 monthly jobs remain exhausted. The timeline-recent cursor stays deferred. 79 calendar windows still have no job."
            )

        manifest = {
            "handle": handle,
            "user_id": AUTHOR_IDS[handle],
            "packaged_at_shanghai": packaged_at,
            "claim_all_tweets": False,
            "unique_posts_stored": len(posts),
            "profile_post_count_at_first_lookup": PROFILE_COUNTS[handle],
            "profile_not_refetched_day2": True,
            "profile_not_refetched_day3": True,
            "post_count_is_not_a_missing_count_proof": True,
            "span_utc": [earliest.get("created_at_utc"), latest.get("created_at_utc")],
            "span_shanghai": [
                earliest.get("created_at_shanghai"),
                latest.get("created_at_shanghai"),
            ],
            "years_utc": year_tables[handle],
            "types": dict(types),
            "earliest": {
                "id": earliest.get("id"),
                "created_at_utc": earliest.get("created_at_utc"),
                "created_at_shanghai": earliest.get("created_at_shanghai"),
            },
            "latest": {
                "id": latest.get("id"),
                "created_at_utc": latest.get("created_at_utc"),
                "created_at_shanghai": latest.get("created_at_shanghai"),
            },
            "expand_job_status_counts": dict(status_counts),
            "windows": h_jobs,
            "open_or_blocked_windows": open_or_blocked,
            "pending_window_labels": pending_labels,
            "calendar_windows_with_no_job_yet": cal,
            "coverage_notes": notes,
            "stopping_reason": "true_75_read_reserve_reached",
            "last_collection_footer": footer,
            "day3_added_vs_day2": len(posts)
            - {"silverfang88": 12862, "iiiinvest": 4712, "alexandr_wang": 1921, "taresky": 8551, "thankUcrypto": 6867}[handle],
        }
        (ROOT / handle / "coverage_manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        md = [
            f"# @{handle} coverage — day3 reserve close",
            "",
            f"Written {packaged_at} (Asia/Shanghai). **Explicitly partial.** {len(posts):,} unique posts. Profile lookup lifetime count {PROFILE_COUNTS[handle]:,} is not a missing-count proof. Profile not refreshed on day3.",
            "",
            f"Stored span: {earliest.get('created_at_shanghai')} → {latest.get('created_at_shanghai')}.",
            "",
            f"Types: {dict(types)}.",
            "",
            "## UTC year indexes",
            "",
            "| UTC year | Captured posts | Archive |",
            "|---|---:|---|",
        ]
        for y in sorted(year_tables[handle]):
            md.append(f"| {y} | {year_tables[handle][y]} | [full text](archives/{y}.md) |")
        md += [
            "",
            "## Exact open / blocked / deferred / stalled windows",
            "",
            "| Window | Status | start_time UTC | end_time UTC | Next token |",
            "|---|---|---|---|---|",
        ]
        for j in open_or_blocked:
            tok = j.get("next_token")
            tok_s = f"`{tok}`" if tok else "`None`"
            md.append(
                f"| {j.get('label')} | {j.get('status')} | `{j.get('start_time')}` | `{j.get('end_time')}` | {tok_s} |"
            )
        if not open_or_blocked:
            md.append("| _(none for this handle)_ | | | | |")
        if pending_labels:
            md.append("")
            md.append("Pending labels: " + ", ".join(pending_labels) + ".")
        if cal:
            md.append("")
            md.append(f"Calendar windows with no job yet: {len(cal)} (see JSON).")
        md.append("")
        md.append("## Notes")
        md.append("")
        for n in notes:
            md.append(f"- {n}")
        md.append("")
        md.append("Machine-readable companion: `coverage_manifest.json`. Remaining-job authority: `../logs/remaining_jobs_day3.json`.")
        md.append("")
        (ROOT / handle / "coverage_manifest.md").write_text("\n".join(md) + "\n", encoding="utf-8")

        accounts_out[handle] = {
            "unique_posts": len(posts),
            "years_utc": year_tables[handle],
            "types": dict(types),
            "span_shanghai": [
                earliest.get("created_at_shanghai"),
                latest.get("created_at_shanghai"),
            ],
            "profile_post_count_at_first_lookup": PROFILE_COUNTS[handle],
        }
        print(f"rebuilt {handle}: {len(posts)} posts, years={year_tables[handle]}")

    summary = {
        "packaged_at_shanghai": packaged_at,
        "pass": "day3-final-five-handles",
        "claim_complete_retrieval": False,
        "unique_total": sum(accounts_out[h]["unique_posts"] for h in HANDLES),
        "added_day3": sum(accounts_out[h]["unique_posts"] for h in HANDLES) - 34913,
        "added_since_day1": sum(accounts_out[h]["unique_posts"] for h in HANDLES) - 15370,
        "day3_calls_ingested": 925,
        "day2_unique_total": 34913,
        "day1_unique_total": 15370,
        "last_collection_footer": footer,
        "daily_remaining": 75,
        "reserve": 75,
        "usable_to_reserve": 0,
        "stopping_reason": "Real live 75-read reserve reached on 2026-11-26 09:31:16 GMT+8 Asia/Shanghai; explicitly partial, not all windows exhausted. Collection stopped; no new X reads in this packaging pass.",
        "daily_reset_shanghai": "2026-11-27 08:00 Asia/Shanghai",
        "remaining_jobs": "logs/remaining_jobs_day3.json",
        "day2_footer": "X reads left for this user: 22 of 30 this minute (resets at 2026-11-25T01:37:00.000Z), 75 of 1000 today (resets at 2026-11-26T00:00:00.000Z).",
        "day1_footer": "X reads left for this user: 23 of 30 this minute (resets at 2026-11-24T12:33:00.000Z), 61 of 1000 today (resets at 2026-11-25T00:00:00.000Z).",
        "accounts": accounts_out,
        "types": dict(types_all),
        "open_work_after_reset": {
            "open_dated": jobs.get("next_priority_open_jobs"),
            "deferred_timeline_recent": jobs.get("deferred_overlapping_timeline_cursors"),
            "unstarted_incremental": jobs.get("incremental_snapshot"),
            "blocked": jobs.get("do_not_start_overlapping_pending"),
            "stalled_or_unproven": jobs.get("pagination_stalled_or_unproven"),
            "job_counts": {
                "open_dated": 1,
                "deferred_timeline_recent": 2,
                "actionable_pending": 0,
                "blocked_sf_2026_11": 1,
                "exhausted": 360,
                "pagination_stalled": 3,
                "no_job_calendar_windows": 210,
                "excluded_precreation_wang_placeholders": 17,
            },
        },
    }
    (ROOT / "collection_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote collection_summary.json total", summary["unique_total"])
    return {"accounts": accounts_out, "total": summary["unique_total"], "packaged_at": packaged_at}


if __name__ == "__main__":
    rebuild()
