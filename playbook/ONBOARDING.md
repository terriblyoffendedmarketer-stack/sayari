# Onboarding a new company (repeatable)

Copy this repo's `playbook/`, `scripts/` and the listener code (`run.py`, `src/`, `config.yaml`, `.github/workflows/`) into a new folder. Empty `content/` and `research/`. Then run the five core tasks **in order, together** (a session or two each). Each task ends with a file, not a chat message.

## Task 1: Read the brief and the company
- Read the client brief, the website, existing social, decks.
- Output `research/company.md`: what they sell, products, proof points (and which are cleared), what they must never say.

## Task 2: Find the real ICP
- Who actually moves on social (practitioners vs budget holders)? What's their day like, what do they fear, joke about, blame?
- Output `research/icp.md`: 1–2 personas in their own words, the feelings, the beginner-language level.

## Task 3: Find the real USP and the competitive gap
- Competitors' positioning, voice, and what they structurally can't say.
- Output `research/competitors/<company>_usp_competitors.md`: the USP in plain words, the gap we own, the competitor names we never use in posts.

## Task 4: Set up the listener (the pulse)
- Discover subreddits, forums, news feeds and blogs where the ICP talks (`python run.py discover`); the human approves sources.
- Edit `config.yaml`: `source_tiers` (core = practitioner voice, adjacent = edge voice), `specific_terms` / `generic_terms`, drop patterns.
- Run `python run.py pipeline`, check `refilter` output for noise, and repeat until the kept items are ~all real practitioner talk.
- Pull the company's own case studies / reports into `research/<company>-site/`.

## Task 5: Build the library
- **Themes:** propose candidates from the research (optionally run the offline corpus engine over `research/`), validate together → `content/themes.md`.
- **Templates:** start from `playbook/templates.md` (generic mechanics), add industry-specific ones.
- **Memes:** collect existing memes about the ICP's job → keep the insights in the meme library.
- **Buckets:** seed `content/buckets/` with the first ideas, hooks first.
- **Voice:** `content/VOICE.md`, the client's personality on top of `playbook/CAPTIONS.md`.

Then the loop starts: pick a bucket → sharpen an idea → wireframe → design → caption → log in POSTS.md.
