# Finance-skills compared with this expanded archive

**Written:** 24 Nov 2026 (Asia/Shanghai, GMT+8), after the expanded store was integrated.

This note compares the vendored docs in [`vendor/finance-skills/`](vendor/finance-skills/) with the stored posts and [`INSIGHTS.md`](INSIGHTS.md). The earlier review (`finance-skills-review`, 24 Nov 2026) used the first-pass analyses (512 / 366 / 354). Those counts are superseded. The post ids from that pass are still in this store. Nothing here is investment advice, a backtest, or proof that anyone has an edge.

Upstream of the vendored tree: https://github.com/himself65/finance-skills at `a0850786e72aa23b92862f9f1635b0de506fe206`. License: MIT, Copyright (c) 2025 Alex Yang, file unchanged. The skills were not installed or run.

## Current evidence, not the first-pass sample

| Account | Stored posts | Profile `post_count` | What this store is strong enough to say | Still thin or unopened |
|---|---:|---:|---|---|
| @alexandr_wang | 788 | 3,762 | Operator voice: Scale building, a 2020 authenticity **reply**, 2025 CAIO announcement on X, 2026 Muse posts and the 23 Nov 2026 safety clarification. Not a trader. | 115 pending months, 2017-05 through 2026-11. 2018–2023 year counts of 25 are year-end samples. 2012–2014 is one post and not proven exhausted. |
| @iiiinvest (电鱼哥) | 736 | 4,858 | 2022–early 2024 is much deeper than the first pass (2022 alone is 408 posts). The 2026 plan-and-add language is still in the store. | 2024-03 and 2024-04 are open. 30 months from 2024-06 through 2026-11 were never opened. 2025–2026 posts are mostly earlier samples plus the recent timeline. |
| @silverfang88 (子时) | 6,576 | 19,982 | 2021–2023 is largely monthly-exhausted (with 2023-09 stalled). Narrative rotation, the 2023 strength/scale-out wording, and the 2024 “满仓挨打” confession are now in a much larger corpus. | 2024-10 through most of 2025–2026 was never opened. **2025 is still 25 posts.** Open windows remain in 2024-03 and 2024-05 through 2024-09. |

Total stored: **8,100**. That is not all tweets. Details: each `coverage_manifest.md`.

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
| Reading X | This repository is the paginated store for these three accounts. | `twitter-reader` is a live, session-based reader. It was not used to build this archive and does not replace it. |

## The conflict that should stay explicit

These are two different rules. This note does not pick a winner and does not backtest either one.

**SEPA skill, not a tweet.** `vendor/finance-skills/plugins/market-analysis/skills/sepa-strategy/SKILL.md` states: “Never average down on a losing position.” The position-sizing note repeats: “Never average down on a losing position. Adding to a loser is the fastest path to account destruction.” Adds, in that document, are only to winners, with decreasing size.

**@iiiinvest, a dated post, not a skill.** On 24 Nov 2026, 17:24:45 GMT+8, he wrote that he bought more SOXL lower and “按照计划越跌越买” ([2125158673203048455](https://x.com/iiiinvest/status/2125158673203048455)). A 27 Mar 2026 plan describes buying Leapmotor in batches, “越跌越补” ([2037361082038362440](https://x.com/iiiinvest/status/2037361082038362440)). Those are his statements about planned dip adds. They are not a published percent stop, and they are not evidence the adds made money.

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
5. For @alexandr_wang, keep the X file as the record of a company operator. The 1 Jul 2025 post is his CAIO announcement. Meta’s re-read leadership HTML supports the title and does not say “first” or “June 2025.” Company-valuation docs applied to Meta or Scale would be a different task from reading his account.
6. The checklist in `INSIGHTS.md` section 5 is our reading method. Week-1 “don’t trade their ideas” and week-2 “your max loss, your instrument” are our instructions to a reader, not their position sizes and not a SEPA signal.
7. Do not install the plugin, opencli, or a browser session unless that install is separately authorized.

## Limits

- 2025 for @silverfang88 and most post-2017 months for @alexandr_wang are still samples. A later batch can change the emphasis.
- No return, rank, or win rate in the tweets or in the SEPA docs is treated here as a measured result. The skill’s “~50–55% win-rate framing” is the document’s framing, not a backtest we ran.
- Reuters URLs cited for Wang were not re-read (HTTP 401). See `public_sources_wang.md`.
