#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEO-forbedring av de norske stadssidene (basert pa soketall for Norge):
- 'gulvsliper' (1000/mnd) og 'parkettsliping' (110/mnd) inn i tekstene
- meta-descriptions trimmet til under 160 tegn (audit: for lange)
- lengre, mer unike lokale seksjoner per by (mindre duplikat-risiko)
Kor: python3 seo_no.py
"""
import io

F = "build_no.py"
s = io.open(F, encoding="utf-8").read()

def rep(old, new, label):
    global s
    assert s.count(old) == 1, "HITTADE %d av [%s]" % (s.count(old), label)
    s = s.replace(old, new, 1)
    print("  ok:", label)

# ---------------------------------------------------------------- 1. TITLAR
rep('"title": "Gulvsliping i Halden og Østfold | CK Måleri & Golv"',
    '"title": "Gulvsliping og gulvsliper i Halden og Østfold | CK Måleri & Golv"',
    "titel halden")
rep('"title": "Gulvsliping i Sarpsborg og Østfold | CK Måleri & Golv"',
    '"title": "Gulvsliping og gulvsliper i Sarpsborg og Østfold | CK Måleri & Golv"',
    "titel sarpsborg")
rep('"title": "Gulvsliping i Fredrikstad og Østfold | CK Måleri & Golv"',
    '"title": "Gulvsliping og gulvsliper i Fredrikstad og Østfold | CK Måleri & Golv"',
    "titel fredrikstad")

# ------------------------------------------------------- 2. META DESCRIPTIONS
rep('''        "desc": ("Gulvsliping av parkett, fiskebensparkett og gamle tregulv i Halden og Østfold. "
                 "Egne Bona-maskiner, støysvakt og nesten støvfritt. Gratis befaring og skriftlig fastpris."),''',
    '''        "desc": ("Gulvsliper i Halden og Østfold. Vi sliper parkett, fiskebensparkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    "desc halden")
rep('''        "desc": ("Gulvsliping av parkett, fiskebensparkett og gamle tregulv i Sarpsborg og Østfold. "
                 "Egne Bona-maskiner, støysvakt og nesten støvfritt. Gratis befaring og skriftlig fastpris."),''',
    '''        "desc": ("Gulvsliper i Sarpsborg og Østfold. Vi sliper parkett, fiskebensparkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    "desc sarpsborg")
rep('''        "desc": ("Gulvsliping av parkett, fiskebensparkett og gamle tregulv i Fredrikstad, Hvaler og "
                 "Østfold. Egne Bona-maskiner, støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    '''        "desc": ("Gulvsliper i Fredrikstad, Hvaler og Østfold. Vi sliper parkett og gamle tregulv "
                 "— støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    "desc fredrikstad")

# ------------------------------------------------------------- 3. HERO-TEKST
rep('''        "hero_tag": ("Vi sliper og behandler tregulv i hele Halden-området. Du får skriftlig fastpris "
                     "på forhånd, og vi kjører over grensen fra Uddevalla med egne Bona-maskiner."),''',
    '''        "hero_tag": ("Vi er gulvslipere fra Uddevalla. Skriftlig fastpris på forhånd, og vi kjører "
                     "over grensen til Halden med egne Bona-maskiner."),''',
    "hero_tag halden")
rep('''        "hero_tag": ("Vi sliper og behandler tregulv i hele Sarpsborg-området. Du får skriftlig fastpris "
                     "på forhånd, og vi kjører over grensen fra Uddevalla med egne Bona-maskiner."),''',
    '''        "hero_tag": ("Vi er gulvslipere fra Uddevalla. Skriftlig fastpris på forhånd, og vi kjører "
                     "over grensen til Sarpsborg med egne Bona-maskiner."),''',
    "hero_tag sarpsborg")
rep('''        "hero_tag": ("Vi sliper og behandler tregulv i hele Fredrikstad og på Hvaler. Du får skriftlig "
                     "fastpris på forhånd, og vi kjører over grensen fra Uddevalla med egne Bona-maskiner."),''',
    '''        "hero_tag": ("Vi er gulvslipere fra Uddevalla. Skriftlig fastpris på forhånd, og vi kjører "
                     "over grensen til Fredrikstad og Hvaler med egne Bona-maskiner."),''',
    "hero_tag fredrikstad")

# ------------------------------------------------- 4. TJENESTESEKSJONENS LEAD
rep('''    <p class="section-lead">Gamle furugulv, fiskebensparkett og slitt eikeparkett — vi sliper og behandler
      til en overflate som holder. Egne Bona-maskiner, støysvakt og tilnærmet støvfritt, og skriftlig
      fastpris etter befaring i {city}.</p>''',
    '''    <p class="section-lead">Gamle furugulv, fiskebensparkett og slitt eikeparkett — vi sliper og behandler
      til en overflate som holder. Parkettsliping og sliping av plankegulv er det vi gjør mest, med egne
      Bona-maskiner, støysvakt og tilnærmet støvfritt. Skriftlig fastpris etter befaring i {city}.</p>''',
    "tjeneste-lead (parkettsliping)")

# --------------------------------------------- 5. LENGRE, MER UNIKE LOKALE TEKSTER
HALDEN_OLD = '''        "local_p": [
            "Halden er en gammel grenseby med mye trehusbebyggelse — empiregårder i sentrum, eldre "
            "villaer i Tistedal og Idd, og en lang rekke hytter langs Iddefjorden og opp mot Svinesund. "
            "Nettopp i den typen hus finner vi gulvene som er mest verdt å ta vare på: brede furuplanker, "
            "gammel fiskebensparkett og slitte parkettgulv som har fått tjue år med møbler og barneføtter.",
            "Vi sliper og behandler tregulv i hele Halden kommune — fra sentrum og Tistedal til Idd, "
            "Rokke, Asak og Sponvika — og tar også malerarbeid, mikrosement på bad og flislegging. "
            "Fordi vi kjører over grensen fra Uddevalla har vi med egne Bona-maskiner og alt materiell, "
            "så jobben går i ett.",
            "Er du usikker på om det gamle gulvet er verdt å redde, sender du bare noen bilder. Vi sier "
            "ærlig fra hvis det ikke lønner seg — og kommer på gratis befaring i Halden når det passer deg.",
        ],'''
HALDEN_NEW = '''        "local_p": [
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
        ],'''
rep(HALDEN_OLD, HALDEN_NEW, "lokal tekst halden")

SARPSBORG_OLD = '''        "local_p": [
            "Sarpsborg har både eldre villaer og nyere blokker, og gulvene varierer deretter. I områder "
            "som Grålum, Borgenhaugen og Hafslund møter vi mye 90-tallsparkett som er slitt, mens de "
            "eldre husene i Skjeberg og Varteig ofte har brede tregulv som bare trenger å bli slipt fram "
            "igjen.",
            "Vi tar hele Sarpsborg kommune — sentrum, Grålum, Borgenhaugen, Skjeberg, Hafslund, Greåker "
            "og Varteig — med gulvsliping, innvendig og utvendig malerarbeid, mikrosement og flislegging. "
            "Siden vi kommer fra Uddevalla over grensen, har vi med egne maskiner og gjør alt selv, uten "
            "å leie inn underleverandører.",
            "Skal leiligheten friskes opp før salg, eller skal hele huset gjøres om? Send noen bilder og "
            "antall kvadratmeter, så får du et realistisk anslag allerede på telefon — og en skriftlig "
            "fastpris etter gratis befaring i Sarpsborg.",
        ],'''
SARPSBORG_NEW = '''        "local_p": [
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
        ],'''
rep(SARPSBORG_OLD, SARPSBORG_NEW, "lokal tekst sarpsborg")

FREDRIKSTAD_OLD = '''        "local_p": [
            "Fredrikstad har en av Norges best bevarte festningsbyer, og i Gamlebyen og områdene rundt "
            "Cicignon står trehusene tett. Der er det sjelden rom for moderne gulv — det skal være plank, "
            "brede bord og overflater som tåler livet i et gammelt hus. Samtidig finner vi en helt annen "
            "type oppdrag på Kråkerøy, Gressvik, Begby og Rolvsøy: nyere eneboliger og rekkehus med "
            "parkett som er moden for sliping.",
            "Vi jobber i hele Fredrikstad og på Hvaler — også Onsøy og øyene — med gulvsliping, "
            "malerarbeid, mikrosement og flislegging. Kysten betyr mange hytter og fritidsboliger, og der "
            "er det ofte et slitent tregulv eller et bad som skal tåle fukt. Det tar vi oss av.",
            "Vi kjører opp fra Uddevalla via E6 og Svinesund med egne Bona-maskiner, og gjør jobben selv "
            "fra start til slutt. Noen bilder og cirka antall kvadratmeter er nok for et første anslag.",
        ],'''
FREDRIKSTAD_NEW = '''        "local_p": [
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
        ],'''
rep(FREDRIKSTAD_OLD, FREDRIKSTAD_NEW, "lokal tekst fredrikstad")

io.open(F, "w", encoding="utf-8").write(s)
print("build_no.py oppdatert")
