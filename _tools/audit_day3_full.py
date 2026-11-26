#!/usr/bin/env python3
"""Day3 full raw-text / provenance / retention / archive audit.

Does not modify day2 validation files or prior ZIPs. Writes
logs/day3_package_validation.json (and a provisional copy before
archive/citation checks can be completed).
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
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
DAY2_COUNTS = {
    "silverfang88": 12862,
    "iiiinvest": 4712,
    "alexandr_wang": 1921,
    "taresky": 8551,
    "thankUcrypto": 6867,
}
DAY2_ZIP = Path("/workspace/x-research-day2-final.zip")
SH = timezone(timedelta(hours=8))

PINNED = {
    ("alexandr_wang", "2103551714536439951"): "../_raw/pinned_posts_get_posts_by_ids.json",
    ("iiiinvest", "2110022220131226106"): "../_raw/pinned_posts_get_posts_by_ids.json",
    ("silverfang88", "2109440726865985560"): "../_raw/pinned_posts_get_posts_by_ids.json",
}
U2028_ID = "2110119596435054716"

PRIOR_ZIPS = {
    "/workspace/x-research-firstpass.zip": "455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976",
    "/workspace/x-research-expanded.zip": "d601957063b3610067d2dafd6cab0a6effb63e771bd642df57233b5e44fee6c7",
    "/workspace/x-research-latest.zip": "1ab3fc4aaee8667c42d833543a85f86f54ff9dabe165f6305d56769aed4d8e58",
    "/workspace/x-research-day1-final.zip": "537597c2d1c295f18773fb2099d751338f78a354be982b65a26aaf7367efea37",
    "/workspace/x-research-day2-final.zip": "7b4523860662a9744cc4d52df7642fee4728d6af0fa059a4a108a8fa71302e0b",
    "/workspace/x-research-day2-final-part01.zip": "7c9c77173aa0acaddf16c715f5048c2e55b8f52685ceeb39b63a87f63febd1e3",
    "/workspace/x-research-day2-final-part02.zip": "61c135dd16dae48692414d5435f9fe59568c3d96d327e5a9c5531de2599410b2",
}


def now_shanghai() -> str:
    return datetime.now(SH).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    raw = path.read_bytes()
    parts = raw.split(b"\n")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [json.loads(x) for x in parts]


def post_text(p: dict) -> str:
    return p.get("full_text") or p.get("text") or ""


def control_issues(s: str) -> list[str]:
    bad = []
    for i, ch in enumerate(s):
        o = ord(ch)
        if o < 32 and ch not in ("\t", "\n", "\r"):
            bad.append(f"U+{o:04X}@{i}")
        elif 0x7F <= o <= 0x9F:
            bad.append(f"U+{o:04X}@{i}")
    return bad


def load_day2_ids() -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    with zipfile.ZipFile(DAY2_ZIP) as z:
        for handle in HANDLES:
            name = f"x-research/{handle}/normalized/posts.jsonl"
            raw = z.read(name)
            parts = raw.split(b"\n")
            if parts and parts[-1] == b"":
                parts = parts[:-1]
            ids = set()
            for line in parts:
                p = json.loads(line)
                ids.add(str(p["id"]))
            out[handle] = ids
    return out


def extract_raw_items(obj) -> dict[str, dict]:
    """Map post id -> raw item dicts found under data (and note-like wrappers)."""
    found: dict[str, dict] = {}

    def consider(item):
        if not isinstance(item, dict):
            return
        pid = item.get("id") or item.get("rest_id")
        if pid is not None and ("text" in item or "full_text" in item or "note_tweet" in item or "note_post" in item):
            found[str(pid)] = item

    if isinstance(obj, dict):
        data = obj.get("data")
        if isinstance(data, list):
            for it in data:
                consider(it)
        elif isinstance(data, dict):
            # unlikely
            consider(data)
            for v in data.values():
                if isinstance(v, list):
                    for it in v:
                        consider(it)
        # also walk includes.tweets? only as fallback later
        inc = obj.get("includes") or {}
        tweets = inc.get("tweets") or inc.get("posts") or []
        for it in tweets:
            consider(it)
    return found


def candidate_texts(item: dict) -> list[str]:
    out = []
    for k in ("text", "full_text"):
        v = item.get(k)
        if isinstance(v, str):
            out.append(v)
    for wrap_key in ("note_tweet", "note_post", "note_tweet_results", "article"):
        w = item.get(wrap_key)
        if isinstance(w, dict):
            # note_tweet_results.result.legacy or .text
            for k in ("text", "full_text", "note"):
                v = w.get(k)
                if isinstance(v, str):
                    out.append(v)
            res = w.get("result") or w.get("note_tweet") or {}
            if isinstance(res, dict):
                for k in ("text", "full_text", "note"):
                    v = res.get(k)
                    if isinstance(v, str):
                        out.append(v)
                leg = res.get("legacy") or {}
                if isinstance(leg, dict) and isinstance(leg.get("full_text"), str):
                    out.append(leg["full_text"])
    # dedup preserve order
    seen = set()
    uniq = []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def texts_match(norm: str, candidates: list[str]) -> bool:
    if norm in candidates:
        return True
    n = norm.replace("\r\n", "\n")
    for c in candidates:
        if c.replace("\r\n", "\n") == n:
            return True
    return False


def resolve_page(handle: str, page_file: str) -> Path | None:
    if not page_file:
        return None
    p = Path(page_file)
    if p.is_absolute() and p.is_file():
        return p
    cand = (ROOT / handle / page_file).resolve()
    if cand.is_file():
        return cand
    cand2 = (ROOT / page_file).resolve()
    if cand2.is_file():
        return cand2
    return None


def audit_core() -> dict:
    report: dict = {
        "written_at_shanghai": now_shanghai(),
        "pass_name": "day3-full-raw-text-provenance-audit",
        "fast_checks": {},
        "full_checks": {},
        "inherited_corrections": {},
        "prior_zip_hashes": {},
        "ok": True,
        "errors": [],
        "warnings": [],
    }

    # prior zips — existence and hash, do not write
    zip_ok = True
    for path, expected in PRIOR_ZIPS.items():
        p = Path(path)
        if not p.is_file():
            report["prior_zip_hashes"][path] = {"present": False}
            report["errors"].append(f"missing prior zip {path}")
            zip_ok = False
            continue
        got = sha256_file(p)
        report["prior_zip_hashes"][path] = {
            "present": True,
            "sha256": got,
            "expected": expected,
            "unchanged": got == expected,
            "size_bytes": p.stat().st_size,
        }
        if got != expected:
            report["errors"].append(f"prior zip hash changed: {path}")
            zip_ok = False
    report["full_checks"]["prior_zips_unchanged"] = zip_ok
    if not zip_ok:
        report["ok"] = False

    day2_ids = load_day2_ids()
    global_ids: set[str] = set()
    per = {}
    page_cache: dict[Path, dict] = {}
    raw_index_cache: dict[Path, dict[str, dict]] = {}

    jsonl_sha = {}
    attr_fail = []
    dup_global = []
    ctrl_fail = []
    missing_page = []
    missing_in_page = []
    text_mismatch = []
    empty_text = 0

    for handle in HANDLES:
        path = ROOT / handle / "normalized" / "posts.jsonl"
        posts = load_jsonl(path)
        jsonl_sha[handle] = sha256_file(path)
        ids = []
        local = set()
        author_ok = 0
        author_bad = 0
        retained = 0
        for p in posts:
            pid = str(p.get("id") or "")
            ids.append(pid)
            if not pid:
                report["errors"].append(f"{handle} empty id")
                continue
            if pid in local:
                dup_global.append((handle, pid, "per-account"))
            local.add(pid)
            if pid in global_ids:
                dup_global.append((handle, pid, "global"))
            global_ids.add(pid)
            aid = str(p.get("author_id") or "")
            if aid == AUTHOR_IDS[handle]:
                author_ok += 1
            else:
                author_bad += 1
                if len(attr_fail) < 20:
                    attr_fail.append({"handle": handle, "id": pid, "author_id": aid})
            if pid in day2_ids[handle]:
                retained += 1
            text = post_text(p)
            if text == "":
                empty_text += 1
            # control chars in text and in raw json of selected fields
            for field in (text, json.dumps(p.get("id"), ensure_ascii=True)):
                issues = control_issues(text)
                if issues:
                    ctrl_fail.append({"handle": handle, "id": pid, "issues": issues[:5]})
                    break
            # U+2028 is allowed (Zl)

            col = p.get("collection") or {}
            page_file = col.get("page_file") or ""
            resolved = resolve_page(handle, page_file)
            if resolved is None:
                missing_page.append({"handle": handle, "id": pid, "page_file": page_file})
                continue
            if resolved not in raw_index_cache:
                try:
                    obj = json.loads(resolved.read_text(encoding="utf-8"))
                except Exception as e:
                    missing_page.append({"handle": handle, "id": pid, "page_file": page_file, "error": str(e)})
                    raw_index_cache[resolved] = {}
                    continue
                raw_index_cache[resolved] = extract_raw_items(obj)
            item = raw_index_cache[resolved].get(pid)
            if item is None:
                missing_in_page.append({"handle": handle, "id": pid, "page_file": str(resolved)})
                continue
            cands = candidate_texts(item)
            norm_text = p.get("text") or ""
            norm_full = p.get("full_text") or ""
            ok = texts_match(text, cands) or (norm_text and texts_match(norm_text, cands)) or (norm_full and texts_match(norm_full, cands))
            if not ok:
                # allow candidate startswith / text startswith for truncated API display
                soft = False
                for c in cands:
                    if text and (text.startswith(c) or c.startswith(text) or c.replace("…","") in text or text.replace("…","") in c):
                        # only if one is a prefix of the other or ellipsis truncation
                        if text.startswith(c) or c.startswith(text.rstrip("…")) or c.rstrip("…") == text.rstrip("…"):
                            soft = True
                            break
                if not soft:
                    if len(text_mismatch) < 50:
                        text_mismatch.append({
                            "handle": handle,
                            "id": pid,
                            "page_file": page_file,
                            "norm_len": len(text),
                            "cand_lens": [len(c) for c in cands],
                            "norm_head": text[:80],
                            "cand_head": (cands[0][:80] if cands else None),
                        })
                    else:
                        text_mismatch.append({"handle": handle, "id": pid})  # count only

        missing_day2 = sorted(day2_ids[handle] - local)
        extra_vs_day2 = len(local) - retained
        per[handle] = {
            "unique": len(local),
            "rows": len(posts),
            "author_ok": author_ok,
            "author_bad": author_bad,
            "day2_count": DAY2_COUNTS[handle],
            "day2_ids_in_zip": len(day2_ids[handle]),
            "day2_ids_retained": retained,
            "day2_ids_missing": len(missing_day2),
            "missing_day2_sample": missing_day2[:10],
            "added_vs_day2": extra_vs_day2,
            "jsonl_sha256": jsonl_sha[handle],
        }
        if len(posts) != len(local):
            report["errors"].append(f"{handle} duplicate ids in jsonl: rows={len(posts)} unique={len(local)}")
        if author_bad:
            report["errors"].append(f"{handle} author_id mismatches: {author_bad}")
        if missing_day2:
            report["errors"].append(f"{handle} lost {len(missing_day2)} day2 ids")
        if len(local) != DAY2_COUNTS[handle] + extra_vs_day2 and not missing_day2:
            # tautological; skip
            pass
        if len(day2_ids[handle]) != DAY2_COUNTS[handle]:
            report["warnings"].append(
                f"{handle} day2 zip unique {len(day2_ids[handle])} != expected {DAY2_COUNTS[handle]}"
            )

    report["fast_checks"] = {
        "unique_total": len(global_ids),
        "per_account": per,
        "global_cross_account_duplicate_ids": [x for x in dup_global if x[2] == "global"][:20],
        "global_cross_account_duplicate_count": sum(1 for x in dup_global if x[2] == "global"),
        "attribution_failures_sample": attr_fail,
        "control_char_failures": len(ctrl_fail),
        "control_char_sample": ctrl_fail[:10],
        "empty_display_text_count": empty_text,
        "expected_total": 53706,
        "id_attribution_day2_retention_ok": (
            len(global_ids) == 53706
            and not attr_fail
            and all(per[h]["day2_ids_missing"] == 0 for h in HANDLES)
            and all(per[h]["author_bad"] == 0 for h in HANDLES)
            and all(per[h]["unique"] == per[h]["rows"] for h in HANDLES)
            and sum(1 for x in dup_global if x[2] == "global") == 0
        ),
    }
    if not report["fast_checks"]["id_attribution_day2_retention_ok"]:
        report["ok"] = False
        report["errors"].append("fast ID/attribution/day2-retention failed")
    if ctrl_fail:
        report["ok"] = False
        report["errors"].append(f"control-char failures: {len(ctrl_fail)}")

    # inherited corrections
    sf_posts = {str(p["id"]): p for p in load_jsonl(ROOT / "silverfang88" / "normalized" / "posts.jsonl")}
    u = sf_posts.get(U2028_ID)
    u_ok = bool(u) and ("\u2028" in post_text(u))
    pinned_ok = True
    pinned_detail = {}
    for (h, pid), expected_path in PINNED.items():
        recs = {str(p["id"]): p for p in load_jsonl(ROOT / h / "normalized" / "posts.jsonl")}
        rec = recs.get(pid)
        got = (rec.get("collection") or {}).get("page_file") if rec else None
        exists = resolve_page(h, got) is not None if got else False
        ok = rec is not None and got == expected_path and exists
        pinned_detail[f"{h}:{pid}"] = {"page_file": got, "expected": expected_path, "ok": ok, "file_exists": exists}
        if not ok:
            pinned_ok = False
    report["inherited_corrections"] = {
        "sf_2110119596435054716_has_U+2028": u_ok,
        "pinned_page_file_paths": pinned_detail,
        "ok": u_ok and pinned_ok,
    }
    if not (u_ok and pinned_ok):
        report["ok"] = False
        report["errors"].append("inherited corrections failed")

    report["full_checks"]["missing_page_file"] = {"count": len(missing_page), "sample": missing_page[:15]}
    report["full_checks"]["id_not_in_page"] = {"count": len(missing_in_page), "sample": missing_in_page[:15]}
    report["full_checks"]["raw_text_mismatch"] = {"count": len(text_mismatch), "sample": text_mismatch[:15]}
    raw_ok = len(missing_page) == 0 and len(missing_in_page) == 0 and len(text_mismatch) == 0
    report["full_checks"]["raw_text_and_provenance_ok"] = raw_ok
    if not raw_ok:
        report["ok"] = False
        report["errors"].append(
            f"raw/provenance issues: missing_page={len(missing_page)} missing_in_page={len(missing_in_page)} text_mismatch={len(text_mismatch)}"
        )

    return report


def audit_lite_and_archives(report: dict) -> dict:
    lite_ok = True
    lite_detail = {}
    arch_ok = True
    arch_detail = {}
    for handle in HANDLES:
        posts = load_jsonl(ROOT / handle / "normalized" / "posts.jsonl")
        lite_path = ROOT / handle / "normalized" / "posts_lite.jsonl"
        lite = load_jsonl(lite_path)
        problems = []
        if len(lite) != len(posts):
            problems.append(f"count lite={len(lite)} full={len(posts)}")
        full_by_id = {str(p["id"]): p for p in posts}
        lite_ids = []
        for row in lite:
            lid = str(row.get("id"))
            lite_ids.append(lid)
            fp = full_by_id.get(lid)
            if fp is None:
                problems.append(f"lite id not in full: {lid}")
                continue
            if row.get("text") != post_text(fp):
                problems.append(f"lite text mismatch {lid}")
            if row.get("created_at_utc") != fp.get("created_at_utc"):
                problems.append(f"lite created_at_utc mismatch {lid}")
        if len(set(lite_ids)) != len(lite_ids):
            problems.append("lite duplicate ids")
        lite_detail[handle] = {"ok": not problems, "problems_sample": problems[:8], "lite_count": len(lite)}
        if problems:
            lite_ok = False

        # archives
        years = defaultdict(list)
        for p in posts:
            years[(p.get("created_at_utc") or "")[:4]].append(p)
        handle_arch_problems = []
        arch_dir = ROOT / handle / "archives"
        for y, yposts in years.items():
            f = arch_dir / f"{y}.md"
            if not f.is_file():
                handle_arch_problems.append(f"missing archives/{y}.md")
                continue
            text = f.read_text(encoding="utf-8")
            if f"# @{handle} — {y}" not in text and f"# @{handle} — {y} " not in text:
                # heading is `# @handle — YEAR (UTC year)`
                if f"# @{handle} — {y} (UTC year)" not in text:
                    handle_arch_problems.append(f"bad heading {y}")
            # sample up to 25 posts including first, last, and any with U+2028
            sample = yposts[:10] + yposts[-5:]
            for p in yposts:
                if p.get("id") == U2028_ID or "\u2028" in post_text(p):
                    sample.append(p)
            seen = set()
            for p in sample:
                pid = str(p["id"])
                if pid in seen:
                    continue
                seen.add(pid)
                if f"## {pid}" not in text:
                    handle_arch_problems.append(f"missing heading {pid} in {y}.md")
                    continue
                body = post_text(p)
                if body and body not in text:
                    handle_arch_problems.append(f"literal text missing for {pid} in {y}.md")
        chrono = (ROOT / handle / "chronological_archive.md").read_text(encoding="utf-8")
        if f"# @{handle} chronological index" not in chrono:
            handle_arch_problems.append("bad chronological heading")
        # spot-check 15 ids present
        for p in posts[:10] + posts[-5:]:
            if f"`{p['id']}`" not in chrono:
                handle_arch_problems.append(f"chrono missing {p['id']}")
        arch_detail[handle] = {"ok": not handle_arch_problems, "problems_sample": handle_arch_problems[:10]}
        if handle_arch_problems:
            arch_ok = False

    report["full_checks"]["lite_equivalence"] = {"ok": lite_ok, "detail": lite_detail}
    report["full_checks"]["archives_heading_and_literal_text"] = {"ok": arch_ok, "detail": arch_detail}
    if not lite_ok:
        report["ok"] = False
        report["errors"].append("lite equivalence failed")
    if not arch_ok:
        report["ok"] = False
        report["errors"].append("archive heading/literal text failed")
    return report


def audit_citations(report: dict, ledger_path: Path) -> dict:
    if not ledger_path.is_file():
        report["full_checks"]["citation_ledger"] = {"ok": False, "reason": "ledger not yet written"}
        report["ok"] = False
        report["errors"].append("citation ledger missing")
        return report
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    posts_idx: dict[str, dict[str, dict]] = {}
    for handle in HANDLES:
        posts_idx[handle] = {str(p["id"]): p for p in load_jsonl(ROOT / handle / "normalized" / "posts.jsonl")}
    failures = []
    items = ledger.get("citations") or ledger.get("items") or ledger
    if isinstance(items, dict) and "citations" not in ledger and "items" not in ledger:
        # maybe {handle: [...]}
        seq = []
        for h, lst in items.items():
            if isinstance(lst, list):
                for it in lst:
                    if isinstance(it, dict):
                        it = dict(it)
                        it.setdefault("handle", h)
                        seq.append(it)
        items = seq
    if not isinstance(items, list):
        failures.append("ledger format not a list of citations")
        items = []
    for it in items:
        h = it.get("handle")
        pid = str(it.get("id") or it.get("post_id") or "")
        excerpt = it.get("excerpt") or it.get("text") or it.get("quote") or ""
        rec = posts_idx.get(h, {}).get(pid)
        if rec is None:
            failures.append({"handle": h, "id": pid, "error": "id not in store"})
            continue
        body = post_text(rec)
        if excerpt and excerpt not in body:
            failures.append({"handle": h, "id": pid, "error": "excerpt not in store text", "excerpt": excerpt[:80]})
        url = it.get("url") or it.get("canonical_url")
        if url and rec.get("canonical_url") and url != rec.get("canonical_url"):
            # allow either form
            expected = rec.get("canonical_url")
            if url.rstrip("/") != (expected or "").rstrip("/"):
                failures.append({"handle": h, "id": pid, "error": "url mismatch", "url": url, "expected": expected})
    report["full_checks"]["citation_ledger"] = {
        "ok": not failures,
        "checked": len(items),
        "failures": failures[:20],
        "ledger": str(ledger_path),
    }
    if failures:
        report["ok"] = False
        report["errors"].append(f"citation ledger failures: {len(failures)}")
    return report


def write_report(report: dict, path: Path) -> None:
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote", path, "ok=", report["ok"], "errors=", report.get("errors"))


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=["core", "after_rebuild", "citations", "all"], default="all")
    ap.add_argument("--ledger", default=str(ROOT / "logs" / "day3_citation_ledger.json"))
    args = ap.parse_args()
    out = ROOT / "logs" / "day3_package_validation.json"
    if args.phase in ("core", "all"):
        report = audit_core()
        write_report(report, out)
    else:
        report = json.loads(out.read_text(encoding="utf-8"))
    if args.phase in ("after_rebuild", "all"):
        report = audit_lite_and_archives(report)
        write_report(report, out)
    if args.phase in ("citations", "all"):
        report = audit_citations(report, Path(args.ledger))
        write_report(report, out)
    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
