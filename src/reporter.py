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
            writer.writerow([
                g.get("term"),
                g.get("frequency"),
                g.get("source_count"),
                "YES (Vendor Buzzword)" if g.get("is_vendor_marketing_only") == 1 else "NO (Real Practitioner Term)",
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

def export_html_viewer(ideas: List[Dict[str, Any]], raw_items: List[Dict[str, Any]], glossary: List[Dict[str, Any]], dropped_items: List[Dict[str, Any]], sweep_time: str, filepath: str = "viewer/index.html"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    ideas_json = json.dumps(ideas)
    items_json = json.dumps(raw_items)
    glossary_json = json.dumps(glossary)
    dropped_json = json.dumps(dropped_items)
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
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; background: var(--bg); color: var(--text); padding: 24px 32px; line-height: 1.5; }}
  
  /* Header */
  header {{ margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
  .title-area h1 {{ font-size: 26px; font-weight: 800; color: #fff; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }}
  .title-area h1 span.radar {{ color: var(--accent); }}
  p.subtitle {{ color: var(--muted); font-size: 14px; margin-top: 4px; }}
  
  .header-actions {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
  .btn-dump-all {{ background: var(--btn-dump); color: #fff; border: none; padding: 10px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: all 0.2s; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25); }}
  .btn-dump-all:hover {{ background: var(--btn-dump-hover); transform: translateY(-1px); }}

  .sweep-badge {{ background: var(--card); border: 1px solid var(--border); padding: 8px 14px; border-radius: 8px; font-size: 12.5px; display: flex; flex-direction: column; align-items: flex-end; gap: 2px; }}
  .sweep-time {{ color: var(--accent); font-weight: 700; }}

  /* Tabs */
  .tabs {{ display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 8px; flex-wrap: wrap; }}
  .tab-btn {{ background: transparent; border: none; color: var(--muted); padding: 10px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; }}
  .tab-btn:hover {{ color: #fff; background: var(--card); }}
  .tab-btn.active {{ background: var(--card); color: var(--accent); border-bottom: 2px solid var(--accent); }}

  /* Filters */
  .filters {{ display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; background: var(--card); padding: 14px 18px; border-radius: 10px; border: 1px solid var(--border); align-items: flex-end; }}
  .filter-group {{ display: flex; flex-direction: column; gap: 4px; flex: 1; min-width: 180px; }}
  label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }}
  select, input {{ background: #0b1120; color: #fff; border: 1px solid var(--border); padding: 9px 12px; border-radius: 6px; font-size: 13px; outline: none; }}
  select:focus, input:focus {{ border-color: var(--accent); }}

  /* Grid & Cards */
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 20px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; gap: 14px; transition: all 0.2s; position: relative; }}
  .card:hover {{ border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }}
  .card-header {{ display: flex; justify-content: space-between; align-items: center; gap: 8px; }}
  .badge {{ font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 5px; text-transform: uppercase; letter-spacing: 0.4px; }}
  .badge-pain {{ background: rgba(248, 113, 113, 0.15); color: var(--tag-pain); border: 1px solid rgba(248, 113, 113, 0.4); }}
  .badge-relief {{ background: rgba(52, 211, 153, 0.15); color: var(--tag-relief); border: 1px solid rgba(52, 211, 153, 0.4); }}
  .badge-receipts {{ background: rgba(251, 191, 36, 0.15); color: var(--tag-receipts); border: 1px solid rgba(251, 191, 36, 0.4); }}
  .badge-news {{ background: rgba(129, 140, 248, 0.15); color: var(--tag-news); border: 1px solid rgba(129, 140, 248, 0.4); }}
  
  .trace-id {{ font-size: 11px; font-family: monospace; color: var(--accent); background: #080d1a; padding: 2px 6px; border-radius: 4px; border: 1px solid var(--border); }}
  .idea-title {{ font-size: 17px; font-weight: 700; color: #fff; line-height: 1.35; }}
  .hook-box {{ background: #080d1a; border-left: 3px solid var(--accent); padding: 12px 14px; border-radius: 6px; font-size: 13.5px; color: #e2e8f0; font-style: italic; }}
  .meta-grid {{ display: grid; grid-template-columns: 1fr; gap: 6px; font-size: 12.5px; color: var(--muted); }}
  .meta-grid strong {{ color: #cbd5e1; }}
  
  .evidence-section {{ margin-top: auto; border-top: 1px solid var(--border); padding-top: 12px; }}
  .evidence-header {{ font-size: 12px; font-weight: 700; color: var(--muted); text-transform: uppercase; margin-bottom: 8px; }}
  .evidence-item {{ font-size: 12px; color: #cbd5e1; margin-bottom: 6px; line-height: 1.4; }}
  
  /* Copy Button */
  .copy-btn {{ background: var(--btn-copy); color: #fff; border: none; padding: 9px 14px; border-radius: 6px; font-size: 12.5px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; transition: background 0.2s; margin-top: 8px; width: 100%; }}
  .copy-btn:hover {{ background: var(--btn-copy-hover); }}

  /* Tables */
  .table-container {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow-x: auto; }}
  .table-view {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
  .table-view th, .table-view td {{ padding: 12px 16px; border-bottom: 1px solid var(--border); }}
  .table-view th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; font-weight: 700; background: #0c1424; }}
  .table-view tr:hover {{ background: rgba(255,255,255,0.02); }}
  
  /* Toast */
  #toast {{ visibility: hidden; min-width: 320px; background-color: #0284c7; color: #fff; text-align: center; border-radius: 8px; padding: 14px 20px; position: fixed; z-index: 100; right: 30px; bottom: 30px; font-size: 14px; font-weight: 600; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }}
  #toast.show {{ visibility: visible; animation: fadein 0.3s, fadeout 0.5s 2.5s; }}
  @keyframes fadein {{ from {{ bottom: 0; opacity: 0; }} to {{ bottom: 30px; opacity: 1; }} }}
  @keyframes fadeout {{ from {{ bottom: 30px; opacity: 1; }} to {{ bottom: 0; opacity: 0; }} }}
</style>
</head>
<body>

<header>
  <div class="title-area">
    <h1><span class="radar">📡</span> Sayari Compliance Signal Radar & Living Brain</h1>
    <p class="subtitle">Continuous public discussion mining, practitioner psychographics, and 4-format LinkedIn idea bank</p>
  </div>
  <div class="header-actions">
    <button id="pwaInstallBtn" style="display:none; background:#38bdf8; color:#090d16; border:none; padding:10px 16px; border-radius:8px; font-weight:700; cursor:pointer; font-size:13.5px; transition:all 0.2s;" onclick="installPWA()">
      📱 Install App
    </button>
    <button class="btn-dump-all" onclick="dumpEntireBrainToClipboard()">
      📋 Dump Entire Brain for Claude (No Links, Trace IDs)
    </button>
    <div class="sweep-badge">
      <div>Last Sweep: <span class="sweep-time">{sweep_time}</span></div>
      <div style="font-size:11px; color:#34d399;">● {len(raw_items)} Signals Active</div>
    </div>
  </div>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('ideas')">🎯 Ranked Idea Bank & Claude Prompts</button>
  <button class="tab-btn" onclick="switchTab('brain')">🧠 Living Brain (Theme Buckets)</button>
  <button class="tab-btn" onclick="switchTab('lexicon')">🍺 "The Beer Test" Lexicon</button>
  <button class="tab-btn" onclick="switchTab('raw')">🔍 Raw Signals Stream ({len(raw_items)} Passed)</button>
  <button class="tab-btn" onclick="switchTab('noise')">🛡️ Noise Shield ({len(dropped_items)} Blocked)</button>
</div>

<div class="filters" id="filterBar">
  <div class="filter-group">
    <label>Format</label>
    <select id="filterFormat" onchange="render()">
      <option value="all">All Formats</option>
      <option value="Pain mirror">Pain mirror (35%)</option>
      <option value="Product as relief">Product as relief (25%)</option>
      <option value="The receipts">The receipts (20%)</option>
      <option value="Headline to what it means for you">Headline / Newsjack (20%)</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Min Intensity</label>
    <select id="filterIntensity" onchange="render()">
      <option value="1">1+ (All Signals)</option>
      <option value="2">2+ (Moderate Frustration)</option>
      <option value="3">3+ (High Frustration/Fear)</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Search Keyword</label>
    <input type="text" id="filterSearch" placeholder="e.g. name matching, swivel chair, ubo, backlog" oninput="render()">
  </div>
</div>

<!-- Tab Containers -->
<div id="ideasContainer" class="grid"></div>

<div id="brainContainer" style="display:none;" class="grid"></div>

<div id="lexiconContainer" style="display:none;" class="table-container">
  <table class="table-view">
    <thead>
      <tr>
        <th>Term (What Practitioners Say)</th>
        <th>Category</th>
        <th>Occurrences</th>
        <th>Sample Real Context</th>
      </tr>
    </thead>
    <tbody id="lexiconTbody"></tbody>
  </table>
</div>

<div id="rawContainer" style="display:none;" class="table-container">
  <table class="table-view">
    <thead>
      <tr>
        <th>Trace ID</th>
        <th>Source</th>
        <th>Title / News / Topic</th>
        <th>Short Excerpt</th>
        <th>Theme</th>
        <th>Emotion</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody id="rawTbody"></tbody>
  </table>
</div>

<div id="noiseContainer" style="display:none;" class="table-container">
  <div style="padding:14px 18px; background:#0c1424; border-bottom:1px solid var(--border); font-size:13px; color:var(--muted);">
    🛡️ <strong>Noise Shield Active:</strong> Showing posts silently blocked from entering your idea bank (vendor promo spam, career questions, and certification guides without daily-work frustration).
  </div>
  <table class="table-view">
    <thead>
      <tr>
        <th>Source</th>
        <th>Title</th>
        <th>Reason Blocked</th>
      </tr>
    </thead>
    <tbody id="noiseTbody"></tbody>
  </table>
</div>

<div id="toast">✅ Text Copied to Clipboard!</div>

<script>
const IDEAS = {ideas_json};
const RAW_ITEMS = {items_json};
const GLOSSARY = {glossary_json};
const DROPPED_ITEMS = {dropped_json};
const CLAUDE_DUMP = {claude_dump_json};

let currentTab = 'ideas';

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

function formatEvidenceLines(idx, sources) {{
  if (!sources || !sources.length) return "- (No evidence attached)";
  return sources.map(function(ev, i) {{
    var cleanSrc = ev.url.replace('https://www.reddit.com/r/', 'Reddit r/').replace('https://', '').split('/')[0];
    return "- [Trace ID #" + (idx + 1) + "-" + (i + 1) + " | Source: " + cleanSrc + "]: \\"" + ev.paraphrase + "\\"";
  }}).join('\\n');
}}

function formatEvidenceHtml(idx, sources) {{
  if (!sources || !sources.length) return "";
  return sources.map(function(ev, i) {{
    var cleanSrc = ev.url.replace('https://www.reddit.com/r/', 'Reddit r/').replace('https://', '').split('/')[0];
    return '<div class="evidence-item"><span class="trace-id" style="font-size:10px;">#' + (idx + 1) + '-' + (i + 1) + '</span> <strong>' + cleanSrc + '</strong> (' + ev.upvotes + ' upvotes): <em>\\"' + ev.paraphrase + '\\"</em></div>';
  }}).join('');
}}

function copyIdeaPrompt(idx) {{
  const idea = IDEAS[idx];
  if (!idea) return;

  const prompt = `I am drafting a LinkedIn post for Sayari targeting compliance officers and financial crime / sanctions analysts.

Format: ${{idea.format}}
Pillar: ${{idea.pillar}}
Post Concept: ${{idea.title}}
The Hook: "${{idea.hook}}"
Visual Metaphor: ${{idea.suggested_visual}}

Verified Evidence & Real Quotes (Sourced with Trace IDs):
` + formatEvidenceLines(idx, idea.evidence_sources) + `

Voice Guidelines:
- Validating, unflinching, human, a little funny, proof-backed.
- Zero vendor buzzwords (no "judgment infrastructure", "zero-resistance", or "synergies"). Must pass the "Beer Test."
- Meet them mid-drown, name the Frankenstack as the real enemy, and show the shift to evidence-based records.

Please write 2 variations of this LinkedIn post ready to publish.`;

  copyTextToClipboard(prompt, `📋 Copied Idea #${{idx+1}} Prompt for Claude!`);
}}

function copyThemePrompt(themeKey) {{
  const b = THEME_BUCKETS[themeKey];
  if (!b) return;

  var angleLines = b.ideas.map(function(i, aIdx) {{
    return "- Angle " + (aIdx + 1) + ': "' + i.title + '" (Hook: "' + i.hook + '")';
  }}).join('\\n');

  const prompt = `I am drafting a LinkedIn post for Sayari focusing on this core compliance theme:

Theme: ` + themeKey + `
The Practitioner Reality: ` + b.desc + `
Sayari Sourced Proof Anchor: ` + b.proof + `

Angles & Hooks to explore:
` + angleLines + `

Voice Guidelines:
- Validating, unflinching, human, a little funny. Pass the "Beer Test".
- Zero vendor buzzwords.

Please write 2 LinkedIn post variations for this theme.`;

  copyTextToClipboard(prompt, "📋 Copied Theme Prompt for Claude!");
}}

function copySignalPrompt(idx) {{
  const it = RAW_ITEMS[idx];
  if (!it) return;

  const cleanSrc = it.source.replace('pasted:', '').replace('rss:', '').replace('manual:', '');
  const text = "[Trace ID #" + (idx + 1) + " | Source: " + cleanSrc + "]\\nTopic: " + it.title + "\\nQuote: \\"" + it.short_excerpt + "\\"\\nContext: " + it.paraphrase + "\\nTheme: " + (it.theme || 'General');

  copyTextToClipboard(text, "📋 Copied Trace ID #" + (idx + 1) + "!");
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
  ['ideasContainer', 'brainContainer', 'lexiconContainer', 'rawContainer', 'noiseContainer'].forEach(id => {{
    document.getElementById(id).style.display = 'none';
  }});

  const filterBar = document.getElementById('filterBar');
  filterBar.style.display = (tab === 'ideas' || tab === 'raw') ? 'flex' : 'none';

  if (tab === 'ideas') {{
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.getElementById('ideasContainer').style.display = 'grid';
  }} else if (tab === 'brain') {{
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
    document.getElementById('brainContainer').style.display = 'grid';
    renderBrain();
  }} else if (tab === 'lexicon') {{
    document.querySelectorAll('.tab-btn')[2].classList.add('active');
    document.getElementById('lexiconContainer').style.display = 'block';
    renderLexicon();
  }} else if (tab === 'raw') {{
    document.querySelectorAll('.tab-btn')[3].classList.add('active');
    document.getElementById('rawContainer').style.display = 'block';
  }} else if (tab === 'noise') {{
    document.querySelectorAll('.tab-btn')[4].classList.add('active');
    document.getElementById('noiseContainer').style.display = 'block';
    renderNoise();
  }}
  render();
}}

let THEME_BUCKETS = {{}};

function renderBrain() {{
  THEME_BUCKETS = {{
    "The Frankenstack & Swivel Chair Effect": {{
      desc: "Analysts drowning across 5-7 disconnected tabs, Excel files, and PDF registries.",
      proof: "Sayari Fortune 50 Energy case: 75+ data sources collapsed into one; costly homegrown system retired.",
      ideas: IDEAS.filter(i => i.pillar.includes('Frankenstack') && i.format.includes('Pain'))
    }},
    "Entity Resolution & Name-Match Purgatory": {{
      desc: "Algorithms generating 90-95% false positives on Spanish, Arabic, or corporate suffix variations.",
      proof: "Fortune 50 Energy Supermajor: 1.2M records screened in real time vs 24-48 hours on competitor.",
      ideas: IDEAS.filter(i => i.title.toLowerCase().includes('name') || i.title.toLowerCase().includes('tabs'))
    }},
    "The Risk in Plain Sight: Nested UBO & Shell Networks": {{
      desc: "Clean supplier questionnaires hiding designated oligarchs across 3 offshore hops.",
      proof: "No. 3 Global Telecom: 72% of flagged risk was on zero watchlists anywhere, buried in nested ownership.",
      ideas: IDEAS.filter(i => i.pillar.includes('plain sight') || i.title.toLowerCase().includes('apartment') || i.title.toLowerCase().includes('ubo'))
    }},
    "A Score Is Not a Defense: Audit Dread & Regulators": {{
      desc: "Regulators rejecting black-box automated risk scores without verifiable registry audit trails.",
      proof: "Enforcement doctrine: a clean self-certification questionnaire is not an audit defense.",
      ideas: IDEAS.filter(i => i.pillar.includes('defense') || i.title.toLowerCase().includes('score'))
    }}
  }};

  const html = Object.entries(THEME_BUCKETS).map(([title, b]) => `
    <div class="card" style="border-top: 3px solid var(--accent);">
      <div class="idea-title" style="color:var(--accent); font-size:18px;">${{title}}</div>
      <p style="font-size:13px; color:#cbd5e1;">${{b.desc}}</p>
      <div style="background:#080d1a; padding:10px 12px; border-radius:6px; font-size:12.5px; border-left:3px solid #34d399;">
        <strong>Sayari Proof Anchor:</strong> ${{b.proof}}
      </div>
      <div style="margin-top:8px;">
        <div style="font-size:12px; font-weight:700; color:var(--muted); margin-bottom:6px;">ASSOCIATED SOURCED ANGLES:</div>
        ${{b.ideas.map(i => `
          <div style="font-size:13px; margin-bottom:6px; display:flex; justify-content:space-between; align-items:center;">
            <span>&bull; ${{i.title}}</span>
            <span class="badge ${{getBadgeClass(i.format)}}" style="font-size:9px;">${{i.format}}</span>
          </div>
        `).join('') || '<div style="font-size:12px; color:var(--muted);">More signals being slotted on next sweep...</div>'}}
      </div>
      <button class="copy-btn" onclick="copyThemePrompt('${{title}}')">
        📋 Copy Theme Prompt for Claude
      </button>
    </div>
  `).join('');
  document.getElementById('brainContainer').innerHTML = html;
}}

function renderLexicon() {{
  const html = GLOSSARY.map(g => `
    <tr>
      <td><strong style="color:#fff;">${{g.term}}</strong></td>
      <td><span class="pill ${{g.is_vendor_marketing_only.includes('YES') ? 'badge-pain' : 'badge-relief'}}">${{g.is_vendor_marketing_only.includes('YES') ? 'Banned Vendor Fluff' : 'Real Practitioner Slang'}}</span></td>
      <td>${{g.frequency}}</td>
      <td style="color:#cbd5e1; font-style:italic;">${{g.example_context}}</td>
    </tr>
  `).join('');
  document.getElementById('lexiconTbody').innerHTML = html;
}}

function renderNoise() {{
  const html = DROPPED_ITEMS.map(d => `
    <tr>
      <td>${{d.source || 'Public Feed'}}</td>
      <td><strong>${{d.title}}</strong></td>
      <td><span style="color:#f87171;">${{d.drop_reason || 'Vendor Promotion / No Frustration'}}</span></td>
    </tr>
  `).join('');
  document.getElementById('noiseTbody').innerHTML = html;
}}

function render() {{
  const fmt = document.getElementById('filterFormat').value;
  const minInt = parseFloat(document.getElementById('filterIntensity').value);
  const q = document.getElementById('filterSearch').value.toLowerCase().trim();

  if (currentTab === 'ideas') {{
    const filtered = IDEAS.filter(idea => {{
      const matchFmt = (fmt === 'all' || idea.format === fmt);
      const matchInt = (idea.avg_intensity >= minInt);
      const matchQ = (!q || idea.title.toLowerCase().includes(q) || idea.hook.toLowerCase().includes(q) || idea.suggested_visual.toLowerCase().includes(q));
      return matchFmt && matchInt && matchQ;
    }});

    const html = filtered.map((idea, idx) => `
      <div class="card">
        <div class="card-header">
          <span class="badge ${{getBadgeClass(idea.format)}}">${{idea.format}}</span>
          <div style="display:flex; align-items:center; gap:6px;">
            <span class="trace-id">Idea #${{idx+1}}</span>
            <span style="font-size: 12px; font-weight:700; color:var(--accent);">Score: ${{idea.rank_score}}</span>
          </div>
        </div>
        <div class="idea-title">${{idea.title}}</div>
        <div class="hook-box">"${{idea.hook}}"</div>
        <div class="meta-grid">
          <div><strong>Pillar:</strong> ${{idea.pillar}}</div>
          <div><strong>Visual Metaphor:</strong> ${{idea.suggested_visual}}</div>
          <div><strong>Extends Doc Idea:</strong> <em>${{idea.extends_idea}}</em></div>
          <div><strong>Verify Before Use:</strong> ${{idea.verify_before_use}}</div>
        </div>
        
        <button class="copy-btn" onclick="copyIdeaPrompt(${{idx}})">
          📋 Copy Prompt for Claude (Link-free, Sourced)
        </button>

        <div class="evidence-section">
          <div class="evidence-header">Real Public Sourced Proof (${{idea.evidence_sources.length}} sources):</div>
          ${{formatEvidenceHtml(idx, idea.evidence_sources)}}
        </div>
      </div>
    `).join('');
    document.getElementById('ideasContainer').innerHTML = html || '<p style="padding:20px; color:var(--muted)">No ideas matched your filter criteria.</p>';
  }} else if (currentTab === 'raw') {{
    const filtered = RAW_ITEMS.filter(it => {{
      const matchInt = ((it.intensity || 1) >= minInt);
      const matchQ = (!q || it.title.toLowerCase().includes(q) || (it.short_excerpt && it.short_excerpt.toLowerCase().includes(q)));
      return matchInt && matchQ;
    }});

    const html = filtered.map((it, idx) => `
      <tr>
        <td><span class="trace-id">#${{idx+1}}</span></td>
        <td>${{it.source.replace('pasted:', '').replace('rss:', '').replace('manual:', '')}}</td>
        <td><strong>${{it.title}}</strong></td>
        <td>${{it.short_excerpt}}</td>
        <td><span style="color:var(--accent); font-weight:600;">${{it.theme || 'General'}}</span></td>
        <td>${{it.emotion || 'frustration'}} (${{it.intensity || 1}}/5)</td>
        <td>
          <button class="copy-btn" style="padding:4px 8px; font-size:11px; margin:0;" onclick="copySignalPrompt(${{idx}})">
            📋 Copy
          </button>
        </td>
      </tr>
    `).join('');
    document.getElementById('rawTbody').innerHTML = html;
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
  window.addEventListener('load', () => {{
    navigator.serviceWorker.register('./sw.js').catch(err => {{
      console.log('SW registration note:', err);
    }});
  }});
}}

render();
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

    export_raw_items_csv(conn, "raw_items.csv")
    export_ideas_csv(ideas, "ideas.csv")
    export_ideas_markdown(ideas, "ideas.md")
    export_glossary_csv(glossary, "glossary.csv")
    export_blocked_sources_md(conn, "blocked_sources.md")
    
    # Fetch raw items for HTML viewer
    cur = conn.cursor()
    cur.execute("SELECT source, url, date, title, short_excerpt, paraphrase, upvotes, comment_count, theme, emotion, intensity, audience FROM raw_items WHERE passed_filters=1")
    raw_items = [dict(r) for r in cur.fetchall()]
    
    cur.execute("SELECT source, title, drop_reason FROM raw_items WHERE passed_filters=0")
    dropped_items = [dict(r) for r in cur.fetchall()]
    
    sweep_time = time.strftime('%Y-%m-%d %H:%M:%S')
    export_html_viewer(ideas, raw_items, glossary, dropped_items, sweep_time, "viewer/index.html")
    export_html_viewer(ideas, raw_items, glossary, dropped_items, sweep_time, "docs/index.html")
    build_all_pwa_assets(["viewer", "docs"])
