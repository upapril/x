#!/usr/bin/env python3
"""Validate the expanded local X archive.

Reads only files in this repository. Does not call the X API.
Post ids are compared as strings. Human timestamps are Asia/Shanghai,
labeled GMT+8. Machine timestamps stay UTC.

The archive is still incomplete. claim_all_tweets must stay false.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HANDLES = ("alexandr_wang", "iiiinvest", "silverfang88")
EXPECTED_POSTS = {"alexandr_wang": 788, "iiiinvest": 736, "silverfang88": 6576}
SHANGHAI = ZoneInfo("Asia/Shanghai")
STATUS_RE = re.compile(r"https://x\.com/(?:[A-Za-z0-9_]+/status|i/status)/(\d+)")
YEAR_ROW_RE = re.compile(r"^\|\s*(\d{4})\s*\|\s*(\d+)\s*\|")

# Substrings that must occur in the stored text or full_text.
REQUIRED_TEXT = (
    ("alexandr_wang", "809663723006611456", "Just hit 200 registered users on @scaleAPI Slack group!"),
    ("alexandr_wang", "1334171701001678848", "Surround yourself with the BEST people"),
    ("alexandr_wang", "1334171701844746240", "Authenticity"),
    ("alexandr_wang", "1607219151059423234", "10s of millions of people will die"),
    ("alexandr_wang", "216361960667754498", "I love Dropbox"),
    ("alexandr_wang", "1939867404252979291", "Chief AI Officer of @Meta"),
    ("alexandr_wang", "2124719968499777546", "this path is not inevitable"),
    ("iiiinvest", "2110022220131226106", "建群了（免费）"),
    ("iiiinvest", "2125158673203048455", "按照计划越跌越买"),
    ("iiiinvest", "2037361082038362440", "越跌越补"),
    ("silverfang88", "1441624264130453510", "my egg is spectacular"),
    ("silverfang88", "1443403746990440455", "NFT is going into a bull market"),
    ("silverfang88", "1437303812616720389", "RT @GoGalaGames"),
    ("silverfang88", "1609058637267492865", "起点的热门小说我基本都看完了"),
    ("silverfang88", "1609058637267492865", "提笔想写一个一年的总结"),
    ("silverfang88", "2109440726865985560", "这场AI游戏至少还要持续一年以上"),
    ("silverfang88", "1740688880007831938", "永远只玩下一个新的故事"),
)

# First-pass ids that the expanded store must still contain.
RETAINED_IDS = (
    "809663723006611456",
    "216361960667754498",
    "1334171701844746240",
    "1441624264130453510",
    "1443403746990440455",
    "1609058637267492865",
    "2110022220131226106",
    "2121172719681294532",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def shanghai_label(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S GMT+8")


def status_ids(text: str) -> list[str]:
    return STATUS_RE.findall(text)


def body(post: dict) -> str:
    return (post.get("text") or "") + "\n" + (post.get("full_text") or "")


def parse_year_table(md: str) -> dict[str, int]:
    lines = md.splitlines()
    start = None
    for i, line in enumerate(lines):
        if "Posts by UTC year" in line or line.strip() == "## Counts by year":
            start = i
            break
    if start is None:
        return {}
    years = {}
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        match = YEAR_ROW_RE.match(line.strip())
        if match:
            years[match.group(1)] = int(match.group(2))
    return years


def windows_of(manifest: dict) -> list[dict]:
    windows = manifest.get("windows") or []
    if isinstance(windows, dict):
        return list(windows.values())
    return list(windows)


def validate(root: Path | None = None) -> dict:
    root = root or repo_root()
    errors: list[str] = []
    summary: dict = {"handles": {}, "total_posts": 0, "completeness_claim": False, "pagination_verified_complete": False}
    by_all: dict[str, tuple[str, dict]] = {}

    pinned_path = root / "_raw" / "pinned_posts_get_posts_by_ids.json"
    pinned_ids: set[str] = set()
    if not pinned_path.exists():
        errors.append("missing _raw/pinned_posts_get_posts_by_ids.json")
    else:
        pinned = json.loads(pinned_path.read_text(encoding="utf-8"))
        for item in pinned.get("data") or []:
            pinned_ids.add(str(item.get("id")))

    profiles = json.loads((root / "profiles.json").read_text(encoding="utf-8"))
    accounts = profiles.get("accounts") or {}
    collection = json.loads((root / "collection_summary.json").read_text(encoding="utf-8"))
    if collection.get("claim_complete_retrieval") is not False:
        errors.append("collection_summary.json claim_complete_retrieval is not false")

    for handle in HANDLES:
        hdir = root / handle
        posts = load_jsonl(hdir / "normalized" / "posts.jsonl")
        lite = load_jsonl(hdir / "normalized" / "posts_lite.jsonl")
        manifest = json.loads((hdir / "coverage_manifest.json").read_text(encoding="utf-8"))
        ids = [p.get("id") for p in posts]
        id_set = set(ids)
        if len(ids) != len(id_set):
            errors.append(f"{handle}: duplicate ids")
        if len(posts) != EXPECTED_POSTS[handle]:
            errors.append(f"{handle}: count {len(posts)} != {EXPECTED_POSTS[handle]}")
        if any(not isinstance(i, str) for i in ids):
            errors.append(f"{handle}: non-string id")
        keys = [(p.get("created_at_utc") or "", p.get("id") or "") for p in posts]
        if keys != sorted(keys, reverse=True):
            errors.append(f"{handle}: posts.jsonl is not newest-first by (created_at_utc, id)")
        if {p.get("id") for p in lite} != id_set:
            errors.append(f"{handle}: posts_lite id set differs")

        by_year: Counter[str] = Counter()
        by_type: Counter[str] = Counter()
        by_id = {p["id"]: p for p in posts}
        for p in posts:
            created = p.get("created_at_utc")
            if not created:
                errors.append(f"{handle}: missing created_at_utc {p.get('id')}")
                continue
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            by_year[str(dt.year)] += 1
            by_type[p.get("post_type")] += 1
            expected = shanghai_label(created)
            if p.get("created_at_shanghai") != expected:
                errors.append(f"{handle}: {p.get('id')} shanghai label mismatch")
            url = p.get("canonical_url") or ""
            if not str(url).startswith("https://x.com/") or str(p.get("id")) not in str(url):
                errors.append(f"{handle}: bad canonical_url {p.get('id')}")
            profile = accounts.get(handle) or {}
            if profile.get("id") and p.get("author_id") != str(profile["id"]):
                errors.append(f"{handle}: author_id mismatch {p.get('id')}")
            by_all[p["id"]] = (handle, p)

        if manifest.get("claim_all_tweets") is not False:
            errors.append(f"{handle}: claim_all_tweets is not false")
        if manifest.get("unique_posts_stored") != len(posts):
            errors.append(f"{handle}: manifest unique_posts_stored != {len(posts)}")
        if {str(k): int(v) for k, v in (manifest.get("years_utc") or {}).items()} != dict(by_year):
            errors.append(f"{handle}: years_utc != posts")
        if manifest.get("types") != dict(by_type):
            errors.append(f"{handle}: types != posts")
        span = manifest.get("span_utc") or []
        chronological = sorted(posts, key=lambda p: (p.get("created_at_utc") or "", p.get("id") or ""))
        if chronological:
            if list(span) != [chronological[0]["created_at_utc"], chronological[-1]["created_at_utc"]]:
                errors.append(f"{handle}: span_utc mismatch")
            shanghai_span = list(manifest.get("span_shanghai") or [])
            if shanghai_span != [chronological[0]["created_at_shanghai"], chronological[-1]["created_at_shanghai"]]:
                errors.append(f"{handle}: span_shanghai mismatch")

        windows = windows_of(manifest)
        counts = Counter(w.get("status") for w in windows)
        declared = manifest.get("expand_job_status_counts") or {}
        if dict(counts) != {k: int(v) for k, v in declared.items()}:
            errors.append(f"{handle}: window status counts {dict(counts)} != {declared}")
        pending = [w.get("label") for w in windows if w.get("status") == "pending"]
        exhausted = [w.get("label") for w in windows if w.get("status") == "exhausted"]
        if pending != manifest.get("pending_window_labels"):
            errors.append(f"{handle}: pending_window_labels != windows")
        if exhausted != manifest.get("exhausted_window_labels"):
            errors.append(f"{handle}: exhausted_window_labels != windows")
        blocked = [w.get("label") for w in windows if w.get("status") in {"open", "pagination_stalled", "not_proven_exhausted"}]
        listed = [w.get("label") for w in (manifest.get("open_or_blocked_windows") or [])]
        if blocked != listed:
            errors.append(f"{handle}: open_or_blocked_windows != open/stalled/unproven windows")
        for w in windows:
            status = w.get("status")
            if status in {"open", "pagination_stalled"} and not w.get("next_token"):
                errors.append(f"{handle}: {w.get('label')} is {status} without next_token")
            if status == "pagination_stalled" and w.get("next_token") != w.get("last_input_token"):
                errors.append(f"{handle}: stalled window {w.get('label')} token != input")
            if status == "pending" and int(w.get("pages_fetched") or 0) != 0:
                errors.append(f"{handle}: pending window {w.get('label')} has pages")

        md_years = parse_year_table((hdir / "coverage_manifest.md").read_text(encoding="utf-8"))
        if md_years != {k: int(v) for k, v in by_year.items()}:
            errors.append(f"{handle}: coverage markdown year table != posts")
        if "not" not in (hdir / "coverage_manifest.md").read_text(encoding="utf-8").lower() or "all tweets" not in (hdir / "coverage_manifest.md").read_text(encoding="utf-8"):
            errors.append(f"{handle}: coverage markdown does not deny all-tweets")

        year_ids: list[str] = []
        seen_years: set[str] = set()
        for path in sorted((hdir / "archives").glob("*.md")):
            year = path.stem
            file_ids = status_ids(path.read_text(encoding="utf-8"))
            if len(file_ids) != len(set(file_ids)):
                errors.append(f"{handle}: duplicate ids in archives/{year}.md")
            times = []
            for pid in file_ids:
                post = by_id.get(pid)
                if not post:
                    errors.append(f"{handle}: archives/{year}.md cites missing {pid}")
                    continue
                if not post["created_at_utc"].startswith(year):
                    errors.append(f"{handle}: {pid} is in archives/{year}.md but UTC year differs")
                times.append(post["created_at_utc"])
            if times != sorted(times):
                errors.append(f"{handle}: archives/{year}.md is not oldest-to-newest")
            year_ids.extend(file_ids)
            seen_years.add(year)
        if set(year_ids) != id_set:
            errors.append(f"{handle}: yearly archives cover {len(set(year_ids))} ids, posts {len(id_set)}")
        if seen_years != set(by_year):
            errors.append(f"{handle}: archive years {sorted(seen_years)} != post years")

        chrono = (hdir / "chronological_archive.md").read_text(encoding="utf-8")
        marker = "## Compact chronological index"
        if marker not in chrono:
            errors.append(f"{handle}: chronological archive has no compact index")
        else:
            index_ids = status_ids(chrono.split(marker, 1)[1])
            if index_ids != list(dict.fromkeys(index_ids)):
                errors.append(f"{handle}: compact index repeats an id")
            if set(index_ids) != id_set:
                errors.append(f"{handle}: compact index is not the full id set")
            times = [by_id[i]["created_at_utc"] for i in index_ids if i in by_id]
            if times != sorted(times):
                errors.append(f"{handle}: compact index is not oldest-to-newest")

        for name in ("analysis.md", "coverage_manifest.md"):
            missing = [i for i in status_ids((hdir / name).read_text(encoding="utf-8")) if i not in id_set]
            if missing:
                errors.append(f"{handle}: {name} cites missing ids {missing[:8]}")

        raw_ids: set[str] = set()
        request_pages = 0
        for path in (hdir / "raw").glob("page_*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            for item in payload.get("data") or []:
                raw_ids.add(str(item.get("id")))
            request = payload.get("request") or {}
            if request:
                request_pages += 1
                query = request.get("query") or ""
                if not str(query).startswith(f"from:{handle}"):
                    errors.append(f"{handle}: {path.name} query is not from:{handle}")
                if request.get("input_token") not in (None, "") and not isinstance(request.get("input_token"), str):
                    errors.append(f"{handle}: {path.name} input_token is not a string")
                for key in ("start_time", "end_time", "window_label"):
                    if not request.get(key):
                        errors.append(f"{handle}: {path.name} request missing {key}")
        if id_set - raw_ids - pinned_ids:
            errors.append(f"{handle}: posts missing from raw pages and pinned file")
        if request_pages == 0:
            errors.append(f"{handle}: no raw page stored a query/window request")

        summary["handles"][handle] = {
            "posts": len(posts),
            "profile_post_count": manifest.get("profile_post_count_at_first_lookup"),
            "span_utc": span,
            "by_type": dict(by_type),
            "pending_windows": len(pending),
            "open_or_blocked_windows": len(blocked),
            "request_pages": request_pages,
            "completeness_claim": False,
        }
        summary["total_posts"] += len(posts)

    for handle, pid, needle in REQUIRED_TEXT:
        pair = by_all.get(pid)
        if not pair or pair[0] != handle:
            errors.append(f"required post missing {handle} {pid}")
            continue
        if needle not in body(pair[1]):
            errors.append(f"{handle} {pid} missing text {needle!r}")

    for pid in RETAINED_IDS:
        if pid not in by_all:
            errors.append(f"first-pass id dropped: {pid}")

    wang_analysis = (root / "alexandr_wang" / "analysis.md").read_text(encoding="utf-8")
    if "status/809675263590961152" in wang_analysis:
        errors.append("analysis still links the absent Slack id 809675263590961152")
    if "809675263590961152" in wang_analysis and "absent" not in wang_analysis:
        errors.append("analysis mentions the absent Slack id without saying it is absent")
    sources = (root / "public_sources_wang.md").read_text(encoding="utf-8")
    if "does **not** contain" not in sources or "June 2025" not in sources:
        errors.append("public_sources_wang.md does not record the Meta HTML limit")
    insights = (root / "INSIGHTS.md").read_text(encoding="utf-8")
    if "first CAIO" in insights:
        errors.append("INSIGHTS.md still calls Wang the first CAIO")
    comparison = root / "FINANCE_SKILLS_COMPARISON.md"
    if not comparison.exists():
        errors.append("missing FINANCE_SKILLS_COMPARISON.md")
    else:
        text = comparison.read_text(encoding="utf-8")
        if "Never average down" not in text or "越跌越买" not in text:
            errors.append("comparison does not keep the average-down conflict explicit")
        if "8,100" not in text:
            errors.append("comparison does not state the expanded total")
    for name in ("INSIGHTS.md", "METHODOLOGY.md", "public_sources_wang.md", "FINANCE_SKILLS_COMPARISON.md", "README.md"):
        missing = [i for i in status_ids((root / name).read_text(encoding="utf-8")) if i not in by_all]
        if missing:
            errors.append(f"{name} cites missing ids {missing[:8]}")

    if summary["total_posts"] != 8100:
        errors.append(f"total posts {summary['total_posts']} != 8100")
    return {"ok": not errors, "error_count": len(errors), "errors": errors, "summary": summary}


def main() -> int:
    report = validate()
    print(json.dumps({"ok": report["ok"], "error_count": report["error_count"], "errors": report["errors"], "summary": report["summary"]}, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
