"""Measure every catalogue entry in a real browser and cache the heights.

The packer needs to know how tall an entry is before it decides which page it
goes on, and estimating that from content has failed twice: once by 12mm per
entry, and again the moment an entry grew a line. So it is measured. This
renders every entry into a probe page at the exact column width, asks Chrome
for each one's height, and writes heights.json in pixels — which is what
build_v2.py divides by 3.7795 to get millimetres.

Re-run it whenever the anatomy of an entry changes. Nothing else needs to know.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

sys.path.insert(0, str(HERE))
import build_monograph as B  # noqa: E402  (importing runs the build, which is harmless)

probe = B.HERE / "heights-probe.html"
# The entries are laid out exactly as a page lays them out — one flow, no
# wrappers — because a wrapper changes how margins collapse and the packer
# needs the height an entry actually costs when it follows another one.
blocks = []
for slug in B.FULL:
    html, _ = B.entry_full(slug)
    blocks.append(html.replace('<div class="', f'<div data-slug="{slug}" class="', 1))

probe.write_text(
    f'<!doctype html><html><head><meta charset="utf-8"><style>{B.CSS}\n'
    f'body {{ margin:0; }}\n'
    f'#flow {{ width:174mm; }}\n'   # the page is 210mm less 18mm of margin each side
    f'</style></head><body>{B.DEFS}<div id="flow">'
    + "".join(blocks) +
    '</div><pre id="out"></pre><script>'
    # `top` is a non-writable window global, so a var of that name silently
    # stays the window object and every subtraction becomes NaN. Named `y0`.
    '(function(){'
    'var e=document.querySelectorAll("#flow [data-slug]"),o={},'
    'f=document.getElementById("flow").getBoundingClientRect();'
    'for(var i=0;i<e.length;i++){'
    'var y0=e[i].getBoundingClientRect().top;'
    'var y1=(i+1<e.length)?e[i+1].getBoundingClientRect().top:f.bottom;'
    'o[e[i].getAttribute("data-slug")]=y1-y0;}'
    'document.getElementById("out").textContent=JSON.stringify(o);'
    '})();'
    '</script></body></html>', encoding="utf-8")

dom = subprocess.run(
    [CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=60000",
     "--dump-dom", f"file://{probe}"],
    capture_output=True, text=True, timeout=600).stdout

m = re.search(r'<pre id="out">(\{.*?\})</pre>', dom, re.S)
if not m:
    raise SystemExit("the probe page did not report any heights")
heights = json.loads(m.group(1))
missing = [s for s in B.FULL if s not in heights]
if missing:
    raise SystemExit(f"{len(missing)} entries unmeasured, e.g. {missing[:3]}")

(B.HERE / "heights.json").write_text(json.dumps(heights, indent=0))
mm = sorted(v / 3.7795 for v in heights.values())
print(f"measured {len(heights)} entries")
print(f"  median {mm[len(mm)//2]:.1f}mm   tallest {mm[-1]:.1f}mm   shortest {mm[0]:.1f}mm")
print(f"  over the {B.BUDGET_MM:.0f}mm page budget: {sum(1 for x in mm if x > B.BUDGET_MM)}")
