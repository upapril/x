#!/usr/bin/env python3
"""Validate the local first-pass X archive.

Reads only files in this repository. Does not call the X API.
Post ids are compared as strings. Human timestamps are Asia/Shanghai,
labeled GMT+8. Machine timestamps stay UTC.

Exit status is 0 when every check passes.
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
SHANGHAI = ZoneInfo("Asia/Shanghai")
STATUS_RE = re.compile(r"https://x\.com/(?:[A-Za-z0-9_]+/status|i/status)/(\d+)")
YEAR_ROW_RE = re.compile(r"^\|\s*(\d{4})\s*\|\s*(\d+)\s*\|$")

# Substrings that must occur in the stored text or full_text of that id.
REQUIRED_TEXT = (
    ("alexandr_wang", "809663723006611456", "Just hit 200 registered users on @scaleAPI Slack group!"),
    ("alexandr_wang", "1334171701001678848", "Surround yourself with the BEST people"),
    ("alexandr_wang", "1334171701844746240", "Authenticity"),
    ("alexandr_wang", "1607219151059423234", "10s of millions of people will die"),
    ("alexandr_wang", "216361960667754498", "I love Dropbox"),
    ("alexandr_wang", "941450889809686528", "Stanford Vision Lab"),
    ("alexandr_wang", "1939867404252979291", "Chief AI Officer of @Meta"),
    ("iiiinvest", "1596860542853218305", "太多机器人"),
    ("iiiinvest", "1597031098667921408", "万事勇为先，第一步很重要"),
    ("iiiinvest", "1597088511764488192", "世事无常"),
    ("iiiinvest", "2110022220131226106", "建群了（免费）"),
    ("iiiinvest", "2121172719681294532", "收益率800%"),
    ("silverfang88", "1441624264130453510", "my egg is spectacular"),
    ("silverfang88", "1443403746990440455", "NFT is going into a bull market"),
    ("silverfang88", "1443399130676559880", "cool that is a brilliant video"),
    ("silverfang88", "1609058637267492865", "提笔想写一个一年的总结"),
    ("silverfang88", "1609058637267492865", "起点的热门小说我基本都看完了"),
    ("silverfang88", "2038551302037217291", "Vintage"),
    ("silverfang88", "2038551302037217291", "时来天地皆同力"),
    ("silverfang88", "2109440726865985560", "全面备战美股中期选举行情"),
)

EXPECTED_SHANGHAI = {
    "809663723006611456": "2016-12-16 15:37:29 GMT+8",
    "1441624264130453510": "2021-09-25 12:43:03 GMT+8",
    "1443403746990440455": "2021-09-30 10:34:05 GMT+8",
    "1444364011559014401": "2021-10-03 02:09:49 GMT+8",
    "1597088511764488192": "2022-11-28 12:42:28 GMT+8",
    "1609058637267492865": "2022-12-31 13:27:28 GMT+8",
    "1609298069941792768": "2023-01-01 05:18:53 GMT+8",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        rows.append(json.loads(line))
        rows[-1]["_line"] = line_no
    return rows


def shanghai_label(iso: str) -> str:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S GMT+8")


def month_span(start_iso: str, end_iso: str) -> list[str]:
    start = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
    y, m = start.year, start.month
    out = []
    while (y, m) <= (end.year, end.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y += 1
            m = 1
    return out


def status_ids(text: str) -> list[str]:
    return STATUS_RE.findall(text)


def parse_year_table(md: str) -> dict[str, int]:
    lines = md.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Counts by year":
            start = i
            break
    if start is None:
        return {}
    years = {}
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        m = YEAR_ROW_RE.match(line.strip())
        if m:
            years[m.group(1)] = int(m.group(2))
    return years


def body(post: dict) -> str:
    return (post.get("text") or "") + "\n" + (post.get("full_text") or "")


def validate(root: Path | None = None) -> dict:
    root = root or repo_root()
    errors: list[str] = []
    summary: dict = {"handles": {}, "total_posts": 0}

    pinned_path = root / "_raw" / "pinned_posts_get_posts_by_ids.json"
    pinned_ids: set[str] = set()
    if not pinned_path.exists():
        errors.append("missing _raw/pinned_posts_get_posts_by_ids.json")
    else:
        pinned = json.loads(pinned_path.read_text(encoding="utf-8"))
        for item in pinned.get("data") or []:
            if item.get("id") is None:
                errors.append("pinned payload has a post without id")
            else:
                pinned_ids.add(str(item.get("id")))

    profiles_path = root / "profiles.json"
    profiles = json.loads(profiles_path.read_text(encoding="utf-8")) if profiles_path.exists() else {}
    accounts = profiles.get("accounts") or {}

    summary_path = root / "collection_summary.json"
    if summary_path.exists():
        collection = json.loads(summary_path.read_text(encoding="utf-8"))
        if collection.get("completeness_claim") is not False:
            errors.append("collection_summary.json completeness_claim is not false")
        integration = collection.get("integration") or {}
        if integration.get("pagination_verified_complete") is not False:
            errors.append("collection_summary.json must keep pagination_verified_complete false")
    else:
        errors.append("missing collection_summary.json")

    for handle in HANDLES:
        hdir = root / handle
        posts_path = hdir / "normalized" / "posts.jsonl"
        lite_path = hdir / "normalized" / "posts_lite.jsonl"
        manifest_path = hdir / "coverage_manifest.json"
        manifest_md = hdir / "coverage_manifest.md"
        analysis = hdir / "analysis.md"
        archive = hdir / "chronological_archive.md"
        packet = hdir / "_reading_packet.md"
        for path in (posts_path, lite_path, manifest_path, manifest_md, analysis, archive):
            if not path.exists():
                errors.append(f"missing {path.relative_to(root)}")

        posts = load_jsonl(posts_path)
        lite = load_jsonl(lite_path)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        ids = [p.get("id") for p in posts]
        id_set = set(ids)

        if len(ids) != len(id_set):
            errors.append(f"{handle}: duplicate ids in posts.jsonl")
        for p in posts:
            if not isinstance(p.get("id"), str):
                errors.append(f"{handle}: id is not a string: {p.get('id')!r}")
            if p.get("author_id") is not None and not isinstance(p.get("author_id"), str):
                errors.append(f"{handle}: author_id is not a string on {p.get('id')}")
            for ref in p.get("referenced_tweets") or []:
                if not isinstance(ref.get("id"), str):
                    errors.append(f"{handle}: referenced id is not a string on {p.get('id')}")

        keys = [(p.get("created_at_utc") or "", p.get("id") or "") for p in posts]
        if keys != sorted(keys, reverse=True):
            errors.append(f"{handle}: posts.jsonl is not newest-first by (created_at_utc, id)")

        lite_ids = [p.get("id") for p in lite]
        if set(lite_ids) != id_set:
            errors.append(f"{handle}: posts_lite.jsonl id set differs from posts.jsonl")
        if any(not isinstance(i, str) for i in lite_ids):
            errors.append(f"{handle}: posts_lite.jsonl has a non-string id")

        by_year = Counter()
        by_month = Counter()
        by_type = Counter()
        for p in posts:
            created = p.get("created_at_utc")
            if not created:
                errors.append(f"{handle}: missing created_at_utc on {p.get('id')}")
                continue
            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            by_year[str(dt.year)] += 1
            by_month[dt.strftime("%Y-%m")] += 1
            by_type[p.get("post_type")] += 1
            expected = shanghai_label(created)
            if p.get("created_at_shanghai") != expected:
                errors.append(
                    f"{handle}: {p.get('id')} shanghai {p.get('created_at_shanghai')!r} != {expected}"
                )
            url = p.get("canonical_url") or ""
            if not url.startswith("https://x.com/") or str(p.get("id")) not in url:
                errors.append(f"{handle}: bad canonical_url for {p.get('id')}: {url}")
            profile = accounts.get(handle) or {}
            if profile.get("id") and p.get("author_id") != str(profile["id"]):
                errors.append(f"{handle}: author_id {p.get('author_id')} != profile {profile.get('id')}")

        if manifest.get("claim_of_completeness") is not False:
            errors.append(f"{handle}: claim_of_completeness is not false")
        if manifest.get("ids_stored_as") != "strings":
            errors.append(f"{handle}: ids_stored_as is not 'strings'")
        if manifest.get("retrieved_unique_posts") != len(posts):
            errors.append(
                f"{handle}: manifest count {manifest.get('retrieved_unique_posts')} != {len(posts)}"
            )
        if {str(k): v for k, v in manifest.get("by_year", {}).items()} != dict(by_year):
            errors.append(f"{handle}: by_year does not match posts")
        if manifest.get("by_year_month") != dict(by_month):
            errors.append(f"{handle}: by_year_month does not match posts")
        if manifest.get("by_type") != dict(by_type):
            errors.append(f"{handle}: by_type does not match posts")
        if sum(by_year.values()) != len(posts) or sum(by_month.values()) != len(posts):
            errors.append(f"{handle}: year/month buckets do not sum to post count")

        created_at = manifest.get("account_created_at_utc")
        newest = (manifest.get("retrieved_span_utc") or {}).get("newest")
        oldest = (manifest.get("retrieved_span_utc") or {}).get("oldest")
        if posts:
            chronological = sorted(posts, key=lambda p: (p.get("created_at_utc") or "", p.get("id") or ""))
            if oldest != chronological[0].get("created_at_utc"):
                errors.append(f"{handle}: manifest oldest != earliest post")
            if newest != chronological[-1].get("created_at_utc"):
                errors.append(f"{handle}: manifest newest != latest post")
        if created_at and newest:
            zero = [m for m in month_span(created_at, newest) if m not in by_month]
            if zero != manifest.get("months_in_account_life_with_zero_retrieved_posts"):
                errors.append(f"{handle}: zero-month list does not match posts and account lifetime")
            if manifest.get("zero_month_count") != len(zero):
                errors.append(f"{handle}: zero_month_count != {len(zero)}")

        raw_ids: set[str] = set()
        raw_files = sorted((hdir / "raw").glob("page_*.json"))
        for f in raw_files:
            payload = json.loads(f.read_text(encoding="utf-8"))
            for item in payload.get("data") or []:
                raw_ids.add(str(item.get("id")))
        missing_raw = id_set - raw_ids - pinned_ids
        if missing_raw:
            errors.append(f"{handle}: {len(missing_raw)} posts not in raw pages or pinned file")
        if manifest.get("api_pages_stored") != len(raw_files):
            errors.append(f"{handle}: api_pages_stored != {len(raw_files)} raw pages")

        index_path = hdir / "raw" / "_page_index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index_files = [p.get("file") for p in index.get("pages") or []]
        if index_files != [f.name for f in raw_files]:
            errors.append(f"{handle}: _page_index.json files do not match raw pages in order")
        index_open = [p for p in index.get("pages") or [] if p.get("next_token")]
        tokens = manifest.get("open_pagination_tokens") or []
        if manifest.get("open_pagination_tokens_count") != len(tokens):
            errors.append(f"{handle}: open_pagination_tokens_count != len(list)")
        if len(tokens) != len(index_open):
            errors.append(f"{handle}: open token list {len(tokens)} != pages with next_token {len(index_open)}")
        for token in tokens:
            if not isinstance(token.get("next_token"), str) or not token.get("next_token"):
                errors.append(f"{handle}: open token entry missing next_token string")
            if token.get("page_file") not in index_files:
                errors.append(f"{handle}: open token page_file missing: {token.get('page_file')}")

        md = manifest_md.read_text(encoding="utf-8")
        year_table = parse_year_table(md)
        if year_table != {k: int(v) for k, v in by_year.items()}:
            errors.append(f"{handle}: coverage_manifest.md year table != posts")
        if f"**{len(posts)}**" not in md:
            errors.append(f"{handle}: coverage_manifest.md does not state count {len(posts)}")
        if "Completeness claim: **no**" not in md:
            errors.append(f"{handle}: coverage_manifest.md does not deny completeness")

        archive_text = archive.read_text(encoding="utf-8")
        archive_ids = status_ids(archive_text)
        if set(archive_ids) != id_set or len(archive_ids) != len(id_set):
            errors.append(
                f"{handle}: chronological_archive.md has {len(archive_ids)} links, {len(set(archive_ids))} unique, posts {len(id_set)}"
            )
        else:
            times = []
            by_id = {p["id"]: p for p in posts}
            for i in archive_ids:
                times.append(by_id[i]["created_at_utc"])
            if times != sorted(times):
                errors.append(f"{handle}: chronological_archive.md is not oldest-to-newest")

        for label, path in (("analysis", analysis), ("archive", archive), ("reading_packet", packet)):
            if not path.exists():
                if label == "reading_packet":
                    continue
                continue
            text = path.read_text(encoding="utf-8")
            missing = [i for i in status_ids(text) if i not in id_set]
            if missing:
                errors.append(f"{handle}: {path.name} cites ids missing from posts.jsonl: {missing[:8]}")

        summary["handles"][handle] = {
            "posts": len(posts),
            "profile_post_count": manifest.get("profile_post_count_at_lookup"),
            "span_utc": manifest.get("retrieved_span_utc"),
            "by_type": dict(by_type),
            "open_next_token_pages": len(tokens),
            "zero_months": manifest.get("zero_month_count"),
            "completeness_claim": False,
        }
        summary["total_posts"] += len(posts)

    by_all = {}
    for handle in HANDLES:
        posts = load_jsonl(root / handle / "normalized" / "posts.jsonl")
        by_all.update({p["id"]: (handle, p) for p in posts})

    for handle, pid, needle in REQUIRED_TEXT:
        pair = by_all.get(pid)
        if not pair or pair[0] != handle:
            errors.append(f"required post {pid} missing from {handle}")
            continue
        if needle not in body(pair[1]):
            errors.append(f"{handle} {pid} does not contain {needle!r}")
        analysis_text = (root / handle / "analysis.md").read_text(encoding="utf-8")
        if pid not in analysis_text:
            errors.append(f"{handle} analysis.md does not cite {pid}")

    for pid, label in EXPECTED_SHANGHAI.items():
        pair = by_all.get(pid)
        if not pair:
            errors.append(f"expected timestamp post missing: {pid}")
        elif pair[1].get("created_at_shanghai") != label:
            errors.append(f"{pid} shanghai {pair[1].get('created_at_shanghai')!r} != {label}")

    wang_analysis = (root / "alexandr_wang" / "analysis.md").read_text(encoding="utf-8")
    if "809675263590961152" in wang_analysis:
        errors.append("alexandr_wang analysis still cites the absent Slack id 809675263590961152")
    sil_analysis = (root / "silverfang88" / "analysis.md").read_text(encoding="utf-8")
    if "ends there" in sil_analysis:
        errors.append("silverfang88 analysis still claims the 2022 note ends early")
    if "Earliest retrieved post is 2021-09-28" in (root / "silverfang88" / "coverage_manifest.md").read_text(encoding="utf-8"):
        errors.append("silverfang88 coverage still says earliest post is 2021-09-28")

    summary["completeness_claim"] = False
    summary["pagination_verified_complete"] = False
    return {"ok": not errors, "error_count": len(errors), "errors": errors, "summary": summary}


def main() -> int:
    report = validate()
    printable = {
        "ok": report["ok"],
        "error_count": report["error_count"],
        "errors": report["errors"],
        "summary": report["summary"],
    }
    print(json.dumps(printable, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
