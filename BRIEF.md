# CK Måleri & Golv — brief

Källa: skärmdumpar på referensförslag + Oskars krav. Uppdatera efter hand.

## Fakta om företaget
- **Namn:** CK Måleri & Golv
- **Område:** Uddevalla och Trestad (Trollhättan–Uddevalla–Vänersborg). *Inte* Karlstad/Värmland.
- **Telefon:** 073-703 37 17
- **E-post:** ckmaleri@gmail.com
- **Instagram:** @ckmaleri (~70 följare, aktiva inlägg om slipning/målning)
- **Domän:** ckmaleri.se — köpt men parkerad hos Loopia, ingen sajt live
- **Omdömen:** 5,0 av 15 omdömen på Servicefinder. Namngivna: Ingrid (ekparkett),
  Annika (furugolv + trappor), Mladen (golv och målning)
- **Försäkrade**, kostnadsfri offert

## Tjänster (fyra ben, från referensen)
1. **Golvslipning** — parkett och fiskben, gamla brädgolv, lack/olja/pigment
2. **Måleri & tapet** — invändigt och fasad, tapetsering, spackling och fog
3. **Microcement** — badrum och kök, golv och väggar, utan fogar
4. **Plattsättning** — kakel och klinker, hall/kök/badrum, fogning, tätskikt

## Referensjobb som nämns
- Kulturhusets scen (stor yta, slipning)
- 30 år gammal parkett som fick nytt liv — Bona Ultra Matt
- Fiskbensparkett, slipad och behandlad
- Furugolv och trappor (kund: Annika)
- Kanoner på Bohusläns försvarsmuseum (rost/måleri)

## Referensens uttryck (ska liknas, inte kopieras)
- Mörkgrön som bärfärg + vit/benvit bakgrund, grön accent
- Stora rubriker där sista ledet är kursivt i accentfärg
  ("Golv, väggar och kakel, *från samma hand*")
- Bock-listor med grön bock
- Stort riktigt foto (herringbone-parkett) som blickfång
- Lodrät grön "RING <nummer>"-flik på höger kant
- Tjänstekort i fyra spalter: bild, rubrik, text, tre bockar, "Begär offert" med pil
- "Tre steg" från samtal till färdigt golv
- Omdömeskort från Servicefinder med initialer i färgcirkel
- FAQ som utfällbara frågor
- Offertformulär med dropdown för jobbtyp (golvslipning, måleri, microcement, plattsättning)
- Fot/galleri med bildtexter ("Mitt i jobbet", "Nylackat", "Fiskben slipat")

## Rubriker värda att slå an (från referensen)
- "Golvet är inte slut, bara slitet"
- "Golv, väggar och kakel, från samma hand"
- "Berätta om golvet, offerten kostar inget"
- "Från första samtalet till färdigt golv"

## Oskars krav
1. Likna referensen i känsla — **inte** en kopia
2. En snygg animering/video (fal.ai — nyckel finns i `~/.hermes/fal.env`, verifierad)
3. SEO gjort ordentligt från början (title, meta, schema, struktur, internlänkar)

## Öppna frågor
- Bilder: CK:s egna (Instagram) eller ska Oskar skicka?
- Logga?
- Ska fyra tjänstesidor byggas (en per ben) utöver startsidan?
- Publicering: ckmaleri.se hos Loopia?

## Status
Byggt: 7 sidor (start + 4 tjänstesidor + tack + integritetspolicy) som statisk HTML.
Källa: `build.py` (kör `python3 build.py` för att bygga om). Formulär via formsubmit.co
till ckmaleri@gmail.com — kräver att CK bekräftar första inskickade formuläret.
Video: fal.ai kling-v1.6 image-to-video, bumerang-loop 10 s, mp4 + webm.
Bilderna är hämtade ur förslaget och uppskalade (esrgan) — original bör ersätta.

