#!/usr/bin/env python3
"""Die OpenGraph-Tags nachtragen, die MyST auslaesst, die Sprache setzen, die Schriften
vorladen und die Abbildungen unter der Falz verzoegert laden.

    python3 tools/head_meta.py <site-url> <html-dir> [--base BASE_URL]

Drei Dinge, alle als Nachbearbeitung am gebauten HTML, weil keines davon in myst.yml
oder im Frontmatter eines Kapitels gesagt werden kann. Portiert aus ds-en am
2026-10-16; dort macht dasselbe Skript noch ein viertes, siehe "Was hier absichtlich
fehlt" unten.


1. Die fuenf Karten-Tags, die MyST auslaesst
-------------------------------------------

MyST schreibt og:title, og:description und og:image und hoert dann auf. Fuenf fehlen:

- **og:url** ist, was eine Plattform als kanonische Identitaet eines geteilten Links
  behandelt: ohne es werden aus zwei Schreibweisen derselben URL zwei Karten mit zwei
  Kommentarstraengen.
- **og:site_name** setzt den Namen des Buchs auf die Karte und speist Googles
  Site-Name-Signal.
- **twitter:card = summary_large_image.** Die Vorschaukarte liegt in 1200x630 vor
  (tools/social_card.py), aber ohne diese Zeile zeigt X die kleine Karte mit
  Briefmarkenbild. Die Inhalte holt X sich aus den og:-Tags, twitter:title und
  twitter:description sind deshalb ueberfluessig -- nur die Kartenform muss gesagt werden.
- **og:type**: "book" auf dem Titelblatt, "article" auf den Kapiteln. Die Vorgabe ohne
  Angabe ist "website", also das, was ein Shop-Startseite waere.
- **og:locale = de_DE** und **og:locale:alternate = en_US**. Die zweite Zeile ist die
  Karten-Entsprechung des hreflang-Paars: sie sagt der Plattform, dass es dieselbe Sache
  auf Englisch gibt (tools/hreflang.py macht das fuer Suchmaschinen).

og:url bekommt dieselbe URL wie der Canonical -- mit Schraegstrich, die Form, die 200
liefert. Deshalb laeuft dieser Schritt *nach* dem Canonical-Schritt in .gitlab-ci.yml.

**Der Name wird aus der Landingpage gelesen, nie hart geschrieben.** Deren <title> ist
der Projekttitel allein, ein Umbenennen in myst.yml traegt sich also von selbst durch
und kann keine veraltete Zeichenkette hinterlassen.


2. Das Vorladen der Schriften
-----------------------------

Die zwei woff2-Dateien liegen seit dem 2026-10-16 auf demselben Server (siehe
_site/fonts/PROVENANCE.txt), aber eine Schrift, die aus einem Stylesheet referenziert
wird, wird immer noch erst entdeckt, wenn dieses Stylesheet geholt und geparst ist. Das
Vorladen holt sie auf Ebene eins.

`crossorigin` ist **noetig, obwohl sie von derselben Herkunft kommen**: Schriftanfragen
laufen im CORS-Modus, und ein Preload, dessen Modus nicht zur spaeteren Anfrage passt,
wird zweimal geholt statt einmal -- der eine Fehler, der aus dieser Verbesserung eine
Verschlechterung macht.


3. loading="lazy" auf den Abbildungen -- und die Preloads, die es aufgehoben haetten
------------------------------------------------------------------------------------

Das erste Bild in <main> bleibt eager: das LCP-Element verzoegert zu laden heisst genau
die Messung zu verschlechtern, um die es geht. Alles danach bekommt `loading="lazy"` und
`decoding="async"`. Das Logo der Navigation steht ausserhalb von <main> und wird nie
angefasst.

**Das Attribut allein haette nichts getan.** MyST schreibt fuer *jedes* Bild der Seite
ein `<link rel="preload" as="image">` in den Kopf -- am 2026-10-16 zwoelf auf kmeans,
sechzehn auf lineare-regression, vierzehn auf dimensionsreduktion, bei null lazy. Das,
und nicht das fehlende Attribut, ist der Grund, warum ein Kapitel seinen ganzen
Abbildungssatz vor dem load-Ereignis holt. Ein vorgeladenes Bild wird sofort geholt, was
`loading` auch sagt; die zwei Tags widersprechen sich und das Preload gewinnt.

Das Preload wird deshalb fuer genau die Bilder entfernt, die lazy geworden sind, und
bleibt fuer die zwei, die es haben sollen: das Logo (ausserhalb von <main>) und die
erste Abbildung (LCP-Kandidat). Die Entfernung an die Menge der lazy gemachten URLs zu
binden, statt alle Preloads zu streichen, ist genau das, was diese zwei erhaelt.

Nur die <main>-Scheibe wird umgeschrieben. Der Rest des Dokuments traegt MySTs
Hydrations-Nutzlast -- die ganze Seite noch einmal als JSON in einem <script> -- und ein
freilaufender regulaerer Ausdruck darauf wuerde Zeichenketten aendern, die der Browser
als Daten liest.


4. lang="de" am <html>
----------------------

Das Theme schreibt `<html lang="en">`, hart im Bundle (am 2026-10-16 zwoelf Vorkommen in
book-theme), und myst.yml hat keinen Schalter dafuer. Eine deutsche Seite, die sich als
englisch ausgibt, laesst Screenreader den Text englisch aussprechen und widerspricht
allem anderen am Dokument: hreflang="de", inLanguage "de" im JSON-LD, 1300 Woerter
Deutsch.

Das Attribut im ausgelieferten HTML zu setzen reicht aber nicht. Die Hydration des Themes
schreibt lang="en" zurueck: am 2026-10-16 nachgemessen, ohne JavaScript "de", mit
JavaScript "en" -- ausgerechnet der Screenreader sieht also die falsche Sprache. Deshalb
geht ein kleiner Waechter mit, ein MutationObserver auf genau diesem Attribut. Einmalig
zuweisen genuegt nicht, weil das Theme ein Client-Router ist und jeder Kapitelwechsel
ohne Neuladen das Attribut erneut setzt.

**Hier reicht das Markup, anders als beim Titel** -- und das ist gemessen, nicht
angenommen. Am 2026-10-16 lokal gegen dasselbe Bundle: `_build/html` auf "de" gepatcht,
mit python3 -m http.server unter dem richtigen Basispfad ausgeliefert, im Browser nach
der Hydration und nach einer Navigation nachgesehen -- beide Male "de". React korrigiert
die Abweichung am Wurzelelement nicht, der Titel dagegen wird aus der Nutzlast neu
gerendert. Das ist der Unterschied, und er war vorher nicht absehbar.

Das sichtbare Datum ("October 16, 2026") haengt *nicht* hieran: das Theme formatiert es
mit toLocaleDateString, also nach der Locale des Lesers, und im serverseitig gebauten
HTML nach der des CI-Containers. Ein eigenes Thema, siehe
todo/seo-landingpage-2026-10-16.md.

Was hier absichtlich fehlt
--------------------------

**Alles, was die Hydration anfasst, steht in tools/hydration.py.** Dieses Skript hier
schreibt ins Markup; das ist richtig fuer alles, was ein Leser ohne JavaScript und ein
einfacher Crawler sehen, aber der <head> gehoert zum React-Baum, und was die Hydration
wegwirft, holt erst der Kopf-Waechter dort zurueck. Die fuenf Karten-Tags von Abschnitt 1
sind so ein Fall; die zwei Schrift-Preloads von Abschnitt 2 sind keiner, denn ein Preload
wirkt nur im ausgelieferten Dokument.

ds-ens Fassung kuerzt zusaetzlich den Titel-Suffix und muss dafuer in die
Hydrations-Nutzlast schreiben, weil das Theme den Titel daraus neu rendert. **Das ist
hier nicht portiert** (Uebergabe aus ds-en, Abschnitt 7): ds-skripts Suffix ist
" - Data Science Vorlesungsskript", 32 Zeichen gegen ds-ens 49, und die Messung, die es
dort rechtfertigte -- auf 29 von 30 Seiten war der Suffix ohnehin abgeschnitten --, ist
hier deutlich milder. `site.title` ist in myst.yml nicht gesetzt, der Hebel existiert
also, falls er je gewollt ist. Wird er gezogen: das Theme rendert den Titel aus der
Nutzlast neu, ein Bearbeiten von <title> im Markup allein ist im Browser wieder weg --
und Google rendert, bevor es indexiert.


Zweimal laufen
--------------

Idempotent, und es prueft Nachbedingungen statt der eigenen Aenderungen: jede Seite muss
am Ende die fuenf Karten-Tags und lang="de" fuehren, und kein lazy gemachtes Bild darf
noch ein Preload tragen. Ein zweiter Lauf ist ein zulaessiger Leerlauf, der trotzdem besteht,
waehrend Markup, das MyST unter uns verschoben hat, auffaellt -- der Fall, fuer den die
Pruefung eigentlich da ist.

Ergaenzt wird deshalb **je Tag**, nicht pauschal: ein Artefakt, das die vorige Fassung
dieses Skripts schon bearbeitet hat, bekommt genau die Tags nach, die ihm fehlen. Die
Alternative -- ein Riegel an og:url fuer alle Tags -- bricht in dem Moment, in dem ein
Tag dazukommt.
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys

# Erkennungszeichen des Sprach-Waechters, damit ein zweiter Lauf Leerlauf bleibt.
MARKER_LANG = "/*lang-waechter*/"

FONTS = ("inter-latin.woff2", "jetbrains-mono-latin.woff2")


def page_url(site: str, rel: pathlib.PurePath) -> str:
    """Die URL, die 200 liefert: mit Schraegstrich, so wie der Canonical sie hat."""
    return f"{site}/" if str(rel) == "." else f"{site}/{rel}/"


def project_title(index_html: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", index_html, re.S | re.I)
    if not m:
        sys.exit("FEHLER: die Landingpage hat kein <title>; kein Name fuer og:site_name")
    title = m.group(1).strip()
    if not title:
        sys.exit("FEHLER: der <title> der Landingpage ist leer")
    return title


def head_tags(
    url: str, site_name: str, base: str, lang: str, is_landing: bool
) -> list[tuple[str, str]]:
    """Die Tags als (Merkmal, Tag): das Merkmal sagt, ob die Seite das Tag schon hat.

    Je Tag gepruefen, nicht einmal pauschal fuer alle. Ein Riegel an og:url allein
    (so stand es bis zum 2026-10-16) heisst: kommt ein Tag hinzu, bleibt es auf jedem
    Artefakt aus, das die vorige Fassung schon bearbeitet hat -- und die Nachbedingung
    schlaegt an, ohne dass ein Lauf das heilen kann. Beim Hinzufuegen der Karten-Tags
    genau so passiert, im Image nachgestellt.
    """
    # de -> de_DE: OpenGraph will den Unterstrich-Code, nicht das Sprachkuerzel.
    locale = {"de": "de_DE", "en": "en_US"}.get(lang, lang)
    alternate = "en_US" if locale != "en_US" else "de_DE"
    tags = [
        (
            'property="og:url"',
            f'<meta property="og:url" content="{html.escape(url, quote=True)}"/>',
        ),
        (
            'property="og:site_name"',
            f'<meta property="og:site_name" content="{html.escape(site_name, quote=True)}"/>',
        ),
        (
            'property="og:type"',
            f'<meta property="og:type" content="{"book" if is_landing else "article"}"/>',
        ),
        ('property="og:locale"', f'<meta property="og:locale" content="{locale}"/>'),
        (
            'property="og:locale:alternate"',
            f'<meta property="og:locale:alternate" content="{alternate}"/>',
        ),
        (
            'name="twitter:card"',
            '<meta name="twitter:card" content="summary_large_image"/>',
        ),
    ]
    tags += [
        (
            f'href="{base}/fonts/{f}"',
            f'<link rel="preload" href="{base}/fonts/{f}" as="font" '
            f"type=\"font/woff2\" crossorigin/>",
        )
        for f in FONTS
    ]
    return tags


def set_html_lang(doc: str, lang: str) -> tuple[str, bool]:
    """Die Sprache am <html> setzen. Gibt das Dokument und zurueck, ob es sie schon hatte."""
    m = re.search(r"<html\b[^>]*>", doc, re.I)
    if not m:
        return doc, False
    tag = m.group(0)
    if re.search(rf'\blang="{re.escape(lang)}"', tag, re.I):
        return doc, True
    if re.search(r'\blang="[^"]*"', tag, re.I):
        new_tag = re.sub(r'\blang="[^"]*"', f'lang="{lang}"', tag, count=1, flags=re.I)
    else:
        new_tag = tag[:5] + f' lang="{lang}"' + tag[5:]
    return doc[: m.start()] + new_tag + doc[m.end() :], False


MONATE = ("Januar", "Februar", "März", "April", "Mai", "Juni",
          "Juli", "August", "September", "Oktober", "November", "Dezember")


def datum_eindeutschen(doc: str) -> tuple[str, int]:
    """Das sichtbare Datum deutsch schreiben. Nur der Text, nie das Attribut.

    MyST rendert `date:` aus dem Frontmatter als `October 16, 2026` -- englisch, weil das
    Theme keine Lokalisierung kennt und seine Sprache ohnehin hart auf "en" steht. Auf einer
    Seite, die sich seit 1f48c57 als lang="de" ausweist, steht damit ein englisches Datum
    unter der deutschen Autorenzeile.

    Ersetzt wird ausschliesslich der **Text** zwischen den Tags. Das `dateTime`-Attribut
    bleibt unberuehrt: es ist die maschinenlesbare Angabe, ISO 8601 ist dort richtig, und
    freshness.py sowie das JSON-LD haengen daran.

    Die Monatsnamen stehen hier als Liste und kommen nicht aus `locale`: der CI-Container
    bringt keine de_DE-Locale mit, und ein stillschweigender Rueckfall auf C haette wieder
    englische Namen geliefert -- derselbe Fehler, nur schwerer zu sehen.

    Betrifft heute genau eine Seite, die Landingpage; die Kapitel tragen kein Datum. Die
    Funktion laeuft trotzdem ueber alle, damit ein kuenftiges Kapiteldatum mitgenommen wird.
    """
    import datetime as _dt

    # Gezaehlt werden Aenderungen, nicht Treffer: ein zweiter Lauf findet dasselbe Element
    # wieder, aendert nichts und soll das auch so berichten.
    geaendert = [0]

    def ersetze(m: re.Match) -> str:
        vor, iso, mitte, text, nach = m.groups()
        try:
            d = _dt.date.fromisoformat(iso)
        except ValueError:
            return m.group(0)
        deutsch = f"{d.day}. {MONATE[d.month - 1]} {d.year}"
        if text == deutsch:
            return m.group(0)
        geaendert[0] += 1
        return f"{vor}{iso}{mitte}{deutsch}{nach}"

    doc, _ = re.subn(
        r'(<time\b[^>]*\bdateTime=")(\d{4}-\d{2}-\d{2})("[^>]*class="[^"]*myst-fm-date-string[^"]*"[^>]*>)'
        r'([^<]*)(</time>)',
        ersetze, doc,
    )
    return doc, geaendert[0]


def keep_html_lang(doc: str, lang: str) -> tuple[str, bool]:
    """Das lang nach der Hydration wieder setzen -- sonst haelt es nur bis zum ersten Frame.

    set_html_lang repariert das *ausgelieferte* HTML. Das reicht fuer Crawler und fuer
    Lesen ohne JavaScript, aber nicht fuer den Leser: das Theme traegt lang="en" hart im
    Bundle, und die Hydration schreibt es zurueck. Nachgemessen am 2026-10-16 auf der
    ausgelieferten Seite -- ohne JavaScript "de", mit JavaScript "en". Ausgerechnet der
    Screenreader, fuer den das Attribut da ist, sieht also die falsche Sprache.

    Ein MutationObserver statt einer einmaligen Zuweisung, weil das Zuruecksetzen erst
    beim Hydrieren passiert, also nach dem Parsen des Dokuments -- ein Skript im <head>
    kaeme sonst zu frueh.

    (Hier stand bis zum 2026-10-29 zusaetzlich, das Theme sei ein Client-Router und setze
    das Attribut bei jedem Kapitelwechsel erneut. Nachgemessen stimmt das nicht: beim
    statischen Bau setzt das Theme "reload" an seine Links, ein Klick im Buch ist ein
    echter Seitenaufruf, und ein Marker auf window ueberlebt ihn nicht. Der Observer ist
    trotzdem richtig, nur aus dem Grund im Absatz darueber.)
    """
    if MARKER_LANG in doc:
        return doc, True
    if "</head>" not in doc:
        return doc, False
    script = (
        f'<script>{MARKER_LANG}(function(){{var l="{lang}",h=document.documentElement;'
        "function f(){if(h.lang!==l)h.lang=l}f();"
        'new MutationObserver(f).observe(h,{attributes:true,attributeFilter:["lang"]});'
        "})();</script>"
    )
    return doc.replace("</head>", script + "</head>", 1), False


def mit_attributen(tag: str, zusatz: str) -> str:
    """Attribute ans Ende eines Tags, mit dem schliessenden Schraegstrich dahinter.

    `<img ... />` endet auf "/>", und wer nur das letzte Zeichen abschneidet und wieder
    anhaengt, schiebt die neuen Attribute *hinter* den Schraegstrich: `... alt="x"/
    loading="lazy">`. Ein Parser liest den Schraegstrich dann als Attributnamen, verzeiht
    es zwar, aber ein Validator nicht -- und genau das stand vom 2026-10-16 bis zum
    2026-10-29 im ausgelieferten HTML, auf jeder der 171 lazy gemachten Abbildungen.
    Gefunden beim Messen von tools/image_dims.py, das dieselbe Stelle anfasst.
    """
    kern = tag[:-1].rstrip()
    schraeg = ""
    if kern.endswith("/"):
        kern, schraeg = kern[:-1].rstrip(), "/"
    return f"{kern} {zusatz}{schraeg}>"


def lazy_load_figures(doc: str) -> tuple[str, set[str]]:
    """Jedes <img> in <main> ausser dem ersten verzoegert laden.

    Gibt das Dokument und die Menge der src-URLs zurueck, die lazy geworden sind, damit
    der Aufrufer die passenden Preloads entfernen kann -- ohne das hat das Attribut
    ueberhaupt keine Wirkung.
    """
    m = re.search(r"<main\b[^>]*>.*?</main>", doc, re.S | re.I)
    if not m:
        return doc, set()

    main = m.group(0)
    lazied: set[str] = set()
    seen = 0

    def img_sub(tag: re.Match) -> str:
        nonlocal seen
        seen += 1
        t = tag.group(0)
        if seen == 1:  # LCP-Kandidat bleibt eager und behaelt sein Preload
            return t
        src = re.search(r'\bsrc="([^"]*)"', t, re.I)
        if src:
            lazied.add(src.group(1))
        if re.search(r"\bloading=", t, re.I):
            return t
        return mit_attributen(t, 'loading="lazy" decoding="async"')

    main_new = re.sub(r"<img\b[^>]*?/?>", img_sub, main, flags=re.I)
    return doc[: m.start()] + main_new + doc[m.end() :], lazied


def drop_image_preloads(doc: str, srcs: set[str]) -> tuple[str, int]:
    """`<link rel="preload" as="image">` fuer die jetzt lazy geladenen Bilder entfernen."""
    if not srcs:
        return doc, 0
    n = 0

    def link_sub(m: re.Match) -> str:
        nonlocal n
        tag = m.group(0)
        if 'as="image"' not in tag:
            return tag
        href = re.search(r'\bhref="([^"]*)"', tag)
        if href and href.group(1) in srcs:
            n += 1
            return ""
        return tag

    doc = re.sub(r'<link\b[^>]*rel="preload"[^>]*/?>', link_sub, doc, flags=re.I)
    return doc, n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("html_dir")
    ap.add_argument("--base", default="", help="BASE_URL, der Pfad, unter dem die Seite liegt")
    ap.add_argument(
        "--lang",
        default="de",
        help='Sprache fuer das <html lang>-Attribut (Vorgabe "de"; das Theme sagt "en")',
    )
    args = ap.parse_args()

    site = args.site.rstrip("/")
    root = pathlib.Path(args.html_dir)
    index = root / "index.html"
    if not index.exists():
        sys.exit(f"FEHLER: {index} existiert nicht; nach dem HTML-Bau laufen lassen")

    name = project_title(index.read_text(encoding="utf-8"))

    pages = sorted(root.rglob("index.html"))
    n_lazy = n_preload = n_head = n_lang = n_guard = n_datum = 0

    for f in pages:
        rel = f.parent.relative_to(root)
        url = page_url(site, rel)
        doc = f.read_text(encoding="utf-8")

        fehlend = [
            tag
            for marker, tag in head_tags(
                url, name, args.base, args.lang, str(rel) == "."
            )
            if marker not in doc
        ]
        if fehlend:
            if "</head>" not in doc:
                sys.exit(f"FEHLER: {f} hat kein </head>")
            doc = doc.replace("</head>", "".join(fehlend) + "</head>", 1)
            n_head += 1

        doc, had_lang = set_html_lang(doc, args.lang)
        if not had_lang:
            n_lang += 1
        doc, had_guard = keep_html_lang(doc, args.lang)
        if not had_guard:
            n_guard += 1

        if args.lang == "de":
            doc, umgestellt = datum_eindeutschen(doc)
            n_datum += umgestellt

        doc, lazied = lazy_load_figures(doc)
        doc, dropped = drop_image_preloads(doc, lazied)
        n_lazy += len(lazied)
        n_preload += dropped

        f.write_text(doc, encoding="utf-8")

    # Nachbedingungen, keine Bilanz dieses Laufs: ein zweiter Lauf ist ein zulaessiger
    # Leerlauf, waehrend unter uns verschobenes Markup auffallen muss.
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        if 'property="og:url"' not in doc:
            sys.exit(f"FEHLER: {f} hat weiterhin kein og:url")
        for prop, kind in (
            ("og:site_name", "property"),
            ("og:type", "property"),
            ("og:locale", "property"),
            ("og:locale:alternate", "property"),
            ("twitter:card", "name"),
        ):
            if f'{kind}="{prop}"' not in doc:
                sys.exit(f"FEHLER: {f} hat weiterhin kein {prop}")
        m_html = re.search(r"<html\b[^>]*>", doc, re.I)
        if not m_html or not re.search(
            rf'\blang="{re.escape(args.lang)}"', m_html.group(0), re.I
        ):
            sys.exit(f'FEHLER: {f} fuehrt weiterhin nicht lang="{args.lang}"')
        if args.lang == "de":
            m_datum = re.search(
                r'class="[^"]*myst-fm-date-string[^"]*"[^>]*>([^<]*)</time>', doc
            )
            if m_datum and re.search(
                r"\b(January|February|March|April|May|June|July|August|September|"
                r"October|November|December)\b", m_datum.group(1)
            ):
                sys.exit(f"FEHLER: {f} zeigt das Datum weiterhin englisch: "
                         f"{m_datum.group(1)!r}")
        if MARKER_LANG not in doc:
            sys.exit(f"FEHLER: {f} hat keinen Sprach-Waechter -- die Hydration"
                     f' setzt lang wieder auf "en"')
        # Ein lazy gemachtes Bild, das noch ein Preload traegt, hebt sich selbst auf.
        m = re.search(r"<main\b[^>]*>.*?</main>", doc, re.S | re.I)
        if not m:
            continue
        lazy_srcs = set(re.findall(r'<img\b[^>]*\bloading="lazy"[^>]*>', m.group(0), re.I))
        lazy_urls = {
            s.group(1)
            for tag in lazy_srcs
            if (s := re.search(r'\bsrc="([^"]*)"', tag))
        }
        for tag in re.findall(r'<link\b[^>]*rel="preload"[^>]*>', doc, re.I):
            if 'as="image"' not in tag:
                continue
            href = re.search(r'\bhref="([^"]*)"', tag)
            if href and href.group(1) in lazy_urls:
                sys.exit(f"FEHLER: {f} laedt ein lazy-Bild weiterhin vor: {href.group(1)}")

    print(
        f"head_meta: {len(pages)} Seiten, die fuenf Karten-Tags auf allen "
        f"({n_head} ergaenzt), lang=\"{args.lang}\" auf allen ({n_lang} gesetzt, "
        f"{n_guard} Waechter), {n_datum} Datum eingedeutscht, "
        f"{n_lazy} Abbildungen lazy, {n_preload} Bild-Preloads entfernt"
    )


if __name__ == "__main__":
    main()
