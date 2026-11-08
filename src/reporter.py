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

def export_html_viewer(ideas: List[Dict[str, Any]], raw_items: List[Dict[str, Any]], filepath: str = "viewer/index.html"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    ideas_json = json.dumps(ideas)
    items_json = json.dumps(raw_items)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sayari Research Tool — Idea Bank & Evidence Explorer</title>
<style>
  :root {{
    --bg: #0f172a;
    --card: #1e293b;
    --text: #f8fafc;
    --muted: #94a3b8;
    --border: #334155;
    --accent: #38bdf8;
    --tag-pain: #f87171;
    --tag-relief: #34d399;
    --tag-receipts: #fbbf24;
    --tag-news: #818cf8;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); padding: 24px; }}
  header {{ margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 16px; display: flex; justify-content: space-between; align-items: flex-end; }}
  h1 {{ font-size: 24px; color: var(--accent); }}
  p.subtitle {{ color: var(--muted); font-size: 14px; margin-top: 4px; }}
  .filters {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; background: var(--card); padding: 14px; border-radius: 8px; border: 1px solid var(--border); }}
  .filter-group {{ display: flex; flex-direction: column; gap: 4px; }}
  label {{ font-size: 12px; color: var(--muted); text-transform: uppercase; font-weight: 600; }}
  select, input {{ background: #0b1120; color: #fff; border: 1px solid var(--border); padding: 8px 12px; border-radius: 6px; font-size: 14px; }}
  .tabs {{ display: flex; gap: 8px; margin-bottom: 16px; }}
  .tab-btn {{ background: var(--card); border: 1px solid var(--border); color: var(--muted); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; }}
  .tab-btn.active {{ background: var(--accent); color: #000; border-color: var(--accent); }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 16px; }}
  .card {{ background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 18px; display: flex; flex-direction: column; gap: 12px; transition: border-color 0.2s; }}
  .card:hover {{ border-color: var(--accent); }}
  .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }}
  .badge {{ font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; }}
  .badge-pain {{ background: rgba(248, 113, 113, 0.2); color: var(--tag-pain); border: 1px solid var(--tag-pain); }}
  .badge-relief {{ background: rgba(52, 211, 153, 0.2); color: var(--tag-relief); border: 1px solid var(--tag-relief); }}
  .badge-receipts {{ background: rgba(251, 191, 36, 0.2); color: var(--tag-receipts); border: 1px solid var(--tag-receipts); }}
  .badge-news {{ background: rgba(129, 140, 248, 0.2); color: var(--tag-news); border: 1px solid var(--tag-news); }}
  .idea-title {{ font-size: 16px; font-weight: 700; line-height: 1.3; }}
  .hook {{ font-size: 14px; color: #e2e8f0; font-style: italic; background: #0b1120; padding: 10px; border-radius: 6px; border-left: 3px solid var(--accent); }}
  .meta {{ font-size: 12px; color: var(--muted); display: flex; flex-direction: column; gap: 4px; }}
  .evidence-box {{ margin-top: auto; border-top: 1px solid var(--border); padding-top: 10px; }}
  .evidence-title {{ font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 6px; }}
  .evidence-item {{ font-size: 12px; margin-bottom: 4px; }}
  .evidence-item a {{ color: var(--accent); text-decoration: none; }}
  .evidence-item a:hover {{ text-decoration: underline; }}
  .table-view {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .table-view th, .table-view td {{ padding: 10px; border-bottom: 1px solid var(--border); text-align: left; }}
  .table-view th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; background: #0b1120; }}
  .table-view tr:hover {{ background: rgba(255,255,255,0.02); }}
</style>
</head>
<body>

<header>
  <div>
    <h1>Sayari Compliance Research & Idea Bank</h1>
    <p class="subtitle">Public evidence mining, real practitioner language, and 4-format LinkedIn idea generation</p>
  </div>
  <div>
    <span style="font-size: 13px; color: var(--muted);" id="stats">Loading...</span>
  </div>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('ideas')">Ranked Ideas Bank</button>
  <button class="tab-btn" onclick="switchTab('raw')">Raw Sourced Items</button>
</div>

<div class="filters">
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
    <label>Min Intensity (1-5)</label>
    <select id="filterIntensity" onchange="render()">
      <option value="1">1+ (All)</option>
      <option value="2">2+ (Moderate)</option>
      <option value="3">3+ (Strong)</option>
      <option value="4">4+ (High frustration/fear)</option>
    </select>
  </div>
  <div class="filter-group">
    <label>Search Keyword</label>
    <input type="text" id="filterSearch" placeholder="e.g. name matching, ubo, backlog" oninput="render()">
  </div>
</div>

<div id="ideasContainer" class="grid"></div>
<div id="rawContainer" style="display:none; background:var(--card); border:1px solid var(--border); border-radius:8px; overflow-x:auto;"></div>

<script>
const IDEAS = {ideas_json};
const RAW_ITEMS = {items_json};
let currentTab = 'ideas';

function getBadgeClass(fmt) {{
  if (fmt.includes('Pain')) return 'badge-pain';
  if (fmt.includes('relief')) return 'badge-relief';
  if (fmt.includes('receipts')) return 'badge-receipts';
  return 'badge-news';
}}

function switchTab(tab) {{
  currentTab = tab;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  if (tab === 'ideas') {{
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.getElementById('ideasContainer').style.display = 'grid';
    document.getElementById('rawContainer').style.display = 'none';
  }} else {{
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
    document.getElementById('ideasContainer').style.display = 'none';
    document.getElementById('rawContainer').style.display = 'block';
  }}
  render();
}}

function render() {{
  const fmt = document.getElementById('filterFormat').value;
  const minInt = parseFloat(document.getElementById('filterIntensity').value);
  const q = document.getElementById('filterSearch').value.toLowerCase().trim();

  document.getElementById('stats').innerText = `${{IDEAS.length}} Ideas Generated | ${{RAW_ITEMS.length}} Public Items Sourced`;

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
        <div class="hook">"${{idea.hook}}"</div>
        <div class="meta">
          <div><strong>Pillar:</strong> ${{idea.pillar}}</div>
          <div><strong>Visual Metaphor:</strong> ${{idea.suggested_visual}}</div>
          <div><strong>Extends Doc Idea:</strong> <em>${{idea.extends_idea}}</em></div>
          <div><strong>Risk / Caution:</strong> ${{idea.risks}}</div>
          <div><strong>Verify Before Use:</strong> ${{idea.verify_before_use}}</div>
        </div>
        <div class="evidence-box">
          <div class="evidence-title">Real Public Evidence (${{idea.evidence_sources.length}} sources):</div>
          ${{idea.evidence_sources.map(ev => `
            <div class="evidence-item">
              &bull; <a href="${{ev.url}}" target="_blank" rel="noopener">${{ev.url.replace('https://', '')}}</a> (${{ev.upvotes}} upvotes): <em>${{ev.paraphrase}}</em>
            </div>
          `).join('')}}
        </div>
      </div>
    `).join('');
    document.getElementById('ideasContainer').innerHTML = html || '<p style="padding:20px; color:var(--muted)">No ideas matched your filter criteria.</p>';
  }} else {{
    const filtered = RAW_ITEMS.filter(it => {{
      const matchInt = ((it.intensity || 1) >= minInt);
      const matchQ = (!q || it.title.toLowerCase().includes(q) || (it.short_excerpt && it.short_excerpt.toLowerCase().includes(q)));
      return matchInt && matchQ;
    }});

    let html = `
      <table class="table-view">
        <thead>
          <tr>
            <th>Source</th>
            <th>Title</th>
            <th>Short Excerpt (Max 25w)</th>
            <th>Theme</th>
            <th>Emotion / Intensity</th>
            <th>Audience</th>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          ${{filtered.map(it => `
            <tr>
              <td>${{it.source}}</td>
              <td><strong>${{it.title}}</strong></td>
              <td>${{it.short_excerpt}}</td>
              <td><span style="color:var(--accent);">${{it.theme || 'General'}}</span></td>
              <td>${{it.emotion || 'frustration'}} (${{it.intensity || 1}}/5)</td>
              <td>${{it.audience || 'analyst'}}</td>
              <td><a href="${{it.url}}" target="_blank" rel="noopener" style="color:var(--accent);">Open Link &rarr;</a></td>
            </tr>
          `).join('')}}
        </tbody>
      </table>
    `;
    document.getElementById('rawContainer').innerHTML = html;
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
    export_raw_items_csv(conn, "raw_items.csv")
    export_ideas_csv(ideas, "ideas.csv")
    export_ideas_markdown(ideas, "ideas.md")
    export_glossary_csv(glossary, "glossary.csv")
    export_blocked_sources_md(conn, "blocked_sources.md")
    
    # Fetch raw items for HTML viewer
    cur = conn.cursor()
    cur.execute("SELECT source, url, date, title, short_excerpt, paraphrase, upvotes, comment_count, theme, emotion, intensity, audience FROM raw_items WHERE passed_filters=1")
    raw_items = [dict(r) for r in cur.fetchall()]
    export_html_viewer(ideas, raw_items, "viewer/index.html")
