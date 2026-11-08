# Sayari Content Research Tool

A lightweight local research tool built for B2B marketers creating LinkedIn content for **Sayari** (corporate ownership and supply chain risk intelligence).

The tool mines public practitioner discussions across Reddit, RSS industry commentary, and manual imports (LinkedIn comments, G2 reviews). It identifies authentic practitioner language, frustrations, and reactions, clustering them into sourced content ideas aligned with Sayari's 4 core social formats:

1. **Pain mirror (35%)** — *The Frankenstack Reckoning* ("that's literally my job")
2. **Product as relief (25%)** — *The Frankenstack Reckoning* ("wait, you can just do that?")
3. **The receipts (20%)** — *The risk hiding in plain sight* (ownership chain teardowns, shell company carousels)
4. **Headline to what it means for you (20%)** — *A score is not a defense* (newsjack takeaways)

---

## Hard Rules & Privacy Standards
- **No scraping of LinkedIn, G2, Glassdoor, or Blind**: Ingested strictly via manual file drop into `data/imports/`.
- **Fair use & copyright limits**: Stores short excerpts only (**max 25 words**) plus a paraphrased summary. Full articles are never stored.
- **Privacy & GDPR/terms**: Never stores usernames or profile metadata. URLs and post IDs only.
- **Robots.txt & paywalls**: Respects site restrictions. Paywalled or anti-bot blocked feeds are logged to `blocked_sources.md` rather than bypassed.

---

## Quickstart

### 1. Environment Setup (via `uv`)
```bash
uv venv .venv
source .venv/bin/activate
uv pip install pyyaml praw feedparser requests beautifulsoup4 pytest
```

### 2. Verify with Seed Text Analysis
```bash
python run.py analyze-text
```
This tests tagging, clustering, glossary generation, and idea bank generation on sample practitioner rants, updating all output files immediately.

### 3. Review Source Discovery Candidates
```bash
python run.py discover
```
Inspect `source_candidates.md` to review suggested subreddits, publications, and target career pages before approving them into `config.yaml`.

---

## Reddit API Registration (Step-by-Step)

Modern Reddit API access requires an official OAuth script app:

1. Log into your Reddit account and visit: **[https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)**
2. Scroll to the bottom and click **"are you a developer? create an app..."** or **"create another app..."**.
3. Choose the **script** option (designed for personal scripts / non-commercial use).
4. Fill in:
   - **name**: `sayari-content-research`
   - **description**: `Non-commercial research tool for B2B compliance content analysis`
   - **about url**: (leave blank)
   - **redirect uri**: `http://localhost:8080` (required placeholder)
5. Click **"create app"**.
6. Note the credentials:
   - **Client ID**: The string displayed immediately beneath the app name (e.g., `AB12cdEF34gh_ij`).
   - **Client Secret**: The string labeled `secret` (e.g., `xyz987_abc123...`).
7. Open `config.yaml` and paste them:
   ```yaml
   reddit:
     client_id: "YOUR_CLIENT_ID"
     client_secret: "YOUR_CLIENT_SECRET"
     user_agent: "SayariContentResearch/1.0 by YourUsername"
   ```

### ⚠️ Free Non-Commercial Tier Check
Reddit's Developer Terms allow free API access for personal, non-commercial research up to **100 queries per minute** via OAuth. This tool operates in read-only mode, enforces rate-limiting sleep intervals, and caches responses in SQLite to remain well under the free rate limits.

---

## Adding New Sources

All sources are configured in `config.yaml`:

### Add a Subreddit
```yaml
reddit:
  subreddits:
    - "AMLCompliance"
    - "financialcrime"
    - "compliance"
    - "RegulatoryCompliance"
    - "OSINT"             # Add new subreddits here
```

### Add an RSS Feed
```yaml
rss_sources:
  major:
    - name: "My New Compliance Feed"
      url: "https://example.com/rss"
      enabled: true
```

### Tier 3 Manual Imports
Drop any `.csv`, `.txt`, or `.md` files containing hand-collected quotes, LinkedIn comments, or G2 review snippets into:
```
data/imports/
```
Then run:
```bash
python run.py import-manual
```

---

## Running the Pipeline

- **Collect from RSS feeds**: `python run.py collect-rss`
- **Collect from Reddit**: `python run.py collect-reddit --sub AMLCompliance`
- **Import manual drops**: `python run.py import-manual`
- **Generate ranked idea bank**: `python run.py generate-ideas`
- **Run full pipeline end-to-end**: `python run.py pipeline`

---

## Generated Outputs

1. **`ideas.md`**: Formatted briefing document of ranked ideas with plain-language hooks, visual metaphors, evidence citations (3+ sources), and risk/verification notes.
2. **`ideas.csv`**: Machine-readable spreadsheet of all ranked content ideas.
3. **`glossary.csv`**: Dictionary of real practitioner language with frequency and context, explicitly flagging vendor marketing buzzwords (e.g. *"judgment infrastructure"*, *"zero-resistance"*).
4. **`raw_items.csv`**: Full export of all validated items with tags, emotion/intensity, and source URLs.
5. **`blocked_sources.md`**: Transparent log of any feeds returning 401/403 or disallowing robots.txt.
6. **`viewer/index.html`**: Interactive local browser dashboard with filters for format, theme, and intensity (open in any browser: `open viewer/index.html`).

---

## Running Tests
```bash
PYTHONPATH=. pytest tests/
```
Verifies compliance keyword matching, career/exam-prep dropping, and daily-work frustration exception logic.
