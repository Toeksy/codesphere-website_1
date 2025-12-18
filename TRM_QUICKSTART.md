# TRM 10x Quick Start Guide

## Pika-aloitus

1. **Aloita sessio**:
   ```powershell
   python tools/trm_start_session.py "Tehtävän kuvaus"
   ```

2. **Päivitä kierros** (1-10):
   ```powershell
   python tools/trm_update_memory.py <kierros> "Opit"
   ```

3. **Viimeistele**:
   ```powershell
   python tools/trm_finalize_session.py "Lopputulos"
   ```

## PowerShell-wrapper (vaihtoehtoinen)

```powershell
.\tools\trm_session.ps1 start "Tehtävä"
.\tools\trm_session.ps1 update 3 "Kierroksen 3 opit"
.\tools\trm_session.ps1 finalize "Lopputulos"
```

## VS Code Tasks (suositus)

VS Codessa voit ajaa valmiit taskit: `Terminal` → `Run Task...`

- `TRM: Check (clean state)`
- `TRM: Start session`
- `TRM: Update round`
- `TRM: Finalize session`

Taskit on määritelty tiedostossa `.vscode/tasks.json`.

## Git pre-commit hook (estää vahingossa commitoinnin)

Repo sisältää versionoidun pre-commit hookin (`.githooks/pre-commit`), joka ajaa `python tools/trm_check.py` ennen `git commit`-komentoa.

Ota hook käyttöön tällä koneella:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\install_git_hooks.ps1 install
```

Tarkista tila:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\install_git_hooks.ps1 status
```

Poista käytöstä:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\install_git_hooks.ps1 uninstall
```

## TRM-kierrokset (10×)

| Kierros | Vaihe | Fokus |
|---------|-------|-------|
| 1-3 | THINK | Ongelma, analyysi, haasteet |
| 4-8 | REFINE | Iteratiivinen kehitys, komponentit |
| 9-10 | MASTER | Toteutus, hyväksymiskriteerit |

## Tiedostorakenne

```text
.github/
  copilot-instructions.md  ← Copilot-ohjesäännöt
trm/
  memory.md               ← Session-historia
  state.json              ← Nykyinen tila
tools/
  trm_start_session.py    ← Aloita sessio
  trm_update_memory.py    ← Päivitä kierros
  trm_finalize_session.py ← Sulje sessio
  trm_session.ps1         ← PowerShell-wrapper
```

## Esimerkit

### Esimerkki 1: Uusi feature

```powershell
python tools/trm_start_session.py "Lisää 'Projects'-osio index.html"
python tools/trm_update_memory.py 1 "Layout grid/flex, accent-border, tumma tausta"
python tools/trm_update_memory.py 2 "Typografia hierarkia: h2 → p → link"
# ... (kierrokset 3-10)
python tools/trm_finalize_session.py "Feature valmis, responsive, dokumentoitu"
```

### Esimerkki 2: Bugfix

```powershell
python tools/trm_start_session.py "Korjaa kontrasti-ongelma brand.html"
python tools/trm_update_memory.py 1 "Tunnistettu: teksti liian vaalea tummaa taustaa vasten"
python tools/trm_update_memory.py 2 "Ratkaisu: muutetaan muted-väri #94A3B8 → #CBD5E1"
# ... (kierrokset 3-10)
python tools/trm_finalize_session.py "Kontrasti WCAG AA, testattu kaikilla sivuilla"
```

## Copilot-integraatio

Kun GitHub Copilot lukee `.github/copilot-instructions.md`, se:

- Noudattaa TRM 10x -prosessia automaattisesti
- Dokumentoi päätökset `trm/memory.md`
- Päivittää `trm/state.json` kierrosten välillä
- Hyödyntää aikaisempia oppeja (Memory-vaihe)

## Tavoitteet

- **10× parempi laatu**: Iteroi 10 kierrosta, jokainen parantaa edellistä.
- **Muisti**: Tallenna opit → seuraava projekti hyötyy aikaisemmasta kontekstista.
- **Johdonmukaisuus**: Kaikki tehtävät noudattavat samaa prosessia.
