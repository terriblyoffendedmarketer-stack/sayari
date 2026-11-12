# P05 · Stage 1: understand the news (Binance hack)

Story sent by Sayari via Ekshika, 2026-11-12: BBC, 30 Oct 2026, https://www.bbc.com/news/articles/cwg7xp8kx4v5o
Checked against Binance's statements, the FBI attribution, the Binance post-mortem coverage (3 Nov) and the tracing firms (Elliptic, TRM, Chainalysis), up to ~10 Nov. No Sayari angle in this file (that's stage 2).

## In one paragraph
On 29 October 2026, attackers drained about **$6.3bn** in crypto from **Binance**, the world's biggest crypto exchange (300M+ users). It's the largest crypto theft on record, about 4× the previous record (Bybit, $1.5bn, Feb 2025). They didn't crack Binance's vault. They got in through **people**: a fake job interview infected an engineer's computer, then they moved through the company until they could make the system approve withdrawals. The **FBI says North Korea did it** (a unit called TraderTraitor, part of what's known as Lazarus). North Korea denies it. About **half the money was frozen** within days. The rest is being **laundered** in small, deliberate steps. Binance says customers won't lose anything; it's covering the losses from its own reserves.

## How they got in (Binance's post-mortem, 3 Nov, as reported)
1. **A fake recruiter.** Someone posing as a project director contacted a Binance software engineer on a real job site. After interviews came a "coding assignment" that installed malware.
2. **Months of patience.** Binance calls it "a months-long campaign". Reports differ on when it started (June vs September).
3. **Moving sideways.** Around 20 Oct, using that foothold plus an internal AI tool, the attackers reached the computers of two wallet engineers (the people with authority over moving funds).
4. **The withdrawal.** On 29 Oct they got into a "service container" (a piece of Binance's internal system) that could reach the wallet-signing service, and submitted withdrawals the system treated as legitimate.
- Binance stresses it was not "one engineer, one click", and it has found no evidence the wallets' private keys leaked. Check Point's summary: attackers "no longer need the vault keys"; they go after the systems and people allowed to use them.

## Who did it
- **FBI (≈31 Oct–1 Nov):** attributes it to North Korea's TraderTraitor. It published wallet addresses and asked crypto businesses to block them.
- **Tracing firms agree:** Chainalysis ("high confidence"), TRM Labs and Elliptic link it to North Korea. TRM says it resembles Bybit.
- **North Korea** has denied involvement in past hacks. **Binance** hasn't named anyone itself.
- **Why it matters beyond crypto:** Western security agencies have said stolen crypto funds North Korea's nuclear and missile programmes.

## The money
| | Amount | Who says |
|---|---|---|
| Taken | ~$6.3bn (reports range $6.3–6.4bn) | Binance; TRM says $6.36bn |
| Frozen | ~$2.6–3bn (about half) | Binance; on-chain estimates (10 Nov) |
| …of which frozen by stablecoin companies | Tether + Circle ≈ $2.4bn (BBC) | Tether, Circle |
| Still with the attackers | ~$2.85bn (estimate) | Onchain Lens, 10 Nov |
| Already moved or laundered | ~$891M (estimate) | Onchain Lens, 10 Nov |
| Actually cashed out | "negligible" so far | Elliptic |
| Customers' losses | none; Binance covering from its SAFU reserve fund (~$1bn) + company funds; ~90% re-backed by 31 Oct | Binance |
Withdrawals were paused, then resumed on ~1 Nov.

## How they're moving it (laundering so far)
- **Converting to ether (ETH)**, mostly (FBI). The FBI expects DeFi platforms and instant swap services next.
- **Scattering:** 20,000+ wallets, 65,000+ transactions, many blockchains (Elliptic, Chainalysis).
- **Fake memecoins** (Elliptic, 9 Nov): they created six joke coins on the NEAR blockchain, bought them with stolen funds from one set of wallets and sold them from another, so the money never visibly goes from A to B. Tiny so far (~$430K). TRM found the same trick on Tron.
- **A small amount** reached China-based laundering groups (Chainalysis: several hundred thousand dollars).

## What's confirmed vs alleged vs unknown
- **Confirmed (by Binance):** the theft, the amount range, the entry via a compromised employee, the freezes, customers covered.
- **Attributed, not proven in court:** North Korea (FBI + tracing firms). Post copy needs "the FBI says / attributed to".
- **Estimates that keep changing:** frozen, remaining and laundered totals. Refresh them on the posting day.
- **Unknown:** how and where the remaining ~$2.85bn gets turned into usable money. That part hasn't happened yet.

## Words used above
- **Exchange:** a company where people buy, sell and hold crypto (Binance is the biggest).
- **Stablecoin (Tether's USDT, Circle's USDC):** a crypto coin pegged to the dollar and run by a company, which can freeze coins. That's why part of the loot could be frozen and the rest (e.g. ether) couldn't.
- **Laundering:** moving stolen money until its origin can't be traced, then turning it into money that can be spent.
- **DeFi / instant swap services:** crypto services that trade coins automatically, often with little or no identity check.

## Sources
BBC (30 Oct) · Richard Teng on X (30 Oct) · BleepingComputer / The Record on the FBI attribution (31 Oct–1 Nov) · CNN, CNBC on withdrawals resuming and coverage (31 Oct–1 Nov) · BleepingComputer, Infosecurity Magazine, TechTarget on the post-mortem (3 Nov) · CoinDesk / VOA on Elliptic's memecoin findings (9 Nov) · FinanceFeeds on Onchain Lens estimates (10 Nov).
