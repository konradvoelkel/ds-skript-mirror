#!/usr/bin/env python3
"""Was in der Hydrations-Nutzlast des Themes steht, richtigstellen.

    python3 tools/hydration.py <site-url> <html-verzeichnis> [--base BASE_URL]
    python3 tools/hydration.py --check <html-verzeichnis> [--base BASE_URL]

Im `pages`-Job nach dem Bau laufen zu lassen, vor `precompress.py` wie jeder Schritt,
der HTML ändert.

Warum es dieses Skript gibt
---------------------------

Der `<head>` gehört zum React-Baum. Remix rendert ihn bei der Hydration aus `<Meta/>`
und `<Links/>` der Route-Module neu und ersetzt dabei die Kopf-Kinder durch seinen
eigenen Satz. Alles, was wir nach dem Bau ins Markup geschrieben haben, ist in diesem
Satz nicht enthalten und ist nach dem ersten Frame weg. Am 2026-10-20 im Browser
gemessen, am **2026-10-29 in der Google Search Console** an der gerenderten Fassung
bestätigt (URL-Prüfung, „Gecrawlte Seite → HTML"): weg sind `rel=canonical`, `og:url`,
`og:site_name`, `og:type`, `og:locale`(`:alternate`), `twitter:card`, alle drei
`hreflang`-Links, `article:modified_time` und der Markdown-`alternate`; `og:image` steht
wieder relativ da. Zwei Dinge bleiben: das `ld+json`-Script (ein `<script>` verwaltet
React hier nicht) und `lang="de"` (eigener MutationObserver in `head_meta.py`).

Das heißt: alles ohne JavaScript — Slack, LinkedIn, Mastodon, einfache Crawler, `curl` —
sieht das, was wir geschrieben haben. Alles, was rendert, und Google rendert vor dem
Indexieren, sieht die Fassung ohne Canonical und ohne Sprachpaar. Begründung, Tabellen
und die Messungen: `todo/seo-landingpage-2026-10-16.md` §16.

Dieses Skript ist der erste Schritt dieser Reparatur, und er ist klein: **die Nutzlast
in Ordnung bringen, bevor irgendetwas aus ihr gebaut wird.**


`page.domain`
-------------

In der Nutzlast steht `page.domain`, und MyST füllt es beim statischen Bau mit der
Origin seines eigenen Dev-Servers: `http://localhost:3000`, genau ein Vorkommen je
Dokument (am 2026-10-29 im ausgelieferten Dokument nachgemessen, und einmal in jeder der
32 Seiten). Es ist **heute wirkungslos** — kein Route-Modul liest es: im Bundle sind alle
212 `.domain`-Treffer d3-Skalen der Diagramme, Plotly-Achsen und gettext-Domänen, und in
den beiden Chunks, die den Kopf rendern, kommt `domain` überhaupt nicht vor.

Es ist aber dieselbe Klasse wie die localhost-Sitemap vom 2026-10-14, und sobald
irgendetwas Tags aus der Nutzlast baut, ist es die Quelle, aus der falsche URLs
entstehen. Also richtigstellen, bevor wir die Nutzlast anfassen, nicht danach.

Gesetzt wird die **Origin ohne Basispfad**, nicht `$SITE`. Das Feld heißt „domain", MyST
füllt es mit Schema und Host, und die einzige Verwendung, die das Theme für so einen
Wert überhaupt kennt, ist `${origin}${location.pathname}` in seinem Meta-Erzeuger — und
`location.pathname` trägt den Basispfad schon. Dass diese Seite unter einem Unterpfad
liegt, kann `domain` nicht ausdrücken; das ist die Grenze des Feldes, nicht unsere.

**Dasselbe Feld steht ein zweites Mal daneben**, in MySTs Seiten-JSON (`<slug>.json`,
eins je Kapitel, von dem das HTML eine Kopie als Nutzlast trägt). Beim Suchen nach dem
einen Vorkommen im Dokument fällt das nicht auf; `grep -rl localhost public` findet es
sofort. Es wird hier mitgesetzt, denn sonst liegt dieselbe falsche Angabe weiter
ausgeliefert daneben, und der Wächter unten wäre grün, weil er nur HTML ansieht — genau
die Art Lücke, aus der die localhost-Sitemap entstanden ist.


Die Falle, und warum hier nach jedem Schreiben geprüft wird
-----------------------------------------------------------

`json.JSONDecoder().raw_decode` liefert den **absoluten Index** des JSON-Endes im
Dokument, nicht die Anzahl verbrauchter Zeichen. Wer ihn als Länge liest und
`doc[start + end:]` schneidet, schneidet um `start` zu weit — hinter das Dokumentende,
und der Rest wird stillschweigend `""`. Genau das ist in ds-en ausgeliefert worden: jede
Seite endete mitten in der Nutzlast, 85 kB zu kurz, ohne `</script>`, `</body>`,
`</html>` und ohne das Modul-Script, das den Client startet. Browser bügeln offene Tags
glatt, es sah also nichts falsch aus — gefehlt hat die ganze Client-Laufzeit, fünfzehn
Stunden lang unbemerkt.

Deshalb steht hier nach jedem Schreiben die Frage „endet das Dokument noch auf `</html>`
und ist die Nutzlast wieder gültiges JSON", und `--check` stellt sie noch einmal über
alles. Das ist eine Nachbedingung, die etwas beweisen *kann*, im Unterschied zu der
Frage, ob ein Tag im gebauten Artefakt steht: die ist bei diesem Theme grün, egal was
der Browser danach daraus macht.


Zweimal laufen
--------------

Idempotent: gesetzt wird nur, was noch nicht gesetzt ist, und ein zweiter Lauf schreibt
keine Datei neu. Er prüft trotzdem alles.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys


def read_payload(doc: str):
    """Die Hydrations-Nutzlast mit Anfang und Ende. None, wenn die Seite keine hat.

    `raw_decode` gibt den **absoluten Index** des JSON-Endes im Dokument zurück, nicht
    die Länge. Wer ihn als Länge liest, schneidet um `start` zu weit und verliert den
    ganzen Rest des Dokuments -- die Falle, die in ds-en fünfzehn Stunden lang jede Seite
    mitten in der Nutzlast abgeschnitten hat, siehe Docstring.
    """
    key = "window.__remixContext = "
    i = doc.find(key)
    if i < 0:
        return None
    start = i + len(key)
    try:
        payload, end = json.JSONDecoder().raw_decode(doc, start)
    except ValueError:
        return None
    return payload, start, end


def routes(payload: dict):
    """Die loaderData-Routen -- dort liegt jeder Wert, den dieses Skript anfasst.

    Über alle Routen, nicht über einen Namen: die Landingpage lag am 2026-10-19 unter
    `routes/_index` und liegt mit gesetztem BASE_URL unter `routes/$`, und das ist nichts,
    woran ein Skript hängen sollte.
    """
    for route in (payload.get("state", {}).get("loaderData") or {}).values():
        if isinstance(route, dict):
            yield route


def edit_payload(doc: str, mutate) -> tuple[str, bool]:
    """Die Nutzlast an `mutate` geben und zurückschreiben, wenn sie sich geändert hat."""
    found = read_payload(doc)
    if found is None:
        return doc, False
    payload, start, end = found
    if not mutate(payload):
        return doc, False
    # Kompakt neu serialisiert. Die drei Ersetzungen halten das JSON als
    # JavaScript-Literal *innerhalb eines <script>* gültig: ein nacktes "<" könnte das
    # Tag früh schließen, und U+2028/U+2029 sind in JSON gewöhnliche Zeichen, in
    # JavaScript aber Zeilenenden. Als \u-Folgen liest JSON dieselben Zeichen zurück.
    out = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    out = out.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace(
        "\u2029", "\\u2029"
    )
    return doc[:start] + out + doc[end:], True


def set_domain(doc: str, origin: str) -> tuple[str, bool]:
    """`page.domain` von der Dev-Server-Origin auf die echte setzen."""

    def mutate(payload: dict) -> bool:
        changed = False
        for route in routes(payload):
            page = route.get("page")
            if isinstance(page, dict) and page.get("domain") != origin:
                page["domain"] = origin
                changed = True
        return changed

    return edit_payload(doc, mutate)


def whole(doc: str, f: pathlib.Path) -> None:
    """Die Nachbedingung, die der ds-en-Unfall gekostet hat: ist das Dokument ganz?

    Nicht „hat sich etwas geändert", sondern „ist das Dokument noch vollständig und die
    Nutzlast noch lesbar". Ein um `start` zu weit gesetzter Schnitt fällt genau hier auf
    und nirgends sonst.
    """
    if not doc.rstrip().endswith("</html>"):
        sys.exit(f"FEHLER: {f} endet nicht auf </html> -- der Schnitt war zu weit")
    if "window.__remixContext" in doc and read_payload(doc) is None:
        sys.exit(f"FEHLER: {f} hat keine lesbare Hydrations-Nutzlast mehr")


def set_json_domain(f: pathlib.Path, origin: str) -> bool:
    """Dasselbe Feld in MySTs Seiten-JSON. Siehe Docstring.

    Nur ein `domain` auf oberster Ebene wird angefasst. `config.json`,
    `myst.search.json` und `myst.xref.json` haben keins und bleiben unberührt.
    """
    data = json.loads(f.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("domain") in (None, origin):
        return False
    data["domain"] = origin
    f.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    return True


def check(root: pathlib.Path) -> int:
    """Noch einmal über alles, nach dem Lauf."""
    pages = sorted(root.rglob("index.html"))
    if not pages:
        sys.exit(f"FEHLER: keine Seite unter {root}")
    # Gesucht wird "localhost:3000", nicht "localhost", und nur in HTML und JSON.
    # Ein Wächter auf das Wort allein wäre der Tag falsch, an dem ein Kapitel erklärt,
    # wie man ein Notebook unter http://localhost:8888 öffnet -- und dann bricht der
    # Deploy an einem Satz im Buch. Die Zeichenkette mit dem Port ist MySTs Dev-Server
    # und sonst nichts; die Angabe selbst wird unten am Feld geprüft, nicht am Text.
    rest = [f for f in sorted(root.rglob("*.json")) if f.is_file()]
    for f in rest:
        if "localhost:3000" in f.read_text(encoding="utf-8", errors="replace"):
            sys.exit(f"FEHLER: {f} nennt weiterhin localhost:3000")
    n = 0
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        whole(doc, f)
        if "localhost:3000" in doc:
            sys.exit(f"FEHLER: {f} nennt weiterhin localhost:3000")
        found = read_payload(doc)
        if not found:
            sys.exit(f"FEHLER: {f} hat keine Hydrations-Nutzlast")
        for route in routes(found[0]):
            page = route.get("page")
            if not isinstance(page, dict) or "domain" not in page:
                continue
            dom = page["domain"]
            if not dom.startswith("https://") or "/" in dom[8:]:
                sys.exit(
                    f"FEHLER: {f}: page.domain ist {dom!r} -- erwartet wird eine"
                    f" Origin mit Schema und ohne Pfad"
                )
            n += 1
    print(
        f"✓ {len(pages)} Seiten: Nutzlast lesbar, {n} mal page.domain als Origin; "
        f"kein localhost:3000 mehr, weder im HTML noch in {len(rest)} Seiten-JSON"
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("site", nargs="?", help="Site-URL mit Basispfad, also $SITE")
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    ap.add_argument("--check", action="store_true", help="nur nachmessen, nichts ändern")
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    base = args.base.rstrip("/")

    if args.check:
        return check(root)

    if not args.site:
        sys.exit("FEHLER: ohne --check ist die Site-URL nötig")
    site = args.site.rstrip("/")
    if base and not site.endswith(base):
        sys.exit(f"FEHLER: {site} endet nicht auf {base} -- dann wäre die Origin geraten")
    origin = site[: len(site) - len(base)] if base else site

    pages = sorted(root.rglob("index.html"))
    if not pages:
        sys.exit(f"FEHLER: keine Seite unter {root}")

    n_dom = 0
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        doc, geaendert = set_domain(doc, origin)
        if not geaendert:
            continue
        whole(doc, f)
        f.write_text(doc, encoding="utf-8")
        n_dom += 1

    n_json = sum(set_json_domain(f, origin) for f in sorted(root.glob("*.json")))

    print(
        f"hydration: {len(pages)} Seiten, page.domain auf {origin} "
        f"({n_dom} Nutzlasten, {n_json} Seiten-JSON)"
    )
    return check(root)


if __name__ == "__main__":
    raise SystemExit(main())
