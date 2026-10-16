#!/usr/bin/env python3
"""Das Navbar-Logo aus seiner SVG-Quelle in das Raster rendern, das die Seite ausliefert.

    python3 tools/logo_raster.py            # images/logo-wide.png neu rendern
    python3 tools/logo_raster.py --verify   # was die CI prueft

`images/logo-wide.svg` ist **437 kB** -- einer seiner siebzehn Pfade ist allein 117 kB
Koordinaten -- und wurde auf allen 32 Seiten geladen. Damit war es das groesste einzelne
Artefakt der Seite.

Es ist die Zeichnung eines aufgeschlagenen Buchs. Sie rendert in der Navigation mit
**72 x 36 CSS-Pixeln**, und sonst nirgends und in keiner anderen Groesse: das Theme
schreibt `class="h-9"`, also `height: 2.25rem`, und das gilt in Desktop- und
Mobilbreiten und bei offenem Mobilmenue. 437 kB Bezierkurven fuer ein Daumennagelbild.

Das SVG wird damit das, was es immer haette sein sollen -- die *Quelle* --, und
ausgeliefert wird ein Raster davon. Es bleibt im Repository, und dieses Werkzeug ist das
Bindeglied.

**Auf der Leitung sind das 120.012 zu etwa 18.000 Bytes, also rund 100 kB und 85 Prozent
weniger je Seite, nicht 96 Prozent.** Ein SVG ist Text und wird gzip-komprimiert
ausgeliefert, die zu nennende Zahl ist also die komprimierte; die PNG ist schon
komprimiert, gzip tut daran nichts mehr. Wer 437 kB gegen 18 kB stellt, rechnet sich die
Verbesserung um den Faktor der gzip-Kompression zu gross.


Warum 216 x 108
---------------

Dreimal die 72 x 36, mit denen es rendert -- scharf auf jedem Display, das jemand hat:
ein Telefon mit DPR 3 bildet ein Bildpixel exakt auf ein Geraetepixel ab. Das
Seitenverhaeltnis ist das des SVG selbst, 2:1 (`viewBox="0 0 30 15"`), und **nicht** der
engere Schnitt der alten `images/logo-wide.png`, die ein unreferenzierter 609x417-Schnitt
derselben Zeichnung war. Dem Theme ein anders beschnittenes Bild zu geben haette die
gerenderte Breite des Logos von 72 auf 53 Pixel geaendert, weil die *Hoehe* festgepinnt
ist -- eine Layoutaenderung im Gewand einer Optimierung.

Ein `srcset` mit 1x/2x/3x spaerte auf Bildschirmen mit niedriger DPI ein paar Kilobyte.
Nicht gemacht: das Theme schreibt ein nacktes `<img>`, es waere also noch mehr
Nachbearbeitung am gebauten HTML -- fuer einstellige Kilobytes an einer 18-kB-Datei.


Warum PNG, und warum nicht die kleinere Palette
-----------------------------------------------

Das Logo sitzt auf einer Navbar, deren Farbe der Hell/Dunkel-Einstellung des Lesers
folgt; seine Transparenz ist also tragend. Eine auf Weiss plattgedrueckte Fassung ist im
Dunkelmodus ein weisser Block.

Die Palettenfassung ist ein Drittel der Groesse und behaelt einen funktionierenden
Alphakanal, verschiebt Farben aber um bis zu 36 von 255 Stufen -- und diese Zeichnung hat
Gradienten, der Globus allein drei radiale von insgesamt 42 im SVG. Genau dort zeigt sich
das als Streifenbildung. Fuer das eine Bild, das die Marke des Buchs ist, auf jeder
Seite, ist Exaktheit die zwoelf Kilobyte wert. Reines RGBA ist exakt.


Warum --verify und nicht --check
--------------------------------

`tools/course_diagram.py` haelt einen byte-exakten `--check`, weil es sein SVG als Text
*schreibt* und damit ueberall reproduzierbar ist. Diese Datei wird *gerendert*, von
librsvg oder Inkscape, gegen die Versionen von cairo und die Systemschriften, die eine
Maschine gerade hat. Ein byte-exakter Vergleich in der CI waere eine Pruefung, die aus
Gruenden scheitert, die mit dem Logo nichts zu tun haben.

Die CI prueft deshalb die Eigenschaften, die wirklich zaehlen und ueber die kein Renderer
anderer Meinung sein kann: dass die Datei da ist, dass sie eine 216x108-PNG ist, dass ihr
PNG-Farbtyp Transparenz ueberhaupt tragen kann, und dass ihr Seitenverhaeltnis noch zum
viewBox des SVG passt. Ein zu kleines, plattgedruecktes oder falsch geschnittenes Logo
ist der Fehler, den das abfaengt.

Der IHDR wird mit der Standardbibliothek gelesen, nicht mit Pillow: ein Waechter, der
eine Abhaengigkeit braucht, um "die Datei hat die richtige Form" zu sagen, berichtet im
Zweifel ueber sein eigenes Setup statt ueber das Bild.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

SVG = pathlib.Path("images/logo-wide.svg")
PNG = pathlib.Path("images/logo-wide.png")

# Das Theme pinnt height: 2.25rem = 36px, das Logo rendert also mit 72x36 CSS-Pixeln.
DISPLAY = (72, 36)
SCALE = 3
WIDTH, HEIGHT = DISPLAY[0] * SCALE, DISPLAY[1] * SCALE


def svg_aspect(path: pathlib.Path) -> float:
    m = re.search(r'viewBox="([\d.\s-]+)"', path.read_text(encoding="utf-8"))
    if not m:
        sys.exit(f"FEHLER: {path} hat kein viewBox; Seitenverhaeltnis nicht pruefbar")
    _, _, w, h = (float(v) for v in m.group(1).split())
    return w / h


def render() -> None:
    if not SVG.exists():
        sys.exit(f"FEHLER: {SVG} fehlt; das ist die Quelle, aus der gerendert wird")

    aspect = svg_aspect(SVG)
    if abs(aspect - WIDTH / HEIGHT) > 0.01:
        sys.exit(
            f"FEHLER: {SVG} ist {aspect:.3f}:1, das Raster aber {WIDTH / HEIGHT:.3f}:1. "
            "Weil die Hoehe gepinnt ist, aendert ein anderes Seitenverhaeltnis die "
            "gerenderte Breite; DISPLAY in dieser Datei anpassen, nicht die Zeichnung "
            "stauchen."
        )

    if shutil.which("rsvg-convert"):
        cmd = ["rsvg-convert", "-w", str(WIDTH), "-h", str(HEIGHT), "-o", str(PNG), str(SVG)]
    elif shutil.which("inkscape"):
        cmd = ["inkscape", "-w", str(WIDTH), "-h", str(HEIGHT), "-o", str(PNG), str(SVG)]
    else:
        sys.exit(
            "FEHLER: kein SVG-Renderer gefunden. librsvg2-bin (rsvg-convert) oder "
            "inkscape installieren. Dieses Werkzeug laeuft nicht in der CI -- die PNG "
            "ist eingecheckt --, das muss also nur auf der Maschine gelten, die das Logo "
            "neu erzeugt."
        )

    subprocess.run(cmd, check=True, capture_output=True)

    from PIL import Image

    with Image.open(PNG) as im:
        im = im.convert("RGBA")
        im.save(PNG, "PNG", optimize=True)

    print(
        f"✓ {PNG} aus {SVG} gerendert, {WIDTH}x{HEIGHT} "
        f"({PNG.stat().st_size:,} Bytes, aus {SVG.stat().st_size:,} als SVG) "
        f"mit {cmd[0]}"
    )


def png_header(data: bytes) -> tuple[int, int, int]:
    """(Breite, Hoehe, Farbtyp) aus dem IHDR, nur mit der Standardbibliothek."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("keine PNG")
    if data[12:16] != b"IHDR":
        raise ValueError("kein IHDR dort, wo eine PNG ihn haben muss")
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    return w, h, data[25]


def verify() -> None:
    if not PNG.exists():
        sys.exit(f"FEHLER: {PNG} fehlt; tools/logo_raster.py laufen lassen")

    data = PNG.read_bytes()
    try:
        w, h, colour_type = png_header(data)
    except ValueError as exc:
        sys.exit(f"FEHLER: {PNG}: {exc}")

    if (w, h) != (WIDTH, HEIGHT):
        sys.exit(
            f"FEHLER: {PNG} ist {w}x{h}, erwartet {WIDTH}x{HEIGHT} -- die Navbar rendert "
            f"es mit {DISPLAY[0]}x{DISPLAY[1]}, eine kleinere Datei ist auf einem "
            "High-DPI-Bildschirm sichtbar weich."
        )

    # Farbtyp 4 und 6 tragen einen Alphakanal; 3 (Palette) kann Transparenz in einem
    # tRNS-Chunk tragen. Typ 0 und 2 koennen gar nicht transparent sein -- und genau das
    # erzeugt ein Plattdruecken auf Weiss, das im Dunkelmodus ein weisser Block ist.
    # Das sagt, dass die Datei transparent sein *kann*, nicht dass jedes Pixel stimmt;
    # letzteres braeuchte einen Dekoder, und der Fehler, der wirklich lohnt, ist der
    # platte Hintergrund.
    if colour_type not in (4, 6) and not (colour_type == 3 and b"tRNS" in data[:4096]):
        sys.exit(
            f"FEHLER: {PNG} hat PNG-Farbtyp {colour_type} und kann keine Transparenz "
            "tragen. Die Navbar wechselt mit der Hell/Dunkel-Einstellung des Lesers die "
            "Farbe; ein plattgedruecktes Logo ist in einer der beiden ein Block."
        )

    if SVG.exists():
        aspect = svg_aspect(SVG)
        if abs(aspect - WIDTH / HEIGHT) > 0.01:
            sys.exit(
                f"FEHLER: {SVG} ist jetzt {aspect:.3f}:1, {PNG} aber "
                f"{WIDTH / HEIGHT:.3f}:1. Die Quelle wurde in anderer Form neu "
                "gezeichnet; das Raster neu rendern."
            )

    print(f"✓ {PNG} ist eine {WIDTH}x{HEIGHT}-PNG, die Transparenz tragen kann ({len(data):,} Bytes)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="die eingecheckte PNG pruefen, nichts rendern")
    args = ap.parse_args()
    verify() if args.verify else render()


if __name__ == "__main__":
    main()
