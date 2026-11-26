#!/usr/bin/env python3
from __future__ import annotations
import json, re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path("/workspace/x-research")
TPL = Path("/tmp/day3w/templates")
SH = timezone(timedelta(hours=8))
HANDLES = {
    "silverfang88": 19848,
    "iiiinvest": 4850,
    "alexandr_wang": 3625,
    "taresky": 17532,
    "thankUcrypto": 7851,
}
LEDGER = []
POSTS = {}
CITE_RE = re.compile(r"\{\{cite:([^:]+):(\d+):(.*?)\}\}", re.S)

def load_jsonl(path: Path):
    raw = path.read_bytes()
    parts = raw.split(b"\n")
    if parts and parts[-1] == b"":
        parts = parts[:-1]
    return [json.loads(x) for x in parts]

def post_text(p):
    return p.get("full_text") or p.get("text") or ""

def load_posts():
    for h in HANDLES:
        POSTS[h] = {str(p["id"]): p for p in load_jsonl(ROOT / h / "normalized" / "posts.jsonl")}

def cite(handle, pid, excerpt, used_in):
    rec = POSTS[handle].get(str(pid))
    if rec is None:
        raise SystemExit(f"citation id missing: {handle} {pid}")
    body = post_text(rec)
    if excerpt not in body:
        raise SystemExit(f"excerpt not in store: {handle} {pid} :: {excerpt!r}")
    url = rec.get("canonical_url") or f"https://x.com/{handle}/status/{pid}"
    when = rec.get("created_at_shanghai") or rec.get("created_at_utc")
    LEDGER.append({"handle": handle, "id": str(pid), "excerpt": excerpt, "url": url, "created_at_shanghai": when, "used_in": used_in})
    return f"“{excerpt}” — [{when}]({url})"

def preamble(handle, n):
    return f"""# @{handle} — day3 analysis, explicitly partial

**26 Nov 2026, Asia/Shanghai (GMT+8).** {n:,} deduplicated captured posts. Start with `coverage_manifest.md`; archives are indexed by UTC year. Profile identity is public account wording only; no private legal-name inference. All performance, fills, forecasts, third-party allegations and market facts below remain the author's statements unless a separate source is expressly identified. This is an evidence-led reading guide, not an audited track record or investment advice. A post being present proves what the captured response says, not that the strategy worked or every underlying event occurred.

The earlier day1 narrative is a **historical snapshot** in `../logs/historical_narratives_day1/`. Day2 analyses are superseded by this file as the current reading guide; retained day2 citations were re-checked against the store. Source excerpts for this synthesis are in `../logs/day3_citation_ledger.json`. Statements below are labeled as **explicit dated advice** (the author's own words on a date), **interpretation** (our reading), or **study recommendations** (ours, not the author's system).

"""

def expand(text, used_in):
    def repl(m):
        return cite(m.group(1), m.group(2), m.group(3), used_in)
    return CITE_RE.sub(repl, text)

def main():
    load_posts()
    mapping = {
        "silverfang88.md": ROOT / "silverfang88" / "analysis.md",
        "iiiinvest.md": ROOT / "iiiinvest" / "analysis.md",
        "alexandr_wang.md": ROOT / "alexandr_wang" / "analysis.md",
        "taresky.md": ROOT / "taresky" / "analysis.md",
        "thankUcrypto.md": ROOT / "thankUcrypto" / "analysis.md",
        "FINANCE_COMPARISON.md": ROOT / "FINANCE_COMPARISON.md",
        "FINANCE_SKILLS_COMPARISON.md": ROOT / "FINANCE_SKILLS_COMPARISON.md",
        "INSIGHTS.md": ROOT / "INSIGHTS.md",
        "METHODOLOGY.md": ROOT / "METHODOLOGY.md",
        "README.md": ROOT / "README.md",
        "PACKAGE_README.md": ROOT / "PACKAGE_README.md",
    }
    for name, dest in mapping.items():
        raw = (TPL / name).read_text(encoding="utf-8")
        if name.endswith("analysis.md") or name in (
            "silverfang88.md","iiiinvest.md","alexandr_wang.md","taresky.md","thankUcrypto.md"
        ):
            handle = name.replace(".md","")
            body = preamble(handle, HANDLES[handle]) + expand(raw, f"{handle}/analysis.md")
        else:
            body = expand(raw, name)
        dest.write_text(body, encoding="utf-8")
        print("wrote", dest, "bytes", dest.stat().st_size)
    # public sources boundary
    path = ROOT / "public_sources_wang.md"
    old = path.read_text(encoding="utf-8")
    marker = "> Day3 audit boundary"
    if not old.startswith(marker):
        prefix = (
            "> Day3 audit boundary (26 Nov 2026, Asia/Shanghai): no Meta page, Scale page, "
            "Reuters article, or profile was fetched or re-fetched on day3. The following remain "
            "the 24 Nov 2026 captured-source notes (with the day2 boundary already recorded below). "
            "Packaging notes in analysis.md are not a substitute for the leadership-page HTML. "
            "No additional significant Meta fact is asserted.\n\n"
        )
        path.write_text(prefix + old, encoding="utf-8")
        print("updated public_sources_wang.md boundary")
    ledger = {
        "written_at_shanghai": datetime.now(SH).isoformat(),
        "pass": "day3",
        "citation_count": len(LEDGER),
        "citations": LEDGER,
    }
    dest = ROOT / "logs" / "day3_citation_ledger.json"
    dest.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ledger", len(LEDGER))

if __name__ == "__main__":
    main()
