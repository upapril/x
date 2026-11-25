#!/usr/bin/env python3
"""New-only day2 package; immutable priors. ZIP CRC and per-file SHA validation."""
import hashlib,json,zipfile,fnmatch
from pathlib import Path
from datetime import datetime,timezone,timedelta
R=Path('/workspace/x-research');OUT=R.parent;STEM='x-research-day2-final';MAX=25_000_000
full=OUT/(STEM+'.zip');external=OUT/(STEM+'-artifacts.json')
assert not full.exists() and not external.exists(),'Never overwrite an existing artifact; choose a new stem.'
ckp=R/'logs/DAY2_CONTEXT_CHECKPOINT.json';ck=json.loads(ckp.read_text());ck.pop('no_day2_package_yet',None);ck.update({'state':'reserve_reached_finalization_complete_before_package_emission','next_action':'Collection stopped at75. Use new day2 artifact manifest beside ZIPs; resume exact remaining jobs after26Nov08:00 Asia/Shanghai reset.','artifact_manifest':str(external)});ckp.write_text(json.dumps(ck,ensure_ascii=True,indent=2)+'\n')
(R/'PACKAGE_README.md').write_text('''# Day2 package extraction and verification

This snapshot contains34,913 unique IDs,19,543 added since day1. Explicitly partial. Collection stopped at last-verified75 daily reads at25Nov2026 09:36 Asia/Shanghai; next reset26Nov08:00 Asia/Shanghai.

The complete new local archive is `x-research-day2-final.zip`. If it exceeds25MB, delivery volumes are `x-research-day2-final-partNN.zip`, each independently extractable and below25,000,000bytes. Extract **all** numbered volumes to the same destination; their disjoint entries share root `x-research/`. No need to concatenate binary chunks. The adjacent `x-research-day2-final-artifacts.json` records exact filenames, bytes, SHA256 and validation. Use either the complete archive OR all delivery volumes, not both.

`FILE_SHA256SUMS.json` checks every included file except itself. ZIPs are CRC-tested and all entries compared by SHA256 to disk. Excludes backup files, Python bytecode/cache. All four older ZIPs are unchanged and outside this tree.

Methods: METHODOLOGY.md. Analyses: INSIGHTS.md, FINANCE_COMPARISON.md and each account analysis.md. Frozen unfinished jobs: logs/DAY2_FINAL_REMAINING_JOBS.json. Historical day1 narratives are labeled snapshots, not live authority. No GitHub writes; future integration requires NEW PR from main, not mergedPR1.
''')
def files():
 return sorted((p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and not fnmatch.fnmatch(p.name,'*.bak*')),key=lambda p:str(p.relative_to(R)))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
entries={str(p.relative_to(R)):digest(p) for p in files() if p.name!='FILE_SHA256SUMS.json'}
(R/'FILE_SHA256SUMS.json').write_text(json.dumps({'algorithm':'SHA256','scope':'All packaged files except this manifest itself; cross-check with adjacent artifact manifest for ZIP hashes.','files':entries},ensure_ascii=True,indent=2)+'\n')
ps=files();allsha={str(p.relative_to(OUT)):digest(p) for p in ps}
with zipfile.ZipFile(full,'x',zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
 for p in ps:z.write(p,p.relative_to(OUT))
with zipfile.ZipFile(full) as z:
 assert z.testzip() is None
 for name,sha in allsha.items():assert hashlib.sha256(z.read(name)).hexdigest()==sha,name
 infos=z.infolist()
 if full.stat().st_size>=MAX:
  groups=[];group=[];size=0
  for info in infos:
   estimated=info.compress_size+len(info.filename.encode())*2+200
   assert estimated<24_000_000,info.filename
   if group and size+estimated>24_000_000:groups.append(group);group=[];size=0
   group.append(info.filename);size+=estimated
  if group:groups.append(group)
  parts=[]
  for n,g in enumerate(groups,1):
   path=OUT/f'{STEM}-part{n:02d}.zip';assert not path.exists()
   with zipfile.ZipFile(path,'x',zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as part:
    for name in g:part.writestr(name,z.read(name))
   assert path.stat().st_size<MAX
   with zipfile.ZipFile(path) as part:
    assert part.testzip() is None
    for name in part.namelist():assert hashlib.sha256(part.read(name)).hexdigest()==allsha[name]
   parts.append(path)
  assert [name for g in groups for name in g]==[i.filename for i in infos]
 else:parts=[full]
for name,sha in allsha.items():assert digest(OUT/name)==sha,('disk changed while packaging',name)
previous={'x-research-firstpass.zip':'455936b9cb14f9e9f5f899510342c03dea127ad3b868e60da825cf9f868ec976','x-research-expanded.zip':'d601957063b3610067d2dafd6cab0a6effb63e771bd642df57233b5e44fee6c7','x-research-latest.zip':'1ab3fc4aaee8667c42d833543a85f86f54ff9dabe165f6305d56769aed4d8e58','x-research-day1-final.zip':'537597c2d1c295f18773fb2099d751338f78a354be982b65a26aaf7367efea37'}
for name,sha in previous.items():assert digest(OUT/name)==sha
meta={'created_at_shanghai':datetime.now(timezone(timedelta(hours=8))).isoformat(),'explicitly_partial':True,'total_unique_posts':34913,'added_day2':19543,'per_account':{'silverfang88':12862,'iiiinvest':4712,'alexandr_wang':1921,'taresky':8551,'thankUcrypto':6867},'collection_stop':'true75-read reserve reached; last verified25Nov2026 09:36 Asia/Shanghai','remaining_daily':75,'usable_to_reserve':0,'calls_day2_ingested':924,'files_packaged':len(ps),'full_archive':{'path':str(full),'bytes':full.stat().st_size,'sha256':digest(full)},'delivery_artifacts':[{'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)} for p in parts],'independently_extractable_delivery_volumes':True,'extract_instruction':'Extract all delivery volumes to same destination; disjoint files under x-research/. Full archive is an optional equivalent local copy.','all_delivery_files_under_25MB':all(p.stat().st_size<MAX for p in parts),'crc_all_pass':True,'all_packaged_files_sha256_match_disk':True,'global_ids_deduplicated':True,'raw_text_attribution_validation':'x-research/logs/day2_validation_checkpoint.json','final_validation':'x-research/logs/day2_package_validation.json','remaining_jobs':'x-research/logs/DAY2_FINAL_REMAINING_JOBS.json','next_reset_shanghai':'2026-11-26 08:00 Asia/Shanghai','prior_zips_unchanged':previous,'no_GitHub_writes':True}
external.write_text(json.dumps(meta,ensure_ascii=True,indent=2)+'\n');print(json.dumps(meta,indent=2))
