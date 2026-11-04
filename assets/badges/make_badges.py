"""Generate stamp-style gym badges (SVG) for the README badge case."""
import base64, math, re, sys
from pathlib import Path
from PIL import Image

ASSETS = Path(sys.argv[1])
OUT = ASSETS / "badges"
OUT.mkdir(exist_ok=True)

# (file slug, logo file, number, year, status)
BADGES = [
    ("01-perch",    "perch-app-icon.png",      "01", "2025", "active"),
    ("02-quant",    "hanyang-blue.png",        "02", "2025", "cleared"),
    ("03-haru",     "lg-electronics-logo.svg", "03", "2025", "cleared"),
    ("04-daiso",    "hyundai-ngv-logo.svg",    "04", "2026", "champion"),
    ("05-grova",    "profita-dark.png",        "05", "2026", "active"),
    ("06-kirothon", "aws-logo.png",            "06", "2026", "award"),
    ("07-ulog",     "kakaoimpact-dark.svg",    "07", "2026", "cleared"),
    ("08-hccl",     "hccl-blue.png",           "08", "2026", "active"),
    ("09-asbg",     "asbg-credly.png",         "09", "2026", "active"),
    ("10-sgr",      "sgr-logo.png",            "10", "2026", "active"),
    ("11-ey",       "ey-logo.svg",             "11", "2026", "active"),
    ("12-mois",     "mois-logo.svg",           "12", "2026", "active"),
]

STYLE = {
    #            light     dark      label
    "active":   ("#2F7BD6", "#0F3F78", "IN PROGRESS"),
    "cleared":  ("#1B3F6E", "#001A3A", "CLEARED"),
    "champion": ("#F2C94C", "#A8740A", "GRAND PRIZE"),
    "award":    ("#F2C94C", "#A8740A", "EXCELLENCE"),
}


def logo_size(path: Path):
    if path.suffix == ".png":
        return Image.open(path).size
    txt = path.read_text()
    m = re.search(r'viewBox="\s*[\d.\-]+[\s,]+[\d.\-]+[\s,]+([\d.]+)[\s,]+([\d.]+)', txt)
    if m:
        return float(m.group(1)), float(m.group(2))
    w = re.search(r'\bwidth="([\d.]+)', txt).group(1)
    h = re.search(r'\bheight="([\d.]+)', txt).group(1)
    return float(w), float(h)


def data_uri(path: Path):
    mime = "image/png" if path.suffix == ".png" else "image/svg+xml"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def scallop(cx, cy, r, amp, n, steps=360):
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        rr = r - amp * (1 - math.cos(n * t)) / 2
        pts.append(f"{cx + rr * math.cos(t):.2f},{cy + rr * math.sin(t):.2f}")
    return "M" + " L".join(pts) + " Z"


def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    return " ".join(pts)


def badge(slug, logo, num, year, status):
    light, dark, label = STYLE[status]
    gold = status in ("champion", "award")
    ink = "#4A3200" if gold else "#FFFFFF"
    path = ASSETS / logo
    w, h = logo_size(path)
    aspect = w / h
    if aspect > 1.6:          # wordmark
        bw, bh = 126, 46
    else:                     # emblem
        bw, bh = 80, 80
    s = min(bw / w, bh / h)
    lw, lh = w * s, h * s
    lx, ly = 100 - lw / 2, 100 - lh / 2

    clip = ""
    clip_attr = ""
    if slug == "01-perch":
        clip = f'<clipPath id="r"><rect x="{lx:.2f}" y="{ly:.2f}" width="{lw:.2f}" height="{lh:.2f}" rx="{lw*0.22:.2f}"/></clipPath>'
        clip_attr = ' clip-path="url(#r)"'

    font = "font-family=\"'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif\" font-weight=\"800\""
    trophy = ""
    if gold:
        trophy = f'<polygon points="{star(100, 34, 7)}" fill="{dark}" opacity="0.9"/>'
    check = ""
    if status == "cleared":
        check = (f'<circle cx="152" cy="152" r="15" fill="#2DA44E" stroke="#FFFFFF" stroke-width="3"/>'
                 f'<path d="M145 152.5 l5 5 l9.5 -10" fill="none" stroke="#FFFFFF" stroke-width="3.2" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{light}"/>
      <stop offset="1" stop-color="{dark}"/>
    </linearGradient>
    <radialGradient id="shine" cx="0.35" cy="0.25" r="0.8">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.35"/>
      <stop offset="0.6" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <path id="top" d="M 19 100 A 81 81 0 0 1 181 100"/>
    <path id="bot" d="M 11 100 A 89 89 0 0 0 189 100"/>
    {clip}
  </defs>
  <path d="{scallop(100, 100, 99, 5, 32)}" fill="url(#g)"/>
  <path d="{scallop(100, 100, 99, 5, 32)}" fill="url(#shine)"/>
  <circle cx="100" cy="100" r="91" fill="none" stroke="{ink}" stroke-opacity="0.55" stroke-width="1.2" stroke-dasharray="2.5 3"/>
  <circle cx="100" cy="100" r="73" fill="{dark}" opacity="0.55"/>
  <circle cx="100" cy="100" r="70" fill="#FFFFFF"/>
  <circle cx="100" cy="100" r="66" fill="none" stroke="{dark}" stroke-opacity="0.18" stroke-width="1.5"/>
  <text {font} font-size="12" letter-spacing="2.2" fill="{ink}">
    <textPath xlink:href="#top" href="#top" startOffset="50%" text-anchor="middle">No.{num} · {year}</textPath>
  </text>
  <text {font} font-size="11" letter-spacing="2.2" fill="{ink}">
    <textPath xlink:href="#bot" href="#bot" startOffset="50%" text-anchor="middle">{label}</textPath>
  </text>
  <polygon points="{star(14, 100, 5)}" fill="{ink}" opacity="0.85"/>
  <polygon points="{star(186, 100, 5)}" fill="{ink}" opacity="0.85"/>
  {trophy}
  <image x="{lx:.2f}" y="{ly:.2f}" width="{lw:.2f}" height="{lh:.2f}" preserveAspectRatio="xMidYMid meet"{clip_attr} xlink:href="{data_uri(path)}" href="{data_uri(path)}"/>
  {check}
</svg>
'''
    (OUT / f"{slug}.svg").write_text(svg)


for b in BADGES:
    badge(*b)
print("ok", len(BADGES))
