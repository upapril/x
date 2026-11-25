# @silverfang88 coverage — day2 reserve close

Written 2026-11-25T09:42:30.677345+08:00 (Asia/Shanghai). **Explicitly partial.** 12,862 unique posts. Profile lookup lifetime count 19,982 is not a missing-count proof. Profile not refreshed on day2.

Stored span: 2021-09-13 14:35:07 GMT+8 → 2026-11-25 00:13:43 GMT+8.

Types: {'repost': 745, 'reply': 5334, 'quote': 1127, 'original': 5656}.

## UTC year indexes

| UTC year | Captured posts | Archive |
|---|---:|---|
| 2021 | 137 | [full text](archives/2021.md) |
| 2022 | 1914 | [full text](archives/2022.md) |
| 2023 | 3057 | [full text](archives/2023.md) |
| 2024 | 3837 | [full text](archives/2024.md) |
| 2025 | 2494 | [full text](archives/2025.md) |
| 2026 | 1423 | [full text](archives/2026.md) |

## Exact open / blocked windows

| Window | Status | start_time UTC | end_time UTC | Next token |
|---|---|---|---|---|
| 2024-03 | open | `2024-03-01T00:00:00Z` | `2024-04-01T00:00:00Z` | `b26v89c19zqg8o3fr5tenupng9quli5mpc13gghztaid9` |
| 2024-06 | open | `2024-06-01T00:00:00Z` | `2024-07-01T00:00:00Z` | `b26v89c19zqg8o3fr62eek5f4qrff1ul9ltd7re7e1u9p` |
| 2024-07 | open | `2024-07-01T00:00:00Z` | `2024-08-01T00:00:00Z` | `b26v89c19zqg8o3frqlvljape4hxiaccagk4pjjh0wu4d` |
| 2024-08 | open | `2024-08-01T00:00:00Z` | `2024-09-01T00:00:00Z` | `b26v89c19zqg8o3frqrrrru86cwk00i1t1o3gbb3xtnjx` |
| 2024-09 | open | `2024-09-01T00:00:00Z` | `2024-10-01T00:00:00Z` | `b26v89c19zqg8o3frqut8grgysui3mzlnxqnlyzly9da5` |
| 2023-09 | pagination_stalled | `2023-09-01T00:00:00Z` | `2023-10-01T00:00:00Z` | `b26v89c19zqg8o3fr5beqknfiduf3z8svkzzdfjkf2ttp` |
| 2026-07 | pagination_stalled | `2026-07-01T00:00:00Z` | `2026-08-01T00:00:00Z` | `b26v89c19zqg8o3juewg2tl5lpfe021lawn2fn8ar26pp` |

Pending jobs (13 including blocked overlaps if present): 2024-10, 2024-11, 2024-12, 2025-01, 2025-02, 2025-03, 2025-04, 2026-01, 2026-02, 2026-03, 2026-04, 2026-05, 2026-11

Additional calendar months with no job yet: 0. Exact bounds in JSON.

Job status counts: {'exhausted': 48, 'pagination_stalled': 2, 'open': 5, 'pending': 13}.

## Terminal windows

2021-09, 2021-10, 2021-11, 2021-12, 2022-01, 2022-02, 2022-03, 2022-04, 2022-05, 2022-06, 2022-07, 2022-08, 2022-09, 2022-10, 2022-11, 2022-12, 2023-01, 2023-02, 2023-03, 2023-04, 2023-05, 2023-06, 2023-07, 2023-08, 2023-09-01to14, 2023-10, 2023-11, 2023-12, 2024-01, 2024-02, 2024-04, 2024-05, 2025-05, 2025-06, 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12, 2026-06, 2026-08, 2026-09, 2026-10, 2026-11-01to08, 2026-11-08to25, 2026-07-01to26, day2-new-2026-11-24T12to25T0035

## Interpretation limits

- Terminal means this saved API query/window/pagination returned a terminal result, not all public account history recovered.
- Open recent timeline tokens can overlap exhausted monthly searches; do not rewalk blindly.
- Empty search windows are not proof of inactivity or deleted-post counts. Missing, protected, withheld or inaccessible posts cannot be inferred.
- Text-equal posts with distinct IDs remain distinct. Reposts preserve their attribution/expanded reference, not an invented original authorship.
- See analysis.md for selective dated synthesis, not a claim every post was manually read.
- Collection stopped at the real75-read reserve; next daily reset Nov26 08:00 Asia/Shanghai.
- Source-of-truth continuation: ../logs/remaining_jobs_day2.json and ../logs/expand_jobs.json. Frozen package snapshot: ../logs/DAY2_FINAL_REMAINING_JOBS.json.
