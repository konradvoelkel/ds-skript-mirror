#!/usr/bin/env python3
"""Jede Abbildung bekommt ihre echten Pixelmasse als width/height ins Markup.

    python3 tools/image_dims.py <html-dir> [--base BASE_URL] [--check]

Gegen den Layoutsprung: ohne width/height kennt der Browser das Seitenverhaeltnis
einer Abbildung erst, wenn ihre ersten Bytes da sind. Bis dahin ist sie null Pixel
hoch, und in dem Moment, in dem der Header gelesen ist, ruckt der ganze Text darunter
nach unten. Ein Kapitel mit sechzehn Matplotlib-Bildern ruckt sechzehnmal. Mit beiden
Attributen rechnet der Browser aus ihnen `aspect-ratio` und haelt den Platz von Anfang
an frei -- das ist der ganze Mechanismus, und er braucht *beide* Werte, ein einzelnes
ist wertlos.

Die Masse stehen **nirgends gepflegt**, anders als bei den alt-Texten (alt-texte.yml):
sie stehen in der Bilddatei selbst, im Header. Also werden sie dort gelesen. Eine
Pflegedatei waere hier nur eine zweite Wahrheit, die veralten kann.


Warum Markup reicht und kein Waechter noetig ist
------------------------------------------------

Der <head> dieses Themes wird bei der Hydration neu gerendert, nachgetragene Tags sind
danach weg (tools/hydration.py). Fuer <main> gilt das **nicht**, und das ist gemessen,
nicht angenommen: am 2026-10-29 lokal gegen dasselbe Bundle ein Bild in kmeans mit
width/height und einem Erkennungsattribut versehen, ausgeliefert, im Browser
nachgesehen -- nach der Hydration da, nach einem Zustandswechsel von React (Umschalten
auf das dunkle Thema) da, nach Scrollen da. React korrigiert ein zusaetzliches Attribut
am hydrierten Knoten nicht.

Ein Kapitelwechsel laedt ohnehin ein neues Dokument: am selben Tag nachgemessen, ein
Klick auf einen Kapitellink im Seitenstreifen erzeugt einen navigation-Eintrag in der
Performance-Zeitleiste und loescht eine zuvor gesetzte Variable am window. Das Markup
ist also bei jedem Seitenaufruf frisch vom Server -- derselbe Befund rechtfertigt
nebenbei das loading="lazy" aus head_meta.py, das seit dem 2026-10-16 ungemessen lief.


Was uebersprungen wird, und warum das keine Vorsicht ist, sondern Messung
-------------------------------------------------------------------------

Das width-Attribut ist kein blosser Hinweis: es wirkt als CSS-Eigenschaft (presentational
hint) und setzt die Breite. Solange die Hoehe `auto` ist -- und das ist sie, das Theme
hat `img, video { max-width: 100%; height: auto; }` --, folgt die Hoehe dem echten
Seitenverhaeltnis, und das Bild sieht aus wie vorher. Schreibt aber *CSS* eine feste
Hoehe und laesst die Breite frei, dann gewinnt die CSS-Hoehe, die Attribut-Breite
gewinnt gegen `auto`, und das Bild wird verzerrt.

Am 2026-10-29 im Browser vorgefuehrt, mit absichtlich falschen Massen 640x480:

- Abbildung ohne eigenes CSS: vorher 536x585 gerendert, nachher 640x699 -- unverzerrt,
  Verhaeltnis gehalten. Mit den **echten** Massen bleibt die Breite 536, es aendert
  sich also nichts am Bild; nur der Platz wird vorher freigehalten.
- Der Lizenzknopf der Landingpage, `style="height:20px"`: vorher rund 107x20, nachher
  **640x19**. Breitgezogen ueber die halbe Seite.

Deshalb zwei Ausnahmen, beide am Markup erkennbar:

1. **Hoehe im style-Attribut** -- der Lizenzknopf. Eine Breite im style ist dagegen
   harmlos (`width:100%` am Kursdiagramm): sie gewinnt gegen den Hinweis, die Hoehe
   bleibt auto, das Verhaeltnis kommt aus den Attributen.
2. **width oder height schon gesetzt** -- das Logo der Navigation traegt
   `height="2.25rem"` vom Theme. Das ist als HTML-Attribut ungueltig (dort stehen
   Pixelzahlen, keine CSS-Laengen) und wird vom Browser ignoriert; eine Breite
   dazuzuschreiben wuerde es aber gueltig machen und das Logo auf 216 Pixel ziehen,
   waehrend die Klasse h-9 die Hoehe bei 36 haelt. Das Logo steht ohnehin ausserhalb
   von <main> und wird hier nie angefasst.

Nur die <main>-Scheibe wird umgeschrieben, aus demselben Grund wie in head_meta.py: der
Rest des Dokuments traegt MySTs Hydrations-Nutzlast, die ganze Seite noch einmal als
JSON, und ein freilaufender regulaerer Ausdruck darauf aendert Daten statt Markup.


Zweimal laufen
--------------

Idempotent: ein Bild, das die Attribute schon fuehrt, faellt unter Ausnahme 2 und wird
nicht noch einmal angefasst. `--check` ist die Nachbedingung am gebauten Artefakt und
prueft nicht, was dieser Lauf getan hat, sondern was am Ende dasteht -- jedes Bild in
<main> traegt entweder beide Attribute mit den Massen seiner Datei, oder es faellt unter
eine der zwei Ausnahmen. Ein Bild mit falschen Massen ist dabei der eigentliche
Fehlerfall: es haelt Platz frei, nur den falschen, und ruckt damit genauso.

Die Masse kommen aus dem Dateikopf, nicht aus einer Bibliothek: Pillow ist im Image des
Jobs (python:3.13-alpine) nicht da, und vier Formate von Hand zu lesen ist weniger
Angriffsflaeche als eine Abhaengigkeit dafuer einzufuehren. Ein unbekanntes Format
bricht ab, statt stillschweigend ohne Masse durchzulaufen.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import struct
import sys
from urllib.parse import unquote, urlparse

IMG_TAG = re.compile(r"<img\b[^>]*?/?>", re.I)
MAIN = re.compile(r"<main\b[^>]*>.*?</main>", re.S | re.I)


# --- Die Masse aus dem Dateikopf lesen ---------------------------------------------


def png_masse(data: bytes) -> tuple[int, int]:
    """IHDR steht immer zuerst und immer an derselben Stelle: Breite und Hoehe als
    32-Bit-Zahlen ab Byte 16."""
    if len(data) < 24 or data[12:16] != b"IHDR":
        raise ValueError("PNG ohne IHDR an der erwarteten Stelle")
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def gif_masse(data: bytes) -> tuple[int, int]:
    if len(data) < 10:
        raise ValueError("GIF zu kurz fuer den Bildschirm-Deskriptor")
    w, h = struct.unpack("<HH", data[6:10])
    return w, h


def jpeg_masse(data: bytes) -> tuple[int, int]:
    """Durch die Marker laufen, bis ein SOF-Segment kommt; dort stehen Hoehe und Breite.

    Die Laengen der uebersprungenen Segmente stehen im Segment selbst, geraten wird
    nichts. SOF4, SOF8 und SOF12 sind keine Rahmen-Marker und werden ausgelassen.
    """
    i = 2  # die beiden Bytes des SOI-Markers
    while i + 3 < len(data):
        if data[i] != 0xFF:
            raise ValueError(f"JPEG: kein Marker an Position {i}")
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        laenge = struct.unpack(">H", data[i + 2 : i + 4])[0]
        if marker in (0xC4, 0xC8, 0xCC):
            pass
        elif 0xC0 <= marker <= 0xCF:
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return w, h
        i += 2 + laenge
    raise ValueError("JPEG ohne SOF-Segment")


def svg_masse(text: str) -> tuple[int, int]:
    """width/height am Wurzelelement, sonst die letzten zwei Zahlen der viewBox.

    Prozentangaben taugen nicht als Attribut (sie sind keine Pixelzahl), deshalb
    faellt der Fall auf die viewBox zurueck -- genau die Form, die Matplotlib und
    unser eigenes Kursdiagramm schreiben.
    """
    m = re.search(r"<svg\b[^>]*>", text, re.I | re.S)
    if not m:
        raise ValueError("SVG ohne <svg>-Element")
    wurzel = m.group(0)

    def laenge(name: str) -> float | None:
        a = re.search(rf'\b{name}="([^"]+)"', wurzel, re.I)
        if not a:
            return None
        z = re.fullmatch(r"\s*([0-9.]+)(px|pt)?\s*", a.group(1))
        return float(z.group(1)) if z else None

    w, h = laenge("width"), laenge("height")
    if w is None or h is None:
        vb = re.search(r'\bviewBox="([^"]+)"', wurzel, re.I)
        if not vb:
            raise ValueError("SVG ohne brauchbare width/height und ohne viewBox")
        teile = re.split(r"[\s,]+", vb.group(1).strip())
        if len(teile) != 4:
            raise ValueError(f"SVG mit unlesbarer viewBox: {vb.group(1)!r}")
        w, h = float(teile[2]), float(teile[3])
    return round(w), round(h)


def masse(pfad: pathlib.Path) -> tuple[int, int]:
    """Nach der Signatur unterscheiden, nicht nach der Endung: eine falsch benannte
    Datei soll als das gelesen werden, was sie ist."""
    data = pfad.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = png_masse(data)
    elif data[:6] in (b"GIF87a", b"GIF89a"):
        w, h = gif_masse(data)
    elif data[:2] == b"\xff\xd8":
        w, h = jpeg_masse(data)
    elif b"<svg" in data[:2048].lower():
        w, h = svg_masse(data.decode("utf-8", "replace"))
    else:
        raise ValueError(f"unbekanntes Bildformat (erste Bytes: {data[:8]!r})")
    if w <= 0 or h <= 0:
        raise ValueError(f"unbrauchbare Masse {w}x{h}")
    return w, h


# --- Vom src zur Datei --------------------------------------------------------------


def quelle(src: str, seite: pathlib.Path, root: pathlib.Path, base: str) -> pathlib.Path | None:
    """Die Datei zu einem src, oder None, wenn sie nicht auf diesem Server liegt."""
    teil = urlparse(src)
    if teil.scheme or teil.netloc:  # http(s):, data:, //fremder.host
        return None
    pfad = unquote(teil.path)
    if not pfad:
        return None
    if pfad.startswith("/"):
        if base and pfad.startswith(base + "/"):
            pfad = pfad[len(base) :]
        return root / pfad.lstrip("/")
    return seite.parent / pfad


# --- Das Markup --------------------------------------------------------------------


def ausnahme(tag: str) -> str | None:
    """Der Grund, aus dem dieses <img> nicht vermasst wird -- oder None."""
    if re.search(r"\b(width|height)=", tag, re.I):
        return "Masse schon gesetzt"
    stil = re.search(r'\bstyle="([^"]*)"', tag, re.I)
    if stil and re.search(r"(^|[;\s])height\s*:", stil.group(1), re.I):
        return "Hoehe im style"
    return None


def mit_massen(tag: str, w: int, h: int) -> str:
    """Die zwei Attribute ans Ende des Tags, vor dem schliessenden Winkel.

    Der abschliessende Schraegstrich von `<img ... />` muss dabei *hinter* den neuen
    Attributen bleiben. Steht er davor, liest ein Parser ihn als Attributnamen: das
    ergibt `... alt="x"/ width="536">`, was Browser zwar verzeihen, ein Validator aber
    nicht -- genau das stand seit dem 2026-10-16 im ausgelieferten HTML, weil
    head_meta.py das loading-Attribut so angehaengt hat.
    """
    kern = tag[:-1].rstrip()
    schraeg = ""
    if kern.endswith("/"):
        kern, schraeg = kern[:-1].rstrip(), "/"
    return f'{kern} width="{w}" height="{h}"{schraeg}>'


def vermassen(
    doc: str, seite: pathlib.Path, root: pathlib.Path, base: str
) -> tuple[str, int, dict[str, int]]:
    """Die <main>-Scheibe umschreiben. Gibt Dokument, Anzahl und Ausnahmen zurueck."""
    m = MAIN.search(doc)
    if not m:
        sys.exit(f"FEHLER: {seite} hat kein <main>; nach dem HTML-Bau laufen lassen")

    gesetzt = 0
    uebersprungen: dict[str, int] = {}

    def img_sub(treffer: re.Match) -> str:
        nonlocal gesetzt
        tag = treffer.group(0)
        if (grund := ausnahme(tag)) is not None:
            uebersprungen[grund] = uebersprungen.get(grund, 0) + 1
            return tag
        src = re.search(r'\bsrc="([^"]*)"', tag, re.I)
        if not src:
            sys.exit(f"FEHLER: {seite} hat ein <img> ohne src: {tag[:80]}")
        datei = quelle(src.group(1), seite, root, base)
        if datei is None:
            uebersprungen["fremde Herkunft"] = uebersprungen.get("fremde Herkunft", 0) + 1
            return tag
        if not datei.exists():
            sys.exit(f"FEHLER: {seite} verweist auf {src.group(1)}, aber {datei} fehlt")
        try:
            w, h = masse(datei)
        except ValueError as e:
            sys.exit(f"FEHLER: {datei} (aus {seite}): {e}")
        gesetzt += 1
        return mit_massen(tag, w, h)

    neu = IMG_TAG.sub(img_sub, m.group(0))
    return doc[: m.start()] + neu + doc[m.end() :], gesetzt, uebersprungen


def pruefen(doc: str, seite: pathlib.Path, root: pathlib.Path, base: str) -> int:
    """Nachbedingung: jedes <img> in <main> traegt die Masse seiner Datei oder faellt
    unter eine der zwei Ausnahmen. Gibt die Zahl der geprueften Bilder zurueck."""
    m = MAIN.search(doc)
    if not m:
        sys.exit(f"FEHLER: {seite} hat kein <main>")

    geprueft = 0
    for tag in IMG_TAG.findall(m.group(0)):
        stil = re.search(r'\bstyle="([^"]*)"', tag, re.I)
        if stil and re.search(r"(^|[;\s])height\s*:", stil.group(1), re.I):
            continue
        # Eine CSS-Laenge als Attribut ("2.25rem", wie das Theme sie ans Logo schreibt)
        # ist nichts, was dieses Skript je geschrieben haette, und der Schreiblauf fasst
        # so ein Bild nicht an. Ohne diese Zeile waere die Pruefung dafuer dauerhaft rot,
        # ohne dass ein Lauf sie heilen koennte -- derselbe Riegel, an dem head_meta.py
        # schon einmal haengengeblieben ist.
        fremd = [
            t for t in re.findall(r'\b(?:width|height)="([^"]*)"', tag, re.I)
            if not t.isdigit()
        ]
        if fremd:
            continue
        src = re.search(r'\bsrc="([^"]*)"', tag, re.I)
        datei = quelle(src.group(1), seite, root, base) if src else None
        if datei is None:
            continue
        w_attr = re.search(r'\bwidth="(\d+)"', tag, re.I)
        h_attr = re.search(r'\bheight="(\d+)"', tag, re.I)
        if not (w_attr and h_attr):
            sys.exit(
                f"FEHLER: {seite} hat ein <img> ohne beide Masse: {src.group(1)} -- "
                f"ohne width *und* height haelt der Browser keinen Platz frei"
            )
        if not datei.exists():
            sys.exit(f"FEHLER: {seite} verweist auf {src.group(1)}, aber {datei} fehlt")
        w, h = masse(datei)
        if (int(w_attr.group(1)), int(h_attr.group(1))) != (w, h):
            sys.exit(
                f"FEHLER: {seite} gibt fuer {src.group(1)} "
                f"{w_attr.group(1)}x{h_attr.group(1)} an, die Datei ist {w}x{h} -- "
                f"falsche Masse halten den falschen Platz frei"
            )
        geprueft += 1
    return geprueft


def main() -> None:
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
    base = "/" + args.base.strip("/") if args.base.strip("/") else ""
    seiten = sorted(root.rglob("index.html"))
    if not seiten:
        sys.exit(f"FEHLER: unter {root} liegt keine index.html; nach dem HTML-Bau laufen lassen")

    if args.check:
        geprueft = sum(
            pruefen(f.read_text(encoding="utf-8"), f, root, base) for f in seiten
        )
        if not geprueft:
            sys.exit(
                "FEHLER: kein einziges Bild geprueft -- entweder ist <main> leer oder "
                "die src-Pfade zeigen nicht mehr auf dieses Artefakt"
            )
        print(f"image_dims --check: {len(seiten)} Seiten, {geprueft} Abbildungen mit "
              f"den Massen ihrer Datei")
        return

    gesamt = 0
    uebersprungen: dict[str, int] = {}
    for f in seiten:
        doc = f.read_text(encoding="utf-8")
        neu, n, aus = vermassen(doc, f, root, base)
        if neu != doc:
            f.write_text(neu, encoding="utf-8")
        gesamt += n
        for grund, k in aus.items():
            uebersprungen[grund] = uebersprungen.get(grund, 0) + k

    geprueft = sum(pruefen(f.read_text(encoding="utf-8"), f, root, base) for f in seiten)
    rest = ", ".join(f"{k} {g}" for g, k in sorted(uebersprungen.items())) or "keine"
    print(
        f"image_dims: {len(seiten)} Seiten, {gesamt} Abbildungen vermasst, "
        f"{geprueft} tragen die Masse ihrer Datei; uebersprungen: {rest}"
    )


if __name__ == "__main__":
    main()
