"""Renders a clean, legible terminal-style screenshot PNG from text lines.

This does NOT capture the real screen. It draws a synthetic terminal window
(titlebar + monospaced body) from the exact text we want shown, so every
slide screenshot is guaranteed clean and readable, with no risk of catching
unrelated windows.

Usage (as a library):
    from render_terminal import render
    render(
        title="~/11_ClaudeCode_Lecture_Demo/build",
        lines=["$ python3 validate.py schedule_v1.json", "", "FAILED — 3 problem(s) found:"],
        out_path="../screenshots/02_validate_v1_fail.png",
    )
"""
from PIL import Image, ImageDraw, ImageFont

FONT_REGULAR = "/usr/share/fonts/truetype/hack/Hack-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/hack/Hack-Bold.ttf"

WIDTH = 1600
FONT_SIZE = 22
LINE_HEIGHT = 34
PAD_X = 28
PAD_TOP = 70
PAD_BOTTOM = 30
TITLEBAR_H = 44
BG = (30, 32, 38)
TITLEBAR_BG = (43, 45, 52)
FG = (222, 226, 232)
GREEN = (98, 209, 150)
RED = (239, 108, 108)
YELLOW = (232, 193, 106)
CYAN = (110, 197, 232)
GRAY = (140, 146, 156)


def _color_for(line: str):
    s = line.strip()
    if s.startswith("$"):
        return CYAN, True
    if s.startswith("x ") or "FAILED" in s:
        return RED, s.startswith("FAILED")
    if "PASSED" in s:
        return GREEN, s.startswith("PASSED")
    if s.startswith("#") or s.startswith("//"):
        return GRAY, False
    return FG, False


def render(title: str, lines: list[str], out_path: str, width: int = WIDTH):
    height = PAD_TOP + len(lines) * LINE_HEIGHT + PAD_BOTTOM
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # titlebar
    draw.rectangle([0, 0, width, TITLEBAR_H], fill=TITLEBAR_BG)
    for i, c in enumerate([RED, YELLOW, GREEN]):
        cx = 26 + i * 26
        draw.ellipse([cx - 7, TITLEBAR_H // 2 - 7, cx + 7, TITLEBAR_H // 2 + 7], fill=c)
    title_font = ImageFont.truetype(FONT_REGULAR, 18)
    tw = draw.textlength(title, font=title_font)
    draw.text(((width - tw) / 2, TITLEBAR_H // 2 - 10), title, font=title_font, fill=GRAY)

    reg = ImageFont.truetype(FONT_REGULAR, FONT_SIZE)
    bold = ImageFont.truetype(FONT_BOLD, FONT_SIZE)

    y = PAD_TOP
    for line in lines:
        color, is_bold = _color_for(line)
        font = bold if is_bold else reg
        draw.text((PAD_X, y), line, font=font, fill=color)
        y += LINE_HEIGHT

    img.save(out_path)
    print(f"rendered: {out_path} ({width}x{height})")


if __name__ == "__main__":
    import sys, json
    spec = json.load(open(sys.argv[1]))
    render(spec["title"], spec["lines"], spec["out"])
