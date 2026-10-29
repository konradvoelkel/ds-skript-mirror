#!/usr/bin/env python3
"""GitLab Pages die Kapitel auch ohne Schraegstrich mit 200 ausliefern lassen.

    python3 tools/pages_redirects.py <html-verzeichnis> --base BASE_URL
    python3 tools/pages_redirects.py --check <html-verzeichnis> --base BASE_URL

Im `pages`-Job hinter den Schritten, die Dateien anlegen: geprueft wird, dass jedes Ziel
wirklich auf der Platte liegt.

Warum es dieses Skript gibt
---------------------------

`/ds-skript/kmeans` beantwortet GitLab Pages mit **302** auf `/ds-skript/kmeans/`, weil
MyST je Kapitel ein Verzeichnis mit `index.html` schreibt. `trailing_slash.py` hat die
Links des Artefakts auf die Form mit Schraegstrich gebracht -- aber nur die, die aus der
Hydrations-Nutzlast kommen. Die Seitenleiste baut ihren href aus
`config.projects[].pages[].slug`, und ein Schraegstrich dort kostet gemessen die
Vorschaukarten aller Links im Artikel und die aufgeklappte Gruppe der aktuellen Seite
(TODO.md Zeile 1i). Nach der Hydration bleiben so 217 der 502 hrefs ohne Schraegstrich.

Die Zeile 1i schlug einen Patch am Theme vor. Dieses Skript nimmt den anderen Weg und
loest dasselbe Problem eine Schicht tiefer: nicht die Links richtigstellen, sondern die
falsche Form kostenlos machen. Ein `_redirects` mit Status 200 ist ein **Rewrite** --
GitLab liefert den Inhalt des Ziels aus, ohne die URL in der Adresszeile zu aendern und
ohne Round-Trip. Das wirkt auf jeden Link, auch auf die, die wir nicht erreichen, und auf
fremde Seiten, die die alte Form verlinken. Und es haengt an nichts, was mystmd beim
naechsten Update umbenennt; ein `sed` auf das minifizierte Buendel haette genau das getan.

Gemessen am 2026-10-29, fuenf Durchlaeufe auf derselben Verbindung: 0,254 s mit der
Weiterleitung, 0,214 s ohne. Rund 40 ms je Link.

Drei Dinge aus der Dokumentation, die hier den Unterschied machen
-----------------------------------------------------------------

1. **Der Projektpfad muss in jede Regel.** Beim Standard-Domain
   (`namespace.pages.example.com/projekt`) sind die Pfade *mit* Prefix zu schreiben, nur
   bei einer eigenen Domain ohne. Unsere URL ist genau diese Form, also lautet die Regel
   `/ds-skript/kmeans /ds-skript/kmeans/index.html 200` und nicht `/kmeans ...`.
2. **"Files on disk take priority over redirects."** Ob ein *Verzeichnis* als solche
   Datei zaehlt und die Weiterleitung schon vor den Regeln greift, sagt die
   Dokumentation nicht. Das ist die offene Frage dieses Schritts, und sie ist nur am
   deployten Stand zu beantworten. Das Risiko dabei ist null: greift die Regel nicht,
   bleibt es beim 302 wie bisher -- es wird nichts schlechter, nur nichts besser.
3. **`<pages-url>/_redirects` listet jede Regel als gueltig oder ungueltig.** Das ist die
   Abnahme dieses Schritts, zusammen mit einem `curl -I` auf die Form ohne
   Schraegstrich.

Warum 200 und nicht 301
-----------------------

301 waere cache-freundlicher als der heutige 302, kostet aber weiter einen Round-Trip.
200 kostet keinen. Dass ein Rewrite auf einen Pfad *ohne* Schraegstrich die relativen
URLs der Seite brechen wuerde, ist der Einwand gegen 200 -- hier gezaehlt und ausgeraeumt:
das Artefakt hat **null** relative `src`/`href`/`srcset`, alles ist wurzelrelativ oder
absolut.

Was dieses Skript nicht tut
---------------------------

Es macht die Links nicht richtig, es macht die falsche Form billig. Canonical, Sitemap,
`og:url` und hreflang nennen weiter die Form mit Schraegstrich, und das bleibt die
kanonische URL. Deshalb ersetzt es `trailing_slash.py` nicht: zwei URLs, die beide 200
liefern, wollen einen Canonical, der sagt, welche gemeint ist.

Keine Kommentarzeilen in der Datei. Netlifys Format kennt `#`, GitLabs Dokumentation sagt
dazu nichts, und eine Zeile, die der Parser als ungueltig verwirft, ist das Letzte, was
eine Konfigurationsdatei braucht, die stillschweigend wirkungslos sein kann. Die
Begruendung steht hier und im CI-Kommentar.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

DATEI = "_redirects"
# Vorgaben der Instanz, nachlesbar in der Dokumentation: 64 KB je Datei, 1000 Regeln je
# Projekt, und nur die ersten 1000 werden ueberhaupt gelesen. Wir schreiben 32.
MAX_REGELN = 1000
MAX_BYTES = 64 * 1024


def seiten_slugs(root: pathlib.Path) -> list[str]:
    """Die Slugs aller Kapitel, aus `config.json` des gebauten Ordners.

    Dieselbe Quelle wie in `head_meta.py`, `trailing_slash.py` und `inject_jsonld.py`.
    Die Reihenfolge der Konfiguration bleibt erhalten, damit die Datei stabil ist und ein
    Diff etwas aussagt.
    """
    cfg = root / "config.json"
    if not cfg.exists():
        sys.exit(f"FEHLER: {cfg} fehlt; ohne die Kapitelliste gibt es keine Regeln")
    try:
        pages = json.loads(cfg.read_text(encoding="utf-8"))["projects"][0]["pages"]
    except (ValueError, KeyError, IndexError, TypeError) as e:
        sys.exit(f"FEHLER: {cfg} hat kein projects[0].pages ({e})")
    slugs = [
        p["slug"] for p in pages if isinstance(p, dict) and isinstance(p.get("slug"), str)
    ]
    if not slugs:
        sys.exit(f"FEHLER: {cfg} nennt keinen einzigen Slug")
    if len(set(slugs)) != len(slugs):
        sys.exit(f"FEHLER: {cfg} nennt einen Slug zweimal -- zwei Regeln auf denselben Pfad")
    return slugs


def regeln(root: pathlib.Path, base: str) -> list[str]:
    """Je Kapitel eine Regel, dazu eine fuer die Startseite.

    Kein Splat (`/ds-skript/* ...`): der wuerde auch auf Pfade passen, die es nicht gibt,
    und eine Regel je Kapitel ist zugleich die Liste, gegen die `--check` prueft. Jedes
    Ziel wird auf der Platte nachgesehen -- eine Regel auf eine Datei, die der Bau nicht
    geschrieben hat, waere ein 404 statt eines 302, also schlechter als nichts.
    """
    aus = []
    for pfad, rel in [(base, pathlib.PurePath("."))] + [
        (f"{base}/{s}", pathlib.PurePath(s)) for s in seiten_slugs(root)
    ]:
        ziel = root / rel / "index.html"
        if not ziel.exists():
            sys.exit(f"FEHLER: {ziel} fehlt -- eine Regel darauf waere ein 404")
        zielpfad = f"{base}/index.html" if str(rel) == "." else f"{base}/{rel}/index.html"
        aus.append(f"{pfad} {zielpfad} 200")
    return aus


def inhalt(zeilen: list[str]) -> str:
    return "".join(z + "\n" for z in zeilen)


def pruefen(root: pathlib.Path, base: str) -> int:
    """Nachbedingung, aus dem Artefakt neu gerechnet statt dem Lauf geglaubt."""
    f = root / DATEI
    if not f.exists():
        sys.exit(f"FEHLER: {f} fehlt -- dann antwortet jeder Kapitelpfad ohne Schraegstrich weiter mit 302")
    ist = f.read_text(encoding="utf-8")
    soll = regeln(root, base)
    if ist != inhalt(soll):
        gefunden = [z for z in ist.split("\n") if z.strip()]
        fehlt = [z for z in soll if z not in gefunden]
        zuviel = [z for z in gefunden if z not in soll]
        sys.exit(
            f"FEHLER: {f} passt nicht zu config.json.\n"
            f"  {len(gefunden)} Regeln in der Datei, {len(soll)} erwartet\n"
            f"  fehlt:  {fehlt[:3]}\n"
            f"  zuviel: {zuviel[:3]}"
        )
    groesse = len(ist.encode("utf-8"))
    if len(soll) > MAX_REGELN:
        sys.exit(f"FEHLER: {len(soll)} Regeln, GitLab liest nur die ersten {MAX_REGELN}")
    if groesse > MAX_BYTES:
        sys.exit(f"FEHLER: {f} ist {groesse} Bytes, die Grenze liegt bei {MAX_BYTES}")
    print(
        f"pages_redirects --check: {len(soll)} Regeln, {groesse} Bytes, jedes Ziel vorhanden"
        f" (Grenzen {MAX_REGELN} Regeln / {MAX_BYTES} Bytes)"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    ap.add_argument(
        "--check",
        action="store_true",
        help="nichts schreiben, nur die Nachbedingung am gebauten Artefakt pruefen",
    )
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    base = args.base.rstrip("/")
    if not base:
        sys.exit(
            "FEHLER: ohne --base fehlt der Projektpfad. Beim Standard-Domain muss er in"
            " jede Regel, sonst passt keine -- siehe Docstring"
        )

    if args.check:
        return pruefen(root, base)

    zeilen = regeln(root, base)
    (root / DATEI).write_text(inhalt(zeilen), encoding="utf-8")
    pruefen(root, base)
    print(
        f"pages_redirects: {len(zeilen)} Rewrites nach {DATEI} geschrieben"
        f" ({len(zeilen) - 1} Kapitel und die Startseite), Status 200"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
