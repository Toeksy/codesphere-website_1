from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random
from typing import Any, cast

from PIL import Image, ImageDraw, ImageFilter, ImageFont


@dataclass(frozen=True)
class Person:
    name: str
    title: str
    phone_display: str
    phone_tel: str


@dataclass(frozen=True)
class Brand:
    bg_dark: tuple[int, int, int] = (10, 15, 26)  # #0A0F1A
    text: tuple[int, int, int] = (241, 245, 249)  # #F1F5F9
    muted: tuple[int, int, int] = (148, 163, 184)  # #94A3B8
    accent: tuple[int, int, int] = (0, 255, 255)  # #00FFFF
    primary: tuple[int, int, int] = (30, 58, 95)  # #1E3A5F


def _try_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    # Windows-friendly: Arial is usually available
    candidates = []
    if bold:
        candidates = ["arialbd.ttf", "Arial Bold.ttf", "arial.ttf"]
    else:
        candidates = ["arial.ttf", "Arial.ttf"]

    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _rounded_rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1):
    # Pillow rounded_rectangle exists in modern versions
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def _vertical_alpha_gradient(size: tuple[int, int], top_a: int, bottom_a: int) -> Image.Image:
    w, h = size
    grad = Image.new("L", (1, h))
    grad.putdata([int(top_a + (bottom_a - top_a) * (y / max(1, h - 1))) for y in range(h)])
    return grad.resize((w, h))


def _rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def _right_fade_mask(size: tuple[int, int], start_x: int, max_a: int) -> Image.Image:
    w, h = size
    start_x = max(0, min(w - 1, start_x))
    max_a = max(0, min(255, max_a))
    row: list[int] = []
    denom = max(1, (w - 1) - start_x)
    for x in range(w):
        if x <= start_x:
            row.append(0)
        else:
            t = (x - start_x) / denom
            row.append(int(max_a * t))
    grad = Image.new("L", (w, 1))
    grad.putdata(row)
    return grad.resize((w, h))


def _make_space_background(size: tuple[int, int], brand: Brand) -> Image.Image:
    """Avaruustausta, joka vastaa `brand-kit/digital/business-card.html` fiilistä."""
    w, h = size
    base = Image.new("RGBA", (w, h), brand.bg_dark + (255,))

    # Radiaaliglown tyyli: body background (accent vasen ylä, primary oikea ala)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse(
        (
            -int(0.55 * w),
            -int(0.45 * h),
            int(0.85 * w),
            int(0.75 * h),
        ),
        fill=brand.accent + (32,),
    )
    gdraw.ellipse(
        (
            int(0.35 * w),
            int(0.25 * h),
            int(1.35 * w),
            int(1.25 * h),
        ),
        fill=brand.primary + (52,),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    base = Image.alpha_composite(base, glow)

    # Card::before-tyyliset pehmeät sumuglown kerrokset
    fog = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    fdraw = ImageDraw.Draw(fog)
    fdraw.ellipse(
        (
            -int(0.20 * w),
            -int(0.20 * h),
            int(0.60 * w),
            int(0.55 * h),
        ),
        fill=brand.accent + (26,),
    )
    fdraw.ellipse(
        (
            int(0.45 * w),
            int(0.20 * h),
            int(1.20 * w),
            int(1.05 * h),
        ),
        fill=brand.primary + (34,),
    )
    fog = fog.filter(ImageFilter.GaussianBlur(18))
    base = Image.alpha_composite(base, fog)

    # Konstellaatio + renkaat koko kortin yli (yksi yhtenäinen tausta)
    rng = random.Random(1337)
    cx, cy = int(w * 0.34), int(h * 0.52)

    rings = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(rings)
    for rad, a, width in [
        (int(min(w, h) * 0.42), 42, 2),
        (int(min(w, h) * 0.50), 30, 2),
        (int(min(w, h) * 0.58), 18, 1),
    ]:
        rdraw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), outline=brand.accent + (a,), width=width)
    rings = rings.filter(ImageFilter.GaussianBlur(0.7))
    base = Image.alpha_composite(base, rings)

    net = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ndraw = ImageDraw.Draw(net)
    pts: list[tuple[int, int]] = []
    for _ in range(52):
        pts.append((rng.randint(int(w * 0.06), int(w * 0.94)), rng.randint(int(h * 0.08), int(h * 0.92))))

    for (x1, y1) in pts:
        candidates = sorted(pts, key=lambda p: (p[0] - x1) ** 2 + (p[1] - y1) ** 2)
        for (x2, y2) in candidates[1:4]:
            d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
            if d2 > (min(w, h) * 0.20) ** 2:
                continue
            ndraw.line((x1, y1, x2, y2), fill=brand.accent + (16,), width=1)

    for (x, y) in pts:
        a = rng.randint(60, 135)
        r = rng.choice([1, 1, 2])
        ndraw.ellipse((x - r, y - r, x + r, y + r), fill=brand.accent + (a,))

    net = net.filter(ImageFilter.GaussianBlur(0.4))
    base = Image.alpha_composite(base, net)

    # Subtle sheen
    sgrad = _vertical_alpha_gradient((w, h), 18, 0)
    sheen = Image.merge("RGBA", (Image.new("L", (w, h), 255),) * 3 + (sgrad,))
    sheen = sheen.rotate(18, expand=False)
    base = Image.alpha_composite(base, _mul_alpha(sheen, 0.50))

    # Vignette
    vignette = Image.new("L", (w, h), 0)
    vdraw = ImageDraw.Draw(vignette)
    vdraw.ellipse((-int(0.15 * w), -int(0.20 * h), int(1.15 * w), int(1.20 * h)), fill=190)
    vignette = vignette.filter(ImageFilter.GaussianBlur(26))
    shade = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    shade.putalpha(vignette)
    base = Image.alpha_composite(base, _mul_alpha(shade, 0.16))

    return base


def _draw_text_shadow(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
    shadow_rgba: tuple[int, int, int, int] = (0, 0, 0, 200),
    radius: int = 2,
) -> None:
    x, y = xy
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, fill=shadow_rgba, font=font)
    draw.text((x, y), text, fill=fill, font=font)


def _mul_alpha(img: Image.Image, factor: float) -> Image.Image:
    r, g, b, a = img.split()
    def _scale_alpha(p: int) -> int:
        v = int(p * factor)
        if v < 0:
            return 0
        if v > 255:
            return 255
        return v

    a = a.point(_scale_alpha)
    return Image.merge("RGBA", (r, g, b, a))


def make_business_card(out_png: Path, logo_path: Path, brand: Brand, people: list[Person]) -> None:
    # Digital business card aspect (same as classic 3.5"x2" @300dpi pixels): 1050x600
    w, h = 1050, 600
    img = _make_space_background((w, h), brand=brand)

    # Yhtenäinen tausta koko kortissa (ei laatikoita). Asetellaan sisältö kahteen sarakkeeseen.
    pad = 62
    gap = 44
    content_w = w - pad * 2
    left_w = int(content_w * 0.48)
    right_x0 = pad + left_w + gap

    # Load logo (large on the left)
    logo = Image.open(logo_path).convert("RGBA")
    target = int(min(left_w * 0.95, h * 0.80))
    if target < 320:
        target = 320
    if target > 520:
        target = 520
    image_any = cast(Any, Image)
    resampling_any = getattr(image_any, "Resampling", image_any)
    resample = getattr(resampling_any, "LANCZOS", getattr(resampling_any, "BICUBIC", 3))
    logo.thumbnail((target, target), cast(Any, resample))

    # Logo glow + placement
    glow_logo = Image.new("RGBA", logo.size, brand.accent + (0,))
    glow_logo.putalpha(logo.split()[-1])
    glow_logo = _mul_alpha(glow_logo.filter(ImageFilter.GaussianBlur(12)), 0.50)

    lx = pad + (left_w - logo.size[0]) // 2
    ly = (h - logo.size[1]) // 2
    img.alpha_composite(glow_logo, (lx, ly))
    img.alpha_composite(logo, (lx, ly))

    # Kontrastivahvistus tekstialueelle (pehmeä liuku, ei laatikkoa)
    fade = _right_fade_mask((w, h), start_x=max(0, right_x0 - 40), max_a=175)
    shade = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    shade.putalpha(fade)
    img = Image.alpha_composite(img, shade)

    draw = ImageDraw.Draw(img)

    # Text area (right column)
    tx = right_x0
    ty = pad + 6

    font_brand = _try_font(34, bold=True)
    font_h1 = _try_font(22, bold=True)
    font_p = _try_font(16, bold=False)

    _draw_text_shadow(draw, (tx, ty), "CODESPHERE", font=font_brand, fill=brand.text + (255,), shadow_rgba=(0, 0, 0, 220), radius=3)
    _draw_text_shadow(draw, (tx, ty + 44), "Yhteystiedot", font=font_p, fill=brand.muted + (245,), shadow_rgba=(0, 0, 0, 210), radius=2)

    # Divider
    div_y = ty + 78
    draw.line((tx, div_y, w - pad, div_y), fill=brand.accent + (140,), width=2)

    y = div_y + 18
    for person in people:
        _draw_text_shadow(draw, (tx, y), person.name, font=font_h1, fill=brand.text + (255,), shadow_rgba=(0, 0, 0, 220), radius=3)
        y += 26
        _draw_text_shadow(draw, (tx, y), person.title, font=font_p, fill=brand.muted + (245,), shadow_rgba=(0, 0, 0, 210), radius=2)
        y += 22
        _draw_text_shadow(draw, (tx, y), person.phone_display, font=font_p, fill=brand.accent + (255,), shadow_rgba=(0, 0, 0, 235), radius=2)
        y += 32

    # Footer small
    foot = "codesphere | globaalia ohjelmistokehitystä"
    _draw_text_shadow(draw, (tx, h - pad - 6), foot, font=_try_font(14, bold=False), fill=brand.muted + (200,), shadow_rgba=(0, 0, 0, 140), radius=1)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_png, format="PNG", optimize=True)


def write_vcards(out_vcf: Path, people: list[Person]) -> None:
    # vCard 3.0, multiple contacts
    lines: list[str] = []
    for person in people:
        # naive split name
        parts = person.name.split(" ")
        last = parts[-1] if parts else ""
        first = " ".join(parts[:-1]) if len(parts) > 1 else person.name
        lines.extend(
            [
                "BEGIN:VCARD",
                "VERSION:3.0",
                f"N:{last};{first};;;",
                f"FN:{person.name}",
                f"TITLE:{person.title}",
                "ORG:Codesphere",
                f"TEL;TYPE=CELL:{person.phone_tel}",
                "END:VCARD",
            ]
        )

    out_vcf.parent.mkdir(parents=True, exist_ok=True)
    out_vcf.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    # Käytä ensisijaisesti läpinäkyvää brand-kit logoversiota (terävämpi PNG:ssä)
    candidates = [
        base / "brand-kit" / "logo" / "codesphere-logo-4096-transparent.png",
        base / "brand-kit" / "logo" / "codesphere-logo-2048-transparent.png",
        base / "brand-kit" / "logo" / "codesphere-logo-1024-transparent.png",
        base / "brand-kit" / "logo" / "codesphere-logo-512-transparent.png",
        base / "codesphere-logo-680.png",
        base / "codesphere-logo-512.png",
    ]
    logo_path = next((p for p in candidates if p.exists()), candidates[-1])

    brand = Brand()
    people = [
        Person(
            name="Timo Aula",
            title="Toimitusjohtaja, Böethius Oy • Ohjelmistokehityksen asiantuntija",
            phone_display="puh +358 45 7977 3133",
            phone_tel="+3584579773133",
        ),
        Person(
            name="Matti Erholtz",
            title="Hallituksen jäsen • Markkinointijohtaja & Tekoälyarkkitehti",
            phone_display="puh +358 40 193 2714",
            phone_tel="+358401932714",
        ),
        Person(
            name="Mika Leppänen",
            title="Kyberturvallisuusasiantuntija • Asiantuntijatodistelu (tuomioistuimet)",
            phone_display="puh +358 46 558 1732",
            phone_tel="+358465581732",
        ),
    ]

    out_dir = base / "brand-kit" / "digital"
    make_business_card(out_dir / "business-card.png", logo_path=logo_path, brand=brand, people=people)
    write_vcards(out_dir / "contacts.vcf", people=people)

    print(f"Generated: {out_dir}")


if __name__ == "__main__":
    main()
