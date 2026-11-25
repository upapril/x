#!/usr/bin/env python3
"""Evidence-linked day2 synthesis from existing captured records; no network."""
import json
from pathlib import Path
R=Path('/workspace/x-research')
H=['silverfang88','iiiinvest','alexandr_wang','taresky','thankUcrypto']
D={h:{p['id']:p for p in map(json.loads,filter(str.strip,(R/h/'normalized/posts.jsonl').read_text().split('\n')))} for h in H}
ledger=[]
def cite(h,i,quote=None):
 p=D[h][i];t=p.get('full_text') or p['text']
 if quote is not None:assert quote in t,(h,i,quote)
 ledger.append({'handle':h,'id':i,'date_shanghai':p['created_at_shanghai'],'url':p['canonical_url'],'literal_excerpt':quote,'post_type':p['post_type'],'provenance':p['collection']})
 return f"[{p['created_at_shanghai']}]({p['canonical_url']})"
def q(h,i,s):return f'“{s}” — {cite(h,i,s)}'
def head(h):
 return f'''# @{h} — day2 analysis, explicitly partial

**25 Nov 2026, Asia/Shanghai (GMT+8).** {len(D[h]):,} deduplicated captured posts. Start with `coverage_manifest.md`; archives are indexed by UTC year. Profile identity is public account wording only; no private legal-name inference. All performance, fills, forecasts, third-party allegations and market facts below remain the author's statements unless a separate source is expressly identified. This is an evidence-led reading guide, not an audited track record or investment advice. A post being present proves what the captured response says, not that the strategy worked or every underlying event occurred.

The earlier day1 narrative is retained as a **historical snapshot**, not current coverage authority, in `../logs/historical_narratives_day1/`. Source excerpts and author checks for this synthesis are in `../logs/day2_citation_ledger.json`.

'''
A={}
h='taresky'
A[h]=head(h)+f'''## Core idea and the most important day2 correction

**Interpretation:** a risk-budgeted arbitrage/technical operator, not a permanently exposure-free machine. The 224-post day1 sample was too thin to infer continuity from a 2022 manifesto. Day2 expands this to 8,551 posts: 2025 and 2026 are now substantial, while much pre-2024 history remains untouched. Dates show a change already underway in **2024**, not merely after the bio's `2025.6` endpoint.

## Chronological evidence

- **2022 baseline:** {q(h,'1608095146834563072','只套利，不承担风险敞口')} This is the rule then; the associated return/drawdown claims in {cite(h,'1608095141713305600')} are unverified.
- **9 Nov 2024 — explicit broadening:** {q(h,'1855145990510329859','今年不得不去研究一些风险敞口不那么确定的、周期又比较长的策略。')} The same post says {q(h,'1855145990510329859','并且可以接受一些回撤了')} This directly qualifies an absolute, timeless reading of the 2022 line. It is self-described adaptation, not evidence of dishonesty or of a specific loss.
- **9 Dec 2024 — documentation before opinion:** {q(h,'1866050575428931769','懂得自己亲手去验证的新人，比什么 KOL、老 OG 都强。')} His discussion of sUSDe/AAVE risk and arbitraging fear is not an audit of those protocols. The linked April article was not fetched in this pass.
- **15 Mar 2025 — personal risk budget:** {q(h,'1900736043835683192','实际的风险杠杆，算了下是 0.25 倍。')} He says he kept 0.25x rather than doubling potential profit at 0.5x, because a misunderstood outcome could create a large actual loss. This is **his undefined risk-leverage measure**, not necessarily exchange displayed leverage or a portable cap.
- **26 Jun 2025 — bounded exception, not zero exceptions:** {q(h,'1938213833245659239','带敞口的交易次数，可能每年不会超过 3 次。')} He lists ENA/CRV shorts and BTC long; his statement that he can hardly remember losing is not a verified sample or win rate.
- **1 Jul 2025 — execution plumbing:** {q(h,'1939870865598128476','前人没有解决好的有且只有一件事：mint/redeem。')} The post breaks this into who can mint/redeem, how quickly, and spread/depth/friction. That is a concrete how-to lens: authority, latency and exit mechanics before nominal yield.
- **21 Oct 2025 — capacity/yield assertion:** he calls an AAVE PT looping opportunity low risk and estimates capacity/APR in {cite(h,'1980458916095095131')}. Those estimates are not independently checked and do not establish risk-free return.
- **10 Nov 2025 — proposed revenue transition:** {q(h,'1987688205093896685','大概率明年的主要收入就不是 DeFi / 套利了。')} This is a forecast, not confirmation of revenue mix.
- **14 Sep 2026 — operating a token-reseller business:** {q(h,'2099292446035427479','做了快一个月 token 批发生意了')} He discusses upstream data/privacy tail risk and says {q(h,'2099292446035427479','我们不留数据，但也无法自证这一点。')} This supports a later public business focus, not the claim that 99% of all providers leak data; that percentage is his conjecture.

## Rules versus a researcher's how-to

**Stated:** focus on arb; admit only a few directional exceptions; keep personal risk leverage low enough to execute; inspect protocol documentation and redemption mechanics; abandon opportunities whose profit/risk/capacity does not fit. The low-risk pool return/drawdown summary in {cite(h,'1989164267254464681')} is an author self-report, not capital-verified P&L.

**Our study procedure, not his advertised system:** map every leg, collateral currency, borrow cost, funding path, redemption permission and latency; model a depeg/withdrawal freeze plus borrow-rate spike; record gross leverage separately from net delta and liquidation distance; calculate capacity after fees. Test the operational route in simulation, not by copying historical yield figures. The corpus does not supply full code, positions, hedge ratios or audited cash flows.

## Contradictions and limits

1. **2022 zero exposure vs 2024 uncertain exposure vs 2025 rare discretionary trades:** a dated evolution is now supported. Day1's gap is no longer merely absence of repeated slogans.
2. **Low-risk / zero-drawdown return claims vs admitted anxiety and tolerated mark-to-market drawdown:** dates, pools and denominators differ. Do not mechanically subtract them or allege a contradiction in the same fund without matching positions.
3. **“无风险” marketing language vs legal, venue, oracle, liquidity and privacy risks:** his own later posts acknowledge several non-price risks. “Arbitrage” does not remove tail risk.
4. Bio recommendations/affiliate links are a commercial context, not proof of bad faith. Public essays and t.co links are not automatically full strategy disclosure; attached media and linked articles were not all downloaded.

## Coverage and next work

All attempted Jan–Nov 2026 monthly searches terminated within saved bounds. All 2025 monthly jobs are terminal. Open 2024 Sep/Oct/Nov cursors remain; 2024 Jan–Aug and older pending/no-job months need work. The recent timeline cursor overlaps completed monthly searches and should not be wastefully rewalked. See exact tokens in the root continuation manifest. **No complete-history claim.**
'''
h='thankUcrypto'
A[h]=head(h)+f'''## Core operating model

**Interpretation:** discretionary, event/flow-aware leveraged trading plus a public copy-trading/media business. A trade's thesis, sizing, stop execution and the follower's experience are separate objects. The expanded corpus (178 → 6,867) makes both his techniques and his inconsistency more visible; it does not establish a profitable audited strategy.

## Chronology: process language, leverage and business pressure

- **14 Apr 2024:** {q(h,'1779446108114284635','降低回撤的办法，杠杆第一 止损计划第二 币种选择最后。')} This is a clear priority order: leverage before stop plan before coin choice, not a published numeric risk budget.
- **22 Jul 2024, copy-trading economics:** {q(h,'1815223717531918486','而且我又不马丁也不用期现套利的方式扛单和保持胜率')} In the same post he says losing followers leave after stops, reducing profit-share income, and advises separating media identity from copy-trading identity. He describes flow and reputational pressure, not merely chart signals. His assertions of near-total legal safety are **not legal advice** and are not endorsed here.
- **24 Jul 2024, project closure:** {q(h,'1815968167170277692','短线很影响睡眠，尤其带单仓位')} He says platform margin/follower-fill problems and responsibility for followers made the project exhausting. The neighboring near-duplicate id is preserved separately because id deduplication is not text deduplication. This is operational capacity evidence, not proof that the quoted 20,000% return occurred.
- **12 Mar 2025, “双损” explanation:** {q(h,'1899757201839038551','既挂了止损单，又同时爆仓损，不会亏到账户里其他保证金。')} He discusses stop slippage, margin removal and isolated margin. Crucially he also writes {q(h,'1899757201839038551','我是没养成这习惯的')} So this is a technique he explains, **not evidence he habitually used it**. Liquidation/isolated margin does not guarantee execution quality or remove exchange risk.
- **31 Mar 2025, observation is not execution:** {q(h,'1906622661045985514','从看到 到 做到相隔千里万里。知易行难。')} He lists inputs learned from other traders: long/short ratios, positions, funding, event thinking, CME gaps, ETF opening/closing prices and on-chain monitoring. His eventual return claims remain unverified.
- **13 Jun 2025, risk appetite expansion:** {q(h,'1933304425243947272','这轮我大饼开到10x doge开到5x，基本没啥心理压力')} This qualifies any reading of him as uniformly low-leverage; the accompanying stop confidence is not proof of bounded portfolio loss.
- **26 Jun 2025:** wide-stop pain in {cite(h,'1938259138863370368')} and {q(h,'1938297622181384628','做交易，永远要靠自己')} sit beside the follow-signal business.
- **2026 losses and re-entry:** the ETH-short loss report in {cite(h,'2066501986653221245')} and the pinned challenge wrap in {cite(h,'2091778918810612183')} must both remain visible. They cannot be netted into a track record.
- **24 Nov 2026:** entry/exit-condition language in {cite(h,'2125155429512855651')} contrasts with {q(h,'2125183975757119963','一路相当于马丁一直加仓')} about an A-share position. This is the strongest dated tension with the 2024 anti-martingale self-description. Different market, same account, not a proof that every crypto strategy was martingale.

## Core rules, and a safe way to study them

**Explicit public ideas:** leverage is the first drawdown lever; define exit conditions; study actual execution rather than admire other traders; adapt tools to one's own temperament; trading is probabilistic; copy-trading may add income but adds execution and social costs.

**Our how-to, not a recommended live trade:** take one dated idea and record its instrument, collateral, horizon, trigger, stop type, slippage assumption and maximum combined loss across accounts. Separate a planned scale-in from loss-driven doubling. For a copied trade, simulate follower fill latency, differing balances, venue limits and stop slippage. Log which rule was written *before* entry and which explanation arrived after the fact. Treat leverage labels as incomplete without notional/equity and collateral.

## Contradictions and uncertainty

1. **“不马丁” (2024) vs “相当于马丁一直加仓” (2026):** a real textual tension, not silently reconciled into one consistent system.
2. **Explain a protective technique vs use it:** his own disclaimer in the 双损 post prevents falsely attributing a standard risk-control habit.
3. **Be independent vs follow signals:** dependence is commercially encouraged and later criticized. The follower's stop/exit timing may differ from his.
4. **Low-leverage advice vs displayed high-leverage examples:** relative-to-whom comparisons are not risk limits.
5. **Large wins, large losses and survivorship:** no audited transfers, complete equity curves, fees, funding, withdrawals or denominator reconciliation. Repeated pasted summaries, screenshots and pinned celebrations are not independent verification.

## Coverage

2026 Jan–Nov attempted monthly searches are terminal through captured bounds; **2025 March remains open**, the other 2025 months are terminal. 2024 April/July are open; March/May/June/August–December attempted windows are terminal; Jan/Feb pending. Earlier years are thin or unsampled. His self-description about moving platforms does not prove X silence before 2025. This package has no complete cross-platform history.
'''
h='silverfang88'
A[h]=head(h)+f'''## Core model and what day2 changes

**Interpretation:** narrative rotation conditioned on cost/information advantage, with attention and liquidity as transmission mechanisms. Day2 adds 3,623 posts, chiefly May–July 2025 and mid-2024. It strengthens the boundary between a new narrative and a trade worth taking; it does not turn narrative commentary into a fixed tested system.

## Chronological rules and qualifications

- **6 Aug 2023:** {q(h,'1688007925552590848','信息优势=判断力优势，判断力=仓位+盈利')} The same rule list advocates strength/breakouts and profit/loss taking, with the dated recipe {q(h,'1688007925552590848','涨1倍出本，3倍出25%，5倍出25%')} No denominator beyond that text is supplied; do not invent a universal account-risk cap or resolve remaining ambiguity as audited position sizing.
- **29 Dec 2023:** {q(h,'1740688880007831938','没成本优势的不参与')} and {q(h,'1740688880007831938','永远只玩下一个新的故事')} The useful distinction is *advantage before participation*, not compulsive rotation.
- **21 Sep 2024 — short selection:** {q(h,'1837472909570322535','避开创新叙事')} He proposes looking at expensive VC projects and declining volume, while using unusually large collateral buffers. His “99%” short-success assertion and assumption that MM/venues see all cards are not verified probabilities or universal market facts. This is a dated proposed screen, not a loss-proof short book.
- **7 Jun 2025 — broad diagnosis:** {q(h,'1931182239712420141','盯上美股和各国其他资产了')} is his explanation for large participants leaving on-chain games. It is not independently measured capital-flow evidence. The sweeping end-of-cycle rhetoric should be read beside continued opportunity posts, not as a proven industry obituary.
- **19 Jun 2025 — familiar knowledge in a new venue:** {q(h,'1935565562832375826','原生加密资产去美股上市')} and {q(h,'1935565562832375826','明显存在币圈对外界的认知套利')} about Circle. He admits {q(h,'1935565562832375826','所以容易卖飞（比方说我）')} A thesis about an information advantage is not a claim of riskless, mechanically hedged arbitrage.
- **10 Jul 2025 — attention is insufficient:** {q(h,'1943173189305274473','注意力带来的流动性是这场短期游戏的伟力')} Yet he lists claim/credit timing, exchange arrival and short-squeeze risks around Pump, and concludes {q(h,'1943173189305274473','它改变不了人生，以大搏小')} This is valuable negative selection: recognize the story without betting on it.
- **8 Jul 2025, operating/social rule:** {q(h,'1942455834233237849','基本不信说的话，只看做了什么')} Relevant to evaluating the feed itself: posted rules and claimed fills are not audited behavior.

## How to operationalize the research, not copy a trade

1. Describe the **story** and its actual attention/liquidity channel separately from the ticker.
2. Write the **advantage**: earlier access, cost, superior domain knowledge, a specific observable catalyst. “It is new” is not enough.
3. List **plumbing**: allocation/claim sequence, withdrawal and exchange-credit timing, hedge availability, borrow cost and squeeze risk. Use the July Pump post as a checklist of reasons to abstain, not a trade recommendation.
4. Predefine **invalidation and worst loss** yourself. The quoted 2023 scale-out numbers do not supply a stop-loss size or leverage limit.
5. Journal thesis quality separately from timing. June's Circle “卖飞” is evidence that a correct-looking story need not become a captured return.

## Contradictions / failure modes

- Buy strength and “next story” can conflict with September 2024 short selection; those are different setups. Do not blend them without a regime rule that the posts have not supplied.
- Sweeping statements that crypto is over coexist with specific crypto/stock opportunities. Read them as changing opportunity-set commentary, not a mechanically consistent asset allocation policy.
- Cognitive “套利” here is not identical to @taresky's paired/operational arb. Both can have information value without hedged price risk.
- Calls, community promotion and exchange links create incentives; attention may also benefit the poster. No private identity is inferred and no wrongdoing is presumed.
- Formula-like maxims, bold numerical win claims and screenshots do not constitute a backtest, full account curve or independently verified edge.

## Coverage

2025 May/June/July priorities are now terminal. Five 2024 monthly cursors remain open: March, June, July, August, September. May is terminal; pending later-2024/early-2025 months remain exactly listed in the manifest. Stalled 2023-09 and 2026-07 parents are never to be reused; completed child windows must not be rewalked. No redundant 2026-November parent search.
'''
h='iiiinvest'
A[h]=head(h)+f'''## Core model, corrected by the deeper 2026 sample

**Interpretation:** a public plan-first discretionary trader, with tactical reversals, averaging and community monetization. Day2 adds 856 posts, mostly the previously open July–September 2026 tails. The evidence is more differentiated than “always 不格局”: he also urges holding through drawdowns, and publishes capital-tier-dependent risk-taking.

## Dated evidence and execution follow-through

- **25 Mar 2026:** {q(h,'2036625322649768054','不格局就不被割')} In context: tactical, disposable trades or cash, not a timeless rule to sell every small gain.
- **15 Jul 2026:** a proposed ADR short in {cite(h,'2077296816547319907')} gives a 187–197 entry range and 197 stop reference. These are **his stated instrument/market assumptions**, not facts independently checked by this archive or prices to trade today.
- **7–9 Aug 2026:** {q(h,'2085629869845790929','拿住！等我信号！')} then {q(h,'2086415326388842962','方向对了，仓位够了，拿住')} explicitly accepts profit drawdown to seek a larger move. This qualifies a one-slogan anti-conviction portrait.
- **10 Aug 2026:** {q(h,'2086712897007452607','交易量代表的是分歧程度')} He frames price action through long-term, speculative, short and unlocking sellers. Those classifications/flow estimates are interpretations, not observed beneficial-owner books.
- **3 Sep → 4 Sep 2026, plan then reported failure:** {q(h,'2095515428634464402','突破150，那么全部止损，说明逻辑错了。')} The next morning: {q(h,'2095721109156995262','昨晚睡前挂了150止损单，醒来已经被干了。')} He calls the seventh short round a loss. This is stronger evidence of **publicly stated invalidation followed by a matching self-reported stop** than an isolated slogan, but not brokerage verification. It does not prove portfolio-wide stop discipline.
- **4 Sep 2026, automated grid overlay:** {q(h,'2095800518098538606','底仓享趋势收益，网格撸震荡收益')} The post's “收益会高出200%” and one-week dollar decomposition are unverified; the benchmark, notional, collateral, fees, funding and full market path are not reconciled. A claimed 37-BTC position and equity cannot be treated as an unlevered portfolio without those details.
- **5 Sep 2026, capital tiers:** {q(h,'2096170727707648118','每次交易梭哈是最佳方式，杠杆要大一些。')} He says that for a 1万元 salaried participant, while later tiers reduce leverage/concentration. This is **his risky advice, not ours**, and makes a blanket “conservative anti-overconfidence trader” label misleading.
- **24 Nov 2026:** {q(h,'2125158673203048455','按照计划越跌越买')} and advice to check key times rather than stare at the screen. A precommitment process is distinct from the financial risk of averaging a leveraged-product long.

## Practical framework to study

**Explicit:** write a plan; interpret relative strength/volume; scale in or out conditionally; invalidate an idea at a stated threshold in some examples; hold when the plan calls for it. **Not supplied universally:** account loss limit, aggregated leverage cap, treatment of gaps and liquidation, or a fixed rule choosing “hold” versus “不格局”.

**Our how-to:** select a public plan with a timestamp before its trigger; record the original threshold without hindsight changes; find the next related update; classify “triggered/reported execution/no follow-up.” Track losing and winning cases equally. For a grid overlay, require equity, notional, benchmark return, funding, fees and drawdown over the same horizon. This corpus offers case studies, not a statistically complete strategy sample.

## Contradictions and incentives

- **Take profits / do not marry a view vs “拿住”:** possibly regime-dependent, but no complete regime-switch policy is established. Do not flatten them into one timeless rule or declare inconsistency where the horizon differs.
- **Stop discipline vs aggressive capital-tier advice:** a correct stop example does not neutralize ruin risk from leveraged all-in sizing.
- **Independent process vs “等我信号”:** followers may not share the author's trigger, latency or exit.
- **“免费” community vs refundable ticket/referral:** {cite(h,'2110022220131226106')} describes the gate and fund claims. Intent and financial transparency are not independently audited; career-return and fund guarantees are self-report.

## Coverage

2026 July/September and the saved Aug01–27 child window are now terminal; the stalled August parent stays blocked. 2024 March/April tails were terminal in batch79. Earlier years remain very uneven: 2022=408, 2023=37, 2024=21, 2025=69, 2026=4,177 stored posts. Empty attempted months do not establish year-long inactivity; unopened pending months still matter.
'''
h='alexandr_wang'
A[h]=head(h)+f'''## Scope: operator, not trader

This remains a business/AI-operator account. No trading method, verified market edge or risk-adjusted return can be derived from his public role. Day2 adds **48** posts, primarily finishing 2016–2017 tails; 2018 Jan–Oct and 2019 August priority tails were exhausted without new unique additions. Recent profiles were **not re-fetched**.

## Chronological core ideas

- **2016:** early community/hiring texture, including the correctly attributed Slack milestone {cite(h,'809663723006611456')}. The old guessed id `809675263590961152` is not a source and must not be reused.
- **4 May 2017, newly captured:** {q(h,'860019733625577472',"always great to see @scaleAPI's audio transcription API used to improve products.")} This is concrete product-use language, not a later reconstructed grand AI thesis.
- **23 May 2017:** {q(h,'866741890980368385',"We announced @scaleAPI's Series A in the @WSJ today!")} The linked reporting itself was not reopened; this establishes a captured announcement, not independently checked financing terms.
- **30 Jun 2017:** {q(h,'880514207153741824','Would love to chat more about your requirements and how we can help!')} The reply supports a customer-requirements/operator emphasis. It is not a communication sent by this research.
- **3 Oct 2017:** {q(h,'915051465659400192','we actually provide a simple API through which you can get images segmented by humans.')} This adds a specific product description to the earlier hiring/data narrative. Our interpretation is bottleneck-solving and customer adoption; it is not a claim that a 2017 tweet predicted later AI outcomes.
- **3 Dec 2020:** {q(h,'1334171701844746240','It is SO much more important to be authentic than it is to please everyone.')} This is a reply, not a stand-alone trading essay.
- **22 Sep 2023:** {q(h,'1705002729897447736',"trust your gut. act quickly. don't let problems stew.")} Operational responsiveness, not a market-timing signal.
- **3 Apr 2025:** {q(h,'1907604573730288060','precision-targeted fixes to identified failure modes')} supports evaluation/diagnosis as a public process argument.

## Significant Meta claims — attribution boundary

No Meta page, press article or profile was fetched on day2. The only inherited official-page wording used here is the literal capture note already in `../public_sources_wang.md`, attributed there to [Meta's leadership page](https://www.meta.com/about/leadership/alexandr-wang/), fetched 24 Nov 2026:

> Alexandr Wang joined Meta in June 2025 as the company’s first-ever Chief AI Officer, where he leads Meta Superintelligence Labs (MSL).

This is **stored source-note wording**, not a new day2 verification or an independently established day-of-month start. The July X announcement {cite(h,'1939867404252979291')} states his title; it does not establish “first-ever” or “June.” The Scale announcement cited in the same note says “is joining Meta to work on Meta’s AI efforts” and does not supply that title. Do not combine these into a stronger new fact. Cloud audit remains outstanding; retained source notes must be checked against their original capture when available.

The 23 Nov 2026 X post {cite(h,'2124719968499777546')} says the path is not inevitable and claims a Muse delay, SI Accords participation and an attributed compute priority. These remain **his captured statements**. This package has not checked a primary signatory list, independent safety implementation, or allocation report. Earlier news summaries repeating the post are not independent evidence. No additional significant Meta fact is asserted here.

## How-to takeaways, labeled as interpretation

For an operator: identify a concrete customer bottleneck; make adoption easy; collect requirements; diagnose specific failure modes; evaluate whether an intervention fixed them. The 2017 API replies and 2025 evaluation statement support those categories.

For a trader, the only transferable idea is **an analogy we propose**: predefine failure modes and measure them instead of relying on a prestigious speaker's confidence. This is not Wang's trading rule. It supplies no entry, exit, stop or sizing policy.

## Tensions and coverage

“Act quickly” and later safety/delay language need not contradict: different decisions have different costs of reversal. Authenticity is not evidence that a quantitative public claim is true. Product, policy and recruitment posts are interested first-party speech, not neutral evaluations of a competitor or industry.

2016 December and all 2017 monthly jobs are now terminal. 2012–2014 remains not-proven-exhausted with a lost historical empty-page input token; do not reopen that parent blindly. 2024–2026 monthly jobs remain mostly pending and overlap a recent exhausted timeline, so assess overlap before spending reads. Seventeen inherited no-job calendar months before account creation are excluded from actionable work, not counted as missing posts. See the machine-readable manifest for every exact bound.
'''
for h,text in A.items():(R/h/'analysis.md').write_text(text)
(R/'logs/day2_citation_ledger.json').write_text(json.dumps({'purpose':'Literal excerpts and attributed post citations used in current day2 analyses; presence is not factual verification of underlying claims.','citations':ledger},ensure_ascii=True,indent=2)+'\n')
print('Wrote five analyses; verified citations',len(ledger))
