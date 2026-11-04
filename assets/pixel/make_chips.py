"""Draw the Experience keyword chips in the Tech Stack inventory style, one SVG per chip.

Usage: python3 assets/pixel/make_chips.py <dir with Galmuri11.ttf and Galmuri11-Bold.ttf>
Edit assets/pixel/chips.json: "entries" maps an entry slug to its chips (label, color, icon,
url); "icons" holds simple-icons paths (CC0) keyed by slug. Writes
assets/pixel/chips/<slug>-<n>.svg and prints the README markdown for each entry.
"""
import json
import sys
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_pixel as mp  # noqa: E402

if len(sys.argv) > 1:
    mp.FONT_DIR = Path(sys.argv[1])

from make_stack import Measure, shade, step_rect, text_color  # noqa: E402

DATA = json.loads((HERE / "chips.json").read_text())
OUT = HERE / "chips"
RAW = "https://raw.githubusercontent.com/Happ11quokka/Happ11quokka/main/assets/pixel/chips"
CHIP_H, FS, ICON, PADX = 34, 16, 16, 10
SHOW_H = 26  # rendered height in the README


def icon_svg(key, color, x, y):
    ic = DATA["icons"].get(key) if key else None
    if not ic:
        return ""
    fill = "#FFFFFF" if text_color(color) == "#FFFFFF" else mp.INK
    return (f'<g transform="translate({x} {y}) scale({ICON/24})">'
            f'<path fill="{fill}" d="{ic}"/></g>')


def chip(it, bold):
    col = it["color"]
    has_icon = bool(it.get("icon")) and it["icon"] in DATA["icons"]
    tw = bold.width(it["label"], FS)
    cw = round(PADX + (ICON + 6 if has_icon else 0) + tw + PADX)
    body = [step_rect(0, 3, cw, CHIP_H - 3, 3, shade(col)), step_rect(0, 0, cw, CHIP_H - 3, 3, col)]
    tx = PADX
    if has_icon:
        body.append(icon_svg(it["icon"], col, tx, (CHIP_H - 3 - ICON) / 2))
        tx += ICON + 6
    body.append(mp.text(tx, 21, it["label"], FS, text_color(col), bold=True))
    css = mp.fonts(bold_text=it["label"])
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {CHIP_H}" width="{cw}" height="{CHIP_H}">\n'
            f'<title>{escape(it["label"])}</title>\n<style>{css}</style>\n' + "\n".join(body) + "\n</svg>\n"), cw


def main():
    bold = Measure("Galmuri11-Bold.ttf")
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for slug, items in DATA["entries"].items():
        tags = []
        for n, it in enumerate(items, 1):
            svg, cw = chip(it, bold)
            name = f"{slug}-{n}.svg"
            (OUT / name).write_text(svg)
            w = round(cw * SHOW_H / CHIP_H)
            img = (f'<img src="{RAW}/{name}" height="{SHOW_H}" width="{w}" '
                   f'alt="{escape(it["label"])}" />')
            tags.append(f'<a href="{escape(it["url"])}">{img}</a>' if it.get("url") else img)
        print(f"<!-- {slug} -->\n<p>\n" + "\n".join(tags) + "\n</p>\n")


if __name__ == "__main__":
    main()
