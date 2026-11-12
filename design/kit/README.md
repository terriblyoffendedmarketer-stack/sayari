# Sayari design kit (base layouts)

Starting points for every post, in Sayari's own design system (tokens copied from the "Sayari" Design System artifact: https://claude.ai/artifact/LeM3wtgJYhXNR8hC3GyhG2). Copy a layout into `content/posts/drafts/`, swap the content, render, and refine there or in Claude Design.

| Layout | Mode | Use for | Template mechanic |
|---|---|---|---|
| `L1-search-stack.html` | navy | Screening-result / name-match pain (P01's look) | Stacked search bars / "same?" |
| `L2-card-grid.html` | beige | Bingo, checklists, "things nobody warns you", archetypes (P02's look) | Bingo card, numbered list, archetype cards |
| `L3-split-compare.html` | beige | Product-as-relief contrasts: questionnaire vs record, before vs after, claim vs source | Before/after split |
| `L4-stat-source.html` | navy | One sourced number (receipts, newsjacks) | Big stat + source |
| `L5-message-thread.html` | navy | Realistic fake Slack / email / auditor chat | Realistic chat/email |
| `L6-carousel-story.html` | navy/beige alternating | Receipts: a real case told as setup → trap → move → result → rule | Story carousel |
| `L7-newsjack-gif.html` | beige, **animated** | Newsjacks: "paperwork said A, reality was B" explainer GIF (Sayari's own newsjack format; see `content/NEWSJACK.md`) | Builds step by step → red end node |

Previews (rendered PNGs) are in `previews/`. Example text comes from real ideas in the idea bank (L3 = idea I05, L6 = idea I04), so they double as first wireframes.

## Rules baked in (from the design system)
- One mode per image (navy or beige). Across the feed (and across carousel slides), vary modes with intent: alternating is the default, but two of the same back to back is fine when there's an organic reason. Strict alternation everywhere gets monotonous too, so don't force it either way.
- Gold (`accent`) once per image: a key word, the annotation, or one tag.
- One handwritten `scrawl` phrase per image at most.
- Nothing under 26px on the 1080×1350 canvas. Left-aligned. 80px side margins.
- Product, search, alert and chat mocks always sit in the dark `panel`.
- Small wordmark in one corner (white on navy, navy on beige).
- **2-second test (client feedback, 2026-11):** someone with zero context gets the image in 2 seconds.
  - **Headline = the conclusion in plain words**, not a riddle or formula ("Two 'clean' 25% owners don't make a clean company", not "25% + 25% = …").
  - **Show the logic visually:** stamps/labels ("TAKING THEIR WORD FOR IT"), boxes that add up into a result bar, arrows. Never a sentence where a visual device can say it.
  - **State the consequence to "you"** ("Result: 50% blocked. You just onboarded a violation.").
  - **End on a one-line takeaway** at the bottom, so the image works without the caption.
  - **Cut metadata noise** (section numbers, "registry record ·", dates) unless it carries meaning.
  - Risk red can be used boldly when it carries the meaning (stamp, result bar).
  - Reference: P03 final (Ekshika's edit) in `content/feedback/assets/P03-final-ekshika-edit.jpg`.
- **Never put a disclaimer on an image**: no "illustrative", "invented", "fictional", "example" or "for illustration" lines. Sources and caveats go in the caption or the first comment.
- A `source` line on the image is only for a **real, public source behind a number that is the point of the post** (e.g. an OFAC settlement amount). Otherwise leave it off.

## Real content inside the frame (variety rule, 2026-11-11)
- Real screenshots (product UI, regulator releases, social posts, emails, Slack) **keep their native colours** (white UI, blue links, platform greens/reds). Don't recolour them navy/beige; the contrast is the visual break.
- The **frame stays Sayari**: navy or beige background, Merriweather headline, wordmark corner. The screenshot sits on it as a card (rounded corners, soft shadow), cropped to the one part that makes the point.
- Gold still marks one thing: a highlight box, circle or scrawl on top of the screenshot.
- Crop out personal data (avatars, emails, usernames). Rebuild social posts rather than screenshotting real accounts.
- Library of usable real content: `content/library/LIBRARY.md`.

## Kit vs Claude Design
The kit is the master for building and rendering. When a post needs hand-tweaking, it also goes onto the Claude Design canvas "Sayari LinkedIn Posts" (https://claude.ai/artifact/Qf9AmewWkDheDkufUh7b1n) as an artboard with inline styles. Once tweaked there, the canvas is that post's source of truth; export the final image from it and save it to `content/posts/assets/`.

## Render
```bash
python3 -I scripts/render_post.py design/kit/layouts/L3-split-compare.html --out content/posts/drafts/P03.png
```
```bash
python3 -I scripts/render_post.py design/kit/layouts/L6-carousel-story.html --slides 5 --pdf --out content/posts/drafts/P04.png
```
The carousel gets one PNG per slide plus a PDF (LinkedIn's carousel format).
```bash
python3 -I scripts/render_gif.py design/kit/layouts/L7-newsjack-gif.html --out content/posts/drafts/P05.gif
```
Animated layouts get a looping GIF + MP4 + a PNG of the final frame (timing comes from the layout's `<meta name="gif">`).

## Gotchas
- Fonts come from Google Fonts: render with internet on, or text falls back to Georgia/system fonts.
- Grids use `minmax(0,1fr)` so a long word (like a filename) can't stretch one column; long mono strings may need a manual break.
- The canvas has 160px bottom padding so content clears the wordmark. Keep big scrawls above that line.
