"""Fail if the built site's math uses KaTeX classes its stylesheet lacks.

Hugo renders math to HTML at build time with its own bundled KaTeX, and the
stylesheet comes from the version pinned in config.toml (params.katex).  When
the two differ across a class rename, as at KaTeX 0.18.0, the markup still
renders but its rules go unstyled: the underline in \\hat{\\underline{h}}
silently disappears.  This checks every class used inside .katex-html on the
built pages against the classes the stylesheet defines.

Usage: python3 tools/check_katex_css.py [public]
"""

import re
import sys
from pathlib import Path

site = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
css_files = sorted(site.glob("css/katex*.css"))
if not css_files:
    sys.exit(f"no KaTeX stylesheet under {site}/css")
defined = set()
for css in css_files:
    defined |= set(re.findall(r"\.([A-Za-z][\w-]*)", css.read_text()))

used = {}
for page in site.rglob("*.html"):
    html = page.read_text(errors="replace")
    for span in re.findall(r'class="?katex-html"?.*?(?=class="?katex"?[ >]|$)', html, flags=re.S):
        for attr in re.findall(r'class=("[^"]*"|[^\s>]+)', span):
            for name in attr.strip('"').split():
                used.setdefault(name, page)

# Classes KaTeX emits only for its own structure or that carry no rule.
missing = {c: p for c, p in used.items() if c not in defined and c.startswith(("katex", "under", "over", "accent", "hline", "rule"))}
for name, page in sorted(missing.items()):
    print(f"{name}: used in {page.relative_to(site)}, not in {', '.join(c.name for c in css_files)}")
if missing:
    sys.exit("KaTeX markup and stylesheet versions differ; set params.katex.version "
             "in config.toml to the KaTeX version bundled with HUGO_VERSION.")
print(f"KaTeX stylesheet defines all {len(used)} classes used in the built math.")
