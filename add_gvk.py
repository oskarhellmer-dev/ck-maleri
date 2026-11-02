#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lagger in GVK (Golv- & Vatrumskontroll) dar det ar relevant.
Kor: python3 add_gvk.py
"""
import io

SE_FILES = ["index.html", "golvslipning.html", "maleri-och-tapet.html", "microcement.html",
            "plattsattning.html", "404.html", "integritetspolicy.html", "tack.html"]

def rd(f):  return io.open(f, encoding="utf-8").read()
def wr(f, s):
    io.open(f, "w", encoding="utf-8").write(s)
    print("  skrev", f)

def rep(s, old, new, label, f, expect=1):
    n = s.count(old)
    if n == 0:
        print("    !! HITTADE INTE [%s] i %s" % (label, f)); return s
    if n != expect:
        print("    ~ %s: %d traeff(ar), forvantade %d" % (label, n, expect))
    else:
        print("    - %s" % label)
    return s.replace(old, new)

# ------------------------------------------------- 1. Footer-trustline (svenska sidor)
def footer_lines():
    old = "Försäkrade · F-skatt · ROT-avdrag"
    new = "Försäkrade · GVK-auktoriserade · F-skatt · ROT-avdrag"
    for f in SE_FILES:
        s = rd(f)
        if new in s:
            print("  %-24s redan" % f); continue
        if old in s:
            wr(f, s.replace(old, new)); print("  %-24s OK" % f)
        else:
            print("  %-24s INGEN TRÄFF" % f)

# ------------------------------------------------------------------- 2. index.html
def patch_index():
    f = "index.html"; s = rd(f)
    if "GVK-auktoriserade</dt>" in s:
        print("  redan uppdaterad"); return
    s = rep(s,
        "Golvslipning, måleri, microcement och plattsättning i Uddevalla och Trestad. Försäkrade, ROT-avdrag och kostnadsfri offert. Ring 073-703 37 17.",
        "Golvslipning, måleri, microcement och plattsättning i Uddevalla och Trestad. GVK-auktoriserade, försäkrade och kostnadsfri offert. Ring 073-703 37 17.",
        "meta + og:description", f, expect=2)
    s = rep(s,
        "<div><dt>Trestad och Fyrbodal</dt><dd>Vi utgår från Uddevalla och jobbar i hela Fyrbodal, inte bara i stan.</dd></div>",
        "<div><dt>GVK-auktoriserade</dt><dd>Vi följer GVK:s branschregler för våtrum, och tätskiktsarbetet granskas av en oberoende kontrollant. Du får dokumentationen på jobbet.</dd></div>",
        "faktaruta", f)
    s = rep(s,
        "<details><summary>Gör ni tätskikt i badrum?</summary><p>Ja. Tätskiktet ska vara rätt utfört, annars hjälper varken kakel eller microcement. Det ingår när vi gör våtrum.</p></details>",
        "<details><summary>Gör ni tätskikt i badrum?</summary><p>Ja. Tätskiktet ska vara rätt utfört, annars hjälper varken kakel eller microcement. Vi är GVK-auktoriserade, så arbetet görs enligt GVK:s branschregler och granskas av en oberoende kontrollant. Du får dokumentationen. Det ingår när vi gör våtrum.</p></details>",
        "FAQ synlig", f)
    s = rep(s,
        '"text":"Ja. Tätskiktet ska vara rätt utfört, annars hjälper varken kakel eller microcement. Det ingår när vi gör våtrum."',
        '"text":"Ja. Tätskiktet ska vara rätt utfört, annars hjälper varken kakel eller microcement. Vi är GVK-auktoriserade, så arbetet görs enligt GVK:s branschregler och granskas av en oberoende kontrollant. Du får dokumentationen. Det ingår när vi gör våtrum."',
        "FAQ-schema", f)
    wr(f, s)

# --------------------------------------------------------------- 3. microcement.html
def patch_micro():
    f = "microcement.html"; s = rd(f)
    if "Vi är GVK-auktoriserade, gör tätskiktet" in s:
        print("  redan uppdaterad"); return
    s = rep(s,
        "Microcement på golv, väggar, bänkskivor och i badrum i Uddevalla och Trestad. Fogfria ytor, ofta direkt på befintligt kakel. Begär kostnadsfri offert.",
        "Microcement på golv, väggar, bänkskivor och i badrum i Uddevalla och Trestad. GVK-auktoriserade för tätskikt i våtrum. Fogfria ytor, ofta på befintligt kakel.",
        "meta + og:description", f, expect=2)
    s = rep(s,
        "Vi gör tätskiktet enligt branschreglerna och dokumenterar med bilder.",
        "Vi är GVK-auktoriserade, gör tätskiktet enligt GVK:s branschregler och dokumenterar med bilder. Arbetet granskas av en oberoende kontrollant.",
        "tätskikts-text (synlig + schema)", f, expect=2)
    s = rep(s,
        "I ett våtrum är det tätskiktet under ytan som godkänns — kakel, klinker och microcement är materialet man ser, medan det är folien bakom som gör rummet vattentätt.",
        "I ett våtrum är det tätskiktet under ytan som godkänns — kakel, klinker och microcement är materialet man ser, medan det är folien bakom som gör rummet vattentätt. Vi är GVK-auktoriserade, så tätskiktet görs enligt GVK:s branschregler och granskas av en oberoende kontrollant.",
        "våtrums-brödtext", f)
    wr(f, s)

def patch_micro_body():
    """Brodtexten är radbruten — matcha med flexibelt blanksteg."""
    import re
    f = "microcement.html"; s = rd(f)
    if "Vi är GVK-auktoriserade, så tätskiktet" in s:
        print("  brödtext: redan"); return
    pat = re.compile(r"Vi gör tätskiktet enligt branschreglerna och dokumenterar arbetet med bilder,\s+så att du har\s+papperen om något skulle hända\.")
    m = pat.search(s)
    if not m:
        print("  !! brödtext: hittade inte"); return
    new = ("Vi är GVK-auktoriserade, så tätskiktet görs enligt GVK:s branschregler och granskas av en "
           "oberoende kontrollant. Du får dokumentationen, så att du har papperen om något skulle hända.")
    wr(f, s[:m.start()] + new + s[m.end():])
    print("  - brödtext")

# ------------------------------------------------------------- 4. plattsattning.html
def patch_plat():
    f = "plattsattning.html"; s = rd(f)
    if "Som GVK-auktoriserade utför vi tätskiktet" in s:
        print("  redan uppdaterad"); return
    s = rep(s,
        "Plattsättning av kakel och klinker i hall, kök och badrum i Uddevalla och Trestad. Korrekt tätskikt, noggrann fogning och fast pris. Begär kostnadsfri offert.",
        "Plattsättning av kakel och klinker i hall, kök och badrum i Uddevalla och Trestad. GVK-auktoriserade för tätskikt i våtrum. Fast pris och kostnadsfri offert.",
        "meta + og:description", f, expect=2)
    s = rep(s,
        "<p>Vi gör tätskikt enligt gällande regler och dokumenterar med bilder, så att du har papperen om något händer.",
        '<p>Vi är <a href="https://www.gvk.se/" rel="noopener">GVK-auktoriserade</a>, vilket betyder att vi följer GVK:s branschregler för våtrum och att tätskiktsarbetet granskas av en oberoende kontrollant. Du får dokumentationen, så att du har papperen om något händer.',
        "brödtext", f)
    s = rep(s,
        "<li>Tätskikt enligt reglerna, med bilddokumentation</li>",
        "<li>Tätskikt enligt GVK:s branschregler, med dokumentation</li>",
        "ingår-lista", f)
    s = rep(s,
        "<h3>Tätskikt och plattor</h3><p>Vi utför, dokumenterar tätskiktet och kontrollerar lutningen löpande.</p>",
        "<h3>Tätskikt och plattor</h3><p>Vi gör tätskiktet enligt GVK:s branschregler, dokumenterar det och kontrollerar lutningen löpande.</p>",
        "steg 2", f)
    s = rep(s,
        "<details><summary>Vem ansvarar för tätskiktet?</summary><p>Vi gör det och lämnar bilder på utförandet. Det är en del av jobbet, inte ett tillval.</p></details>",
        "<details><summary>Vem ansvarar för tätskiktet?</summary><p>Vi gör det. Som GVK-auktoriserade utför vi tätskiktet enligt GVK:s branschregler och låter en oberoende kontrollant granska arbetet. Du får dokumentationen. Det är en del av jobbet, inte ett tillval.</p></details>"
        "<details><summary>Vad innebär det att ni är GVK-auktoriserade?</summary><p>GVK står för Golv- &amp; Våtrumskontroll och är branschens kontrollsystem för våtrum. Auktorisationen betyder att vi jobbar enligt GVK:s branschregler och att en oberoende kontrollant granskar tätskiktsarbetet. Du får en kontrollrapport på jobbet — det är dokumentationen som gör att du står tryggt om något skulle hända.</p></details>",
        "FAQ synlig (+ny fråga)", f)
    s = rep(s,
        '"text": "Vi gör det och lämnar bilder på utförandet. Det är en del av jobbet, inte ett tillval."',
        '"text": "Vi gör det. Som GVK-auktoriserade utför vi tätskiktet enligt GVK:s branschregler och låter en oberoende kontrollant granska arbetet. Du får dokumentationen. Det är en del av jobbet, inte ett tillval."}}, '
        '{"@type": "Question", "name": "Vad innebär det att ni är GVK-auktoriserade?", "acceptedAnswer": {"@type": "Answer", "text": "GVK står för Golv- & Våtrumskontroll och är branschens kontrollsystem för våtrum. Auktorisationen betyder att vi jobbar enligt GVK:s branschregler och att en oberoende kontrollant granskar tätskiktsarbetet. Du får en kontrollrapport på jobbet."',
        "FAQ-schema (+ny fråga)", f)
    wr(f, s)

if __name__ == "__main__":
    print("1) Footer-trustline"); footer_lines()
    print("2) index.html");       patch_index()
    print("3) microcement.html"); patch_micro(); patch_micro_body()
    print("4) plattsattning.html"); patch_plat()
    print("Klart.")
