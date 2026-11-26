# finance-skills vs the day3 X archive

**26 Nov 2026, Asia/Shanghai (GMT+8).** This note updates the 24 Nov 2026 document review of the public repo [himself65/finance-skills](https://github.com/himself65/finance-skills) against the day3 five-account archive in `/workspace/x-research`. Skills were **read as docs only** on 24 Nov 2026. They were **not installed, not executed, and not re-fetched** on day3. Star counts, push dates, and skill-doc wording below remain those of the 24 Nov 2026 review unless a sentence says otherwise. Nothing here is investment advice, and neither source proves profitability. No backtest was run or fabricated.

The original first-pass comparison file outside this tree is left untouched as a historical snapshot.

## 1. Repo overview (not re-verified on day3)

From the 24 Nov 2026 review of GitHub API + README on branch `main` (not by installing or running the skills): MIT-licensed “agent skills for financial analysis and trading”; docs site https://skills.himself65.com/; the site then described “24 skills” and about 3.6k stars while the README skill tables listed **26 named skills**. Both figures were recorded as written; this update does not guess why they differed and does not refresh them.

Market-analysis skills named in that README included `sepa-strategy` (SEPA/Minervini), valuation, earnings, ETF premium, options payoff, correlation, liquidity, and `yfinance-data`. Social-reader skills included `twitter-reader` (opencli / browser-session). The README warned: educational and informational only; not financial advice.

`sepa-strategy` docs, as reviewed then, give a structured decision process (stage, trend template, VCP/base, pivot, stop, size) and include an iron rule: **never average down on a loser.** Treat “Strong Buy Setup” language in that skill as a report template, not a signal with proven results. The position-size formula recorded in the earlier review was `Shares = (Account Value × Risk Per Trade %) ÷ (Entry − Stop)`. This package does not execute that formula on any captured trade and does not invent a Risk Per Trade percent for any of the five accounts.

## 2. What the day3 X analyses actually are

Source: each `analysis.md`, `coverage_manifest.md`, and this package's `collection_summary.json`. Day3 corpus (unique retrieved posts): @silverfang88 19,848; @iiiinvest 4,850; @alexandr_wang 3,625; @taresky 17,532; @thankUcrypto 7,851; total 53,706. Profile lookup lifetime counts (Wang 3,762, III 4,858, SF 19,982, taresky 34,003, thankUcrypto 8,097) are not missing-count proofs. The archive is still **explicitly partial**.

- **@alexandr_wang** — operator, not a presumed trader. Public voice of Scale AI’s founder and, in later captured posts and an inherited Meta leadership-page note, Meta-related role language. This is an executive/policy/product feed, not a trading journal. No fresh Meta-page verification was performed on day3; leadership-page wording lives in `public_sources_wang.md` and must not be conflated with packaging notes.
- **@iiiinvest** — Chinese-language live-trading commentator. Recurring **explicit** claims: trade a written plan; waiting/cash is a skill; dated 2026 plans around Nasdaq / SOXL / TQQQ / BTC, including “越跌越买” and “越跌越补.” Community plus referral and a “free” group that still requires a ticket. P&L and ranking figures are self-reported and unverified.
- **@silverfang88** — narrative commentator on crypto and later US stocks / AI themes. Recurring claims: play the next narrative; don’t participate without a cost/information advantage; dated 2023 scale-out recipe; also, on 6 Jun 2023, “很简单 越跌越买.” P&L is self-reported and unverified.
- **@taresky** — arb/technical operator whose 2022 “只套利，不承担风险敞口” slogan is qualified by January 2023 profit-side exposure language, 2024 uncertain-exposure research, and 2025 personal 0.25x risk-leverage comments. Self-reported returns are not a verified edge.
- **@thankUcrypto** — leveraged discretionary trading plus copy-trading/media economics. 2024 “不马丁” is in textual tension with 2026 averaging / “相当于马丁一直加仓” language.

The archive’s distinctive value is sourced, dated posts, identity and monetization context, tensions in the speakers’ own words, and explicit coverage limits. It does not itself back-test their trades or supply valuation models.

## 3. Overlaps and the disagreement that must stay explicit

| Theme | In the day3 X analyses | In finance-skills docs (24 Nov 2026 review) |
|---|---|---|
| Have a plan; don’t trade anxiety | @iiiinvest: written plans, “别焦虑” | SEPA: pre-define entry, stop, size, and skip if reward/risk < 2:1 |
| Waiting / cash is allowed | @iiiinvest: waiting as a skill | SEPA: only buy Stage 2; bear environment → 0% risk, no new positions |
| Earnings as a timing gate | @iiiinvest waits around named earnings in some plans | `earnings-preview` / `earnings-recap`; SEPA: avoid entries within 2 weeks of earnings |
| Hormuz / oil as a macro factor | @silverfang88 pin and later commentary list oil/Hormuz among themes | `hormuz-strait` skill (shipping, oil impact, insurance risk) |
| Prediction-market input | @silverfang88 affiliation and Polymarket use | `finance-sentiment` lists Polymarket among Adanos sources |
| AI-capex / mega-cap tape | Traders discuss NVIDIA / AI; Wang discusses the industry as an operator | Valuation/earnings skills — company models, not executive-voice analysis |
| Reading X | This archive is a collected, cited, paginated corpus | `twitter-reader` is a live opencli/browser-session workflow; it does not replace the existing archive |
| Redemption / venue plumbing | @taresky’s mint/redeem checklist | Not a core SEPA rule; data/venue tools may help *after* a thesis exists |

An important **disagreement**, not an overlap: SEPA’s documented “iron rules” say **never average down** on a loser. @iiiinvest’s retrieved posts include planned dip-buying (“越跌越买,” “越跌越补,” Leapmotor batches, adding SOXL at lower prices, a BTC 7万底线 plan). @silverfang88 (6 Jun 2023) and @thankUcrypto (Nov 2026) also use “越跌越买” in captured posts. The two families of source make that conflict explicit; they do not settle which rule is better.

@alexandr_wang does not supply a competing averaging rule. Do not force-fit SEPA or dip-buying onto his operator feed.

## 4. What finance-skills adds that the tweet analyses do not

These are documented agent workflows from the earlier review, not tested strategies and not a guarantee of better results. They were not run here.

1. A formal valuation stack and earnings/estimate checklists.
2. A complete SEPA/Minervini scorecard and the position-size formula quoted above.
3. Market-structure tools the posts do not systematically teach: liquidity, correlation/pairs, ETF premium vs NAV, options payoff charts.
4. Optional data connectors the archive does not include (Fintel, TradingView wrappers, Hyperliquid, yfinance) — listed, not installed.
5. A dedicated Hormuz monitor and a sentiment skill — useful as *question lists* against @silverfang88’s narrative, not as proof.

What the tweet analyses still uniquely provide: these five people’s actual wording over time, community/referral structures, inconsistent self-reported P&L, taresky’s dated slogan-vs-practice evolution, and coverage honesty about open/stalled/blocked windows. finance-skills has no historical archive of these accounts and no method for reconstructing their worldview.

`twitter-reader` remains a poor substitute for `/workspace/x-research`. It is a live, session-based reader with default limits of 10–20 posts, not a multi-year paginated archive, and it was not used here. This project’s collection used the public shared X MCP `search_posts_all` path, not opencli session reuse.

## 5. Complementary practical workflow (read-only; do not install unless separately authorized)

Use the two sources as a **journal and a checklist**, not as signals.

1. From each `analysis.md`, extract the person’s stated rules and tensions, with post URLs. Keep unverified P&L labeled as claims.
2. For @iiiinvest, @silverfang88 and @thankUcrypto, run those rules against the SEPA docs as a critique sheet: Is there a stage and a defined stop? Is size derived from risk, or from a dollar headline? Is this “越跌越买” or a planned pyramid into a winner? Is the tape bull, choppy, or bear by the skill’s own criteria?
3. For @taresky, use the skill docs only as a reminder to map venue/redemption/liquidation risk; do not relabel his arb posts as SEPA setups.
4. For @alexandr_wang, keep the X analysis as the record of his public arguments. Company-valuation or earnings skills can be used later on Meta or Scale as issuers; that is a different task from understanding the account, and it is not authorized or performed here.
5. If testing a rule, use a proper backtest or paper journal. finance-skills is not itself a backtester, and this package does not invent one.
6. Do not install the plugin, opencli, or browser-session tools unless the user clearly authorizes that install.

## 6. Limits of this update

- Skills were not re-read from GitHub on day3; wording and repo stats are inherited from the 24 Nov 2026 review plus the day3 X corpus.
- No install, no execution, no runtime verification, no fork, and no vendored copy of finance-skills into this tree.
- No profitability, ranking, or “works in live trading” claim is supported by either source as reviewed here.
