# Codesphere – brändimateriaalit (exportit)

Tämä kansio sisältää valmiit jaettavat tiedostot webiin, mainontaan ja painoon.

## Värit (site + brändi)

- Accent (logo): `#00FFFF`
- Primary: `#1E3A5F`
- Primary light: `#2D5A87`
- Background: `#0A0F1A`
- Text: `#F1F5F9`

Värikartta: `palette/codesphere-palette.png`

## Logot

- Läpinäkyvät logot: `logo/codesphere-logo-*-transparent.png`
- Pixel-logo (nearest): `logo/codesphere-logo-pixel-*.png`

## Some / web

- Profiili: `social/profile.png` (1024×1024)
- Postaus: `social/post.png` (1080×1080)
- Story: `social/story.png` (1080×1920)
- OG-kuva: `social/og.png` (1200×630)
- X header: `social/x-header.png` (1500×500)
- LinkedIn banner: `social/linkedin-banner.png` (1584×396)

## Mainonta (display)

- `ads/300x250.png`
- `ads/728x90.png`
- `ads/160x600.png`
- `ads/970x250.png`

## Digitaalinen käyntikortti

- PNG: `digital/business-card.png` (1050×600)
- vCard: `digital/contacts.vcf`
- Live: `digital/business-card.html` (selaimessa, sisältää Codesphere-sivun esikatselun)

## Print (PNG, 300 DPI metadata)

- A4: `print/a4-portrait.png` (2480×3508 @300DPI)
- A5: `print/a5-portrait.png` (1748×2480 @300DPI)
- Käyntikortti: `print/business-card-3.5x2in.png` (1050×600 @300DPI)
- Käyntikortti bleedeillä: `print/business-card-bleed-3.75x2.25in.png` (1125×675 @300DPI)

## Print (PDF, bleed + turva-alue)

- A4: `print-pdf/codesphere-a4-portrait.pdf` (trim 210×297mm, bleed 3mm, safe 5mm)
- A5: `print-pdf/codesphere-a5-portrait.pdf` (trim 148×210mm, bleed 3mm, safe 5mm)
- Käyntikortti: `print-pdf/codesphere-business-card-85x55.pdf` (trim 85×55mm, bleed 3mm, safe 4mm)

Huom: painotalot pyytävät usein PDF/SVG-aineistoa. Nämä PNG:t ovat käyttökelpoisia moniin käyttötarkoituksiin, mutta jos haluat, teen seuraavaksi myös painovalmiit PDF:t (bleed + turva-alue).

## Uudelleen generointi

Aja:

```powershell
Set-Location "C:\Users\matti\Desktop\VS-Code\Käyttäjä\Codesphere\website"
python .\tools\generate_brandkit.py

# PDF:t painoon
python .\tools\generate_print_pdfs.py
```
