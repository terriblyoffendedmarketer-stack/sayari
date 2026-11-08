# CLAUDE.md — Sayari Content Research Tool

## Status
- **Summary**: Local research and public discussion mining tool for Sayari LinkedIn content generation. Captures practitioner language, frustrations, and opinions from Reddit, RSS/news feeds, and manual imports, clustering them into ranked content ideas mapped to Sayari's 4 core formats.
- **Current Phase**: Signal & Psychographic Intelligence Reporting complete; dual Reddit listening active (Apify live actor ready + official PRAW pending request review).
- **In Progress**: Reddit official API review approval; continuous multi-source ingestion.
- **What's Next**: Ingesting live community queries and feeding extracted signals into Claude for post copywriting.

## Roadmap
- [x] Phase 1: Local SQLite schema, strict privacy rules (no usernames, <=25 words excerpt, paraphrases).
- [x] Phase 2: Analysis engine (keyword filtering, frustration overrides, sentiment/intensity tagging, theme clustering with Ollama + TF-IDF fallback).
- [x] Phase 3: Content ideator (mapped to 4 formats: Pain Mirror 35%, Product as Relief 25%, Receipts 20%, Newsjack 20%, linking 3+ sources).
- [x] Phase 4: Output generators (`ideas.csv`, `ideas.md`, `glossary.csv`, `raw_items.csv`, `blocked_sources.md`, `viewer/index.html`).
- [x] Phase 5: Official Reddit PRAW collector (caching, rate-limiting, promo skip, privacy compliance).
- [x] Phase 6: RSS public feeds collector with robots.txt check & blocked source logging.
- [x] Phase 7: Tier 3 manual import processor (`data/imports/` for CSV & text files).
- [x] Phase 8: Source discovery engine exporting `source_candidates.md` for human approval.
- [x] Phase 9: Unit tests for filter engine (`tests/test_filters.py`).
- [ ] Phase 10: Plug live Reddit API credentials and run scheduled daily updates.

## File Map
- `config.yaml`: Central editable configuration (sources, keywords, drop patterns, format weights, LLM config).
- `run.py`: CLI entry point (`analyze-text`, `discover`, `collect-apify`, `collect-reddit`, `collect-rss`, `import-manual`, `generate-ideas`, `pipeline`).
- `src/collectors/apify.py`: Live Reddit scraper via Apify actor with time-stratified signal tagging.
- `reports/compliance_psychographic_report.md`: Master psychographic report, practitioner lexicon, cross-channel patterns, and Claude hand-off prompt templates.
- `source_candidates.md`: Discovered subreddits, publications, and target career pages for user review.
- `ideas.csv` / `ideas.md`: Ranked content ideas with hooks, visual metaphors, evidence citations, and risk notes.
- `glossary.csv`: Extracted practitioner terms vs. flagged vendor marketing buzzwords.
- `raw_items.csv`: All ingested and filtered public items.
- `blocked_sources.md`: Log of paywalled or blocked sources (no scraping bypasses).
- `src/db.py`: SQLite schema and data operations enforcing privacy and excerpt word limits.
- `src/filters.py`: Keyword filter and drop rule evaluator with frustration exception logic.
- `src/analyzer.py`: Emotion/intensity, audience, post type, practitioner terminology, and clustering.
- `src/ideator.py`: Four-format idea generator, doc idea extension mapping, and ranking algorithm.
- `src/discovery.py`: Discovers candidate subreddits, authors, publications, and companies for review.
- `src/collectors/reddit.py`: Official PRAW collector with rate limiting and caching.
- `src/collectors/rss.py`: Public RSS collector checking robots.txt and paywalls.
- `src/collectors/manual.py`: Ingests hand-collected CSV/text files from `data/imports/`.
- `src/reporter.py`: Exports CSVs, Markdown briefs, and interactive HTML viewer.
- `viewer/index.html`: Interactive local dashboard with format, theme, and intensity filters.
- `tests/test_filters.py`: Pytest suite for compliance keyword and drop rules.
- `learnings.md`: Debugging notes and operational learnings (`what broke | why | what fixed it`).

## Setup & Run Instructions
1. **Prerequisites**: Python 3.12+ and `uv`.
2. **Environment**:
   ```bash
   uv venv .venv
   source .venv/bin/activate
   uv pip install pyyaml praw feedparser requests beautifulsoup4 pytest
   ```
3. **Execution**:
   - Test text analysis & idea generator: `python run.py analyze-text`
   - Run source discovery: `python run.py discover`
   - Collect RSS feeds: `python run.py collect-rss`
   - Ingest manual files: `python run.py import-manual`
   - Run Reddit collector: `python run.py collect-reddit --sub AMLCompliance`
   - Run full pipeline: `python run.py pipeline`
   - Run tests: `PYTHONPATH=. pytest tests/`
   - Open viewer: open `viewer/index.html` in any browser.

## Bug Notes & Gotchas
- *Promotional Posts vs. Comments*: Promotional vendor posts and tool pitches are dropped from the idea bank, BUT their comments sections are actively harvested. Practitioner objections, skepticism, questions, and praise left under vendor ads represent unfiltered goldmine signals.
- *Reddit credentials*: Modern PRAW requires OAuth script credentials (`client_id` + `client_secret`). Register at `https://www.reddit.com/prefs/apps`.
- *Paywalled feeds*: ACAMS moneylaundering.com (403) and FCPA Blog (401) block automated RSS requests. Per project rules, they are logged to `blocked_sources.md` rather than scraped.
- *Privacy*: No usernames or profile data are ever stored in SQLite or CSV outputs. Excerpts are clipped to max 25 words.
