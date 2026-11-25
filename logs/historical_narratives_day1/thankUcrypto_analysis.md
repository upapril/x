# Analysis — @thankUcrypto (allincrypto 熬鹰资本)

**Corpus (day-1 initial sample only):** 178 unique stored posts, 2022-12-30 17:55:07 GMT+8 → 2026-11-24 19:05:18 GMT+8 (Asia/Shanghai). Types: original 82, reply 74, quote 21, repost 1. Profile `post_count` at 24 Nov 2026 20:31 GMT+8 lookup: **8,097**. Followers: 229,472.

**Coverage (read this first).** This is **not** a complete history. Day-1 collection was a budget-limited public sample: the profile, one recent `get_users_posts` page, first pages of nine dated windows (2026-11, 2026-10, 2026-06, 2025-12, 2025-06, 2024-12, 2023-12, 2022-12, 2018-12), and the pinned post (expansion 404, later retrieved with `get_posts_by_ids`). 2018-12 came back empty (that month only). 2022-12 returned two posts but still has a `next_token`. Account created 2016-03-04; most pre-2025 months were not opened. A 28 Jun 2025 reply says he shared on Weibo “22-24” and “25年才转的推” ([1938878237918273854](https://x.com/thankUcrypto/status/1938878237918273854)) — that is self-description, not proof the earlier X timeline is empty. See `coverage_manifest.md` and `logs/remaining_jobs_day1.json`.

Public identity is taken only from the public profile and posts: display name “allincrypto 熬鹰资本 🇨🇳”; bio “多次创业成功并归零，今年1万美金再次重返1000万美金”; location text “你就是你自己的交易之神。”; website expanded to https://vlink.cc/aoyingzhuli; bio also contains a Binance t.co link and an assistant mention `@xiaoweio9983`; verified_type blue. **No legal name is inferred.** Bio P&L is self-reported and unverified.

Times below are Asia/Shanghai (GMT+8) unless labeled UTC.

---

## Core operating model (from the posts we have)

In this sample he presents as a high-activity directional trader (crypto, later also US-related stocks and a brief A-share experiment) who talks in fills, funding-rate games, copy-trading / “带单,” and large self-reported P&L swings. The current pinned post (24 Aug 2026) says it is “最后一次更新实盘挑战系列数据,” then gives unverified figures: two weeks “搞了2.3M,” the 带单号 “赚了1.6M,” “合计交易总盈利5M,” “跟单分润10%赚0.6M,” and “从五月做1WU直播挑战到今天总收益5.6M。换汇率就是3600万R左右。” ([2091778918810612183](https://x.com/thankUcrypto/status/2091778918810612183)). **None of those numbers is audited here.**

The most compact **process** statement in the newest page is 24 Nov 2026:

> 交易和短线不短线不重要。
> 你为什么开，什么条件开，为什么平，什么条件平，很重要。

Source: [2125155429512855651](https://x.com/thankUcrypto/status/2125155429512855651) (2026-11-24 17:11:52 GMT+8). The same post describes a Nvidia long he wanted midday and sized into at night, with a 150 take-profit conditioned on “黄仁勋12.1号听证会没大利空.”

A June 2025 post states a different crisp rule: “做交易，永远要靠自己,” criticizing people who wait for him to say when he flattened ([1938297622181384628](https://x.com/thankUcrypto/status/1938297622181384628)).

**Interpretation (not a proven edge):** the public book in this sample is discretionary, narrative- and microstructure-aware (funding-rate timing on Sahara in Jun 2025; event-driven Nvidia in Nov 2026), often leveraged, and frequently revised in public after the fact. It is not a documented mechanical system.

---

## How-to / rules that actually appear

- **Define open and close conditions** (Nov 2026), quoted above. That is a process rule; the same 24-hour window also shows missed adds and a filled take-profit he then regretted.
- **Do not outsource the exit to the caller** (Jun 2025): “做交易，永远要靠自己.”
- **Tighten wide stops after a scare** (26 Jun 2025): “最高亏了特么60wu…差2%止损。以后宽损还是放窄点儿好。” ([1938259138863370368](https://x.com/thankUcrypto/status/1938259138863370368)). Self-reported; unverified.
- **Control leverage when chasing a breakdown** (29 Dec 2023): “这里下跌确定性变大了，追了一些空，请控制自己杠杆。做跌破思路。” ([1740786429972852753](https://x.com/thankUcrypto/status/1740786429972852753)).
- **Withdrawals / cash** (23 Nov 2026): “提现永远是对的…在市场里留4000万还是留1000万都是一样的，杠杆是活的，善用杠杆就行了。继续提现。” ([2124746863656231190](https://x.com/thankUcrypto/status/2124746863656231190)). This is a cash-management slogan plus a living-leverage slogan — not a size formula, and not independently checked.
- **A-share post-mortem** (24 Nov 2026): “我炒 a 股真是一窍不通，只能选哥美股强关联的产业。但是一路，300-700-1000-1400-2000，一路相当于马丁一直加仓。才加到这时候解套跑的。不准备买大 A 个股了，等着便宜了买股指。” ([2125183975757119963](https://x.com/thankUcrypto/status/2125183975757119963)).

Dec 2023 posts also show short-horizon altcoin / BSV / Sol calls, scale-out language (“我会在109开始减仓”), and a “双损” / margin-moved-out note. Treat those as dated trade journal entries, not a standing playbook.

---

## Contradictions and limits

- **Huge self-reported wins and huge self-reported losses sit in the same year.** Compare the Aug 2026 pin (5.6M challenge total, unverified) with 26 Jun 2025 “最高亏了特么60wu” and 15 Jun 2026 “几个小时10wu无了” after a 5x copy-trade short and an ETH short that “全损” ([2066501986653221245](https://x.com/thankUcrypto/status/2066501986653221245)). These can all be true in a volatile book, or some can be wrong; this research cannot settle it.
- **Process rule vs same-week behavior.** “为什么开，什么条件开，为什么平” is posted the same day as a martingale-like A-share add (300–2000) he later forswears, and a day after a take-profit fill he did not want. That is a real contradiction between stated process and described sizing — not proof the process rule is fake, and not proof the martingale was a one-off.
- **“提现永远是对的” / “杠杆是活的”** can be read against the wide-stop scare and the martingale add. The corpus does not resolve which slogan governs when.
- Bio “1万美金再次重返1000万美金,” challenge totals, and copy-trading share are **unverified**. Monetization (带单, assistant, exchange / vlink links) sits next to the advice.
- Pre-2025 X coverage is a sliver. Do not describe a 2016–2024 “style history” from this sample.

---

## Practical test (not advice)

A practical reading of the *stated* Nov 2026 rule would be: write the open condition and the invalidation / take-profit *before* the fill, and do not scale like a martingale unless that scale plan was also written down. A practical reading of the Jun 2025 stop comment would be: if a 2% buffer almost tags after a 600k-U mark-to-market, the stop was not actually sized to the book. This research has no fill tape and does not claim those tests would have made money.
