# sync_captions.py — Copies captions edited in the Content Hub back into content/posts/POSTS.md
# Usage:
#   1. Claude dumps the hub's caption docs:  ArtifactData list, url = hub URL, collection "captions",
#      out_dir = <scratch dir>   (writes <scratch dir>/captions/<P0X-vN>.json)
#   2. python3 -I scripts/sync_captions.py <scratch dir>/captions         (dry run: shows what would change)
#      python3 -I scripts/sync_captions.py <scratch dir>/captions --write (edits POSTS.md)
#   3. Rebuild + republish the hub as usual. Hub edits keep overriding POSTS.md (the db wins), so after
#      a sync both say the same thing.
# Requires: Python 3 only.
#
# Gotchas:
# - Keys are "<post id>-v<version index>", e.g. P04-v2 = the 2nd "#### Version" section of P04;
#   a post with no version headings has only -v1. Renumbering versions in POSTS.md breaks the mapping.
# - The caption is the FIRST run of "> " quote lines in that section (same rule build_hub.py reads),
#   so keep the caption as the first blockquote under the post / version heading.
# - When Claude edits a caption in POSTS.md directly, also write it to the hub db (captions/<key>
#   {text, at, by:null}), otherwise an older hub edit keeps overriding it on the page.
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "content/posts/POSTS.md")


def quoted(text):
    return [("> " + l) if l.strip() else ">" for l in text.splitlines()]


def replace_caption(md, key, text):
    m = re.match(r"(P\d\d)-v(\d+)$", key)
    if not m:
        return md, "bad key"
    pid, vi = m.group(1), int(m.group(2))
    start = md.find(f"\n## {pid} ")
    if start < 0:
        return md, "post not found"
    end = md.find("\n## ", start + 1)
    end = len(md) if end < 0 else end
    block = md[start:end]
    heads = [h.end() for h in re.finditer(r"\n#### Version \d+ · [^\n]*\n", block)]
    if heads:
        if vi > len(heads):
            return md, "version not found"
        s = heads[vi - 1]
        e = heads[vi] if vi < len(heads) else len(block)
    else:
        if vi != 1:
            return md, "version not found"
        s, e = 0, len(block)
    lines = block[s:e].split("\n")
    i = next((n for n, l in enumerate(lines) if l.startswith(">")), None)
    if i is None:
        return md, "no caption quote found"
    j = i
    while j < len(lines) and lines[j].startswith(">"):
        j += 1
    old = "\n".join(lines[i:j])
    new = "\n".join(quoted(text))
    if old == new:
        return md, "same"
    lines[i:j] = quoted(text)
    block = block[:s] + "\n".join(lines) + block[e:]
    return md[:start] + block + md[end:], "changed"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__ or "usage: sync_captions.py <dir of captions/*.json> [--write]")
    folder, write = sys.argv[1], "--write" in sys.argv
    md = open(POSTS, encoding="utf-8").read()
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".json"):
            continue
        doc = json.load(open(os.path.join(folder, f), encoding="utf-8"))
        data = doc.get("data", doc)
        key = f[:-5]
        md, status = replace_caption(md, key, data.get("text", ""))
        print(f"{key}: {status}" + (f" (edited {data.get('at', '?')})" if status == "changed" else ""))
    if write:
        open(POSTS, "w", encoding="utf-8").write(md)
        print("POSTS.md written")
    else:
        print("dry run; add --write to save")


if __name__ == "__main__":
    main()
