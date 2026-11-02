#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utokar Omraden-sektionen med Norge (Ostfold) + fler Fyrbodal-orter.
Kor: python3 update_areas.py
"""
import io, re, json, os, glob

SE = ["Uddevalla", "Trollhättan", "Vänersborg", "Ljungskile", "Munkedal", "Färgelanda",
      "Lilla Edet", "Stenungsund", "Tjörn", "Orust", "Lysekil", "Smögen", "Sotenäs",
      "Tanum", "Grebbestad", "Mellerud", "Åmål", "Strömstad", "Lidköping"]
NO = [("Halden", "halden.html"), ("Sarpsborg", "sarpsborg.html"),
      ("Fredrikstad", "fredrikstad.html"), ("Hvaler", "fredrikstad.html")]

def se_list():
    return '<ul class="areas">' + "".join("<li>%s</li>" % c for c in SE) + "</ul>"

def no_list():
    return ('<ul class="areas">'
            + "".join('<li><a href="%s">%s</a></li>' % (u, n) for n, u in NO)
            + "</ul>")

def split_block():
    return ('<div class="areas-split">\n'
            '      <div>\n'
            '        <h3>Sverige · Trestad och Fyrbodal</h3>\n'
            '        %s\n'
            '      </div>\n'
            '      <div>\n'
            '        <h3>Norge · Østfold</h3>\n'
            '        %s\n'
            '      </div>\n'
            '    </div>' % (se_list(), no_list()))

# ------------------------------------------------------------------ 1. CSS
CSS_ADD = """
/* Områden: Sverige / Norge sida vid sida */
.areas-split{display:grid;grid-template-columns:1.15fr 1fr;gap:var(--sp-10);margin-top:var(--sp-6)}
.areas-split h3{font-size:var(--fs-base);font-weight:700;letter-spacing:.01em;margin:0 0 var(--sp-4);color:var(--ink)}
.areas-split .areas{margin:0}
.areas a{color:var(--accent-dark);text-decoration:none;border-bottom:1.5px solid rgba(63,143,94,.35)}
.areas a:hover{border-bottom-color:var(--accent)}
.section-lead a{color:var(--accent-dark);font-weight:600;text-decoration:none;
  border-bottom:1.5px solid rgba(63,143,94,.35)}
.section-lead a:hover{border-bottom-color:var(--accent)}
@media (max-width:760px){.areas-split{grid-template-columns:1fr;gap:var(--sp-6)}}
"""

def patch_css():
    fn = "assets/styles.css"
    s = io.open(fn, encoding="utf-8").read()
    if ".areas-split" in s:
        print("  CSS redan uppdaterad"); return
    anchor = '.areas li:not(:last-child)::after{content:"·";margin-left:var(--sp-6);color:var(--line)}\n'
    assert anchor in s, "hittade inte areas-regeln"
    s = s.replace(anchor, anchor + CSS_ADD, 1)
    io.open(fn, "w", encoding="utf-8").write(s)
    print("  CSS: lade till .areas-split (%d tecken)" % len(CSS_ADD))

# ------------------------------------------------------- 2. Omraden-sektionen
def patch_section(fn, h2, lead):
    s = io.open(fn, encoding="utf-8").read()
    if "areas-split" in s:
        print("  %s redan uppdaterad" % fn); return
    pat = re.compile(r'(<p class="eyebrow">Områden</p>\s*<h2>).*?(</h2>\s*<p class="section-lead">).*?(</p>\s*)<ul class="areas">.*?</ul>', re.S)
    m = pat.search(s)
    assert m, "hittade inte Omraden-sektionen i " + fn
    new = (m.group(1) + h2 + m.group(2) + lead + m.group(3) + split_block())
    s = s[:m.start()] + new + s[m.end():]
    io.open(fn, "w", encoding="utf-8").write(s)
    print("  %s: Omraden-sektionen uppdaterad" % fn)

# ------------------------------------------------------ 3. areaServed i JSON-LD
def patch_schema():
    fn = "index.html"
    s = io.open(fn, encoding="utf-8").read()
    if '"Halden"' in s:
        print("  JSON-LD redan uppdaterad"); return
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    d = json.loads(m.group(2))
    for name in ["Halden", "Sarpsborg", "Fredrikstad"]:
        d["areaServed"].append({"@type": "City", "name": name})
    d["areaServed"].append({"@type": "AdministrativeArea", "name": "Østfold"})
    d["areaServed"].append({"@type": "AdministrativeArea", "name": "Norge"})
    s = s[:m.start(2)] + json.dumps(d, ensure_ascii=False) + s[m.end(2):]
    io.open(fn, "w", encoding="utf-8").write(s)
    print("  index.html: areaServed -> %d omraden" % len(d["areaServed"]))

# ------------------------------------------------------------------ 4. cache-bump
def bump():
    n = 0
    for fn in glob.glob("*.html"):
        s = io.open(fn, encoding="utf-8").read()
        if "?v=6" in s:
            s = s.replace("?v=6", "?v=7")
            io.open(fn, "w", encoding="utf-8").write(s)
            n += 1
    print("  cache v=6 -> v=7 i %d filer" % n)

if __name__ == "__main__":
    print("1) CSS")
    patch_css()
    print("2) Omraden-sektioner")
    patch_section("index.html",
        "Trestad, Fyrbodal — och <em>Østfold</em>",
        ("Vi utgår från Uddevalla och jobbar i Trestad — Uddevalla, Trollhättan och Vänersborg — och "
         "vidare ut i övriga Fyrbodal. Över gränsen tar vi uppdrag i <a href=\"halden.html\">Halden</a>, "
         "<a href=\"sarpsborg.html\">Sarpsborg</a> och <a href=\"fredrikstad.html\">Fredrikstad</a>. "
         "Är du osäker på om vi kommer till dig, ring och fråga."))
    patch_section("microcement.html",
        "Vi lägger microcement i hela <em>Trestad</em> och Østfold",
        ("Utgår från Uddevalla. Bygderna runtomkring tar vi oss också till — och grensområdet i Norge: "
         "<a href=\"halden.html\">Halden</a>, <a href=\"sarpsborg.html\">Sarpsborg</a> och "
         "<a href=\"fredrikstad.html\">Fredrikstad</a>."))
    print("3) areaServed i JSON-LD")
    patch_schema()
    print("4) Cache-bump")
    bump()
    print("Klart.")
