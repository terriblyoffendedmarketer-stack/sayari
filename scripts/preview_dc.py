# preview_dc.py — Renders Claude Design artboard files (.dc.html) locally to PNG, plus one contact sheet,
# so artboards can be reviewed without opening the canvas (no claude.ai sign-in needed).
# Usage: python3 -I scripts/preview_dc.py <folder-with-project/> <out-dir>
#   e.g. python3 -I scripts/preview_dc.py "$SCRATCH/canvas" /tmp/dc-preview
# Requires: Google Chrome (headless), internet for Google Fonts. Uses scripts/render_post.py.
#
# Gotchas:
# - Artboards reference uploaded logos as /_blob/<id>; those only resolve on claude.ai. BLOB_MAP swaps the known
#   Sayari wordmark ids for the local SVGs in design/kit/assets. Add new ids here when new assets are uploaded.
# - Only the static markup is previewed: <x-dc>/<helmet> wrappers are unwrapped and the DCLogic script is dropped,
#   so {{holes}} or interactive bits won't render. Fine for posts, which are static.
import os, re, sys, subprocess, glob, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KIT = os.path.join(ROOT, "design/kit/assets")
BLOB_MAP = {
    "0f8dbaa0047c8cd27ea9b50e46bf0bbe": f"file://{KIT}/wordmark-white.svg",
    "733466657a3c42c339281205b292e42c": f"file://{KIT}/wordmark-navy.svg",
    "877ce553c75fd33117e42bd3f39f4653": f"file://{KIT}/wordmark-navy.svg",
}

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
canvas = json.load(open(os.path.join(src, "project/canvas.json")))
pngs = []
for name in canvas["order"]:
    html = open(os.path.join(src, "project", name)).read()
    helmet = re.search(r"<helmet>(.*?)</helmet>", html, re.S)
    body = re.search(r"</helmet>(.*?)</x-dc>", html, re.S) or re.search(r"<x-dc>(.*?)</x-dc>", html, re.S)
    page = "<!doctype html><meta charset='utf-8'>" + (helmet.group(1) if helmet else "") + \
           "<style>html,body{margin:0;background:#555}</style>" + body.group(1)
    for bid, local in BLOB_MAP.items():
        page = page.replace(f"/_blob/{bid}", local)
    stem = os.path.join(out, name.replace(".dc.html", ""))
    open(stem + ".html", "w").write(page)
    subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts/render_post.py"), stem + ".html", "--out", stem + ".png"], check=True)
    pngs.append((name, canvas["boards"][name], stem + ".png"))

# contact sheet laid out like the canvas, scaled to 25%
xs = [b["x"] + b["w"] for _, b, _ in pngs]; ys = [b["y"] + b["h"] for _, b, _ in pngs]
W, H, k = max(xs), max(ys), 0.25
tiles = "".join(f"<img src='file://{p}' style='position:absolute;left:{b['x']*k}px;top:{b['y']*k}px;width:{b['w']*k}px'>"
                f"<div style='position:absolute;left:{b['x']*k}px;top:{b['y']*k-18}px;font:12px sans-serif;color:#fff'>{b.get('title', n)}</div>"
                for n, b, p in pngs)
sheet = os.path.join(out, "contact-sheet.html")
open(sheet, "w").write(f"<!doctype html><body style='margin:0;background:#333'><div style='position:relative;width:{W*k}px;height:{H*k+20}px;margin:24px'>{tiles}</div></body>")
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                f"--window-size={int(W*k)+48},{int(H*k)+68}", f"--screenshot={os.path.join(out, 'contact-sheet.png')}",
                "--virtual-time-budget=3000", "file://" + sheet], capture_output=True)
print("wrote", len(pngs), "artboards +", os.path.join(out, "contact-sheet.png"))
