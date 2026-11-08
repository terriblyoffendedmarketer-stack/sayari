# src/discovery.py — Source Discovery Module
# Usage: from src.discovery import discover_candidates, export_discovery_list
# Requires: typing, json
#
# Gotchas:
# - No unapproved scraping. All discovered candidates are presented for human review before ingestion.
# - Do not scrape LinkedIn, G2, Glassdoor or Blind automatically — list them as manual targets only.

from typing import Dict, List, Any

DISCOVERY_CATALOG = {
    "subreddits": [
        {"name": "r/AMLCompliance", "relevance": "Primary hub for AML/KYC investigators, L1 alert fatigue, SAR filing rants"},
        {"name": "r/financialcrime", "relevance": "Trade-based money laundering, sanctions evasion, shell company investigations"},
        {"name": "r/compliance", "relevance": "Corporate compliance officers, regulator exams, audit panic, policy battles"},
        {"name": "r/RegulatoryCompliance", "relevance": "Banking and fintech regulatory examinations, EDD backlogs"},
        {"name": "r/OSINT", "relevance": "Corporate registry digging, ownership mapping, open-source intelligence tactics"},
        {"name": "r/supplychain", "relevance": "UFLPA compliance, transshipment routing, supplier questionnaire frustrations"},
        {"name": "r/customs", "relevance": "Customs broker holds, BIS export controls, dual-use shipping documents"}
    ],
    "publications_and_authors": [
        {"name": "FiveBy Risk News & Insights (Substack)", "focus": "Sanctions evasion networks, transshipment hubs, investigative teardowns"},
        {"name": "Steptoe International Compliance Blog", "focus": "OFAC enforcement, export control rule updates, BIS advisory notices"},
        {"name": "Holland & Hart TradeSanctions.com", "focus": "Practical commentary on trade sanctions, SDN designations, 50% rule traps"},
        {"name": "FCPA Blog", "focus": "Anti-bribery enforcement, third-party risk management (TPRM), corporate corruption cases"},
        {"name": "Export Control Navigator", "focus": "Semiconductor export curbs, dual-use technology diversion, Russian sanction evasion"},
        {"name": "ACAMS moneylaundering.com", "focus": "Global financial crime news, regulatory exams, FinCEN advisories"},
        {"name": "AML Intelligence", "focus": "European AML authority developments, banking penalties, sanctions enforcement"}
    ],
    "target_companies_career_pages": [
        {"company": "JPMorgan Chase / Citi / HSBC (Global Banks)", "reason": "Job descriptions detail exact pain points: alert clearing volume, name screening false positives, legacy watchlists"},
        {"company": "Stripe / Revolut / Wise (Fintechs)", "reason": "Fast-scaling KYB backlog, merchant entity resolution, automated onboarding friction"},
        {"company": "PwC / EY / Deloitte / Guidehouse (AML Advisory)", "reason": "Remediation projects for banks under consent decrees; reveals what broken compliance looks like"},
        {"company": "Boeing / Caterpillar / Apple / Flex (Global Manufacturing)", "reason": "Supply chain Tier 1 vs Tier 2 visibility, UFLPA detention notices, forced labor audits"},
        {"company": "Archer Daniels Midland / Bunge / Cargill (Ag & Commodities)", "reason": "Complex maritime transshipment, ownership obscurity, multi-jurisdiction trade routes"}
    ],
    "manual_import_only_sources": [
        {"platform": "LinkedIn Comments & Posts", "note": "Collect by hand only (never scrape). Paste rants and commentary into data/imports/"},
        {"platform": "G2 / Capterra Reviews", "note": "Customer reviews of screening tools (Moody's, LexisNexis, Dow Jones) highlighting UI lag and false positives"},
        {"platform": "Glassdoor / Blind", "note": "Employee reviews of L1 compliance operations ('sweatshop alert mills', backlog quotas)"}
    ]
}

def discover_candidates() -> Dict[str, Any]:
    """Returns candidate sources structured for human review and approval."""
    return DISCOVERY_CATALOG

def export_discovery_markdown(filepath: str = "source_candidates.md"):
    """Writes out the discovery candidates into a readable Markdown approval document."""
    lines = [
        "# Source Discovery: Candidate Review & Approval List",
        "",
        "> [!IMPORTANT]",
        "> Per project rules, no source is collected until you review and approve it.",
        "> Automated scrapers for LinkedIn, G2, Glassdoor, and Blind are strictly disabled.",
        "",
        "## 1. Candidate Subreddits",
        "| Subreddit | Why It Matters | Status |",
        "| :--- | :--- | :--- |"
    ]
    for sub in DISCOVERY_CATALOG["subreddits"]:
        lines.append(f"| **{sub['name']}** | {sub['relevance']} | [x] Approved in config.yaml |" if sub["name"] in ["r/AMLCompliance", "r/financialcrime", "r/compliance", "r/RegulatoryCompliance"] else f"| **{sub['name']}** | {sub['relevance']} | [ ] Recommended for approval |")

    lines.extend([
        "",
        "## 2. Industry Publications & Expert Commentary (RSS / Public Pages)",
        "| Source | Editorial Focus | Status |",
        "| :--- | :--- | :--- |"
    ])
    for pub in DISCOVERY_CATALOG["publications_and_authors"]:
        lines.append(f"| **{pub['name']}** | {pub['focus']} | [x] Configured in config.yaml |")

    lines.extend([
        "",
        "## 3. Companies Whose Career Pages Reveal Real Stack Frustrations",
        "| Company Archetype | What Job Postings Reveal | Manual / Feed |",
        "| :--- | :--- | :--- |"
    ])
    for co in DISCOVERY_CATALOG["target_companies_career_pages"]:
        lines.append(f"| **{co['company']}** | {co['reason']} | Inspect public job board RSS/alerts |")

    lines.extend([
        "",
        "## 4. Manual Import Only (Do NOT Scrape)",
        "| Platform | Recommended Use |",
        "| :--- | :--- |"
    ])
    for m in DISCOVERY_CATALOG["manual_import_only_sources"]:
        lines.append(f"| **{m['platform']}** | {m['note']} |")

    lines.extend([
        "",
        "---",
        "*To approve additional subreddits or RSS feeds, add them to `config.yaml`.*"
    ])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return filepath
