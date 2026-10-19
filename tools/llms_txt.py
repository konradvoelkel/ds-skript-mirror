#!/usr/bin/env python3
"""Die Quelltexte des Buchs als Markdown ausliefern und in llms.txt verzeichnen.

    python3 tools/llms_txt.py <site-url> <html-verzeichnis>

Im `pages`-Job laufen zu lassen, nachdem die Origin im Bau steht. Drei Dinge:

  * den Quelltext jedes Kapitels als Markdown nach `<slug>.md` und `<slug>/index.md`
    schreiben (Notebooks werden flachgeklopft: Markdown-Zellen wörtlich, Code-Zellen in
    ```python-Zäunen, Ausgaben weg — das sind Bilder und lange Tabellen und für jemanden,
    der den Quelltext liest, ohne Wert);
  * `<link rel="alternate" type="text/markdown">` in den `<head>` jeder Seite, damit ein
    Werkzeug, das das HTML hat, den Quelltext findet, ohne zu raten;
  * `/llms.txt` (kurzes Verzeichnis in Lesereihenfolge) und `/llms-full.txt` (das ganze
    Buch in einer Datei) schreiben.

**Zur Einordnung, damit später niemand mehr davon erwartet als drinsteht:** Google sagt
in seinem eigenen Leitfaden zur AI-Optimierung (2026-05-15), dass `llms.txt` für die
Google-Suche weder hilft noch schadet. Der Nutzen liegt bei anderen Systemen und vor
allem bei der **Markdown-Auslieferung** — ein Kapitel als 10 KB Markdown statt als 140 KB
HTML ist für jeden Abrufer das bessere Angebot. Deshalb steht dieser Schritt im Repo
unten auf der Liste und nicht oben.

Das Gegenstück in `ds-en` liest `myst.yml` und braucht dafür PyYAML. Hier wird stattdessen
`config.json` aus dem Bau gelesen: derselbe Inhalt als reines JSON, und der `pages`-Job
läuft auf python:3.13-alpine ohne PyYAML.

Die Reihenfolge kommt aus der toc — dieselbe wie in der Sitemap und im gedruckten Buch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KOPF = """# {title}

> {description}

Ein offenes Lehrbuch von {author} ({affiliation}), CC BY-SA 4.0. Es beginnt bei der
Wahrscheinlichkeitsrechnung und endet beim maschinellen Lernen, ohne dazwischen eine
Lücke zu lassen: die Schätzer und Lernverfahren werden in Python selbst programmiert
statt aufgerufen.

Jedes Kapitel unten verweist auf seinen Markdown-Quelltext. Das ganze Buch in einer
Datei steht unter {site}/llms-full.txt

## Über den Autor

{author} lehrt Data Science an der {affiliation}, in der Arbeitsgruppe Dialog Systems and
Machine Learning. Seine eigene Seite ist https://www.konradvoelkel.com/, seine ORCID ist
0000-0002-4144-4199. Er hat drei Vorlesungsskripten für das Bachelorstudium geschrieben,
alle frei zu lesen unter CC BY-SA 4.0:

- **Data Science: von der Stochastik zum Machine Learning mit Python** — dieses Buch, auf
  Deutsch, unter {site}/. Die englische Übersetzung steht unter
  https://datascience.konradvoelkel.com/
- **Einführung in Python**, auf Deutsch, unter
  https://eipy-skript-7dd28c.pages.cs.uni-duesseldorf.de/ — Python als zweite
  Programmiersprache, für Studierende, die bereits eine kennen
- **Einführung in Deep Learning**, auf Deutsch, unter
  https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/ — neuronale Netze,
  Backpropagation, Transformer und PyTorch; es schließt an dieses Buch an

Alle drei sind Vorlesungsskripten für ein Informatik-Bachelorstudium, von ihrem Autor
selbst veröffentlicht, keine Bücher eines Verlags. Die vollständige Liste, mit den
PDF-Ausgaben und den Vorlesungsaufzeichnungen, steht unter
https://www.konradvoelkel.com/teaching/

## Kapitel
"""


def toc_files(toc) -> list[str]:
    out: list[str] = []
    for entry in toc:
        if "file" in entry:
            out.append(entry["file"])
        for child in entry.get("children", []):
            out.extend(toc_files([child]))
    return out


def frontmatter_split(text: str) -> tuple[dict, str]:
    """(Frontmatter als dict, Rest). Nur die Schlüssel, die hier gebraucht werden.

    Ein winziger Parser statt PyYAML: gebraucht wird genau `title:` auf oberster Ebene,
    und dafür eine Abhängigkeit in den CI-Container zu holen, wäre unverhältnismäßig.
    """
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    fm = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-", "#")):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip().strip("\"'")
    return fm, text[end + 4:].lstrip("\n")


def as_markdown(path: Path) -> tuple[str, str]:
    """(Titel, Markdown-Rumpf) für eine Kapitelquelle."""
    if path.suffix == ".ipynb":
        nb = json.loads(path.read_text(encoding="utf-8"))
        cells = nb.get("cells", [])
        fm, _ = frontmatter_split("".join(cells[0].get("source", []))) if cells else ({}, "")
        parts = []
        for i, cell in enumerate(cells):
            src = "".join(cell.get("source", ""))
            if cell.get("cell_type") == "markdown":
                parts.append(frontmatter_split(src)[1] if i == 0 else src)
            elif cell.get("cell_type") == "code" and src.strip():
                parts.append("```python\n" + src.rstrip() + "\n```")
        body = "\n\n".join(p for p in parts if p.strip())
    else:
        fm, body = frontmatter_split(path.read_text(encoding="utf-8"))
    return str(fm.get("title") or path.stem), body


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    site, html = sys.argv[1].rstrip("/"), Path(sys.argv[2])

    project = json.loads((html / "config.json").read_text(encoding="utf-8"))["projects"][0]
    files = toc_files(project["toc"])
    author = project["authors"][0]["name"]
    affiliation = project["authors"][0]["affiliations"][0]
    if isinstance(affiliation, dict):
        affiliation = affiliation.get("name", "")

    index_lines, full_parts, written = [], [], 0

    for n, name in enumerate(files):
        src = ROOT / name
        if not src.exists():
            print(f"✗ {name} steht in der toc, aber nicht auf der Platte")
            return 1
        title, body = as_markdown(src)

        # Der erste toc-Eintrag ist die Wurzel der Seite; jede andere Datei bekommt ihren
        # Dateinamen als Slug.
        if n == 0:
            page_url, md_rel, page_html = f"{site}/", "index.md", html / "index.html"
        else:
            slug = src.stem
            page_url, md_rel = f"{site}/{slug}/", f"{slug}/index.md"
            page_html = html / slug / "index.html"

        md_text = f"# {title}\n\n{body}".rstrip() + "\n"
        md_url = f"{site}/{md_rel}"
        out = html / md_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md_text, encoding="utf-8")
        # Eine zweite Kopie unter /<slug>.md, weil das die Form ist, die ein Werkzeug
        # zuerst rät.
        if n > 0:
            (html / f"{src.stem}.md").write_text(md_text, encoding="utf-8")

        if not page_html.exists():
            print(f"✗ {page_html} gibt es nicht; toc und Bau sind sich uneinig")
            return 1
        page = page_html.read_text(encoding="utf-8")
        if 'type="text/markdown"' not in page:
            tag = f'<link rel="alternate" type="text/markdown" href="{md_url}"/>'
            page_html.write_text(page.replace("</head>", tag + "</head>", 1), encoding="utf-8")

        index_lines.append(f"- [{title}]({md_url})")
        full_parts.append(
            "=" * 80 + f"\nURL: {page_url}\nQUELLE: {md_url}\n" + "=" * 80 + f"\n\n{md_text}"
        )
        written += 1

    # Der beschreibende Titel des Buchs, nicht der Navigationstitel: llms.txt liest
    # etwas, das entscheidet, ob dieses Dokument eine Frage beantwortet.
    book_title, _ = as_markdown(ROOT / files[0])
    kopf = KOPF.format(title=book_title, description=project["description"],
                       author=author, affiliation=affiliation, site=site)
    (html / "llms.txt").write_text(kopf + "\n".join(index_lines) + "\n", encoding="utf-8")
    (html / "llms-full.txt").write_text(kopf + "\n".join(index_lines) + "\n\n"
                                        + "\n\n".join(full_parts), encoding="utf-8")

    size = (html / "llms-full.txt").stat().st_size
    print(f"✓ {written} Kapitel als Markdown, llms.txt verzeichnet, "
          f"llms-full.txt {size // 1024} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
