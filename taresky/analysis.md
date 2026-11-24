# Analysis — @taresky (𝘁𝗮𝗿𝗲𝘀𝗸𝘆)

**Corpus (day-1 initial sample only):** 224 unique stored posts, 2016-12-15 08:47:22 GMT+8 → 2026-11-24 17:10:31 GMT+8 (Asia/Shanghai). Types: original 53, reply 138, quote 22, repost 11. Profile `post_count` at 24 Nov 2026 20:31 GMT+8 lookup: **34,003**. Followers: 55,145.

**Coverage (read this first).** This is **not** a complete history and is not close to one. Day-1 collection was a budget-limited public sample: the profile, one recent `get_users_posts` page, first pages of nine dated windows (2026-11, 2026-10, 2026-06, 2025-12, 2025-06, 2024-12, 2022-12, 2021-01, 2016-12), and the pinned post (expansion 404, later retrieved with `get_posts_by_ids`). Every dated window still has a `next_token`. Account created 2011-09-05; most months from 2011–2026 were not opened. Year counts of 25 are first-page / year-end sampling artifacts, not proof of low activity. See `coverage_manifest.md` and `../logs/remaining_jobs_day1.json`.

Public identity is taken only from the public profile and posts: display name 𝘁𝗮𝗿𝗲𝘀𝗸𝘆; bio text `套利 1~100x | 2021~2025.6`; website expanded to https://taresky.com; verified_type blue. **No legal name or private-life inference is made.** Bio wording is not a verified track record.

Times below are Asia/Shanghai (GMT+8) unless labeled UTC.

---

## Core operating model (from the posts we have)

The clearest **explicit** strategy statement in this sample is from a 28 Dec 2022 thread, not from the 2025–2026 pages:

> 自从我了解到 Crypto 这件事物起，我的风格、策略、预期就从未改变：只套利，不承担风险敞口。

Source: [1608095146834563072](https://x.com/taresky/status/1608095146834563072) (2022-12-28 21:38:54 GMT+8). In the same thread he says he prefers bear markets because others blow up, calls the game zero-sum, and (in the root post) self-reports 2021 APY “大致 200%” with max drawdown “不超过 10%,” and 2022 APY “也超过 50%” with max drawdown “不超过 5%,” plus “Fuck you money” and that most of the money was made in the half-year *not* spent at a job ([1608095141713305600](https://x.com/taresky/status/1608095141713305600)). **Those P&L figures are self-reported and unverified.**

A same-day year-end post breaks 2022 income (self-reported, “脱敏”) as 73% investment, 16% from a half-year of work “包括基本工资、作为基金经理的业绩收入,” and 4% outsourcing ([1609076695885307907](https://x.com/taresky/status/1609076695885307907)). The pinned post (2023-09-09) frames a career arc in hashtags — “数字游民和自由职业,” “从产品经理到基金经理” — and says that before taking a job he had been “有点天真，认为靠自己的劳动，创造价值挣钱才是社会的主流” ([1700606366606565686](https://x.com/taresky/status/1700606366606565686)).

**Interpretation (not something this sample can prove as a continuing rule):** in late 2022 he presented himself as a no-directional-exposure crypto arbitrage operator who also did a period of fund-manager / product-manager work. The current bio dates that arb window as `2021~2025.6`. The 2025-06, 2025-12, and 2026 pages in *this* sample are dominated by tooling, AI/app building, and product/affiliate notes; they do **not** repeat “只套利，不承担风险敞口.” Absence in a thin sample is not proof he stopped, and it is not proof the bio end-date marks a style change. That question is still open for later pages.

---

## How-to / rules that actually appear

- **Partnership rule (2026-06-29):** “我找人合作/合伙的标准是：愿意跟这个人平分所有收益。要不然就不要合作，走雇佣，供参考。” ([2071431063684178369](https://x.com/taresky/status/2071431063684178369)). This is a cooperation rule, not a market-entry rule.
- **Self-employment preference (2022-12-29):** “21 年已经完成副业到全职的转换了，给自己打工的时候效率永远是最高的。” ([1608300180427644928](https://x.com/taresky/status/1608300180427644928)).
- **Operational security (2025-12-26):** after a Trust Wallet incident, he says it is a wallet he uses for “临时 or 机器人私钥生成,” and “建议最近不要打开这个App，如果非要打开，一定不要联网…等完整事故报告出来之后再联网。” ([2004389388479091056](https://x.com/taresky/status/2004389388479091056)).
- **“破除迷信” (2022-12-28)** in the same arb thread: institutions can miss obvious basis (he cites CEX desks missing a CRV 10% 期现价差 “两轮”); domain jumpers are beginners ([1608095148910710784](https://x.com/taresky/status/1608095148910710784)). This is an argument about *who is actually competing*, not a sizing formula.

Insurance-as-leverage remarks in Jan 2021 ([1355813095877144578](https://x.com/taresky/status/1355813095877144578)) are about household cash and insurance, not trading leverage. Do not transplant them as a trading rule.

This sample does **not** contain an explicit entry/exit, position-size, or invalidation playbook comparable to the 2023 rule list stored for @silverfang88.

---

## Contradictions and limits

- Self-reported returns and “Fuck you money” are not audited. Treat them as claims in a dated post.
- “风格、策略、预期就从未改变：只套利” (Dec 2022) versus a bio that *ends* the stated arb period in mid-2025, versus 2025–2026 sampled posts that do not restate the arb rule: this is a **tension to check**, not a proven style change.
- 2011–2015, most of 2016–2021, and most months of 2022–2026 are not in the store. Any “he always/never” claim is unsupported.
- Monetization / invite / cashback posts appear in the 2026 sample; they sit beside the craft talk, as with the other trader accounts.

---

## Practical test (not advice)

If someone wanted to *test* the 2022 stated model rather than the author’s biography: it would be a market-neutral / basis / funding book with a tight drawdown cap, not a directional “story” book. This research has **no** fill data, no backtest, and no evidence that the self-reported APY or drawdowns are reproducible. The 2025–2026 sample is too thin to say whether that model is still what he does.
