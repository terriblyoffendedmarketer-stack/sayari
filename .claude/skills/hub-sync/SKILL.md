---
name: hub-sync
description: One-step sync between the Content Hub, the Claude Design canvas and the repo for the Sayari project. Use when the user says "hub sync", "/hub-sync", "sync the hub", "file my inbox", or at the start of a post work session.
---

# Hub sync (Sayari)

Goal: bring everything the user did outside the chat into the repo, then republish the hub, in as few tokens as possible. Report in 3–5 lines at the end. Don't paste file contents or long listings into the chat.

URLs (also in CLAUDE.md): hub `https://claude.ai/artifact/Gmw5L8TenBeGWB3iVTRHaj`, canvas `https://claude.ai/artifact/Qf9AmewWkDheDkufUh7b1n`. Use the scratchpad for all dumps (`$S` below).

1. **Captions.** ArtifactData `list` (hub url, collection `captions`, out_dir `$S/hub`) → `python3 -I scripts/sync_captions.py $S/hub/captions --write`.
2. **Canvas → post images.** Artifact `list` scope `files` on the canvas url, then Artifact `read` with `paths` = `project/canvas.json` + every `project/*.dc.html`, out_dir `$S/canvas` → `python3 -I scripts/sync_canvas.py $S/canvas --write`. Old images go to `content/posts/archive/history/<stamp>/` automatically, and the editable Canva PDFs in `content/posts/editable/` are regenerated. If it reports a NEW artboard, ask the user which post it is, add it to `content/posts/canvas_map.json`, and re-run. If a post's design changed, also update its entry in POSTS.md if the text on the image changed.
3. **Inbox.** ArtifactData `list` (hub url, collection `inbox`, out_dir `$S/hub`) → `python3 -I scripts/inbox_report.py $S/hub/inbox`. For each unfiled item:
   - Ideas, insights, angles, hooks → a new row in `content/buckets/IDEA_BANK.md` (next free I## or H## id). Use the item's "sorted" tags if present, and correct them if they're wrong. Put the user's context note in the gist or needs.
   - Images and screenshots → fetch only if needed (Artifact read, hub url, path = assetId). Save them to `content/inbox/assets/<date>-<slug>.<ext>`, add a line to `content/inbox/LIBRARY.md` (what it is, the user's context, where it could be used), and link the idea row to it. Copyrighted third-party images (memes, news screenshots) go in `content/idea-doc-images/images/` instead, which is gitignored.
   - Links → into the idea row's needs/source, or `research/` if it's a source document.
   - Then ArtifactData `batch` of `update` ops: `inbox/<id>` `{status: "filed", filedAs: "<id or file>"}`.
   - Unclear item → leave it as is and list it in the report as a question for the user.
3b. **Backup shelf.** ArtifactData `list` (hub url, collection `shelf`). Each doc id (`P0X-vN`) is a version the user moved to Backup on the Posts tab (Restore deletes the doc). Mirror it in the POSTS.md index Status column ("Backup") and report changes. Backup ≠ archive: archive is recovery only.
4. **Rebuild + republish the hub.** `python3 -I scripts/build_hub.py`, then Artifact publish `content/hub/hub.html` to the hub url. Pass only the changed images as `files` (`posts/<f>` ← `content/posts/assets/<f>`, and `editable/<f>` ← `content/posts/editable/<f>` when designs changed). Omit `capabilities`.
5. **Commit** with a message listing what came in (e.g. "hub-sync: 2 captions, P04 slide 3 from canvas, 4 inbox items → I53–I55").

Rules: the inbox is the user's private scratch space. Never show it on the hub's shared tabs, and never put it in `content/feedback/`. Follow the project rules in CLAUDE.md (no memes in posts, hyper-relevant not hyper-niche).
