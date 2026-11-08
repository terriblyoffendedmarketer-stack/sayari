# Source Discovery: Candidate Review & Approval List

> [!IMPORTANT]
> Per project rules, no source is collected until you review and approve it.
> Automated scrapers for LinkedIn, G2, Glassdoor, and Blind are strictly disabled.

## 1. Candidate Subreddits
| Subreddit | Why It Matters | Status |
| :--- | :--- | :--- |
| **r/AMLCompliance** | Primary hub for AML/KYC investigators, L1 alert fatigue, SAR filing rants | [x] Approved in config.yaml |
| **r/financialcrime** | Trade-based money laundering, sanctions evasion, shell company investigations | [x] Approved in config.yaml |
| **r/compliance** | Corporate compliance officers, regulator exams, audit panic, policy battles | [x] Approved in config.yaml |
| **r/RegulatoryCompliance** | Banking and fintech regulatory examinations, EDD backlogs | [x] Approved in config.yaml |
| **r/OSINT** | Corporate registry digging, ownership mapping, open-source intelligence tactics | [ ] Recommended for approval |
| **r/supplychain** | UFLPA compliance, transshipment routing, supplier questionnaire frustrations | [ ] Recommended for approval |
| **r/customs** | Customs broker holds, BIS export controls, dual-use shipping documents | [ ] Recommended for approval |

## 2. Industry Publications & Expert Commentary (RSS / Public Pages)
| Source | Editorial Focus | Status |
| :--- | :--- | :--- |
| **FiveBy Risk News & Insights (Substack)** | Sanctions evasion networks, transshipment hubs, investigative teardowns | [x] Configured in config.yaml |
| **Steptoe International Compliance Blog** | OFAC enforcement, export control rule updates, BIS advisory notices | [x] Configured in config.yaml |
| **Holland & Hart TradeSanctions.com** | Practical commentary on trade sanctions, SDN designations, 50% rule traps | [x] Configured in config.yaml |
| **FCPA Blog** | Anti-bribery enforcement, third-party risk management (TPRM), corporate corruption cases | [x] Configured in config.yaml |
| **Export Control Navigator** | Semiconductor export curbs, dual-use technology diversion, Russian sanction evasion | [x] Configured in config.yaml |
| **ACAMS moneylaundering.com** | Global financial crime news, regulatory exams, FinCEN advisories | [x] Configured in config.yaml |
| **AML Intelligence** | European AML authority developments, banking penalties, sanctions enforcement | [x] Configured in config.yaml |

## 3. Companies Whose Career Pages Reveal Real Stack Frustrations
| Company Archetype | What Job Postings Reveal | Manual / Feed |
| :--- | :--- | :--- |
| **JPMorgan Chase / Citi / HSBC (Global Banks)** | Job descriptions detail exact pain points: alert clearing volume, name screening false positives, legacy watchlists | Inspect public job board RSS/alerts |
| **Stripe / Revolut / Wise (Fintechs)** | Fast-scaling KYB backlog, merchant entity resolution, automated onboarding friction | Inspect public job board RSS/alerts |
| **PwC / EY / Deloitte / Guidehouse (AML Advisory)** | Remediation projects for banks under consent decrees; reveals what broken compliance looks like | Inspect public job board RSS/alerts |
| **Boeing / Caterpillar / Apple / Flex (Global Manufacturing)** | Supply chain Tier 1 vs Tier 2 visibility, UFLPA detention notices, forced labor audits | Inspect public job board RSS/alerts |
| **Archer Daniels Midland / Bunge / Cargill (Ag & Commodities)** | Complex maritime transshipment, ownership obscurity, multi-jurisdiction trade routes | Inspect public job board RSS/alerts |

## 4. Manual Import Only (Do NOT Scrape)
| Platform | Recommended Use |
| :--- | :--- |
| **LinkedIn Comments & Posts** | Collect by hand only (never scrape). Paste rants and commentary into data/imports/ |
| **G2 / Capterra Reviews** | Customer reviews of screening tools (Moody's, LexisNexis, Dow Jones) highlighting UI lag and false positives |
| **Glassdoor / Blind** | Employee reviews of L1 compliance operations ('sweatshop alert mills', backlog quotas) |

---
*To approve additional subreddits or RSS feeds, add them to `config.yaml`.*
