# Commit Message Template

## Fix: Business card mobile layout - browser now fills full height

**Ongelma:**
Selain-mock ei hyödyntänyt koko vasemman alueen korkeutta mobiilissa/tabletilla.
Sommittelu oli "kasaan painunut" – paljon tyhjää tilaa kortin ylä-/alapuolella.

**Syy:**
- `.inner` käytti `grid-template-rows: auto auto` → rivit eivät venyneet
- `.left` ei ollut flex-container → `.browser { height: 100%; }` ei toiminut
- Kiinteät `min-height`-arvot eivät riittäneet

**Ratkaisu:**
- Muutettu `.inner` grid-rows: `auto auto` → `1fr 1fr` (mobile/tablet)
- Lisätty `.left { display: flex; flex-direction: column; min-height: 0; }`
- Lisätty `.browser { flex: 1; min-height: 0; }` → venyy täyttämään tilan

**Muutetut media queryt:**
- Mobile (<720px)
- Tablet (721-900px)
- Mid landscape (901-1280px)
- Small landscape (<900px)

**Testaus:**
- ✅ UI Smoke Test: PASS
- ✅ Chrome DevTools: 375px, 768px, 1024px
- ✅ Selain venyy nyt koko korkeudelle kaikilla laitteilla

**Tiedostot:**
- `brand-kit/digital/business-card.html` — Korjattu mobiilisommittelu
- `docs/session-2025-12-18-mobile-layout-fix.md` — Session-dokumentaatio
- `docs/mobile-layout-fix-before-after.md` — Visuaalinen vertailu
- `trm/memory.md` — Päivitetty TRM-muisti

---

## Git Commands

```bash
git add brand-kit/digital/business-card.html
git add docs/session-2025-12-18-mobile-layout-fix.md
git add docs/mobile-layout-fix-before-after.md
git add trm/memory.md

git commit -m "Fix: business card mobile layout - browser fills full height

- Changed .inner grid-rows from 'auto auto' to '1fr 1fr'
- Added .left flex layout (display: flex, flex-direction: column)
- Added .browser flex: 1 to fill available space
- Updated all media queries: mobile, tablet, landscape
- UI Smoke Test: PASS
- Tested: 375px, 768px, 1024px viewports"

git push origin master
```

---

## Deploy

GitHub Pages deployaa automaattisesti masterin pushissa.

**Testauslinkki:**
```
https://toeksy.github.io/codesphere-website_1/brand-kit/digital/business-card.html?v=mobile-fix
```

**Huom:** Android-selaimessa käytä "Hard Reload" tai incognitoa jos cache-ongelma.
