#!/usr/bin/env python3
# Bygger ckmaleri.se som statisk HTML. Kör: python3 build.py
import os, json, re, html

DOMAIN = "https://ckmaleri.se"
NAME = "CK Måleri & Golv"
PHONE_DISPLAY = "073-703 37 17"
PHONE_LINK = "+46" + "737033717"
EMAIL = "ckmaleri@gmail.com"
IG = "https://www.instagram.com/ckmaleri/"
IG_HANDLE = "@ckmaleri"
AREA_SHORT = "Uddevalla · Trestad"
CITIES = ["Uddevalla", "Trollhättan", "Vänersborg", "Ljungskile",
          "Lilla Edet", "Färgelanda", "Munkedal", "Sjuntorp"]
FORM_ACTION = "https://formsubmit.co/" + EMAIL
HAS_VIDEO = os.path.exists("assets/video.mp4")

def local_business():
    return {
        "@context": "https://schema.org",
        "@type": "HousePainter",
        "name": NAME,
        "url": DOMAIN + "/",
        "telephone": "+46 737 03 37 17",
        "email": EMAIL,
        "image": DOMAIN + "/assets/img/hero.jpg",
        "priceRange": "Offert efter besiktning",
        "address": {"@type": "PostalAddress", "addressLocality": "Uddevalla",
                    "addressRegion": "Västra Götalands län", "addressCountry": "SE"},
        "geo": {"@type": "GeoCoordinates", "latitude": "58.3494", "longitude": "11.9410"},
        "areaServed": [{"@type": "City", "name": c} for c in CITIES],
        "sameAs": [IG],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0",
                            "reviewCount": "15", "bestRating": "5"},
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Golvslipning", "url": DOMAIN + "/golvslipning.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Måleri och tapetsering", "url": DOMAIN + "/maleri-och-tapet.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Microcement", "url": DOMAIN + "/microcement.html"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Plattsättning", "url": DOMAIN + "/plattsattning.html"}},
        ],
    }

def faq_schema(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                 "item": DOMAIN + u} for i, (n, u) in enumerate(items)]}

def service_schema(svc_name, slug, desc, faq=None):
    g = [{"@context": "https://schema.org", "@type": "Service",
          "name": svc_name + " i Uddevalla och Trestad",
          "serviceType": svc_name, "description": desc,
          "url": DOMAIN + "/" + slug,
          "provider": {"@type": "HousePainter", "name": NAME, "telephone": "+46 737 03 37 17",
                       "url": DOMAIN + "/"},
          "areaServed": [{"@type": "City", "name": c} for c in CITIES]},
         crumbs_schema([("Start", "/"), (svc_name, "/" + slug)])]
    if faq:
        f = faq_schema(faq); f.pop("@context"); g.append(f)
    return {"@context": "https://schema.org", "@graph": g}

def head(title, desc, path, schema, extra_head="", robots="index,follow"):
    canon = DOMAIN + path
    return f"""<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/assets/img/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16382c">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/styles.css">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
{extra_head}</head>
<body>
<a class="skip" href="#main">Hoppa till innehåll</a>
"""

RING_SVG = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 '
            '19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 '
            '2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 '
            '1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')

def header(active=""):
    items = [("Golvslipning", "/golvslipning.html"), ("Måleri & tapet", "/maleri-och-tapet.html"),
             ("Microcement", "/microcement.html"), ("Plattsättning", "/plattsattning.html"),
             ("Våra jobb", "/#jobb"), ("Frågor", "/#fragor"), ("Kontakt", "/#kontakt")]
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if u == active else "", n)
        for n, u in items)
    return f"""<div class="topbar">
  <div class="wrap">
    <a href="tel:{PHONE_LINK}">{RING_SVG} {PHONE_DISPLAY}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span class="right">{AREA_SHORT} · kostnadsfri offert</span>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/">
      <span class="brand-mark" aria-hidden="true">CK</span>
      <span class="brand-text">{NAME}<small>{AREA_SHORT}</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Meny</button>
    <nav class="nav" id="nav" aria-label="Huvudmeny">{nav}</nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a>
      <a class="btn btn-primary" href="/#kontakt">Begär offert</a>
    </div>
  </div>
</header>
<a class="ring-tab" href="tel:{PHONE_LINK}" aria-label="Ring {PHONE_DISPLAY}">{RING_SVG} RING {PHONE_DISPLAY}</a>
"""

def footer():
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <span class="brand-mark" aria-hidden="true">CK</span>
      <div>
        <strong>{NAME}</strong>
        <p>Golvslipning, måleri, microcement och plattsättning i Uddevalla och Trestad.<br>
        Försäkrade · F-skatt · ROT-avdrag</p>
      </div>
    </div>
    <div class="footer-col">
      <strong>Tjänster</strong>
      <a href="/golvslipning.html">Golvslipning</a>
      <a href="/maleri-och-tapet.html">Måleri &amp; tapet</a>
      <a href="/microcement.html">Microcement</a>
      <a href="/plattsattning.html">Plattsättning</a>
    </div>
    <div class="footer-col">
      <strong>Områden</strong>
      <a href="/#omraden">Uddevalla</a>
      <a href="/#omraden">Trollhättan</a>
      <a href="/#omraden">Vänersborg</a>
      <a href="/#omraden">Ljungskile</a>
    </div>
    <div class="footer-col">
      <strong>Kontakt</strong>
      <a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
      <a href="{IG}" rel="noopener">{IG_HANDLE}</a>
      <a href="/integritetspolicy.html">Integritetspolicy</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span id="ar">2026</span> {NAME} · Uddevalla</span>
    <span>Hemsida av <a href="https://varmlandswebb.se" rel="noopener">Värmlandswebb</a></span>
  </div>
</footer>
<script src="/assets/app.js" defer></script>
</body>
</html>
"""

def form_card(title="Be om kostnadsfri offert", with_select=True):
    sel = """<label>Vad gäller det?
  <select name="Tjanst" required>
    <option value="">Välj…</option>
    <option>Golvslipning</option>
    <option>Måleri &amp; tapet</option>
    <option>Microcement</option>
    <option>Plattsättning</option>
    <option>Vet inte / något annat</option>
  </select>
</label>""" if with_select else ""
    return f"""<form class="form-card" method="POST" action="{FORM_ACTION}">
  <h3>{title}</h3>
  <input type="hidden" name="_subject" value="Offertförfrågan från ckmaleri.se">
  <input type="hidden" name="_next" value="{DOMAIN}/tack.html">
  <input type="hidden" name="_captcha" value="false">
  <input type="text" name="_honey" style="display:none">
  <label>Namn<input type="text" name="Namn" autocomplete="name" required></label>
  <label>Telefon<input type="tel" name="Telefon" autocomplete="tel" required></label>
  <label>E-post <span style="font-weight:400;color:#6d7a72">(frivilligt)</span>
    <input type="email" name="Epost" autocomplete="email"></label>
  {sel}
  <label>Kort om jobbet
    <textarea name="Meddelande" rows="4" required placeholder="T.ex. 45 kvm ekparkett i vardagsrum och hall som är repigt, vill ha matt yta."></textarea>
  </label>
  <button class="btn btn-primary" type="submit">Skicka förfrågan</button>
  <p class="form-note">Uppgifterna används bara för att svara på din förfrågan. Läs mer i
    <a href="/integritetspolicy.html">integritetspolicyn</a>.</p>
</form>
"""

# ---------------------------------------------------------------- startsida
def build_index():
    faq = [
        ("Vad kostar en golvslipning?",
         "Det avgörs av ytan, skicket och vilken behandling du vill ha. Du får ett riktmärke direkt på telefon och ett fast pris efter att vi tittat på golvet."),
        ("Kostar offerten något?",
         "Nej. Besiktning och offert är kostnadsfritt och du binder inte upp dig på något."),
        ("Kan jag använda ROT-avdrag?",
         "Ja, för arbete i din bostad. ROT ger 30 % av arbetskostnaden tillbaka, upp till ett tak per person och år. Vi drar av det direkt på fakturan och sköter ansökan."),
        ("Går mitt gamla golv att rädda?",
         "Nästan alltid. Så länge trät inte är genomgånget eller fuktskadat går det att slipa fram en fräsch yta. Ser vi att det inte är värt pengarna säger vi det."),
        ("Lack eller olja?",
         "Lack tål mer och är enklare att hålla rent. Olja ger en mattare och mer levande yta som går att bättra lokalt. Vi går igenom skillnaden så att du kan välja."),
        ("Vad är microcement?",
         "En tunn massa som läggs på golv, väggar och bänkskivor och ger en fogfri yta med stenkänsla. Den kan ofta läggas ovanpå befintligt underlag."),
        ("Gör ni tätskikt i badrum?",
         "Ja. Tätskiktet ska vara rätt utfört, annars hjälper varken kakel eller microcement. Det ingår när vi gör våtrum."),
        ("Var arbetar ni?",
         "Uddevalla, Trollhättan, Vänersborg och bygderna runtomkring. Ring om du är osäker på om vi kommer till dig."),
    ]
    faq_html = "".join(
        '<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in faq)
    cities = "".join('<li>%s</li>' % c for c in CITIES)

    hero_media = ('<div class="hero-bg"><video autoplay muted loop playsinline preload="auto" '
                  'poster="assets/img/hero.jpg">'
                  '<source src="assets/video.webm" type="video/webm">'
                  '<source src="assets/video.mp4" type="video/mp4"></video></div>'
                  ) if HAS_VIDEO else ('<div class="hero-bg"><img src="assets/img/hero.jpg" alt="'
                                       'Nyslipat fiskbensgolv i ek med kvällsljus över ytan" '
                                       'width="1600" height="893"></div>')

    body = f"""
<main id="main">
<section class="hero">
  {hero_media}
  <div class="hero-overlay"></div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow">Måleri &amp; golv i Uddevalla</p>
      <h1>Reporna sitter i ytan. <em>Inte i golvet.</em></h1>
      <p class="lead">Vi slipar trägolv, målar och tapetserar, lägger microcement och sätter kakel
        i Uddevalla och Trestad. Ett gäng, ett pris, en kontakt — och ytor som håller längre än du tror.</p>
      <ul class="hero-list">
        <li>Kostnadsfri besiktning och offert</li>
        <li>Fast pris innan vi börjar</li>
        <li>Försäkrade och F-skatt</li>
        <li>ROT-avdrag där det gäller</li>
      </ul>
      <div class="hero-cta">
        <a class="btn btn-primary" href="#kontakt">Begär kostnadsfri offert <span class="arrow">→</span></a>
        <a class="btn btn-light" href="tel:{PHONE_LINK}">Ring {PHONE_DISPLAY}</a>
      </div>
    </div>
    <aside class="hero-card">
      <strong>5,0 i snitt på 15 omdömen</strong>
      <span>Från Servicefinder. Vi frågar hellre än gissar, och städar efter oss.</span>
    </aside>
  </div>
</section>

<div class="trustbar">
  <div class="wrap">
    <div><b>Golvslipning</b> · parkett och fiskben</div>
    <div><b>Måleri &amp; tapet</b> · inne och ute</div>
    <div><b>Microcement</b> · fogfria ytor</div>
    <div><b>Plattsättning</b> · kakel och klinker</div>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Vad vi gör</p>
    <h2>Golv, väggar och våtrum — <em>utan att lämna över</em></h2>
    <p class="section-lead">Ett golv som slipas och ett badrum som kaklas hänger ihop: nivåer, lister,
      tätskikt och ordning. Vi gör allt själva, så du slipper samordna tre firmor och två tidsplaner.</p>
    <div class="svc-grid">
      <a class="svc" href="/golvslipning.html">
        <img src="/assets/img/tjanst-golvslipning.jpg" alt="Golvslipmaskin på ett trägolv under arbete" loading="lazy" width="290" height="200">
        <div class="svc-body">
          <h3>Golvslipning</h3>
          <p>Parkett, fiskben och gamla brädgolv slipas och behandlas om. Ofta är golvet du redan har bättre än det du tänkt köpa.</p>
          <ul><li>Parkett och fiskben</li><li>Gamla brädgolv</li><li>Lack, olja eller pigment</li></ul>
          <span class="svc-more">Läs mer <span class="arrow">→</span></span>
        </div>
      </a>
      <a class="svc" href="/maleri-och-tapet.html">
        <img src="/assets/img/tjanst-maleri.jpg" alt="Måleriarbete utvändigt på en rödmålad byggnad" loading="lazy" width="290" height="200">
        <div class="svc-body">
          <h3>Måleri &amp; tapet</h3>
          <p>Väggar, tak, fönster, dörrar och fasader. Vi spacklar och grundar ordentligt — annars syns fusket i dåligt ljus.</p>
          <ul><li>Invändigt och fasad</li><li>Tapetsering</li><li>Spackling och fog</li></ul>
          <span class="svc-more">Läs mer <span class="arrow">→</span></span>
        </div>
      </a>
      <a class="svc" href="/microcement.html">
        <img src="/assets/img/tjanst-microcement.jpg" alt="Badrum med fogfri microcementyta" loading="lazy" width="290" height="200">
        <div class="svc-body">
          <h3>Microcement</h3>
          <p>Fogfria ytor på golv, väggar och bänkskivor. Ett badrum i ett stycke, utan fogar som missfärgas.</p>
          <ul><li>Badrum och kök</li><li>Golv och väggar</li><li>Utan fogar</li></ul>
          <span class="svc-more">Läs mer <span class="arrow">→</span></span>
        </div>
      </a>
      <a class="svc" href="/plattsattning.html">
        <img src="/assets/img/tjanst-plattsattning.jpg" alt="Nylagt kakel i badrum med dusch och rund spegel" loading="lazy" width="290" height="200">
        <div class="svc-body">
          <h3>Plattsättning</h3>
          <p>Kakel och klinker i hall, kök och badrum — med tätskikt som är gjort rätt, inte bara snyggt på ytan.</p>
          <ul><li>Kakel och klinker</li><li>Hall, kök och badrum</li><li>Fogning och tätskikt</li></ul>
          <span class="svc-more">Läs mer <span class="arrow">→</span></span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section section-alt" id="jobb">
  <div class="wrap">
    <p class="eyebrow">Våra jobb</p>
    <h2>Bilder från <em>riktiga</em> jobb</h2>
    <p class="section-lead">Inga stockfoton. Det här är ytor vi gjort i Uddevalla med omnejd.</p>
    <div class="gallery">
      <figure class="fig">
        <img src="/assets/img/jobb-fiskben-slipat.jpg" alt="Fiskbensparkett i ek efter slipning" loading="lazy" width="400" height="300">
        <figcaption><b>Fiskben, slipat</b><br>Herringbone i ek — samma mönster, helt annan yta.</figcaption>
      </figure>
      <figure class="fig">
        <img src="/assets/img/jobb-nylackat.jpg" alt="Nylackat trägolv med ljusinfall från fönster" loading="lazy" width="400" height="300">
        <figcaption><b>Nylackat</b><br>Gammal parkett efter slipning och behandling.</figcaption>
      </figure>
      <figure class="fig">
        <img src="/assets/img/jobb-kulturhuset-scen.jpg" alt="Stor scenyta i trä under slipning" loading="lazy" width="400" height="300">
        <figcaption><b>Kulturhusets scen</b><br>Stor yta, tagen i etapper mellan bokningar.</figcaption>
      </figure>
      <figure class="fig">
        <img src="/assets/img/jobb-mitt-i-jobbet.jpg" alt="Trägolv halvvägs genom slipning med maskin i bild" loading="lazy" width="400" height="300">
        <figcaption><b>Mitt i jobbet</b><br>Halva golvet kvar att slipa ner till rent trä.</figcaption>
      </figure>
      <figure class="fig">
        <img src="/assets/img/jobb-ljust-och-rent.jpg" alt="Ljust och rent trägolv efter slipning" loading="lazy" width="400" height="300">
        <figcaption><b>Ljust och rent</b><br>Furugolv, färdigt och avdammat.</figcaption>
      </figure>
      <figure class="fig">
        <img src="/assets/img/jobb-maskinerna.jpg" alt="Golvslipmaskin av märket Bona på plats i lokalen" loading="lazy" width="400" height="300">
        <figcaption><b>Maskinerna på plats</b><br>Rätt maskin gör jämn yta — fel maskin gör ränder.</figcaption>
      </figure>
    </div>
    <p class="reviews-note">Fler jobb läggs upp löpande på
      <a href="{IG}" rel="noopener">{IG_HANDLE}</a>.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Så går det till</p>
    <h2>Du ska veta vad som händer, <em>hela vägen</em></h2>
    <ol class="steps">
      <li>
        <span class="step-num">1</span>
        <h3>Hör av dig</h3>
        <p>Ring eller skicka formuläret. Berätta vad det gäller och var — några rader räcker.</p>
      </li>
      <li>
        <span class="step-num">2</span>
        <h3>Kostnadsfri offert</h3>
        <p>Vi tittar på ytan, går igenom material och kulör och lämnar ett fast pris. Det kostar ingenting.</p>
      </li>
      <li>
        <span class="step-num">3</span>
        <h3>Vi gör jobbet</h3>
        <p>Vi slipar, målar, gjuter eller sätter kakel tills det är klart — och städar efter oss.</p>
      </li>
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Varför CK</p>
      <h2>Ett litet gäng med <em>rätt maskiner</em></h2>
      <p class="section-lead">Vi är inte störst. Vi är de som tar jobbet, gör det själva och svarar när du ringer.</p>
    </div>
    <dl class="facts">
      <div><dt>Fast pris skriftligt</dt><dd>Priset du får efter besiktning är priset. Inga tillägg när jobbet är igång.</dd></div>
      <div><dt>Egna slipmaskiner</dt><dd>Bona-maskiner och rätt slipsteg — därför blir ytan jämn och inte randig.</dd></div>
      <div><dt>Försäkrat</dt><dd>F-skatt, företags- och ansvarsförsäkring. Du kan lämna över nycklarna.</dd></div>
      <div><dt>ROT-avdrag</dt><dd>Där arbetet kvalificerar drar vi av det direkt på fakturan.</dd></div>
      <div><dt>Städat efter oss</dt><dd>Slipdamm och färgstänk följer inte med hem. Vi dammsuger och torkar av.</dd></div>
      <div><dt>En kontakt</dt><dd>Samma person från offert till färdigt jobb — ingen växel, inga mellanhänder.</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">Omdömen</p>
    <h2>Vad kunderna <em>säger</em></h2>
    <div class="reviews">
      <div class="review">
        <p>”Väldigt nöjd med slipning och behandling av mitt parkettgolv, det blev precis som jag hade hoppats på. Dessutom trevligt bemötande och bra kommunikation.”</p>
        <div class="who"><span class="avatar" style="background:#4a6fa5">I</span><span><b>Ingrid</b><small>Servicefinder · ekparkett</small></span></div>
      </div>
      <div class="review">
        <p>”Jag är jättenöjd med slipning och behandling av mitt furugolv samt trappor. De blev precis som jag hade tänkt mig.”</p>
        <div class="who"><span class="avatar" style="background:#c07a34">A</span><span><b>Annika</b><small>Servicefinder · furugolv och trappor</small></span></div>
      </div>
      <div class="review">
        <p>”Jäkligt duktiga och väldigt bra service fick man. Otroligt trevliga och hjälpsamma.”</p>
        <div class="who"><span class="avatar" style="background:#3f8f5e">M</span><span><b>Mladen</b><small>Servicefinder · golv och målning</small></span></div>
      </div>
    </div>
    <p class="reviews-note">Omdömena är hämtade från Servicefinder. Snitt 5,0 av 15 omdömen.</p>
  </div>
</section>

<section class="section section-alt" id="omraden">
  <div class="wrap">
    <p class="eyebrow">Områden</p>
    <h2>Uddevalla och <em>Trestad</em></h2>
    <p class="section-lead">Vi utgår från Uddevalla och jobbar i Trestad — Uddevalla, Trollhättan och
      Vänersborg — och i bygderna runtomkring. Är du osäker på om vi kommer till dig, ring och fråga.</p>
    <ul class="areas">{cities}</ul>
  </div>
</section>

<section class="section" id="fragor">
  <div class="wrap narrow">
    <p class="eyebrow">Vanliga frågor</p>
    <h2>Det folk frågar om <em>först</em></h2>
    <p class="section-lead">Pengar och risk först. Det praktiska kommer efter.</p>
    {faq_html}
  </div>
</section>

<section class="section section-alt" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <p class="eyebrow">Kontakt</p>
      <h2>Berätta vad du har för yta</h2>
      <p class="section-lead">Skicka några rader om jobbet, eller ring. Du får svar samma dag och
        förslag på tid för besiktning.</p>
      <ul class="contact-list">
        <li><span>Telefon</span><a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a></li>
        <li><span>E-post</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Instagram</span><a href="{IG}" rel="noopener">{IG_HANDLE}</a></li>
        <li><span>Område</span>Uddevalla · Trollhättan · Vänersborg</li>
      </ul>
    </div>
    {form_card("Berätta kort om jobbet")}
  </div>
</section>
</main>
"""
    title = "Måleri, golv och kakel i Uddevalla | CK Måleri & Golv"
    desc = ("Golvslipning, måleri, microcement och plattsättning i Uddevalla och Trestad. "
            "Försäkrade, ROT-avdrag och kostnadsfri offert. Ring 073-703 37 17.")
    page = head(title, desc, "/", local_business()) + header() + body + footer()
    write("index.html", page)
    return title, desc

# ---------------------------------------------------------------- tjänstesidor
def service_page(slug, nav_name, title, desc, h1, lead, img, img_alt,
                 intro_paras, checks, method, faq, price_note, related):
    faq_html = "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in faq)
    paras = "".join('<p>%s</p>' % p for p in intro_paras)
    check_html = "".join('<li>%s</li>' % c for c in checks)
    method_html = "".join(
        '<li><span class="step-num">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, t, d)
        for i, (t, d) in enumerate(method))
    rel = "".join('<a class="svc" href="%s"><div class="svc-body"><h3>%s</h3>'
                  '<p>%s</p><span class="svc-more">Läs mer <span class="arrow">→</span></span>'
                  '</div></a>' % (u, n, d) for n, u, d in related)
    body = f"""
<main id="main">
<section class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Brödsmulor"><a href="/">Start</a><span>/</span>{nav_name}</nav>
    <p class="eyebrow" style="margin-top:22px">Tjänst · Uddevalla &amp; Trestad</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
<div class="wrap page-media">
  <img src="{img}" alt="{img_alt}" width="1200" height="525">
</div>

<section class="section">
  <div class="wrap two-col prose">
    <div>
      <h2>{nav_name} — så gör vi</h2>
      {paras}
    </div>
    <div>
      <div class="price-box">{price_note}</div>
      <h3>Det här ingår</h3>
      <ul class="checks">{check_html}</ul>
      <p><a class="btn btn-primary" href="/#kontakt">Begär kostnadsfri offert <span class="arrow">→</span></a></p>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <p class="eyebrow">Arbetsgång</p>
    <h2>Från första samtal till <em>färdigt resultat</em></h2>
    <ol class="steps">{method_html}</ol>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">Frågor om {nav_name.lower()}</p>
    <h2>Vanliga frågor</h2>
    {faq_html}
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <p class="eyebrow">Mer vi gör</p>
    <h2>Andra tjänster</h2>
    <div class="svc-grid" style="grid-template-columns:repeat(3,1fr)">{rel}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>Kostnadsfri offert på {nav_name.lower()}</h2>
        <p style="margin:6px 0 0;color:#cfe3d6">Skicka några rader om ytan, eller ring — vi svarar samma dag.</p>
      </div>
      <div style="display:flex;gap:12px;flex-wrap:wrap">
        <a class="btn btn-primary" href="/#kontakt">Begär offert</a>
        <a class="btn btn-light" href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a>
      </div>
    </div>
  </div>
</section>
</main>
"""
    page = (head(title, desc, "/" + slug, service_schema(nav_name, slug, desc, faq))
            + header("/" + slug) + body + footer())
    write(slug, page)
    return title, desc

def build_services():
    out = []
    out.append(service_page(
        "golvslipning.html", "Golvslipning",
        "Golvslipning i Uddevalla och Trestad | CK Måleri & Golv",
        "Vi slipar och behandlar parkett, fiskben och gamla brädgolv i Uddevalla, Trollhättan och Vänersborg. Fast pris, ROT-avdrag och kostnadsfri offert.",
        "Slipning som får <em>ditt</em> golv att se nytt ut",
        "Under repor och grå yta ligger nästan alltid ett bra trägolv. Vi slipar fram det och behandlar det — lack, olja eller pigment.",
        "/assets/img/jobb-fiskben-slipat.jpg",
        "Fiskbensparkett i ek efter slipning och behandling",
        ["Ett trägolv som legat i trettio år har tjockt nog med trä kvar för att slipas om flera gånger. Det är därför ett gammalt golv ofta blir vackrare än ett nytt: årsringarna, mönstret och dimensionerna finns redan.",
         "Vi börjar med att titta på underlaget. Är trät fuktskadat, genomgånget eller ligger det ojämnt i förhållande till resten av huset säger vi det innan vi börjar — hellre ett tråkigt besked i tid än en överraskning halvvägs.",
         "Sedan slipar vi i flera steg, spacklar springor och kvistar, och behandlar ytan. Matt lack tål mer än folk tror, olja ger en mer levande yta som går att bättra lokalt. Vi går igenom skillnaden med dig, för det är du som ska leva med golvet."],
        ["Kostnadsfri bedömning av golvet på plats", "Slipning i flera steg, inte bara en övergång",
         "Spackling av springor och kvistar", "Kant- och trösklar slipas för hand",
         "Lack, olja, hårdvax eller pigment", "Trappor och mindre ytor tas med samma besök",
         "Dammsugning och avtorkning efteråt"],
        [("Hör av dig", "Ring eller skicka några rader om ytan — kvadratmeter, träslag och hur golvet ser ut i dag."),
         ("Vi tittar på golvet", "Vi kommer ut, känner på trät och säger vad som är möjligt. Det kostar ingenting."),
         ("Fast pris och datum", "Du får skriftligt pris och en tid. Sedan slipar vi, behandlar och städar.")],
        [("Behöver jag flytta ut medan ni slipar?", "Möbler flyttar vi undan tillsammans. Du behöver inte flytta ut, men räkna med att rummet inte går att använda under själva slipningen och torktiden."),
         ("Luktar det mycket?", "Vattenbaserad lack och olja luktar betydligt mindre än de gamla lösningsmedlen. Vi vädrar under arbetet och säger till om ett rum behöver stå tomt över natten."),
         ("Hur länge håller en slipning?", "Så länge ytbehandlingen klarar sig. Lack i hall och kök slits snabbare — då kan man bättra eller lägga ett nytt lager utan att slipa om allt."),
         ("Går det att slippa dammet?", "Det mesta fångas i maskinen. Vi maskerar dörrar och täcker ytor, men helt dammfritt blir det aldrig. Räknas med ärlig inställning, inte löften.")],
        "<p><strong>Priset sätts efter besiktning.</strong> Vi ger ett riktmärke direkt på telefon och ett fast pris när vi sett ytan. ROT-avdrag drar vi av direkt på fakturan där det gäller.</p>",
        [("Måleri &amp; tapet", "/maleri-och-tapet.html", "Väggar, tak, fönster och fasad — spacklat och grundat ordentligt."),
         ("Microcement", "/microcement.html", "Fogfria golv och väggar i badrum och kök."),
         ("Plattsättning", "/plattsattning.html", "Kakel och klinker med tätskikt som håller.")]))

    out.append(service_page(
        "maleri-och-tapet.html", "Måleri & tapet",
        "Måleri och tapetsering i Uddevalla | CK Måleri & Golv",
        "Invändig och utvändig målning, tapetsering, spackling och fasad i Uddevalla och Trestad. Fast pris, försäkrat och ROT-avdrag. Begär kostnadsfri offert.",
        "Måleri som ser färdigt ut <em>även</em> i kvällsljus",
        "Väggar, tak, fönster, dörrar och fasader. Vi lägger tiden på spackel, grundning och täckning — det är där ett måleri­jobb avgörs.",
        "/assets/img/tjanst-maleri.jpg",
        "Utvändigt måleriarbete på rödmålad byggnad",
        ["Ett måleriarbete som ska hålla börjar långt före första strykningen. Handlar det om utvändigt trä ska löst sittande färg bort, trät tvättas och grundas — målar man över gammal, dåligt fästande färg följer allt med inom ett par år.",
         "Invändigt handlar det mesta om underlaget. Spackel som inte torkat klart, hörn som är slarvigt satta eller gammal tapetlim som lämnats kvar syns direkt i släpljuset från ett fönster. Vi lägger tiden där i stället för att lägga på fler lager färg.",
         "Sedan målar vi. Kulörer går vi igenom med dig innan vi börjar, på provbit om du är osäker, så att du inte står med ett färdigt rum i fel ton."],
        ["Spackling, slipning och grundning", "Målning av väggar och tak",
         "Fönster, dörrar, lister och foder", "Tapetsering med mönsterpassning",
         "Borttagning av gammalt tapetlim", "Fasad, knutar och fönster utvändigt",
         "Täckning av möbler och golv, städat efteråt"],
        [("Hör av dig", "Berätta vilka rum eller vilken fasad det gäller och om något behöver lagas först."),
         ("Vi tittar och mäter", "Vi bedömer underlaget på plats och går igenom kulör och material."),
         ("Vi utför och städar", "Fast pris skriftligt innan start. Sedan är det bara att vänta på det färdiga resultatet.")],
        [("Kan ni tapetsera i badrum?", "Våtrumstapet går bra, men bara med rätt underlag och lim bakom. Vi kontrollerar det innan, annars lossnar tapeten i fukten."),
         ("Hur många strykningar behövs?", "Oftast två på vägg, och mer om du byter från mörk till ljus kulör. Det står i offerten så du vet vad du betalar för."),
         ("Måste jag flytta ut möblerna?", "Nej. Vi täcker och flyttar ihop. Plocka undan personliga saker och sådant som är ömtåligt."),
         ("Hur lång tid tar en fasad?", "Det beror på storlek och på hur mycket färg som måste skrapas. Vi ger en tidsplan i offerten, väderberoende utvändigt.")],
        "<p><strong>Fasta priser efter besiktning.</strong> Inga tillägg under arbetet. ROT-avdrag drar vi av direkt på fakturan för arbete i din bostad.</p>",
        [("Golvslipning", "/golvslipning.html", "Parkett, fiskben och gamla brädgolv — slipade och behandlade."),
         ("Microcement", "/microcement.html", "Fogfria ytor på golv, väggar och bänkskivor."),
         ("Plattsättning", "/plattsattning.html", "Kakel och klinker i hall, kök och badrum.")]))

    out.append(service_page(
        "microcement.html", "Microcement",
        "Microcement i Uddevalla och Trestad | CK Måleri & Golv",
        "Fogfria ytor med microcement på golv, väggar och bänkskivor i Uddevalla, Trollhättan och Vänersborg. Ofta ovanpå befintligt underlag. Kostnadsfri offert.",
        "Ett badrum i ett stycke, <em>utan fogar</em>",
        "Microcement ger en tunn, fogfri yta med stenkänsla — på golv, väggar och bänkskivor. Ofta kan du behålla underlaget du har.",
        "/assets/img/tjanst-microcement.jpg",
        "Badrum med fogfri microcementyta och glasdörr",
        ["Fogar är det som åldras först i ett badrum. De missfärgas, blir svåra att få rena och kräver till slut ny fog. Microcement läggs i tunna lager över hela ytan och ger i stället en sammanhängande yta utan skarvar att hålla efter.",
         "Det går att lägga på många underlag — kakel, betong, golvspån och vissa plastmaterial — förutsatt att underlaget sitter fast och är stabilt. Vi bedömer det på plats. Rör det sig eller är vått säger vi nej, för då spricker ytan oavsett hur snyggt det läggs.",
         "Resultatet är tåligt men inte oförstörbart. Vi går igenom hur du håller efter ytan, vilket är enkelt: milt rengöringsmedel och ingen skurborste."],
        ["Bedömning av underlaget", "Grundning och armering där det behövs",
         "Två till tre lager microcement", "Slipning mellan lagren",
         "Försegling i vald glans", "Fogfria golv, väggar och bänkskivor",
         "Rekommendationer för rengöring efteråt"],
        [("Bedömning", "Vi tittar på ytan och avgör om microcement är rätt — eller om du blir gladare av kakel."),
         ("Provyta och kulör", "Vi går igenom ton och glans innan hela ytan läggs."),
         ("Läggning och försegling", "Lagren läggs, slipas och förseglas. Ytan kan användas efter härdning.")],
        [("Kan microcement läggas ovanpå kakel?", "Ja, i många fall. Kravet är att plattorna sitter fast och att ytan är jämn. Har kakel börjat släppa måste det bort först."),
         ("Hur tåligt är det?", "Tåligt i normal användning, men det ska skötas milt. Skurmedel och skurborste sliter på förseglingen."),
         ("Funkar det i duschen?", "Ja, med rätt försegling och korrekt tätskikt bakom. Utan tätskikt ska det inte läggas i våtrum."),
         ("Hur länge innan ytan kan användas?", "Den går att gå på tidigare än man tror, men full belastning och blöta ytor väntar vi med. Exakt tid får du i offerten.")],
        "<p><strong>Pris efter besiktning.</strong> Microcement kostar mer i arbetstid än kakel men sparar underlag — och slipper fogar. Vi räknar på ditt badrum och du får siffran svart på vitt.</p>",
        [("Golvslipning", "/golvslipning.html", "Trägolv slipas och behandlas — ofta istället för nytt golv."),
         ("Måleri &amp; tapet", "/maleri-och-tapet.html", "Väggar, tak, fönster och fasad."),
         ("Plattsättning", "/plattsattning.html", "Kakel och klinker med tätskikt gjort rätt.")]))

    out.append(service_page(
        "plattsattning.html", "Plattsättning",
        "Plattsättning och kakel i Uddevalla | CK Måleri & Golv",
        "Plattsättning av kakel och klinker i hall, kök och badrum i Uddevalla och Trestad. Korrekt tätskikt, noggrann fogning och fast pris. Begär kostnadsfri offert.",
        "Plattor är enkla. <em>Tätskiktet</em> är det som gäller.",
        "Kakel och klinker i hall, kök och badrum — med tätskikt som är gjort rätt. Det är där badrum faktiskt håller eller inte.",
        "/assets/img/tjanst-plattsattning.jpg",
        "Nylagt kakel i badrum med dusch, handfat och rund spegel",
        ["Ett badrum kan se färdigt ut och ändå vara fel. Tätskiktet ligger bakom plattorna, osynligt för alla utom den som gjort jobbet. Är det slarvigt gjort märks det ett par år senare, som fukt i väggen eller en fog som aldrig torkar.",
         "Vi gör tätskikt enligt gällande regler och dokumenterar med bilder, så att du har papperen om något händer. Sedan sätter vi plattorna. Fall mot golvbrunn kontrolleras löpande, inte på slutet — lutning går inte att rätta efteråt.",
         "Fogning är sista intrycket. Vi går igenom färg och bredd med dig innan, och fogar och silikonar hörn och anslutningar med rätt produkt."],
        ["Tätskikt enligt reglerna, med bilddokumentation", "Fall mot golvbrunn kontrolleras under arbetet",
         "Kakel och klinker i hall, kök och badrum", "Fogning i vald färg och bredd",
         "Silikon i hörn och vid anslutningar", "Kapning och montering kring rör och blandare",
         "Städning och avtorkning efteråt"],
        [("Genomgång", "Vi tittar på rummet, underlaget och vad som behöver flyttas eller rivas."),
         ("Tätskikt och plattor", "Vi utför, dokumenterar tätskiktet och kontrollerar lutningen löpande."),
         ("Fogning och slutkontroll", "Fogat, silikonat och genomgånget tillsammans innan vi lämnar.")],
        [("Tar ni bort gamla plattor?", "Ja, när det behövs. Sitter de fast och ytan är jämn kan vi ibland lägga ovanpå, men vi säger till om det är fel väg att gå."),
         ("Vem ansvarar för tätskiktet?", "Vi gör det och lämnar bilder på utförandet. Det är en del av jobbet, inte ett tillval."),
         ("Kan ni klinkers i hall och kök?", "Ja. I hall och kök är klinker ofta rätt val — slitstarkt och lätt att hålla rent."),
         ("Får jag se något liknande jobb?", "Vi visar bilder på badrum vi gjort och du får prata med tidigare kunder om du vill.")],
        "<p><strong>Fast pris efter besiktning</strong>, där tätskikt, plattor, fog och silikon ingår. ROT-avdrag drar vi av på fakturan där det gäller.</p>",
        [("Golvslipning", "/golvslipning.html", "Parkett, fiskben och gamla brädgolv."),
         ("Måleri &amp; tapet", "/maleri-och-tapet.html", "Väggar, tak, fönster och fasad."),
         ("Microcement", "/microcement.html", "Fogfria badrum och kök — ofta ovanpå kakel.")]))
    return out

# ---------------------------------------------------------------- övrigt
def build_extra():
    title = "Tack för din förfrågan | CK Måleri & Golv"
    desc = "Vi har tagit emot din förfrågan och hör av oss samma dag."
    body = f"""
<main id="main">
<section class="page-head"><div class="wrap">
  <p class="eyebrow">Tack</p>
  <h1>Vi har fått din förfrågan</h1>
  <p class="lead">Du hör av oss samma dag — oftast inom någon timme. Har du bråttom, ring
    <a href="tel:{PHONE_LINK}" style="color:#8fd6a8">{PHONE_DISPLAY}</a>.</p>
</div></section>
<section class="section"><div class="wrap narrow prose">
  <p>Under tiden kan du läsa mer om det vi gör, eller se bilder från jobb vi gjort.</p>
  <p><a class="btn btn-primary" href="/">Till startsidan</a>
     <a class="btn btn-outline" href="{IG}" rel="noopener" style="margin-left:8px">{IG_HANDLE} på Instagram</a></p>
</div></section>
</main>
"""
    schema = {"@context": "https://schema.org", "@type": "WebPage", "name": title,
              "url": DOMAIN + "/tack.html"}
    page = (head(title, desc, "/tack.html", schema, robots="noindex,follow")
            + header() + body + footer())
    write("tack.html", page)

    # integritetspolicy
    title = "Integritetspolicy | CK Måleri & Golv"
    desc = "Så hanterar CK Måleri & Golv personuppgifter när du skickar en förfrågan via ckmaleri.se."
    body = f"""
<main id="main">
<section class="page-head"><div class="wrap">
  <p class="eyebrow">Integritet</p>
  <h1>Integritetspolicy</h1>
  <p class="lead">Vi samlar bara in det vi behöver för att kunna svara på din förfrågan och lämna offert.</p>
</div></section>
<section class="section"><div class="wrap narrow prose">
  <h2>Vilka uppgifter vi samlar in</h2>
  <p>När du skickar formuläret sparar vi namn, telefonnummer, e-postadress och den beskrivning du
     själv skriver om jobbet. Vi använder inga marknadsföringscookies och säljer inga uppgifter.</p>
  <h2>Varför</h2>
  <p>Uppgifterna används endast för att kontakta dig, boka besiktning och lämna offert. Det är vårt
     berättigade intresse att kunna svara på din förfrågan.</p>
  <h2>Hur länge vi sparar dem</h2>
  <p>Förfrågningar som inte leder till ett jobb raderas löpande. Blir det ett jobb sparas uppgifterna
     så länge det krävs för bokföring och garanti enligt bokföringslagen.</p>
  <h2>Vem som ser dem</h2>
  <p>Bara vi. Formuläret skickas via en e-posttjänst och uppgifterna lagras hos vår leverantör av
     webbhotell och e-post inom EU.</p>
  <h2>Dina rättigheter</h2>
  <p>Du kan begära att få se, rätta eller radera de uppgifter vi har om dig. Kontakta oss på
     <a href="mailto:{EMAIL}">{EMAIL}</a> eller ring <a href="tel:{PHONE_LINK}">{PHONE_DISPLAY}</a>.</p>
  <p style="margin-top:34px"><a class="btn btn-outline" href="/">Till startsidan</a></p>
</div></section>
</main>
"""
    schema = {"@context": "https://schema.org", "@type": "WebPage", "name": title,
              "url": DOMAIN + "/integritetspolicy.html"}
    page = (head(title, desc, "/integritetspolicy.html", schema)
            + header() + body + footer())
    write("integritetspolicy.html", page)

def relativize(h):
    """Gör interna absoluta sökvägar relativa så att sajten fungerar både på
    egen domän i roten och under en underkatalog (t.ex. GitHub Pages /ck-maleri/)."""
    h = re.sub(r'href="/#([^"]*)"', r'href="index.html#\1"', h)
    h = re.sub(r'href="/"', 'href="index.html"', h)
    h = re.sub(r'href="/([^"]*)"', r'href="\1"', h)
    h = re.sub(r'src="/([^"]*)"', r'src="\1"', h)
    h = re.sub(r'action="/([^"]*)"', r'action="\1"', h)
    return h

def write(path, content):
    if path.endswith(".html"):
        content = relativize(content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def build_sitemap_and_robots():
    urls = ["/", "/golvslipning.html", "/maleri-och-tapet.html", "/microcement.html",
            "/plattsattning.html", "/integritetspolicy.html"]
    prio = {"/": "1.0", "/integritetspolicy.html": "0.2"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>%s%s</loc><changefreq>monthly</changefreq>"
                  "<priority>%s</priority></url>" % (DOMAIN, u, prio.get(u, "0.8")))
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN)
    write("llms.txt", f"""# {NAME}

> Golvslipning, måleri och tapetsering, microcement och plattsättning i Uddevalla och Trestad
> (Uddevalla, Trollhättan, Vänersborg). Försäkrade, F-skatt, ROT-avdrag och kostnadsfri offert.

## Kontakt
- Telefon: {PHONE_DISPLAY}
- E-post: {EMAIL}
- Instagram: {IG}

## Tjänster
- [Golvslipning]({DOMAIN}/golvslipning.html): parkett, fiskben och gamla brädgolv slipas
  och behandlas med lack, olja eller pigment.
- [Måleri & tapet]({DOMAIN}/maleri-och-tapet.html): invändig och utvändig målning,
  tapetsering, spackling, fasad.
- [Microcement]({DOMAIN}/microcement.html): fogfria ytor på golv, väggar och bänkskivor,
  ofta ovanpå befintligt underlag.
- [Plattsättning]({DOMAIN}/plattsattning.html): kakel och klinker i hall, kök och badrum,
  tätskikt enligt reglerna.

## Områden
{cities_line()}
""")

def cities_line():
    return ", ".join(CITIES)

if __name__ == "__main__":
    rows = [build_index()] + build_services()
    build_extra()
    build_sitemap_and_robots()
    print("%-58s %5s %5s" % ("TITLE", "tlen", "mlen"))
    bad = 0
    for t, d in rows:
        ok = len(t) <= 62 and 115 <= len(d) <= 162
        bad += 0 if ok else 1
        print("%-58s %5d %5d %s" % (t[:56], len(t), len(d), "" if ok else "  <-- KOLLA"))
    print("\n%d sidor byggda, %d med längd utanför mål" % (len(rows) + 2, bad))
