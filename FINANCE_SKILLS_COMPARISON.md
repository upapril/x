# Finance-skills compared with the day-2 archive

**25 Nov 2026, Asia/Shanghai (GMT+8).** Stored posts: **34,913** unique ids (day 1 had 15,370; day 2 added 19,543). Still partial. This note puts those dated statements next to the vendored skill docs. It is not a ranking, a backtest, or a recommendation to trade.

The account-to-account comparison, without the skill docs, is [`FINANCE_COMPARISON.md`](FINANCE_COMPARISON.md). The reading guide is [`INSIGHTS.md`](INSIGHTS.md).

Vendored tree: [`vendor/finance-skills/`](vendor/finance-skills/) at upstream `a0850786e72aa23b92862f9f1635b0de506fe206`. License: MIT, Copyright (c) 2025 Alex Yang, unchanged. The skills were not installed or run.

## What the store can support now

| Account | Stored | Profile `post_count` | Dated statements this comparison uses | Do not generalize |
|---|---:|---:|---|---|
| @silverfang88 | 12,862 | 19,982 | 29 Dec 2023 next-story filter; 10 Jul 2025 Pump attention vs “以大搏小”; 19 Jun 2025 Circle “认知套利” | Open 2024-03 and 2024-06–09. Attention is not a verified fill. “认知套利” is not a hedged pair. |
| @iiiinvest | 4,712 | 4,858 | 3 Sep 2026 stop above 150, 4 Sep report that the stop filled, 5 Sep leveraged all-in advice for a small account; earlier “越跌越买” | One reported stop is not a portfolio rule. 2023–2025 stay thinner than 2026. |
| @alexandr_wang | 1,921 | 3,762 | 30 Jun 2017 customer-requirements reply; 3 Oct 2017 segmentation API reply. Operator, not a trader. | 2024–2026 months are still mostly the older samples. No finance system is in the posts. |
| @taresky | 8,551 | 34,003 | 28 Dec 2022 “只套利，不承担风险敞口”; 9 Nov 2024 he says he researched less-certain, longer-cycle exposure and accepts some drawdown; 15 Mar 2025 “风险杠杆” 0.25x vs 0.5x | 131 calendar months still have no job. The 2024 sentence limits a timeless reading of 2022. It does not prove the arb book ended, and the APY/drawdown lines stay unverified. |
| @thankUcrypto | 6,867 | 8,097 | 22 Jul 2024 “我又不马丁” beside copy-trading economics; 24 Nov 2026 “什么条件开” / “什么条件平” and, the same day, “相当于马丁一直加仓” | 2025-03 and 2024-04/07 are still open. 79 months have no job. Do not net the self-reported millions and the self-reported losses. |

## Skill docs versus those sentences

| Question | What a stored post says | What the vendored SEPA doc says |
|---|---|---|
| Add as price falls | @iiiinvest, 24 Nov 2026: “按照计划越跌越买” ([2125158673203048455](https://x.com/iiiinvest/status/2125158673203048455)) and 27 Mar 2026 “越跌越补” ([2037361082038362440](https://x.com/iiiinvest/status/2037361082038362440)). @thankUcrypto, 24 Nov 2026: “一路相当于马丁一直加仓” ([2125183975757119963](https://x.com/thankUcrypto/status/2125183975757119963)). | `sepa-strategy/SKILL.md`: “Never average down on a losing position.” Adds in that document are only to winners. |
| Refuse that pattern | @thankUcrypto, 22 Jul 2024: “我又不马丁” ([1815223717531918486](https://x.com/thankUcrypto/status/1815223717531918486)), in a post about stops, followers leaving, and profit-share income. | Same SEPA line. His 2024 sentence and his 2026 sentence disagree with each other. The skill does not settle which one he followed. |
| Write the condition first | @thankUcrypto, 24 Nov 2026, 17:11:52 GMT+8: “什么条件开” and “什么条件平” ([2125155429512855651](https://x.com/thankUcrypto/status/2125155429512855651)). @iiiinvest, 3 Sep 2026: full stop above 150 ([2095515428634464402](https://x.com/iiiinvest/status/2095515428634464402)), then 4 Sep he reports the stop was hit ([2095721109156995262](https://x.com/iiiinvest/status/2095721109156995262)). | SEPA: pre-define entry, stop, and size. The 3–4 Sep pair is his report of one short, not an audited fill tape. The 5 Sep post then tells a small account to use large leverage ([2096170727707648118](https://x.com/iiiinvest/status/2096170727707648118)). |
| No directional exposure | @taresky, 28 Dec 2022: “只套利，不承担风险敞口” ([1608095146834563072](https://x.com/taresky/status/1608095146834563072)). On 9 Nov 2024 he describes researching exposure that is less certain and longer cycle, and accepting drawdown ([1855145990510329859](https://x.com/taresky/status/1855145990510329859)). | SEPA is a directional Stage-2 method, not his arb book. His 15 Mar 2025 “风险杠杆” of 0.25x ([1900736043835683192](https://x.com/taresky/status/1900736043835683192)) is his label. Do not rewrite it as the skill’s `Risk Per Trade %` formula. |
| Attention versus a trade | @silverfang88, 10 Jul 2025: attention brings liquidity around Pump, and he still calls the setup “以大搏小” ([1943173189305274473](https://x.com/silverfang88/status/1943173189305274473)). 19 Jun 2025 Circle note is “认知套利,” including that familiarity can make you sell early ([1935565562832375826](https://x.com/silverfang88/status/1935565562832375826)). | No skill doc verifies those calls. “认知套利” keeps directional risk. |
| Operator, not a system | @alexandr_wang, 30 Jun 2017, asks about customer requirements ([880514207153741824](https://x.com/alexandr_wang/status/880514207153741824)). 3 Oct 2017 offers a human image-segmentation API ([915051465659400192](https://x.com/alexandr_wang/status/915051465659400192)). | Company-valuation docs are a different task from reading this account. |

The size formula in `sepa-strategy/SKILL.md`, `Shares = (Account Value × Risk Per Trade %) ÷ (Entry Price − Stop Price)`, and the bear-market 0% line are the skill file’s rules. None of the five accounts posted that formula. Do not invent a percent and assign it to them.

## Study checklist (ours)

1. Keep the timestamp, the exact words, and the market (NFT, SOXL, A-shares, basis, Pump) on the note.
2. Split explicit wording, interpretation, and a test you could run. The 3 Sep / 4 Sep iiiinvest pair is a public plan and a public loss report. It is not a verified brokerage statement.
3. Do not average “只套利,” “越跌越买,” “我又不马丁,” and “相当于马丁” into one method.
4. Self-reported P&L, APY, and challenge totals stay claims. Do not add them across posts.
5. Wang’s 2017 posts are customer and API chronology. Any trading use is an analogy we write, not his rule.

## Meta wording, unchanged by day 2

No new Meta page was read on day 2. HTML captured from https://www.meta.com/about/leadership/alexandr-wang/ on 24 Nov 2026 supports the Chief AI Officer title and a short vision sentence, and does not contain “first-ever,” “June 2025,” or “Meta Superintelligence Labs.” A retained packaging note attributes that longer sentence to the same URL. Scale’s 12 Jun 2025 page supports the investment, the board seat, the interim CEO, and “joining Meta to work on Meta’s AI efforts,” and does not use the CAIO title. See `public_sources_wang.md`.

## Still open

11 dated cursors remain open (silverfang 2024-03 and 2024-06–09; taresky 2024-09–11; thankUcrypto 2025-03, 2024-04, 2024-07). Two recent-timeline cursors overlap monthly coverage and should not be rewalked while those months are the live jobs. 93 pending jobs. 210 calendar months have no job yet (taresky 131, thankUcrypto 79). 17 pre-creation Wang month labels are excluded and are not missing posts. Next reset: **26 Nov 2026 08:00 Asia/Shanghai**. Exact tokens: `logs/DAY2_FINAL_REMAINING_JOBS.json`.
