# TRM (10x) – PNG-käyntikortin design-speksi (Codesphere)

Tavoite: `business-card.png` (1050×600) näyttää **samalta perheeltä** kuin `brand-kit/digital/business-card.html`, mutta layoutilla:
- vasen: **logo + abstrakti syaani-glow/sheeni** (ei selainta, ei avaruutta/tähtiä)
- oikea: **yhteystiedot** selkeästi ja premium-tyylillä

Rajoitteet:
- Ei uusia väriteemoja (pysy Codesphere-syaanissa).
- Ei valkoista/harmaata “paperitaustaa” → koko kuva pysyy tummana.
- Hyödynnä olemassa olevat elementit: paletti, border/shadow-idea, typografinen hierarkia.

## Kierros 1/10 – THINK: ongelman rajaus
- Nykyinen PNG rikkoo teemaa: tausta on liian vaalea, kontrasti huono, aksentti väärä (vihreä).
- PNG:n tulee toimia yksinään (ei sivun taustaa), joten **koko canvas** pitää olla suunniteltu.

## Kierros 2/10 – THINK: mikä tekee live-kortista toimivan
- Tumma tausta + **radiaalinen glow** (accent + primary)
- Kortin reunus: accent-border + sisäreuna (inset) + pehmeä ulkohehku
- Selkeä typografiahierarkia: BRAND → “Yhteystiedot” → henkilöt → footer

## Kierros 3/10 – THINK: layout-päätökset
- Grid: 2 saraketta kuten live-kortissa (1.05fr / 0.95fr)
- Väli: ~22px
- Sisämarginaalit: ~26px

## Kierros 4/10 – REFINE: vasen paneeli (logo)
- Ei selaimen mockia.
- Vasen paneeli = tumma paneli, jossa:
  - 2 radiaalista glowta (accent vasemmalla ylhäällä, primary oikealla alhaalla)
  - kevyt diagonaalinen sheen (valkoinen alpha 0.03–0.06)
- Logo sijoitus: keskitetty pystysuunnassa, hieman vasemmalle ("hero"-tuntuma).
- Logo ympärille syaani-outer-glow alpha maltillinen (premium, ei neon-överi).

## Kierros 5/10 – REFINE: oikea paneeli (luettavuus)
- Oikealle tehdään tumma ”text-safe” -alue (tai vähintään säilytetään tausta tummana).
- Divider: syaani viiva, mieluummin hieman gradient-mäinen (mutta riittää myös tasainen accent).

## Kierros 6/10 – REFINE: väripaletti (lukittu)
- `bg_dark`: #0A0F1A
- `text`: #F1F5F9
- `muted`: #94A3B8
- `accent`: #00FFFF
- `primary`: #1E3A5F

## Kierros 7/10 – REFINE: typografia
- BRAND: ~34px, bold
- Nimi: ~22px, bold
- Titteli: ~16px, muted
- Puhelin: ~16px, accent
- Footer: ~14px, muted

## Kierros 8/10 – REFINE: kontrastisäännöt
- Ei vaaleaa taustaa oikealle.
- Kaikki tekstit vähintään AA-kontrastissa tummaa taustaa vasten.
- Jos jokin alue näyttää "harmaalta", sitä tummennetaan ennen tekstin piirtämistä.

## Kierros 9/10 – MASTER: toteutussuunnitelma (Pillow)
- Piirrä koko canvas tummaan `bg_dark`.
- Lisää taustaglowt (kaksi ellipsiä) + blur.
- Piirrä card-frame: rounded rect, accent outline, inset line, ulkohehku.
- Piirrä vasen paneli omana RGBA-kuvana ja maskaa rounded corners.
- Piirrä logo + glow vasempaan paneliin.
- Piirrä oikea teksti suoraan canvasille (tai kevyen right-panel overlayn päälle).

## Kierros 10/10 – MASTER: hyväksymiskriteerit
- PNG näyttää tummalta (ei “valkoinen paperi” -fiilistä).
- Vasen osa: logo + abstrakti glow/sheeni, ei avaruutta/tähtiä.
- Oikea osa: teksti on selkeä ja brändin mukainen.
- Aksentti on syaani, ei vihreä.
