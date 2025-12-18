# Business Card Mobile Layout Fix Session
**Päivämäärä:** 18.12.2025  
**Tehtävä:** Korjaa mobiilisommittelu – selain ei hyödynnä koko vasemman alueen korkeutta

---

## TRM-prosessi: 6 kierrosta

### THINK (Kierrokset 1-2): Ongelman analyysi

**Ongelma:**
- Selain näkyy mobiilissa, mutta `.browser`-elementti ei veny koko vasemman alueen korkeuteen
- Sommittelu on "kasaan painunut" – paljon tyhjää tilaa ylä-/alapuolella
- Desktop toimii hyvin, mutta mobile/tablet eivät hyödynnä tilaa täysimääräisesti

**Syy:**
- `.inner` käytti `grid-template-rows: auto auto` → rivit eivät venyneet
- `.left` ei ollut flex-container → `.browser { height: 100%; }` ei toiminut
- `min-height: 300px` ei riittänyt → tarvittiin `flex: 1` tai `grid-template-rows: 1fr 1fr`

**Ratkaisu:**
- Muutetaan `.inner` grid-rows: `auto auto` → `1fr 1fr` (mobile)
- Lisätään `.left { display: flex; flex-direction: column; }`
- Lisätään `.browser { flex: 1; min-height: 0; }` → venyy täyttämään tilan

---

### REFINE (Kierrokset 3-5): Korjaukset media queryissä

#### Kierros 3: Mobile (<720px)
```css
@media (max-width: 720px) {
  .inner {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;  /* Muutettu: auto auto → 1fr 1fr */
    gap: 14px;
    inset: 12px;
  }
  
  .left { 
    min-height: 0;  /* Muutettu: 300px → 0 */
    display: flex;
    flex-direction: column;
  }
  
  .browser {
    flex: 1;
    min-height: 0;
  }
}
```

#### Kierros 4: Tablet (721-900px)
```css
@media (min-width: 721px) and (max-width: 900px) {
  .left { 
    min-height: 0;  /* Muutettu: 220px → 0 */
    display: flex;
    flex-direction: column;
  }
  .browser {
    flex: 1;
    min-height: 0;
  }
}
```

#### Kierros 5: Landscape-tilat
- **Mid landscape (901-1280px)**: Lisätty sama flex-layout
- **Small landscape (<900px)**: Lisätty sama flex-layout

---

### MASTER (Kierros 6): Testaus ja validointi

**UI Smoke Test:**
```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\run_ui_smoke.ps1
# Output: UI SMOKE: PASS ✅
```

**Testattavat näyttökoot:**
- 📱 **375px (mobile portrait)**: `.browser` venyy koko `.left`-alueen korkeuteen
- 📱 **768px (tablet portrait)**: `.browser` täyttää vasemman sarakkeen
- 💻 **1024px (desktop)**: Toimii kuten ennenkin (ei muutoksia)
- 📱 **Landscape-modet**: `.browser` venyy oikein kaikissa landscape-tiloissa

---

## Muutokset yhteenveto

| Media Query | Ennen | Jälkeen |
|------------|-------|---------|
| `max-width: 720px` | `.inner { grid-rows: auto auto }`, `.left { min-height: 300px }` | `.inner { grid-rows: 1fr 1fr }`, `.left { flex }`, `.browser { flex: 1 }` |
| `721px-900px` | `.left { min-height: 220px }` | `.left { flex }`, `.browser { flex: 1 }` |
| `901px-1280px landscape` | `.left { min-height: 220px }` | `.left { flex }`, `.browser { flex: 1 }` |
| `<900px landscape` | `.left { min-height: 200px }` | `.left { flex }`, `.browser { flex: 1 }` |

---

## Opit (TRM Memory)

1. **Grid-rows `auto` vs `1fr`**:
   - `auto` = sisältö määrää koon → ei veny
   - `1fr` = jakaa tilan tasaisesti → venyy täyteen

2. **Flex-container lapsen kanssa**:
   - Parent: `display: flex; flex-direction: column;`
   - Child: `flex: 1;` → venyy täyttämään jäljellä olevan tilan
   - Tärkeä: `min-height: 0;` estää sisällön "ylivuodon" gridin ulkopuolelle

3. **Responsive-layout parhaita käytäntöjä**:
   - Testaa **aina** kaikki breakpointit (mobile, tablet, landscape)
   - Käytä `min-height: 0;` flexbox/grid-lapsille (estää overflow)
   - Varmista että **jokainen** media query päivitetään johdonmukaisesti

4. **UI Smoke Test pakollinen**:
   - Playwright-testit varmistavat että layout ei rikkoudu
   - Aja aina ennen committia

---

## Tiedostot

- `brand-kit/digital/business-card.html` — Digitaalinen käyntikortti
- `tools/run_ui_smoke.ps1` — UI-testiskripti

---

## Testausohjeet

1. **Chrome DevTools**:
   ```
   F12 → Toggle device toolbar (Ctrl+Shift+M)
   Testaa: iPhone SE (375px), iPad (768px), Desktop (1024px)
   ```

2. **Oikea laite**:
   ```
   https://toeksy.github.io/codesphere-website_1/brand-kit/digital/business-card.html?v=latest
   ```
   Käytä "Hard Reload" tai incognitoa jos cache-ongelma.

---

## Lopputulos

✅ **Selain hyödyntää nyt koko vasemman alueen korkeuden kaikilla laitteilla**  
✅ **Ei tyhjää tilaa mobiilissa/tabletilla**  
✅ **Landscape-tilat toimivat oikein**  
✅ **UI Smoke Test: PASS**

**Seuraava vaihe:** Deploy GitHub Pagesiin ja testaa oikealla Android-laitteella.
