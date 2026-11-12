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

## Lessons from P05 (Binance, 2026-11-12; corrected by the user): use these on every newsjack
**The lens, always:** how does this connect to Sayari and the people who use it?

**Process: stages, one file each** in `content/posts/newsjack/<P0X-slug>/`, with the user's OK between stages.
1. **Understand the news (01).** Read it properly, primary sources first. Explain what happened so a layperson with no compliance background gets it. Already start noticing where it touches Sayari.
2. **Why it matters (02).** Hunt for the **strongest** connections to Sayari's users. Often the headline won't obviously connect to Sayari at first glance; that's exactly why this stage exists. News that sits directly in compliance is even more valuable. **Name the ICPs each angle serves** (compliance officers, heads of financial crime, sanctions and KYB teams, investigators and intelligence analysts, third-party/supplier risk, trade compliance, risk assessment), not just "compliance teams": the user wants exposure to the clientele, even if posts later use a collective term.
3. **Story (03)** → 4. **Creative (04)** → 5. **Caption (05)**.
- Check Sayari's partners before framing (Chainalysis is one): complement, never "they can't, we can".

**Accuracy (correct the user on any of these)**
- Attribution ≠ proof: "The FBI says North Korea…", never "North Korea stole…".
- Keep who said what: the UN's 40% figure is "one member state", cited in a UN panel report. North Korea hadn't denied *this* hack ("has denied similar accusations before").
- Don't quote moving estimates that sources use inconsistently.
- Don't import an old case as the spine.

**Caption writing** (P05's shape is submitted, not validated, so it isn't a rule yet)
- **Clarity over everything.** P05's drafts had clarity issues; fix those first.
- **Active voice, punchy, journalistic with an op-ed edge.** The hook moved from "Binance says $6.3bn in digital assets were hit…" to "$6.3bn stolen from Binance…": the first four words carry it.
- No AI signposts or patterns ("Here's why it matters:", double colons, "it's not X, it's Y").
- Cut what only matters to the company's customers or insiders.

**Creative (a minimum, not a template)**
- The image must not be pointless without the caption: the headline makes sense on its own and doesn't orphan the news.
- It shows why it matters to the reader, where the news meets Sayari, not every fact in the post (that bloats it). P05: the news (the theft) + where it goes next (companies that look like your customers).
- Trim with hierarchy (size), never by demoting the news line. No blank first frame. Don't copy Sayari's example GIF; build new for each story. Invented company names; "front company", not "shell".
- Deliver: GIF (`scripts/render_gif.py`) → `content/posts/assets/<P0X>-final.gif/png` → canvas artboard → editable PDF (`scripts/export_editable.py <canvas-dir> <P0X>`).
