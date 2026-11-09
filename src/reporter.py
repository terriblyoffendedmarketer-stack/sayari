# src/reporter.py — Output Generator & Local Viewer Exporter
# Usage: from src.reporter import generate_all_outputs
# Requires: csv, json, os, sqlite3

import os
import csv
import json
import sqlite3
from typing import List, Dict, Any

def export_raw_items_csv(conn: sqlite3.Connection, filepath: str = "raw_items.csv"):
    cur = conn.cursor()
    cur.execute("""
    SELECT id, source, url, date, title, short_excerpt, paraphrase, upvotes, comment_count, theme, emotion, intensity, post_type, audience, passed_filters
    FROM raw_items
    ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    
    headers = ["id", "source", "url", "date", "title", "short_excerpt", "paraphrase", "upvotes", "comment_count", "theme", "emotion", "intensity", "post_type", "audience", "passed_filters"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in rows:
            writer.writerow([r[h] for h in headers])

def export_ideas_csv(ideas: List[Dict[str, Any]], filepath: str = "ideas.csv"):
    headers = [
        "rank_score", "title", "format", "pillar", "hook", "suggested_visual",
        "extends_idea", "source_count", "avg_intensity", "engagement_score",
        "risks", "verify_before_use", "evidence_urls"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for idea in ideas:
            evidence_urls = "; ".join([ev.get("url", "") for ev in idea.get("evidence_sources", [])])
            writer.writerow([
                idea.get("rank_score", 0),
                idea.get("title", ""),
                idea.get("format", ""),
                idea.get("pillar", ""),
                idea.get("hook", ""),
                idea.get("suggested_visual", ""),
                idea.get("extends_idea", ""),
                idea.get("source_count", 0),
                idea.get("avg_intensity", 0),
                idea.get("engagement_score", 0),
                idea.get("risks", ""),
                idea.get("verify_before_use", ""),
                evidence_urls
            ])

def export_ideas_markdown(ideas: List[Dict[str, Any]], filepath: str = "ideas.md"):
    lines = [
        "# Sayari Content Idea Bank (Ranked & Sourced)",
        "",
        "Every idea below is mapped to Sayari's 4 core formats, backed by multiple public sources, and includes suggested visual portrayal, hook, and risk checks.",
        "",
        "| Rank | Score | Title | Format | Pillar | Extends Doc Idea | Sources | Intensity |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for idx, idea in enumerate(ideas, start=1):
        lines.append(
            f"| {idx} | **{idea.get('rank_score')}** | [{idea.get('title')}](#idea-{idx}) | {idea.get('format')} | {idea.get('pillar')} | {idea.get('extends_idea')} | {idea.get('source_count')} | {idea.get('avg_intensity')}/5 |"
        )
    
    lines.append("\n---\n")
    
    for idx, idea in enumerate(ideas, start=1):
        lines.extend([
            f"### <a id='idea-{idx}'></a>#{idx}. {idea.get('title')}",
            f"- **Format:** `{idea.get('format')}`",
            f"- **Pillar:** {idea.get('pillar')}",
            f"- **Extends Doc Idea:** *{idea.get('extends_idea')}*",
            f"- **The Hook:** \"{idea.get('hook')}\"",
            f"- **Suggested Visual Portrayal:** {idea.get('suggested_visual')}",
            f"- **Metrics:** Backed by {idea.get('source_count')} independent sources | Engagement Score: {idea.get('engagement_score')} | Avg Intensity: {idea.get('avg_intensity')}/5",
            f"- **Risks:** {idea.get('risks')}",
            f"- **Verify Before Use:** {idea.get('verify_before_use')}",
            "",
            "**Evidence & Sourced Public Reaction:**"
        ])
        for ev in idea.get("evidence_sources", []):
            lines.append(f"  - [{ev.get('url')}]({ev.get('url')}) ({ev.get('date')}, {ev.get('upvotes')} upvotes, {ev.get('comments')} comments): *\"{ev.get('paraphrase')}\"*")
        lines.append("\n---\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def export_glossary_csv(glossary: List[Dict[str, Any]], filepath: str = "glossary.csv"):
    headers = ["term", "frequency", "source_count", "is_vendor_marketing_only", "example_context"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for g in glossary:
            is_vendor_flag = "YES (Vendor Buzzword)" if (str(g.get("is_vendor_marketing_only", "")).upper() in ("1", "YES", "TRUE") or g.get("is_vendor_marketing_only") == 1) else "NO (Real Practitioner Term)"
            writer.writerow([
                g.get("term"),
                g.get("frequency"),
                g.get("source_count"),
                is_vendor_flag,
                g.get("example_context", "")
            ])

def export_blocked_sources_md(conn: sqlite3.Connection, filepath: str = "blocked_sources.md"):
    cur = conn.cursor()
    cur.execute("SELECT source_name, url, reason, timestamp FROM blocked_sources ORDER BY timestamp DESC")
    rows = cur.fetchall()

    lines = [
        "# Blocked Sources Log",
        "",
        "> [!NOTE]",
        "> Per project rules, we respect robots.txt and paywalls. When a source cannot be accessed legitimately, it is logged here rather than attempting anti-bot circumvention or proxy rotation.",
        "",
        "| Source | URL | Reason Logged | Timestamp |",
        "| :--- | :--- | :--- | :--- |"
    ]
    if not rows:
        lines.append("| *(None logged yet)* | - | All configured feeds currently responding normally | - |")
    else:
        for r in rows:
            lines.append(f"| **{r['source_name']}** | {r['url']} | {r['reason']} | {r['timestamp']} |")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

def generate_claude_dump_text(ideas: List[Dict[str, Any]], raw_items: List[Dict[str, Any]], glossary: List[Dict[str, Any]]) -> str:
    lines = [
        "# SAYARI COMPLIANCE SIGNAL BANK & INTELLIGENCE DUMP",
        "# (Link-free format with unique trace IDs for direct input into Claude)",
        "",
        "## 1. VOICE, AUDIENCE & STRATEGY CONTEXT",
        "- Brand: Sayari (Corporate ownership and supply chain risk intelligence).",
        "- Primary Audience: Compliance officers (sanctions, financial crime, KYB) and investigations/L1 analysts. NOT C-suite budget approvers.",
        "- Audience Psychographics: Powerless but accountable, drowning in alerts, cynical of new tools, quietly afraid of audits.",
        "- Tone: Validating, unflinching, human, a little funny, proof-backed. Must pass the 'Beer Test'.",
        "- Banned Vendor Buzzwords: 'judgment infrastructure', 'zero-resistance', 'leverage synergies', 'holistic ecosystem', 'single pane of glass'.",
        "- 4 Formats: Pain Mirror (35%), Product as Relief (25%), The Receipts / Investigation Teardown (20%), Headline to Lesson / Newsjack (20%).",
        "",
        "## 2. THE 'BEER TEST' LEXICON (PRACTITIONER SLANG VS VENDOR FLUFF)",
    ]
    
    for g in glossary:
        term = g.get("term", "")
        vendor_val = str(g.get("is_vendor_marketing_only", "")).upper()
        is_vendor = "BANNED VENDOR BUZZWORD" if ("YES" in vendor_val or vendor_val == "1") else "AUTHENTIC PRACTITIONER TERM"
        lines.append(f"- {term.upper()} [{is_vendor}]: {g.get('example_context', '')}")

    lines.append("\n## 3. SAYARI VERIFIED PROOF ANCHORS")
    lines.append("- [Proof #1] No. 3 Global Telecom: 72% of flagged risk was on zero watchlists anywhere, hidden in nested ownership (60K+ partners screened continuously).")
    lines.append("- [Proof #2] Fortune 50 Energy Supermajor: 1.2M records screened in real time (competing platform required 24–48 hours).")
    lines.append("- [Proof #3] Fortune 50 Energy Company: 75+ disparate data sources collapsed into one; costly homegrown system retired.")
    lines.append("- [Proof #4] Top-5 Global Tech Company: Chose Sayari over supply-chain incumbent for sub-tier mapping.")
    lines.append("- [Benchmark #1] Sanctions screening false positive rate is 90% to 95%.")
    lines.append("- [Benchmark #2] 81% of compliance teams say their risk tools are not integrated.")
    lines.append("- [Benchmark #3] 65% rely on manual Google searches for adverse media; >25% manage periodic reviews in spreadsheets.")

    lines.append("\n## 4. MASTER RANKED IDEAS BANK (WITH HOOKS & METAPHORS)")
    for idx, idea in enumerate(ideas, 1):
        lines.append(f"\n### [Idea #{idx:02d}] {idea.get('title')}")
        lines.append(f"- Format: {idea.get('format')} | Pillar: {idea.get('pillar')}")
        lines.append(f"- The Hook: \"{idea.get('hook')}\"")
        lines.append(f"- Suggested Visual Metaphor: {idea.get('suggested_visual')}")
        lines.append(f"- Supporting Public Evidence:")
        for ev_idx, ev in enumerate(idea.get("evidence_sources", []), 1):
            source_clean = ev.get("url", "").replace("https://www.reddit.com/r/", "Reddit r/").replace("https://", "").split("/")[0]
            lines.append(f"  * [Evidence #{idx:02d}-{ev_idx:02d} | Source: {source_clean}]: \"{ev.get('paraphrase')}\"")

    lines.append("\n## 5. COMPLETE EVIDENCE BANK (SOURCED WITH UNIQUE TRACE IDS)")
    for idx, it in enumerate(raw_items, 1):
        source_clean = it.get("source", "").replace("pasted:", "").replace("rss:", "").replace("manual:", "")
        lines.append(f"\n[Trace ID #{idx:02d}]")
        lines.append(f"- Source Channel: {source_clean}")
        lines.append(f"- Title/Topic: {it.get('title')}")
        lines.append(f"- Excerpt/Quote: \"{it.get('short_excerpt')}\"")
        lines.append(f"- Context Summary: \"{it.get('paraphrase')}\"")
        lines.append(f"- Theme: {it.get('theme', 'General')} | Emotion Intensity: {it.get('intensity', 1)}/5 ({it.get('emotion', 'frustration')})")

    lines.append("\n## 6. INSTRUCTIONS FOR CLAUDE")
    lines.append("Use the signals, quotes, and proof points above to draft authentic LinkedIn posts for Sayari.")
    lines.append("Follow the 4 core formats, strictly maintain the human/unflinching tone, and avoid all vendor buzzwords.")

    return "\n".join(lines)

def export_claude_dump_md(dump_text: str, filepath: str = "reports/claude_dump.md"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(dump_text)

def export_html_viewer(
    ideas: List[Dict[str, Any]],
    raw_items: List[Dict[str, Any]],
    glossary: List[Dict[str, Any]],
    dropped_items: List[Dict[str, Any]],
    pipeline_runs: List[Dict[str, Any]],
    sweep_time: str,
    filepath: str = "viewer/index.html"
):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    ideas_json = json.dumps(ideas)
    items_json = json.dumps(raw_items)
    glossary_json = json.dumps(glossary)
    dropped_json = json.dumps(dropped_items)
    runs_json = json.dumps(pipeline_runs)
    claude_dump_text = generate_claude_dump_text(ideas, raw_items, glossary)
    claude_dump_json = json.dumps(claude_dump_text)
    export_claude_dump_md(claude_dump_text, "reports/claude_dump.md")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sayari Compliance Signal Radar & Living Brain</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" type="image/svg+xml" href="icons/icon.svg">
<link rel="alternate icon" type="image/png" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Sayari Radar">
<meta name="theme-color" content="#090d16">
<meta name="description" content="Living psychographic compliance radar & content ideas for Sayari.">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<style>
  :root {{
    --bg: #090d16;
    --card: #131c2e;
    --card-hover: #1a273f;
    --text: #f8fafc;
    --muted: #94a3b8;
    --border: #23314a;
    --accent: #38bdf8;
    --accent-glow: rgba(56, 189, 248, 0.15);
    --tag-pain: #f87171;
    --tag-relief: #34d399;
    --tag-receipts: #fbbf24;
    --tag-news: #818cf8;
    --btn-copy: #0284c7;
    --btn-copy-hover: #0369a1;
    --btn-dump: #10b981;
    --btn-dump-hover: #059669;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; background: var(--bg); color: var(--text); padding: 20px 28px; line-height: 1.5; }}
  
  /* Header */
  header {{ margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; }}
  .title-area h1 {{ font-size: 24px; font-weight: 800; color: #fff; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }}
  .title-area h1 span.radar {{ color: var(--accent); }}
  p.subtitle {{ color: var(--muted); font-size: 13.5px; margin-top: 4px; }}
  
  .header-actions {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .btn-dump-all {{ background: var(--btn-dump); color: #fff; border: none; padding: 9px 16px; border-radius: 8px; font-size: 13px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25); }}
  .btn-dump-all:hover {{ background: var(--btn-dump-hover); transform: translateY(-1px); }}
  .sweep-badge {{ background: var(--card); border: 1px solid var(--border); padding: 7px 12px; border-radius: 8px; font-size: 12px; display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }}
  .sweep-time {{ color: var(--accent); font-weight: 700; }}

  /* Tabs */
  .tabs {{ display: flex; gap: 8px; margin-bottom: 18px; border-bottom: 1px solid var(--border); padding-bottom: 8px; flex-wrap: wrap; }}
  .tab-btn {{ background: transparent; border: none; color: var(--muted); padding: 9px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 13.5px; transition: all 0.2s; }}
  .tab-btn:hover {{ color: #fff; background: var(--card); }}
  .tab-btn.active {{ background: var(--card); color: var(--accent); border-bottom: 2px solid var(--accent); }}

  /* Filters */
  .filters {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; background: var(--card); padding: 12px 16px; border-radius: 10px; border: 1px solid var(--border); align-items: flex-end; }}
  .filter-group {{ display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 170px; }}
  label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }}
  select, input {{ background: #0b1120; color: #fff; border: 1px solid var(--border); padding: 8px 12px; border-radius: 6px; font-size: 13px; outline: none; }}
  select:focus, input:focus {{ border-color: var(--accent); }}

  /* Grid & Cards */
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(440px, 1fr)); gap: 18px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 12px; transition: all 0.2s; position: relative; }}
  .card:hover {{ border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }}
  .card-header {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; }}
  
  .badge {{ font-size: 11px; font-weight: 700; text-transform: uppercase; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.5px; }}
  .badge-pain {{ background: rgba(248, 113, 113, 0.2); color: var(--tag-pain); border: 1px solid var(--tag-pain); }}
  .badge-relief {{ background: rgba(52, 211, 153, 0.2); color: var(--tag-relief); border: 1px solid var(--tag-relief); }}
  .badge-receipts {{ background: rgba(251, 191, 36, 0.2); color: var(--tag-receipts); border: 1px solid var(--tag-receipts); }}
  .badge-news {{ background: rgba(129, 140, 248, 0.2); color: var(--tag-news); border: 1px solid var(--tag-news); }}

  .idea-title {{ font-size: 16.5px; font-weight: 700; color: #fff; line-height: 1.35; }}
  .hook-box {{ background: #0b1220; border-left: 3px solid var(--accent); padding: 10px 14px; font-style: italic; color: #e2e8f0; font-size: 13px; border-radius: 0 6px 6px 0; }}
  
  .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px; color: var(--muted); }}
  .meta-grid div {{ background: #0f172a; padding: 6px 10px; border-radius: 6px; border: 1px solid var(--border); }}
  .meta-grid strong {{ color: #cbd5e1; }}
  
  .evidence-section {{ background: #0c1424; padding: 10px 12px; border-radius: 6px; font-size: 12px; border: 1px dashed var(--border); }}
  .evidence-header {{ font-weight: 700; color: #cbd5e1; margin-bottom: 6px; }}
  .evidence-item {{ margin-bottom: 6px; color: #94a3b8; line-height: 1.4; }}
  
  .copy-btn {{ background: var(--btn-copy); color: #fff; border: none; padding: 7px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.2s; display: inline-flex; align-items: center; gap: 6px; align-self: flex-start; }}
  .copy-btn:hover {{ background: var(--btn-copy-hover); }}

  /* Responsive Table View (No Horizontal Scrolling, Word Wrap) */
  .table-container {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin-top: 10px; }}
  .table-view {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; table-layout: fixed; }}
  .table-view th {{ background: #0f182c; padding: 10px 12px; font-weight: 700; color: var(--muted); text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; border-bottom: 1px solid var(--border); }}
  .table-view td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); color: #e2e8f0; vertical-align: top; word-wrap: break-word; overflow-wrap: break-word; }}
  .table-view tr:hover td {{ background: #162238; }}
  
  /* Sized Down Images */
  .table-view img, .evidence-section img, .card img {{
    max-width: 120px;
    max-height: 80px;
    object-fit: contain;
    border-radius: 4px;
    border: 1px solid var(--border);
    display: block;
    margin: 4px 0;
  }}

  /* Collapsible Text / Expand Toggle */
  .collapsible-text {{ max-height: 60px; overflow: hidden; position: relative; line-height: 1.4; }}
  .collapsible-text.expanded {{ max-height: none; }}
  .expand-btn {{ background: transparent; border: none; color: var(--accent); font-size: 11px; cursor: pointer; font-weight: 700; padding: 2px 0; display: inline-block; }}
  .expand-btn:hover {{ text-decoration: underline; }}
  
  .source-link {{ color: var(--accent); text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; }}
  .source-link:hover {{ text-decoration: underline; color: #7dd3fc; }}

  .trace-id {{ display: inline-block; background: #1e293b; color: #38bdf8; font-family: monospace; font-size: 11px; padding: 2px 6px; border-radius: 4px; border: 1px solid #334155; }}
  .pill {{ font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600; display: inline-block; }}

  /* Run Log Badge */
  .badge-cloud {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #38bdf8; }}
  .badge-local {{ background: rgba(148, 163, 184, 0.2); color: #94a3b8; border: 1px solid #64748b; }}

  /* Knowledge Graph Canvas Area */
  #graphContainer {{ background: #070b14; border: 1px solid var(--border); border-radius: 12px; position: relative; overflow: hidden; }}
  #graphCanvas {{ width: 100%; height: 620px; display: block; }}
  .graph-legend {{ position: absolute; bottom: 16px; left: 16px; background: rgba(19, 28, 46, 0.9); border: 1px solid var(--border); padding: 10px 14px; border-radius: 8px; font-size: 12px; display: flex; gap: 14px; backdrop-filter: blur(4px); }}
  .legend-item {{ display: flex; align-items: center; gap: 6px; }}
  .legend-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}

  /* Toast Notification */
  #toast {{ visibility: hidden; min-width: 250px; background-color: #10b981; color: #fff; text-align: center; border-radius: 8px; padding: 12px 18px; position: fixed; z-index: 9999; right: 30px; bottom: 30px; font-size: 13.5px; font-weight: 700; box-shadow: 0 4px 16px rgba(0,0,0,0.4); }}
  #toast.show {{ visibility: visible; animation: fadein 0.3s, fadeout 0.3s 2.5s; }}
  @keyframes fadein {{ from {{ bottom: 0; opacity: 0; }} to {{ bottom: 30px; opacity: 1; }} }}
  @keyframes fadeout {{ from {{ bottom: 30px; opacity: 1; }} to {{ bottom: 0; opacity: 0; }} }}
</style>
</head>
<body>

<header>
  <div class="title-area">
    <h1><span class="radar">📡</span> Sayari Compliance Signal Radar & Living Brain</h1>
    <p class="subtitle">Continuous public discussion mining, bottom-up practitioner opinions, and 4-format LinkedIn idea bank</p>
  </div>
  <div class="header-actions">
    <button id="pwaInstallBtn" style="display:none; background:#38bdf8; color:#090d16; border:none; padding:9px 15px; border-radius:8px; font-weight:700; cursor:pointer; font-size:13px; transition:all 0.2s;" onclick="installPWA()">
      📱 Install App
    </button>
    <button class="btn-dump-all" onclick="dumpEntireBrainToClipboard()">
      📋 Dump Entire Brain for Claude (No Links, Trace IDs)
    </button>
    <div class="sweep-badge">
      <div>Last Sweep: <span class="sweep-time">{sweep_time}</span></div>
      <div style="font-size:11px; color:#34d399;">● {len(raw_items)} Signals Active | {len(pipeline_runs)} Runs Logged</div>
    </div>
  </div>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('living_brain')">🧠 Living Brain: Key Opinions & Angles</button>
  <button class="tab-btn" onclick="switchTab('run_logs')">📜 Pull History & Run Logs ({len(pipeline_runs)})</button>
  <button class="tab-btn" onclick="switchTab('lexicon')">🍺 "The Beer Test" Lexicon ({len(glossary)})</button>
  <button class="tab-btn" onclick="switchTab('raw')">🔍 Raw Signals Stream ({len(raw_items)} Passed)</button>
  <button class="tab-btn" onclick="switchTab('noise')">🛡️ Noise Shield ({len(dropped_items)} Blocked)</button>
  <button class="tab-btn" onclick="switchTab('graph')">🕸️ Interactive Knowledge Graph</button>
</div>

<div class="filters" id="filterBar">
  <div class="filter-group">
    <label>Format Filter</label>
    <select id="filterFormat" onchange="renderCurrentTab()">
      <option value="all">All 4 Core Formats</option>
      <option value="Pain mirror">Pain mirror (35%)</option>
      <option value="Product as relief">Product as relief (25%)</option>
      <option value="The receipts">The receipts (20%)</option>
      <option value="Headline to what it means for you">Headline / Newsjack (20%)</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Min Frustration Intensity</label>
    <select id="filterIntensity" onchange="renderCurrentTab()">
      <option value="1">1+ (All Signals)</option>
      <option value="2">2+ (Moderate Frustration)</option>
      <option value="3">3+ (High Frustration & Fear)</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Search Community Term / Topic</label>
    <input type="text" id="filterSearch" placeholder="e.g. name matching, swivel chair, ubo, backlog, webull" oninput="renderCurrentTab()">
  </div>
</div>

<!-- Tab 1: Combined Living Brain & Key Opinions -->
<div id="livingBrainContainer" class="grid"></div>

<!-- Tab 2: Run History & Pull Logs -->
<div id="runLogsContainer" style="display:none;" class="table-container">
  <table class="table-view">
    <thead>
      <tr>
        <th style="width: 130px;">Timestamp (UTC)</th>
        <th style="width: 140px;">Trigger</th>
        <th style="width: 25%;">Sources Swept</th>
        <th style="width: 20%;">Time Range</th>
        <th style="width: 100px;">Counts</th>
        <th style="width: 30%;">Pull Learnings & Summary</th>
      </tr>
    </thead>
    <tbody id="runLogsTbody"></tbody>
  </table>
</div>

<!-- Tab 3: Beer Test Lexicon -->
<div id="lexiconContainer" style="display:none;" class="table-container">
  <table class="table-view">
    <thead>
      <tr>
        <th style="width: 220px;">Term (What Practitioners Say)</th>
        <th style="width: 180px;">Category</th>
        <th style="width: 90px;">Frequency</th>
        <th>Real Practitioner Context / Usage Rule</th>
      </tr>
    </thead>
    <tbody id="lexiconTbody"></tbody>
  </table>
</div>

<!-- Tab 4: Raw Signals Stream -->
<div id="rawContainer" style="display:none;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; background:var(--card); padding:10px 14px; border-radius:8px; border:1px solid var(--border);">
    <span style="font-size:13px; color:var(--muted);">Showing verified compliance signals with clickable original sources and expandable full text.</span>
    <button class="copy-btn" onclick="copyAllRawSignalsToClipboard()">
      📋 Copy All Raw Signals (Formatted for Claude)
    </button>
  </div>
  <div class="table-container">
    <table class="table-view">
      <thead>
        <tr>
          <th style="width: 65px;">Trace ID</th>
          <th style="width: 110px;">Source</th>
          <th style="width: 20%;">Original Title & URL</th>
          <th style="width: 22%;">Summary Takeaway</th>
          <th style="width: 30%;">Practitioner Excerpt (Expandable)</th>
          <th style="width: 110px;">Theme</th>
          <th style="width: 65px;">Action</th>
        </tr>
      </thead>
      <tbody id="rawTbody"></tbody>
    </table>
  </div>
</div>

<!-- Tab 5: Noise Shield (Blocked) -->
<div id="noiseContainer" style="display:none;" class="table-container">
  <div style="padding:12px 16px; background:#0c1424; border-bottom:1px solid var(--border); font-size:13px; color:var(--muted);">
    🛡️ <strong>Noise Shield Active:</strong> Items filtered out because they were vendor product advertisements without practitioner debate, or generic career questions. Click any title to inspect the original post.
  </div>
  <table class="table-view">
    <thead>
      <tr>
        <th style="width: 130px;">Source</th>
        <th style="width: 35%;">Original Post Title & Link</th>
        <th style="width: 25%;">Reason Blocked</th>
        <th>Excerpt Preview</th>
      </tr>
    </thead>
    <tbody id="noiseTbody"></tbody>
  </table>
</div>

<!-- Tab 6: Knowledge Graph -->
<div id="graphContainer" style="display:none;">
  <div style="padding:12px 18px; border-bottom:1px solid var(--border); background:#0c1424; display:flex; justify-content:space-between; align-items:center;">
    <div>
      <strong style="color:#fff; font-size:14px;">🕸️ Compliance Intelligence Knowledge Graph</strong>
      <span style="color:var(--muted); font-size:12px; margin-left:10px;">Drag nodes to explore. Click/hover to highlight connected pains, evasion tactics, regulators, and Sayari proof points.</span>
    </div>
    <button class="copy-btn" style="padding:4px 8px; font-size:11px;" onclick="resetGraph()">↺ Reset Graph</button>
  </div>
  <canvas id="graphCanvas"></canvas>
  <div class="graph-legend">
    <div class="legend-item"><span class="legend-dot" style="background:#f87171;"></span> 🔴 Practitioner Pains</div>
    <div class="legend-item"><span class="legend-dot" style="background:#fbbf24;"></span> 🟡 Evasion & Hidden Risk</div>
    <div class="legend-item"><span class="legend-dot" style="background:#818cf8;"></span> 🟣 Regulators & Laws</div>
    <div class="legend-item"><span class="legend-dot" style="background:#34d399;"></span> 🟢 Sayari Proof Anchors</div>
  </div>
</div>

<div id="toast">✅ Text Copied to Clipboard!</div>

<script>
const IDEAS = {ideas_json};
const RAW_ITEMS = {items_json};
const GLOSSARY = {glossary_json};
const DROPPED_ITEMS = {dropped_json};
const PIPELINE_RUNS = {runs_json};
const CLAUDE_DUMP = {claude_dump_json};

let currentTab = 'living_brain';

function showToast(msg) {{
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.className = 'show';
  setTimeout(() => {{ toast.className = toast.className.replace('show', ''); }}, 2800);
}}

function copyTextToClipboard(text, successMsg) {{
  if (navigator.clipboard && window.isSecureContext) {{
    navigator.clipboard.writeText(text).then(() => {{
      showToast(successMsg);
    }}).catch(() => {{
      fallbackCopy(text, successMsg);
    }});
  }} else {{
    fallbackCopy(text, successMsg);
  }}
}}

function fallbackCopy(text, successMsg) {{
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-999999px';
  ta.style.top = '-999999px';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try {{
    document.execCommand('copy');
    showToast(successMsg);
  }} catch (err) {{
    alert('Copy failed. Please manually copy from reports/claude_dump.md');
  }}
  document.body.removeChild(ta);
}}

function dumpEntireBrainToClipboard() {{
  copyTextToClipboard(CLAUDE_DUMP, '📋 Full Brain Copied (No links, Sourced with IDs)! Paste into Claude.');
}}

function copyAllRawSignalsToClipboard() {{
  var lines = [
    "# SAYARI RAW COMPLIANCE SIGNALS & PRACTITIONER DISCUSSIONS",
    "# Formatted for Claude analysis with Trace IDs and Context",
    ""
  ];
  RAW_ITEMS.forEach(function(it, idx) {{
    var src = it.source.replace('pasted:', '').replace('rss:', '').replace('manual:', '');
    lines.push("[Trace ID #" + (idx + 1) + "]");
    lines.push("- Source: " + src);
    lines.push("- Title: " + it.title);
    if (it.url) lines.push("- Original URL: " + it.url);
    lines.push("- Summary: " + (it.paraphrase || it.title));
    lines.push("- Practitioner Excerpt: \\"" + it.short_excerpt + "\\"");
    lines.push("- Theme: " + (it.theme || 'General') + " | Emotion: " + (it.emotion || 'frustration') + " (" + (it.intensity || 1) + "/5)");
    lines.push("");
  }});
  copyTextToClipboard(lines.join('\\n'), '📋 Copied All Raw Signals for Claude!');
}}

function toggleExpand(id) {{
  const el = document.getElementById(id);
  const btn = document.getElementById(id + '-btn');
  if (el) {{
    if (el.classList.contains('expanded')) {{
      el.classList.remove('expanded');
      if (btn) btn.innerText = '[+] Expand full text';
    }} else {{
      el.classList.add('expanded');
      if (btn) btn.innerText = '[-] Collapse';
    }}
  }}
}}

function formatEvidenceHtml(sources) {{
  if (!sources || !sources.length) return "<div style='color:var(--muted); font-size:11px;'>No direct quotes attached.</div>";
  return sources.map(function(ev, i) {{
    var cleanSrc = ev.url ? ev.url.replace('https://www.reddit.com/r/', 'r/').replace('https://', '').split('/')[0] : 'Community Source';
    var linkHtml = ev.url ? '<a href="' + ev.url + '" target="_blank" rel="noopener" class="source-link">' + cleanSrc + ' ↗</a>' : cleanSrc;
    return '<div class="evidence-item">• ' + linkHtml + ' (' + ev.upvotes + ' upvotes): <em>\\"' + (ev.paraphrase || '') + '\\"</em></div>';
  }}).join('');
}}

function copyIdeaPrompt(idx) {{
  const idea = IDEAS[idx];
  if (!idea) return;

  var evidenceLines = (idea.evidence_sources || []).map(function(ev, i) {{
    var cleanSrc = ev.url ? ev.url.replace('https://www.reddit.com/r/', 'r/').replace('https://', '').split('/')[0] : 'Source';
    return "  * [Source: " + cleanSrc + " | " + ev.upvotes + " upvotes]: \\"" + ev.paraphrase + "\\"";
  }}).join('\\n');

  const prompt = `I am drafting a LinkedIn post for Sayari targeting compliance officers and financial crime / sanctions analysts.

Format: ${{idea.format}}
Pillar: ${{idea.pillar}}
Post Concept: ${{idea.title}}
The Hook: "${{idea.hook}}"
Visual Metaphor: ${{idea.suggested_visual}}

Verified Evidence & Real Quotes:
` + evidenceLines + `

Voice Guidelines:
- Validating, unflinching, human, a little funny, proof-backed.
- Zero vendor buzzwords (no "judgment infrastructure", "zero-resistance", or "synergies"). Must pass the "Beer Test."
- Meet them mid-drown, name the Frankenstack as the real enemy, and show the shift to evidence-based records.

Please write 2 variations of this LinkedIn post ready to publish.`;

  copyTextToClipboard(prompt, `📋 Copied Idea #${{idx+1}} Prompt for Claude!`);
}}

function copyOpinionPrompt(opinionTitle, opinionDesc, angles) {{
  var angleLines = angles.map(function(a, idx) {{
    return "Angle #" + (idx + 1) + " (" + a.format + "): \\"" + a.title + "\\"\\nHook: \\"" + a.hook + "\\"\\nVisual: " + a.suggested_visual;
  }}).join('\\n\\n');

  const prompt = `I am drafting LinkedIn content for Sayari based on this core practitioner opinion:

Key Opinion / Tension: ` + opinionTitle + `
Practitioner Reality: ` + opinionDesc + `

Actionable Post Angles:
` + angleLines + `

Voice Guidelines:
- Validating, unflinching, human, a little funny. Pass the "Beer Test".
- Zero vendor buzzwords.
- Use Sayari proof anchors (e.g., 72% unlisted risk in nested ownership, 1.2M records screened real-time vs 48h competitor).

Please write 2 publish-ready LinkedIn posts for this opinion.`;

  copyTextToClipboard(prompt, "📋 Copied Key Opinion Package for Claude!");
}}

function getBadgeClass(fmt) {{
  if (fmt.includes('Pain')) return 'badge-pain';
  if (fmt.includes('relief')) return 'badge-relief';
  if (fmt.includes('receipts')) return 'badge-receipts';
  return 'badge-news';
}}

function switchTab(tab) {{
  currentTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  ['livingBrainContainer', 'runLogsContainer', 'lexiconContainer', 'rawContainer', 'noiseContainer', 'graphContainer'].forEach(id => {{
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  }});

  const filterBar = document.getElementById('filterBar');
  filterBar.style.display = (tab === 'living_brain' || tab === 'raw') ? 'flex' : 'none';

  if (tab === 'living_brain') {{
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.getElementById('livingBrainContainer').style.display = 'grid';
  }} else if (tab === 'run_logs') {{
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
    document.getElementById('runLogsContainer').style.display = 'block';
  }} else if (tab === 'lexicon') {{
    document.querySelectorAll('.tab-btn')[2].classList.add('active');
    document.getElementById('lexiconContainer').style.display = 'block';
  }} else if (tab === 'raw') {{
    document.querySelectorAll('.tab-btn')[3].classList.add('active');
    document.getElementById('rawContainer').style.display = 'block';
  }} else if (tab === 'noise') {{
    document.querySelectorAll('.tab-btn')[4].classList.add('active');
    document.getElementById('noiseContainer').style.display = 'block';
  }} else if (tab === 'graph') {{
    document.querySelectorAll('.tab-btn')[5].classList.add('active');
    document.getElementById('graphContainer').style.display = 'block';
    initGraph();
  }}
  renderCurrentTab();
}}

// 1. Render Living Brain (Key Opinions Consolidated with Ideas)
function renderLivingBrain() {{
  const fmt = document.getElementById('filterFormat').value;
  const minInt = parseFloat(document.getElementById('filterIntensity').value);
  const q = document.getElementById('filterSearch').value.toLowerCase().trim();

  // Group ideas bottom-up into Key Practitioner Opinions
  const OPINION_MAP = [
    {{
      title: "Vendor Questionnaires Are Compliance Theater",
      tension: "Self-disclosure forms are useless; illicit networks never check 'Yes' on SDN ties; 72% of flagged risk is hidden 3+ layers deep in nested ownership.",
      proof: "No. 3 Global Telecom: 72% of high-risk entities appeared clean on watchlists, hidden in nested corporate structures.",
      match: i => i.title.toLowerCase().includes('watchlist') || i.title.toLowerCase().includes('72%') || i.title.toLowerCase().includes('questionnaire') || i.title.toLowerCase().includes('ubo') || i.title.toLowerCase().includes('apartment')
    }},
    {{
      title: "Alert Fatigue is a Tool Failure, Not an Analyst Failure",
      tension: "Industry false-positive rates of 90-95% are caused by crude keyword tools, turning L1 review into soul-crushing whack-a-mole.",
      proof: "Fortune 50 Energy Supermajor: 1.2M records screened in real time vs 24-48 hours on legacy platform.",
      match: i => i.title.toLowerCase().includes('alert') || i.title.toLowerCase().includes('queue') || i.title.toLowerCase().includes('name') || i.title.toLowerCase().includes('purgatory')
    }},
    {{
      title: "The Swivel Chair Trap: Fragmented Tools Paralyze Investigation",
      tension: "Analysts waste 45 minutes per vendor manually copy-pasting numbers across 6-8 disconnected vendor tabs and spreadsheets.",
      proof: "Fortune 50 Energy: 75+ disparate data feeds collapsed into a single unified registry query.",
      match: i => i.title.toLowerCase().includes('frankenstack') || i.title.toLowerCase().includes('tabs') || i.title.toLowerCase().includes('75+') || i.title.toLowerCase().includes('breakup')
    }},
    {{
      title: "A Vendor Risk Score is Not an Audit Defense",
      tension: "Regulators reject automated black-box risk scores; examiners demand primary registry documents and defensible provenance.",
      proof: "Recent regulatory enforcement doctrine: an algorithm score cannot substitute for verified registry audit trails.",
      match: i => i.title.toLowerCase().includes('score') || i.title.toLowerCase().includes('regulator') || i.title.toLowerCase().includes('audit') || i.title.toLowerCase().includes('settle') || i.title.toLowerCase().includes('defense')
    }},
    {{
      title: "The Sub-Tier Supply Chain Blind Spot (Beyond Tier 1)",
      tension: "Tier-1 suppliers pass questionnaires easily; UFLPA detentions and export bans strike Tier-2 and Tier-3 raw component hubs.",
      proof: "Top-5 Global Tech Company: Chose Sayari over supply-chain incumbent specifically for sub-tier component mapping.",
      match: i => i.title.toLowerCase().includes('supply') || i.title.toLowerCase().includes('tier') || i.title.toLowerCase().includes('tech') || i.title.toLowerCase().includes('labor')
    }}
  ];

  const html = OPINION_MAP.map((op, opIdx) => {{
    let matchingIdeas = IDEAS.filter(op.match);
    if (!matchingIdeas.length) {{
      matchingIdeas = IDEAS.slice(opIdx * 3, opIdx * 3 + 3);
    }}

    // Apply filters
    const filteredAngles = matchingIdeas.filter(idea => {{
      const matchFmt = (fmt === 'all' || idea.format === fmt);
      const matchInt = (idea.avg_intensity >= minInt);
      const matchQ = (!q || idea.title.toLowerCase().includes(q) || idea.hook.toLowerCase().includes(q) || op.title.toLowerCase().includes(q));
      return matchFmt && matchInt && matchQ;
    }});

    if (!filteredAngles.length && (fmt !== 'all' || q)) return '';

    const anglesHtml = filteredAngles.map((idea, aIdx) => `
      <div style="background:#090f1d; border:1px solid var(--border); border-radius:8px; padding:12px; margin-top:10px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <span class="badge ${{getBadgeClass(idea.format)}}">${{idea.format}}</span>
          <span style="font-size:11px; color:var(--muted); font-weight:700;">Score: ${{idea.rank_score}}</span>
        </div>
        <div style="font-weight:700; color:#fff; font-size:14px; margin-bottom:4px;">${{idea.title}}</div>
        <div class="hook-box" style="margin:6px 0; font-size:12.5px;">"${{idea.hook}}"</div>
        <div style="font-size:11.5px; color:var(--muted); margin-bottom:8px;">
          <strong>Visual:</strong> ${{idea.suggested_visual}}
        </div>
        <button class="copy-btn" style="padding:4px 9px; font-size:11px;" onclick="copyIdeaPrompt(${{IDEAS.indexOf(idea)}})">
          📋 Copy Angle Prompt for Claude
        </button>
      </div>
    `).join('');

    return `
      <div class="card" style="border-top:3px solid var(--accent);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
          <div>
            <span class="pill badge-news" style="margin-bottom:6px;">Key Practitioner Stance #${{opIdx+1}}</span>
            <div class="idea-title" style="font-size:17px; color:#fff;">${{op.title}}</div>
          </div>
        </div>
        
        <p style="font-size:13px; color:#cbd5e1; line-height:1.45;">${{op.tension}}</p>
        
        <div style="background:#080d1a; padding:10px 12px; border-radius:6px; font-size:12px; border-left:3px solid #34d399;">
          <strong style="color:#34d399;">Sayari Proof Anchor:</strong> ${{op.proof}}
        </div>

        <div style="margin-top:4px;">
          <strong style="font-size:12px; color:var(--muted); text-transform:uppercase;">Actionable Content Angles (${{filteredAngles.length}} available):</strong>
          ${{anglesHtml || '<p style="color:var(--muted); font-size:12px; padding:8px 0;">No angles match your current format filter.</p>'}}
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px; padding-top:10px; border-top:1px solid var(--border);">
          <span style="font-size:11px; color:var(--muted);">Grounded in public Reddit/RSS chatter</span>
          <button class="copy-btn" onclick="copyOpinionPrompt('${{op.title}}', '${{op.tension}}', ${{JSON.stringify(filteredAngles)}})">
            📋 Copy Complete Opinion Package
          </button>
        </div>
      </div>
    `;
  }}).join('');

  document.getElementById('livingBrainContainer').innerHTML = html || '<p style="padding:20px; color:var(--muted)">No themes matched your search criteria.</p>';
}}

// 2. Render Run Logs
function renderRunLogs() {{
  const html = PIPELINE_RUNS.map((run, idx) => `
    <tr>
      <td><strong>${{run.timestamp}}</strong></td>
      <td><span class="pill ${{run.trigger_type.includes('Cloud') ? 'badge-cloud' : 'badge-local'}}">${{run.trigger_type}}</span></td>
      <td>${{run.sources_swept}}</td>
      <td><span style="color:#94a3b8; font-size:12px;">${{run.time_ranges}}</span></td>
      <td>
        <div style="font-size:12px;">
          <strong style="color:#38bdf8;">${{run.raw_collected_count}}</strong> gathered<br>
          <span style="color:#34d399;">${{run.passed_filters_count}} passed</span><br>
          <span style="color:#f87171;">${{run.dropped_noise_count}} noise</span>
        </div>
      </td>
      <td style="font-size:12.5px; color:#cbd5e1; line-height:1.4;">${{run.summary_learnings}}</td>
    </tr>
  `).join('');
  document.getElementById('runLogsTbody').innerHTML = html || '<tr><td colspan="6" style="padding:20px; text-align:center; color:var(--muted);">No run logs recorded yet.</td></tr>';
}}

// 3. Render Beer Test Lexicon (Fixed bug: string/boolean safe)
function renderLexicon() {{
  const html = GLOSSARY.map(g => {{
    const isVendor = String(g.is_vendor_marketing_only).includes('YES') || g.is_vendor_marketing_only === 1 || String(g.is_vendor_marketing_only) === '1';
    return `
      <tr>
        <td><strong style="color:#fff; font-size:13.5px;">${{g.term}}</strong></td>
        <td><span class="pill ${{isVendor ? 'badge-pain' : 'badge-relief'}}">${{isVendor ? 'Banned Vendor Fluff' : 'Real Practitioner Slang'}}</span></td>
        <td><strong style="color:var(--accent);">${{g.frequency}}</strong></td>
        <td style="color:#cbd5e1; font-style:italic;">${{g.example_context || 'Practitioner term mined from compliance community discussions.'}}</td>
      </tr>
    `;
  }}).join('');
  document.getElementById('lexiconTbody').innerHTML = html;
}}

// 4. Render Raw Streams (With Summary, Clickable Links, Expand Toggle, Decreased Width)
function renderRawStream() {{
  const minInt = parseFloat(document.getElementById('filterIntensity').value);
  const q = document.getElementById('filterSearch').value.toLowerCase().trim();

  const filtered = RAW_ITEMS.filter(it => {{
    const matchInt = ((it.intensity || 1) >= minInt);
    const matchQ = (!q || it.title.toLowerCase().includes(q) || (it.short_excerpt && it.short_excerpt.toLowerCase().includes(q)) || (it.paraphrase && it.paraphrase.toLowerCase().includes(q)));
    return matchInt && matchQ;
  }});

  const html = filtered.map((it, idx) => {{
    const linkHtml = it.url ? `<a href="${{it.url}}" target="_blank" rel="noopener" class="source-link">${{it.title}} ↗</a>` : `<strong>${{it.title}}</strong>`;
    const cleanSrc = it.source.replace('pasted:', '').replace('rss:', '').replace('manual:', '');
    const collapseId = 'excerpt-' + idx;

    return `
      <tr>
        <td><span class="trace-id">#${{idx+1}}</span></td>
        <td><span style="font-size:11.5px; color:var(--muted); font-weight:600;">${{cleanSrc}}</span></td>
        <td>
          <div style="font-size:13px; font-weight:700; margin-bottom:4px;">${{linkHtml}}</div>
          <span style="font-size:11px; color:#64748b;">${{it.date || 'Recent'}}</span>
        </td>
        <td>
          <div style="font-size:12.5px; color:#cbd5e1; line-height:1.4;">${{it.paraphrase || it.title}}</div>
        </td>
        <td>
          <div id="${{collapseId}}" class="collapsible-text">
            <span style="font-style:italic; color:#94a3b8; font-size:12px;">"${{it.short_excerpt}}"</span>
          </div>
          <button id="${{collapseId}}-btn" class="expand-btn" onclick="toggleExpand('${{collapseId}}')">[+] Expand full text</button>
        </td>
        <td>
          <span style="color:var(--accent); font-weight:600; font-size:11.5px;">${{it.theme || 'General'}}</span><br>
          <span style="color:var(--muted); font-size:11px;">Intensity: ${{it.intensity || 1}}/5</span>
        </td>
        <td>
          <button class="copy-btn" style="padding:4px 8px; font-size:11px; margin:0;" onclick="copySignalPrompt(${{idx}})">
            📋 Copy
          </button>
        </td>
      </tr>
    `;
  }}).join('');

  document.getElementById('rawTbody').innerHTML = html || '<tr><td colspan="7" style="padding:20px; text-align:center; color:var(--muted);">No signals match your filter.</td></tr>';
}}

// 5. Render Noise Shield (With Clickable Links)
function renderNoise() {{
  const html = DROPPED_ITEMS.map((d, idx) => {{
    const linkHtml = d.url ? `<a href="${{d.url}}" target="_blank" rel="noopener" class="source-link">${{d.title}} ↗</a>` : `<strong>${{d.title}}</strong>`;
    return `
      <tr>
        <td><span style="font-size:12px; color:var(--muted);">${{d.source || 'Public Source'}}</span></td>
        <td>${{linkHtml}}</td>
        <td><span style="color:#f87171; font-weight:600; font-size:12px;">${{d.drop_reason || 'Vendor Promotion / No Frustration'}}</span></td>
        <td style="color:#64748b; font-size:11.5px; font-style:italic;">${{d.short_excerpt || 'No excerpt available'}}</td>
      </tr>
    `;
  }}).join('');
  document.getElementById('noiseTbody').innerHTML = html;
}}

function copySignalPrompt(idx) {{
  const it = RAW_ITEMS[idx];
  if (!it) return;

  const cleanSrc = it.source.replace('pasted:', '').replace('rss:', '').replace('manual:', '');
  const text = `[Trace ID #${{idx + 1}} | Source: ${{cleanSrc}}]
Title: ${{it.title}}
URL: ${{it.url || 'N/A'}}
Summary: ${{it.paraphrase || it.title}}
Practitioner Excerpt: "${{it.short_excerpt}}"
Theme: ${{it.theme || 'General'}} | Emotion: ${{it.emotion || 'frustration'}} (${{it.intensity || 1}}/5)`;

  copyTextToClipboard(text, `📋 Copied Trace ID #${{idx + 1}}!`);
}}

function renderCurrentTab() {{
  if (currentTab === 'living_brain') renderLivingBrain();
  else if (currentTab === 'run_logs') renderRunLogs();
  else if (currentTab === 'lexicon') renderLexicon();
  else if (currentTab === 'raw') renderRawStream();
  else if (currentTab === 'noise') renderNoise();
}}

// 6. Interactive Knowledge Graph Implementation
let graphNodes = [];
let graphEdges = [];
let animFrameId = null;
let hoveredNode = null;
let draggedNode = null;

function initGraph() {{
  const canvas = document.getElementById('graphCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  // Set internal resolution
  canvas.width = canvas.parentElement.clientWidth || 900;
  canvas.height = 620;

  const W = canvas.width;
  const H = canvas.height;

  graphNodes = [
    // Pains (Red)
    {{ id: 'p1', label: 'Alert Fatigue & Backlog', category: 'pain', color: '#f87171', x: W * 0.25, y: H * 0.25, vx: 0, vy: 0, r: 24, desc: '90-95% false positives swamping L1 analyst review.' }},
    {{ id: 'p2', label: 'Swivel Chair (7+ Logins)', category: 'pain', color: '#f87171', x: W * 0.18, y: H * 0.55, vx: 0, vy: 0, r: 22, desc: '45 mins lost copy-pasting numbers across disconnected tabs.' }},
    {{ id: 'p3', label: 'Name Match Purgatory', category: 'pain', color: '#f87171', x: W * 0.32, y: H * 0.40, vx: 0, vy: 0, r: 22, desc: 'Common surname false hits vs evasion spelling tricks.' }},
    {{ id: 'p4', label: 'Audit Dread & Exam Panic', category: 'pain', color: '#f87171', x: W * 0.28, y: H * 0.75, vx: 0, vy: 0, r: 22, desc: 'Regulators rejecting black-box automated risk scores.' }},

    // Evasion & Risk (Amber)
    {{ id: 'e1', label: 'Nested UBO (3+ Layers Deep)', category: 'evasion', color: '#fbbf24', x: W * 0.52, y: H * 0.22, vx: 0, vy: 0, r: 24, desc: 'Clean tier-1 supplier hiding sanctioned oligarch across offshore hops.' }},
    {{ id: 'e2', label: '147 Shells at 1 Flat', category: 'evasion', color: '#fbbf24', x: W * 0.48, y: H * 0.48, vx: 0, vy: 0, r: 22, desc: 'Residential addresses in Belize/Cyprus routing $42M dual-use tech.' }},
    {{ id: 'e3', label: 'Transshipment Hubs', category: 'evasion', color: '#fbbf24', x: W * 0.55, y: H * 0.72, vx: 0, vy: 0, r: 22, desc: 'Sub-tier component routes skirting export sanctions.' }},

    // Regulators (Purple)
    {{ id: 'r1', label: 'OFAC 50% Rule', category: 'reg', color: '#818cf8', x: W * 0.40, y: H * 0.15, vx: 0, vy: 0, r: 20, desc: 'Aggregate ownership thresholds triggering automatic sanctions.' }},
    {{ id: 'r2', label: 'UFLPA Forced Labor', category: 'reg', color: '#818cf8', x: W * 0.62, y: H * 0.85, vx: 0, vy: 0, r: 20, desc: 'Sub-tier polysilicon and component detentions at customs.' }},
    {{ id: 'r3', label: 'FinCEN Whistleblower', category: 'reg', color: '#818cf8', x: W * 0.38, y: H * 0.90, vx: 0, vy: 0, r: 20, desc: 'Spike in whistleblower reports triggering immediate audits.' }},
    {{ id: 'r4', label: 'DOJ Penalties (e.g. Webull)', category: 'reg', color: '#818cf8', x: W * 0.15, y: H * 0.82, vx: 0, vy: 0, r: 20, desc: 'Multi-million dollar settlements for inadequate AML scrutiny.' }},

    // Sayari Proof Anchors (Green)
    {{ id: 's1', label: '72% Unlisted Risk Unmasked', category: 'sayari', color: '#34d399', x: W * 0.78, y: H * 0.25, vx: 0, vy: 0, r: 25, desc: 'Global telecom case: 72% of high-risk partners were on zero watchlists.' }},
    {{ id: 's2', label: '1.2M Records in Real Time', category: 'sayari', color: '#34d399', x: W * 0.75, y: H * 0.50, vx: 0, vy: 0, r: 25, desc: 'Energy supermajor: instant screening vs 48-hour competitor lag.' }},
    {{ id: 's3', label: '75+ Data Feeds Collapsed', category: 'sayari', color: '#34d399', x: W * 0.80, y: H * 0.72, vx: 0, vy: 0, r: 25, desc: 'Retired homegrown frankenstack into a single graph query.' }},
    {{ id: 's4', label: 'Sub-Tier Tech Mapping', category: 'sayari', color: '#34d399', x: W * 0.70, y: H * 0.88, vx: 0, vy: 0, r: 24, desc: 'Top-5 tech giant chose Sayari over incumbent for Tier-2/Tier-3 traceability.' }}
  ];

  graphEdges = [
    {{ from: 'p1', to: 'p3', label: 'causes' }},
    {{ from: 'p2', to: 'p1', label: 'amplifies' }},
    {{ from: 'p3', to: 'e1', label: 'evaded by' }},
    {{ from: 'e1', to: 'r1', label: 'triggers' }},
    {{ from: 'e2', to: 'p4', label: 'risks' }},
    {{ from: 'e3', to: 'r2', label: 'violates' }},
    {{ from: 'r4', to: 'p4', label: 'escalates' }},
    {{ from: 'r3', to: 'p4', label: 'triggers' }},
    
    // Sayari Connections
    {{ from: 'e1', to: 's1', label: 'unmasked by' }},
    {{ from: 'p1', to: 's2', label: 'cured by' }},
    {{ from: 'p2', to: 's3', label: 'eliminated by' }},
    {{ from: 'p4', to: 's2', label: 'defended by' }},
    {{ from: 'r2', to: 's4', label: 'mapped by' }},
    {{ from: 'e3', to: 's4', label: 'exposed by' }}
  ];

  setupGraphInteractivity(canvas);
  animateGraph(canvas, ctx);
}}

function setupGraphInteractivity(canvas) {{
  canvas.onmousedown = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    draggedNode = graphNodes.find(n => Math.hypot(n.x - mx, n.y - my) < n.r);
  }};

  canvas.onmousemove = (e) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    if (draggedNode) {{
      draggedNode.x = mx;
      draggedNode.y = my;
    }} else {{
      hoveredNode = graphNodes.find(n => Math.hypot(n.x - mx, n.y - my) < n.r);
    }}
  }};

  window.onmouseup = () => {{
    draggedNode = null;
  }};
}}

function resetGraph() {{
  initGraph();
}}

function animateGraph(canvas, ctx) {{
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw Edges
  graphEdges.forEach(e => {{
    const n1 = graphNodes.find(n => n.id === e.from);
    const n2 = graphNodes.find(n => n.id === e.to);
    if (!n1 || !n2) return;

    const isHighlight = hoveredNode && (hoveredNode.id === n1.id || hoveredNode.id === n2.id);

    ctx.beginPath();
    ctx.moveTo(n1.x, n1.y);
    ctx.lineTo(n2.x, n2.y);
    ctx.strokeStyle = isHighlight ? '#38bdf8' : 'rgba(51, 65, 85, 0.4)';
    ctx.lineWidth = isHighlight ? 2.5 : 1.2;
    ctx.stroke();

    // Draw relation label
    if (isHighlight) {{
      const mx = (n1.x + n2.x) / 2;
      const my = (n1.y + n2.y) / 2;
      ctx.fillStyle = '#cbd5e1';
      ctx.font = '10px -apple-system, sans-serif';
      ctx.fillText(e.label, mx, my);
    }}
  }});

  // Draw Nodes
  graphNodes.forEach(n => {{
    const isHovered = hoveredNode && hoveredNode.id === n.id;
    const isNeighbor = hoveredNode && graphEdges.some(e => (e.from === hoveredNode.id && e.to === n.id) || (e.to === hoveredNode.id && e.from === n.id));

    ctx.beginPath();
    ctx.arc(n.x, n.y, isHovered ? n.r + 4 : n.r, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.shadowBlur = isHovered ? 16 : 6;
    ctx.shadowColor = n.color;
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.strokeStyle = '#fff';
    ctx.lineWidth = isHovered ? 2 : 1;
    ctx.stroke();

    // Node text
    ctx.fillStyle = '#fff';
    ctx.font = '11px -apple-system, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(n.label, n.x, n.y + n.r + 14);

    // Tooltip for hovered node
    if (isHovered) {{
      ctx.fillStyle = 'rgba(15, 23, 42, 0.95)';
      ctx.strokeStyle = n.color;
      ctx.lineWidth = 1;
      const tw = ctx.measureText(n.desc).width + 24;
      const tx = Math.min(canvas.width - tw - 10, Math.max(10, n.x - tw / 2));
      const ty = n.y - n.r - 35;
      ctx.fillRect(tx, ty, tw, 26);
      ctx.strokeRect(tx, ty, tw, 26);
      ctx.fillStyle = '#f8fafc';
      ctx.textAlign = 'left';
      ctx.fillText(n.desc, tx + 12, ty + 17);
    }}
  }});

  if (currentTab === 'graph') {{
    animFrameId = requestAnimationFrame(() => animateGraph(canvas, ctx));
  }}
}}

// PWA Service Worker & Install Handler
let deferredPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {{
  e.preventDefault();
  deferredPrompt = e;
  const btn = document.getElementById('pwaInstallBtn');
  if (btn) btn.style.display = 'inline-flex';
}});

function installPWA() {{
  if (deferredPrompt) {{
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(() => {{
      deferredPrompt = null;
      const btn = document.getElementById('pwaInstallBtn');
      if (btn) btn.style.display = 'none';
    }});
  }}
}}

if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.addEventListener('controllerchange', () => {{
    window.location.reload();
  }});

  window.addEventListener('load', () => {{
    navigator.serviceWorker.register('./sw.js?t=' + Date.now()).then(reg => {{
      reg.update();
      reg.onupdatefound = () => {{
        const installingWorker = reg.installing;
        if (installingWorker) {{
          installingWorker.onstatechange = () => {{
            if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {{
              window.location.reload();
            }}
          }};
        }}
      }};
    }}).catch(err => {{
      console.log('SW registration note:', err);
    }});
  }});
}}

renderCurrentTab();
</script>
</body>
</html>
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_all_outputs(conn: sqlite3.Connection, ideas: List[Dict[str, Any]], glossary: List[Dict[str, Any]]):
    """Exports all required files: CSVs, Markdown, logs, and interactive viewer."""
    import time
    from src.pwa_assets import build_all_pwa_assets
    from src.db import get_recent_pipeline_runs

    export_raw_items_csv(conn, "raw_items.csv")
    export_ideas_csv(ideas, "ideas.csv")
    export_ideas_markdown(ideas, "ideas.md")
    export_glossary_csv(glossary, "glossary.csv")
    export_blocked_sources_md(conn, "blocked_sources.md")
    
    # Fetch pipeline runs
    pipeline_runs = get_recent_pipeline_runs(conn, limit=25)

    # Fetch raw items for HTML viewer
    cur = conn.cursor()
    cur.execute("SELECT id, source, url, date, title, short_excerpt, paraphrase, upvotes, comment_count, theme, emotion, intensity, audience FROM raw_items WHERE passed_filters=1 ORDER BY created_at DESC")
    raw_items = [dict(r) for r in cur.fetchall()]
    
    cur.execute("SELECT source, url, title, drop_reason, short_excerpt FROM raw_items WHERE passed_filters=0 ORDER BY created_at DESC")
    dropped_items = [dict(r) for r in cur.fetchall()]
    
    sweep_time = time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    export_html_viewer(ideas, raw_items, glossary, dropped_items, pipeline_runs, sweep_time, "viewer/index.html")
    export_html_viewer(ideas, raw_items, glossary, dropped_items, pipeline_runs, sweep_time, "docs/index.html")
    build_all_pwa_assets(["viewer", "docs"])
