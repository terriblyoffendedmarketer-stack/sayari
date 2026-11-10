# sync_canvas.py — Pulls changed artboards from the Claude Design canvas into the post images the hub shows,
# archiving every image it replaces. Run as part of the /hub-sync routine (.claude/skills/hub-sync/SKILL.md).
# Usage: python3 -I scripts/sync_canvas.py <canvas-dir> [--write]
#   <canvas-dir> holds project/canvas.json + project/*.dc.html, downloaded with Artifact read (paths=...) from
#   the canvas URL in CLAUDE.md. Without --write it only reports what changed.
# Requires: Google Chrome (headless), internet for Google Fonts. Uses scripts/render_post.py.
# Map: content/posts/canvas_map.json  {artboard file: {"out": [asset pngs], "pdf": [carousel pdfs to rebuild], "sha": source hash}}
#
# Gotchas:
# - Change detection hashes the artboard SOURCE, not the PNG: headless renders can differ by a pixel between runs,
#   so comparing images would archive false changes.
# - Replaced images go to content/posts/archive/history/<YYYY-MM-DD_HHMM>/ (old file, same name). Never deleted.
# - New artboards not in canvas_map.json are only reported; add them to the map (which post file they become).
# - Carousel PDFs are rebuilt from the slide PNGs (one image per page) whenever any slide changes.
# - /_blob/<id> logos only resolve on claude.ai; BLOB_MAP in preview_dc.py swaps known ids for local SVGs.
#   A new uploaded image in an artboard needs its id added there, or it renders blank.
import hashlib, json, os, re, shutil, subprocess, sys, datetime, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(ROOT, "content/posts/assets")
MAP = os.path.join(ROOT, "content/posts/canvas_map.json")
KIT = os.path.join(ROOT, "design/kit/assets")
BLOB_MAP = {
    "0f8dbaa0047c8cd27ea9b50e46bf0bbe": f"file://{KIT}/wordmark-white.svg",
    "733466657a3c42c339281205b292e42c": f"file://{KIT}/wordmark-navy.svg",
    "877ce553c75fd33117e42bd3f39f4653": f"file://{KIT}/wordmark-navy.svg",
}
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def page_for(html):
    helmets = "".join(re.findall(r"<helmet>(.*?)</helmet>", html, re.S))
    body = re.search(r"</helmet>(.*?)</x-dc>", html, re.S) or re.search(r"<x-dc>(.*?)</x-dc>", html, re.S)
    body = re.sub(r"<helmet>.*?</helmet>", "", body.group(1), flags=re.S)
    page = "<!doctype html><meta charset='utf-8'>" + helmets + "<style>html,body{margin:0}</style>" + body
    for bid, local in BLOB_MAP.items():
        page = page.replace(f"/_blob/{bid}", local)
    unknown = set(re.findall(r"/_blob/([0-9a-f]{32})", page))
    return page, unknown


def build_pdf(pngs, out):
    with tempfile.TemporaryDirectory() as t:
        h = os.path.join(t, "deck.html")
        imgs = "".join(f"<img src='file://{p}'>" for p in pngs)
        open(h, "w").write("<!doctype html><style>@page{size:1080px 1350px;margin:0}html,body{margin:0}"
                           "img{display:block;width:1080px;height:1350px;page-break-after:always}</style>" + imgs)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                        "--no-pdf-header-footer", f"--print-to-pdf={out}", "file://" + h], capture_output=True, check=True)


def main():
    src, write = sys.argv[1], "--write" in sys.argv
    canvas = json.load(open(os.path.join(src, "project/canvas.json")))
    cmap = json.load(open(MAP))
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    archive = os.path.join(ROOT, "content/posts/archive/history", stamp)
    changed, pdfs = [], set()
    for name in canvas["order"]:
        if name not in cmap:
            print(f"NEW artboard (not mapped, skipped): {name} · {canvas['boards'][name].get('title', '')}")
            continue
        html = open(os.path.join(src, "project", name), encoding="utf-8").read()
        sha = hashlib.sha256(html.encode()).hexdigest()[:16]
        if cmap[name].get("sha") == sha:
            continue
        changed.append(name)
        print(f"changed: {name} -> {', '.join(cmap[name]['out'])}")
        if not write:
            continue
        page, unknown = page_for(html)
        if unknown:
            print(f"  warning: unknown uploaded image(s) {unknown}; add to BLOB_MAP or they render blank")
        with tempfile.TemporaryDirectory() as t:
            h = os.path.join(t, "board.html"); open(h, "w", encoding="utf-8").write(page)
            png = os.path.join(t, "board.png")
            subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts/render_post.py"), h, "--out", png],
                           check=True, capture_output=True)
            for out in cmap[name]["out"]:
                dst = os.path.join(ASSETS, out)
                if os.path.exists(dst):
                    os.makedirs(archive, exist_ok=True); shutil.copy2(dst, os.path.join(archive, out))
                shutil.copy2(png, dst)
        if cmap[name].get("pdf"):
            pdfs.update(cmap[name]["pdf"])
        cmap[name]["sha"] = sha
    for pdf in sorted(pdfs):
        stem = pdf[:-4]
        slides = sorted(f for f in os.listdir(ASSETS) if re.fullmatch(re.escape(stem) + r"-\d\d\.png", f))
        dst = os.path.join(ASSETS, pdf)
        if os.path.exists(dst):
            os.makedirs(archive, exist_ok=True); shutil.copy2(dst, os.path.join(archive, pdf))
        build_pdf([os.path.join(ASSETS, s) for s in slides], dst)
        print(f"rebuilt {pdf} from {len(slides)} slides")
    if write:
        json.dump(cmap, open(MAP, "w"), indent=1)
    print(f"{len(changed)} artboard(s) changed" + ("" if write else " (dry run; add --write)") +
          (f"; old images archived in {os.path.relpath(archive, ROOT)}" if write and os.path.isdir(archive) else ""))


if __name__ == "__main__":
    main()
