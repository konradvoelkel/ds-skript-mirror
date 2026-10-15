#!/usr/bin/env python3
"""Listet die Abbildungen auf, deren `alt`-Text nichts aussagt.

    uv run myst build --html          # vorher, das Skript liest das gebaute HTML
    python3 tools/alt_text_report.py  # Arbeitsliste nach Kapiteln

Warum es das gibt: Matplotlib-Ausgaben in Notebooks tragen im `.ipynb` eine
`text/plain`-Darstellung der Figure — wörtlich `<Figure size 640x480 with 1 Axes>`.
MyST nimmt genau die als `alt`. Das Attribut ist also **da**, aber es sagt nichts; eine
Prüfung auf „fehlt `alt`?" geht glatt durch, der Screenreader liest Unsinn vor, und für
die Bildersuche ist es wertlos. Wo das Buch `{figure}` mit `:alt:` benutzt, stimmt es
schon — die Lücke sind die Notebook-Ausgaben.

Das Skript **prüft nicht**, es berichtet: es läuft nicht in der CI und bricht nichts ab.
Ein harter Check wäre heute auf 150+ Stellen rot, und das wäre kein Signal, sondern
Lärm. Wenn die Lücke einmal geschlossen ist, kann man daraus einen Check machen.

Zwei Wege, eine Stelle zu reparieren, beide am Notebook:
  * `{figure}`-Direktive mit `:alt:` drumherum — so macht es das Buch an den Stellen,
    an denen es schon stimmt;
  * oder die Zelle so enden lassen, dass gar kein `text/plain` entsteht (`plt.show()`,
    abschließendes Semikolon). Dann steht kein irreführender Text da — aber eben auch
    keiner, der der Bildersuche hilft. Die erste Variante ist die richtige.
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "_build" / "html"

REPR_ALT = re.compile(r"^(&lt;|<)Figure size")
LATEX = re.compile(r"\\[a-zA-Z]+|\$")


def cell_hint(page: str) -> list[str]:
    """Je Bild die Zelle, die es erzeugt hat -- als Anhaltspunkt beim Schreiben.

    Eine Zelle kann mehrere Bilder ausgeben, deshalb wird je Bild ein Eintrag erzeugt und
    nicht je Zelle; sonst verrutscht die Zuordnung ab dem ersten Mehrfachplot.
    """
    p = ROOT / f"{page}.ipynb"
    if not p.exists():
        return []
    hints = []
    for n, cell in enumerate(json.loads(p.read_text())["cells"]):
        imgs = sum("image/png" in o.get("data", {}) for o in cell.get("outputs", []))
        if not imgs:
            continue
        src = [l.strip() for l in "".join(cell["source"]).splitlines() if l.strip()]
        head = src[0][:64] if src else ""
        for k in range(imgs):
            suffix = f"  [Bild {k + 1} von {imgs}]" if imgs > 1 else ""
            hints.append(f"Zelle {n}: {head}{suffix}")
    return hints


def main() -> int:
    if not HTML.exists():
        print("✗ _build/html fehlt -- erst `uv run myst build --html`")
        return 1
    per_page: dict[str, list[str]] = collections.defaultdict(list)
    latex_alts: list[tuple[str, str]] = []
    total = ok = 0
    for f in sorted(HTML.rglob("index.html")):
        page = f.parent.name if f.parent != HTML else "(Startseite)"
        for m in re.finditer(r"<img\b[^>]*>", f.read_text(errors="replace")):
            a = re.search(r'\balt="([^"]*)"', m.group(0))
            total += 1
            if not a or not a.group(1).strip():
                per_page[page].append("(kein alt)")
            elif REPR_ALT.match(a.group(1)):
                per_page[page].append(a.group(1))
            else:
                ok += 1
                if LATEX.search(a.group(1)):
                    latex_alts.append((page, a.group(1)[:90]))

    missing = sum(len(v) for v in per_page.values())
    print(f"{total} Bilder, {ok} mit aussagekräftigem alt, {missing} ohne.\n")
    for page in sorted(per_page, key=lambda p: -len(per_page[p])):
        hints = cell_hint(page)
        print(f"  {page}  ({len(per_page[page])})")
        for i, _ in enumerate(per_page[page]):
            hint = hints[i] if i < len(hints) else "(keine Zelle zugeordnet)"
            print(f"      {i + 1:2}. {hint}")
    if latex_alts:
        print("\nalt-Texte mit LaTeX darin (ein Screenreader liest die Quelle vor):")
        for page, alt in latex_alts:
            print(f"  {page}: {alt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
