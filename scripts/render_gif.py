# render_gif.py — Renders an animated post HTML (e.g. design/kit/layouts/L7-newsjack-gif.html) to a looping GIF
# (plus an MP4 and a PNG of the final frame), for Sayari-style newsjack explainer GIFs.
# Usage:
#   python3 -I scripts/render_gif.py <post.html> [--out content/posts/drafts/P05.gif] [--width 900] [--fps 12]
# The HTML declares its timing in <meta name="gif" content="duration=12;settle=9.6;fps=12">:
#   duration = loop length in seconds, settle = when the last animation has finished (frames after it are copies,
#   so the final state holds on screen until the loop restarts).
# Requires: Google Chrome at /Applications (headless), ffmpeg (Homebrew), internet for Google Fonts.
#
# Gotchas:
# - No Playwright/Puppeteer here: each frame is one headless-Chrome screenshot of <file>#t=SECONDS; the page's own
#   script pauses every CSS animation at t (document.getAnimations()). Frames run in parallel (6 at a time).
# - Warm one --user-data-dir first (caches Google Fonts), then give each parallel worker its OWN copy: Chrome refuses
#   to run two instances on one profile ("Failed to create a ProcessSingleton", SingletonLock exists).
# - Freeze animations both before AND after document.fonts.ready, or the screenshot can land mid-animation.
# - GIF palette: palettegen stats_mode=full + paletteuse dither=none keeps flat brand colours clean and small;
#   bayer dithering adds visible noise on beige.
import argparse, concurrent.futures as cf, os, re, shutil, subprocess, sys, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def shot(url, out, profile):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
           "--virtual-time-budget=5000", "--run-all-compositor-stages-before-draw", f"--user-data-dir={profile}",
           "--window-size=1080,1350", f"--screenshot={out}", url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out):
        sys.exit(f"frame failed: {out}\n{r.stderr[-600:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html"); ap.add_argument("--out"); ap.add_argument("--width", type=int, default=900)
    ap.add_argument("--fps", type=int); ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    src = os.path.abspath(a.html)
    meta = re.search(r'name="gif"\s+content="([^"]+)"', open(src, encoding="utf-8").read())
    cfg = dict(kv.split("=") for kv in meta.group(1).split(";")) if meta else {}
    dur = float(cfg.get("duration", 10)); settle = float(cfg.get("settle", dur)); fps = a.fps or int(cfg.get("fps", 12))
    stem = os.path.splitext(a.out or src)[0]
    os.makedirs(os.path.dirname(stem) or ".", exist_ok=True)

    tmp = tempfile.mkdtemp(prefix="gif-"); profile = os.path.join(tmp, "profile")
    n = int(round(dur * fps)); last = min(n - 1, int(settle * fps) + 1)
    shot("file://" + src + f"#t={settle + 2:.3f}", os.path.join(tmp, "warm.png"), profile)  # caches fonts
    profiles = []
    for w in range(a.jobs):
        d = f"{profile}{w}"; shutil.copytree(profile, d, symlinks=True,
                                             ignore=shutil.ignore_patterns("Singleton*")); profiles.append(d)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(lambda i: shot("file://" + src + f"#t={i / fps:.3f}", os.path.join(tmp, f"f{i:04d}.png"),
                                   profiles[i % a.jobs]), range(last + 1)))
    for i in range(last + 1, n):
        shutil.copy(os.path.join(tmp, f"f{last:04d}.png"), os.path.join(tmp, f"f{i:04d}.png"))

    frames = os.path.join(tmp, "f%04d.png"); scale = f"scale={a.width}:-2:flags=lanczos"
    ff = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", frames]
    subprocess.run(ff + ["-vf", f"{scale},split[s0][s1];[s0]palettegen=stats_mode=full:max_colors=128[p];"
                         "[s1][p]paletteuse=dither=none", "-loop", "0", stem + ".gif"], check=True)
    subprocess.run(ff + ["-vf", f"scale=1080:-2", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                         stem + ".mp4"], check=True)
    shutil.copy(os.path.join(tmp, f"f{last:04d}.png"), stem + ".png")
    shutil.rmtree(tmp, ignore_errors=True)
    for ext in (".gif", ".mp4", ".png"):
        print("wrote", stem + ext, f"{os.path.getsize(stem + ext) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
