#!/usr/bin/env python3
"""Refresh exact day2 continuation state from disk; no API reads, analysis, or packaging."""
import json, collections, hashlib, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
r=Path('/workspace/x-research');logs=r/'logs';now=datetime.now(timezone(timedelta(hours=8))).isoformat()
reason=sys.argv[1] if len(sys.argv)>1 else 'context_checkpoint_not_budget_stop'
e=json.loads((logs/'expand_jobs.json').read_text());b=json.loads((logs/'live_budget.json').read_text());m=json.loads((logs/'remaining_jobs_day2.json').read_text());jobs=e['jobs']
blocked=[j for j in jobs if j['status']=='pending' and j['handle']=='silverfang88' and j['label']=='2026-11'];pending=[j for j in jobs if j['status']=='pending' and j not in blocked]
priority=[j for j in jobs if j['status']=='open' and j['handle'] in ('taresky','thankUcrypto') and j['label']!='timeline-recent']
priority=sorted(priority,key=lambda j:(j['label'],j['handle']),reverse=True)
counts=b['unique_posts'];total=b['unique_total'];added=total-15370;remaining=b['daily_remaining'];usable=b['usable'];calls=b['calls_this_chunk']
next_batch=max(int(p.stem.split('batch')[-1]) for p in logs.glob('day2_batch[0-9]*.txt'))+1
notes=[
'Explicitly partial; collection has not reached reserve. Continue same-day DATA ONLY. A context checkpoint is not a budget stop.',
'Original high-priority SF2025May/Jun/Jul and III2026Jul/Sep/Aug01to27 exhausted; do not reopen exhausted or stalled parent/subwindow tokens.',
'Both new accounts now have all attempted2026 monthly windows Jan-Nov exhausted (November only through captured bound); not a claim all account history is complete. Fixed incremental end2026-11-25T00:35:00Z is also terminal for all five, after two empty tails captured in batch44.',
'Do not rewalk overlapping timeline-recent tokens while monthly searches cover their recent interval; keep formal open status honest.',
'Next: remaining open new-account2025 monthly tokens and Wang2017June tail; all new-account2025 months have jobs now. Then Wang2017Jul-Dec gaps and pending new-account2024 months/newer unstarted windows by value; lower-priority SF open2024 tokens remain. Do not duplicate terminal months.',
'No analysis, coverage/year-index/archive rebuild or new ZIP yet; day1 presentation/manifests remain stale by design until reserve reached.',
'Prior ZIPs immutable. No GitHub writes. PR1 merged into main fb75058962f33f1c176f0297e47eb4cfde74d929; parent later uses NEW PR from main, with no merge authorization.',
'Literal source corrections retained: one inherited U+2028 restored from captured raw and3 pinned relative provenance paths fixed; see day2_literal_corrections.json.',
'Validation checks strict JSONL, control escaping, dedup string IDs, author attribution, all original day1 IDs retained, and literal source text/provenance files. Changes vs immutable baseline are only the audited four inherited corrections.',
f'Latest budget{remaining} daily left,{usable} usable to75reserve; all{calls} day2 calls ingested. No pending fetched pages. Next batch{next_batch} after this checkpoint.',
'Next reset Nov26 08:00 Asia/Shanghai. No new routine created; prior routine fired/deleted itself.']
m.update({'written_at_shanghai':now,'stop_reason':reason,'authoritative_last_collection_footer':b['authoritative_footer'],'footer_captured_at_shanghai':b['written_at_shanghai'],'daily_remaining':remaining,'usable_to_reserve':usable,'counts':counts,'total':total,'new_since_day1':added,'collection_calls_this_day2_chunk':calls,'next_priority_open_jobs':priority,'pending_recent_priority':[j for j in pending if j['handle'] in ('taresky','thankUcrypto') and j['label'].startswith('2025-')],'open_windows':[j for j in jobs if j['status']=='open'],'pending_windows':pending,'do_not_start_overlapping_pending':blocked,'pagination_stalled_or_unproven':[j for j in jobs if j['status'] in ('pagination_stalled','not_proven_exhausted')],'exhausted_windows':[j for j in jobs if j['status']=='exhausted'],'all_jobs_snapshot':jobs,'notes':notes})
m['incremental_snapshot']['status']='exhausted all five; TA/THANK terminal tails confirmed batch44; do not reopen'
(logs/'remaining_jobs_day2.json').write_text(json.dumps(m,ensure_ascii=True,indent=2)+'\n')
for name in ('RESUME_OPEN_JOBS.json','live_budget.json'):
 p=logs/name;o=json.loads(p.read_text());o['stop_reason']=reason;o['checkpointed_at_shanghai']=now
 if name=='RESUME_OPEN_JOBS.json':o['notes']=notes
 p.write_text(json.dumps(o,ensure_ascii=True,indent=2)+'\n')
nf=json.loads((logs/'NEXT_FIRE.json').read_text());nf.update({'stop_reason':reason,'authority':'remaining_jobs_day2.json + expand_jobs.json; not a scheduled routine','updated_at_shanghai':now});(logs/'NEXT_FIRE.json').write_text(json.dumps(nf,ensure_ascii=True,indent=2)+'\n')
v=json.loads((logs/'day2_validation_checkpoint.json').read_text());assert v['pass'] and v['total']==total
summary={'written_at_shanghai':now,'stop_reason':reason,'live_footer':b['authoritative_footer'],'remaining':remaining,'usable_to75_reserve':usable,'count':total,'added_day2':added,'per_account':counts,'calls_day2':calls,'no_pending_ingest':True,'next_batch':next_batch,'remaining_manifest':'logs/remaining_jobs_day2.json','validation':'logs/day2_validation_checkpoint.json','literal_corrections':'logs/day2_literal_corrections.json','all_jobs_status_counts':dict(collections.Counter(j['status'] for j in jobs)),'no_job_windows':sum(len(v) for v in m['calendar_windows_with_no_job_yet'].values()),'prior_day1_zip_sha256':hashlib.sha256(Path('/workspace/x-research-day1-final.zip').read_bytes()).hexdigest(),'no_day2_package_yet':True,'next_action':'Continue DATA ONLY current new-account historical and2025 monthly tokens, then recent pending months, then Wang/lower priorities; stop around75 remaining before analyzing/packaging.'}
(logs/'DAY2_CONTEXT_CHECKPOINT.json').write_text(json.dumps(summary,ensure_ascii=True,indent=2)+'\n');print(json.dumps(summary,indent=2))
