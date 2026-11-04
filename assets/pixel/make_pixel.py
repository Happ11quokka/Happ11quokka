"""Pixel-art pieces for the profile README (original art, retro RPG look).

Usage: python3 assets/pixel/make_pixel.py <dir with Galmuri11.ttf and Galmuri11-Bold.ttf>
Fonts: Galmuri by Lee Minseo, SIL OFL 1.1 (https://github.com/quiple/galmuri),
       npm galmuri@2.40.2 dist/. Each SVG embeds only the glyphs it uses.
Writes: assets/pixel/{header,footer,hello,title-*}.svg
"""
import base64, io, sys
from html import escape
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE

# ── palette ────────────────────────────────────────────────
INK = "#1B2238"
NAVY = "#002856"
BLUE = "#1C5FA8"
SKY = ["#1C5FA8", "#2A70BE", "#3B82CF", "#4F95DC", "#66A8E6", "#80BBEE", "#9CCDF4"]
CREAM = "#FFF8E7"
FRAME_IN = "#5C9BD9"
GRASS, GRASS_D, GRASS_L = "#4CAF50", "#2E7D32", "#81C784"
DIRT, DIRT_D = "#A0683A", "#7A4A24"
HILL_B, HILL_F = "#2F6B8F", "#3E8E64"


# ── fonts ──────────────────────────────────────────────────
def font_face(family, file, text):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = []
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    f = TTFont(FONT_DIR / file)
    s = subset.Subsetter(opts)
    s.populate(text=text + " ")
    s.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{b64}) format('woff2');}}"


def fonts(regular_text="", bold_text=""):
    css = ""
    if regular_text:
        css += font_face("GalmuriR", "Galmuri11.ttf", regular_text)
    if bold_text:
        css += font_face("GalmuriB", "Galmuri11-Bold.ttf", bold_text)
    return css


def text(x, y, s, size, fill, bold=False, anchor="start", shadow=None, extra=""):
    fam = "GalmuriB" if bold else "GalmuriR"
    t = escape(s)
    out = ""
    if shadow:
        dx = max(2, size // 11)
        out += (f'<text x="{x+dx}" y="{y+dx}" font-family="{fam}" font-size="{size}" fill="{shadow}" '
                f'text-anchor="{anchor}"{extra}>{t}</text>')
    out += (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{extra}>{t}</text>')
    return out


# ── sprites (original) ─────────────────────────────────────
QUOKKA = [
    "...oo......oo...",
    "..obbo....obbo..",
    "..obpboooobpbo..",
    "..obbbbbbbbbbo..",
    ".obbbbbbbbbbbbo.",
    ".obbebbbbbbebbo.",
    ".obbebbbbbbebbo.",
    ".obpbllnnllbpbo.",
    ".obbllllllllbbo.",
    "..obllollollbo..",
    "..obbllooollbbo.",
    "...obbbbbbbbo...",
    "..obbllllllbbo..",
    "..obllllllllbo..",
    "..obbllllllbbo..",
    "..oobbo..obboo..",
]
QUOKKA_C = {"o": "#3B2414", "b": "#A9713F", "l": "#EBC9A0", "p": "#F2A0A0", "e": "#1B1B1B", "n": "#3B2414"}

BIRD = [
    "....oooo....",
    "...oyyyyo...",
    "..oyyeyyyo..",
    "..oyyyyykko.",
    "..oyyyyykko.",
    "..ogyyyyyo..",
    ".oggggggggo.",
    ".ogggdddggo.",
    ".oggdddddgo.",
    "..oggdddgo..",
    "...oggggo...",
    "....k..k....",
]
BIRD_C = {"o": "#1E3A1E", "y": "#FFE066", "e": "#1B1B1B", "k": "#F28C28", "g": "#5DC26A", "d": "#2E8B57"}

ICONS = {
    "bolt": ["...oooo.", "..oyyyo.", ".oyyyo..", "oyyyyyyo", "oooyyyo.", "..oyyo..", ".oyyo...", ".oo....."],
    "medal": ["oo....oo", "orr..bbo", ".orrbbo.", "..oyyo..", ".oyyyyo.", "oyyhyyyo", "oyyyyyyo", ".oyyyyo."],
    "bag": ["..oooo..", ".o....o.", "oooooooo", "onnnnnno", "onnyynno", "onnnnnno", "onnnnnno", "oooooooo"],
    "chat": ["oooooooo", "owwwwwwo", "owbwbwbo", "owwwwwwo", "oooowooo", "...owo..", "...oo...", "........"],
}
ICON_C = {"n": "#B5763C", "o": INK, "y": "#FFC83D", "r": "#E5484D", "b": BLUE, "h": "#FFF2B3", "w": "#FFFFFF"}


def sprite(rows, colors, px, x0, y0):
    out = []
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            ch = row[c]
            if ch == ".":
                c += 1
                continue
            run = 1
            while c + run < len(row) and row[c + run] == ch:
                run += 1
            out.append(f'<rect x="{x0 + c*px}" y="{y0 + r*px}" width="{run*px}" height="{px}" fill="{colors[ch]}"/>')
            c += run
    return "".join(out)


def pixel_frame(x, y, w, h, fill, outer=INK, inner=FRAME_IN, p=4):
    """RPG window: dark outline with stepped corners + light inner rule."""
    def box(x, y, w, h, s):
        return (f"M{x+s},{y} H{x+w-s} V{y+s} H{x+w} V{y+h-s} H{x+w-s} V{y+h} H{x+s} V{y+h-s} H{x} V{y+s} H{x+s} Z")
    return (f'<path d="{box(x, y, w, h, p)}" fill="{outer}"/>'
            f'<path d="{box(x+p, y+p, w-2*p, h-2*p, p)}" fill="{fill}"/>'
            f'<path d="{box(x+2*p, y+2*p, w-4*p, h-4*p, p)}" fill="none" stroke="{inner}" stroke-width="{p/2}"/>')


def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'shape-rendering="crispEdges">\n<title>{escape(title)}</title>\n<style>{css}</style>\n{body}\n</svg>\n')


# ── ground / scenery helpers ───────────────────────────────
def sky(w, h, band=None):
    band = band or h / len(SKY)
    return "".join(f'<rect x="0" y="{i*band:.0f}" width="{w}" height="{band+1:.0f}" fill="{c}"/>' for i, c in enumerate(SKY))


def cloud(x, y, px=6):
    rows = ["..wwww....", ".wwwwwww..", "wwwwwwwwww", ".ssssssss."]
    return sprite(rows, {"w": "#FFFFFF", "s": "#D6E9F8"}, px, x, y)


def hills(w, base, color, step, heights, seed):
    pts = []
    x = 0
    i = seed
    while x < w + step:
        hgt = heights[i % len(heights)]
        pts.append(f'<rect x="{x}" y="{base-hgt}" width="{step}" height="{hgt+200}" fill="{color}"/>')
        x += step
        i += 1
    return "".join(pts)


def ground(w, y, h):
    out = [f'<rect x="0" y="{y}" width="{w}" height="{h}" fill="{DIRT}"/>',
           f'<rect x="0" y="{y}" width="{w}" height="12" fill="{GRASS}"/>',
           f'<rect x="0" y="{y+12}" width="{w}" height="4" fill="{GRASS_D}"/>']
    for x in range(0, w, 24):
        out.append(f'<rect x="{x+4}" y="{y}" width="4" height="4" fill="{GRASS_L}"/>')
        out.append(f'<rect x="{x+14}" y="{y-4}" width="4" height="4" fill="{GRASS}"/>')
    for i, x in enumerate(range(8, w, 36)):
        yy = y + 24 + (i * 13) % (max(8, h - 32))
        out.append(f'<rect x="{x}" y="{yy}" width="8" height="4" fill="{DIRT_D}"/>')
    return "".join(out)


def bob(content, dy=-4, dur="0.8s"):
    return (f'<g>{content}<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 {dy};0 0" keyTimes="0;0.5;1" calcMode="discrete" dur="{dur}" repeatCount="indefinite"/></g>')


def drift(content, dist, dur):
    return (f'<g>{content}<animateTransform attributeName="transform" type="translate" '
            f'values="0 0;{dist} 0;0 0" dur="{dur}" repeatCount="indefinite"/></g>')


# ── pieces ─────────────────────────────────────────────────
def header():
    W, H = 1200, 320
    title, sub = "HI, I'M DONGHYUN", "AI ENGINEER · SOFTWARE ENGINEER · SINGULARITY MAKER"
    body = [sky(W, 260, 260 / len(SKY))]
    body.append(drift(cloud(40, 34) + cloud(980, 84, 5), 30, "14s"))
    body.append(drift(cloud(1060, 24, 4), -24, "18s"))
    body.append(hills(W, 236, HILL_B, 40, [56, 72, 88, 72, 60, 48, 64, 80, 96, 80, 64, 52], 0))
    body.append(hills(W, 252, HILL_F, 32, [24, 32, 40, 32, 24, 20, 28, 36, 28, 22], 3))
    body.append(ground(W, 252, 68))
    body.append(text(600, 104, title, 66, "#FFFFFF", bold=True, anchor="middle", shadow=NAVY))
    body.append(text(600, 146, sub, 22, "#FFFFFF", anchor="middle", shadow=NAVY))
    body.append(bob(sprite(QUOKKA, QUOKKA_C, 6, 150, 252 - 16 * 6)))
    # speech bubble
    body.append(pixel_frame(256, 160, 84, 50, "#FFFFFF", p=4))
    body.append(f'<rect x="252" y="196" width="8" height="12" fill="{INK}"/><rect x="256" y="200" width="4" height="4" fill="#FFFFFF"/>')
    body.append(text(298, 194, "HI!", 22, INK, bold=True, anchor="middle"))
    body.append(bob(sprite(BIRD, BIRD_C, 6, 984, 252 - 12 * 6), dy=-6, dur="1.1s"))
    css = fonts(regular_text=sub, bold_text=title + "HI!")
    return svg(W, H, "\n".join(body), css, "Hi, I'm Donghyun — AI Engineer · Software Engineer · Singularity Maker")


def hello():
    W, H = 1200, 196
    l1 = "Hi, I'm DONGHYUN!"
    l2 = "An AI / Software Engineer building real-world AI systems"
    l3 = "and exploring what comes next."
    body = [pixel_frame(4, 4, W - 8, H - 8, CREAM, p=6)]
    body.append(text(52, 72, l1, 33, BLUE, bold=True))
    body.append(text(52, 118, l2, 27, INK))
    body.append(text(52, 158, l3, 27, INK))
    arrow = f'<path d="M1124 150 h24 v6 h-6 v6 h-6 v6 h-6 v-6 h-6 v-6 h0 z" fill="{INK}"/>'
    body.append(f'<g>{arrow}<animate attributeName="opacity" values="1;0;1" keyTimes="0;0.5;1" calcMode="discrete" dur="1s" repeatCount="indefinite"/></g>')
    css = fonts(regular_text=l2 + l3, bold_text=l1)
    return svg(W, H, "\n".join(body), css, f"{l1} {l2} {l3}")


def title_bar(slug, icon, label, sub=""):
    W, H = 1200, 96
    body = [pixel_frame(4, 4, W - 8, H - 8, CREAM, p=6)]
    body.append(sprite(ICONS[icon], ICON_C, 5, 44, 28))
    body.append(text(108, 64, label, 33, NAVY, bold=True))
    if sub:
        body.append(text(W - 48, 62, sub, 27, BLUE, bold=True, anchor="end"))
    blink = f'<path d="M84 42 h0" />'
    css = fonts(bold_text=label + sub)
    (HERE / f"title-{slug}.svg").write_text(svg(W, H, "\n".join(body), css, f"{label} {sub}".strip()))


def footer():
    W, H = 1200, 200
    body = [f'<rect width="{W}" height="{H}" fill="{NAVY}"/>']
    stars = [(60, 30), (180, 70), (300, 24), (430, 60), (560, 34), (700, 76), (820, 28), (950, 58), (1080, 36), (1150, 80), (250, 110), (900, 110)]
    for i, (x, y) in enumerate(stars):
        body.append(f'<rect x="{x}" y="{y}" width="4" height="4" fill="#FFF2B3"><animate attributeName="opacity" values="1;0.2;1" dur="{1.6 + (i % 4) * 0.5}s" repeatCount="indefinite"/></rect>')
    body.append(sprite(["..mmm.", ".mmm..", "mmm...", "mmm...", ".mmm..", "..mmm."], {"m": "#FFF2B3"}, 6, 1040, 20))
    body.append(hills(W, 150, "#123B6B", 40, [24, 36, 48, 36, 28, 20, 32, 44, 52, 40, 30, 22], 2))
    body.append(ground(W, 150, 50))
    line = "THANKS FOR STOPPING BY!"
    sub = "SEE YOU AT THE NEXT GYM  ·  MADE IN SEOUL"
    body.append(text(600, 74, line, 33, "#FFFFFF", bold=True, anchor="middle", shadow="#000F24"))
    body.append(text(600, 108, sub, 16.5, "#9CCDF4", anchor="middle"))
    walker = sprite(QUOKKA, QUOKKA_C, 4, 0, 150 - 16 * 4)
    body.append(f'<g>{bob(walker, dy=-4, dur="0.5s")}<animateTransform attributeName="transform" type="translate" '
                f'values="-80 0;1220 0" dur="16s" repeatCount="indefinite"/></g>')
    css = fonts(regular_text=sub, bold_text=line)
    return svg(W, H, "\n".join(body), css, "Thanks for stopping by!")


def main():
    (HERE / "header.svg").write_text(header())
    (HERE / "hello.svg").write_text(hello())
    (HERE / "footer.svg").write_text(footer())
    title_bar("working-on", "bolt", "WHAT I'M WORKING ON")
    title_bar("gym", "medal", "GYM CHALLENGE", "도장깨기")
    title_bar("stack", "bag", "TECH STACK")
    title_bar("say-hi", "chat", "SAY HI")
    for f in sorted(HERE.glob("*.svg")):
        print(f.name, f.stat().st_size)


if __name__ == "__main__":
    main()
