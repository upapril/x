# @silverfang88 coverage — day3 reserve close

Written 2026-11-26T09:39:36.364018+08:00 (Asia/Shanghai). **Explicitly partial.** 19,848 unique posts. Profile lookup lifetime count 19,982 is not a missing-count proof. Profile not refreshed on day3.

Stored span: 2021-09-13 14:35:07 GMT+8 → 2026-11-25 00:13:43 GMT+8.

Types: {'original': 8417, 'quote': 1569, 'reply': 9005, 'repost': 857}.

## UTC year indexes

| UTC year | Captured posts | Archive |
|---|---:|---|
| 2021 | 137 | [full text](archives/2021.md) |
| 2022 | 1914 | [full text](archives/2022.md) |
| 2023 | 3057 | [full text](archives/2023.md) |
| 2024 | 5475 | [full text](archives/2024.md) |
| 2025 | 6045 | [full text](archives/2025.md) |
| 2026 | 3220 | [full text](archives/2026.md) |

## Exact open / blocked / deferred / stalled windows

| Window | Status | start_time UTC | end_time UTC | Next token |
|---|---|---|---|---|
| 2026-11 | pending | `2026-11-01T00:00:00Z` | `2026-11-25T00:00:00Z` | `None` |
| 2023-09 | pagination_stalled | `2023-09-01T00:00:00Z` | `2023-10-01T00:00:00Z` | `b26v89c19zqg8o3fr5beqknfiduf3z8svkzzdfjkf2ttp` |
| 2026-07 | pagination_stalled | `2026-07-01T00:00:00Z` | `2026-08-01T00:00:00Z` | `b26v89c19zqg8o3juewg2tl5lpfe021lawn2fn8ar26pp` |

Pending labels: 2026-11.

## Notes

- Explicitly partial. Day3 collection stopped at the true 75-read daily reserve (usable 0). Not window exhaustion.
- Profile lookup lifetime counts are not missing-count proofs. Profiles were not refreshed on day3.
- Archives and this manifest were rebuilt from canonical normalized/posts.jsonl at day3 packaging.
- Never reuse stalled parents 2023-09 or 2026-07. Never open the blocked pending 2026-11 window. Other previously pending 2024–2026 monthly jobs walked on day3 are now exhausted as listed in remaining_jobs_day3.json.

Machine-readable companion: `coverage_manifest.json`. Remaining-job authority: `../logs/remaining_jobs_day3.json`.

