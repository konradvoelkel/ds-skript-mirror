#!/usr/bin/env python3
"""Die JSON-LD-Beschreibung des Buchs in die gebaute Landingpage schreiben.

    python3 tools/inject_jsonld.py <site-url> <html-verzeichnis>

Nach `freshness.py` laufen zu lassen, im `pages`-Job, nachdem die Origin im Bau steht.

MyST emittiert keine strukturierten Daten, und der Block kann nicht in `landing-page.md`
stehen: eine `{raw} html`-Direktive dort landete im PDF-Export. Also wird er dem gebauten
HTML hinzugefügt.

**Nur die Landingpage bekommt ihn.** Die Entität ist das Buch als Ganzes; derselbe Block
auf 32 Seiten behauptete 32 Bücher.

Nicht behauptet wird `Course` samt `hasCourseInstance` und `provider`. Das Skript *gehört*
zu einer Lehrveranstaltung der HHU, aber die Seite ist nicht deren Anmeldeseite — das
läuft über ILIAS. Schema.org-Angaben, die ein Suchsystem nicht nachprüfen kann und die
Nutzer ins Leere führen, bleiben weg. Die Angabe zur Zugehörigkeit des Autors stimmt und
bleibt deshalb drin.

Zwei Werte werden aus der Seite **zurückgelesen** statt fest eingetragen:

* die Vorschaukarte aus `og:image` — MyST hängt einen Hash an den Dateinamen, der sich
  bei jedem Neuerzeugen der Karte ändert;
* das Änderungsdatum aus `article:modified_time`, das `freshness.py` vorher gesetzt hat.
  Dasselbe Datum zweimal zu berechnen hieße, zwei Quellen der Wahrheit zu haben.

Dadurch hängt dieses Skript an der Reihenfolge im Job: erst `freshness.py`, dann dieses.
Fehlt eins von beidem, bricht es ab, statt die Angabe still wegzulassen.


Was das Buch ausmacht: Zielgruppe, Herausgeber, Kapitel
-------------------------------------------------------

Drei Angaben, die der SEO-Befund vom 2026-10-16 vorschlug (`todo/seo-landingpage-2026-10-16.md`,
Punkt 6), zwei davon fest in `structured-data.json`, eine erzeugt:

* `audience`: eine `EducationalAudience` mit `educationalRole: student`. Zusammen mit
  `educationalLevel: Bachelor`, das schon dastand, sagt das, *fuer wen* das Buch ist.
* `publisher`: eine Referenz auf `#author`, **nicht** auf die HHU. Der Befund schlug die
  Universitaet vor; das waere falsch. Das Buch ist selbst veroeffentlicht -- genau das sagt
  auch `llms.txt` ("von ihrem Autor selbst veroeffentlicht, keine Buecher eines Verlags") --,
  und ein `publisher: Heinrich-Heine-Universitaet` behauptete eine Herausgeberschaft, die
  niemand ausuebt: kein Lektorat, keine ISBN, keine Freigabe. Die Zugehoerigkeit des Autors
  steht bereits als `affiliation` da und ist die Angabe, die stimmt. Dieselbe Linie wie beim
  nicht behaupteten `Course`/`provider` oben.
* `hasPart`: die 31 Kapitel als `Chapter`-Knoten mit `position`, `name` und `url`.

`hasPart` wird **aus dem Bau gelesen, nicht gepflegt**: `config.json` im gebauten Ordner
fuehrt unter `projects[0].pages` die flache Leseliste, Teil-Ueberschriften (ohne `slug`) und
Kapitel (mit `slug`, `title`) in der Reihenfolge der `toc`. Ein neues Kapitel wandert damit
von selbst in die strukturierten Daten; eine hier gepflegte Liste waere spaetestens beim
dritten Umbenennen falsch. Dieselbe Quelle benutzt `llms_txt.py`.

Die `description` der Kapitel kommt **nicht** mit: sie steht auf jeder Kapitelseite schon als
`meta name="description"`, und die 31 Beschreibungen sind zusammen 5,1 kB -- sie wuerden den
Block von 12,8 auf rund 18 kB treiben, ohne eine Angabe hinzuzufuegen, die ein Crawler nicht
an ihrer eigenen URL findet. Die Kapitelliste selbst kostet 10,4 kB (2,4 kB vorher, 12,8
nachher, am 2026-10-20 am gebauten Artefakt gemessen); komprimiert geht davon ein Bruchteil
ueber die Leitung.
`position` kommt mit, weil die Reihenfolge eines Lehrbuchs eine Aussage ist: Kapitel 3 setzt
Kapitel 2 voraus.


Drei Werke, ein Autor
---------------------

Im Oktober 2026 nach der Zahl der Vorlesungsskripten von Konrad Völkel gefragt, antwortete
ChatGPT, es könne „keine verlässliche Gesamtzahl“ bestätigen, und nannte erst auf Nachfrage
die richtigen drei, mit einem Vorbehalt daneben. Es hatte genau eine Quelle für die
Behauptung: den Absatz über die Nachbarskripten auf dieser Landingpage, in Prosa, in einer
Ausgabe — und der verlangte vom Lesenden, eins zu zwei zu addieren. Die beiden anderen
Werke tragen bislang überhaupt keine strukturierten Daten, und nirgends stand die Menge.

Deshalb steht auf der Landingpage jetzt ein `@graph` statt des nackten Buchknotens, und die
beiden anderen Werke stehen darin: `tools/sibling-works.json`, jedes ein
`["Book","LearningResource"]`, dessen `author` dieselbe `{"@id": .../#author}`-Referenz ist
wie beim Buch. Mehr wird über sie nicht behauptet, als ihre eigene `myst.yml` ohnehin sagt —
Titel, Sprache, CC BY-SA, Vorlesungsskript für den Bachelor —, denn diese Seite ist nicht
ihr Herausgeber, und eine hier erfundene Beschreibung wäre genau die nicht nachprüfbare
Angabe, die oben begründet wegbleibt.

Ihre `@id`s sind `<ihre-url>/#work`, dasselbe Muster, das diese Seite für ihr eigenes Buch
benutzt. Wenn jene beiden Seiten eigene strukturierte Daten bekommen, prägen sie dieselbe
`@id`, und aus den zwei Hälften wird eine Entität statt zweier Beschreibungen einer URL.

Die englische Ausgabe *dieses* Buchs steht bewusst nicht in der Liste: sie ist dasselbe Werk
in einer anderen Sprache, und das sagt `workTranslation` am Buchknoten bereits richtig.

Eine `Person` hat in schema.org keine Eigenschaft „Werke“; deshalb wird von der Seite der
Werke her formuliert und nicht von der des Autors. Aus demselben Grund ist es keine
`ItemList`: eine Liste von dreien ist eine Aussage über den Inhalt einer Seite, drei Knoten
mit demselben `author` sind eine Aussage über die Welt — und gemeint ist die zweite.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "structured-data.json"
SIBLINGS = Path(__file__).resolve().parent / "sibling-works.json"


def chapter_nodes(site: str, html: Path) -> list[dict]:
    """Die Kapitel als `hasPart`, in der Reihenfolge der toc. Siehe oben, Abschnitt 2.

    Quelle ist `config.json` des *gebauten* Ordners, nicht `myst.yml`: der Bau hat die toc
    schon aufgeloest (Teile und Kapitel flach, mit Slug und Titel), und dieses Skript
    arbeitet ohnehin am Artefakt.
    """
    cfg = json.loads((html / "config.json").read_text(encoding="utf-8"))["projects"][0]
    index = cfg.get("index")
    nodes: list[dict] = []
    for page in cfg.get("pages", []):
        slug = page.get("slug")
        # Ohne Slug ist der Eintrag eine Teil-Ueberschrift ("Einfuehrung") und hat keine
        # eigene Seite; der Index ist die Landingpage und nicht Teil ihrer selbst.
        if not slug or slug == index:
            continue
        if not (html / slug / "index.html").exists():
            raise SystemExit(
                f"✗ config.json nennt das Kapitel {slug}, aber {html / slug} ist nicht gebaut"
            )
        nodes.append({
            "@type": "Chapter",
            "position": len(nodes) + 1,
            "name": page.get("title") or slug,
            "url": f"{site}/{slug}/",
        })
    if not nodes:
        raise SystemExit(f"✗ {html / 'config.json'} nennt kein einziges Kapitel")
    return nodes


def sibling_nodes(site: str, book: dict) -> list[dict]:
    """Die beiden anderen Vorlesungsskripten. Siehe „Drei Werke, ein Autor“."""
    nodes = json.loads(SIBLINGS.read_text(encoding="utf-8").replace("__SITE__", site))
    for node in nodes:
        # Die Referenz muss sich innerhalb desselben Dokuments auflösen, sonst sagt der
        # Graph dreimal „irgendein Autor“ statt dreimal „dieser Autor“.
        if node["author"]["@id"] != book["author"]["@id"]:
            raise SystemExit(
                f"✗ {SIBLINGS.name}: {node['name']} ist {node['author']['@id']} "
                f"zugeschrieben, nicht dem Autor des Buchs {book['author']['@id']}"
            )
        if node["@id"] == book["@id"]:
            raise SystemExit(f"✗ {SIBLINGS.name}: {node['name']} benutzt die @id des Buchs")
    return nodes


def pruefen(target: Path, page: str, book: dict, site: str, html: Path) -> int:
    """Nachbedingung am gebauten HTML, nicht eine Bilanz dessen, was dieser Lauf schrieb.

    Läuft auch dann, wenn der Block schon dastand: ein zweiter Lauf schreibt nichts, soll
    aber trotzdem merken, wenn der Graph seine Nebenwerke verloren hat oder sie jemand
    anderem zuschreibt. Die CI hat für die Landingpage kein eigenes Gatter — das hier ist
    es.
    """
    found = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
    if len(found) != 1:
        print(f"✗ {target} trägt {len(found)} ld+json-Blöcke, erwartet war genau einer")
        return 1
    try:
        payload = json.loads(found[0])
    except json.JSONDecodeError as exc:
        print(f"✗ {target} trägt ld+json, das nicht parst: {exc}")
        return 1
    # Der Buchknoten wird über seine @id gesucht, nicht über seine Stelle im Graphen;
    # die Reihenfolge trägt also nichts.
    graph = payload.get("@graph", [payload])
    buch = next((n for n in graph if n.get("@id") == book["@id"]), None)
    if buch is None:
        print(f"✗ der Graph der Landingpage hat keinen Knoten {book['@id']}; "
              f"er nennt {[n.get('@id') for n in graph]}")
        return 1
    if not str(buch.get("image", "")).startswith("http"):
        print(f"✗ {target}: image im Buchknoten ist keine absolute URL")
        return 1
    if not str(buch.get("dateModified", "")).startswith("20"):
        print(f"✗ {target}: dateModified im Buchknoten fehlt oder ist unplausibel")
        return 1
    if buch.get("publisher", {}).get("@id") != book["author"]["@id"]:
        print(f"✗ {target}: publisher ist {buch.get('publisher')}, erwartet war eine "
              f"Referenz auf {book['author']['@id']} (selbst veroeffentlicht)")
        return 1
    if buch.get("audience", {}).get("@type") != "EducationalAudience":
        print(f"✗ {target}: audience fehlt oder ist keine EducationalAudience")
        return 1
    # Die Kapitelliste wird gegen den Bau geprueft, nicht gegen sich selbst: ein Kapitel,
    # das die toc nicht mehr fuehrt, muss hier auffallen und nicht stehenbleiben.
    kapitel = buch.get("hasPart") or []
    soll = chapter_nodes(site, html)
    if kapitel != soll:
        fehlend = [n["url"] for n in soll if n["url"] not in {k.get("url") for k in kapitel}]
        zuviel = [k.get("url") for k in kapitel if k.get("url") not in {n["url"] for n in soll}]
        print(f"✗ {target}: hasPart nennt {len(kapitel)} Kapitel, der Bau {len(soll)}"
              + (f"; es fehlen {fehlend[:3]}" if fehlend else "")
              + (f"; zu viel sind {zuviel[:3]}" if zuviel else "")
              + ("; gleiche Menge, andere Reihenfolge oder Benennung"
                 if not fehlend and not zuviel else ""))
        return 1

    andere = [n for n in graph if n is not buch]
    erwartet = sibling_nodes(site, book)
    if len(andere) != len(erwartet):
        print(f"✗ die Landingpage nennt {len(andere)} weitere Werke, "
              f"{SIBLINGS.name} führt {len(erwartet)}")
        return 1
    for node in andere:
        if node.get("author", {}).get("@id") != book["author"]["@id"]:
            print(f"✗ {node.get('name')} auf der Landingpage ist nicht "
                  f"{book['author']['@id']} zugeschrieben")
            return 1
    print(f"✓ strukturierte Daten auf {target}: {buch['@type'][0]} {buch['url']}, "
          f"Stand {buch['dateModified'][:10]}, Autor {book['author']['@id']}, "
          f"{len(kapitel)} Kapitel in hasPart, "
          f"dazu {len(andere)} weitere Werke desselben Autors: "
          f"{', '.join(n.get('name', '?') for n in andere)}")
    return 0


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    site, html = sys.argv[1].rstrip("/"), Path(sys.argv[2])
    target = html / "index.html"

    page = target.read_text(encoding="utf-8")
    data = json.loads(TEMPLATE.read_text(encoding="utf-8").replace("__SITE__", site))

    if "application/ld+json" in page:
        print(f"✓ {target} trägt bereits strukturierte Daten; nichts geschrieben")
        return pruefen(target, page, data, site, html)

    card = re.search(r'<meta property="og:image" content="([^"]+)"', page)
    if not card:
        print(f"✗ {target} hat kein og:image, auf das die strukturierten Daten zeigen könnten")
        return 1
    if not card.group(1).startswith("http"):
        print(f"✗ {target} hat ein relatives og:image: {card.group(1)}")
        return 1
    data["image"] = card.group(1)

    stamp = re.search(r'<meta property="article:modified_time" content="([^"]+)"', page)
    if not stamp:
        print(f"✗ {target} hat kein article:modified_time — lief freshness.py vorher?")
        return 1
    data["dateModified"] = stamp.group(1)

    # Die Kapitel aus dem Bau, nicht von Hand: siehe Abschnitt 2 des Docstrings.
    data["hasPart"] = chapter_nodes(site, html)

    # Der Kontext wandert hoch zum Graphen; ein Knoten innerhalb eines `@graph`, der seinen
    # eigenen mitführt, ist zwar erlaubt, aber Rauschen.
    buch = {k: v for k, v in data.items() if k != "@context"}
    graph = {
        "@context": "https://schema.org",
        "@graph": [buch, *sibling_nodes(site, data)],
    }

    # ensure_ascii, damit die Nutzlast jede Kodierungsüberraschung unterwegs übersteht;
    # "</" wird getrennt, weil ein wörtliches </script> das Element früh schlösse.
    payload = json.dumps(graph, ensure_ascii=True, indent=2).replace("</", "<\\/")
    block = f'<script type="application/ld+json">{payload}</script>'

    if "</head>" not in page:
        print(f"✗ {target} hat kein </head>")
        return 1
    page = page.replace("</head>", block + "</head>", 1)
    target.write_text(page, encoding="utf-8")
    print(f"✓ strukturierte Daten in {target} ({len(payload)} Bytes, "
          f"Karte {data['image'].split('/')[-1]}, Stand {data['dateModified'][:10]}, "
          f"{len(data['hasPart'])} Kapitel)")
    return pruefen(target, page, data, site, html)


if __name__ == "__main__":
    raise SystemExit(main())
