#!/usr/bin/env python3
"""Regenerate imgs/banner-*.png from scripts/banner-sources/*.txt (Andale Mono)."""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "scripts" / "banner-sources"
FONT_PATH = "/System/Library/Fonts/Supplemental/Andale Mono.ttf"
FONT_SIZE = 22
LINE_EXTRA = 3
PAD = 28
FG_DEFAULT = (137, 206, 120)
# Must match style.css body.page-submit --submit-mint (#30dcca).
FG_SUBMIT_PAGE = (0x30, 0xDC, 0xCA)
# About page banner text colour (requested).
FG_ABOUT_PAGE = (0xFE, 0x57, 0x99)  # #fe5799

# (txt, png, bg, fg)
JOBS = [
    ("home.txt", "banner-home.png", (19, 19, 19), FG_DEFAULT),
    ("home.txt", "banner-about.png", (0, 0, 0), FG_ABOUT_PAGE),
    ("home.txt", "banner-submit.png", (0, 0, 0), FG_SUBMIT_PAGE),
]


def load_lines(name: str) -> list[str]:
    path = SOURCES / name
    if not path.is_file():
        sys.exit(f"Missing {path}")
    raw = path.read_text(encoding="utf-8")
    lines = raw.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def render(
    lines: list[str],
    bg: tuple[int, int, int],
    fg: tuple[int, int, int],
    out_path: Path,
) -> None:
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    probe = Image.new("RGB", (8, 8), bg)
    draw = ImageDraw.Draw(probe)
    max_w = 0
    line_h = FONT_SIZE + LINE_EXTRA
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        max_w = max(max_w, bbox[2] - bbox[0])
    img_w = max_w + 2 * PAD
    img_h = len(lines) * line_h + 2 * PAD
    im = Image.new("RGB", (img_w, img_h), bg)
    draw = ImageDraw.Draw(im)
    y = PAD
    for line in lines:
        draw.text((PAD, y), line, font=font, fill=fg)
        y += line_h
    im.save(out_path, optimize=True)


def main() -> None:
    for txt_name, png_name, bg, fg in JOBS:
        lines = load_lines(txt_name)
        out = ROOT / "imgs" / png_name
        render(lines, bg, fg, out)
        print(f"wrote {out} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
