# Listener audit (2026-11-09)

Snapshot: 249 items in `data/sayari.db` (after pulling the latest cloud sweep). **155 are marked "kept".**

## Where the 155 kept items come from

| Bucket | Kept | Verdict |
|---|---|---|
| Core subs (r/AMLCompliance, r/financialcrime, r/compliance) | 60 | **Signal.** This is the real practitioner voice. |
| r/FinancialCareers (targeted thread) | 41 | **Mixed.** Mostly career chat ("should I go into compliance", salaries), plus traders mocking compliance. About 10 are useful *identity* signals ("cost centre", "only noticed when it hits the fan", "many systems stitched together"). |
| RSS news (Steptoe, FiveBy, Compliance Week) | 29 | **Different job.** Good for newsjacks, but it's lawyer and editor voice, not practitioner voice. Shouldn't feed the lingo or pattern view. |
| Off-topic subs | 12 | **Noise.** r/deinfluencingPH ("swivel chair" = a nursing chair), r/ModernHiring ("backlog" = recruiting), r/conspiracy, r/antiwork, r/PakistaniTech (consumer asking "why am I on the AML list"), r/scrapingtools (a vendor listicle). |
| Adjacent subs (r/fintech, r/business) | 11 | **Useful edge signal.** Founders asking "do I just search the OFAC site by hand?" This was the source of idea #4. |
| `manual:sample_manual_reviews.csv` | 2 | **Fake seed data.** "We get 400 false positives a day…" is an invented sample, yet the brain dump labels it an "authentic practitioner term". It must go. |

**Roughly 35 to 40% of the "kept" pile is noise or the wrong voice.**

## Why the noise gets in

1. **Cross-Reddit keyword search** (`src/collectors/apify.py:295`, e.g. "sanctions screening backlog") searches *all* of Reddit. Generic words in the results ("swivel chair", "backlog") then match seed keywords.
2. **One generic keyword is enough to pass** (`src/filters.py`). Seed list includes `audit`, `screening`, `queue`, `backlog`, `alerts`, `investigation`, `surveillance`, `spreadsheet`, `settlement`, `burnout`, `turnover`, `back office`. Any one of these passes an item, with no check on *who* is talking or *where*.
3. **The subreddit name counts as a keyword** (`filters.py`, `source_words`). Anything from r/compliance or r/AMLCompliance auto-matches "compliance", so even "Thanks man" passes.
4. **No speaker check.** Nothing separates a practitioner from a student, a trader, a vendor, a consumer, or a journalist.
5. **News and practitioner talk share one pile**, so headline words (OFAC, TPRM) inflate the "lexicon".

## Why the output isn't useful for creative work yet

- `ideas.csv` is template-filled: "The Practitioner Reality of The Reality Gap: Vendor Promises vs Practitioner Daily Grind…", with an invented "45 minutes per vendor" stat. The ideas come from keyword counts, not from understanding.
- The "lexicon" reports **words**. What we need is **thinking patterns**: what they believe, fear, joke about, and blame, and the recurring situations they describe.
- There's no **accessibility check**. "L1 review" and "UBO" are fine (a beginner can follow), but deep in-group shorthand that only one other officer would get isn't.

## ⚠️ Public-exposure issue (needs your call)

The repo and the GitHub Pages site are **public**. The confidential proof points (72% telecom, 1.2M records, 75+ sources, top-5 tech) are in:
- `config.yaml` → `customer_proof_points` (labelled "approved_for", but they are not approved yet)
- `reports/claude_dump.md` → "SAYARI VERIFIED PROOF ANCHORS", which the live dashboard serves

Fix options: move them to a gitignored local file and scrub them from the dump/site going forward. Old commits keep them unless history is rewritten, so tell Sayari if that matters. Alternatively, make the repo private (GitHub Pages on a private repo needs a paid plan).

## Fixes (proposed, not yet applied)

1. **Source allowlist with tiers**: core subs = practitioner voice; adjacent subs (fintech, business, smallbusiness, FinancialCareers) = edge voice, but only items that pass an LLM relevance check; cross-Reddit keyword hits = drop unless the subreddit is on the allowlist; RSS = a separate **news lane** that never feeds the pattern or lingo view.
2. **Remove the subreddit-name keyword bonus.** Require either 2+ seed terms or 1 *specific* term (ofac, kyc, ubo, false positive, name match, sanctions…). Generic terms only count in combination.
3. **LLM judge per item** (cheap model): who is speaking (practitioner / student / trader / vendor / consumer / journalist), is it about the actual work, what's the underlying thought, and a 1–5 accessibility score. Keep only practitioner and edge voices about the work.
4. **Delete the fake seed CSV** from inputs and from the dump.
5. **Pattern extraction instead of a word list**: cluster kept items into recurring *situations* ("the same name with no DOB", "the auditor asks why", "the manager says quick check", "we're a cost centre") with frequency, emotion, and 2–3 paraphrased examples each. The idea engine reads these.
