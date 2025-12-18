# TRM 10× Demo: Käyttöesimerkki (Skenaario)

## Skenaario: Lisää "Team"-osio Codesphere-sivustolle

Tässä demossa näytetään, miten TRM 10× -järjestelmää käytetään oikean kehitystehtävän parissa.

---

## 1. ALOITA SESSIO

```powershell
PS W:\Codex\Codesphere\website> python tools/trm_start_session.py "Lisää Team-osio index.html – esittelee Timo, Matti, Mika dark-theme-tyylillä"
```

**Output**:
```
╔════════════════════════════════════════════════════════════╗
║  🚀 TRM-AJATTELUMALLI (Thinking, Reasoning, Memory)        ║
╚════════════════════════════════════════════════════════════╝

Tehtävä: Lisää Team-osio index.html – esittelee Timo, Matti, Mika dark-theme-tyylillä
Kierrokset: 10

─────────────────────────────────────────────────────────────
🔄 KIERROS 1/10 – ALKUPERÄINEN SUUNNITELMA (THINK)
   • Ymmärrä ongelma
   • Tunnista keskeiset haasteet
   • Luo alustava ratkaisu
─────────────────────────────────────────────────────────────

✅ Sessio aloitettu: 2025-12-18T14:30:00
📁 Tila tallennettu: W:\Codex\Codesphere\website\trm\state.json
```

---

## 2. KIERROS 1: THINK – Ymmärrä ongelma

**Kehittäjä työstää**:
- Tutkii `index.html` -rakennetta (hero, features, footer).
- Tutkii `styles.css` (dark theme, `.card`-tyylit, accent-värit).
- Päättää: Team-osio sijoittuu Features-osion ja footerin väliin.
- Layout: 3-sarake grid (Timo, Matti, Mika).

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 1 "Layout: 3-sarake grid, sijoitus ennen footeria. Hyödynnetään .card-tyyliä, accent-border, tumma tausta. Kunkin henkilön kortti: nimi, rooli, lyhyt bio."
```

**Output**:
```
─────────────────────────────────────────────────────────────
🔄 KIERROS 1/10 – THINK
   Ongelma ymmärretty ja analysoitu
   [█████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 10%
─────────────────────────────────────────────────────────────

💡 Opit kierrokselta 1:
   Layout: 3-sarake grid, sijoitus ennen footeria. Hyödynnetään .card-tyyliä, accent-border, tumma tausta. Kunkin henkilön kortti: nimi, rooli, lyhyt bio.

✅ Kierros 1/10 valmis.
📁 Tila tallennettu: W:\Codex\Codesphere\website\trm\state.json

💡 Seuraavaksi:
   1. Työstä kierros 2.
   2. Päivitä tila: python tools/trm_update_memory.py 2 "Kierroksen 2 opit"
```

---

## 3. KIERROS 2: THINK – Kriittinen analyysi

**Kehittäjä analysoi**:
- Onko `.card`-tyyli riittävän yhtenäinen? → Kyllä, mutta lisätään hover-efekti (glow).
- Responsiivisuus? → 3 saraketta desktopilla, 1 sarake mobilella.
- Profiilikuvat? → Placeholder-avataarit (Codesphere-logo-pohjaiset).

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 2 "Lisätään hover-glow .card:hover. Responsiivisuus: grid 3-sarake → 1-sarake mobilella. Placeholder-avataarit: syaani-reunus, tumma tausta."
```

---

## 4. KIERROS 3: THINK – Layout-päätökset

**Kehittäjä suunnittelee HTML-rakenteen**:
```html
<section id="team" class="section">
  <h2 class="section-title">Tiimimme</h2>
  <div class="team-grid">
    <div class="card team-member">
      <div class="avatar"></div>
      <h3>Timo</h3>
      <p class="role">Lead Developer</p>
      <p class="bio">...</p>
    </div>
    <!-- Matti, Mika -->
  </div>
</section>
```

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 3 "HTML-rakenne suunniteltu: #team-section, .team-grid (grid 3-sarake), .team-member (card-tyyli), .avatar (syaani-reunus), .role (muted-väri), .bio (text-väri)."
```

---

## 5. KIERROS 4: REFINE – Avatar-komponentti

**Kehittäjä luo CSS**:
```css
.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  background: var(--bg-dark);
  margin: 0 auto 1rem;
}
```

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 4 "Avatar-tyyli valmis: pyöreä, syaani-reunus, tumma tausta. Placeholder-kuvat lisätään myöhemmin."
```

---

## 6. KIERROS 5: REFINE – Team-grid-layout

**Kehittäjä luo CSS**:
```css
.team-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .team-grid {
    grid-template-columns: 1fr;
  }
}
```

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 5 "Grid-layout valmis: 3 saraketta desktopilla, 1 sarake mobilella. Gap 2rem, responsiivinen breakpoint 768px."
```

---

## 7. KIERROS 6: REFINE – Typografia

**Kehittäjä tarkistaa ja lisää**:
```css
.team-member h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--text);
}

.team-member .role {
  font-size: 1rem;
  color: var(--muted);
  margin-bottom: 1rem;
}

.team-member .bio {
  font-size: 0.95rem;
  line-height: 1.6;
  color: var(--text);
}
```

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 6 "Typografia hierarkia: h3 (1.5rem, text), .role (1rem, muted), .bio (0.95rem, text, line-height 1.6)."
```

---

## 8. KIERROS 7: REFINE – Hover-efekti

**Kehittäjä lisää**:
```css
.team-member:hover {
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.4), 0 0 50px rgba(30, 58, 95, 0.3);
  transform: translateY(-5px);
  transition: all 0.3s ease;
}
```

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 7 "Hover-efekti valmis: glow (syaani + primary), translateY(-5px), smooth transition 0.3s."
```

---

## 9. KIERROS 8: REFINE – Kontrasti ja saavutettavuus

**Kehittäjä testaa**:
- Tarkistaa kontrastin (WCAG AA): ✅ Kaikki tekstit OK.
- Lisää `aria-label` avataareille (accessibility).

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 8 "Kontrasti testattu: WCAG AA OK. Lisätty aria-label avataarit. Saavutettavuus varmistettu."
```

---

## 10. KIERROS 9: MASTER – Toteutussuunnitelma

**Kehittäjä kokoaa**:
1. HTML: `<section id="team">` lisätään `index.html` (ennen footeria).
2. CSS: `.team-grid`, `.team-member`, `.avatar`, hover-efekti lisätään `styles.css`.
3. Placeholder-avataarit: Käytetään `codesphere-logo-128.png` väliaikaisesti.
4. Testaus: Desktop (3 saraketta), mobile (1 sarake), hover-efekti.

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 9 "Toteutus: HTML + CSS valmis, placeholder-avataarit, desktop/mobile-testaus suoritettu. Kaikki toimii."
```

---

## 11. KIERROS 10: MASTER – Hyväksymiskriteerit

**Kehittäjä tarkistaa**:
- ✅ Team-osio näkyy desktopilla (3 saraketta) ja mobilella (1 sarake).
- ✅ Hover-efekti toimii (glow + translateY).
- ✅ Typografia yhtenäinen (nimi → rooli → bio).
- ✅ Kontrasti WCAG AA.
- ✅ Dark theme säilyy (ei vaaleita taustoja).

**Päivitä muisti**:
```powershell
PS W:\Codex\Codesphere\website> python tools/trm_update_memory.py 10 "Hyväksymiskriteerit täytetty: responsive, hover, typografia, kontrasti, dark theme. Team-osio valmis."
```

---

## 12. VIIMEISTELE SESSIO

```powershell
PS W:\Codex\Codesphere\website> python tools/trm_finalize_session.py "Team-osio index.html valmis. Responsive 3-sarake → 1-sarake. Hover-glow, typografia-hierarkia, WCAG AA kontrasti. Dark theme säilyy. Kaikki testit OK."
```

**Output**:
```
╔════════════════════════════════════════════════════════════╗
║  ✅ TRM-SESSIO SULJETTU                                     ║
╚════════════════════════════════════════════════════════════╝

Tehtävä: Lisää Team-osio index.html – esittelee Timo, Matti, Mika dark-theme-tyylillä
Kierroksia suoritettu: 10
Malli: Thinking ➜ Reasoning ➜ Memory

─────────────────────────────────────────────────────────────
📄 TULOKSEN RAKENNE:

   1. Thinking (Ajattelu)
       Ongelma ymmärretty ja analysoitu

   2. Reasoning (Päättely)
       Ratkaisu kehitetty iteratiivisesti

   3. Memory (Muisti)
       Opit tallennettu tulevaa käyttöä varten

─────────────────────────────────────────────────────────────
✅ Opit tallennettu: W:\Codex\Codesphere\website\trm\memory.md
✅ Tila nollattu: W:\Codex\Codesphere\website\trm\state.json

💡 Voit nyt aloittaa uuden session:
   python tools/trm_start_session.py "Uusi tehtävä"
```

---

## 13. TARKISTA MUISTI

```powershell
PS W:\Codex\Codesphere\website> cat trm/memory.md | Select-String -Pattern "Session.*Team"
```

**Output**:
```
## Session: 2025-12-18 – Lisää Team-osio index.html – esittelee Timo, Matti, Mika dark-theme-tyylillä
```

**→ Opit tallennettu! Seuraava projekti hyötyy näistä oppeista (esim. avatar-tyyli, grid-layout, hover-efekti).**

---

## Yhteenveto

TRM 10× -järjestelmä ohjasi kehittäjän iteroimaan Team-osion 10 kierroksen kautta:
1. **Kierrokset 1-3 (THINK)**: Ongelma ymmärretty, layout suunniteltu, HTML-rakenne luotu.
2. **Kierrokset 4-8 (REFINE)**: Avatar, grid, typografia, hover, kontrasti kehitetty iteratiivisesti.
3. **Kierrokset 9-10 (MASTER)**: Toteutussuunnitelma ja hyväksymiskriteerit tarkistettu.

**Lopputulos**: Premium-laatuinen Team-osio, joka on responsiivinen, saavutettava ja yhtenäinen Codesphere-teeman kanssa. Opit tallennettu `trm/memory.md` → seuraava projekti on 10× helpompi.
