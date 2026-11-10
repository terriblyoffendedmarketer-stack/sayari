# Real-content & UGC library (the visual break from navy/beige)

Built 2026-11-11 for the variety agenda (items 1, 2, 4). Goal: posts that show **real things** (product UI, regulator releases, practitioner posts, customer quotes), not only our infographics. Pair with `research/sayari-site/FEATURE_MAP.md` (F# ids below).

Images live in `content/library/assets/` (gitignored: client and third-party material stays out of the public repo). Re-fetch commands are noted per item.

## 1. Real Sayari product UI
| File | What it shows | Fits |
|---|---|---|
| `assets/sayari-ui/learn-export-controls-1.png` (1212×578) | Graph search results: "jinzhou xinyu material", 32 entities, Chinese + English name, 3 registry IDs, a forced-labor warning icon | F6, F11 (native-language record), P01 sequel (F10) |
| `assets/sayari-ui/learn-export-controls-2.png` (1257×595) | Entity profile translated to English (yellow highlights), **"Possibly Same As (2)"** in the sidebar, "Generate AI Summary" button | **P01 sequel** ("same company?" → "Possibly Same As"), F11 translate |
| `assets/sayari-ui/learn-export-controls-3.png` (1212×577) | Network graph: company → shareholders/officers; "Forced labor 1: Owner of Xinjiang-Based Entity" popover | F6 (risk two hops away), F3 |

- Source: Sayari Learn tutorial "Sayari Graph for Export Controls" (Nov 2024 UI). Fetch: open the page, take `img.currentSrc`, `curl -L` (it 302-redirects to img.notionusercontent.com).
- ⚠ Screenshot 2 has a Sayari employee's profile photo top right: crop or cover it before use.
- More available, not downloaded: "Sayari Graph for Forced Labor" (4 screenshots, same Jinzhou walkthrough). "Alternative Suppliers" tutorial images are broken (Google-hosted). Graph/Map quick-starts not scanned (Notion was timing out).
- **Ask Ekshika** for current product screenshots (Signal, Pilot, Guide, Supply Chain Mapping); the public ones are 2 years old.

## 2. UGC: customer quotes and named results (from `research/sayari-site/case-studies/`)
**Named (strongest, can show name + title):**
- "If we were unable to find an entity in other solutions, 95% of the time we could find it in Sayari." (Ben Seager, Integrity and Compliance Manager, Honeywell) · 75% of analyst time was manual verification · F4, F10
- "Sayari helps our specialists uncover previously unknown corporate structures and international connections…" (Anna Makarenko, Head of Department, ARMA Ukraine) · 4 suspects linked abroad, assets confirmed in 2 countries · F3

**Anonymized titles (quote + role only):**
- "…ready with evidence, not excuses." (Compliance Lead, Top 10 electronics manufacturer) · tier 1→5 in 6 months · F6
- "Every tier, from raw material to retail shelf, is mapped and monitored." (Head of Forced Labor Compliance, Top 5 grocery retailer) · <50% questionnaire response · F6
- "Entity resolution is more important than algorithm tuning for sanctions screening accuracy." (CCO, global logistics provider) · F10
- "When the next wave of designations hits, the team has the resolution infrastructure to absorb the volume without breaking." (Head of Sanctions, Top 3 US bank) · 90–95% time on false positives · F10
- "We can now independently verify vendor ownership claims… rather than relying on vendor self-reporting." (Head of TPRM, #3 US telecom) · 800 vendors in 90 days · F13
- "Investigators who once waited in a queue… now access data directly, in real time, on live cases." (Deputy Director, UK law enforcement agency) · £10M found in month one · F12
- "We now build data centers with supply chain visibility that exceeds the capability of most government agencies." (VP Supply Chain Provenance, Top 3 tech) · F6
- "Workflows match our processes, not the other way around." (Head of Compliance, largest marine insurer) · platform went down in peak renewal season
- **Near-miss story (no quote, best plot):** US energy infrastructure company: test run found a sanctioned vendor on the ACTIVE list that the legacy tool missed; "nearly approved". F1

## 3. Practitioner posts (listener DB) → rebuild as anonymized social cards
Rules: no usernames or avatars, paraphrase, ≤25-word excerpts, widely shared phrasing only. Rebuild in the post (L5 message-thread layout or a Reddit-style card); don't screenshot the real thread.
- r/AMLCompliance (58↑, 28 comments): third analyst gone in 4 months, all to fintechs paying 20–30% more with half the alert volume. → burnout/alert volume, F10/F14
- r/business (16 comments): "Can you get fined if you don't screen for sanctions?" Top reply: yes, per transaction. → F1 hook (⚠ verify the current OFAC per-violation maximum before quoting a number)
- r/business comment: "Are you actually manually looking up each entity on the OFAC website?" → Fortune 100 manufacturer's spreadsheet screening
- r/fintech (14 comments): sanctions screening at scale without constant false positives; common names. → P01 sequel, F10
- r/fintech comment: treat a possible match as something to look into, not an automatic reject. → F10 match quality
- r/FinancialCareers (172↑, 119 comments): "Why does compliance have such a bad rep?" → culture / Friday relatable
Query: `sqlite3 data/sayari.db "select … from raw_items where passed_filters=1 order by intensity desc, upvotes+comment_count desc"`

## 4. Regulator and news releases (screenshot when a post needs one; verify URLs then)
- OFAC enforcement releases (e.g. Medallion, 21 Dec 2023, used in P04): ofac.treasury.gov → Civil Penalties and Enforcement Information. F1, F12
- OFAC 50 Percent Rule guidance (OFAC FAQs on entities owned by blocked persons). F1
- BIS Entity List / MEU List and the affiliates (50%) rule: check its current status first. F2
- CBP UFLPA statistics dashboard (detention values; the case studies cite $3.7B since June 2022, check for a newer figure). DHS UFLPA Entity List. F6
- Sayari's own blog posts as real headers: `transshipment-penalty`, `1260h-list-update`, `alert-adjudication-amla`, `kyb-automation-gap`, `moosavi-hezbollah-network` (sayari.com/resources/…)
- Sayari API change log JSON (`risk_notifications` added/removed): a real code snippet. F13

## 5. Faked-but-real-feeling artifacts (allowed)
Slack threads, emails, ticket queues, calendar invites: build with L5 (message thread) or a native-UI mock. Keep company and people names invented; no disclaimers on the image.

## Frame rule (agenda item 4)
See `design/kit/README.md` → "Real content inside the frame".
