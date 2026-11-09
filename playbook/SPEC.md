# Content OS spec: how we run social for a B2B company

Company-agnostic. This folder (`playbook/`) gets copied to every new client project; the client-specific version lives in `content/`. Sayari is client #1.

## The goal
Build a well-structured library of **themes, templates, memes, ideas, references and past posts** for a company, so that making a post becomes a **matching problem**: the right theme + the right template + the right proof + a hook with personality. No bloat: every item is tagged and findable, and new ideas get added to the right place.

Bottom line per post: the reader **stops, reads, relates, saves it, and comes away liking the brand**, so they suggest it "in the room" later.

## The stack (same for every client)
```
RESEARCH ─► THEMES ─► TEMPLATES ─► MEME LIBRARY ─► IDEA BUCKETS ─► IDEAS ─► POSTS (log)
inputs      validated  reusable     what already    graphs, stories,  hooked     shipped, tagged,
(listener,  patterns   mechanics    exists about    lists, artifacts  ideas      with captions
case        in the     (generic,    the ICP's job                                + results
studies,    ICP's      shared                                                    
news)       world      across                                                   
                       clients)                                                 
```
| Layer | Lives in | Reusable across clients? |
|---|---|---|
| Research | `research/` | No (company + industry specific) |
| Themes | `content/themes.md` | No |
| Templates (meme and design mechanics) | `playbook/templates.md` | **Yes**: the quadrant, "Did you mean", before/during/after work for any industry |
| Meme library | `content/idea-doc-images/` | Mostly no (industry memes) |
| Idea buckets → ideas | `content/buckets/` | The bucket *types* yes, the ideas no |
| Sharpened ideas | `content/sharpened/` | No |
| Posts log | `content/posts/POSTS.md` | No |
| Caption craft | `playbook/CAPTIONS.md` | **Yes** (the client's voice goes in `content/VOICE.md`) |
| Design kit | `design/kit/` (kit.css + base layouts + `scripts/render_post.py`) | **The structure, yes**: swap kit.css tokens and the logo for a new client |

## Rules for every idea
1. **Hook first.** The hook is the idea and decides the format. We never bolt one on at the end.
2. **The best format wins.** Carousel when each beat tops the last; single image for one sharp contrast; we never preset it.
3. **UGC wherever possible:** regulator or government releases, real practitioner quotes (no usernames), customer quotes, news and report snippets, real dashboards.
4. **Brand value check:** does it serve the company's USP or competitive edge? Funny alone isn't done.
5. **Proof gates:** no number without a source; customer proof needs client clearance.
6. **Hyper-relevant and relatable, not hyper-niche.** The listener is for understanding the landscape, not for copying rare jargon. A word or situation goes in a post only if it **recurs across many people/sources** (a pattern), in the **most widely shared phrasing**, so a beginner in the field gets it and nobody feels shut out. Single niche comments are context, never copy.
7. **Simulated data looks real:** when a mock image needs names, numbers or labels, pull them from the research layer (real lingo, real situations, realistic figures), not generic filler.

## How a session works (the dialectic)
We learn and decide together. The human stays on top of the work, so:
- **Short turns.** At most 2–3 suggestions at a time, each with a one-line "why". Never a wall of text the human would skim and rubber-stamp.
- **I propose, you push back.** I give an opinion and my reasoning; you pick, reject or redirect.
- **Scoped asks stay scoped.** "Suggest graph ideas" → I search only the graphs bucket (plus the research that feeds it).
- **Starting cold** ("let's make 4–5 posts"): I read `content/posts/POSTS.md` first, look at what we've posted (formats, pillars, themes), and propose a short **macro angle** for the batch plus 2–3 first picks, with reasons.
- **Idle time:** when nothing is pending, I can prepare wireframes and variants for templates we've validated, so ideas have a visual starting point.

## Continuity across chats (no bloat)
- `CLAUDE.md` = status + file map (short index).
- `playbook/` = how we work (this file, onboarding, captions, templates).
- `content/` = the client's living library. Every new idea, theme or template gets added to its file, tagged, not left in chat.
- `content/posts/POSTS.md` = the source of truth for what shipped.
- `.claude/skills/<client>-content/SKILL.md` = loads the rules at the start of content work.
- **Content Hub** = a private page generated from these files (`scripts/build_hub.py`). Rebuild and republish it whenever the library changes, so the human can browse everything visually.
- Done when: a new chat can read CLAUDE.md → SPEC → POSTS and continue without asking what happened.

## Quality bar for a finished post
Hook works in the first line (scroll test) · the image is understood in 2 seconds · it uses something real (UGC/proof) or is a precise simulation · the caption has personality (see CAPTIONS.md) · it passes the brand value check · sources noted · logged in POSTS.md with tags.
