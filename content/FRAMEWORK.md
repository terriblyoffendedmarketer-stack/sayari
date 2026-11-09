# Sayari content framework: the foundation we build on

Written 2026-11-10 from the working session. This is the lens for every content decision. We build the foundation slowly and together; after that, making posts is mostly picking and matching.

## The bottom line (why any post exists)
The reader **stops, reads, relates, saves it, and comes away liking Sayari**, so that months later, "in the room", they suggest it. Social won't close deals; it builds that association. So we give practitioners lots of **useful, savable, relatable** material, and Sayari shows up as the relief, never the brochure.

Who we talk to (from the brief): **compliance officers / heads of financial crime, sanctions, KYB** (the Protector + the Skeptic) and **investigations & intelligence analysts** (the Optimizer + the Builder). Not CCOs or budget holders.

## The layers

```
RESEARCH (inputs)  →  1 THEMES  →  2 TEMPLATES  →  3 MEME LIBRARY  →  4 IDEA BUCKETS → IDEAS → POSTS
listener, case          patterns     meme/design     existing memes      e.g. Graphs → "chasm curve
studies, briefs,        we've        mechanics we    about the job,      of compliance" → 3 posts
competitors, news       validated    can reuse       re-said cleanly
```

### Research (inputs, keeps growing)
| Source | Where | What it gives us |
|---|---|---|
| Listener (Reddit + RSS, every 6h) | dashboard / PWA, `data/sayari.db` | How practitioners think and talk (patterns, not single words) |
| Sayari case studies (20) | `research/sayari-site/case-studies/` | Real stories, numbers, quotes (UGC) |
| Investigation briefs (19), buyer guides (3) | `research/sayari-site/OTHER_CONTENT_INDEX.md` | "Receipts" stories, Sayari's own framing of buyer pain |
| Competitors and USP | `research/competitors/` | What only Sayari can credibly say |
| The brief and the idea bank | Google Docs, `content/idea-doc-images/` | Strategy, formats, reference images |

The language filter: a **beginner** in compliance should follow it. "L1 review" and "UBO" are fine. Shorthand that only another officer at the same bank would get is not.

### 1. Themes: recurring patterns, validated
A theme is something that shows up **again and again across sources** (listener + case studies + blogs), not a one-off quote. Each theme records: the pattern in plain words, the feeling behind it, evidence (with links), which Sayari pillar/USP it serves, and a status of `candidate` or `validated`. Themes get sharper as the listener finds more. File: `content/themes.md` (we build this next, together).

### 2. Templates: meme mechanics → design templates
A meme is a **mechanic** (a reusable joke structure). One mechanic can become several clean design templates. Examples from our image dump:
- "Did you mean…" search → a fake Google search card
- Alignment quadrant (lawful/chaotic) → a typographic 2×2
- Before / during / after (the road patch) → a three-panel timeline
- Crossing-the-chasm curve, graph with a highlighted zone → graphs we can **use almost as is**, since a clean graph is already an infographic
- Calendar block, Spotify playlist, Slack thread, email → realistic fake artifacts
Each template records: the mechanic, what it's good for, design variants, and which themes fit. File: `content/templates.md`.

### 3. Meme library: what already exists about this job
Existing compliance memes (the 12 "pulse" images, and more we find). We keep the **insight** and say it in a template that suits Sayari (no raw memes for now). Catalogue: `content/idea-doc-images/IMAGE_IDEAS.md`.

### 4. Idea buckets → ideas → posts
Ideas cluster into big buckets. Each idea can produce several posts.
| Bucket | Example ideas |
|---|---|
| Graphs and data | inflection-point graphs, chasm curve, "evolution of X", sorted bars with a punchline |
| Product and dashboard screens | six tabs → one query, framed screenshots of real findings |
| Charts-as-jokes | alignment quadrant, bingo, calendar |
| Case studies as stories | ARMA, the live sanctioned vendor, PURE (OFAC) |
| Realistic artifacts | Slack "quick one", examiner email, "Did you mean" search |
| Lists and tips (saveable) | "10 shortcuts that backfire", demo questions, tips to be a better analyst |
| Newsjacks | OFAC/BIS actions, two-line takeaway |
| UGC reposts | regulator releases, Reddit/LinkedIn quotes, customer quotes, report snippets |
File: `content/buckets/` (one file per bucket as we fill them).

## Rules we apply to every idea
1. **Hook first.** The hook *is* the idea, and it tells us how to tell it. We don't bolt a hook on at the end.
2. **The best format wins; we don't pick in advance.** If each beat should top the last (e.g. "things compliance people do"), it's a carousel. If it's one sharp contrast, it's a single image. We match the story to the format.
3. **UGC wherever possible:** regulator releases, real practitioner quotes (no usernames), customer quotes from case studies, news and report snippets, dashboard screens, trends.
4. **Sayari value check:** does it serve the USP? *Source not score* (evidence over risk scores) · *ownership depth* (the risk is one hop away) · *one place instead of the Frankenstack*. If it's only funny, it isn't done.
5. **Proof gates:** no number without a source. Customer proof needs Sayari's clearance. Named enforcement cases must be public.
6. **Voice:** validating, unflinching, human and a little funny, proof-backed. No "judgment infrastructure".

## How we work a session
"Let's find more graph ideas" → I search **only** that bucket (research, templates, themes) → bring back a few strong candidates with hooks and evidence → we discuss → sharpen one → wireframe → final design (Claude Design + the "Sayari" design system). Sharpened ideas live in `content/sharpened/`.

## Tools
- **Listener** (this repo): `python run.py pipeline`; tune `config.yaml` and run `python run.py refilter`.
- **Offline corpus engine** (`~/Documents/Claude Code/Offline data analysis`): local models (Ollama: qwen2.5-coder 7B, nomic-embed) that cluster a folder of markdown into themes with verbatim-quote checks. Use it on `research/` to propose *candidate* themes; we validate them together. (Its built-in fetcher fakes a browser; don't use that on Sayari's site.)
- **Claude Design**: the Design artifact type, with the "Sayari" design system in the account.
- Scripts: `scripts/extract_doc_images.py`, `scripts/build_image_gallery.py`.

## First candidate themes (from reading all 20 case studies + the listener), to validate together
1. **"Trust but can't verify":** questionnaires and self-attestation stop at tier 1 (grocery: <50% response; telecom, tech, auto, PURE).
2. **The data assembly tax:** most of the day goes to stitching records, not judging risk (Honeywell 75/25, energy, NCA).
3. **The name passed, the owner didn't:** each party screened alone; the risk is one ownership hop away (logistics, the live sanctioned vendor, energy trader's 50% rule, PURE).
4. **Clearing false positives all day:** "a shipping company in Singapore is not a sanctioned person in Tehran" (bank 90–95%, listener's 44% thread).
5. **"An analyst checked a spreadsheet" isn't an answer:** the audit trail problem; black-box scores rejected (manufacturer, energy trader, DoD).
6. **Blind exactly where you're growing:** coverage collapses in China, LatAm, Africa (payments <50% match, Honeywell's "China blind spot").
7. **Three vendors, sixty workflows:** the Frankenstack, quantified (energy trader 3→1, energy 60 workflows, 75+ sources).
8. **Understaffed and accountable:** turnover, "quick one" asks, a cost centre noticed only when it breaks (listener).
9. **Deadline and volume crunch:** 800 vendors in 90 days, February renewals, 30-day case windows.
