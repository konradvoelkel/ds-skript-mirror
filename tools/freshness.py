#!/usr/bin/env python3
"""Jede Seite und jeden Sitemap-Eintrag mit dem Datum ihrer letzten Änderung versehen.

    python3 tools/freshness.py <html-verzeichnis> [--check]

Nach dem Bau auf `public/` laufen zu lassen, vor `inject_jsonld.py`.

Warum überhaupt
---------------
Dieses Buch wird laufend gepflegt, aber **keine einzige Seite sagte das** (gemessen am
Live-Stand 2026-10-16: kein Datum im `<head>`, keins im Text, `<lastmod>` in null von 32
Sitemap-Einträgen). Für AI-Antwortsysteme ist Aktualität eines der stärksten
Auswahlsignale — wir haben sie und haben sie verschenkt.

Woher das Datum kommt
---------------------
Aus `git log` der *Quelldatei*, nicht aus der Bauzeit. Ein Bau am Dienstag macht ein
Kapitel von 2024 nicht frisch; ein Datum, das das behauptet, wäre schlechter als gar
keins. Deshalb gibt es hier auch **keine Rückfallebene auf die Uhr**: liefert git für
eine Datei nichts, bricht das Skript ab, statt etwas Plausibles zu erfinden.

Das heißt, der Job braucht eine **vollständige Historie**. GitLab klont standardmäßig
flach (`GIT_DEPTH: 20`); eine Datei, die seit zwanzig Commits unberührt ist, hat dann
keinen Eintrag. `variables: GIT_DEPTH: "0"` im Job ist deshalb Pflicht, und die
Fehlermeldung unten sagt das auch.

Nicht enthalten: ein *sichtbares* Datum auf der Seite. Das Theme rendert den Seitenkopf
aus einem eingebetteten JSON-Block neu, eine ins Markup geschriebene Zeile wäre nach der
Hydration wieder weg. Der saubere Weg dafür ist `date:` im Frontmatter — eine
Quelltextänderung, und die wartet auf Zuruf.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = '<meta property="article:modified_time" content="{date}"/>'


def toc_files(toc) -> list[str]:
    """Alle Dateien der Inhaltsübersicht, in Lesereihenfolge."""
    out: list[str] = []
    for entry in toc:
        if "file" in entry:
            out.append(entry["file"])
        for child in entry.get("children", []):
            out.extend(toc_files([child]))
    return out


def project(html: Path) -> dict:
    """Der Projektblock aus der gebauten config.json.

    Bewusst nicht aus myst.yml: der `pages`-Job läuft auf python:3.13-alpine ohne
    PyYAML, und config.json enthält dieselben Angaben als reines JSON.
    """
    cfg = json.loads((html / "config.json").read_text(encoding="utf-8"))
    return cfg["projects"][0]


def git_date(name: str) -> str:
    """ISO-8601-Datum des letzten Commits, der diese Datei angefasst hat."""
    try:
        res = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", name],
            cwd=ROOT, capture_output=True, text=True,
        )
    except FileNotFoundError:
        raise SystemExit(
            "✗ git ist nicht installiert.\n"
            "  Im CI heisst das: python:3.13-alpine bringt keins mit.\n"
            '  Der Job braucht "apk add --no-cache git" vor diesem Schritt.'
        )
    if res.returncode != 0:
        # Ein Fehler von git ist etwas anderes als "git kennt diese Datei nicht", und die
        # beiden zu verwechseln kostete beim Bauen eine halbe Stunde Fehlersuche: bei einem
        # Rechteproblem meldete das Skript "flacher Klon" und schickte in die falsche Richtung.
        raise SystemExit(f"✗ git scheiterte fuer {name}:\n  {res.stderr.strip()}")
    date = res.stdout.strip()
    if not date:
        raise SystemExit(
            f"✗ git kennt kein Datum für {name}.\n"
            f"  Bei einem flachen Klon ist das der Normalfall. Der Job braucht\n"
            f"  variables:\n    GIT_DEPTH: \"0\"\n"
            f"  Erfunden wird hier nichts."
        )
    return date


def pages(html: Path) -> list[tuple[str, Path, str]]:
    """(slug, index.html, datum) je Seite. Der erste toc-Eintrag ist die Startseite."""
    out = []
    for n, name in enumerate(toc_files(project(html)["toc"])):
        slug = "" if n == 0 else Path(name).stem
        target = html / "index.html" if n == 0 else html / slug / "index.html"
        if not target.exists():
            raise SystemExit(f"✗ {target} fehlt; toc und Bau sind sich uneinig")
        out.append((slug, target, git_date(name)))
    return out


def book_date(html: Path) -> str:
    """Das jüngste Seitendatum — das Datum des Werks als Ganzes."""
    return max(date for _, _, date in pages(html))


def stamp_html(entries) -> int:
    done = 0
    for _, target, date in entries:
        page = target.read_text(encoding="utf-8")
        if "article:modified_time" in page:
            continue
        target.write_text(page.replace("</head>", META.format(date=date) + "</head>", 1),
                          encoding="utf-8")
        done += 1
    return done


def stamp_sitemap(html: Path, entries) -> int:
    """<lastmod> in jeden <url>-Block schreiben, zugeordnet über den letzten Pfadteil.

    Über den Pfad und nicht über die volle URL, damit der Schritt unabhängig davon ist,
    ob die Origin-Ersetzung im Job vorher oder nachher läuft.
    """
    path = html / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    if "<lastmod>" in xml:
        return 0
    by_slug = {slug: date for slug, _, date in entries}
    hits = 0

    def add(match: re.Match) -> str:
        nonlocal hits
        block, loc = match.group(0), match.group(1)
        slug = loc.rstrip("/").rsplit("/", 1)[-1]
        date = by_slug.get(slug if slug in by_slug else "")
        if date is None:
            return block
        hits += 1
        return block.replace("</loc>", f"</loc><lastmod>{date}</lastmod>", 1)

    path.write_text(re.sub(r"<url>\s*<loc>([^<]+)</loc>", add, xml), encoding="utf-8")
    return hits


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    html = Path(args[0])
    entries = pages(html)

    if "--check" in sys.argv:
        pages_without = [str(t) for _, t, _ in entries
                         if "article:modified_time" not in t.read_text(encoding="utf-8")]
        stamps = (html / "sitemap.xml").read_text(encoding="utf-8").count("<lastmod>")
        if pages_without or stamps != len(entries):
            print(f"✗ {len(pages_without)} Seiten ohne Datum, "
                  f"{stamps} von {len(entries)} Sitemap-Einträgen mit <lastmod>")
            for p in pages_without[:5]:
                print(f"    {p}")
            return 1
        print(f"✓ {len(entries)} Seiten mit Datum, {stamps} Sitemap-Einträge mit <lastmod>")
        return 0

    n_html, n_map = stamp_html(entries), stamp_sitemap(html, entries)
    print(f"✓ {n_html} Seiten datiert, {n_map} Sitemap-Einträge mit <lastmod>; "
          f"jüngste Änderung {book_date(html)[:10]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
