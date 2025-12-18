# TRM Memory (Codesphere Website)

Tämä tiedosto tallentaa kaikki TRM 10x -sessionien opit ja päätökset. Jokainen sessio dokumentoidaan seuraavassa muodossa:

---

## Session: 2025-12-18 – PNG-käyntikortin design (business-card.png)

**Ongelma**: Luo 1050×600 PNG-käyntikortti Codesphere-teeman mukaisesti. Vasen puoli: iso logo + abstrakti syaani-glow/sheeni (ei avaruus/tähtitausta). Oikea puoli: selkeät yhteystiedot (Timo/Matti/Mika) premium-tyylillä.

**Ratkaisu**:
- Hyödynnettiin `business-card.html` -palettia ja typografiaa.
- Toteutettu Pillow-kirjastolla (Python).
- Vasen paneeli: tumma tausta + kaksi radiaalista glowta (accent + primary) + diagonaalinen sheen.
- Logo: keskitetty, syaani-outer-glow.
- Oikea paneeli: tumma alue, selkeä teksti-hierarkia (BRAND → Yhteystiedot → henkilöt → footer).
- Aksentti: syaani (`#00FFFF`), tausta: tumma (`#0A0F1A`).

**Opit**:
- **Ei vaaleita taustoja** – koko PNG on tumma; välttää "valkoiselta paperilta" -fiilistä.
- **Radiaalinen glow** – toimii paremmin kuin tasainen gradient.
- **Typografiahierarkia** – tärkeintä ensin (BRAND → nimi → titteli → yhteystieto).
- **Kontrastisäännöt** – tekstin tulee olla vähintään AA-tasolla (WCAG) tummaa taustaa vasten.
- **Rounded corners** – card-frame tulee maskia samalla pyöristyksellä kuin live-kortissa.

**Hyväksymiskriteerit täyttyneet**:
- ✅ PNG näyttää tummalta ja premium-tyylisenä.
- ✅ Vasen osa: logo + abstrakti glow, ei avaruutta.
- ✅ Oikea osa: teksti selkeä ja brändin mukainen.
- ✅ Aksentti on syaani, ei vihreä.

---



---

## Session: 2025-12-18 – Demo: Testaa TRM-järjestelmän toimivuus

**Ongelma**: Demo: Testaa TRM-järjestelmän toimivuus

**Ratkaisu**: TRM-järjestelmä toimii täysin: Copilot-ohjeet, muistit ja automaatio integroitu. Hyväksymiskriteerit täyttyneet.

**Opit**:

- **Kierros 1**: TRM-järjestelmä asennettu onnistuneesti. Copilot-ohjeet, muistitiedostot ja automaatioskriptit toimivat.

**Hyväksymiskriteerit täyttyneet**:
- ✅ (Täytä hyväksymiskriteerit tähän)

---

## Session: 2025-12-18 – Mobiilisommittelun korjaus (business-card.html)

**Ongelma**: Selain näkyy mobiilissa, mutta `.browser`-elementti ei hyödynnä koko vasemman alueen korkeutta. Sommittelu on "kasaan painunut" – paljon tyhjää tilaa ylä-/alapuolella.

**Ratkaisu**: 
- Muutettu `.inner` grid-rows: `auto auto` → `1fr 1fr` (mobile/tablet)
- Lisätty `.left { display: flex; flex-direction: column; }`
- Lisätty `.browser { flex: 1; min-height: 0; }` → venyy täyttämään tilan
- Päivitetty kaikki media queryt: mobile (<720px), tablet (721-900px), landscape (901-1280px, <900px)

**Opit**:

- **Kierros 1-2 (THINK)**: Grid-rows `auto` vs `1fr` – `auto` ei veny, `1fr` jakaa tilan tasaisesti
- **Kierros 3 (REFINE)**: Mobile (<720px) – `.inner { grid-rows: 1fr 1fr }` + `.left { flex }` + `.browser { flex: 1 }`
- **Kierros 4 (REFINE)**: Tablet (721-900px) – sama flex-layout kuin mobilessa
- **Kierros 5 (REFINE)**: Landscape-tilat (901-1280px, <900px) – flex-layout kaikille
- **Kierros 6 (MASTER)**: UI Smoke Test PASS, testattu kaikki breakpointit

**Tärkeät opit**:
- **`min-height: 0`** on kriittinen flexbox/grid-lapsille → estää sisällön "ylivuodon"
- **Flex-container + `flex: 1` child** → venyy täyttämään jäljellä olevan tilan
- **Testaa AINA kaikki breakpointit** (mobile, tablet, landscape) → johdonmukaisuus

**Hyväksymiskriteerit täyttyneet**:
- ✅ Selain hyödyntää koko vasemman alueen korkeuden kaikilla laitteilla
- ✅ Ei tyhjää tilaa mobiilissa/tabletilla
- ✅ Landscape-tilat toimivat oikein
- ✅ UI Smoke Test: PASS



---

## Session: 2025-12-18 – TRM smoke test (local)

**Ongelma**: TRM smoke test (local)

**Ratkaisu**: TRM smoke test complete

**Opit**:

- **Kierros 1**: Smoke test round 1 insights

**Hyväksymiskriteerit täyttyneet**:
- ✅ (Täytä hyväksymiskriteerit tähän)



---

## Session: 2025-12-18 – TRM automation verification

**Ongelma**: TRM automation verification

**Ratkaisu**: Automation verification complete

**Opit**:

- **Kierros 1**: Automation: round 1

**Hyväksymiskriteerit täyttyneet**:
- ✅ (Täytä hyväksymiskriteerit tähän)

## (Lisää tulevat sessionit tänne)

**Muistilista**:
- Tallenna jokaisen 10-kierroksen session lopputulos.
- Päivitä `trm/state.json` -tila ennen ja jälkeen session.
- Hyödynnä aikaisempia oppeja seuraavissa tehtävissä.
