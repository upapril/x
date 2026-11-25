#!/usr/bin/env python3
"""Ingest search_posts_all pages and rewrite resume/budget checkpoints. DATA ONLY."""
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ASSETS = Path("/cursor/stores/user/grok-bot/agents/898997d6-7db9-4848-8f4f-e163f93ec083/assets/")
ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / "logs" / "expand_jobs.json"
RESUME = ROOT / "logs" / "RESUME_OPEN_JOBS.json"
BUDGET = ROOT / "logs" / "live_budget.json"
NEXTF = ROOT / "logs" / "NEXT_FIRE.json"
SH = timezone(timedelta(hours=8))
HANDLES = ["silverfang88", "iiiinvest", "alexandr_wang", "taresky", "thankUcrypto"]
STALL_FIXED = [
    {"handle":"silverfang88","label":"2023-09","token":"b26v89c19zqg8o3fr5beqknfiduf3z8svkzzdfjkf2ttp"},
    {"handle":"silverfang88","label":"2026-07","token":"b26v89c19zqg8o3juewg2tl5lpfe021lawn2fn8ar26pp"},
    {"handle":"iiiinvest","label":"2026-08","token":"b26v89c19zqg8o3juezgp0sqjwdnag097te7ltdd0hzlp"},
    {"handle":"iiiinvest","label":"2026-08","token":"b26v89c19zqg8o3juezgoudctnrq3quemi6wf56f1d5dp"},
]
PACKAGED = 15370
BASE_CALLS_BEFORE_DATA_CHUNK = 892  # expand_jobs calls_this_pass at start of data-only work ~490

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pairs", nargs="+", help="handle:filename:label")
    ap.add_argument("--log", default=str(ROOT/"logs"/"last_ingest.txt"))
    args = ap.parse_args()
    by_h = {h: [] for h in HANDLES}
    lines = []
    last = None
    fail = []
    for item in args.pairs:
        h, fn, lab = item.split(":", 2)
        p = ASSETS / fn if not fn.startswith("/") else Path(fn)
        t = p.read_text(encoding="utf-8", errors="replace")
        sz = p.stat().st_size
        rc = re.findall(r'"result_count":\s*\d+', t)
        nxt = bool(re.search(r'"next_token":\s*"[^"]+"', t))
        foot = re.findall(r"X reads left[^\n]+", t)
        if foot:
            candidate = foot[-1]
            old_n = re.search(r"(\d+) of 1000 today", last or "")
            new_n = re.search(r"(\d+) of 1000 today", candidate)
            if new_n and (not old_n or int(new_n.group(1)) < int(old_n.group(1))):
                last = candidate
        bad = ("Too Many Requests" in t and '"result_count"' not in t) or ('"result_count"' not in t and sz < 200)
        if bad:
            fail.append((h, lab, fn))
        lines.append(f"{h[:3]} {lab:16} {sz:6d} {rc} nxt={nxt} BAD={bad}")
        by_h[h].append((fn, lab, bad, str(p.name)))
    lines.append("LAST_FOOTER " + str(last))
    if fail:
        lines.append("FAILED " + str(fail))

    for h in HANDLES:
        good = [(fn, lab) for fn, lab, bad, _ in by_h[h] if not bad]
        if not good:
            continue
        cmd = ["python3", str(ROOT/"_tools"/"batch_update.py"), h] + [f"{fn}:{lab}" for fn, lab in good]
        r = subprocess.run(cmd, capture_output=True, text=True)
        lines.append(r.stdout)
        if r.returncode != 0:
            lines.append("ERR " + r.stderr)
            Path(args.log).write_text("\n".join(lines) + "\n")
            sys.exit(r.returncode)

    u = {}
    for h in HANDLES:
        u[h] = sum(1 for line in (ROOT/h/"normalized"/"posts.jsonl").read_text().split('\n') if line.strip())
    m = re.search(r"(\d+) of 1000 today \(resets at ([^)]+)\)", last or "")
    daily = int(m.group(1)) if m else None
    reset = m.group(2) if m else None
    usable = None if daily is None else daily - 75
    lines.append(f"UNIQUES {u} sum {sum(u.values())}")
    lines.append(f"DAILY {daily} USABLE {usable}")

    j = json.loads(JOBS.read_text())
    hv = []
    for x in j["jobs"]:
        if x["status"] != "open":
            continue
        if x["handle"] == "silverfang88" and x["label"].startswith("2024"):
            continue
        if x["handle"] == "alexandr_wang" and x["label"].startswith("201"):
            continue
        rec = {k: x.get(k) for k in ["handle","label","pages_fetched","posts_added","next_token","start_time","end_time","query"]}
        rec["pages"] = rec.pop("pages_fetched")
        rec["added"] = rec.pop("posts_added")
        hv.append(rec)
        # tokens persist in NEXT_FIRE.json / RESUME_OPEN_JOBS.json, not stdout
    for x in j["jobs"]:
        if x["status"] in ("pagination_stalled", "not_proven_exhausted"):
            lines.append(f"STALL {x['status']} {x['handle']} {x['label']} {x.get('next_token')}")
        if x["status"] == "exhausted" and (
            x["label"].startswith("2026-") or x["label"].startswith("2025-") or
            (x["handle"]=="alexandr_wang" and x["label"].startswith("2022-")) or
            (x["handle"]=="alexandr_wang" and x["label"].startswith("2023-"))
        ):
            # only print ones just maybe relevant; keep short
            pass
    # print any newly exhausted among this batch labels
    batch_labels = {(h, lab) for h in HANDLES for _, lab, _, _ in by_h[h]}
    for x in j["jobs"]:
        if x["status"] == "exhausted" and (x["handle"], x["label"]) in batch_labels:
            lines.append(f"EXH {x['handle']} {x['label']} p{x.get('pages_fetched')} +{x.get('posts_added')}")

    stall_tokens = list(STALL_FIXED)
    seen = {(s["handle"], s["token"]) for s in stall_tokens}
    for x in j["jobs"]:
        if x["status"] == "pagination_stalled":
            tok = x.get("next_token") or x.get("last_input_token")
            key = (x["handle"], tok)
            if tok and key not in seen:
                stall_tokens.append({"handle":x["handle"],"label":x["label"],"token":tok})
                seen.add(key)

    pending = {h: [x["label"] for x in j["jobs"] if x["handle"]==h and x["status"]=="pending"] for h in HANDLES}
    chunk = (j.get("calls_this_pass") or 0) - BASE_CALLS_BEFORE_DATA_CHUNK
    now_sh = datetime.now(SH).strftime("%Y-%m-%d %H:%M:%S GMT+8")
    ckpt = {
        "written_at_shanghai": now_sh,
        "written_at_utc": datetime.now(timezone.utc).isoformat(),
        "pass": "data-collection-day2-2026-11-25",
        "stop_reason": "in_progress",
        "authoritative_footer": last,
        "daily_remaining": daily,
        "daily_reset_utc": reset,
        "daily_reset_shanghai": "2026-11-26 08:00:00 GMT+8",
        "reserve": 75,
        "usable": usable,
        "budget_malfunction": False,
        "expand_jobs_calls_this_pass": j.get("calls_this_pass"),
        "calls_this_chunk": chunk,
        "unique_posts": u,
        "unique_total": sum(u.values()),
        "packaged_in_latest_zip": PACKAGED,
        "added_on_disk_vs_latest_zip": sum(u.values()) - PACKAGED,
        "do_not_reuse_stalled_tokens": stall_tokens,
        "next_high_value_open": hv,
        "open_jobs": [
            {k: x.get(k) for k in ["handle","label","query","start_time","end_time","status","pages_fetched","posts_added","next_token","last_input_token"]}
            for x in j["jobs"] if x["status"] in ("open","pagination_stalled","not_proven_exhausted")
        ],
        "pending_by_handle": pending,
        "notes": [
            "Do not open silverfang88 pending 2026-11 (overlaps exhausted 2026-11-01to08 and 2026-11-08to25).",
            "Never reuse stalled parent tokens or reopen exhausted child windows. Read current expand_jobs.json and remaining_jobs_day2.json for exact status.",
            "Data-collection only; no analysis/archive rebuild, no new zip, no Meta refetch, no GitHub writes.",
            "latest.zip left immutable. SHA256 1ab3fc4aaee8667c42d833543a85f86f54ff9dabe165f6305d56769aed4d8e58",
        ],
    }
    RESUME.write_text(json.dumps(ckpt, ensure_ascii=False, indent=2) + "\n")
    BUDGET.write_text(json.dumps({k: ckpt[k] for k in [
        "written_at_shanghai","authoritative_footer","daily_remaining","daily_reset_utc",
        "reserve","usable","unique_posts","unique_total","calls_this_chunk","budget_malfunction","stop_reason"
    ]}, indent=2) + "\n")
    NEXTF.write_text(json.dumps({
        "footer": last,
        "usable": usable,
        "do_not_reuse": stall_tokens,
        "open_high_value": hv,
    }, ensure_ascii=False, indent=2) + "\n")
    lines.append(f"checkpointed calls_this_pass {j.get('calls_this_pass')} chunk {chunk} daily {daily} usable {usable}")
    Path(args.log).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
