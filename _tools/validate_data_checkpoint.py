#!/usr/bin/env python3
import json, zipfile, hashlib, collections, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
ROOT=Path('/workspace/x-research')
sys.path.insert(0,str(ROOT/'_tools'))
from ingest_page import HANDLES
z=zipfile.ZipFile('/workspace/x-research-day1-final.zip')
out={'written_at_shanghai':datetime.now(timezone(timedelta(hours=8))).isoformat(),'baseline_zip':'/workspace/x-research-day1-final.zip','accounts':{},'corrections_audit':'logs/day2_literal_corrections.json'}
for aid,h in HANDLES.items():
 p=ROOT/h/'normalized/posts.jsonl';text=p.read_text();lines=[l for l in text.split('\n') if l];rows=[json.loads(l) for l in lines];cur={x['id']:x for x in rows}
 baseline=[json.loads(l) for l in z.read('x-research/'+h+'/normalized/posts.jsonl').decode().split('\n') if l]
 changed=collections.Counter();missing=[];textchanges=[]
 for b in baseline:
  if b['id'] not in cur:missing.append(b['id']);continue
  n=cur[b['id']]
  for k in set(b)|set(n):
   if b.get(k)!=n.get(k):
    changed[k]+=1
    if k in ('text','full_text'):textchanges.append({'id':b['id'],'field':k})
 by_page={};prov=[];mismatch=[]
 for x in rows:
  page=ROOT/h/(x.get('collection',{}).get('page_file') or 'UNSET')
  if not page.is_file():prov.append(x['id']);continue
  by_page.setdefault(page,[]).append(x)
 for page,rs in by_page.items():
  obj=json.loads(page.read_text());obj=obj.get('response',obj);data={str(x['id']):x for x in obj.get('data',[])}
  for x in rs:
   raw=data.get(x['id'])
   if raw is None or raw.get('text','')!=x['text']:mismatch.append(x['id'])
 v={'count':len(rows),'baseline_count':len(baseline),'added':len(rows)-len(baseline),'duplicate_ids':len(rows)-len(cur),'nonstring_ids':sum(not isinstance(x['id'],str) for x in rows),'author_mismatches':sum(x['author_id']!=aid or x['author_username'].lower()!=h.lower() for x in rows),'missing_baseline_ids':missing,'changed_baseline_fields':dict(changed),'changed_baseline_text':textchanges,'missing_provenance_files':prov,'raw_text_mismatches':mismatch,'control_char_lines':sum(any(ord(c)<32 for c in l) for l in lines),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 out['accounts'][h]=v
out['total']=sum(x['count'] for x in out['accounts'].values());out['added']=sum(x['added'] for x in out['accounts'].values())
out['pass']=all(not v[k] for v in out['accounts'].values() for k in ['duplicate_ids','nonstring_ids','author_mismatches','missing_baseline_ids','missing_provenance_files','raw_text_mismatches','control_char_lines'])
(ROOT/'logs/day2_validation_checkpoint.json').write_text(json.dumps(out,ensure_ascii=True,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['pass']
