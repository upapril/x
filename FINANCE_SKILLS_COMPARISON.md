# Finance-skills compared with the day-1 archive

**Written:** 24 Nov 2026 (Asia/Shanghai, GMT+8), after the day-1 close (15,370 posts, five accounts).

This note compares the vendored docs in [`vendor/finance-skills/`](vendor/finance-skills/) with the stored posts and [`INSIGHTS.md`](INSIGHTS.md). Earlier drafts used 1,232 and then 8,100 posts. Those ids are still here. Nothing here is investment advice, a backtest, or proof that anyone has an edge.

Upstream of the vendored tree: https://github.com/himself65/finance-skills at `a0850786e72aa23b92862f9f1635b0de506fe206`. License: MIT, Copyright (c) 2025 Alex Yang, file unchanged. The skills were not installed or run.

## Current evidence, not the first-pass sample

| Account | Stored posts | Profile `post_count` | What this store is strong enough to say | Still thin or unopened |
|---|---:|---:|---|---|
| @alexandr_wang | 1,873 | 3,762 | Operator voice through 2023 is much denser (2023 is 352 posts, every 2023 month marked exhausted). The 1 Jul 2025 CAIO post and the 23 Nov 2026 safety post are still his wording. Not a trader. | 2012–2014 not proven exhausted. 2018-01–10 and 2019-08 still open. 2024–2026 are still the older samples (50 / 75 / 161). |
| @iiiinvest (电鱼哥) | 3,856 | 4,858 | 2026 is now deep (3,321 posts), including the plan-and-add lines. 2022 is 408. | 2023–2025 stay thin (37 / 21 / 69). Open: 2024-03, 2024-04, 2026-07, 2026-09, 2026-08-01to27. Pending through mid-2025. |
| @silverfang88 (子时) | 9,239 | 19,982 | 2021–2023 remain the deep rotation corpus. 2025 is now 1,469 posts and 2026 is 1,422, so the old “2025 is 25 posts” limit no longer applies. | 2024-10–12, 2025-01–04, and several 2026 months are still pending. 2025-05–07 and parts of 2024 are open. 2023-09 and 2026-07 are stalled. |
| @taresky | 224 | 34,003 | A thin first sample that contains one explicit 28 Dec 2022 rule: “只套利，不承担风险敞口” ([1608095146834563072](https://x.com/taresky/status/1608095146834563072)). | 224 of 34,003. Almost every opened window still has a next token. 2025–2026 pages in this sample do not restate the arb rule. That is a gap, not proof he stopped. |
| @thankUcrypto | 178 | 8,097 | A thin first sample. 24 Nov 2026 states open/close conditions ([2125155429512855651](https://x.com/thankUcrypto/status/2125155429512855651)) and, the same day, a martingale-like A-share add he then drops ([2125183975757119963](https://x.com/thankUcrypto/status/2125183975757119963)). | 178 of 8,097. Pre-2025 is a sliver. Do not write a 2016–2024 style history from it. |

Total stored: **15,370**. That is not all tweets. Details: each `coverage_manifest.md` and `logs/remaining_jobs_day1.json`.

## What each source is for

The archive is dated public wording, with coverage limits. [`INSIGHTS.md`](INSIGHTS.md) is **our** study checklist for reading those feeds. It is not their rulebook.

`vendor/finance-skills` is a set of agent-skill documents: valuation and earnings checklists, a SEPA/Minervini scorecard, liquidity and correlation notes, options payoff, and read-only data connectors. The README says the project is educational and is not financial advice. Linking or vendoring it is not authorization to install it.

## Overlaps (same question, different source)

| Question | In the stored posts | In the vendored skill docs |
|---|---|---|
| Have a plan before you act | @iiiinvest, 24 Nov 2026, 17:24:45 GMT+8: “只要有计划就按照计划操作，别焦虑，别害怕” and “按照计划越跌越买” ([2125158673203048455](https://x.com/iiiinvest/status/2125158673203048455)). | SEPA docs say to pre-define entry, stop, and size, and to skip a trade when reward/risk is under 2:1 (`plugins/market-analysis/skills/sepa-strategy/references/entry-rules.md`). |
| Cash and waiting are allowed | @iiiinvest’s retrieved lines include waiting and “暂不持仓” in the 2026 sample discussed in `iiiinvest/analysis.md`. | Bear environment: risk per new trade is 0% and max positions are 0 (`sepa-strategy/SKILL.md`). |
| Earnings as a clock | @iiiinvest’s November 2026 plans name NVIDIA earnings as a date to wait for. | `earnings-preview` / `earnings-recap` are document templates. SEPA says to avoid entries within two weeks of earnings. |
| A story plus a separate timing decision | @silverfang88’s 12 Oct 2026 pin holds both “这场AI游戏至少还要持续一年以上” and buying a midterm scare ([2109440726865985560](https://x.com/silverfang88/status/2109440726865985560)). | SEPA separates “Stage 2 trend” from “do not buy this week.” That is a checklist, not his pin. |
| Oil / Hormuz and prediction markets | The same pin lists oil and Hormuz. The profile shows a Polymarket Traders badge. | `hormuz-strait` and `finance-sentiment` are question lists and data wrappers. They do not confirm his narrative. |
| Reading X | This repository is the paginated store for these five accounts. | `twitter-reader` is a live, session-based reader. It was not used to build this archive and does not replace it. |
| Neutral vs directional | @taresky, 28 Dec 2022: “只套利，不承担风险敞口.” Self-reported APY and drawdown in the same thread are unverified. | SEPA is a directional Stage-2 trend method, not a market-neutral arb manual. Do not treat the skill as his 2022 book. |

## The conflict that should stay explicit

These are two different rules. This note does not pick a winner and does not backtest either one.

**SEPA skill, not a tweet.** `vendor/finance-skills/plugins/market-analysis/skills/sepa-strategy/SKILL.md` states: “Never average down on a losing position.” The position-sizing note repeats: “Never average down on a losing position. Adding to a loser is the fastest path to account destruction.” Adds, in that document, are only to winners, with decreasing size.

**@iiiinvest, dated posts, not a skill.** On 24 Nov 2026, 17:24:45 GMT+8, he wrote that he bought more SOXL lower and “按照计划越跌越买” ([2125158673203048455](https://x.com/iiiinvest/status/2125158673203048455)). A 27 Mar 2026 plan describes buying Leapmotor in batches, “越跌越补” ([2037361082038362440](https://x.com/iiiinvest/status/2037361082038362440)). Those lines are still in the deeper 2026 store. They are his statements about planned dip adds. They are not a published percent stop, and they are not evidence the adds made money.

**@thankUcrypto, same day, two different sentences.** At 17:11:52 GMT+8 he wrote “什么条件开” and “什么条件平” — why you open, on what condition, why you close, on what condition ([2125155429512855651](https://x.com/thankUcrypto/status/2125155429512855651)). At 19:05:18 GMT+8 he described an A-share path “300-700-1000-1400-2000，一路相当于马丁一直加仓” and said he is done buying individual A-shares ([2125183975757119963](https://x.com/thankUcrypto/status/2125183975757119963)). That is a stated process rule next to a described add-into-a-loser path. It is not a proven system, and the sample is 178 posts. Large self-reported wins and losses in the same window stay unverified and are not netted here.

**@taresky is a third stated approach, in one 2022 thread, not a fifth version of SEPA.** “只套利，不承担风险敞口” is the opposite of both dip-adds and of a directional breakout system. The bio text `2021~2025.6` is his dating of an arb window. The 2025–2026 pages in this 224-post sample do not repeat the rule. Do not generalize that into “he trades this way now.”

**@silverfang88 is not a third version of the same rule.** In the 2023 sample he talks about buying strength and scaling out (see `silverfang88/analysis.md`). The 12 Oct 2026 pin talks about entering low after a scare. The 27 Mar 2024 post is a confession of being fully positioned and wrong ([1772997321271173274](https://x.com/silverfang88/status/1772997321271173274)). Do not collapse “next story,” “buy strength,” and “越跌越买” into one method.

Our study line, which is **ours** and not attributed to them or to the skill authors: if a note says “add as it falls,” write the condition that ends the add before you copy the behavior. The skill’s formula `Shares = (Account Value × Risk Per Trade %) ÷ (Entry Price − Stop Price)` is a SEPA document formula. Neither trading account posted that formula. Do not invent a risk percent and assign it to them.

## What the skill docs add

These are workflows in the vendored markdown, not tested results.

1. A valuation stack (DCF, peers, SOTP, scenarios) and earnings/estimate checklists.
2. The SEPA scorecard: stage, trend template, base, pivot, stop, and the size formula above, plus the bear-market 0% rule.
3. Liquidity, correlation, ETF premium, and options-payoff notes the posts do not teach as a system.
4. Connectors the archive does not include: yfinance, Fintel, TradingView, Hyperliquid, Adanos. They were not run.

What the posts still add, and the skills do not: these three people’s wording over time, the referral and “免费” ticket structure, separate unverified P&L claims, and an explicit list of months that were not collected.

## How to use both without mixing authors

1. From `analysis.md` and `INSIGHTS.md`, copy only sentences that have a post URL. Label P&L and ranks as claims.
2. Put @iiiinvest’s dip-add posts next to the SEPA “never average down” lines and write which rule **you** are testing. Do not say either man, or the skill file, proved the other wrong.
3. For an earnings date they mention, the earnings-preview doc is a template for questions. It does not fill in the numbers.
4. For @silverfang88’s midterm / AI / Hormuz pin, the Hormuz and sentiment docs are ways to list what would confirm or break the story. A skill report would not be confirmation, and none was run.
5. For @alexandr_wang, keep the X file as the record of a company operator. The 1 Jul 2025 post is his CAIO announcement. Scale’s 12 Jun 2025 page does not use that title. Two HTML captures of Meta’s leadership URL support the title and a short vision sentence, and do not contain “first-ever,” “June 2025,” or “Meta Superintelligence Labs.” A day-1 note attributes a longer sentence to the same URL. See `public_sources_wang.md`. Company-valuation docs applied to Meta or Scale would be a different task from reading his account.
6. The checklist in `INSIGHTS.md` section 5 is our reading method. Week-1 “don’t trade their ideas” and week-2 “your max loss, your instrument” are our instructions to a reader, not their position sizes and not a SEPA signal.
7. Do not install the plugin, opencli, or a browser session unless that install is separately authorized.

## Limits

- @taresky and @thankUcrypto are first samples. @silverfang88 still has open 2024 and early-2025 windows. @alexandr_wang’s 2024–2026 months were mostly not opened. A later batch, after the 25 Nov 2026 08:00 Asia/Shanghai reset, can change the emphasis. The day-1 footer left 61 of 1,000 daily reads.
- No return, rank, or win rate in the tweets or in the SEPA docs is treated here as a measured result. The skill’s “~50–55% win-rate framing” is the document’s framing, not a backtest we ran.
- Reuters URLs cited for Wang were not re-read (HTTP 401). See `public_sources_wang.md`.
