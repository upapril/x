# Day2 package extraction and verification

This snapshot contains34,913 unique IDs,19,543 added since day1. Explicitly partial. Collection stopped at last-verified75 daily reads at25Nov2026 09:36 Asia/Shanghai; next reset26Nov08:00 Asia/Shanghai.

The complete new local archive is `x-research-day2-final.zip`. If it exceeds25MB, delivery volumes are `x-research-day2-final-partNN.zip`, each independently extractable and below25,000,000bytes. Extract **all** numbered volumes to the same destination; their disjoint entries share root `x-research/`. No need to concatenate binary chunks. The adjacent `x-research-day2-final-artifacts.json` records exact filenames, bytes, SHA256 and validation. Use either the complete archive OR all delivery volumes, not both.

`FILE_SHA256SUMS.json` checks every included file except itself. ZIPs are CRC-tested and all entries compared by SHA256 to disk. Excludes backup files, Python bytecode/cache. All four older ZIPs are unchanged and outside this tree.

Methods: METHODOLOGY.md. Analyses: INSIGHTS.md, FINANCE_COMPARISON.md and each account analysis.md. Frozen unfinished jobs: logs/DAY2_FINAL_REMAINING_JOBS.json. Historical day1 narratives are labeled snapshots, not live authority. No GitHub writes; future integration requires NEW PR from main, not mergedPR1.
