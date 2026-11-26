#!/usr/bin/env python3
"""Rebuild manifests, chronological archives, collection summary, resume files."""
from __future__ import annotations

import json
import hashlib
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path("/workspace/x-research")
HANDLES = ["alexandr_wang", "iiiinvest", "silverfang88", "taresky", "thankUcrypto"]
PROFILE_COUNTS = {
    "alexandr_wang": {"user_id": "615818451", "post_count_at_lookup": 3762, "display": "Alexandr Wang"},
    "iiiinvest": {"user_id": "1589763597705437184", "post_count_at_lookup": 4858, "display": "电鱼哥"},
    "silverfang88": {"user_id": "1435990322702520320", "post_count_at_lookup": 19982, "display": "子时"},
    "taresky": {"user_id": "368245720", "post_count_at_lookup": 34003, "display": "𝘁𝗮𝗿𝗲𝘀𝗸𝘆"},
    "thankUcrypto": {"user_id": "705564530936418304", "post_count_at_lookup": 8097, "display": "allincrypto 熬鹰资本"},
}
SH = timezone(timedelta(hours=8))


def now_sh():
    return datetime.now(SH)


def load_posts(handle: str):
    path = ROOT / handle / "normalized" / "posts.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").split('\n'):
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
    return s


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
            import re
            text = text_of(r)
            fence = "`" * max(3, max([len(m.group(0))+1 for m in re.finditer(r"`+", text)] or [3]))
            lines.append(fence)
            lines.append(text)
            lines.append(fence)
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
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")
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



def main():
    import shutil
    logs=ROOT/'logs';packed_at=now_sh().isoformat()
    budget=json.loads((logs/'live_budget.json').read_text());assert budget['daily_remaining']==75 and budget['usable']==0
    jd=load_jobs();jobs=jd['jobs'];remaining=json.loads((logs/'remaining_jobs_day2.json').read_text())
    profiles={h:json.loads((ROOT/h/'profile.json').read_text()) for h in HANDLES}
    excluded=remaining.get('excluded_precreation_calendar_windows',[])
    for h,windows in remaining['calendar_windows_with_no_job_yet'].items():
        created=profiles[h]['created_at'];keep=[]
        for w in windows:
            if w['end_time']<=created:excluded.append(w)
            else:keep.append(w)
        remaining['calendar_windows_with_no_job_yet'][h]=keep
    remaining.update({'title':'Day2 reserve close — exact unfinished jobs for Nov26 08:00 Asia/Shanghai continuation','written_at_shanghai':packed_at,'stop_reason':'reserve_reached','excluded_precreation_calendar_windows':excluded})
    remaining['incremental_snapshot']['status']='All five fixed windows terminal: TA/THANK empty tails batch44; SF last empty tail batch77; III/Wang earlier. Do not reopen.'
    remaining['incremental_snapshot']['proposed_next_unstarted_fixed_window']={'start_time':'2026-11-25T00:35:00Z','end_time':'2026-11-25T23:59:00Z','end_shanghai':'2026-11-26 07:59:00 Asia/Shanghai','status':'unstarted proposal for next reset, not a completed read','query_per_handle':'from:<handle>','next_token':None,'note':'60s buffer before requested08:00 continuation. Carry this exact end forward if used; do not claim Nov26 posts captured now.'}
    remaining['notes']=[
      'True budget stop:75 daily reads remain,0 usable to reserve. No new collection before reset or explicit changed budget. No pending fetched pages.',
      'Reset Nov26 08:00 Asia/Shanghai. No routine was created here; previous routine fired/deleted itself.',
      'Continue current saved open dated jobs after reset, then unstarted pending/no-job months. Do not rewalk overlapping recent timeline tokens while monthly coverage is terminal.',
      'Both new accounts2026 Jan-Nov terminal through captured bounds. TA all2025 terminal. THANK2025 March remains open; other2025 months terminal.',
      'SF2025 May/June/July and III2026 July/September/Aug01to27 terminal. All Wang2016Dec/2017months and2018Jan-Oct/2019Aug priority tails terminal.',
      'SF2024 March/June/July/August/September open. TA2024 September/October/November open. THANK2024 April/July open. Tokens/query/bounds copied exactly below.',
      'Do not open redundant SF pending2026Nov. Never reuse exhausted/stalled parents, including III2026Aug and SF2023Sep/2026Jul. Unproven Wang2012-2014 requires a separately documented coverage audit, not blind parent-token reuse.',
      'Former calendar no-job list contained17 months before Wang account creation; retained in excluded_precreation_calendar_windows, removed from actionable gap counts. No posts were removed.',
      'Prior ZIPs immutable. No GitHub writes. PR1 merged main fb75058962f33f1c176f0297e47eb4cfde74d929; parent later uses NEW PR from main, no merge authorization.',
      'Audited inherited corrections only: literal U+2028 restored in one SF post;3 pinned-post provenance path corrections. See day2_literal_corrections.json.',
      'Synthesis is selective, source-linked and explicitly partial, not a manual reread of34913 posts. Performance and underlying market facts remain unverified unless explicitly sourced.'
    ]
    for name in ['remaining_jobs_day2.json','DAY2_FINAL_REMAINING_JOBS.json']:(logs/name).write_text(json.dumps(remaining,ensure_ascii=True,indent=2)+'\n')
    resume=json.loads((logs/'RESUME_OPEN_JOBS.json').read_text());resume.update({'notes':remaining['notes'],'stop_reason':'reserve_reached','authority':'remaining_jobs_day2.json + expand_jobs.json; frozen package snapshot DAY2_FINAL_REMAINING_JOBS.json','next_action':'Finalize day2 package now; collection can resume after Nov26 reset using exact current jobs.'});(logs/'RESUME_OPEN_JOBS.json').write_text(json.dumps(resume,ensure_ascii=True,indent=2)+'\n')
    nf=json.loads((logs/'NEXT_FIRE.json').read_text());nf.update({'usable':0,'stop_reason':'reserve_reached','next_action':'No scheduled routine; after reset use remaining_jobs_day2.json, not stale prior fire instructions.'});(logs/'NEXT_FIRE.json').write_text(json.dumps(nf,ensure_ascii=True,indent=2)+'\n')
    summary={'packaged_at_shanghai':packed_at,'pass':'day2-final-five-handles','claim_complete_retrieval':False,'unique_total':budget['unique_total'],'added_day2':budget['unique_total']-15370,'day2_calls_ingested':budget['calls_this_chunk'],'last_collection_footer':budget['authoritative_footer'],'daily_remaining':75,'reserve':75,'stopping_reason':'Real live75-read reserve reached; explicitly partial, not all windows exhausted. No pending ingest.','daily_reset_shanghai':'2026-11-26 08:00 Asia/Shanghai','remaining_jobs':'logs/DAY2_FINAL_REMAINING_JOBS.json','day1_footer':'X reads left for this user: 23 of 30 this minute (resets at 2026-11-24T12:33:00.000Z), 61 of 1000 today (resets at 2026-11-25T00:00:00.000Z).','accounts':{}}
    alltypes=Counter()
    for h in HANDLES:
        posts=load_posts(h);assert len(posts)==budget['unique_posts'][h]
        stats=write_archives(h,posts);alltypes.update(stats['types'])
        own=[j for j in jobs if j['handle']==h];openj=[j for j in own if j['status']=='open'];pending=[j for j in own if j['status']=='pending'];unproven=[j for j in own if j['status'] in ('pagination_stalled','not_proven_exhausted')]
        manifest={'handle':h,'user_id':profiles[h]['id'],'packaged_at_shanghai':packed_at,'claim_all_tweets':False,'unique_posts_stored':len(posts),'profile_post_count_at_first_lookup':profiles[h]['public_metrics']['post_count'],'profile_not_refetched_day2':True,'post_count_is_not_a_missing_count_proof':True,'span_utc':[stats['first_utc'],stats['last_utc']],'span_shanghai':[stats['first_shanghai'],stats['last_shanghai']],'years_utc':stats['years'],'types':stats['types'],'earliest':{'id':stats['first_id'],'url':stats['first_url']},'latest':{'id':stats['last_id'],'url':stats['last_url']},'expand_job_status_counts':dict(Counter(j['status'] for j in own)),'windows':own,'open_or_blocked_windows':openj+unproven,'pending_window_labels':[j['label'] for j in pending],'calendar_windows_with_no_job_yet':remaining['calendar_windows_with_no_job_yet'][h],'coverage_notes':remaining['notes'],'stopping_reason':summary['stopping_reason'],'last_collection_footer':budget['authoritative_footer']}
        (ROOT/h/'coverage_manifest.json').write_text(json.dumps(manifest,ensure_ascii=True,indent=2)+'\n')
        md=[f'# @{h} coverage — day2 reserve close','',f'Written {packed_at} (Asia/Shanghai). **Explicitly partial.** {len(posts):,} unique posts. Profile lookup lifetime count {profiles[h]["public_metrics"]["post_count"]:,} is not a missing-count proof. Profile not refreshed on day2.','',f'Stored span: {stats["first_shanghai"]} → {stats["last_shanghai"]}.','',f'Types: {dict(stats["types"])}.','', '## UTC year indexes','', '| UTC year | Captured posts | Archive |','|---|---:|---|']
        md += [f'| {y} | {n} | [full text](archives/{y}.md) |' for y,n in stats['years'].items()]
        md += ['','## Exact open / blocked windows','', '| Window | Status | start_time UTC | end_time UTC | Next token |','|---|---|---|---|---|']
        md += [f'| {j["label"]} | {j["status"]} | `{j.get("start_time")}` | `{j.get("end_time")}` | `{j.get("next_token")}` |' for j in openj+unproven]
        md += ['',f'Pending jobs ({len(pending)} including blocked overlaps if present): '+', '.join(j['label'] for j in pending),'',f'Additional calendar months with no job yet: {len(remaining["calendar_windows_with_no_job_yet"][h])}. Exact bounds in JSON.','',f'Job status counts: {manifest["expand_job_status_counts"]}.','', '## Terminal windows','',', '.join(j['label'] for j in own if j['status']=='exhausted'),'', '## Interpretation limits','', '- Terminal means this saved API query/window/pagination returned a terminal result, not all public account history recovered.','- Open recent timeline tokens can overlap exhausted monthly searches; do not rewalk blindly.','- Empty search windows are not proof of inactivity or deleted-post counts. Missing, protected, withheld or inaccessible posts cannot be inferred.','- Text-equal posts with distinct IDs remain distinct. Reposts preserve their attribution/expanded reference, not an invented original authorship.','- See analysis.md for selective dated synthesis, not a claim every post was manually read.','- Collection stopped at the real75-read reserve; next daily reset Nov26 08:00 Asia/Shanghai.','- Source-of-truth continuation: ../logs/remaining_jobs_day2.json and ../logs/expand_jobs.json. Frozen package snapshot: ../logs/DAY2_FINAL_REMAINING_JOBS.json.']
        (ROOT/h/'coverage_manifest.md').write_text('\n'.join(md)+'\n')
        prov={'handle':h,'user_id':profiles[h]['id'],'profile_source':'../profiles.json plus profile.json; normalized public profile snapshot from day1; not refreshed day2','profile_raw_source_asset':profiles[h].get('profile_source_file'),'posts_source_tools':sorted(set(p['collection']['tool'] if 'tool' in p['collection'] else p['collection'].get('source_tool','unspecified') for p in posts)),'post_provenance':'Each normalized post.collection points to captured raw response under raw/ or ../_raw/. All literal text/provenance files validated.','author_id_checked':True,'canonical_account_url':f'https://x.com/{h}'}
        if profiles[h].get('profile_source_file'):
            source=Path(profiles[h]['profile_source_file'])
            if source.exists():
                dest=ROOT/h/'raw/profile_lookup_day1_response.txt';shutil.copyfile(source,dest);prov['portable_profile_raw_response']='raw/profile_lookup_day1_response.txt'
        (ROOT/h/'provenance.json').write_text(json.dumps(prov,ensure_ascii=True,indent=2)+'\n')
        (ROOT/h/'PROVENANCE.md').write_text(f'# @{h} provenance\n\nPublic profile snapshot is from24 Nov2026, not a new day2 lookup. Account id `{profiles[h]["id"]}` is checked against each stored top-level post. See `provenance.json`, per-post `collection`, `raw/`, and the root validation report. Original-three profile snapshots are normalized captures in `../profiles.json`; their original lookup asset is not reconstructed. The two later-added profiles retain their named original response where available. Repost/quote expansions remain separately attributed; a referenced writer is not relabeled as this handle.\n')
        summary['accounts'][h]={k:manifest[k] for k in ['user_id','unique_posts_stored','years_utc','types','span_shanghai','expand_job_status_counts','profile_post_count_at_first_lookup']}
    summary['types']=dict(alltypes)
    (ROOT/'collection_summary.json').write_text(json.dumps(summary,ensure_ascii=True,indent=2)+'\n')
    (logs/'EXPAND_STATUS.md').write_text(f'# Day2 reserve close\n\n{packed_at} Asia/Shanghai. **34,913** unique posts, **19,543** added versus immutable day1 ZIP. **924** day2 collection calls ingested, no pending responses. Last live footer:75 daily remain; reset **26 Nov2026 08:00 Asia/Shanghai**. Collection is stopped at real reserve, not complete. Current continuation manifest `remaining_jobs_day2.json`; frozen package copy `DAY2_FINAL_REMAINING_JOBS.json`. Day1 snapshot remains historical. No GitHub writes; earlier PR1 is merged, future integration requires a NEW PR from main.\n')
    ck=json.loads((logs/'DAY2_CONTEXT_CHECKPOINT.json').read_text());ck.update({'stop_reason':'reserve_reached','no_job_windows':sum(len(v) for v in remaining['calendar_windows_with_no_job_yet'].values()),'excluded_precreation_windows':len(excluded),'next_action':'Collection STOPPED at75 reserve. Finalize analyses/archives/package on disk; resume collection only after next reset.','no_day2_package_yet':True});(logs/'DAY2_CONTEXT_CHECKPOINT.json').write_text(json.dumps(ck,ensure_ascii=True,indent=2)+'\n')
    print(json.dumps({'counts':budget['unique_posts'],'total':budget['unique_total'],'types':dict(alltypes),'open':len(remaining['open_windows']),'pending_actionable':len(remaining['pending_windows']),'no_job_actionable':sum(len(v) for v in remaining['calendar_windows_with_no_job_yet'].values()),'excluded_precreation':len(excluded)},indent=2))

if __name__=='__main__':main()
