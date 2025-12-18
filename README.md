# Codesphere website

Static site for GitHub Pages.

---

## TRM 10x -järjestelmä (Thinking, Reasoning, Memory)

Tämä repo käyttää **TRM 10x -mallia** kaikkiin kehitystehtäviin. TRM:n tavoite on tuottaa 10× parempia tuloksia iteroimalla ratkaisu 10 kierroksen kautta ja tallentamalla opit muistiin.

### Miten TRM toimii?

1. **Thinking (Kierrokset 1-3)**: Ymmärrä ongelma syvällisesti, analysoi rajoitteet ja haasteet.
2. **Reasoning (Kierrokset 4-8)**: Kehitä ratkaisu iteratiivisesti; jokainen kierros parantaa edellistä.
3. **Memory (Kierrokset 9-10)**: Tallenna opit `trm/memory.md` -tiedostoon; hyödynnä aikaisempaa kontekstia.

### Käyttö

**Aloita uusi sessio**:
```powershell
python tools/trm_start_session.py "Tehtävän kuvaus (esim. Luo PNG-käyntikortti)"
# tai PowerShell-wrapper:
.\tools\trm_session.ps1 start "Tehtävän kuvaus"
```

**Päivitä kierros** (1-10):
```powershell
python tools/trm_update_memory.py 3 "Kierroksen 3 opit ja päätökset"
# tai:
.\tools\trm_session.ps1 update 3 "Kierroksen 3 opit"
```

**Viimeistele sessio**:
```powershell
python tools/trm_finalize_session.py "Lopputulos ja hyväksymiskriteerit täyttyneet"
# tai:
.\tools\trm_session.ps1 finalize "Lopputulos ja hyväksymiskriteerit"
```

### Tiedostot

- **`.github/copilot-instructions.md`**: Copilot-ohjesäännöt (TRM-prosessi, tavoitteet, rajoitteet).
- **`trm/memory.md`**: Kaikki TRM-sessionien opit (historia).
- **`trm/state.json`**: Nykyinen session tila (kierros, status, insights).
- **`tools/trm_*.py`**: Automaatioskriptit session hallintaan.
- **`tools/trm_session.ps1`**: PowerShell-wrapper Python-skripteille.

### Esimerkki: PNG-käyntikortin design

1. **Aloita**: `python tools/trm_start_session.py "PNG-käyntikortti 1050x600, tumma teema, vasen: logo + glow, oikea: yhteystiedot"`
2. **Kierrokset 1-10**: Työstä ratkaisu iteratiivisesti; päivitä tila jokaisen kierroksen jälkeen.
3. **Viimeistele**: `python tools/trm_finalize_session.py "Premium PNG valmis, kaikki kriteerit täyttyneet"`
4. **Tulos**: Opit tallennettu `trm/memory.md` -tiedostoon; seuraava projekti hyötyy aikaisemmasta kontekstista.

---

## UI smoke test (Docker)

Prereq: Docker Desktop running with Linux engine.

Run:

```pwsh
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\run_ui_smoke.ps1
```

Expected output:

- `UI SMOKE: PASS`
