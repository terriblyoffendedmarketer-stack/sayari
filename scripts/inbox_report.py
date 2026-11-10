# inbox_report.py — Prints the hub Inbox (db docs dumped to JSON) as a compact list, so filing it costs few tokens.
# Usage: python3 -I scripts/inbox_report.py <dir of inbox/*.json> [--all]
#   Dump first: ArtifactData list, url = hub URL, collection "inbox", out_dir = <scratch dir>.
#   Default shows only items not yet filed; --all includes filed ones.
# Requires: Python 3 only.
#
# Gotchas:
# - Doc ids are the filenames; use them when marking items filed (ArtifactData update inbox/<id>
#   {status: "filed", filedAs: "I53"}).
# - Images are assets: fetch one with Artifact read, url = hub URL, path = <assetId>, only when the
#   image matters for filing (it lands in the artifact's scratch folder).
import json, os, sys


def main():
    folder, show_all = sys.argv[1], "--all" in sys.argv
    items = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".json"):
            d = json.load(open(os.path.join(folder, f), encoding="utf-8"))
            items.append((f[:-5], d.get("data", d)))
    items.sort(key=lambda x: x[1].get("at", ""))
    shown = [x for x in items if show_all or x[1].get("status") != "filed"]
    print(f"{len(shown)} item(s) to file ({len(items)} in inbox)")
    for i, d in shown:
        s = d.get("sort") or {}
        print(f"\n[{i}] {d.get('status')} · {d.get('at', '')[:16]}" + (f" · image {d['assetId']}" if d.get("assetId") else ""))
        for k in ("text", "link", "context"):
            if d.get(k):
                print(f"  {k}: {d[k]}")
        if s:
            print(f"  sorted: {s.get('start')} | {s.get('bucket')} | {s.get('format')} | {s.get('title')} — {s.get('gist')}"
                  + (f" (needs {s['needs']})" if s.get("needs") else ""))


if __name__ == "__main__":
    main()
