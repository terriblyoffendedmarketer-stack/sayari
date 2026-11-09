---
name: sayari-content
description: Use when working on Sayari LinkedIn content in this repo — finding themes, templates, ideas, sharpening a post, or researching for one. Loads the content framework and working rules.
---

# Sayari content work

1. Read `content/posts/POSTS.md` (what shipped) and `content/STRATEGY.md` (where we're heading), then `playbook/SPEC.md` (the method and session rules) and `content/FRAMEWORK.md` (Sayari specifics). For captions: `playbook/CAPTIONS.md` + `content/VOICE.md`.
   Together they define the layers (research → themes → templates → meme library → idea buckets), the rules (hook first, the best format wins, UGC wherever possible, the Sayari value check, proof gates) and the language filter (a beginner in compliance should follow it).
2. Work **one bucket or one idea at a time**, with the user. Bring back a few strong candidates, not long lists. The user reads everything, so keep it short.
3. Where things live:
   - Research inputs: `research/` (brief_summary.md, lexicon.md, case studies in `research/sayari-site/case-studies/`, an index of other site content, competitors, the listener audit)
   - Listener data: `data/sayari.db` (use only `passed_filters=1`; the practitioner lane is the core subreddits)
   - Idea bank (all ideas, tagged): `content/buckets/IDEA_BANK.md`. Add new ideas as rows, never only in chat.
   - Content layers: `content/themes.md`, `playbook/templates.md`, `content/buckets/`, `content/sharpened/`, `content/idea-doc-images/IMAGE_IDEAS.md`
   - Shipped posts + captions: `content/posts/POSTS.md` (log every new post there, tagged)
4. No raw memes for now. Rebuild a meme's insight as a realistic artifact, typographic card, chart or carousel.
5. Never fetch sayari.com with curl/requests or a spoofed User-Agent; it's blocked. See `research/sayari-site/OTHER_CONTENT_INDEX.md` for the browser method.
6. After changing any content file, rebuild the hub (`python3 -I scripts/build_hub.py`) and republish `content/hub/hub.html` to https://claude.ai/artifact/Gmw5L8TenBeGWB3iVTRHaj (pass it as `url` from a new chat).
7. Listener data shows the landscape; don't copy rare lingo. Use situations and words that recur across many people, phrased so a beginner gets them (hyper-relevant, not hyper-niche).
