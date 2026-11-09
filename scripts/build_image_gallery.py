# build_image_gallery.py — Builds a local HTML gallery (gallery.html) of the idea-doc images,
# pairing each image with its row from IMAGE_IDEAS.md (what it is + Sayari non-meme version).
# Usage: python -I scripts/build_image_gallery.py client-private/idea-doc-images
# Requires: stdlib only. Output stays local (images are confidential/copyrighted; don't publish).
#
# Gotchas:
# - Rows are matched by the leading "| NN |" number in IMAGE_IDEAS.md tables; keep that format.
import sys, os, re, html
d = sys.argv[1]
md = open(os.path.join(d, "IMAGE_IDEAS.md")).read()
rows, section = {}, ""
for line in md.splitlines():
    if line.startswith("## "): section = line[3:]
    m = re.match(r"\|\s*(\d{2})\s*\|(.*)\|\s*$", line)
    if m:
        cells = [c.strip() for c in m.group(2).split("|")]
        rows[m.group(1)] = (section, cells)
imgs = sorted(f for f in os.listdir(os.path.join(d, "images")) if f.endswith(".png"))
def md2h(s): return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(s))
cards = []
for f in imgs:
    n = f[:2]; sec, cells = rows.get(n, ("Other (sales/marketing meme, skip)", [f[3:-4]]))
    tag = "pulse" if sec.startswith("C") else "brief" if sec.startswith("A") else "format" if sec.startswith("B") else "skip"
    body = "".join(f"<p>{md2h(c)}</p>" for c in cells[1:])
    cards.append(f'<article class="{tag}" id="i{n}"><a href="images/{f}" target="_blank"><img loading="lazy" src="images/{f}"></a>'
                 f'<div><span class="tag">{tag}</span><h3>#{n} · {html.escape(f[3:-4])}</h3>{body}</div></article>')
open(os.path.join(d, "gallery.html"), "w").write(f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Idea Doc Gallery</title><style>
:root{{--bg:#FAF8F4;--ink:#1D2440;--mut:#6A6760;--gold:#C57F27;--card:#fff}}
body{{background:var(--bg);color:var(--ink);font:15px/1.45 Inter,system-ui,sans-serif;margin:0;padding:24px 16px}}
h1{{font-family:Merriweather,Georgia,serif;margin:0 0 6px}} .sub{{color:var(--mut);margin-bottom:16px}}
nav button{{border:1px solid var(--ink);background:none;color:var(--ink);padding:6px 12px;border-radius:99px;margin:0 6px 8px 0;cursor:pointer}}
nav button.on{{background:var(--ink);color:var(--bg)}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}}
article{{background:var(--card);border-radius:10px;overflow:hidden;box-shadow:0 1px 3px #0002;display:flex;flex-direction:column}}
article img{{width:100%;max-height:420px;object-fit:contain;background:#eee;display:block}}
article div{{padding:12px 14px}} h3{{margin:4px 0 6px;font-size:15px}} p{{margin:4px 0;font-size:13.5px}}
.tag{{font:600 11px/1 Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}}
</style><h1>Idea doc: all {len(imgs)} images</h1><div class=sub>Click an image for full size. Pulse = keep the insight, change the format (no memes for now).</div>
<nav>{''.join(f'<button data-f="{t}">{t}</button>' for t in ['all','pulse','format','brief','skip'])}</nav><main>{''.join(cards)}</main>
<script>document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('on',x==b));
document.querySelectorAll('article').forEach(a=>a.style.display=(b.dataset.f=='all'||a.className==b.dataset.f)?'':'none')}});document.querySelector('nav button').click()</script>""")
print("cards:", len(cards), "matched:", sum(1 for f in imgs if f[:2] in rows))
