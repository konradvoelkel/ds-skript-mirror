#!/usr/bin/env python3
"""Was die Hydration des Themes anfasst: die Nutzlast, und der Kopf danach.

    python3 tools/hydration.py <site-url> <html-verzeichnis> [--base BASE_URL]
    python3 tools/hydration.py --check <html-verzeichnis> [--base BASE_URL]

Im `pages`-Job als **letzter** Kopf-Schritt laufen zu lassen, nach `hreflang.py`,
`freshness.py`, `inject_jsonld.py` und `llms_txt.py`: das Skript liest die Tags, die
diese geschrieben haben, aus dem Kopf zurück und baut daraus seinen Wächter. Vor
`precompress.py`, wie jeder Schritt, der HTML ändert.

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

Zwei Dinge tut dieses Skript: es bringt die Nutzlast in Ordnung, und es hängt einen
kleinen Wächter in den Kopf, der die Tags zurückholt, die React ausgeräumt hat. **Welcher
Weg für welches Tag gilt, ist nicht Geschmack**: wo das Theme ein Feld der Nutzlast
rendert, wird das Feld gesetzt (dann rendert React es von selbst richtig und es gibt gar
keine Abweichung); wo es keines gibt, bleibt nur der Wächter.


1. `page.domain`
----------------

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


2. Die Vorschaukarte absolut, in der Nutzlast
---------------------------------------------

Die zwei `sed`-Zeilen im `pages`-Job machen `og:image` im Markup absolut, weil OpenGraph
keine relative URL akzeptiert. Nach der Hydration steht die Karte wieder relativ da, denn
das Theme baut `og:image` aus `page.frontmatter.thumbnailOptimized || thumbnail`
(Kapitel) bzw. `project.thumbnailOptimized || thumbnail` (Landingpage) **neu aus der
Nutzlast**.

Das ist der eine Fall, in dem es ein Feld gibt — also hier und nicht im Wächter unten:
schreibt die Nutzlast dieselbe absolute URL, rendert React sie von selbst richtig, und
die Abweichung zwischen ausgeliefertem und hydriertem Kopf verschwindet, statt
überschrieben zu werden. Dieselbe Stelle, die ds-ens `head_meta.py` aus demselben Grund
anfasst (`set_payload_card`).

**Nur diese vier Felder.** Die Nutzlast trägt zusätzlich `project.pages[]` und
`config.projects[0].pages[]`, einen Eintrag je Seite des Buchs mit eigenem `thumbnail`,
und das sind keine Kartenangaben: das Theme rendert sie als die kleine Vorschau, die beim
Überfahren eines internen Links aufgeht. Die mit umzuschreiben machte jede Vorschau im
Buch zur gleichen Karte.


3. Der Kopf-Wächter
-------------------

Für die übrigen Tags gibt es **keinen Platz in der Nutzlast**, und das ist gemessen, nicht
vermutet: im Bundle nachgelesen ist `links()` in beiden Route-Modulen eine *Konstante*
(die vier Stylesheets des Themes, `()=>[Cp]` bzw. `()=>[{rel:"stylesheet",…}]`), und der
Meta-Erzeuger nimmt nur `origin`, `url`, `title`, `description`, `image`, `twitter` und
`keywords` — kein Canonical, kein hreflang, kein `og:site_name`, `og:type`, `og:locale`.
`og:url` käme heraus, aber beide Route-Module übergeben `origin:""` hart im Bundle, und
`""` ist falsch, also pusht das Theme das Tag nie. Es gibt also schlicht kein Feld, das
man setzen könnte; der Vergleich mit ds-ens Titel-Suffix (das aus `project.title` kommt,
einem echten Feld) trägt hier nicht.

Bleiben zwei Wege, und der Unterschied ist der Preis: ein Patch am minifizierten,
fingerprinted Bundle — der bricht beim nächsten Theme-Update still, derselbe Grund, aus
dem Punkt 10 der SEO-Notiz zurückgenommen wurde — oder ein kleiner Wächter, derselbe
Griff, mit dem `lang="de"` seit dem 2026-10-16 hält. Der Wächter gewinnt: er kennt das
Theme nicht, er kennt nur die Tags.

Er trägt die Tags **seiner eigenen Seite** als Daten bei sich, ausgelesen aus dem Kopf,
den die Schritte davor geschrieben haben. Eine Liste von Sollwerten hier im Skript wäre
eine zweite Quelle der Wahrheit neben `hreflang.py`, `freshness.py`, `llms_txt.py` und
den `sed`-Zeilen des Jobs und liefe irgendwann auseinander; so ist jedes Tag, das ein
Schritt in den Kopf schreibt, von selbst mitgeschützt, sobald sein Muster in
`GESCHUETZT` steht.

`MutationObserver` auf `childList` des `<head>`, nicht eine einmalige Zuweisung: React
räumt die Kopf-Kinder erst beim Hydrieren aus, und das passiert nach dem Parsen. Mit
Wiedereintritts-Riegel, weil das Anhängen im Callback den Observer erneut auslöst.

**Was der Wächter nicht zurückholt: die zwei Schrift-Preloads — und das ist eine
Entscheidung, keine Lücke.** Ein Preload wirkt im *ausgelieferten* Dokument: es holt die
Schrift auf Ebene eins, noch bevor das Stylesheet geparst ist, und genau darum geht es
(siehe Abschnitt 2 von `head_meta.py`). Zum Zeitpunkt der Hydration sind beide `woff2`
längst angefragt; ein Preload danach wieder einzuhängen bewirkt nichts, außer dass eine
Messung grün aussieht. Sie stehen im Markup, dort wirken sie, dort bleiben sie — und
`GESCHUETZT` führt sie deshalb nicht. Dasselbe gilt für das leere `keywords`-Tag aus
Punkt 10 der SEO-Notiz, nur in der anderen Richtung: das baut das Theme von selbst
wieder, und es herauszuhalten wäre ein Kampf um ein Tag, das niemand auswertet.


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

Idempotent. In der Nutzlast wird nur gesetzt, was noch nicht gesetzt ist. Der Wächter
wird an seinem Erkennungszeichen erkannt und **ersetzt**, nicht ein zweites Mal
angehängt: er trägt Daten, und die können sich geändert haben.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Erkennungszeichen des Kopf-Wächters. Ein zweiter Lauf ersetzt ihn daran.
MARKER = "/*kopf-waechter*/"

GUARD_RE = re.compile(r"<script>" + re.escape(MARKER) + r".*?</script>", re.S)

# Die Tags, die die Hydration wegwirft und die der Wächter zurückholt, je als
# (Muster im Kopf, Attribute, die die Identität des Tags ausmachen).
#
# Die Werte stehen *nicht* hier, sondern werden aus dem gebauten Kopf gelesen -- siehe
# Abschnitt 3 des Docstrings. og:image fehlt mit Absicht: dafuer gibt es ein Feld in der
# Nutzlast, siehe absolute_card().
GESCHUETZT = (
    (re.compile(r'<link\b[^>]*\brel="canonical"[^>]*>', re.I), ("rel",)),
    (re.compile(r'<link\b[^>]*\bhreflang="[^"]*"[^>]*>', re.I), ("rel", "hreflang")),
    (
        re.compile(
            r'<meta\b[^>]*\bproperty="(?:og:url|og:site_name|og:type|og:locale'
            r'|og:locale:alternate|article:modified_time)"[^>]*>',
            re.I,
        ),
        ("property",),
    ),
    (re.compile(r'<meta\b[^>]*\bname="twitter:card"[^>]*>', re.I), ("name",)),
    (re.compile(r'<link\b[^>]*\btype="text/markdown"[^>]*>', re.I), ("rel", "type")),
)

ATTR_RE = re.compile(r'([a-zA-Z:_-]+)\s*=\s*"([^"]*)"')


def head_slice(doc: str, f: pathlib.Path) -> str:
    """Nur der Kopf. Der Rest des Dokuments trägt die Nutzlast -- die ganze Seite noch
    einmal als JSON --, und ein Muster darauf fände Zeichenketten, die Daten sind."""
    i = doc.find("</head>")
    if i < 0:
        sys.exit(f"FEHLER: {f} hat kein </head>")
    return doc[:i]


def collect_tags(head: str) -> list[dict]:
    """Die geschützten Tags aus dem Kopf lesen, als Daten für den Wächter.

    Je Tag: der Elementname, alle Attribute, und der Selektor, an dem der Wächter es im
    hydrierten Kopf wiedererkennt. Der Selektor nennt nur die Identitätsattribute
    (`rel`, `hreflang`, `property`, `name`), nicht `href` oder `content`: sonst würde ein
    Tag mit falschem Wert nicht korrigiert, sondern ein zweites daneben gestellt.
    """
    tags: list[dict] = []
    gesehen: set[str] = set()
    for muster, ident in GESCHUETZT:
        for m in muster.finditer(head):
            tag = m.group(0)
            name = "link" if tag.lower().startswith("<link") else "meta"
            attrs = dict(ATTR_RE.findall(tag))
            fehlend = [k for k in ident if k not in attrs]
            if fehlend:
                sys.exit(f"FEHLER: {tag} fehlt {fehlend} -- kein Selektor zu bauen")
            sel = name + "".join(f'[{k}="{attrs[k]}"]' for k in ident)
            if sel in gesehen:
                sys.exit(
                    f"FEHLER: zwei Tags mit demselben Selektor {sel} -- der Wächter"
                    " könnte sie nicht auseinanderhalten"
                )
            gesehen.add(sel)
            tags.append({"n": name, "s": sel, "a": attrs})
    return tags


def js_literal(obj) -> str:
    """JSON als JavaScript-Literal innerhalb eines `<script>`.

    Ein nacktes `<` könnte das Tag früh schließen, und U+2028/U+2029 sind in JSON
    gewöhnliche Zeichen, in JavaScript aber Zeilenenden. Als `\\u`-Folgen liest JSON
    dieselben Zeichen zurück.
    """
    out = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    return (
        out.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    )


def guard_script(path: str, tags: list[dict]) -> str:
    """Der Wächter: hängt an, was fehlt, und korrigiert, was falsch steht.

    `location.pathname` wird gegen den Pfad geprüft, für den dieser Satz gebaut wurde.
    Beim statischen Bau ist jeder Klick im Buch ein echter Seitenaufruf -- das Theme setzt
    im `staticBuild`-Modus `reload` an seine Links, am 2026-10-29 nachgemessen: ein Marker
    auf `window` überlebt keinen Kapitelwechsel --, der Fall tritt also nicht ein. Täte er
    es doch, trägt die Seite *keine* Tags statt der falschen, und das ist die richtige
    Richtung: ein Canonical, der auf die vorige Seite zeigt, ist schlimmer als keiner.
    """
    daten = js_literal({"p": path, "t": tags})
    js = (
        "(function(){var D=" + daten + ",b=false;"
        'function p(){var x=location.pathname;return x.charAt(x.length-1)==="/"?x:x+"/"}'
        "function f(){if(b||p()!==D.p)return;b=true;try{"
        "for(var i=0;i<D.t.length;i++){var t=D.t[i],e=document.head.querySelector(t.s);"
        "if(!e){e=document.createElement(t.n);document.head.appendChild(e)}"
        "for(var k in t.a){if(e.getAttribute(k)!==t.a[k])e.setAttribute(k,t.a[k])}}"
        "}finally{b=false}}f();"
        "new MutationObserver(f).observe(document.head,{childList:true});})();"
    )
    return f"<script>{MARKER}{js}</script>"


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
    return doc[:start] + js_literal(payload) + doc[end:], True


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


def absolute_card(doc: str, site: str, base: str) -> tuple[str, bool]:
    """Die Vorschaukarte in der Nutzlast absolut machen. Abschnitt 2 des Docstrings.

    Umgeschrieben wird nur, was wurzelrelativ unter dem Basispfad auf `/build/` zeigt --
    damit ein zweiter Lauf Leerlauf bleibt und eine fremde URL unberührt.
    """
    prefix = f"{base}/build/"

    def mutate(payload: dict) -> bool:
        changed = False
        for route in routes(payload):
            page = route.get("page")
            front = page.get("frontmatter") if isinstance(page, dict) else None
            for node in (front, route.get("project")):
                if not isinstance(node, dict):
                    continue
                for key in ("thumbnail", "thumbnailOptimized"):
                    url = node.get(key)
                    if isinstance(url, str) and url.startswith(prefix):
                        node[key] = site + url[len(base) :]
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


def page_path(base: str, rel: pathlib.PurePath) -> str:
    """Der Pfad, unter dem die Seite ausgeliefert wird -- mit Schrägstrich am Ende."""
    return f"{base}/" if str(rel) == "." else f"{base}/{rel}/"


def check(root: pathlib.Path, base: str) -> int:
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
    n = n_tags = 0
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        whole(doc, f)
        if "localhost:3000" in doc:
            sys.exit(f"FEHLER: {f} nennt weiterhin localhost:3000")
        # Der Wächter wird gegen den Kopf gerechnet, in dem er steht. Passt er nicht,
        # hat nach ihm noch ein Schritt Tags geschrieben -- und die hielte er dann nicht.
        tags = collect_tags(head_slice(doc, f))
        if guard_script(page_path(base, f.parent.relative_to(root)), tags) not in doc:
            sys.exit(
                f"FEHLER: {f} trägt keinen Wächter, der zu ihrem Kopf passt -- hat ein"
                " Schritt nach hydration.py noch Tags geschrieben?"
            )
        if not any(t["s"] == 'link[rel="canonical"]' for t in tags):
            sys.exit(f"FEHLER: {f} hat keinen Canonical, den der Wächter halten könnte")
        n_tags += len(tags)
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
            front = page.get("frontmatter")
            for node in (front, route.get("project")):
                if not isinstance(node, dict):
                    continue
                for key in ("thumbnail", "thumbnailOptimized"):
                    url = node.get(key)
                    if isinstance(url, str) and url.startswith(f"{base}/build/"):
                        sys.exit(
                            f"FEHLER: {f}: {key} in der Nutzlast ist weiterhin relativ"
                            f" ({url}) -- og:image waere nach der Hydration wieder relativ"
                        )
    print(
        f"✓ {len(pages)} Seiten: Nutzlast lesbar, {n} mal page.domain als Origin; "
        f"kein localhost:3000 mehr, weder im HTML noch in {len(rest)} Seiten-JSON"
    )
    print(f"✓ {n_tags} Tags in {len(pages)} Kopf-Wächtern, jeder passend zu seinem Kopf")
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
        return check(root, base)

    if not args.site:
        sys.exit("FEHLER: ohne --check ist die Site-URL nötig")
    site = args.site.rstrip("/")
    if base and not site.endswith(base):
        sys.exit(f"FEHLER: {site} endet nicht auf {base} -- dann wäre die Origin geraten")
    origin = site[: len(site) - len(base)] if base else site

    pages = sorted(root.rglob("index.html"))
    if not pages:
        sys.exit(f"FEHLER: keine Seite unter {root}")

    n_dom = n_card = n_tags = 0
    for f in pages:
        doc = f.read_text(encoding="utf-8")
        rel = f.parent.relative_to(root)

        doc, geaendert = set_domain(doc, origin)
        n_dom += geaendert
        doc, karte = absolute_card(doc, site, base)
        n_card += karte

        tags = collect_tags(head_slice(doc, f))
        script = guard_script(page_path(base, rel), tags)
        if MARKER in doc:
            doc = GUARD_RE.sub(lambda _: script, doc, count=1)
        else:
            doc = doc.replace("</head>", script + "</head>", 1)
        n_tags += len(tags)

        whole(doc, f)
        f.write_text(doc, encoding="utf-8")

    n_json = sum(set_json_domain(f, origin) for f in sorted(root.glob("*.json")))

    print(
        f"hydration: {len(pages)} Seiten, page.domain auf {origin} "
        f"({n_dom} Nutzlasten, {n_json} Seiten-JSON), Karte absolut ({n_card}), "
        f"{n_tags} Tags in den Wächtern"
    )
    return check(root, base)


if __name__ == "__main__":
    raise SystemExit(main())
