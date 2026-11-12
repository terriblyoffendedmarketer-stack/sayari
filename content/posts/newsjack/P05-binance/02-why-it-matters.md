# P05 · Stage 2: why it matters (to our ICP, to Sayari)

Builds on `01-news.md`. Not the story yet (that's stage 3).
**ICP:** compliance officers and heads of financial crime, sanctions and KYB, plus investigations and intelligence analysts. At banks, payment and fintech firms, crypto businesses, corporates and government.

## Why it matters to them
1. **It's a sanctions problem now, not just a hack.** The FBI ties the money to North Korea, which is under heavy sanctions. It published wallet addresses and asked businesses to block them. Anyone whose business touches those funds has sanctions exposure: exchanges, payment firms, OTC desks, and banks that serve crypto companies.
2. **The part still ahead is the part that reaches them.** About $2.85bn hasn't been cashed out yet. To be spent, it has to leave crypto and become ordinary money. In past North Korean cases, that happened through OTC traders and front companies that paid for goods (US Treasury/DOJ, 2023). When it lands, it looks like a normal company payment in someone's KYB or payments queue.
3. **The way in looked like a legitimate business.** The attack started with a fake recruiter. North Korea has used real, registered US companies for exactly this before: BlockNovas LLC (New Mexico) and SoftGlide LLC (New York) ran fake job interviews to infect crypto developers. The FBI seized BlockNovas's website (Silent Push research, Apr 2025). Binance hasn't named the company used against it. The lesson for KYB and third-party-risk teams: a real registration doesn't mean a real business.
4. **The biggest theft ever means questions from above.** Boards and regulators ask "could this touch us?". North Korea sanctions enforcement keeps growing: Treasury designated more North Korean bankers and front-linked entities in Nov 2025 and says North Korea stole $3bn+ in crypto over three years.

## Why it matters to Sayari
- **Fit:** every point where stolen crypto meets the real economy is a **company**: the fake recruiting firm, the OTC desk, the front company that pays for goods, the trading company that sends the wire. That's Sayari's ground: who owns a company, who runs it, what it's connected to, across borders.
- **It complements blockchain analytics; it doesn't compete with them.** Chainalysis is listed as a **Sayari partner**. Blockchain firms follow the coins; Sayari covers the companies and people at the edges. Our tone has to respect that: no "they can't do this, we can".
- **Wider audience than crypto.** The cash-out hits ordinary banking and payments, so the story speaks to Sayari's core buyers (banks, payments KYB, corporates, government), not only crypto firms.
- **Timely and big.** The largest theft on record, still developing (laundering news every few days), so it can be refreshed.

## Limits and risks (keep us honest)
- Sayari doesn't trace wallets and doesn't stop hacks (that's cybersecurity). Never imply it would have prevented this one.
- **The link to Sayari isn't in the hack's own facts yet.** It comes from North Korea's documented pattern (fake companies, front companies, OTC cash-outs). The post has to label it as a pattern ("last time…", "this tactic has…"), not as what happened at Binance.
- North Korea = "the FBI says" (an attribution, not a court finding).
- Binance is a big brand (and could be anyone's customer or partner). Stay factual: no mockery or blame.

## Questions for Ekshika / Sayari
- OK to mention or lean on the Chainalysis partnership, or keep it unspoken?
- Does Sayari have any crypto or VASP-related data or a use case it wants highlighted, or do we stick to companies and ownership?

## Sources
Stage 1 sources, plus: US Treasury jy1435 (24 Apr 2023) + DOJ US v. Sim Hyon Sop · Silent Push via Reuters/CoinDesk/The Block (25 Apr 2025: BlockNovas, SoftGlide) · TRM Labs on the Treasury action of 4 Nov 2025 (DPRK bankers, Korea Mangyongdae Computer Technology Co.) · Sayari partner ecosystem page (lists Chainalysis).

---

## How Sayari's 4 posts made the news → Sayari connection (and ours)
Their method, every time:
1. **Find the company-level fact inside the news:** an entity, an owner, a controller, a registration. Ignore everything else, however big (GPUs, invoices, AI model weights).
2. **Name the claim that hid it:** paperwork, an invoice, "a minority stake", "no foreign owner".
3. **Turn it into the risk team's own question** ("Who owns the transshipment company?", "Diligence has to cover who controls the target", "what does your memo cite?").
4. **One Sayari line = data + verb + "side by side / in one place":** corporate (and trade) records, 250+ jurisdictions → maps / traces / surfaces → the claim and the reality "show up side by side", "in one place", "a head start", "there when needed". Modest, never "would have caught it".

| Post | Company-level fact in the news | The risk team's question | Sayari line's payoff |
|---|---|---|---|
| Earthmade | The **transshipment company** buying the servers | Who owns it? Where did its past shipments end up? | "compliant" first stop and real destination side by side |
| A7 | **Two UAE shells registered by the same person** (from the NYT story) | Catch it in the network, not the invoice | front company and the network behind it in one place |
| MOFCOM | The **"actual controller"** of a Chinese AI company | Who controls the target, not just who owns it | a head start on the control question |
| ICBC | **Minority stakes, JVs, obscured shareholders** | What does your exception memo cite? | the records are there when needed |

**For Binance, drop the crypto.** Coins, wallets, ether and memecoins are blockchain analytics' ground (and Chainalysis is a Sayari partner). The company-level fact *in this story*: the $6.3bn heist started with **a "Project Director" at a fictitious company**, with a fake HR rep, a fake CEO and social accounts built to look real (Binance post-mortem, 3–4 Nov).
- **The claim that hid it:** a convincing company front (people, profiles, a project).
- **The risk team's question:** onboarding companies is the KYB job. Does this company actually exist? If it's registered, who registered it, at what address, linked to whom? North Korea has registered real shells for this same tactic before (BlockNovas LLC, New Mexico; SoftGlide LLC, New York; Apr 2025), so a registration alone proves nothing.
- **Sayari line (draft, in their pattern):** "Sayari's corporate records across 250+ jurisdictions show who sits behind a company: its owners, officers, addresses and links. So a polished front and a company that doesn't exist on paper are easy to tell apart." (Supported by the Aug 2026 shell-company risk factors: mass address, mass registration, implausible date of birth, company service providers.)
- **The gap to bridge honestly:** at Binance, the fake company targeted a job candidate, not a compliance check. The post has to make the jump explicit: the same front, built to fool a candidate, is what risk teams meet as a new customer, vendor or counterparty.
