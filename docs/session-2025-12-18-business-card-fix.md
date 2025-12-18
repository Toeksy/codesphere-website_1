# Codesphere Business Card Fix Session
**Päivämäärä:** 18.12.2025

---

## Yhteenveto

Tässä sessiossa korjattiin digitaalisen käyntikortin (`business-card.html`) skaalausongelmat Androidilla sekä lisättiin live-kotisivujen esikatselu selain-mockiin.

---

## Ongelmat

1. **Android-skaalaus ei toiminut** — käyntikortin sisältö leikkautui eikä Mika Leppäsen yhteystiedot näkyneet
2. **Selain-mock näytti vain staattisen kuvan** mobiililla — live-kotisivut näkyivät vain desktopilla (>901px)
3. **Cache-ongelma** — GitHub Pages deployasi oikein, mutta Android-selain piti vanhaa versiota välimuistissa

---

## Tehdyt korjaukset

### 1. Android-safe scaling (`d081b97`)

**Ongelma:** Aiempi `transform: scale()` kohdistui `.card`-elementtiin, joka on clipping container (`overflow: hidden`). Tämä ei toiminut Androidilla.

**Ratkaisu:** 
- Lisättiin uusi `.fit-content` wrapper kortin sisälle
- Skaalaus kohdistuu nyt sisältöön, ei containeriin
- Käytetään `window.visualViewport` API:a tarkempaan mittaukseen
- Double-rAF (requestAnimationFrame) paremman Android-yhteensopivuuden vuoksi

```css
.fit-content {
  position: absolute;
  inset: 0;
  transform: scale(var(--contentScale, 1));
  transform-origin: center;
  will-change: transform;
}
```

### 2. Live preview kaikille laitteille (`cc5b705`)

**Ongelma:** Kotisivujen live-esikatselu toimi vain desktopilla.

**Ratkaisu:** Poistettiin `min-width: 901px` -rajoitus:

```javascript
// Ennen:
const canLive = window.matchMedia('(min-width: 901px)').matches;

// Jälkeen:
// Always show live preview
if (!sitePreview.getAttribute('src')) sitePreview.setAttribute('src', liveSrc);
previewBox.classList.add('is-live');
```

---

## Diagnoosi: Miksi muutokset eivät näkyneet

1. **GitHub Pages deployasi oikein** — `raw.githubusercontent.com` ja `toeksy.github.io` sisälsivät saman koodin
2. **Android-selaimen välimuisti** oli syyllinen:
   - Chrome ja Samsung Internet pitävät sivuja aggressiivisesti cachessa
   - Jopa `?v=xxx` query string ei aina riitä
   
**Ratkaisu:** 
- Hard refresh (pitkä painallus Refresh-nappia)
- Incognito-tila
- Täysin uusi URL parametreilla

---

## Commitit

| SHA | Viesti | Muutokset |
|-----|--------|-----------|
| `0300c0d` | Fix: scale business card to fit viewport | Ensimmäinen scaling-yritys |
| `d081b97` | Fix: Android-safe business card fit | `.fit-content` wrapper + visualViewport |
| `cc5b705` | Fix: enable live homepage preview on all devices | Live preview kaikille |

---

## Testaus

Kaikki muutokset validoitiin ennen pushia:

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File .\tools\run_ui_smoke.ps1
# Output: UI SMOKE: PASS
```

---

## Testilinkki

```
https://toeksy.github.io/codesphere-website_1/brand-kit/digital/business-card.html?v=cc5b705
```

**Huom:** Käytä incognitoa tai "Hard Reload" -toimintoa Android-selaimessa.

---

## Tiedostot

- `brand-kit/digital/business-card.html` — Digitaalinen käyntikortti
- `tools/run_ui_smoke.ps1` — UI-testiskripti
- `README.md` — Repo-dokumentaatio

---

## Workflow

Noudatettiin iteratiivista prosessia:
1. Yksi muutos kerrallaan
2. Containerized Playwright smoke test
3. Commit + push
4. Testaus oikealla laitteella
