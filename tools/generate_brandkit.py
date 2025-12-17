from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class Palette:
    primary: str = "#1e3a5f"
    primary_light: str = "#2d5a87"
    accent: str = "#00ffff"
    bg_dark: str = "#0a0f1a"
    text: str = "#f1f5f9"


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load_logo(path: Path) -> Image.Image:
    return Image.open(path).convert("RGBA")


def _contain(img: Image.Image, target_w: int, target_h: int, padding: int) -> Image.Image:
    # keep aspect, fit within target minus padding
    max_w = max(1, target_w - 2 * padding)
    max_h = max(1, target_h - 2 * padding)

    w, h = img.size
    scale = min(max_w / w, max_h / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))

    resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def _contain_pixel_nearest(img: Image.Image, target_w: int, target_h: int, padding: int) -> Image.Image:
    # integer scaling only (for pixel logo)
    max_w = max(1, target_w - 2 * padding)
    max_h = max(1, target_h - 2 * padding)
    w, h = img.size
    scale = max(1, min(max_w // w, max_h // h))

    resized = img.resize((w * scale, h * scale), Image.NEAREST)
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    x = (target_w - resized.size[0]) // 2
    y = (target_h - resized.size[1]) // 2
    canvas.alpha_composite(resized, (x, y))
    return canvas


def _bg_solid(size: tuple[int, int], hex_color: str) -> Image.Image:
    r, g, b = _hex_to_rgb(hex_color)
    return Image.new("RGBA", size, (r, g, b, 255))


def _save_png(img: Image.Image, out_path: Path, dpi: tuple[int, int] | None = None) -> None:
    _ensure_dir(out_path.parent)
    save_kwargs = {}
    if dpi is not None:
        save_kwargs["dpi"] = dpi
    img.save(out_path, format="PNG", optimize=True, **save_kwargs)


def _draw_palette_swatch(out_path: Path, palette: Palette) -> None:
    w, h = 1400, 900
    img = _bg_solid((w, h), palette.bg_dark)
    draw = ImageDraw.Draw(img)

    items = [
        ("ACCENT", palette.accent),
        ("PRIMARY", palette.primary),
        ("PRIMARY_LIGHT", palette.primary_light),
        ("BG_DARK", palette.bg_dark),
        ("TEXT", palette.text),
    ]

    # font: try system, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 42)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()

    x0, y0 = 80, 80
    box_w, box_h, gap = 520, 110, 30

    for i, (label, hexc) in enumerate(items):
        y = y0 + i * (box_h + gap)
        draw.rounded_rectangle((x0, y, x0 + box_w, y + box_h), radius=18, fill=_hex_to_rgb(hexc) + (255,))
        draw.text((x0 + box_w + 40, y + 14), label, fill=_hex_to_rgb(palette.text) + (255,), font=font)
        draw.text((x0 + box_w + 40, y + 64), hexc.upper(), fill=_hex_to_rgb(palette.text) + (200,), font=font_small)

    _save_png(img, out_path)


def generate(out_dir: Path, base_dir: Path) -> None:
    palette = Palette()

    logo_main = _load_logo(base_dir / "codesphere-logo-680.png")
    logo_pixel = _load_logo(base_dir / "codesphere-logo-64.png")

    # === Logo pack (transparent) ===
    for size in (512, 1024, 2048, 4096):
        canvas = _contain(logo_main, size, size, padding=int(size * 0.12))
        _save_png(canvas, out_dir / "logo" / f"codesphere-logo-{size}-transparent.png")

    # Pixel logo pack
    for size in (256, 512, 1024):
        canvas = _contain_pixel_nearest(logo_pixel, size, size, padding=int(size * 0.12))
        _save_png(canvas, out_dir / "logo" / f"codesphere-logo-pixel-{size}.png")

    # === Social / web ===
    social = [
        ("social/profile", 1024, 1024),
        ("social/post", 1080, 1080),
        ("social/story", 1080, 1920),
        ("social/og", 1200, 630),
        ("social/x-header", 1500, 500),
        ("social/linkedin-banner", 1584, 396),
    ]

    for name, w, h in social:
        bg = _bg_solid((w, h), palette.bg_dark)
        placed = _contain(logo_main, w, h, padding=int(min(w, h) * 0.14))
        bg.alpha_composite(placed)
        _save_png(bg, out_dir / f"{name}.png")

    # === Display ads ===
    ads = [
        ("ads/300x250", 300, 250),
        ("ads/728x90", 728, 90),
        ("ads/160x600", 160, 600),
        ("ads/970x250", 970, 250),
    ]

    for name, w, h in ads:
        bg = _bg_solid((w, h), palette.bg_dark)
        placed = _contain(logo_main, w, h, padding=max(10, int(min(w, h) * 0.12)))
        bg.alpha_composite(placed)
        _save_png(bg, out_dir / f"{name}.png")

    # === Print (PNG with 300 DPI metadata) ===
    # A4 2480x3508 @300DPI, A5 1748x2480 @300DPI
    prints = [
        ("print/a4-portrait", 2480, 3508),
        ("print/a5-portrait", 1748, 2480),
        ("print/business-card-3.5x2in", 1050, 600),
        ("print/business-card-bleed-3.75x2.25in", 1125, 675),
    ]

    for name, w, h in prints:
        bg = _bg_solid((w, h), palette.bg_dark)
        placed = _contain(logo_main, w, h, padding=int(min(w, h) * 0.18))
        bg.alpha_composite(placed)
        _save_png(bg, out_dir / f"{name}.png", dpi=(300, 300))

    # Palette swatch
    _draw_palette_swatch(out_dir / "palette" / "codesphere-palette.png", palette)


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    out_dir = base_dir / "brand-kit"

    # Safety: avoid writing outside repo
    os.chdir(base_dir)
    generate(out_dir=out_dir, base_dir=base_dir)
    print(f"Brand kit generated: {out_dir}")


if __name__ == "__main__":
    main()
