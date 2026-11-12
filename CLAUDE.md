# CLAUDE.md — Sayari Content Research Tool

## New session? Start here (in this order)
1. This file (status, links, file map). 2. `content/posts/POSTS.md` (what exists, versions, captions). 3. `content/STRATEGY.md` (where we're heading). 4. `playbook/SPEC.md` + `playbook/PITCH.md` (how we work and how every post is pitched). 5. `playbook/CAPTIONS.md` + `content/VOICE.md` (voice). 6. Then, as needed: `content/buckets/IDEA_BANK.md`, `content/themes.md`, `content/FRAMEWORK.md`, `research/` (lexicon, brief summary, case studies), `design/kit/README.md`.
The project skill `.claude/skills/sayari-content/SKILL.md` and auto-memory carry the working rules (one idea at a time; pitch format; hooks kept separate in pitches; no memes; no disclaimers on images; hyper-relevant, not hyper-niche; explain choices plainly; no unprompted lessons; colour rhythm).

## Status
- **Summary**: Sayari LinkedIn content system: a listener (Reddit/RSS → filtered practitioner signal, PWA dashboard) plus a content library (research → themes → templates → idea bank → posts), a design kit, a Claude Design canvas and a Content Hub page.
- **Current Phase**: B. Production, **newsjack mode** (2026-11-12). **Mode change (2026-11-12): newsjack-only for now.** Sayari sends us the news; we turn each story into a newsjack in their formats (explainer GIF or digest carousel; `content/NEWSJACK.md`). Nothing else is retired: the shortlist, idea bank, P01–P04 and every evergreen idea stay as the bank, ready the moment they want that content back. Later: prep extra newsjack formats beyond the two so the feed doesn't look repetitive (not until Sayari replies).
- **Posts**: all four simplified after Ekshika's round-1 feedback. P01 (tab 1) and P03 (tab 5) final = Ekshika's edits; P02 bingo (tab 3) and P04 PURE carousel (tab 4, 2 versions) reworked by us, to send to Ekshika. POSTS.md holds current versions only; superseded ones are in `content/posts/archive/`.
- **Who's who**: the user is freelance; **Ekshika** is the account manager who reviews/edits posts and liaises with Sayari (not a Sayari employee). Sent to Ekshika = submitted.
- **Client feedback round 1 (Ekshika, 2026-11-10):** too verbose. Simplicity-first rules (2-second images, ~30–90-word captions, one personality move) are now in CAPTIONS.md, the kit README, PITCH.md, VOICE.md and the skill; details in `content/feedback/LEARNING_TRACKER.md`. P01/P03 finals (her edits) are logged as versions.
- **NEXT SESSION AGENDA (user's note, 2026-11-10; remind the user at the start, then start on it):** fix monotony before post 5. (1) **Real content as the visual break** beyond the two brand colours: screenshots of news and regulator releases, LinkedIn/Reddit posts, Slack chats and emails (faked is fine), product screenshots. (2) **Add more UGC** (not fewer infographics): infographics stay, UGC joins the mix. Case studies count as UGC (quotes, testimonials, named results). (3) **Sayari release notes and product pages, for context as well as images:** what each feature or addition does and why it matters, plus its screenshots. Then **cross-reference the case studies** to see where that feature (or something like it) was used, and connect them into posts (feature → real customer story). (4) **Wiggle room outside brand colours** (e.g. native UI colours inside screenshots) within the Sayari frame. Plan: build the real-content/UGC library and release-note context map first, then pick post 5 from it. **Progress 2026-11-11:** item 3 done → `research/sayari-site/FEATURE_MAP.md` (15 features × case studies, top 5 pairs, image sources). Items 1, 2 and 4 done → `content/library/LIBRARY.md` (real Graph screenshots, quote bank, listener social cards, regulator sources) + frame rule in `design/kit/README.md`.
- **Shortlist (2026-11-11, parked during newsjack mode, not discarded):** `content/buckets/SHORTLIST.md`, 15 sharpened posts; this week = #1 "Did you mean" search (I38) + #2 tier-visibility chart (I53/H01).
- **Newsjacks (Ekshika, 2026-11-12): required.** Match Sayari's in-house format: explainer GIFs ("paperwork said A, reality was B") and investigation-digest carousels. Breakdown + process: `content/NEWSJACK.md`; animated layout `design/kit/layouts/L7-newsjack-gif.html`, renderer `scripts/render_gif.py`. Captions ~240–440 words for newsjacks (user confirmed); series row I55.
- **What's Next**: the next newsjack, from the story Sayari sends (fallback: our own candidates in `content/buckets/NEWSJACK_STORIES.md`). When evergreen posts resume: post 5 (after the agenda above). The mix needs a Friday-3pm relatable piece (I40 calendar / I38 "Did you mean") or a saveable list (I08 demo questions, tab 8). Pitch it in the PITCH format.
- **Numbering**: idea IDs I01–I09 = the doc's idea tabs (I04 = tab 4); other IDs are internal and stay fixed. "Doc #" column = the doc tab.
- **No memes for now**: storytelling images and carousels only; meme ideas are mined for insight.

## Live PWA & Links
- **GitHub Repository**: https://github.com/terriblyoffendedmarketer-stack/sayari
- **Content Hub (claude.ai page, shared "anyone with the link" by owner choice 2026-11-10; includes the meme images, which stay out of git)**: https://claude.ai/artifact/Gmw5L8TenBeGWB3iVTRHaj (posts, themes, templates, ideas, memes, research). Rebuild after editing any content markdown: `python3 -I scripts/build_hub.py`, then republish `content/hub/hub.html` to that URL (from a new chat, pass it as `url`). Images are published as files: `posts/<f>` ← `content/posts/assets/<f>`, `kit/<f>` ← `design/kit/previews/<f>`, `images/<f>` ← `content/idea-doc-images/images/<f>` (memes, hub-only). Files left out of a publish are kept, so only send new/changed images. Carousel PDFs: `posts/P0X-vK.pdf` ← `content/posts/assets/P0X-vK.pdf` (the hub shows a "Download carousel (PDF)" button for them). The hub declares `downloads`, `db` (rule: `inbox` owner-only read+write), `user`, `assets`, `sample` with images (omit `capabilities` on redeploys so they carry forward). **Inbox tab (owner only):** the user dumps ideas, links, images + context; "Sort with Claude" tags them (uses the user's own Claude usage) and they show in the Ideas tab as `inbox` rows. **Run `/hub-sync` (`.claude/skills/hub-sync/SKILL.md`) at the start of post work:** pulls caption edits, renders changed canvas artboards into post images (old ones archived), files the inbox into IDEA_BANK / `content/inbox/`, rebuilds, republishes, commits. **Backup shelf (Posts tab, owner only):** select versions → "Move selected to Backup" (db `shelf/<P0X-vN>`; Restore deletes the doc). For versions set aside for later; the archive stays recovery-only. P04 (both versions) moved to Backup 2026-11-11. **Never republish the hub without the user's OK, and check `capdrafts` first** (a publish reloads the page; unsaved typing was lost on 2026-11-12). The caption editor now keeps drafts as you type (browser + db `capdrafts/<key>`, `editing:true` while open), and every Save adds a permanent history entry with Restore. **Captions are editable on the hub's Posts tab** (owner only while it's shared by link; Ekshika views). Edits live in the hub db (`captions/<P0X-vN>`, history under `captions/<key>/history`) and override POSTS.md on the page. **At the start of post work, pull them back:** ArtifactData list `captions` with out_dir → `python3 -I scripts/sync_captions.py <dir>/captions --write`. If you edit a caption in POSTS.md, also write it to the db or the old hub edit keeps showing.
- **Claude Design canvas "Sayari LinkedIn Posts" (private)**: https://claude.ai/artifact/Qf9AmewWkDheDkufUh7b1n. Synced to current versions on 2026-11-11 (P02 reworked, P03 = Ekshika's design rebuilt, P04 simplified). Row 1: P01 (`P01-name-match.dc.html`), P02 (`P02-frankenstack-bingo.dc.html`), P03 (`Main.dc.html`). Row 2: P04 version 1 (files `-1C`/`-5C`), one artboard per slide (`P04-1C`, `P04-2`, `P04-3`, `P04-4`, `P04-5C`, `P04-6`). Row 3: P04 version 2's unique slides (`P04-1B`, `P04-5B`); slides 2/3/4/6 are shared. The Sayari design system is installed in the canvas. Add new posts as new artboards. (P01/P02 finals were copied from the older chat canvas "Post 1: name-match purgatory", https://claude.ai/artifact/L7KzYoX9S9Qq55GmjXHkZU, which also holds unused bingo drafts.) For hand-tweaks it becomes the post's source of truth; mirror final changes back to `content/posts/`. To edit artboards from a new chat: read the canvas files first (Artifact read), edit, publish with the canvas `url`; review with `scripts/preview_dc.py`.
- **Learning Tracker (private page)**: https://claude.ai/artifact/DxDxJRddLk96QeQcyAJ5Uz. Built from `content/feedback/LEARNING_TRACKER.md` by `scripts/build_tracker.py` → `content/feedback/tracker.html`; republish to that URL after each feedback round. Never share it, and never put it in the hub.
- **Live PWA Dashboard (Shareable)**: https://terriblyoffendedmarketer-stack.github.io/sayari/
- **Cloud Automation**: Runs every 6 hours via `.github/workflows/scheduled-sweep.yml` using GitHub Actions + Apify Secret.

## Content Roadmap (where this project is going)
- [x] **A. Foundation:** research, idea bank, strategy, voice, captions, templates list, posts log, hub, design kit (6 base layouts + renderer). Themes get validated as posts use them.
- [~] **B. Production:** make posts one at a time together (hook → format → design → caption), logging each in POSTS.md. Target: the first 5–6 images, then 3–4 a week.
- [ ] **C. A well-oiled engine:** a library of built templates and wireframes, recurring series, captions that consistently land; making a post becomes matching.
- [ ] **D. Replicable framework:** `playbook/` proven on Sayari, then reused for new companies (`playbook/ONBOARDING.md`). Don't build for D now; it emerges from doing B and C well.

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
- `playbook/`: **company-agnostic method, reused for every client.** `SPEC.md` (the content OS: layers, rules, session dialectic, continuity), `ONBOARDING.md` (5 core tasks for a new company), `PITCH.md` (how every post is pitched and pressure-tested), `CAPTIONS.md` (caption craft), `templates.md` (meme and design mechanics library).
- `content/`: Sayari's content layers. `posts/POSTS.md` = **log of shipped posts with captions and tags (read first)**. `VOICE.md` = Sayari voice. `STRATEGY.md` = the 3-month plan (arc, weekly rhythm, series, current sprint). `FRAMEWORK.md` = Sayari specifics plus 9 candidate themes.
  - `buckets/SHORTLIST.md`: the current 15-post shortlist (picked from the bank; pitch before making).
  - `buckets/IDEA_BANK.md`: **every starting point, one row each**, typed idea / insight / angle / hook (I## / H##), with gist, format, bucket, status and needs. Add new ones here, never only in chat.
  - `themes.md`: validated themes (1 so far). `sharpened/`: one file per idea after sharpening. `brand/`: Sayari logos.
  - `idea-doc-images/`: `IMAGE_IDEAS.md` (49 images catalogued), `gallery.html` (local visual gallery). `images/` is gitignored (copyrighted memes; regenerate with the extractor).
- `content/posts/archive/`: **our original versions, archived per feedback round** (e.g. `2026-11-10_round1-originals/`: P01–P04 images, PDFs, sources, captions). Never discard originals; archive before applying client edits.
- `content/feedback/`: **private learning tracker** (`LEARNING_TRACKER.md`: client feedback rounds, our version vs theirs, lessons and where each was applied) + `assets/` (their edited creatives). Not read by the hub, because Ekshika sees the hub. Log every feedback round here.
- `research/`: inputs. `sayari-site/newsjack-examples.md` = Sayari's 4 past newsjacks, full captions + caption skeleton. `icp_psychographics.md` (who the ICP is beyond work; living file, built lesson by lesson), `brief_summary.md` (the Sayari brief's rules on one page), `lexicon.md` (words practitioners actually use, plain meanings, beginner-safe flags, banned words). `sayari-site/case-studies/` (all 20 Sayari case studies, saved 2026-11-10), `sayari-site/FEATURE_MAP.md` (release notes + product pages → feature-to-case-study map, image sources), `sayari-site/OTHER_CONTENT_INDEX.md` (19 investigation briefs + 3 buyer guides, plus how to fetch), `competitors/`, `listener_audit.md`.
- `.claude/skills/sayari-content/SKILL.md`: project skill that loads the framework rules for content work.
- `design/kit/`: **design kit**. `kit.css` (tokens copied from the Sayari Design System artifact), 6 base layouts in `layouts/` (L1 search stack, L2 card grid, L3 split compare, L4 stat + source, L5 message thread, L6 story carousel), `previews/` PNGs, README with rules.
- `scripts/sync_canvas.py` + `content/posts/canvas_map.json`: renders changed canvas artboards into `content/posts/assets/` (source-hash change detection), archives replaced images to `content/posts/archive/history/<stamp>/`, rebuilds carousel PDFs.
- `scripts/export_editable.py`: editable PDFs (real text, vector shapes) of each post from the canvas → `content/posts/editable/`, for Ekshika to import into Canva; fonts cached in `design/kit/fonts/`. Hub shows an "Editable PDF (Canva)" button; published as `editable/<f>`.
- `scripts/inbox_report.py`: compact list of the hub Inbox (dumped db docs) for filing.
- `content/library/`: real-content & UGC library (`LIBRARY.md`; `assets/` gitignored).
- `content/inbox/`: filed Inbox items (`LIBRARY.md` index + `assets/`).
- `scripts/sync_captions.py`: copies captions edited in the hub (db docs dumped to JSON) back into POSTS.md.
- `scripts/build_tracker.py`: renders the private learning tracker page from LEARNING_TRACKER.md.
- `scripts/preview_dc.py`: renders Claude Design artboards (.dc.html) locally + a contact sheet laid out like the canvas, for reviewing without claude.ai sign-in.
- `scripts/render_gif.py`: renders an animated post HTML (L7) to a looping GIF + MP4 + final-frame PNG (headless Chrome frames + ffmpeg).
- `content/posts/newsjack/<P0X-slug>/`: one folder per newsjack, one file per stage (01-news, 02-why-it-matters, 03-story…).
- `content/buckets/NEWSJACK_STORIES.md`: newsjack story log (candidates per search, status).
- `content/NEWSJACK.md`: how Sayari's own newsjack posts work (GIF + digest carousel), caption pattern, our newsjack process.
- `scripts/render_post.py`: renders a post HTML to a 1080×1350 PNG (carousels: PNG per slide + PDF) via headless Chrome.
- `scripts/build_hub.py` + `content/hub/template.html`: generate `content/hub/hub.html` (the Content Hub) from POSTS, FRAMEWORK, templates, IMAGE_IDEAS, sharpened ideas, case studies and the listener DB.
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
