# export_editable.py — Exports each post from the Claude Design canvas as an EDITABLE PDF (real text, vector shapes,
# one page per slide), so Ekshika can import it into Canva (or Figma/Illustrator) and move individual elements.
# Usage: python3 -I scripts/export_editable.py <canvas-dir>     (same download as sync_canvas.py)
#   Writes content/posts/editable/<P0X>-editable.pdf (single image) or <P0X-vN>-editable.pdf (carousel).
#   /hub-sync runs it after sync_canvas.py; the hub shows an "Editable PDF (Canva)" button per post.
# Requires: Google Chrome (headless), internet for Google Fonts. Groups come from content/posts/canvas_map.json.
#
# Gotchas:
# - Use print-to-pdf, never screenshots: printing keeps text as text (fonts embedded) and boxes as vectors.
#   Screenshot PDFs (like the carousel PDFs for LinkedIn) are flat images Canva can't take apart.
# - print-color-adjust:exact is required or Chrome drops background colours (navy slides print white).
# - Chrome's print-to-pdf does NOT wait for Google Fonts (even with --virtual-time-budget): text came out in
#   Menlo / Merriweather Light. Fonts are cached once as local TTFs in design/kit/fonts/ and inlined as @font-face.
# - box-shadow prints as a dark rasterised rectangle (seen on P04 cover), so shadows are removed in these files.
# - Canva: upload the PDF (Create design → Import file). Text comes in as editable text boxes; check fonts map
#   to Merriweather / Inter / JetBrains Mono (all available in Canva).
import hashlib, json, os, re, subprocess, sys, tempfile, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from sync_canvas import page_for, CHROME  # noqa: E402

OUT = os.path.join(ROOT, "content/posts/editable")
MAP = os.path.join(ROOT, "content/posts/canvas_map.json")
FONTS = os.path.join(ROOT, "design/kit/fonts")


def local_fonts(head):
    """Swap Google Fonts <link>s for @font-face rules pointing at cached local TTFs (downloaded once)."""
    def swap(m):
        url = "https://" + m.group(1).replace("&amp;", "&")
        key = hashlib.sha1(url.encode()).hexdigest()[:10]
        css_path = os.path.join(FONTS, f"css-{key}.css")
        if not os.path.exists(css_path):
            os.makedirs(FONTS, exist_ok=True)
            css = urllib.request.urlopen(url, timeout=20).read().decode()  # no browser UA -> plain TTF urls
            for f in set(re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", css)):
                name = re.sub(r"[^A-Za-z0-9._-]", "_", f.split("/s/")[-1])
                dst = os.path.join(FONTS, name)
                if not os.path.exists(dst):
                    open(dst, "wb").write(urllib.request.urlopen(f, timeout=20).read())
                css = css.replace(f, "file://" + dst)
            open(css_path, "w").write(css)
        css = open(css_path).read()
        import base64  # inline as data: URIs; file:// font URLs were not applied in print
        css = re.sub(r"url\(file://([^)]+)\)", lambda u: "url(data:font/ttf;base64," + base64.b64encode(open(u.group(1), "rb").read()).decode() + ")", css)
        return "<style>" + css + "</style>"
    head = re.sub(r"<link[^>]+rel=\"preconnect\"[^>]*>", "", head)
    return re.sub(r"<link[^>]+href=\"https://(fonts\.googleapis\.com/css2\?[^\"]+)\"[^>]*>", swap, head)


def groups():
    g = {}
    for board, v in json.load(open(MAP)).items():
        for png in v["out"]:
            m = re.match(r"(P\d\d-v\d+)-(\d\d)\.png$", png)
            key, order = (m.group(1), int(m.group(2))) if m else (png.split("-")[0], 0)
            g.setdefault(key, []).append((order, board))
    return {k: [b for _, b in sorted(v)] for k, v in g.items()}


def export(src, key, boards):
    heads, pages = [], []
    for b in boards:
        html = open(os.path.join(src, "project", b), encoding="utf-8").read()
        page, unknown = page_for(html)
        if unknown:
            print(f"  warning: {b} uses unknown uploaded image(s) {unknown}; add them to BLOB_MAP in sync_canvas.py")
        head, body = page.split("<style>html,body{margin:0}</style>", 1)
        heads.append(local_fonts(head.replace("<!doctype html><meta charset='utf-8'>", "")))
        pages.append(f"<div class='pg'>{body}</div>")
    doc = ("<!doctype html><meta charset='utf-8'>" + "".join(dict.fromkeys(heads)) +
           "<style>@page{size:1080px 1350px;margin:0}html,body{margin:0}"
           "*{-webkit-print-color-adjust:exact;print-color-adjust:exact;box-shadow:none!important}"
           ".pg{width:1080px;height:1350px;overflow:hidden;position:relative;break-after:page}"
           ".pg:last-child{break-after:auto}</style>" + "".join(pages))
    os.makedirs(OUT, exist_ok=True)
    out = os.path.join(OUT, f"{key}-editable.pdf")
    with tempfile.TemporaryDirectory() as t:
        h = os.path.join(t, "doc.html"); open(h, "w", encoding="utf-8").write(doc)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                        "--virtual-time-budget=8000", "--run-all-compositor-stages-before-draw",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}", "file://" + h],
                       capture_output=True, check=True)
    print(f"wrote {os.path.relpath(out, ROOT)} ({len(boards)} page{'s' if len(boards) > 1 else ''})")


def main():
    src = sys.argv[1]
    only = sys.argv[2:]  # optional group keys
    for key, boards in groups().items():
        if not only or key in only:
            export(src, key, boards)


if __name__ == "__main__":
    main()
