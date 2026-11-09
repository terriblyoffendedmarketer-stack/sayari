# render_post.py — Renders a 1080x1350 post HTML (design/kit layouts or a post built from them) to PNG,
# or a carousel to one PNG per slide plus a LinkedIn-ready PDF.
# Usage:
#   python3 -I scripts/render_post.py design/kit/layouts/L1-search-stack.html            -> same-name .png next to it
#   python3 -I scripts/render_post.py <file.html> --out design/kit/previews/L1.png
#   python3 -I scripts/render_post.py <carousel.html> --slides 5 [--pdf]                  -> <name>-1.png … + <name>.pdf
# Requires: Google Chrome at /Applications (headless), internet for Google Fonts.
#
# Gotchas:
# - Fonts load from Google Fonts; without --virtual-time-budget Chrome screenshots before they arrive and
#   falls back to Georgia/system fonts. 6000ms is enough on a normal connection.
# - Carousel slides are picked with a URL hash (#1, #2…), which the layout's script reads; PDF uses print mode
#   (@page 1080x1350 in kit.css) so each .canvas becomes one page.
import argparse, os, subprocess, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def chrome(args):
    base = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw"]
    r = subprocess.run(base + args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr[-800:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("--out"); ap.add_argument("--slides", type=int, default=0)
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    src = os.path.abspath(a.html); url = "file://" + src
    stem = os.path.splitext(a.out or src)[0]
    if a.slides:
        for i in range(1, a.slides + 1):
            chrome(["--window-size=1080,1350", f"--screenshot={stem}-{i}.png", f"{url}#{i}"]); print("wrote", f"{stem}-{i}.png")
        if a.pdf:
            chrome(["--no-pdf-header-footer", f"--print-to-pdf={stem}.pdf", url]); print("wrote", f"{stem}.pdf")
    else:
        out = a.out or stem + ".png"
        chrome(["--window-size=1080,1350", f"--screenshot={out}", url]); print("wrote", out)


if __name__ == "__main__":
    main()
