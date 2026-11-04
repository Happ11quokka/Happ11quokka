"""Draw the Tech Stack as a pixel 'inventory' window from stack.json.

Usage: python3 assets/pixel/make_stack.py <dir with Galmuri11.ttf and Galmuri11-Bold.ttf>
Edit assets/pixel/stack.json to change items (label, chip colour, icon key, icon colour)
or levels (Advanced / Intermediate / Learning). Icon paths are from simple-icons (CC0).
Writes assets/pixel/stack.svg and prints the alt text.
"""
import json
import sys
from html import escape
from pathlib import Path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_pixel as mp  # noqa: E402

if len(sys.argv) > 1:
    mp.FONT_DIR = Path(sys.argv[1])

DATA = json.loads((HERE / "stack.json").read_text())
LEVELS = {"Advanced": 3, "Intermediate": 2, "Learning": 1}

W = 1200
PAD = 40
DOM_X, DOM_W = 52, 220
CHIP_X0, CHIP_X1 = 292, 1004
LV_X = 1032
CHIP_H, CHIP_GAP, LINE_GAP = 34, 8, 8
CHIP_FS, DOM_FS, LV_FS = 16, 20, 12
ICON = 16
LINE = "#E3D6B4"


class Measure:
    def __init__(self, file):
        f = TTFont(mp.FONT_DIR / file)
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        self.upm = f["head"].unitsPerEm

    def width(self, s, size):
        total = 0
        for ch in s:
            g = self.cmap.get(ord(ch))
            total += self.hmtx[g][0] if g else self.upm * 0.6
        return total * size / self.upm


def text_color(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return mp.INK if lum > 0.62 else "#FFFFFF"


def shade(hex_color, k=0.7):
    h = hex_color.lstrip("#")
    return "#" + "".join(f"{int(int(h[i:i + 2], 16) * k):02X}" for i in (0, 2, 4))


def step_rect(x, y, w, h, s, fill):
    return (f'<path fill="{fill}" d="M{x+s},{y} H{x+w-s} V{y+s} H{x+w} V{y+h-s} H{x+w-s} V{y+h} '
            f'H{x+s} V{y+h-s} H{x} V{y+s} H{x+s} Z"/>')


def icon_svg(key, color, x, y):
    ic = DATA["icons"].get(key) if key else None
    if not ic:
        return ""
    if "uri" in ic:
        return f'<image x="{x}" y="{y}" width="{ICON}" height="{ICON}" href="{escape(ic["uri"])}"/>'
    fill = "#FFFFFF" if color == "white" else ("#000000" if color == "black" else "#" + color.lstrip("#"))
    return (f'<g transform="translate({x} {y}) scale({ICON/24})">'
            f'<path fill="{fill}" d="{ic["path"]}"/></g>')


def main():
    bold = Measure("Galmuri11-Bold.ttf")
    body, chars_b, chars_r = [], set(), set()
    y = PAD + 52
    # column captions
    for x, cap, anchor in ((DOM_X, "DOMAIN", "start"), (CHIP_X0, "ITEMS", "start"), (W - PAD - 12, "LV", "end")):
        body.append(mp.text(x, PAD + 30, cap, 14, mp.BLUE, bold=True, anchor=anchor))
        chars_b.update(cap)
    body.append(f'<rect x="{PAD+8}" y="{PAD+42}" width="{W-2*PAD-16}" height="4" fill="{mp.INK}"/>')
    y = PAD + 62

    for ri, row in enumerate(DATA["rows"]):
        # lay chips out in lines
        lines, cur, cx = [], [], CHIP_X0
        for it in row["items"]:
            tw = bold.width(it["label"], CHIP_FS)
            cw = 10 + (ICON + 6 if it["icon"] and it["icon"] in DATA["icons"] else 0) + tw + 10
            if cur and cx + cw > CHIP_X1:
                lines.append(cur)
                cur, cx = [], CHIP_X0
            cur.append((it, cx, cw))
            cx += cw + CHIP_GAP
        if cur:
            lines.append(cur)
        block_h = len(lines) * CHIP_H + (len(lines) - 1) * LINE_GAP
        # domain (wrap on " · ")
        dom = row["domain"]
        parts = [dom] if bold.width(dom, DOM_FS) <= DOM_W else [p.strip() for p in dom.split("·")]
        if len(parts) == 2 and bold.width(dom, DOM_FS) > DOM_W:
            parts[0] += " ·"
        row_h = max(block_h, len(parts) * 26)
        top = y + 12
        dy0 = top + (row_h - len(parts) * 26) / 2 + 20
        for k, p in enumerate(parts):
            body.append(mp.text(DOM_X, dy0 + k * 26, p, DOM_FS, mp.NAVY, bold=True))
            chars_b.update(p)
        # chips
        cy = top + (row_h - block_h) / 2
        for line in lines:
            for it, x, cw in line:
                col = it["color"]
                body.append(step_rect(x, cy + 3, cw, CHIP_H - 3, 3, shade(col)))
                body.append(step_rect(x, cy, cw, CHIP_H - 3, 3, col))
                tx = x + 10
                ico = icon_svg(it["icon"], it["icon_color"], tx, cy + (CHIP_H - 3 - ICON) / 2)
                if ico:
                    body.append(ico)
                    tx += ICON + 6
                body.append(mp.text(tx, cy + 21, it["label"], CHIP_FS, text_color(col), bold=True))
                chars_b.update(it["label"])
            cy += CHIP_H + LINE_GAP
        # level gauge
        n = LEVELS.get(row["level"], 0)
        gy = top + row_h / 2 - 14
        for k in range(3):
            gx = LV_X + k * 36
            body.append(f'<rect x="{gx}" y="{gy}" width="30" height="14" fill="{mp.INK}"/>')
            body.append(f'<rect x="{gx+3}" y="{gy+3}" width="24" height="8" fill="{"#FFC83D" if k < n else "#F3E9CF"}"/>')
        body.append(mp.text(LV_X + 51, gy + 32, row["level"].upper(), LV_FS, mp.BLUE, bold=True, anchor="middle"))
        chars_b.update(row["level"].upper())
        y = top + row_h + 12
        if ri < len(DATA["rows"]) - 1:
            for dx in range(PAD + 12, W - PAD - 12, 12):
                body.append(f'<rect x="{dx}" y="{y}" width="6" height="2" fill="{LINE}"/>')
    H = int(y + PAD + 4)
    frame = mp.pixel_frame(4, 4, W - 8, H - 8, mp.CREAM, p=6)
    css = mp.fonts(bold_text="".join(sorted(chars_b)))
    alt = "Tech Stack — " + " / ".join(f'{r["domain"]} ({r["level"]}): ' + ", ".join(i["label"] for i in r["items"]) for r in DATA["rows"])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n'
           f'<title>{escape(alt)}</title>\n<style>{css}</style>\n{frame}\n' + "\n".join(body) + "\n</svg>\n")
    (HERE / "stack.svg").write_text(svg)
    print(alt)


if __name__ == "__main__":
    main()
