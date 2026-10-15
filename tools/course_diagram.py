#!/usr/bin/env python3
"""Erzeugt images/course-structure.svg, das Übersichtsdiagramm der Landingpage.

    python3 tools/course_diagram.py            # SVG schreiben
    python3 tools/course_diagram.py --check    # scheitern, wenn die Datei veraltet ist
                                               # oder von myst.yml abweicht

Warum kein Mermaid: MyST zeichnet einen ```{mermaid}``-Block erst im Browser. Im
statischen HTML steht nur `<figure class=""></figure>` -- ein Crawler, eine Leserin ohne
JavaScript und ein Screenreader bekommen nichts. Und die Direktive nimmt kein
`:caption:` (geprüft: „unexpected option"). Mit mermaid-cli vorzurendern hieße, für ein
Bild ein headless Chromium in den Bau zu ziehen. Die Struktur ist klein und regelmäßig
genug, um sie direkt zu zeichnen -- das bringt zusätzlich eine Bildunterschrift, einen
Alternativtext, die Markenfarbe des Buchs und ein Diagramm, das dem Hell-/Dunkelmodus
der Leserin folgt.

Deutsche Fassung des gleichnamigen Skripts aus `../ds-en` (gleiche Geometrie, gleiche
Marken-Hexwerte, andere Texte). Ein Unterschied ist Absicht: der Bandhintergrund ist hier
`#d8f5f5`, die in BRANDING.md abgeleitete helle Fläche, während ds-en ein selbst
gewähltes, helleres `#f2fbfb` benutzt. BRANDING.md sagt: Varianten werden abgeleitet,
nicht erfunden.

Der Inhalt ist derselbe wie im abgelösten Mermaid-Block und **muss mit den
Teil-Überschriften in myst.yml in Schritt bleiben** -- `--check` erzwingt das.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "course-structure.svg"

# (Teil-Überschrift, [Knoten, ...]); ein Knoten ist eine Liste von Zeilen.
# Die Teil-Überschriften müssen wörtlich den `title:`-Einträgen in myst.yml entsprechen.
PARTS: list[tuple[str, list[list[str]]]] = [
    ("Einführung", [["Was ist Data Science?"], ["Stochastik"], ["Python"]]),
    ("Diskrete Stochastik und Numpy",
     [["Zufallsvariablen, Verteilungen,", "Erwartungswert"], ["Numpy"],
      ["Diskrete Verteilungen,", "erste Exploration"]]),
    ("Stetige Stochastik und Scipy",
     [["Stetige Verteilungen,", "Normalverteilung, Scipy"]]),
    ("Explorative Datenanalyse",
     [["Deskriptive Statistik,", "Beispiele, Iris"], ["Pandas, Daten putzen"]]),
    ("Multivariate Stochastik",
     [["Kovarianz, multivariate", "Normalverteilung, relative Entropie"]]),
    ("Datenschutz", [["Datenschutz-Glossar"]]),
    ("Maschinelles Lernen",
     [["Clustering,", "Dimensionsreduktion"], ["Statistische Modelle,", "Regression, Kernel"],
      ["Tests, Modellwahl,", "Expectation Maximization"]]),
]

W = 920
PAD = 18           # Rand des Bandes
LABEL_H = 24       # Streifen für die Teil-Überschrift
LINE_H = 17
NODE_PAD_Y = 11
NODE_PAD_X = 16
GAP_X = 42         # zwischen Knoten, trägt den Pfeil
GAP_Y = 30         # zwischen Bändern, trägt den Pfeil
CHAR_W = 6.55      # mittlere Vorschubbreite bei 12,5px DejaVu/Inter; gemessen, nicht geraten


def text_w(lines: list[str]) -> float:
    return max(len(line) for line in lines) * CHAR_W


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build() -> str:
    bands, y = [], PAD
    for title, nodes in PARTS:
        widths = [text_w(n) + 2 * NODE_PAD_X for n in nodes]
        heights = [len(n) * LINE_H + 2 * NODE_PAD_Y for n in nodes]
        row_h = max(heights)
        band_h = LABEL_H + row_h + 2 * PAD
        total = sum(widths) + GAP_X * (len(nodes) - 1)
        x = (W - total) / 2
        placed = []
        for node, w, h in zip(nodes, widths, heights):
            placed.append((x, y + LABEL_H + PAD + (row_h - h) / 2, w, h, node))
            x += w + GAP_X
        bands.append((title, y, band_h, placed))
        y += band_h + GAP_Y
    height = y - GAP_Y + PAD

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:.0f}" '
        f'width="{W}" height="{height:.0f}" role="img" '
        f'aria-labelledby="ttl dsc">'
    )
    p.append('<title id="ttl">Wie die Teile der Vorlesung aufeinander aufbauen</title>')
    p.append(
        '<desc id="dsc">Sieben Teile nacheinander, jeder führt zum nächsten: '
        + "; ".join(f"{t} ({', '.join(' '.join(n) for n in ns)})" for t, ns in PARTS)
        + ".</desc>"
    )
    p.append("""<style>
  :root { color-scheme: light dark; }
  .band  { fill: #d8f5f5; stroke: #a9dede; }
  .node  { fill: #ffffff; stroke: #007d7e; stroke-width: 1.5; }
  .ptitle{ fill: #006364; font-weight: 600; }
  .ntext { fill: #1a1a1a; }
  .arrow { stroke: #007d7e; stroke-width: 2; fill: none; }
  .head  { fill: #007d7e; }
  text { font-family: Inter, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; }
  @media (prefers-color-scheme: dark) {
    .band  { fill: #16211f; stroke: #2a3d3c; }
    .node  { fill: #1b2225; stroke: #2cc5c5; }
    .ptitle{ fill: #6fdcdc; }
    .ntext { fill: #e9ecef; }
    .arrow { stroke: #2cc5c5; }
    .head  { fill: #2cc5c5; }
  }
</style>""")
    p.append('<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
             'markerHeight="7" orient="auto-start-reverse">'
             '<path class="head" d="M0,0 L10,5 L0,10 z"/></marker></defs>')

    for title, by, bh, placed in bands:
        p.append(f'<rect class="band" x="{PAD}" y="{by:.0f}" width="{W - 2 * PAD}" '
                 f'height="{bh:.0f}" rx="10"/>')
        p.append(f'<text class="ptitle" x="{PAD + 16}" y="{by + 19:.0f}" font-size="13.5">'
                 f'{esc(title)}</text>')
        for i, (nx, ny, nw, nh, lines) in enumerate(placed):
            p.append(f'<rect class="node" x="{nx:.1f}" y="{ny:.1f}" width="{nw:.1f}" '
                     f'height="{nh:.1f}" rx="7"/>')
            first = ny + NODE_PAD_Y + LINE_H - 5
            for k, line in enumerate(lines):
                p.append(f'<text class="ntext" x="{nx + nw / 2:.1f}" '
                         f'y="{first + k * LINE_H:.1f}" font-size="12.5" '
                         f'text-anchor="middle">{esc(line)}</text>')
            if i + 1 < len(placed):
                nx2 = placed[i + 1][0]
                cy = ny + nh / 2
                p.append(f'<path class="arrow" marker-end="url(#a)" '
                         f'd="M{nx + nw + 7:.1f},{cy:.1f} H{nx2 - 8:.1f}"/>')

    for (t1, y1, h1, _), (t2, y2, _, _) in zip(bands, bands[1:]):
        p.append(f'<path class="arrow" marker-end="url(#a)" '
                 f'd="M{W / 2:.0f},{y1 + h1 + 4:.0f} V{y2 - 5:.0f}"/>')

    p.append("</svg>")
    return "\n".join(p) + "\n"


def check_against_myst() -> int:
    """Die Teil-Überschriften hier gegen die in myst.yml halten.

    Dieselbe Driftfalle wie toc gegen articles: eine umbenannte oder neue Teil-Überschrift
    würde sonst stillschweigend ein Diagramm hinterlassen, das etwas anderes behauptet als
    das Inhaltsverzeichnis daneben.
    """
    try:
        import yaml
    except ImportError:
        print("✗ PyYAML fehlt; mit `uv run --with pyyaml python tools/course_diagram.py --check`")
        return 1
    cfg = yaml.safe_load((ROOT / "myst.yml").read_text(encoding="utf-8"))
    in_toc = [e["title"] for e in cfg["project"]["toc"] if "title" in e]
    here = [t for t, _ in PARTS]
    if in_toc != here:
        print("✗ Die Teil-Überschriften laufen auseinander.")
        print(f"  myst.yml:            {in_toc}")
        print(f"  course_diagram.py:   {here}")
        return 1
    print(f"✓ {len(here)} Teil-Überschriften stimmen mit myst.yml überein")
    return 0


def main() -> int:
    svg = build()
    if "--check" in sys.argv:
        rc = check_against_myst()
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != svg:
            print(f"✗ {OUT.relative_to(ROOT)} ist veraltet; tools/course_diagram.py ausführen")
            return 1
        print(f"✓ {OUT.relative_to(ROOT)} passt zu tools/course_diagram.py")
        return rc
    OUT.write_text(svg, encoding="utf-8")
    print(f"✓ {OUT.relative_to(ROOT)} geschrieben ({OUT.stat().st_size} Bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
