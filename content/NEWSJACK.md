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
- **Theirs run long (240–440 words):** a cold open on the most concrete detail → "X just reported…" → a numbered 1–7 breakdown → one extra striking detail → "the questions for risk teams are:" → the Sayari line → sometimes a closing question.
- **Confirmed (user, 2026-11-12):** ~240–440 words is right for newsjacks, because explaining the news is the value. The creative also carries more words than other posts. It's still not a reading slog: numbered steps, short lines, one mechanism. The GIF's movement adds the interactivity.
- **Spacing:** newsjacks aren't continuous. Run them when a good story lands, between the regular posts.

## Our process for one newsjack
1. **Find:** DOJ/OFAC/BIS/Commerce releases, ICIJ/NYT/FT/Reuters investigations, MOFCOM or EU notices from the last 2 weeks. Read the primary source.
2. **Pick the mechanism:** can it be drawn as "paperwork vs reality" (GIF) or as "N cases" (carousel)? If neither, skip it.
3. **Pitch** in the PITCH.md format, with the source link and the hedges.
4. **Build** with L7 or L6, render, then caption.
