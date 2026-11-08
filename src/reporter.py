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

def export_html_viewer(ideas: List[Dict[str, Any]], raw_items: List[Dict[str, Any]], glossary: List[Dict[str, Any]], dropped_items: List[Dict[str, Any]], sweep_time: str, filepath: str = "viewer/index.html"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    ideas_json = json.dumps(ideas)
    items_json = json.dumps(raw_items)
    glossary_json = json.dumps(glossary)
    dropped_json = json.dumps(dropped_items)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sayari Compliance Signal Radar & Living Brain</title>
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
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif; background: var(--bg); color: var(--text); padding: 24px 32px; line-height: 1.5; }}
  
  /* Header */
  header {{ margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 20px; display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px; }}
  .title-area h1 {{ font-size: 26px; font-weight: 800; color: #fff; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }}
  .title-area h1 span.radar {{ color: var(--accent); }}
  p.subtitle {{ color: var(--muted); font-size: 14px; margin-top: 4px; }}
  
  .sweep-badge {{ background: var(--card); border: 1px solid var(--border); padding: 10px 16px; border-radius: 8px; font-size: 13px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }}
  .sweep-time {{ color: var(--accent); font-weight: 700; }}
  .status-indicators {{ display: flex; gap: 8px; margin-top: 4px; }}
  .pill {{ font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600; }}
  .pill-green {{ background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }}
  .pill-blue {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }}
  .pill-amber {{ background: rgba(251, 191, 36, 0.15); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }}

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
  
  .idea-title {{ font-size: 17px; font-weight: 700; color: #fff; line-height: 1.35; }}
  .hook-box {{ background: #080d1a; border-left: 3px solid var(--accent); padding: 12px 14px; border-radius: 6px; font-size: 13.5px; color: #e2e8f0; font-style: italic; }}
  .meta-grid {{ display: grid; grid-template-columns: 1fr; gap: 6px; font-size: 12.5px; color: var(--muted); }}
  .meta-grid strong {{ color: #cbd5e1; }}
  
  .evidence-section {{ margin-top: auto; border-top: 1px solid var(--border); padding-top: 12px; }}
  .evidence-header {{ font-size: 12px; font-weight: 700; color: var(--muted); text-transform: uppercase; margin-bottom: 8px; }}
  .evidence-item {{ font-size: 12px; color: #cbd5e1; margin-bottom: 6px; line-height: 1.4; }}
  .evidence-item a {{ color: var(--accent); text-decoration: none; word-break: break-all; }}
  .evidence-item a:hover {{ text-decoration: underline; }}
  
  /* Copy Button */
  .copy-btn {{ background: var(--btn-copy); color: #fff; border: none; padding: 8px 14px; border-radius: 6px; font-size: 12.5px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; transition: background 0.2s; margin-top: 8px; width: 100%; }}
  .copy-btn:hover {{ background: var(--btn-copy-hover); }}

  /* Tables */
  .table-container {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; overflow-x: auto; }}
  .table-view {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
  .table-view th, .table-view td {{ padding: 12px 16px; border-bottom: 1px solid var(--border); }}
  .table-view th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; font-weight: 700; background: #0c1424; }}
  .table-view tr:hover {{ background: rgba(255,255,255,0.02); }}
  
  /* Toast */
  #toast {{ visibility: hidden; min-width: 280px; background-color: #0284c7; color: #fff; text-align: center; border-radius: 8px; padding: 14px 20px; position: fixed; z-index: 100; right: 30px; bottom: 30px; font-size: 14px; font-weight: 600; box-shadow: 0 8px 24px rgba(0,0,0,0.4); }}
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
  <div class="sweep-badge">
    <div>Last Sweep: <span class="sweep-time">{sweep_time}</span></div>
    <div class="status-indicators">
      <span class="pill pill-green">Reddit (Apify/PRAW Active)</span>
      <span class="pill pill-blue">RSS Feeds Active</span>
      <span class="pill pill-amber">Manual Drops Ready</span>
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
        <th>Source</th>
        <th>Title</th>
        <th>Short Excerpt (Max 25w)</th>
        <th>Theme</th>
        <th>Emotion (1-5)</th>
        <th>URL</th>
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

<div id="toast">✅ Prompt Copied to Clipboard! Paste into Claude.</div>

<script>
const IDEAS = {ideas_json};
const RAW_ITEMS = {items_json};
const GLOSSARY = {glossary_json};
const DROPPED_ITEMS = {dropped_json};

let currentTab = 'ideas';

function showToast(msg) {{
  const toast = document.getElementById('toast');
  toast.innerText = msg;
  toast.className = 'show';
  setTimeout(() => {{ toast.className = toast.className.replace('show', ''); }}, 2800);
}}

function copyClaudePrompt(ideaTitle, format, pillar, hook, visual, evidenceList) {{
  const prompt = `I am drafting a LinkedIn post for Sayari targeting compliance officers and financial crime / sanctions analysts.

Format: ${{format}}
Pillar: ${{pillar}}
Post Concept: ${{ideaTitle}}
The Hook: "${{hook}}"
Visual Metaphor: ${{visual}}

Real Practitioner Evidence & Sourced Sentiment:
${{evidenceList.map(e => '- ' + e.paraphrase + ' (Source: ' + e.url + ')').join('\\n')}}

Voice Guidelines:
- Validating, unflinching, human, a little funny, proof-backed.
- Zero vendor buzzwords (no "judgment infrastructure", "zero-resistance", or "synergies"). Must pass the "Beer Test."
- Meet them mid-drown, name the Frankenstack as the real enemy, and show the shift to evidence-based records.

Please write 2 variations of this LinkedIn post ready to publish.`;

  navigator.clipboard.writeText(prompt).then(() => {{
    showToast('📋 Copied Claude Prompt! Paste into Claude to generate your post.');
  }});
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

function renderBrain() {{
  // Group ideas and evidence into master theme buckets (the growing brain)
  const buckets = {{
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

  const html = Object.entries(buckets).map(([title, b]) => `
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
          <span style="font-size: 12px; font-weight:700; color:var(--accent);">Score: ${{idea.rank_score}}</span>
        </div>
        <div class="idea-title">${{idea.title}}</div>
        <div class="hook-box">"${{idea.hook}}"</div>
        <div class="meta-grid">
          <div><strong>Pillar:</strong> ${{idea.pillar}}</div>
          <div><strong>Visual Metaphor:</strong> ${{idea.suggested_visual}}</div>
          <div><strong>Extends Doc Idea:</strong> <em>${{idea.extends_idea}}</em></div>
          <div><strong>Verify Before Use:</strong> ${{idea.verify_before_use}}</div>
        </div>
        
        <button class="copy-btn" onclick='copyClaudePrompt("${{idea.title.replace(/"/g, '&quot;')}}", "${{idea.format}}", "${{idea.pillar}}", "${{idea.hook.replace(/"/g, '&quot;')}}", "${{idea.suggested_visual.replace(/"/g, '&quot;')}}", ${{JSON.stringify(idea.evidence_sources)}})'>
          📋 Copy Prompt for Claude
        </button>

        <div class="evidence-section">
          <div class="evidence-header">Real Public Sourced Proof (${{idea.evidence_sources.length}} sources):</div>
          ${{idea.evidence_sources.map(ev => `
            <div class="evidence-item">
              &bull; <a href="${{ev.url}}" target="_blank" rel="noopener">${{ev.url.replace('https://', '')}}</a> (${{ev.upvotes}} upvotes): <em>"${{ev.paraphrase}}"</em>
            </div>
          `).join('')}}
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

    const html = filtered.map(it => `
      <tr>
        <td>${{it.source}}</td>
        <td><strong>${{it.title}}</strong></td>
        <td>${{it.short_excerpt}}</td>
        <td><span style="color:var(--accent); font-weight:600;">${{it.theme || 'General'}}</span></td>
        <td>${{it.emotion || 'frustration'}} (${{it.intensity || 1}}/5)</td>
        <td><a href="${{it.url}}" target="_blank" rel="noopener" style="color:var(--accent);">Open Link &rarr;</a></td>
      </tr>
    `).join('');
    document.getElementById('rawTbody').innerHTML = html;
  }}
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
