# Newsjack posts: how Sayari's own team makes them (and how we match it)

Ekshika asked on 2026-11-12 for posts like four that Sayari's in-house team published (seen in Sayari's Ordinal workspace): **Earthmade** (GIF, DOJ smuggling indictment), **A7** (GIF, NYT on a Russian sanctions-evasion network), **MOFCOM** (GIF, China's proposed AI export controls) and **ICBC London Files** (8-slide carousel, ICIJ investigation). "Newsjacking posts required."

## What they have in common
- **A real, recent public story with a primary source:** a DOJ press release, an NYT/FT/ICIJ investigation or a government notice. The source link goes in the approval comments, not on the image.
- **One mechanism, explained:** *how* it happened (paperwork said X, goods went to Y; invoice said floor mats, money paid for drone parts; control changes hands without the tech moving). Not just "this happened".
- **The Sayari turn is one or two sentences at the end:** "Risk teams won't catch this by reading the invoice… they catch it in the network. That's the kind of connection Sayari surfaces." Ownership and network across borders, "250+ jurisdictions".
- **Legal hedging is built in:** "prosecutors say", "allegations in an indictment, not findings", "per ICIJ", "allegedly".
- **Timing:** 1–3 weeks from the news to the post (MOFCOM: proposed 16 Oct, posted 5 Nov). Their approval chain takes about a week, so a draft that's ready fast matters more than same-day speed.
- **Best performer: A7**, the "playbook" angle (a numbered how-to of the evasion scheme). It got about twice the impressions and shares of the others.

## Format 1: the explainer GIF (3 of 4), our layout L7
`design/kit/layouts/L7-newsjack-gif.html` → `python3 -I scripts/render_gif.py <file> --out content/posts/drafts/P0X.gif` (GIF + MP4 + final-frame PNG, ~1 min).
- Beige. Two-line Merriweather headline as a contrast: **"The [paperwork] said [A]. The [reality] went to [B]."** The two contrast words are gold italic.
- A mono kicker with the case's numbers ("ALLEGED DIVERSION · $300M+ IN GPU SERVERS").
- A white card split in two. Left: **what the paperwork or name screen showed** (form fields plus a green "✓ No match / Signed" chip). Right: **what was actually behind it**, a node chain that appears one step at a time and ends on a **red node + red chip** ("License required", "Under sanctions") or a red rubber stamp ("REGISTRATION REQUIRED").
- About a 10–12 s loop: the headline arrives line by line, the card fills, nodes build, then a ~3 s hold on the final state.
- Variant (MOFCOM): one node swaps (Chinese owner → foreign buyer) and a field flips colour. Use it for "a rule changed" stories.

## Format 2: the investigation-digest carousel (ICBC)
- 8 slides: cover (big number + folder icon, "7 cases flagged") → 2 cases per slide, each with a gold kicker pill ("CASES 1 & 2 OF 7 · SANCTIONS"), a headline with one gold italic word, a navy panel with icons or bars, and a 2-line italic summary → "What to ask your team" → **a real screenshot of the source article with a hand-drawn gold arrow** ("Read the full investigation").
- Use for long reports (ICIJ, NYT, a Senate report): "a 26-minute read, digested in a minute".
- Build with L6 (carousel) + the real-content frame rule in `design/kit/README.md`.

## Captions
- **Their captions are a reference, not a rule** (user, 2026-11-12). We may beat them; if not, they become the rule.
- **Full verbatim captions + skeleton:** `research/sayari-site/newsjack-examples.md`.
- **Theirs run long (240–440 words):** a cold open on the most concrete detail → "X just reported…" → a numbered 1–7 breakdown → one extra striking detail → "the questions for risk teams are:" → the Sayari line → sometimes a closing question.
- **Confirmed (user, 2026-11-12):** ~240–440 words is right for newsjacks, because explaining the news is the value. The creative also carries more words than other posts. It's still not a reading slog: numbered steps, short lines, one mechanism. The GIF's movement adds the interactivity.
- **Spacing:** newsjacks aren't continuous. Run them when a good story lands, between the regular posts.

## Mode and flow (2026-11-12)
- Sayari wants **newsjacks only, for now**. Evergreen work isn't retired; it's banked.
- **Flow:** Sayari sends the story → we read the primary source → pick GIF or carousel → pitch → build → caption.
- **For now, use only their two formats.** Later (not yet): prep more newsjack formats so the feed doesn't look repetitive, e.g. a timeline GIF, a single-stat card or a regulator-document annotation.

## How Sayari builds them
In **Canva**: an animated design downloaded as a GIF (Canva animates elements and pages and exports GIF/MP4). Their PDF export of the Earthmade design (2 versions, the second adds a "$176M+ paid…" callout box) is in `content/library/assets/sayari-examples/` (gitignored). L7 matches it: wordmark top right, no bottom takeaway, optional callout.

## Our process for one newsjack (user, 2026-11-12: decoupled stages, one at a time, agree before moving on)
One-shotting (article → angle → image in one go) skipped the thinking. Each stage gets the user's OK before the next.
1. **Understand the news.** Read the article and the primary sources. Explain plainly what happened, who did what, what's confirmed and what's alleged. No Sayari angle yet.
2. **Why it matters.** Why it matters to our ICP (risk, compliance and trade teams) and why it matters to Sayari.
3. **Define the story from Sayari's side.** Agree the one story (the trick or claim, the link to Sayari, the hedges) before any design.
4. **Make the creative: a GIF or a carousel, built new for this story.** Don't copy Sayari's example GIF layout (P05 v1 looked like a copy). Carousels can flex more.
5. **Caption.** Sayari's example captions are a reference, not a rule.

**No templates for now.** Make each post fresh. Templates come later, as the outcome once enough posts exist.

## Lessons from P05 (Binance, 2026-11-12): use these on every newsjack
**Process**
- Run the stages, one file each, in `content/posts/newsjack/<P0X-slug>/` (01-news → 02-why-it-matters → 03-story → 04-creative → 05-caption), with the user's OK between stages. The one-shot v1 skipped the thinking and copied Sayari's template.
- Read the primary sources first: the company's own statement or post-mortem, the government notice, the tracing firms. Press coverage changes the facts (the fake job interview only appeared in Binance's post-mortem).

**Finding the link to Sayari**
- The news topic is rarely Sayari's ground (crypto, AI, chips). Look for the **company-level fact**: the companies, owners and controllers the story runs through, and where they land in a compliance team's day (onboarding queue, payments, supply chain).
- The strongest link makes Sayari the **second half of the story** ("the money has to move through people and companies… Sayari shows who's behind them"), not a line bolted on at the end.
- Check Sayari's partners before framing (Chainalysis is a partner): complement, never "they can't, we can".

**Accuracy (the user wants to be corrected on all of these)**
- Attribution ≠ proof: "The FBI says North Korea…", never "North Korea stole…".
- Keep who said what: the UN's 40% figure is "one member state", cited in a UN panel report. North Korea hadn't denied *this* hack ("has denied similar accusations before").
- Don't quote moving estimates that sources use inconsistently ($2.85bn was "frozen" in one, "with the attacker" in another).
- Never import an old case as the spine (v2's 2023 Treasury chain read heavy and borrowed).

**Caption (the user's final shape, ~200 words)**
Hook (the news, attributed) → "If you work in sanctions, KYB or financial crime, it's your problem too." → why it reaches your desk → "Here's what we know so far" (2 arrows, only what matters to compliance) → the stakes (sourced) → the question on its own line → what answering it takes today (the human pain line) → Sayari, woven in, **no "Where Sayari fits" heading**. No closing CTA question this time.
- Cut anything that only matters to the exchange's customers or crypto insiders (Binance covering losses, who froze what, how the hack worked).
- Avoid AI signposts and patterns: "Here's why it matters:", double colons, "it's not X, it's Y".

**Creative**
- It must work **without the caption**: the news is the big headline (attributed); the consequence is a smaller subline; the image shows the reader's own screen (native UI) and ends on one question.
- Trim with hierarchy (size), never by demoting the line that carries the news into a small kicker.
- No blank first frame: the message is on screen from frame 0; animate only the part that tells the story.
- Don't copy Sayari's example GIF layout; build new for each story. Use invented company names; "front company", not "shell" (a shell is empty, a front looks real).
- Deliver: GIF (`scripts/render_gif.py`) → `content/posts/assets/<P0X>-final.gif/png` → artboard on the Claude Design canvas → editable PDF for Canva (`scripts/export_editable.py <canvas-dir> <P0X>`).

**Hub**
- Before any hub publish, check `capdrafts`; never publish while `editing:true`. Send previews as files, not hub republishes.
