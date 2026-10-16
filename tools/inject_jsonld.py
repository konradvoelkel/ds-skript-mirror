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
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent / "structured-data.json"


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    site, html = sys.argv[1].rstrip("/"), Path(sys.argv[2])
    target = html / "index.html"

    page = target.read_text(encoding="utf-8")
    if "application/ld+json" in page:
        print(f"✓ {target} trägt bereits strukturierte Daten; nichts getan")
        return 0

    data = json.loads(TEMPLATE.read_text(encoding="utf-8").replace("__SITE__", site))

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

    # ensure_ascii, damit die Nutzlast jede Kodierungsüberraschung unterwegs übersteht;
    # "</" wird getrennt, weil ein wörtliches </script> das Element früh schlösse.
    payload = json.dumps(data, ensure_ascii=True, indent=2).replace("</", "<\\/")
    block = f'<script type="application/ld+json">{payload}</script>'

    if "</head>" not in page:
        print(f"✗ {target} hat kein </head>")
        return 1
    target.write_text(page.replace("</head>", block + "</head>", 1), encoding="utf-8")
    print(f"✓ strukturierte Daten in {target} ({len(payload)} Bytes, "
          f"Karte {data['image'].split('/')[-1]}, Stand {data['dateModified'][:10]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
