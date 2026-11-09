# Other Sayari site content (not downloaded yet; pull when a bucket needs it)

Pulled 2026-11-10 from sayari.com's public content API through the browser. Full text is fetched on demand; the case studies are already in `case-studies/`.

## Investigation briefs (story material for "The receipts" carousels)
- Russia's Military-Industrial Complex: corporate structures & sanctions vulnerabilities (2026-11-05) — https://sayari.com/resources/investigation-briefs/russia-military-industrial-complex/
- Ghost Directors and Shell Companies: UK High Street Crime (2026-05-23) — https://sayari.com/resources/investigation-briefs/uk-high-street-crime/
- Cross-Border Fentanyl and Methamphetamine Network (2026-05-04) — https://sayari.com/resources/investigation-briefs/fentanyl-network/
- Combining Digital Footprint Data: Fentanyl Uncovered (2026-05-04) — https://sayari.com/resources/investigation-briefs/fivecast-fentanyl/
- The War on Fraud (2026-04-06) — https://sayari.com/resources/investigation-briefs/war-on-fraud/
- The Economic Security Mandate (2026-01-11) — https://sayari.com/resources/investigation-briefs/economic-security-mandate/
- Sabotage at Sea: Russian Shadow Fleet (2025-06-25, Brent Phillips) — https://sayari.com/resources/investigation-briefs/sabotage-at-sea-russian-shadow-fleet/
- Unmasking the Iranian Oil Smuggling Shadow Fleet (2025-05-07, Brent Phillips) — https://sayari.com/resources/investigation-briefs/unmasking-iranian-oil-smuggling/
- Corporativo y Enlace RAM: DTO Chemical Procurement Network (2025-04-06, Ben Power) — https://sayari.com/resources/investigation-briefs/enlace-ram/
- The Fentanyl Equipment Supply Chain Behind CapsulCN (2025-04-06, Ben Power) — https://sayari.com/resources/investigation-briefs/capsulcn/
- High-Risk Mexican Importers of Essential Chemicals (2025-04-06, Ben Power) — https://sayari.com/resources/investigation-briefs/essential-chemicals/
- Talent Recruitment (2024-05-07, Brent Phillips) — https://sayari.com/resources/investigation-briefs/talent-recruitment/
- Balkan Transnational Criminal Organizations (2024-04-10, Ben Power) — https://sayari.com/resources/investigation-briefs/balkan-tco/
- Left of Launch: Adversary UAS Supply Chains (2024-04-10, Ben Power) — https://sayari.com/resources/investigation-briefs/uas-supply-chain/
- Wang Yunhe Transnational Money Laundering (2024-04-09, Ben Power) — https://sayari.com/resources/investigation-briefs/wang-yunhe/
- Russian Banks Cash-for-Gold Sanctions Circumvention (2024-04-06) — https://sayari.com/resources/investigation-briefs/russian-banks/
- China's Use of Golden Shares (2024-04-06) — https://sayari.com/resources/investigation-briefs/golden-shares/
- Chinese State Ownership and Investment Vehicles (2024-04-06) — https://sayari.com/resources/investigation-briefs/chinese-state-ownership/
- Starlink Terminal Diversion to Sanctioned Jurisdictions (2024-04-06) — https://sayari.com/resources/investigation-briefs/starlink-diversion/

## Buyer guides (Sayari's own framing of buyer pain; hooks and stats live here)
- Enterprise Risk: "Enterprise risk programs share one structural flaw. They were built to manage silos, not risk itself." — https://sayari.com/resources/buyer-guides/enterprise-risk/
- Supply Chain Risk Intelligence: "Supply chain risk platforms look similar in a demo. They don't perform the same in production." — https://sayari.com/resources/buyer-guides/supply-chain/
- Financial Services KYB: "Your KYB program automates 30% of verifications. The other 70% is where fraud hides." — https://sayari.com/resources/buyer-guides/financial-services-kyb/

## How these were fetched (gotcha)
Plain curl/requests gets 403 (Cloudflare), and spoofing a browser User-Agent is blocked by Claude Code's safety rules, so don't.
What works: open https://sayari.com in a real browser tab (Claude in Chrome, or the built-in pane) and run
`fetch('/wp-json/wp/v2/case-study?per_page=100&_fields=slug,link,date,title,content')` in the page
(other types: `investigation-brief`, `buyer-guide`). Then write the text out from the session.
The pane can't POST to localhost or trigger downloads, so text has to come back through the session.
