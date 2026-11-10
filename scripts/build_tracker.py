# build_tracker.py — Renders the private learning tracker (content/feedback/LEARNING_TRACKER.md) into a standalone
# page, content/feedback/tracker.html, published as its own PRIVATE artifact (never part of the Content Hub, which
# Ekshika can see). The .md stays the source of truth; rebuild + republish after each feedback round.
# Usage: python3 -I scripts/build_tracker.py   then republish content/feedback/tracker.html to the tracker URL in CLAUDE.md
# Requires: stdlib only.
import json, os, datetime
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
md = open(os.path.join(ROOT, "content/feedback/LEARNING_TRACKER.md"), encoding="utf-8").read()
built = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
html = r"""<title>Sayari Learning Tracker</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Merriweather:wght@700&family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
/* Layout: one readable column; rounds as sections, comparison tables scroll sideways on phones. */
:root{--paper:#FAF8F4;--surface:#FFFFFF;--ink:#1D2440;--muted:#6A6760;--line:#E6E1D7;--gold:#C57F27;--chip:#EFEBE3;
  --ok:#2F6B4F;--ok-soft:#E3EFE8;--warn:#8A5A12;--warn-soft:#F7ECD8;--idle:#5E6475;--idle-soft:#E9EAEF;
  --display:"Merriweather",Georgia,serif;--body:"Inter",-apple-system,"Segoe UI",sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--paper:#141A2E;--surface:#1D2440;--ink:#F1ECE2;--muted:#A9A69F;--line:#2E3654;--gold:#F4B941;--chip:#262E4D;
  --ok:#8FD1AE;--ok-soft:#1F3A30;--warn:#F2C877;--warn-soft:#3B3020;--idle:#B4B9C9;--idle-soft:#2A3150;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#141A2E;--surface:#1D2440;--ink:#F1ECE2;--muted:#A9A69F;--line:#2E3654;--gold:#F4B941;--chip:#262E4D;
  --ok:#8FD1AE;--ok-soft:#1F3A30;--warn:#F2C877;--warn-soft:#3B3020;--idle:#B4B9C9;--idle-soft:#2A3150;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--paper);color:var(--ink);font:15.5px/1.6 var(--body);margin:0}
.wrap{max-width:860px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:32px 64px}
.eyebrow{font:500 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
h1{font:700 30px/1.2 var(--display);margin:6px 0 4px;text-wrap:balance}
h2{font:700 21px/1.3 var(--display);margin:36px 0 10px;padding-top:20px;border-top:1px solid var(--line);text-wrap:balance}
h3{font:600 16px/1.35 var(--body);margin:22px 0 8px;color:var(--gold)}
p,li{max-width:72ch} ul,ol{padding-left:20px}
code{font:13px var(--mono);background:var(--chip);padding:1px 5px;border-radius:4px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--surface);margin:10px 0}
table{border-collapse:collapse;width:100%;min-width:600px;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
th{font:500 11px var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);background:var(--paper)}
tr:last-child td{border-bottom:0}
.st{font:600 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;padding:3px 7px;border-radius:999px;white-space:nowrap}
.st.applied,.st.done,.st.closed{background:var(--ok-soft);color:var(--ok)} .st.testing,.st.in{background:var(--warn-soft);color:var(--warn)} .st.open,.st.noted{background:var(--idle-soft);color:var(--idle)}
footer{color:var(--muted);font-size:13px;margin-top:40px}
</style>
<div class="wrap"><div class="eyebrow">Private · our learnings from client feedback</div><div id="doc"></div><footer id="foot"></footer></div>
<script>
const MD = __MD__, BUILT = __BUILT__;
const esc = s => String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const inline = t => esc(t).replace(/`(applied|testing|open|noted|done|closed|in progress)`/g,(m,w)=>`<span class="st ${w.split(" ")[0]}">${w}</span>`)
  .replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/\*(.+?)\*/g,"<i>$1</i>").replace(/`([^`]+)`/g,"<code>$1</code>");
function md(src){ const L=src.split("\n"); let h="",i=0;
  while(i<L.length){ const l=L[i];
    if(/^#{1,3} /.test(l)){const n=l.match(/^#+/)[0].length; h+=`<h${n}>${inline(l.replace(/^#+ /,""))}</h${n}>`; i++; continue;}
    if(/^---\s*$/.test(l)){i++; continue;}
    if(l.startsWith("|")){const rows=[]; while(i<L.length&&L[i].startsWith("|")){ if(!/^\|[-| :]+\|$/.test(L[i])) rows.push(L[i].trim().replace(/^\||\|$/g,"").split("|")); i++;}
      h+=`<div class="tablewrap"><table><thead><tr>${rows[0].map(c=>`<th>${inline(c.trim())}</th>`).join("")}</tr></thead><tbody>${rows.slice(1).map(r=>`<tr>${r.map(c=>`<td>${inline(c.trim())}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`; continue;}
    if(/^(- |\d+\. )/.test(l)){const ol=/^\d+\. /.test(l); let it=""; while(i<L.length&&/^(- |\d+\. )/.test(L[i])){it+=`<li>${inline(L[i].replace(/^(- |\d+\. )/,""))}</li>`; i++;} h+=ol?`<ol>${it}</ol>`:`<ul>${it}</ul>`; continue;}
    if(l.trim()) h+=`<p>${inline(l)}</p>`; i++; }
  return h; }
document.getElementById("doc").innerHTML = md(MD).replace("<h1>","<h1>").replace(/<h1>[^<]*<\/h1>/,"<h1>Sayari Learning Tracker</h1>");
document.getElementById("foot").textContent = `Built ${BUILT} from content/feedback/LEARNING_TRACKER.md (scripts/build_tracker.py).`;
</script>
"""
html = html.replace("__MD__", json.dumps(md, ensure_ascii=False).replace("</", "<\\/")).replace("__BUILT__", json.dumps(built))
out = os.path.join(ROOT, "content/feedback/tracker.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote", out)
