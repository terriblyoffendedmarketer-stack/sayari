# build_hub.py — Builds the Content Hub page (content/hub/hub.html) from the repo's markdown + listener DB.
# The hub is a read-only view of the whole content library: posts log, themes, templates, buckets,
# sharpened ideas, meme library (text only), research (case studies, briefs) and listener stats.
# Usage: python3 -I scripts/build_hub.py        (then republish content/hub/hub.html as the artifact)
# Requires: stdlib only (re, json, sqlite3). Template: content/hub/template.html (has /*__HUB_DATA__*/).
#
# Gotchas:
# - Parsing relies on the markdown shapes in POSTS.md ("## P01 · Title"), FRAMEWORK.md (numbered
#   candidate themes, "| Bucket |" table), templates.md and IMAGE_IDEAS.md tables ("| NN | file |...").
#   Keep those shapes or update the parsers here.
# - Never embed the idea-doc meme images: they're copyrighted and gitignored. The hub shows text only.
import json, os, re, sqlite3, glob, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
P = lambda *a: os.path.join(ROOT, *a)
read = lambda p: open(P(p), encoding="utf-8").read()
strip_md = lambda s: re.sub(r"\*\*(.+?)\*\*", r"\1", re.sub(r"`([^`]+)`", r"\1", s)).strip()


def table_rows(md, header_startswith):
    """Rows of the first markdown table whose header row starts with header_startswith."""
    lines = md.splitlines()
    for i, l in enumerate(lines):
        if l.startswith(header_startswith):
            out = []
            for r in lines[i + 2:]:
                if not r.startswith("|"):
                    break
                out.append([strip_md(c) for c in r.strip().strip("|").split("|")])
            return out
    return []


def posts():
    md = read("content/posts/POSTS.md")
    out = []
    for block in re.split(r"\n## (?=P\d\d)", md)[1:]:
        head, *rest = block.split("\n")
        num, title = [x.strip() for x in head.split("·", 1)]
        body = "\n".join(rest)
        field = lambda k: (re.search(r"\*\*" + k + r":\*\*\s*(.+)", body) or [None, ""])[1].split(" · **")[0].strip()
        tags = dict(re.findall(r"\*\*([A-Za-z ]+):\*\*\s*([^·\n]+)", body))
        caption = "\n".join(l[2:] if l.startswith("> ") else l[1:] for l in body.splitlines() if l.startswith(">"))
        out.append({
            "id": num, "title": title,
            "format": strip_md(tags.get("Format", "")), "pillar": strip_md(tags.get("Pillar", "")),
            "template": strip_md(tags.get("Template", "")), "bucket": strip_md(tags.get("Bucket", "")),
            "theme": strip_md(tags.get("Theme", "")), "hook": strip_md(field("Hook type")),
            "moves": strip_md(field("Personality moves")), "image": strip_md(field("Image")),
            "results": strip_md(field("Results")), "caption": caption,
        })
    pipeline = re.findall(r"^- \*\*(.+?)\*\*:?\s*(.*)$", md.split("## In the pipeline")[-1], re.M) if "## In the pipeline" in md else []
    mix_note = (re.search(r"^Mix so far:.*$", md, re.M) or [""])[0]
    return out, [{"title": strip_md(t), "note": strip_md(n)} for t, n in pipeline], strip_md(mix_note)


def themes():
    md = read("content/FRAMEWORK.md")
    sec = md.split("## First candidate themes")[-1]
    out = []
    for name, rest in re.findall(r"^\d+\.\s+\*\*(.+?)\*\*\s*(.*)$", sec, re.M):
        ev = re.search(r"\(([^()]*)\)\s*\.?\s*$", rest)
        out.append({"name": name.rstrip(":"), "desc": strip_md(re.sub(r"\s*\([^()]*\)\s*\.?\s*$", "", rest)),
                    "evidence": ev.group(1) if ev else "", "status": "candidate"})
    validated = P("content/themes.md")
    if os.path.exists(validated):  # once themes.md exists, its "## Name" + "Status: x" entries win
        vmd = open(validated).read()
        for name, body in re.findall(r"^## (.+?)\n(.*?)(?=^## |\Z)", vmd, re.M | re.S):
            st = (re.search(r"Status:\s*(\w+)", body) or [None, "validated"])[1]
            for t in out:
                if t["name"].lower() == name.strip().lower():
                    t["status"] = st
    buckets = [{"name": r[0], "examples": r[1]} for r in table_rows(md, "| Bucket")]
    return out, buckets


def templates():
    rows = table_rows(read("playbook/templates.md"), "| Mechanic")
    return [dict(zip(["mechanic", "why", "variants", "best_for", "seen_in", "status"], r)) for r in rows if len(r) >= 6]


def memes():
    md = read("content/idea-doc-images/IMAGE_IDEAS.md")
    out, section = [], ""
    for l in md.splitlines():
        if l.startswith("## "):
            section = l[3:]
        m = re.match(r"\|\s*(\d{2})\s*\|(.*)\|\s*$", l)
        if m:
            c = [strip_md(x) for x in m.group(2).split("|")]
            kind = "pulse" if section.startswith("C") else "format" if section.startswith("B") else "brief"
            if kind == "pulse":
                out.append({"n": m.group(1), "kind": kind, "name": c[0], "what": c[1], "insight": c[2], "sayari": c[3]})
            else:
                out.append({"n": m.group(1), "kind": kind, "name": c[0], "what": c[1], "insight": "", "sayari": c[2] if len(c) > 2 else ""})
    picks = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*\s*\((.+?)\)", md.split("## Top picks")[-1], re.M) if "## Top picks" in md else []
    return out, [{"title": t, "why": w} for t, w in picks]


def sharpened():
    out = []
    for f in sorted(glob.glob(P("content/sharpened/*.md"))):
        md = open(f).read()
        title = md.splitlines()[0].lstrip("# ").strip()
        core = (re.search(r"\*\*Core truth:\*\*\s*(.+)", md) or [None, ""])[1]
        angles = re.findall(r"^\*\*([A-C])\.\s*(.+?)\*\*", md, re.M)
        out.append({"title": title, "core": strip_md(core), "angles": [f"{a}. {strip_md(t)}" for a, t in angles],
                    "file": os.path.relpath(f, ROOT)})
    return out


def case_studies():
    out = []
    for f in sorted(glob.glob(P("research/sayari-site/case-studies/*.md"))):
        md = open(f).read()
        L = md.splitlines()
        g = lambda k: (re.search(r"^" + k + r":\s*(.+)$", md, re.M) or [None, ""])[1]
        sub = (re.search(r"^## (.+)$", md, re.M) or [None, ""])[1]
        paras = [l for l in L if l and not l.startswith(("#", "Source:", "Published:", "Type:", "-", ">"))]
        quote = (re.search(r'^> "(.+?)"', md, re.M) or [None, ""])[1]
        out.append({"title": L[0].lstrip("# "), "who": sub, "summary": paras[0] if paras else "",
                    "quote": quote, "url": g("Source"), "date": g("Published"), "type": g("Type")})
    return out


def briefs():
    md = read("research/sayari-site/OTHER_CONTENT_INDEX.md")
    out = []
    for kind, sec in (("Investigation brief", "## Investigation briefs"), ("Buyer guide", "## Buyer guides")):
        part = md.split(sec)[-1].split("\n## ")[0]
        for line in re.findall(r"^- (.+)$", part, re.M):
            url = (re.search(r"https://\S+", line) or [""])[0]
            out.append({"kind": kind, "title": line.split(" — ")[0].strip(), "url": url})
    return out


def listener():
    db = P("data/sayari.db")
    if not os.path.exists(db):
        return {}
    con = sqlite3.connect(db)
    q = lambda s: con.execute(s).fetchall()
    total, kept = q("select count(*), sum(passed_filters) from raw_items")[0]
    lanes = {}
    for src, n in q("select source, count(*) from raw_items where passed_filters=1 group by 1"):
        lane = "news" if src.startswith("rss:") else "manual" if src.startswith("manual:") else "reddit"
        lanes[lane] = lanes.get(lane, 0) + n
    top = q("""select short_excerpt, upvotes, source, url from raw_items where passed_filters=1 and source like 'reddit:%'
               order by upvotes desc limit 12""")
    last = q("select max(timestamp) from pipeline_runs")[0][0]
    con.close()
    return {"total": total, "kept": kept or 0, "lanes": lanes, "last_run": last,
            "voices": [{"text": t, "up": u, "src": re.sub(r"reddit:(r/)+", "r/", s).split(":")[0], "url": url} for t, u, s, url in top]}


def main():
    p, pipeline, mix = posts()
    th, buckets = themes()
    mm, picks = memes()
    data = {"built": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "posts": p, "pipeline": pipeline, "mix": mix,
            "themes": th, "buckets": buckets, "templates": templates(), "memes": mm, "picks": picks,
            "sharpened": sharpened(), "cases": case_studies(), "briefs": briefs(), "listener": listener()}
    tpl = read("content/hub/template.html")
    html = tpl.replace("/*__HUB_DATA__*/null", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    open(P("content/hub/hub.html"), "w", encoding="utf-8").write(html)
    print("hub built:", {k: len(v) if isinstance(v, list) else "" for k, v in data.items()})


if __name__ == "__main__":
    main()
