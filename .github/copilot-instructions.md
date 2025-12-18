# GitHub Copilot – TRM-ohjeet (Codesphere Website)

## Yleisperiaatteet

Kun työskentelet tässä repossa, **noudata aina TRM-mallia** (Thinking, Reasoning, Memory):

1. **THINK** – Ymmärrä ongelma syvällisesti ennen koodin kirjoittamista.
2. **REASON** – Kehitä ratkaisu iteratiivisesti 10 kierroksessa; jokainen kierros parantaa edellistä.
3. **MEMORY** – Tallenna oppimasi `trm/memory.md` -tiedostoon; hyödynnä aikaisempaa kontekstia.

---

## TRM 10x -prosessi (Codesphere)

### Tavoitteet
- Premium **dark theme** (Codesphere-syaani `#00FFFF`, tumma tausta `#0A0F1A`).
- Yhtenäinen visuaalinen identiteetti: sama paletti, typografia, border/shadow -ajatus kaikissa asseteissa.
- Ei vaaleita/harmaita taustoja (vain tumma teema).
- Korkea kontrasti tekstille (vähintään WCAG AA).

### Rajoitteet
- **Ei uusia värejä** – paletti on lukittu (ks. `brand-kit/palette/`).
- **Ei avaruus-teemaa** – abstrakti glow/sheeni riittää.
- **Ei vihreää aksenttia** – vain syaani tai primary.

### Työnkulku (10 kierrosta)
1. **Kierros 1**: Ongelma rajaus (THINK)
2. **Kierros 2**: Kriittinen analyysi (THINK)
3. **Kierros 3**: Layout-päätökset (THINK)
4. **Kierros 4**: Ensimmäinen komponentti/osa (REFINE)
5. **Kierros 5**: Toinen komponentti/osa (REFINE)
6. **Kierros 6**: Kolmas komponentti (REFINE) – esim. väripaletti vahvistus
7. **Kierros 7**: Neljäs komponentti (REFINE) – esim. typografia
8. **Kierros 8**: Viides komponentti (REFINE) – esim. kontrasti
9. **Kierros 9**: Toteutussuunnitelma (MASTER)
10. **Kierros 10**: Hyväksymiskriteerit (MASTER)

Jokaisen kierroksen lopussa:
- Dokumentoi päätökset `trm/memory.md`-tiedostoon.
- Päivitä `trm/state.json` -tila (kierros, status, opit).

---

## Koodityyli ja parhaita käytäntöjä

### HTML/CSS (brand-kit, index.html, brand.html)
- Käytä CSS-muuttujia (`:root`) kaikille väreille.
- Responsiivisuus: mobile-first; `@media (min-width: 768px)` tabletille/desktopille.
- Shadow: `box-shadow: 0 0 20px rgba(0,255,255,0.3), 0 0 40px rgba(30,58,95,0.2)`.
- Border: `border: 1px solid #00FFFF`.

### Python (tools/)
- Pillow-kirjasto PNG/kuva-asseteille.
- Selkeät funktiot: `draw_glow()`, `draw_text()`, `apply_border()`.
- Kommentit suomeksi: jokaisen funktion alussa lyhyt kuvaus.

### PowerShell (tools/)
- Käytä `-NoProfile -ExecutionPolicy Bypass`.
- Verbose-outputti: `Write-Host` eri väreillä (`-ForegroundColor Cyan/Green/Yellow`).
- Virheenkäsittely: `try/catch`, `$LASTEXITCODE`.

---

## Muistijärjestelmä (`trm/`)

### `trm/memory.md`
Tallenna tänne jokaisen TRM-session lopputulos:
```markdown
## Session: [päivämäärä] – [tehtävä]
**Ongelma**: ...
**Ratkaisu**: ...
**Opit**:
- ...
- ...
```

### `trm/state.json`
```json
{
  "current_round": 5,
  "status": "in-progress",
  "task": "PNG-käyntikortin design",
  "insights": ["...", "..."]
}
```

Päivitä automaattisesti `tools/trm_update_memory.py` -skriptillä.

---

## Automaatio

### `tools/trm_start_session.py`
Luo uusi TRM-sessio: alustaa `state.json`, tulostaa briefin.

### `tools/trm_update_memory.py`
Päivittää `trm/state.json` kierroksen jälkeen (varsinainen sessiotiivistelmä kirjoitetaan `trm/memory.md`-tiedostoon `tools/trm_finalize_session.py`-vaiheessa).

### `tools/trm_finalize_session.py`
Sulkee session, kopioi opit `memory.md`-tiedostoon, resetoi `state.json`.

---

## Käyttö

**Ennen uutta tehtävää**:
```powershell
python tools/trm_start_session.py "Uuden asseton/ominaisuuden kuvaus"
```

**Jokaisen kierroksen jälkeen**:
```powershell
python tools/trm_update_memory.py 3 "Kierroksen 3 opit ja päätökset"
```

**Tehtävän lopussa**:
```powershell
python tools/trm_finalize_session.py "Lopputulos ja hyväksymiskriteerit täyttyneet"
```

---

## Esimerkkejä

### Esimerkki 1: PNG-käyntikortti (business-card.png)
- **Ongelma**: 1050×600 PNG, tumma teema, vasen: logo + glow, oikea: yhteystiedot.
- **TRM-speksi**: `brand-kit/digital/TRM_PNG_DESIGN_SPEC.md`
- **Tulos**: Premium PNG, joka näyttää samalta "perheeltä" kuin `business-card.html`.

### Esimerkki 2: Uusi feature (`index.html`)
- **Ongelma**: Lisää "Projects"-osio hero-kuvan alle.
- **TRM**:
  1. Kierros 1: Ymmärrä layout (grid/flex).
  2. Kierros 2: Värit (accent-border, tumma tausta).
  3. Kierros 3–8: Iteroi typografia, shadow, hover-efektit.
  4. Kierros 9: Toteuta HTML + CSS.
  5. Kierros 10: Testaa responsive, dokumentoi `trm/memory.md`.

---

## Yhteenveto

**Muista aina**:
- TRM 10x -malli on pakollinen kaikille tehtäville.
- Dokumentoi `trm/memory.md` + `trm/state.json`.
- Käytä automaatioskriptejä (`tools/trm_*.py`).
- Premium dark theme, Codesphere-paletti, ei vaaleita taustoja.

**Tavoite**: Jokainen tehtävä on 10× parempi, koska iteroit 10 kierrosta ja tallennat opit muistiin.
