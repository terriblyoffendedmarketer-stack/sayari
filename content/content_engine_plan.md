# Content engine plan: from listener to approved images, mostly automated

Goal: a constant supply of hyper-relevant post ideas, each with a wireframe, so the team approves ideas and doesn't have to start from a blank page. Target: about 90% automated, with a human approving at two gates.

Not memes: "cleaned-up memes" means the *situation and joke* of a meme, rebuilt as realistic artifacts, typographic cards, charts and carousels in Sayari's brand. That's its own category: it reads as funny because it's true, not because it's a template.

```
 LISTEN ──► UNDERSTAND ──► IDEATE ──► WIREFRAME ──► [GATE 1: approve] ──► FINAL DESIGN ──► [GATE 2: sign-off] ──► POST
 (Reddit,    (who's talking,  (situation   (HTML template      review board         Claude Design         copy + visual
  RSS)        what pattern)    × format)    → PNG, low-fi)      approve / reject /    'Sayari' system,      + caption
                                                                 note                  carousel PDF
        ▲                                                            │
        └──────────── rejections + notes re-weight what gets generated next ┘
```

## Stage 1: Listen (exists; needs the audit fixes)
Apply `listener_audit.md` fixes: source tiers, stricter keyword logic, LLM judge per item, delete the fake seed data, split the news lane from the practitioner lane.

## Stage 2: Understand → `patterns.json` (new)
Cluster judged items into **situations**, not words. Each pattern has:
- `situation`: "Same name, no DOB, clear it by EOD"
- `belief / feeling`: "I'm accountable for a call I can't prove"
- `frequency`, `sources` (trace IDs), 2–3 paraphrased examples (no usernames, ≤25 words)
- `lingo`: the terms actually used, each with an **accessibility score 1–5** (5 = a layman gets it; 3 = a beginner in compliance gets it, e.g. "L1 review", "UBO"; 1 = only insiders). **Posts may use level ≥3 only.**
- `pillar` fit (Frankenstack / Score ≠ defense / Hidden risk) and `news hook` if any

## Stage 3: Ideate → idea cards (new, replaces `src/ideator.py` templates)
Inputs: `patterns.json` × **format library** (the ~30 layouts from `IMAGE_IDEAS.md` + the brief's 4 formats) × pillars × **done list** (posts already made: name-match, bingo) × mix targets (35/25/20/20).

Each idea card: title, format, pillar, pattern it comes from (with trace IDs), hook line, on-image text, slide plan if carousel, caption draft, "beginner test" pass/fail, clearance needs (e.g. "needs cleared product screen"), and a novelty check against the done list.
Volume: about 20 new cards per run, with near-duplicates of approved or rejected ideas removed.

## Stage 4: Wireframes (new)
**Bulk wireframes come from HTML/CSS templates, rendered to PNG with headless Chrome.** One template per format (calendar, dialogue card, typographic list, alignment quadrant, before/after split, ownership-chain carousel, search-bar "Did you mean", bingo, archetype cards…), all in Sayari tokens (navy/beige/gold, Merriweather/Inter/JetBrains Mono, 1080×1350).
Why templates and not AI image generation: text must be exact (fake artifacts live or die on legible, believable copy), it costs nothing per image, every image is on-brand, and it's fast enough for 50+ a day.
AI image generation is only for photoreal props (e.g. the red-string corkboard), and only after approval.

## Stage 5: Review board, Gate 1 (new)
A page showing wireframe + hook + caption + source pattern, with **Approve / Reject / Note**. Notes like "funnier", "too niche", "use a different company name" feed back into the next run (rejected patterns and formats get down-weighted; approved ones spawn variants).

## Stage 6: Final design, Gate 2
Approved ideas → hi-fi version in **Claude Design** (Design artifact type + the 'Sayari' design system already in your account), or the same HTML template at full fidelity for simple cards. Carousels export as PDF for LinkedIn.

## Automation and cadence
- Listener: every 6h (already running on GitHub Actions).
- Understand + Ideate + Wireframe: daily or twice a week, as a batch.
- Human time: about 10 min per batch at Gate 1, plus final sign-off.

## Build order
1. Listener fixes + LLM judge + `patterns.json` (the foundation; everything downstream depends on clean input)
2. Format template library (start with 8 formats from the top picks) + PNG renderer
3. Idea generator v2 + done list + novelty check
4. Review board + feedback loop
5. Scheduling

## Decisions needed
- Which LLM runs the judge and ideation in the cloud: Claude API key as a GitHub secret (fully automatic), or batches run from Claude Code (no extra key, but they only run when you or I trigger them)
- Where the review board lives: private claude.ai page with shared approve/reject state (you and Ekshika can both vote), or a local page
- The public-repo exposure of the proof points (see `listener_audit.md`)
