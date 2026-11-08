#!/usr/bin/env python3
# run.py — Command-Line Interface for the Sayari Research Tool
# Usage:
#   python run.py analyze-text           # Test analysis, tagging & idea generation on text
#   python run.py discover               # Discover and review candidate subreddits & sources
#   python run.py collect-reddit [sub]   # Collect from official Reddit API with PRAW
#   python run.py collect-rss            # Collect from public RSS & commentary feeds
#   python run.py import-manual          # Import hand-collected CSV or TXT files from data/imports/
#   python run.py generate-ideas         # Generate ranked idea bank & glossary from stored items
#   python run.py pipeline               # Run full pipeline and update all exports & HTML viewer
#
# Requires: pyyaml, feedparser, praw, beautifulsoup4, requests

import sys
import os
import argparse
import time

from src.config import load_config
from src.db import init_db, get_db_connection, insert_raw_item
from src.filters import evaluate_item
from src.analyzer import analyze_item, cluster_items_ollama, extract_glossary_from_items
from src.ideator import generate_ranked_ideas
from src.discovery import export_discovery_markdown, discover_candidates
from src.collectors.reddit import collect_from_reddit
from src.collectors.rss import collect_from_rss_source
from src.collectors.manual import import_manual_files
from src.reporter import generate_all_outputs

def cmd_discover(config):
    print("\n--- Source Discovery: Candidate Review List ---")
    candidates = discover_candidates()
    print(f"\n[1] Subreddits ({len(candidates['subreddits'])} identified):")
    for s in candidates['subreddits']:
        print(f"  - {s['name']}: {s['relevance']}")

    print(f"\n[2] Publications & Commentary ({len(candidates['publications_and_authors'])} identified):")
    for p in candidates['publications_and_authors']:
        print(f"  - {p['name']} ({p['focus']})")

    print(f"\n[3] Companies Whose Career Pages Reveal Stack Frustrations ({len(candidates['target_companies_career_pages'])} archetypes):")
    for c in candidates['target_companies_career_pages']:
        print(f"  - {c['company']}")

    print("\n[4] Manual Import Only (Do NOT Scrape):")
    for m in candidates['manual_import_only_sources']:
        print(f"  - {m['platform']}: {m['note']}")

    md_path = export_discovery_markdown("source_candidates.md")
    print(f"\nDiscovery candidate list exported to: {md_path}")
    print("Review and approve candidates before adding them to config.yaml.\n")

def cmd_analyze_text(config, text_sample=None):
    print("\n--- Running Analysis on Text Input ---")
    db_path = config.get("database", {}).get("path", "data/sayari.db")
    init_db(db_path)
    conn = get_db_connection(db_path)

    # Seed samples representing real practitioner discussions if none passed
    sample_posts = [
        # Theme: Entity Resolution & Name Matching
        {
            "id": "sample_1",
            "source": "pasted:r/AMLCompliance",
            "url": "https://reddit.com/r/AMLCompliance/comments/nm01",
            "title": "Drowning in name matching false positives on common Latin names",
            "body": "Our L1 review queue has 800 alerts backlog. The screening tool flags every Jose Gomez regardless of DOB or jurisdiction. Swivel chairing between 6 tabs to find the beneficial ownership record is a nightmare."
        },
        {
            "id": "sample_2",
            "source": "pasted:r/compliance",
            "url": "https://reddit.com/r/compliance/comments/nm02",
            "title": "One company in three spellings keeps breaking automated onboarding",
            "body": "Global Electronics Inc, Global Electronic LLC, and Global Electronics Ltd are all in our vendor database. Automated name match treats them as three different entities. Manual review takes 45 mins per supplier."
        },
        {
            "id": "sample_3",
            "source": "pasted:r/financialcrime",
            "url": "https://reddit.com/r/financialcrime/comments/nm03",
            "title": "False positive rates over 95% on fuzzy name matching algorithms",
            "body": "Management bought an AI screening tool promising zero-resistance. Reality: 98% false positives and our analysts are manually clearing identical names in Excel spreadsheets."
        },
        # Theme: UBO, Shell Companies & Transshipment
        {
            "id": "sample_4",
            "source": "pasted:r/financialcrime",
            "url": "https://reddit.com/r/financialcrime/comments/ubo01",
            "title": "Vendor questionnaire claimed zero SDN ties, but UBO is an OFAC designated oligarch",
            "body": "Supplier screening questionnaire was completely clean. But when we pulled the corporate ownership chain, the Cyprus holding company is 51% owned by a sanctioned entity under the 50 percent rule."
        },
        {
            "id": "sample_5",
            "source": "pasted:r/AMLCompliance",
            "url": "https://reddit.com/r/AMLCompliance/comments/ubo02",
            "title": "One single residential flat in Belize registered to 240 shell companies",
            "body": "Investigating a wire transfer for electronic components. Found a single residential address housing over two hundred registered trading entities. Pure transshipment evasion front."
        },
        {
            "id": "sample_6",
            "source": "pasted:r/OSINT",
            "url": "https://reddit.com/r/OSINT/comments/ubo03",
            "title": "Four layers of holding companies to hide beneficial ownership in UAE free zones",
            "body": "Tracing dual-use tech exports. Every tier references another nominee director until you hit an offshore trust. Self-certified forms are completely useless."
        },
        # Theme: Swivel Chair Manual Review & Frankenstack
        {
            "id": "sample_7",
            "source": "pasted:r/RegulatoryCompliance",
            "url": "https://reddit.com/r/RegulatoryCompliance/comments/fs01",
            "title": "The Frankenstack is real: Excel, Dow Jones, Moody's, and endless tabs",
            "body": "We have 4 different watchlist screening tools and none of them talk to each other. An analyst has to manually check each company name in 3 spellings across 6 tabs."
        },
        {
            "id": "sample_8",
            "source": "pasted:r/AMLCompliance",
            "url": "https://reddit.com/r/AMLCompliance/comments/fs02",
            "title": "Breakup note to our compliance tech stack",
            "body": "Dear vendor stack: I cannot keep copy-pasting business registration numbers from registry PDFs into Excel final_v7.xlsx. Swivel chair review is destroying our analysts."
        },
        {
            "id": "sample_9",
            "source": "pasted:r/compliance",
            "url": "https://reddit.com/r/compliance/comments/fs03",
            "title": "81% of our compliance tools don't talk to each other",
            "body": "Our EDD workflow requires querying 5 databases, exporting CSVs, and manually reconciling corporate hierarchies. The backlog is now 6 weeks deep."
        },
        # Theme: Audit Panic & Regulatory Examination
        {
            "id": "sample_10",
            "source": "pasted:r/compliance",
            "url": "https://reddit.com/r/compliance/comments/audit01",
            "title": "Audit panic: regulator exam asked for our disposition rationale",
            "body": "The regulator audit asked how we verified tier-2 suppliers under UFLPA. Our compliance stack gave us a risk score of 87, but the examiner said a score is not a defense without registry proof."
        },
        {
            "id": "sample_11",
            "source": "pasted:r/financialcrime",
            "url": "https://reddit.com/r/financialcrime/comments/audit02",
            "title": "Regulators don't accept 'the tool gave it an 85' as due diligence",
            "body": "FinCEN and OFAC enforcement actions show that relying on an automated black-box score without source documents guarantees a penalty notice."
        },
        {
            "id": "sample_12",
            "source": "pasted:r/RegulatoryCompliance",
            "url": "https://reddit.com/r/RegulatoryCompliance/comments/audit03",
            "title": "Examiner asked for proof of our sub-tier forced labor audit trail",
            "body": "We had clean questionnaires from tier 1 suppliers, but zero visibility into sub-tier component manufacturers. The exam team wrote us up for deficient TPRM."
        }
    ]

    items_to_process = []
    if text_sample:
        items_to_process.append({
            "id": "user_pasted_1",
            "source": "manual:pasted_text",
            "url": "file://manual_input",
            "title": text_sample[:60],
            "body": text_sample
        })
    else:
        items_to_process = sample_posts

    processed_items = []
    for post in items_to_process:
        passed, reason, matched = evaluate_item(post["title"], post["body"], config)
        analysis = analyze_item(post["title"], post["body"], config)
        
        item_dict = {
            "id": post["id"],
            "source": post["source"],
            "url": post["url"],
            "date": time.strftime("%Y-%m-%d"),
            "title": post["title"],
            "short_excerpt": post["body"],
            "paraphrase": post["body"],
            "upvotes": 15,
            "comment_count": 8,
            "paraphrased_top_comments": ["Same exact issue at our bank.", "Spreadsheets are our entire screening stack."],
            "theme": analysis["theme"],
            "emotion": analysis["emotion"],
            "intensity": analysis["intensity"],
            "post_type": analysis["post_type"],
            "audience": analysis["audience"],
            "used_terms": analysis["used_terms"],
            "passed_filters": passed,
            "drop_reason": reason
        }
        insert_raw_item(conn, item_dict)
        if passed:
            processed_items.append(item_dict)

    print(f"Evaluated {len(items_to_process)} items -> {len(processed_items)} passed compliance filters.")

    # Clustering and Idea Generation
    clusters = cluster_items_ollama(processed_items, config)
    print(f"Clustered into {len(clusters)} themes.")
    for theme, itms in clusters.items():
        print(f"  * {theme}: {len(itms)} sources")

    glossary = extract_glossary_from_items(processed_items)
    ideas = generate_ranked_ideas(clusters)
    
    print(f"\nGenerated {len(ideas)} ranked content ideas:")
    for idx, idea in enumerate(ideas, 1):
        print(f"  [{idx}] ({idea['format']}) {idea['title']} (Score: {idea['rank_score']})")

    generate_all_outputs(conn, ideas, glossary)
    conn.close()
    print("\nExported: ideas.csv, ideas.md, glossary.csv, raw_items.csv, viewer/index.html")

def cmd_collect_reddit(config, sub_name=None):
    reddit_cfg = config.get("reddit", {})
    client_id = reddit_cfg.get("client_id", "").strip()
    client_secret = reddit_cfg.get("client_secret", "").strip()

    if not client_id or not client_secret:
        print("\n" + "="*70)
        print("REDDIT API SETUP INSTRUCTIONS")
        print("="*70)
        print("To collect public Reddit posts via the official API:")
        print("1. Go to https://www.reddit.com/prefs/apps and log in.")
        print("2. Scroll to the bottom and click 'create another app...' (or 'create app').")
        print("3. Select 'script' (for personal use / non-commercial research).")
        print("4. Set name: e.g. 'sayari-research-tool'")
        print("5. Set redirect uri: http://localhost:8080 (required placeholder).")
        print("6. Copy the client ID (under app name) and secret into config.yaml:")
        print("     reddit:")
        print("       client_id: 'YOUR_CLIENT_ID'")
        print("       client_secret: 'YOUR_CLIENT_SECRET'")
        print("\nREMINDER ON FREE NON-COMMERCIAL TIER:")
        print("Reddit's Developer Terms grant free API access for personal, non-commercial")
        print("research scripts (up to 100 queries/minute via OAuth). Ensure your use fits")
        print("non-commercial content research before scaling.")
        print("="*70 + "\n")
        return

    subreddits = [sub_name] if sub_name else reddit_cfg.get("subreddits", ["AMLCompliance"])
    db_path = config.get("database", {}).get("path", "data/sayari.db")
    init_db(db_path)
    conn = get_db_connection(db_path)

    for sub in subreddits:
        print(f"[reddit] Collecting posts from r/{sub}...")
        posts = collect_from_reddit(sub, config)
        print(f"[reddit] Fetched {len(posts)} posts from r/{sub}.")
        for post in posts:
            passed, reason, matched = evaluate_item(post["title"], post["short_excerpt"], config)
            analysis = analyze_item(post["title"], post["short_excerpt"], config)
            post.update(analysis)
            post["passed_filters"] = passed
            post["drop_reason"] = reason
            insert_raw_item(conn, post)

    conn.close()
    print("[reddit] Collection complete. Run 'python run.py generate-ideas' to update the idea bank.")

def cmd_collect_rss(config):
    print("\n--- Collecting from Public RSS Feeds & Commentary ---")
    db_path = config.get("database", {}).get("path", "data/sayari.db")
    init_db(db_path)
    conn = get_db_connection(db_path)

    rss_sources = config.get("rss_sources", {})
    all_sources = rss_sources.get("major", []) + rss_sources.get("independent", [])

    total_added = 0
    for src in all_sources:
        if not src.get("enabled", True):
            continue
        print(f"[rss] Fetching {src.get('name')} ({src.get('url')})...")
        items = collect_from_rss_source(src, config, conn)
        print(f"      -> {len(items)} items received.")
        for item in items:
            passed, reason, matched = evaluate_item(item["title"], item["short_excerpt"], config)
            analysis = analyze_item(item["title"], item["short_excerpt"], config)
            item.update(analysis)
            item["passed_filters"] = passed
            item["drop_reason"] = reason
            insert_raw_item(conn, item)
            total_added += 1

    conn.close()
    print(f"\nRSS collection complete. Processed {total_added} entries across feeds.")

def cmd_import_manual(config):
    print("\n--- Importing from Manual Files (data/imports/) ---")
    db_path = config.get("database", {}).get("path", "data/sayari.db")
    init_db(db_path)
    conn = get_db_connection(db_path)

    manual_dir = config.get("storage", {}).get("manual_import_dir", "data/imports")
    items = import_manual_files(manual_dir)
    print(f"Found {len(items)} items across manual import files.")

    for item in items:
        passed, reason, matched = evaluate_item(item["title"], item["short_excerpt"], config)
        analysis = analyze_item(item["title"], item["short_excerpt"], config)
        item.update(analysis)
        item["passed_filters"] = passed
        item["drop_reason"] = reason
        insert_raw_item(conn, item)

    conn.close()
    print(f"Imported {len(items)} manual entries into SQLite.")

def cmd_generate_ideas(config):
    print("\n--- Generating Idea Bank & Glossary ---")
    db_path = config.get("database", {}).get("path", "data/sayari.db")
    init_db(db_path)
    conn = get_db_connection(db_path)

    cur = conn.cursor()
    cur.execute("SELECT * FROM raw_items WHERE passed_filters=1")
    rows = [dict(r) for r in cur.fetchall()]
    print(f"Analyzing {len(rows)} validated compliance items from SQLite...")

    if not rows:
        print("No items in database yet. Running initial seed analysis...")
        cmd_analyze_text(config)
        return

    clusters = cluster_items_ollama(rows, config)
    glossary = extract_glossary_from_items(rows)
    ideas = generate_ranked_ideas(clusters)

    generate_all_outputs(conn, ideas, glossary)
    conn.close()

    print(f"\nIdea bank successfully generated with {len(ideas)} ideas.")
    print("Files updated:")
    print("  - ideas.csv (Ranked & structured)")
    print("  - ideas.md (Detailed brief with evidence citations)")
    print("  - glossary.csv (Practitioner language vs vendor buzzwords)")
    print("  - raw_items.csv (All filtered items)")
    print("  - blocked_sources.md (Compliance & robots.txt log)")
    print("  - viewer/index.html (Interactive local viewer)")

def cmd_pipeline(config):
    print("\n=======================================================")
    print("SAYARI CONTENT RESEARCH TOOL — FULL RUN PIPELINE")
    print("=======================================================")
    cmd_import_manual(config)
    cmd_collect_rss(config)
    cmd_collect_reddit(config)
    cmd_generate_ideas(config)
    print("\nPipeline execution complete! Open viewer/index.html in browser to explore.")

def main():
    parser = argparse.ArgumentParser(description="Sayari LinkedIn Research & Idea Bank Tool")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("discover", help="Discover candidate subreddits & sources for approval")
    
    analyze_parser = subparsers.add_parser("analyze-text", help="Analyze pasted text or run seed test")
    analyze_parser.add_argument("--text", type=str, default=None, help="Pasted compliance text to analyze")

    reddit_parser = subparsers.add_parser("collect-reddit", help="Collect from official Reddit API")
    reddit_parser.add_argument("--sub", type=str, default=None, help="Specific subreddit to collect")

    subparsers.add_parser("collect-rss", help="Collect from public RSS news and commentary feeds")
    subparsers.add_parser("import-manual", help="Import hand-collected CSV or text files")
    subparsers.add_parser("generate-ideas", help="Cluster items and generate ranked idea bank")
    subparsers.add_parser("pipeline", help="Run full end-to-end collection and idea generation")

    args = parser.parse_args()
    config = load_config()

    if args.command == "discover":
        cmd_discover(config)
    elif args.command == "analyze-text":
        cmd_analyze_text(config, args.text)
    elif args.command == "collect-reddit":
        cmd_collect_reddit(config, args.sub)
    elif args.command == "collect-rss":
        cmd_collect_rss(config)
    elif args.command == "import-manual":
        cmd_import_manual(config)
    elif args.command == "generate-ideas":
        cmd_generate_ideas(config)
    elif args.command == "pipeline":
        cmd_pipeline(config)
    else:
        # Default behavior: run text analysis & show status
        cmd_analyze_text(config)

if __name__ == "__main__":
    main()
