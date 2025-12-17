from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rl_canvas


@dataclass(frozen=True)
class Brand:
    bg_dark: Color = Color(10 / 255, 15 / 255, 26 / 255)
    accent: Color = Color(0, 1, 1)  # #00FFFF
    primary: Color = Color(30 / 255, 58 / 255, 95 / 255)  # #1E3A5F


def _mm(v: float) -> float:
    return v * mm


def _draw_boxes(c: rl_canvas.Canvas, trim_w: float, trim_h: float, bleed: float, safe: float, brand: Brand) -> None:
    page_w = trim_w + 2 * bleed
    page_h = trim_h + 2 * bleed

    # Background to full bleed
    c.setFillColor(brand.bg_dark)
    c.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    # Trim box
    c.saveState()
    c.setStrokeColor(Color(1, 1, 1, alpha=0.45))
    c.setLineWidth(0.6)
    c.rect(bleed, bleed, trim_w, trim_h, stroke=1, fill=0)

    # Safe box
    c.setStrokeColor(Color(0, 1, 1, alpha=0.35))
    c.setDash(4, 3)
    c.setLineWidth(0.6)
    c.rect(bleed + safe, bleed + safe, trim_w - 2 * safe, trim_h - 2 * safe, stroke=1, fill=0)
    c.restoreState()

    # Crop marks
    mark = _mm(6)
    gap = _mm(1)
    c.saveState()
    c.setStrokeColor(Color(1, 1, 1, alpha=0.7))
    c.setLineWidth(0.8)

    x0, y0 = bleed, bleed
    x1, y1 = bleed + trim_w, bleed + trim_h

    # Bottom-left
    c.line(x0 - gap - mark, y0, x0 - gap, y0)
    c.line(x0, y0 - gap - mark, x0, y0 - gap)
    # Bottom-right
    c.line(x1 + gap, y0, x1 + gap + mark, y0)
    c.line(x1, y0 - gap - mark, x1, y0 - gap)
    # Top-left
    c.line(x0 - gap - mark, y1, x0 - gap, y1)
    c.line(x0, y1 + gap, x0, y1 + gap + mark)
    # Top-right
    c.line(x1 + gap, y1, x1 + gap + mark, y1)
    c.line(x1, y1 + gap, x1, y1 + gap + mark)

    c.restoreState()


def _place_logo(c: rl_canvas.Canvas, logo_path: Path, page_w: float, page_h: float, bleed: float, safe: float) -> None:
    # Place logo inside safe area, centered
    safe_w = page_w - 2 * (bleed + safe)
    safe_h = page_h - 2 * (bleed + safe)

    # target: about 35% of shorter safe dimension
    target = min(safe_w, safe_h) * 0.55

    # reportlab can read PNG directly
    x = (page_w - target) / 2
    y = (page_h - target) / 2
    c.drawImage(str(logo_path), x, y, width=target, height=target, mask='auto', preserveAspectRatio=True, anchor='c')


def _make_pdf(out_path: Path, trim_mm_w: float, trim_mm_h: float, bleed_mm: float, safe_mm: float, logo_path: Path, title: str) -> None:
    brand = Brand()
    trim_w = _mm(trim_mm_w)
    trim_h = _mm(trim_mm_h)
    bleed = _mm(bleed_mm)
    safe = _mm(safe_mm)

    page_w = trim_w + 2 * bleed
    page_h = trim_h + 2 * bleed

    out_path.parent.mkdir(parents=True, exist_ok=True)
    c = rl_canvas.Canvas(str(out_path), pagesize=(page_w, page_h))

    _draw_boxes(c, trim_w=trim_w, trim_h=trim_h, bleed=bleed, safe=safe, brand=brand)
    _place_logo(c, logo_path=logo_path, page_w=page_w, page_h=page_h, bleed=bleed, safe=safe)

    # small label (outside safe, but inside bleed) for operator clarity
    c.saveState()
    c.setFillColor(Color(1, 1, 1, alpha=0.65))
    c.setFont("Helvetica", 8)
    c.drawString(_mm(4), _mm(3), f"{title} | trim {trim_mm_w}×{trim_mm_h}mm | bleed {bleed_mm}mm | safe {safe_mm}mm")
    c.restoreState()

    c.showPage()
    c.save()


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    logo = base / "codesphere-logo-680.png"
    out_dir = base / "brand-kit" / "print-pdf"

    # Common print settings
    bleed_mm = 3.0
    safe_mm = 5.0

    # A4 portrait
    _make_pdf(
        out_dir / "codesphere-a4-portrait.pdf",
        trim_mm_w=210,
        trim_mm_h=297,
        bleed_mm=bleed_mm,
        safe_mm=safe_mm,
        logo_path=logo,
        title="Codesphere A4",
    )

    # A5 portrait
    _make_pdf(
        out_dir / "codesphere-a5-portrait.pdf",
        trim_mm_w=148,
        trim_mm_h=210,
        bleed_mm=bleed_mm,
        safe_mm=safe_mm,
        logo_path=logo,
        title="Codesphere A5",
    )

    # Business card (FIN common 85×55mm)
    _make_pdf(
        out_dir / "codesphere-business-card-85x55.pdf",
        trim_mm_w=85,
        trim_mm_h=55,
        bleed_mm=bleed_mm,
        safe_mm=4.0,
        logo_path=logo,
        title="Codesphere business card",
    )

    print(f"Generated PDFs in: {out_dir}")


if __name__ == "__main__":
    main()
