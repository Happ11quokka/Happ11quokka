"""Build the Gym Challenge cards and README block from the pixel badges.

Usage: python3 assets/badges/make_cards.py
Writes assets/badges/cards/NN-<slug>.svg and prints the README block.
To add a badge: drop <slug>.png (square) into assets/badges/ and add a row to BADGES.
"""
import base64
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARDS = HERE / "cards"
RAW = "https://raw.githubusercontent.com/Happ11quokka/Happ11quokka/main/assets/badges/cards/"

A, C, G = "active", "cleared", "trophy"
# slug, link, name, role, year, status, prize
BADGES = [
    ("perch", "https://apps.apple.com/us/app/%ED%8D%BC%EC%B9%98%EC%BC%80%EC%96%B4/id6758549078?l=ko", "Perch", "Founder · App & Smart Scale", "2025", A, None),
    ("hanyang-quant", "https://github.com/Happ11quokka/StockNewsEstimator", "Hanyang Quant Lab", "Research Intern · APAF 2025", "2025", C, None),
    ("nexon", "https://kr-newsroom.nexon.com/press-center/3399289", "Nexon HelloMate", "Coding Mentor", "2025", C, None),
    ("lg-haru", "https://github.com/Happ11quokka/SWE-G04-SPACE", "HARU × LG Electronics", "IC-PBL · iOS / watchOS", "2025", C, None),
    ("kople", "https://github.com/Happ11quokka/koplegame", "Kople Game", "Real-time PWA Game", "2025", C, None),
    ("hyundai-daiso", "https://github.com/Happ11quokka/hyu-ngv-manufacturing-ai-agent", "dAIso × Hyundai NGV", "Manufacturing AI Agent", "2026", G, "GRAND PRIZE"),
    ("profita", "https://www.aiprofita.com", "GROVA Technology", "AI Engineer · Profita", "2026", A, None),
    ("lg-aimers", "https://github.com/Happ11quokka/lg-aimers8-llm-compression", "LG Aimers 8th", "LLM Compression", "2026", C, None),
    ("aws-kirothon", "https://github.com/Happ11quokka/hackathon-store", "AWS KIROTHON", "Kiro Hackathon", "2026", G, "EXCELLENCE"),
    ("hyu-agentic-rag", "https://github.com/Happ11quokka/agentic-rag", "Capstone · Agentic RAG", "Speculative Retrieval", "2026", A, None),
    ("kakao-ulog", "https://github.com/Happ11quokka/kakao_impact", "Ulog × Kakao Impact", "Backend & AI", "2026", C, None),
    ("hcc", "https://hcc.hanyang.ac.kr/", "Hanyang HCC Lab", "Undergraduate Researcher", "2026", A, None),
    ("asbg", "https://www.credly.com/badges/99ddc943-1d93-48bc-8511-415eb236ccd4", "ASBG @ HYU", "AWS Builders · Core Team", "2026", A, None),
    ("sgr", "https://www.samsungsgr.com", "Samsung Global Research", "FDE & AX Advisor", "2026", A, None),
    ("ey", "https://www.ey.com/ko_kr", "Hanyang × EY Han Young", "Undergraduate Researcher", "2026", A, None),
    ("mois", "https://www.mois.go.kr", "Korea MOIS", "Youth Public AX Supporter", "2026", A, None),
]

STATUS = {  # chip colour, chip text
    A: ("#2F7BD6", "IN PROGRESS"),
    C: ("#2DA44E", "✓ CLEARED"),
    G: ("#C9971C", None),
}

W, H = 200, 262


def pixel_rect(x, y, w, h, s):
    """Rectangle with stepped (pixel-art) corners, step size s."""
    return (f"M{x+2*s},{y} H{x+w-2*s} V{y+s} H{x+w-s} V{y+2*s} H{x+w} V{y+h-2*s} H{x+w-s} V{y+h-s} "
            f"H{x+w-2*s} V{y+h} H{x+2*s} V{y+h-s} H{x+s} V{y+h-2*s} H{x} V{y+2*s} H{x+s} V{y+s} H{x+2*s} Z")


def card(i, slug, name, role, year, status, prize):
    color, chip = STATUS[status]
    if status == G:
        chip = f"★ {prize}"
    png = base64.b64encode((HERE / f"{slug}.png").read_bytes()).decode()
    mono = "font-family=\"'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace\" font-weight=\"700\""
    sans = "font-family=\"-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif\""
    fit = ' textLength="180" lengthAdjust="spacingAndGlyphs"' if len(name) > 21 else ""
    chip_w = 22 + 7.4 * len(chip)
    edge = color if status == G else None
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <style>
    .panel {{ fill: #F6F8FA; stroke: {edge or "#D0D7DE"}; }}
    .fg {{ fill: #1F2328; }}
    .muted {{ fill: #59636E; }}
    @media (prefers-color-scheme: dark) {{
      .panel {{ fill: #161B22; stroke: {edge or "#3D444D"}; }}
      .fg {{ fill: #F0F6FC; }}
      .muted {{ fill: #9198A1; }}
    }}
  </style>
  <path class="panel" stroke-width="2" d="{pixel_rect(2, 2, W-4, H-4, 4)}"/>
  <text class="muted" x="16" y="25" {mono} font-size="11.5" letter-spacing="1">No.{i:02d}</text>
  <text class="muted" x="{W-16}" y="25" {mono} font-size="11.5" letter-spacing="1" text-anchor="end">{year}</text>
  <image x="36" y="36" width="128" height="128" xlink:href="data:image/png;base64,{png}" href="data:image/png;base64,{png}"/>
  <text class="fg" x="{W/2}" y="190" {sans} font-size="14.5" font-weight="700" text-anchor="middle"{fit}>{escape(name)}</text>
  <text class="muted" x="{W/2}" y="209" {sans} font-size="11.5" text-anchor="middle">{escape(role)}</text>
  <path fill="{color}" d="{pixel_rect(W/2 - chip_w/2, 224, chip_w, 22, 2)}"/>
  <text x="{W/2}" y="239" {mono} font-size="10.5" letter-spacing="0.8" fill="#FFFFFF" text-anchor="middle">{escape(chip)}</text>
</svg>
'''


def main():
    CARDS.mkdir(exist_ok=True)
    rows, row = [], []
    for i, (slug, link, name, role, year, status, prize) in enumerate(BADGES, 1):
        fname = f"{i:02d}-{slug}.svg"
        (CARDS / fname).write_text(card(i, slug, name, role, year, status, prize))
        row.append(f'<a href="{link}"><img src="{RAW}{fname}" width="180" alt="No.{i:02d} {escape(name)} — {escape(role)}" /></a>')
        if len(row) == 4:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    n = {s: sum(1 for b in BADGES if b[5] == s) for s in (A, C, G)}
    print(f"""<!-- ══════════════════════════════════════════════════════ -->
<!-- GYM CHALLENGE                                           -->
<!-- ══════════════════════════════════════════════════════ -->

## 🏅 Gym Challenge

<div align="center">

<sub><i>Every gym I've walked into so far, numbered in the order I showed up.</i></sub>

![Badges](https://img.shields.io/badge/Badges-{len(BADGES)}-002856?style=for-the-badge)
![In Progress](https://img.shields.io/badge/In_Progress-{n[A]}-2F7BD6?style=for-the-badge)
![Cleared](https://img.shields.io/badge/Cleared-{n[C]}-2DA44E?style=for-the-badge)
![Trophies](https://img.shields.io/badge/Trophies-{n[G]}-C9971C?style=for-the-badge)

</div>
""")
    for r in rows:
        print('<p align="center">\n  ' + "\n  ".join(r) + "\n</p>\n")


if __name__ == "__main__":
    main()
