#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger de tre norske landingssidene for CK Maleri & Golv (Ostfold).

Kjor:  python3 build_no.py

Skriver:
  halden.html, sarpsborg.html, fredrikstad.html   (norske landingssider)
  takk.html                                       (norsk takke-side for skjemaet)
Oppdaterer:
  Omraden-kolonnen i footeren pa alle svenske sider
  sitemap.xml
"""
import json, re, io, os

DOMAIN      = "https://ckmaleri.se"
NAME        = "CK Måleri & Golv"
PHONE_LINK  = "+46737033717"
PHONE_PRETTY = "+46 73 703 37 17"
EMAIL       = "ckmaleri@gmail.com"
CSS_V       = "9"
STREET      = "Föreningsgatan 12"
POSTAL      = "451 52"
LOCALITY    = "Uddevalla"
COUNTRY     = "SE"
OG_IMAGE    = DOMAIN + "/assets/img/og.jpg"
INSTAGRAM   = "https://www.instagram.com/ckmaleri/"
FACEBOOK    = "https://www.facebook.com/p/CK-M%C3%A5leri-Golv-100068038089752/"

PHONE_SVG = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 '
             '2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 '
             '2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 '
             '1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/></svg>')

# ---------------------------------------------------------------- stedsdata
CITIES = {
    "halden": {
        "file": "halden.html",
        "name": "Halden",
        "title": "Gulvsliper i Halden og Østfold | CK Måleri & Golv",
        "desc": ("Vi er gulvslipere i Halden og Østfold. Sliper parkett, fiskebensparkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),
        "h1": "Gulvsliping i Halden og Østfold",
        "hero_tag": ("Vi er gulvslipere fra Uddevalla. Skriftlig fastpris på forhånd, og vi kjører "
                     "over grensen til Halden med egne Bona-maskiner."),
        "areas": ["Halden", "Tistedal", "Idd", "Svinesund", "Rokke", "Asak", "Sponvika", "Berg"],
        "local_h": "Gulvsliping i Halden og omegn",
        "local_p": [
            "Halden er en gammel grenseby med mye trehusbebyggelse — empiregårder i sentrum, eldre "
            "villaer i Tistedal og Idd, og en lang rekke hytter langs Iddefjorden og opp mot Svinesund. "
            "Nettopp i den typen hus finner vi gulvene som er mest verdt å ta vare på: brede furuplanker, "
            "gammel fiskebensparkett og slitte parkettgulv som har fått tjue år med møbler og barneføtter.",
            "Vi sliper og behandler tregulv i hele Halden kommune — fra sentrum og Tistedal til Idd, "
            "Rokke, Asak og Sponvika. Parkettsliping og sliping av brede plankegulv er det vi gjør mest, "
            "men vi tar også malerarbeid, mikrosement på bad og flislegging. Fordi vi kjører over grensen "
            "fra Uddevalla har vi alltid med egne Bona-maskiner og alt materiell, så jobben går i ett.",
            "Mange av husene her er gamle, og da er det sjelden lurt å legge nytt gulv oppå det gamle. Et "
            "tregulv som har ligget i femti år er tørrere og mer stabilt enn det meste du får kjøpt i dag — "
            "det trenger bare å bli slipt ned til rent tre og behandlet på nytt. Ser vi at gulvet ikke er "
            "verdt å redde, sier vi det før vi begynner.",
            "Står du med et gammelt gulv og vurderer å leie inn gulvsliper, sender du bare noen bilder. Du "
            "får et realistisk anslag med en gang — og vi kommer på gratis befaring i Halden når det passer "
            "deg.",
        ],
    },
    "sarpsborg": {
        "file": "sarpsborg.html",
        "name": "Sarpsborg",
        "title": "Gulvsliper i Sarpsborg og Østfold | CK Måleri & Golv",
        "desc": ("Vi er gulvslipere i Sarpsborg og Østfold. Sliper parkett, fiskebensparkett og "
                 "gamle tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),
        "h1": "Gulvsliping i Sarpsborg og Østfold",
        "hero_tag": ("Vi er gulvslipere fra Uddevalla. Skriftlig fastpris på forhånd, og vi kjører "
                     "over grensen til Sarpsborg med egne Bona-maskiner."),
        "areas": ["Sarpsborg", "Grålum", "Borgenhaugen", "Skjeberg", "Hafslund", "Greåker", "Varteig", "Hafslundsøy"],
        "local_h": "Gulvsliping i Sarpsborg og omegn",
        "local_p": [
            "Sarpsborg er fylkessete i Østfold og har både eldre villaer og nyere blokker — og gulvene "
            "varierer deretter. I områder som Grålum, Borgenhaugen og Hafslund møter vi mye 90-tallsparkett "
            "som er slitt, mens de eldre husene i Skjeberg og Varteig ofte har brede tregulv som bare "
            "trenger å bli slipt fram igjen.",
            "Vi tar hele Sarpsborg kommune — sentrum, Grålum, Borgenhaugen, Skjeberg, Hafslund, Greåker "
            "og Varteig. Parkettsliping og sliping av gamle gulv er det vi gjør mest, men vi utfører også "
            "innvendig og utvendig malerarbeid, mikrosement og flislegging. Siden vi kommer fra Uddevalla "
            "over grensen, har vi med egne maskiner og gjør alt selv, uten å leie inn underleverandører.",
            "Den vanligste jobben her er en leilighet eller et hus der parketten har mistet glansen og "
            "blitt ripete i gangen, men egentlig er helt fin å redde. Da sliper vi ned, behandler, og du "
            "har et gulv som ser nytt ut — til en brøkdel av prisen for nytt gulv.",
            "Skal leiligheten friskes opp før salg, eller skal hele huset gjøres om? Send noen bilder og "
            "antall kvadratmeter, så får du et realistisk anslag allerede på telefon — og en skriftlig "
            "fastpris etter gratis befaring i Sarpsborg.",
        ],
    },
    "fredrikstad": {
        "file": "fredrikstad.html",
        "name": "Fredrikstad",
        "title": "Gulvsliper i Fredrikstad og Østfold | CK Måleri & Golv",
        "desc": ("Vi er gulvslipere i Fredrikstad, Hvaler og Østfold. Sliper parkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),
        "h1": "Gulvsliping i Fredrikstad og Østfold",
        "hero_tag": ("Vi er gulvslipere fra Uddevalla. Skriftlig fastpris på forhånd, og vi kjører "
                     "over grensen til Fredrikstad og Hvaler med egne Bona-maskiner."),
        "areas": ["Fredrikstad", "Kråkerøy", "Gressvik", "Begby", "Rolvsøy", "Onsøy", "Hvaler", "Cicignon"],
        "local_h": "Gulvsliping i Fredrikstad og på Hvaler",
        "local_p": [
            "Fredrikstad har en av Norges best bevarte festningsbyer, og i Gamlebyen og områdene rundt "
            "Cicignon står trehusene tett. Der er det sjelden rom for moderne gulv — det skal være plank, "
            "brede bord og overflater som tåler livet i et gammelt hus. Samtidig finner vi en helt annen "
            "type oppdrag på Kråkerøy, Gressvik, Begby og Rolvsøy: nyere eneboliger og rekkehus med "
            "parkett som er moden for sliping.",
            "Vi jobber i hele Fredrikstad og på Hvaler — også Onsøy og øyene — med gulvsliping, "
            "malerarbeid, mikrosement og flislegging. Kysten betyr mange hytter og fritidsboliger, og der "
            "er det ofte et slitent tregulv eller et bad som skal tåle fukt. Det tar vi oss av.",
            "I Gamlebyen og på Kråkerøy ligger det mange gamle plankegulv med bredder som ikke lages "
            "lenger. De er verdt å ta vare på, og med riktig parkettsliping og behandling holder de i "
            "flere tiår til. Hyttene på Hvaler har ofte gulv som har stått tomme og tørket ut — det fikser "
            "vi med sliping og olje eller lakk.",
            "Vi kjører opp fra Uddevalla via E6 og Svinesund med egne Bona-maskiner, og gjør jobben selv "
            "fra start til slutt. Noen bilder og cirka antall kvadratmeter er nok for et første anslag.",
        ],
    },
}
ORDER = ["halden", "sarpsborg", "fredrikstad"]

# ------------------------------------------------------------------ skjema
def local_business(c):
    data = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "@id": DOMAIN + "/" + c["file"] + "#business",
        "name": NAME,
        "url": DOMAIN + "/" + c["file"],
        "image": OG_IMAGE,
        "description": ("Gulvsliping, malerarbeid, mikrosement og flislegging i " + c["name"] +
                        " og Østfold — utført av CK Måleri & Golv fra Uddevalla, med over 15 års erfaring."),
        "telephone": PHONE_LINK,
        "email": EMAIL,
        "priceRange": "Fastpris etter befaring",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": STREET,
            "postalCode": POSTAL,
            "addressLocality": LOCALITY,
            "addressCountry": COUNTRY,
        },
        "areaServed": [
            {"@type": "City", "name": c["name"]},
            {"@type": "AdministrativeArea", "name": "Østfold"},
        ],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "07:00", "closes": "20:00",
        }],
        "sameAs": [INSTAGRAM, FACEBOOK],
        "parentOrganization": {"@type": "Organization", "name": NAME, "url": DOMAIN + "/"},
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

def faq_pairs(c):
    return [
        ("Koster det noe å få dere på befaring i %s?" % c["name"],
         "Nei, befaring og pristilbud er helt gratis og uforpliktende."),
        ("Hvordan fungerer prising og fakturering når dere holder til i Sverige?",
         "Du får en skriftlig fastpris før vi starter. Ingen skjulte tillegg for reise eller bompenger "
         "etter at prisen er avtalt."),
        ("Hva koster gulvsliping per kvadratmeter?",
         "Det avhenger av tregulvets tilstand, hvor mye som må slipes ned og hvilken behandling du "
         "velger. Du får et anslag på telefon og en skriftlig fastpris etter befaring."),
        ("Kan mitt gamle tregulv eller parkettgulv reddes?",
         "Nesten alltid. Så lenge treet ikke er gjennomslitt eller fuktskadet, går det å slipe fram en "
         "frisk overflate. Er det ikke verdt pengene, sier vi det."),
        ("Hvor lang tid tar det før dere kan starte i %s?" % c["name"],
         "Vi planlegger befaring raskt, som regel innen et par uker, og setter av sammenhengende dager "
         "til jobben så vi blir ferdige i én runde."),
        ("Kan svensker med bolig eller hytte i Norge bruke ROT-fradrag?",
         "Ja, dersom du skatter i Sverige og eier boligen eller hytta i Norge, gjelder svensk "
         "ROT-fradrag innen EØS. Si fra ved befaring, så ser vi på det."),
        ("Blir arbeidet på bad godkjent?",
         "Ja. Vi er GVK-auktoriserte og utfører tettesjikt etter GVK sine bransjeregler. Arbeidet "
         "kontrolleres av en uavhengig kontrollør, og du får dokumentasjonen skriftlig."),
    ]

def faq_schema(c):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq_pairs(c)
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))

def faq_html(c):
    out = []
    for q, a in faq_pairs(c):
        out.append("<details><summary>%s</summary><p>%s</p></details>" % (q, a))
    return "".join(out)

def areas_links(c):
    out = []
    for key in ORDER:
        if key == c["key"]:
            out.append("<b>%s</b>" % CITIES[key]["name"])
        else:
            out.append('<a href="%s">%s</a>' % (CITIES[key]["file"], CITIES[key]["name"]))
    return " | ".join(out)

# ------------------------------------------------------------------ mal
SVC_FEATURE = {
    "href": "golvslipning.html",
    "img": "assets/img/tj-golv.webp",
    "alt": "Lyst ferdigslipet tregulv i et moderne kjøkken",
    "h3": "Gulvsliping",
    "body": ("Vi tar gulvet ned til rent tre, kontrollerer med lampe mellom hvert steg og legger valgt "
             "overflate — lakk, olje eller pigment. Gamle gulv blir ofte bedre enn det du planla å kjøpe."),
    "bullets": ["Parkett og fiskebensparkett", "Gamle tregulv og plankegulv",
                "Lakk, olje eller pigment", "Støysvakt og nesten støvfritt"],
}

# Sekundære tjenester — bevisst nedtonet. Flislegging først, malerarbeid sist.
SVC_MINI = [
    ("plattsattning.html", "assets/img/tj-plattsattning.webp",
     "Bad med store grå fliser, vegghengt toalett, servant og glassdusj",
     "Flislegging",
     "Fliser i gang, kjøkken og bad — med tettesjikt utført etter GVK sine bransjeregler.",
     ["Fliser og klinker", "Fuging og tettesjikt"]),
    ("microcement.html", "assets/img/tj-microcement.webp",
     "Bøtte merket Mikrosement og sparkelspader på et nylagt fugefritt gulv",
     "Mikrosement",
     "Fugefrie overflater på bad, gulv og vegger — ofte rett på eksisterende fliser.",
     ["Bad og kjøkken", "Helt fugefritt"]),
    ("maleri-och-tapet.html", "assets/img/tj-maleri.webp",
     "Maleruller som drar lys farge over en jevn vegg",
     "Malerarbeid &amp; tapet",
     "Vegger, tak, vinduer og fasader, samt sparkling og tapetsering når det trengs.",
     ["Innvendig og fasade", "Sparkling og fuging"]),
]

GALLERY = [
    ("assets/img/jobb-ladugard.webp?v=4", "Gulvslipemaskin på et gammelt tregulv i en låve, halve gulvet nyslipt",
     "Gulvet i låven", "Gammelt tregulv — halve flaten allerede slipt ned til rent tre.", 768, 1280),
    ("assets/img/jobb-bona-fiskben.webp?v=3", "Fiskebensparkett der den ene halvdelen er slipt og den andre venter, Bona-maskin på gulvet",
     "Midt i jobben", "Fiskebensparkett — én side nyslipt, den andre venter.", 768, 1280),
    ("assets/img/jobb-scen-ny.webp", "Parkettgulv i en stor sal med blå veggpaneler under behandling",
     "Scenen i kulturhuset", "Stor flate, parkettgulvet tatt i etapper.", 960, 1280),
    ("assets/img/jobb-kok.webp", "Moderne kjøkken med lyst tregulv og store skyvedører",
     "Lyst og ferdig", "Lyst tregulv i et moderne kjøkken, ferdig.", 960, 1280),
    ("assets/img/jobb-krona-ny.webp", "Parkettgulv i et sekelskifterom med krystallkrone og speil",
     "Sekelskifterrommet", "Krystallkrone, speil og nyslipt parkett.", 960, 1280),
]

USP = [
    ("Svensk prisnivå og skriftlig fastpris",
     "Konkurransedyktige priser og en gunstig kronekurs — alltid med skriftlig fastpris etter befaring."),
    ("Kort vei via E6",
     "Vi kjører rett opp E6 over Svinesund og er i {city} på rundt en time for gratis befaring."),
    ("Over 15 års erfaring og egne Bona-maskiner",
     "Støysvak og tilnærmet støvfri sliping."),
    ("Én kontaktperson hele veien",
     "Vi koordinerer gulv, maling, mikrosement og fliser selv."),
    ("Ryddig og rengjort",
     "Vi støvsuger, vasker av og rydder alltid etter oss."),
    ("Forsikret og GVK-auktorisert",
     "Ansvarsforsikring og ryddige avtaler. Vi er GVK-auktoriserte, så tettesjikt i våtrom "
     "kontrolleres av en uavhengig kontrollør."),
]

TOPBAR = """<div class="topbar">
  <div class="wrap">
    <a href="tel:{phone_link}">{phone_svg15} {phone_pretty}</a>
    <a href="mailto:{email}">{email}</a>
    <span class="right">Halden · Sarpsborg · Fredrikstad · Gratis befaring</span>
  </div>
</div>"""

HEADER = """<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="./"><img class="brand-logo" src="assets/img/logo.webp" alt="CK Måleri &amp; Golv" width="1400" height="582"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Meny</button>
    <nav class="nav" id="nav" aria-label="Hovedmeny"><a href="#tjenester">Tjenester</a><a href="#prosjekter">Prosjekter</a><a href="#hvorfor">Hvorfor oss</a><a href="#ostfold">Østfold</a><a href="#faq">Spørsmål</a><a href="#kontakt">Kontakt</a><div class="nav-cta"><a class="btn btn-primary" href="#kontakt">Bestill gratis befaring <span class="arrow">→</span></a><a class="btn btn-outline nav-cta-call" href="tel:{phone_link}">Ring {phone_pretty}</a></div></nav>
    <div class="header-cta">
      <a class="header-phone" href="tel:{phone_link}">{phone_pretty}</a>
      <a class="btn btn-primary" href="#kontakt">Bestill befaring</a>
    </div>
  </div>
</header>
<a class="ring-tab" href="tel:{phone_link}" aria-label="Ring {phone_pretty}">{phone_svg15} RING {phone_pretty}</a>"""

HERO = """<section class="hero">
  <div class="hero-bg"><video autoplay muted loop playsinline preload="auto" poster="assets/img/hero.webp"><source src="assets/video.webm" type="video/webm"><source src="assets/video.mp4" type="video/mp4"></video></div>
  <div class="hero-overlay"></div>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow hero-eyebrow">CK Måleri &amp; Golv · {city} og Østfold · Kun en drøy time via E6</p>
      <h1 class="hero-title">Gulvsliping<span class="hero-title-sub">i {city} og Østfold</span></h1>
      <p class="hero-sub">Sliping av parkett, fiskebensparkett og gamle tregulv</p>
      <p class="hero-tag">{hero_tag}</p>
      <div class="hero-cta">
        <a class="btn btn-primary btn-lg" href="#kontakt">Bestill gratis befaring <span class="arrow">→</span></a>
        <a class="btn btn-outline btn-lg" href="tel:{phone_link}">{phone_svg17} Ring {phone_pretty}</a>
      </div>
      <p class="hero-trust">★★★★★ <b>5,0 av 5</b> i snittkarakter — 15 oppdrag via Servicefinder</p>
    </div>
  </div>
</section>"""

SERVICES = """<section class="section" id="tjenester">
  <div class="wrap">
    <p class="eyebrow">Det vi gjør best</p>
    <h2>Spesialister på <em>sliping av tregulv og parkett</em></h2>
    <p class="section-lead">Gamle furugulv, fiskebensparkett og slitt eikeparkett — vi sliper og behandler
      til en overflate som holder. Sliping av parkett og gamle plankegulv er det vi gjør mest, med egne
      Bona-maskiner, støysvakt og tilnærmet støvfritt. Skriftlig fastpris etter befaring i {city}.</p>
    <div class="svc-grid svc-grid--floor">
{feature}

{secondary}
    </div>
    <p class="reviews-note" style="margin-top:var(--sp-6)">Vi utfører også flislegging, mikrosement og
      malerarbeid — men gulvsliping er det vi lever av. Send gjerne en melding om du er usikker på hva
      gulvet ditt trenger.</p>
  </div>
</section>"""

WHY = """<section class="section section-pine" id="hvorfor">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Hvorfor oss</p>
      <h2>Hvorfor velge et <em>svensk team</em> i {city} og Østfold?</h2>
      <p class="section-lead">Vi er ikke størst. Vi er de som tar jobben, gjør den selv og svarer når du ringer.</p>
    </div>
    <dl class="facts">
{facts}
    </dl>
  </div>
</section>"""

GALLERY_HTML = """<section class="section section-alt" id="prosjekter">
  <div class="wrap">
    <p class="eyebrow">Våre prosjekter</p>
    <h2>Bilder fra <em>ekte</em> prosjekter</h2>
    <p class="section-lead">Ingen stockfoto. Dette er overflater vi har gjort i Uddevalla med omegn.</p>
    <div class="gallery">
{figs}
    </div>
    <p class="reviews-note jobs-cta">Vil du se hva vi kan gjøre med dine overflater?
      <a href="#kontakt">Be om et gratis prisforslag <span class="arrow">→</span></a></p>
  </div>
</section>"""

LOCAL = """<section class="section" id="ostfold">
  <div class="wrap narrow">
    <p class="eyebrow">Lokalt i Østfold</p>
    <h2>{local_h}</h2>
    <div class="prose">
{local_p}
      <p class="section-lead" style="margin:26px 0 0">Vi jobber i hele Østfold: {city_links}.</p>
    </div>
  </div>
</section>"""

FAQ = """<section class="section section-alt" id="faq">
  <div class="wrap narrow">
    <p class="eyebrow">Ofte stilte spørsmål</p>
    <h2>Ofte stilte spørsmål fra <em>kunder i Norge</em></h2>
    <p class="section-lead">Penger og risiko først. Det praktiske kommer etter.</p>
{faq}
  </div>
</section>"""

CONTACT = """<section class="section" id="kontakt">
  <div class="wrap contact-grid">
    <div>
      <p class="eyebrow">Kontakt</p>
      <h2>Fortell oss om oppdraget ditt</h2>
      <p class="section-lead">Send noen linjer om jobben, eller ring. Du får svar samme dag og forslag
        til tid for befaring i {city}.</p>
      <p class="contact-call">Vil du heller ringe?
        <a href="tel:{phone_link}">Slå på tråden: {phone_pretty}</a></p>
    </div>
    <form class="form-card" method="POST" action="https://formsubmit.co/{email}">
  <h3>Fortell kort om oppdraget</h3>
  <input type="hidden" name="_subject" value="Befaring fra ckmaleri.se ({city})">
  <input type="hidden" name="_next" value="{domain}/takk.html">
  <input type="hidden" name="_captcha" value="false">
  <input type="text" name="_honey" style="display:none">
  <label>Navn<input type="text" name="Navn" autocomplete="name" required></label>
  <label>Telefon<input type="tel" name="Telefon" inputmode="tel" autocomplete="tel" required></label>
  <label>E-post <span style="font-weight:400;color:#6d7a72">(valgfritt)</span>
    <input type="email" name="Epost" autocomplete="email"></label>
  <label>Hva gjelder det?
  <select name="Tjeneste" required>
    <option value="">Velg…</option>
    <option>Gulvsliping</option>
    <option>Malerarbeid &amp; tapet</option>
    <option>Mikrosement</option>
    <option>Flislegging</option>
    <option>Vet ikke / noe annet</option>
  </select>
</label>
  <label>Sted <span style="font-weight:400;color:#6d7a72">(f.eks. {city})</span>
    <input type="text" name="Sted" autocomplete="address-level2"></label>
  <label>Fortell kort om oppdraget og ca. antall kvm
    <textarea name="Melding" rows="4" required placeholder="F.eks. 45 kvm gammel furuparkett i stue og gang som er ripete, ønsker matt overflate."></textarea>
  </label>
  <button class="btn btn-primary" type="submit">Send forespørsel</button>
  <p class="form-note">Opplysningene brukes kun til å svare på forespørselen din. Les mer i
    <a href="integritetspolicy.html">personvernerklæringen</a>.</p>
</form>

  </div>
</section>"""

FOOTER = """<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img class="brand-logo footer-logo" src="assets/img/logo.webp" alt="CK Måleri &amp; Golv" width="1400" height="582">
      <div>
        <strong>CK Måleri &amp; Golv</strong>
        <p>Gulvsliping, malerarbeid, mikrosement og flislegging i Uddevalla og Østfold.<br>
        {street}, {postal} {locality}<br>
        Over 15 års erfaring · Forsikret · GVK-auktorisert · Fastpris etter befaring</p>
      </div>
    </div>
    <div class="footer-col">
      <strong>Tjenester</strong>
      <a href="golvslipning.html">Gulvsliping</a>
      <a href="maleri-och-tapet.html">Malerarbeid &amp; tapet</a>
      <a href="microcement.html">Mikrosement</a>
      <a href="plattsattning.html">Flislegging</a>
    </div>
    <div class="footer-col">
      <strong>Områder</strong>
      <a href="halden.html">Halden</a>
      <a href="sarpsborg.html">Sarpsborg</a>
      <a href="fredrikstad.html">Fredrikstad</a>
      <a href="index.html">Uddevalla og Trestad</a>
    </div>
    <div class="footer-col">
      <strong>Kontakt</strong>
      <a href="tel:{phone_link}">{phone_pretty}</a>
      <a href="mailto:{email}">{email}</a>
      <a href="{instagram}" rel="noopener">@ckmaleri på Instagram</a>
      <a href="{facebook}" rel="noopener">CK Måleri &amp; Golv på Facebook</a>
      <a href="integritetspolicy.html">Personvern</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <span id="ar">2026</span> CK Måleri &amp; Golv · Uddevalla</span>
    <span>Nettside av <a href="https://varmlandswebb.se" rel="noopener">Värmlandswebb</a></span>
  </div>
</footer>"""

PAGE = """<!DOCTYPE html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="website">
<meta property="og:locale" content="nb_NO">
<meta property="og:site_name" content="CK Måleri &amp; Golv">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16382c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/styles.css?v={css_v}">
<script type="application/ld+json">{schema}</script>
<script type="application/ld+json">{faq_schema}</script>
</head>
<body>
<a class="skip" href="#main">Hopp til innhold</a>
{topbar}
{header}

<main id="main">
{hero}

{services}

{gallery}

{why}

{local}

{faq_section}

{contact}
</main>
{footer}
<script src="assets/app.js?v={css_v}" defer></script>
</body>
</html>
"""

TAKK_PAGE = """<!DOCTYPE html>
<html lang="nb">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Takk for forespørselen | CK Måleri &amp; Golv</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{domain}/takk.html">
<meta name="theme-color" content="#16382c">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/styles.css?v={css_v}">
</head>
<body>
<a class="skip" href="#main">Hopp til innhold</a>
{topbar}
{header}
<main id="main">
<section class="section">
  <div class="wrap narrow">
    <p class="eyebrow">Takk</p>
    <h2>Vi har mottatt forespørselen din</h2>
    <p class="section-lead">Du hører fra oss samme dag, som regel innen et par timer på dagtid. Har du
      hastverk, kan du ringe direkte.</p>
    <p class="contact-call">Ring gjerne:
      <a href="tel:{phone_link}">{phone_pretty}</a></p>
    <p style="margin-top:32px"><a class="btn btn-primary" href="./">Tilbake til forsiden <span class="arrow">→</span></a></p>
  </div>
</section>
</main>
{footer}
<script src="assets/app.js?v={css_v}" defer></script>
</body>
</html>
"""


def fmt(html, **kw):
    return html.format(**kw)


def build_page(key):
    c = dict(CITIES[key])
    c["key"] = key
    common = dict(
        phone_link=PHONE_LINK, phone_pretty=PHONE_PRETTY, email=EMAIL,
        phone_svg15=PHONE_SVG.format(s=15), phone_svg17=PHONE_SVG.format(s=17),
        css_v=CSS_V, domain=DOMAIN, og_image=OG_IMAGE,
        street=STREET, postal=POSTAL, locality=LOCALITY,
        instagram=INSTAGRAM, facebook=FACEBOOK,
    )
    kw = dict(common)
    kw.update(dict(
        title=c["title"], desc=c["desc"], canonical=DOMAIN + "/" + c["file"],
        schema=local_business(c), faq_schema=faq_schema(c),
        city=c["name"], h1=c["h1"], hero_tag=c["hero_tag"],
    ))
    kw.update(dict(
        topbar=fmt(TOPBAR, **common),
        local_p="\n".join("      <p>%s</p>" % p for p in c["local_p"]),
        city_links=areas_links(c),
        faq=faq_html(c),
        header=fmt(HEADER, **common),
        footer=fmt(FOOTER, **common),
        hero=fmt(HERO, **kw),
        services=fmt(SERVICES, city=c["name"], feature=svc_feature(), secondary=svc_mini()),
        gallery=fmt(GALLERY_HTML, figs=gallery_figs()),
        why=fmt(WHY, city=c["name"], facts=usp_dl(c["name"])),
        local=fmt(LOCAL, local_h=c["local_h"],
                  local_p="\n".join("      <p>%s</p>" % p for p in c["local_p"]),
                  city_links=areas_links(c)),
        faq_section=fmt(FAQ, faq=faq_html(c)),
        contact=fmt(CONTACT, **common, city=c["name"]),
    ))
    return fmt(PAGE, **kw)


def svc_feature():
    c = SVC_FEATURE
    li = "".join("<li>%s</li>" % b for b in c["bullets"])
    return (
        '      <a class="svc svc-feature" href="%s">\n'
        '        <img src="%s" alt="%s" loading="lazy" width="800" height="600">\n'
        '        <div class="svc-body">\n'
        '          <h3>%s</h3>\n'
        '          <p>%s</p>\n'
        '          <ul>%s</ul>\n'
        '          <span class="svc-more">Les om gulvsliping <span class="arrow">→</span></span>\n'
        '        </div>\n'
        '      </a>' % (c["href"], c["img"], c["alt"], c["h3"], c["body"], li))


def svc_mini():
    out = []
    for href, img, alt, h3, body, bullets in SVC_MINI:
        li = "".join("<li>%s</li>" % b for b in bullets)
        out.append(
            '      <a class="svc svc--mini" href="%s">\n'
            '        <img src="%s" alt="%s" loading="lazy" width="600" height="600">\n'
            '        <div class="svc-body">\n'
            '          <h3>%s</h3>\n'
            '          <p>%s</p>\n'
            '          <ul>%s</ul>\n'
            '          <span class="svc-more">Les mer <span class="arrow">→</span></span>\n'
            '        </div>\n'
            '      </a>' % (href, img, alt, h3, body, li))
    return "\n".join(out)


def gallery_figs():
    out = []
    for src, alt, cap, desc, w, h in GALLERY:
        out.append(
            '      <figure class="fig">\n'
            '        <img src="%s" alt="%s" loading="lazy" width="%d" height="%d">\n'
            '        <figcaption><b>%s</b><br>%s</figcaption>\n'
            '      </figure>' % (src, alt, w, h, cap, desc))
    return "\n".join(out)


def usp_dl(city):
    out = []
    for dt, dd in USP:
        out.append("      <div><dt>%s</dt><dd>%s</dd></div>" % (dt, dd.format(city=city)))
    return "\n".join(out)


def write(name, content):
    with io.open(name, "w", encoding="utf-8") as f:
        f.write(content)
    print("  skrev %-22s %6d tecken" % (name, len(content)))


# -------------------------------------------------- svensk footer-oppdatering
NO_LINKS_OLD = ('      <a href="#omraden">Ljungskile</a>')
NO_LINKS_NEW = ('      <a href="#omraden">Ljungskile</a>\n'
                '      <a href="halden.html">Halden</a>\n'
                '      <a href="sarpsborg.html">Sarpsborg</a>\n'
                '      <a href="fredrikstad.html">Fredrikstad</a>')
NO_LINKS_OLD2 = ('      <a href="./#omraden">Ljungskile</a>')
NO_LINKS_NEW2 = ('      <a href="./#omraden">Ljungskile</a>\n'
                 '      <a href="halden.html">Halden</a>\n'
                 '      <a href="sarpsborg.html">Sarpsborg</a>\n'
                 '      <a href="fredrikstad.html">Fredrikstad</a>')

def patch_swedish_footers():
    files = ["index.html", "golvslipning.html", "maleri-och-tapet.html", "microcement.html",
             "plattsattning.html", "404.html", "integritetspolicy.html", "tack.html"]
    for fn in files:
        if not os.path.exists(fn):
            print("  hoppar over (saknas): %s" % fn)
            continue
        s = io.open(fn, encoding="utf-8").read()
        if 'href="halden.html"' in s:
            print("  %-24s redan uppdaterad" % fn)
            continue
        if NO_LINKS_OLD2 in s:
            s = s.replace(NO_LINKS_OLD2, NO_LINKS_NEW2, 1)
        elif NO_LINKS_OLD in s:
            s = s.replace(NO_LINKS_OLD, NO_LINKS_NEW, 1)
        else:
            print("  VARNING: hittade inget Ljungskile-anchor i %s" % fn)
            continue
        write(fn, s)


def patch_sitemap():
    fn = "sitemap.xml"
    s = io.open(fn, encoding="utf-8").read()
    if "halden.html" in s:
        print("  sitemap redan uppdaterad")
        return
    add = []
    for key in ORDER:
        add.append('  <url><loc>%s/%s</loc><lastmod>%s</lastmod>'
                   '<changefreq>monthly</changefreq><priority>0.7</priority></url>'
                   % (DOMAIN, CITIES[key]["file"], "2026-11-02"))
    s = s.replace("</urlset>", "\n".join(add) + "\n</urlset>")
    write(fn, s)


if __name__ == "__main__":
    print("Bygger norske landingssider ...")
    for key in ORDER:
        write(CITIES[key]["file"], build_page(key))
    print("Bygger takk.html ...")
    c = dict(CITIES["halden"])
    common = dict(phone_link=PHONE_LINK, phone_pretty=PHONE_PRETTY, email=EMAIL,
                  phone_svg15=PHONE_SVG.format(s=15), css_v=CSS_V, domain=DOMAIN,
                  instagram=INSTAGRAM, facebook=FACEBOOK, street=STREET, postal=POSTAL,
                  locality=LOCALITY, og_image=OG_IMAGE)
    write("takk.html", fmt(TAKK_PAGE, **common,
                           topbar=fmt(TOPBAR, **common),
                           header=fmt(HEADER, **common),
                           footer=fmt(FOOTER, **common)))
    print("Oppdaterer svenske footere ...")
    patch_swedish_footers()
    print("Oppdaterer sitemap.xml ...")
    patch_sitemap()
    print("Klart.")
