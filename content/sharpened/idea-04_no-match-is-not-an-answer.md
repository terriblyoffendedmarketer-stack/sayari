# Idea 4, sharpened: "No match found" is the start of the question (post 4 pitch)

**Core truth:** a sanctions-list search checks a *name*. The 50% rule is about *owners*. A company owned 50%+ by sanctioned people is blocked even if its own name is on no list, and OFAC keeps no public list of those companies.

## 1. What the idea is
From the idea doc (tab "4", "The SDN search is a name lookup, not an ownership lookup"), picked by Ekshika. The original was a single image: a search box saying "No match found" with a faded "who owns it?" chain behind it. Sharpened, it becomes a **true story told as a carousel**, using a real US Treasury (OFAC) penalty:
- **PURE**, a US insurer, settled with OFAC on 21 Dec 2023 for **$466,200**.
- In **2010** a client questionnaire named the *sole shareholder* of a Panama company, Medallion: Viktor Vekselberg.
- In **April 2018** Vekselberg was sanctioned. From that day Medallion was blocked too (50% rule), but Medallion's own name was on no list.
- PURE kept insuring it: **39 violations** across four policies, May 2018 to July 2020. The ownership info sat in their files and never reached their screening.
- OFAC also noted PURE never reviewed its screening after the 50% rule was expanded in 2014.

## 2. Why they'd relate
Every analyst has run a name search, seen "no match", and felt relieved. This story is the nightmare version of that relief. And the twist is painfully familiar: the answer was **in their own files**, in a different system from the one doing the screening. That's the swivel chair / Frankenstack in one real case. Nobody was careless in an obvious way; the information just never met.

## 3. Is it real?
Fully. Every fact is from OFAC's own settlement release (amount, dates, 39 violations, the 2010 questionnaire). It's a named, public enforcement action, which the brief explicitly endorses as story material. It also matches Sayari's case studies: the energy trader flags "OFAC 50 Percent Rule exposure: ownership-based restrictions invisible to list screening", and an energy company found a live sanctioned vendor through an ownership chain its legacy tool missed.

## 4. Strategy fit
- Content type: **receipts** (the brief's strongest format; we have 0 so far).
- Pillars: *the risk hiding in plain sight* + *a score is not a defense*. Theme: **the name passed, the owner didn't** (validated).
- Pairs with P03 (the 50% rule explained with a mock) by showing the same rule with a real penalty.
- Note: the brief wants a **named Sayari analyst's face** on receipts. This is a public case, not a Sayari investigation, so a face is optional here.

## 5. Product fit
Good, with one honesty limit. Sayari's point is **ownership-aware screening with the source attached**: the owner's designation and the company it owns are linked in one record, and Signal watches for ownership changes against new designations (energy trader case study). That's precisely the gap PURE fell into.
Possible ending: "A name search tells you if the name is on a list. Ownership tells you if the company is." Then a soft line about connecting the ownership record to the screen.
Limit: we must not claim Sayari would have caught PURE's specific case (we don't know its data covered Medallion). Talk about the gap, not a counterfactual.

## 6. Hooks (one per option; my pick at the end)
- **A. "In 2010, a client told them exactly who owned the company."** A story opener that creates suspense; the reader swipes to find out what went wrong.
- **B. "The answer was in their own files."** Leads with the twist. Lands because everyone has information stuck in a system the screening never sees; instant recognition, a little dread.
- **C. "'No match found.' 39 times. Then a $466,200 penalty."** Numbers as the punch. Stark and scroll-stopping, but colder and more fear-led than our voice usually is.
- **D. "A clean name search is the start of the question, not the answer."** The lesson as a contrarian line. Clear and useful, but it gives away the payoff, so there's less reason to swipe.
**My pick: B.** It's the most relatable and the most "us": not fear, but recognition ("that could be our setup"). It also sets up the Frankenstack point without saying the word.

## 7. Format and proof
- **Story carousel, 5–6 slides**, kit layout **L6** (a wireframe already exists): cover → 2010, the form → 2018, the designation → the screen, "no match" ×39 → the receipt, $466,200 → the lesson.
- UGC/proof: a screenshot of OFAC's settlement release on the receipt slide (a real public source line is allowed there); the OFAC link in the first comment.
- Checks: facts re-checked against OFAC's PDF before posting; factual tone about PURE (no mocking a named company); naming Vekselberg is fine (public SDN designation).

Sources: [OFAC PURE settlement](https://ofac.treasury.gov/recent-actions/20231221_33) · [OFAC 2023 enforcement chart](https://ofac.treasury.gov/civil-penalties-and-enforcement-information/2023-enforcement-information) · [Meshkat Law on 50% rule enforcement](https://meshkatlaw.com/ofacs-enforcement-of-the-50-percent-rule/)
