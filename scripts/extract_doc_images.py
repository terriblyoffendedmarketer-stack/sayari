# extract_doc_images.py — Exports a Google Doc's embedded images and maps each to the
# nearest preceding heading/text so you know which section of the doc it sits under.
# Usage: python -I scripts/extract_doc_images.py <google-doc-id> <out-dir>
# Requires: stdlib only (urllib, zipfile, html.parser). Doc must be link-shared ("anyone with link").
#
# Gotchas:
# - The Drive MCP read_file_content returns text only, images are silently dropped.
#   The public export endpoint /export?format=zip gives HTML + images/ folder instead.
# - Images are numbered by file order, NOT doc order. Use the <img src> order in the HTML.
import sys, os, zipfile, io, json, urllib.request
from html.parser import HTMLParser

doc_id, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
url = f"https://docs.google.com/document/d/{doc_id}/export?format=zip"
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url).read()))
z.extractall(out)
html_name = [n for n in z.namelist() if n.endswith(".html")][0]

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.ctx = []; s.heading = ""; s.in_h = False; s.rows = []; s.buf = ""
    def handle_starttag(s, t, a):
        if t in ("h1", "h2", "h3", "h4"): s.in_h = True; s.buf = ""
        if t == "img":
            s.rows.append({"order": len(s.rows) + 1, "file": dict(a).get("src"),
                           "heading": s.heading, "text_before": " ".join(s.ctx)[-200:]})
    def handle_endtag(s, t):
        if t in ("h1", "h2", "h3", "h4"):
            s.in_h = False; s.heading = s.buf.strip() or s.heading; s.ctx = []
    def handle_data(s, d):
        d = d.strip()
        if not d: return
        if s.in_h: s.buf += " " + d
        else: s.ctx.append(d); s.ctx = s.ctx[-6:]

p = P(); p.feed(z.read(html_name).decode("utf-8"))
json.dump(p.rows, open(os.path.join(out, "image_map.json"), "w"), indent=1)
for r in p.rows: print(r["order"], r["file"], "|", r["heading"], "|", r["text_before"][-90:])
