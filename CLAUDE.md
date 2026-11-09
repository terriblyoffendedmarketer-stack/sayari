# CLAUDE.md — Sayari Content Research Tool

## Status
- **Summary**: Local research and public discussion mining tool for Sayari LinkedIn content generation. Captures practitioner language, frustrations, and opinions from Reddit, RSS/news feeds, and manual imports, clustering them into ranked content ideas mapped to Sayari's 4 core formats.
- **Current Phase**: Deployed to GitHub Pages as an installable Progressive Web App (PWA); automated cloud listening active via GitHub Actions (sweeps every 6 hours without laptop required).
- **In Progress**: Autonomous cloud ingestion across Apify and RSS feeds.
- **What's Next**: Build `content/themes.md` together: validate the 9 candidate themes in FRAMEWORK.md, then templates, then buckets. One bucket at a time.
- **Content production (2026-11-09)**: Brand-page LinkedIn posts. Posts 1–2 are done (in the Google Doc). Selected ideas are 1, 3, 4, 5, 8. **Done: Post 1 = idea 1 (name match, Brightwell), Post 2 = idea 3 (bingo).** Next: 4, 5, 8. **No memes for now**: storytelling images and carousels only. The meme ideas are kept for their insight. Visuals are made with the Claude Design artifact type and the 'Sayari' design system.

## Live PWA & Links
- **GitHub Repository**: https://github.com/terriblyoffendedmarketer-stack/sayari
- **Live PWA Dashboard (Shareable)**: https://terriblyoffendedmarketer-stack.github.io/sayari/
- **Cloud Automation**: Runs every 6 hours via `.github/workflows/scheduled-sweep.yml` using GitHub Actions + Apify Secret.

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
- `src/filters.py`: Filter v2. Source tiers (core subs = practitioner lane, adjacent = edge lane, RSS = news lane, other subs dropped), specific vs generic terms, career/promo drops. `source_lane()` decides what feeds the lexicon.
- `src/analyzer.py`: Emotion/intensity, audience, post type, practitioner terminology, and clustering.
- `src/ideator.py`: Four-format idea generator, doc idea extension mapping, and ranking algorithm.
- `src/discovery.py`: Discovers candidate subreddits, authors, publications, and companies for review.
- `src/collectors/reddit.py`: Official PRAW collector with rate limiting and caching.
- `src/collectors/rss.py`: Public RSS collector checking robots.txt and paywalls.
- `src/collectors/manual.py`: Ingests hand-collected CSV/text files from `data/imports/`.
- `src/reporter.py`: Exports CSVs, Markdown briefs, and interactive HTML viewer.
- `viewer/index.html`: Interactive local dashboard with format, theme, and intensity filters.
- `tests/test_filters.py`: Pytest suite for compliance keyword and drop rules.
- `content/`: content layers. **Start at `content/FRAMEWORK.md`** (the foundation: themes → templates → meme library → idea buckets, plus rules and workflow).
  - `sharpened/`: one file per idea after sharpening. `buckets/`: idea buckets as we fill them. `brand/`: Sayari logos.
  - `idea-doc-images/`: `IMAGE_IDEAS.md` (49 images catalogued), `gallery.html` (local visual gallery). `images/` is gitignored (copyrighted memes; regenerate with the extractor).
- `research/`: inputs. `sayari-site/case-studies/` (all 20 Sayari case studies, saved 2026-11-10), `sayari-site/OTHER_CONTENT_INDEX.md` (19 investigation briefs + 3 buyer guides, plus how to fetch), `competitors/`, `listener_audit.md`.
- `.claude/skills/sayari-content/SKILL.md`: project skill that loads the framework rules for content work.
- `scripts/build_image_gallery.py`: Rebuilds gallery.html from IMAGE_IDEAS.md.
- `scripts/extract_doc_images.py`: Exports a link-shared Google Doc's images and maps each to its section.
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
   - Re-apply filter rules to stored items: `python run.py refilter` (the pipeline runs this automatically)
   - Run full pipeline: `python run.py pipeline`
   - Run tests: `PYTHONPATH=. pytest tests/`
   - Open viewer: open `viewer/index.html` in any browser.

## Bug Notes & Gotchas
- *Promotional Posts vs. Comments*: Promotional vendor posts and tool pitches are dropped from the idea bank, BUT their comments sections are actively harvested. Practitioner objections, skepticism, questions, and praise left under vendor ads represent unfiltered goldmine signals.
- *Reddit credentials*: Modern PRAW requires OAuth script credentials (`client_id` + `client_secret`). Register at `https://www.reddit.com/prefs/apps`.
- *Paywalled feeds*: ACAMS moneylaundering.com (403) and FCPA Blog (401) block automated RSS requests. Per project rules, they are logged to `blocked_sources.md` rather than scraped.
- *Public repo*: GitHub Pages repo is PUBLIC. Only `content/idea-doc-images/images/` is gitignored (copyrighted memes). Customer proof points are public in config.yaml by owner decision (2026-11-09); the ARR split is deliberately not written anywhere.
- *Listener noise (fixed 2026-11-09)*: v1 kept 155/249 items, about 40% noise (off-topic subs, career chat, fake seed CSV). Filter v2 keeps 71. Tune it via `config.yaml` `source_tiers` and `keywords`, then run `refilter`. See `research/listener_audit.md`.
- *Privacy*: No usernames or profile data are ever stored in SQLite or CSV outputs. Excerpts are clipped to max 25 words.
