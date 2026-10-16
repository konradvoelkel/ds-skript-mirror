#!/usr/bin/env python3
"""Die PNG des Buchs an Ort und Stelle neu kodieren und die ueberbreiten Quellen kappen.

    python3 tools/optimize_images.py images/ --max-width 1600
    python3 tools/optimize_images.py _build/html/build       # CI: nur neu kodieren
    python3 tools/optimize_images.py images/ --max-width 1600 --check

Gemessen am gebauten Stand, 2026-10-16: 199 PNG, **21,2 MB**. Die groesste einzelne ist
`ds-process-oneill.png` mit 5,79 MB, angezeigt wird sie mit 480 px Breite.


Warum es ueberhaupt etwas zu holen gibt
---------------------------------------

Matplotlib speichert RGBA. Ein Plot hat keine Transparenz, von der zu reden waere --
`savefig` schreibt einen deckend weissen Hintergrund --, aber der vierte Kanal ist
trotzdem da, und PNGs Filter komprimieren vier Kanaele deutlich schlechter als einen.
Dazu ist ein Plot eine Handvoll flaecher Farben und etwas kantengeglaetteter Text. Als
Palettenbild gespeichert ist das keine Annaeherung, sondern dasselbe Bild in einem Byte
je Pixel statt in vier.

Die Umformung ist also: den Alphakanal fallen lassen, wenn er nachweislich unbenutzt
ist, dann als 256-Farben-Palette speichern, wenn das entweder exakt verlustfrei oder
messbar nahe dran ist. Sonst aendert sich nichts an der Datei -- gleicher Name, gleiche
Abmessungen, fuer das Auge gleiche Pixel.


Was nie angefasst wird
----------------------

**Bilder, deren Alphakanal wirklich benutzt wird.** Die Seite folgt der
Hell/Dunkel-Einstellung des Lesers, und eine Abbildung mit transparentem Hintergrund ist
eine, die *gezeichnet* wurde, um auf beidem zu sitzen. Sie auf Weiss plattzudruecken
sieht im Build richtig aus und auf der Haelfte der Maschinen falsch, die sie geoeffnet
haben.

Diese Unterscheidung wird gemessen, nicht angenommen: das Minimum des Alphakanals ist
255 oder es ist es nicht, und nur der erste Fall wird plattgedrueckt. Auf den *Modus* zu
schauen genuegt nicht -- Matplotlib schreibt RGBA auch dort, wo nichts transparent ist.


Das Qualitaetstor
-----------------

Ein Bild mit 256 Farben oder weniger wandelt sich *exakt* in eine Palette, und das
Werkzeug behauptet das nicht, sondern prueft es: es vergleicht jedes Pixel und verwirft
das Ergebnis, wenn ein einziges sich bewegt hat. Keine Schwelle, kein Ermessen.

Ueber 256 Farben ist die Wandlung eine Annaeherung, wird also gemessen und verriegelt:
mittlerer absoluter Fehler <= 1,5/255 und 99,9-Perzentil <= 40/255, ueber alle drei
Kanaele. Echte Abbildungen liegen bei 0,2 bis 0,8 im Mittel, weit innerhalb; eine glatte
Farbkarte, die merklich Streifen zeigen wuerde, liegt darueber und behaelt ihre
Vollfarbkodierung. Ein Kandidat, der durchfaellt oder nicht wirklich kleiner ist, wird
verworfen und das Original stattdessen verlustfrei neu komprimiert.


--max-width, und warum nur fuer die Quellen
-------------------------------------------

`images/` haelt handgemachte Abbildungen in der Groesse, in der sie gezeichnet oder
gescannt wurden. Die Breite zu kappen kostet nichts, was auf dem Bildschirm zu sehen
waere, und liegt immer noch weit ueber dem, was das PDF braucht: 1600 px ueber eine
textbreite Abbildung sind im Druck ueber 300 dpi.

Notebook-Ausgaben bekommen **keine** Kappung. Matplotlib hat die in der Figurengroesse
geschrieben, die das Notebook verlangt hat, sie kommen also etwa in Anzeigegroesse an;
sie herunterzurechnen hiesse, einen Plot schlecht neu zu rendern statt ein Bild gut zu
komprimieren.

**Die Notebooks selbst werden nicht angefasst.** Die eingebetteten base64-Ausgaben
bleiben, wie sie sind; MyST schreibt sie beim Bauen als Dateien nach `build/`, und dort
laeuft dieses Werkzeug. Das ist der Grund, warum der Gewinn ohne eine einzige Aenderung
an den 15 Notebooks mit Bildausgaben zu haben ist -- und warum ein Neuausfuehren eines
Notebooks hier nichts kaputt macht.


--check
-------

Meldet, was noch zu holen waere, und endet mit 1, wenn etwas uebrig ist. Das ist der
Waechter fuer das eingecheckte `images/`: er kodiert das Repository nicht hinter dem
Ruecken neu, sondern scheitert und sagt, dass das Werkzeug zu laufen hat. Auf dem
Build-Verzeichnis laeuft die CI einfach die Optimierung, weil diese Ausgabe erzeugt und
nicht begutachtet wird.


Warum nicht WebP, was besser waere
----------------------------------

WebP mit q82 ist deutlich kleiner. Nicht gemacht, weil sich dafuer der Dateiname aendern
muesste, und der Name steht zweimal je Seite: einmal im <img> und einmal in
`window.__remixContext`, der Hydrations-Nutzlast, die die ganze Seite noch einmal als
JSON haelt. Beide umzuschreiben ist moeglich; es falsch zu machen heisst, die
servergerenderte Seite ist richtig und die hydrierte liefert fuer jede Abbildung 404 --
unsichtbar fuer einen Crawler und offensichtlich fuer einen Leser. Die sichere Haelfte
des Gewinns braucht gar kein Umschreiben von Referenzen, also kommt sie zuerst.
"""

from __future__ import annotations

import argparse
import io
import pathlib
import re
import sys

import numpy as np
from PIL import Image

MAE_LIMIT = 1.5
P999_LIMIT = 40.0
MAX_COLOURS = 256

# Eine Neukodierung muss ihren Commit verdienen. Die Palettenwandlung ueber ein Bild zu
# fahren, das schon ein Palettenbild ist, schabt eine Handvoll Bytes ab -- die adaptive
# Palette kommt in etwas anderer Reihenfolge heraus --, und ohne Untergrenze wuerde das
# Werkzeug bei jedem Lauf jede Datei neu schreiben und `--check` niemals gruen werden.
# Ein Waechter, der nicht zu befriedigen ist, bringt Leute dazu, ihn zu ignorieren.
# Unter der Grenze bleibt die Datei exakt, wie sie ist -- das macht das Werkzeug auch
# idempotent.
MIN_GAIN_BYTES = 2048
MIN_GAIN_RATIO = 0.02

# Artwork, das ein Erzeuger besitzt und das ein Erzeuger byteweise prueft.
#
# social_card.py --check vergleicht die eingecheckte Karte mit einer frisch gerenderten.
# Sie hier neu zu kodieren laesst diese Pruefung die Karte als veraltet melden, und die
# naheliegende Antwort -- den Erzeuger neu laufen lassen -- macht die Optimierung
# stillschweigend wieder zunichte. Dass der Erzeuger die einzige Quelle der Wahrheit
# fuer seine eigene Ausgabe bleibt, ist mehr wert als die Bytes, und eine Pruefung, die
# falschen Alarm schlaegt, ist weniger als nichts wert.
#
# logo-wide.png steht hier absichtlich NICHT, obwohl logo_raster.py sie erzeugt: ihr
# Alphakanal ist wirklich in Benutzung, sie erreicht den Palettenzweig also nie, und
# reines Neukomprimieren bleibt unter der Untergrenze oben. Am 2026-10-16 nachgeprueft.
# course-structure.svg hat dieselbe Lage, ist aber kein PNG und kommt hier nie an.
GENERATED = {"social-card.png"}


def unfingerprint(name: str) -> str:
    """'social-card-<32 hex>.png' -> 'social-card.png'; alles andere unveraendert."""
    return re.sub(r"-[0-9a-f]{32}(\.png)$", r"\1", name)


def encode(im: Image.Image) -> bytes:
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def alpha_is_used(im: Image.Image) -> bool:
    if im.mode not in ("RGBA", "LA", "PA"):
        return False
    if im.mode == "PA":
        return True
    return im.getchannel("A").getextrema()[0] < 255


def best_encoding(im: Image.Image) -> tuple[bytes, str]:
    """Kleinste zulaessige PNG fuer dieses Bild, und ein Wort fuer das Getane."""
    keep_alpha = alpha_is_used(im)
    base = im if keep_alpha else im.convert("RGB")
    candidates = [(encode(base), "neu komprimiert")]

    if not keep_alpha:
        pal = base.convert("P", palette=Image.ADAPTIVE, colors=MAX_COLOURS)
        before = np.asarray(base, dtype=np.int16)
        after = np.asarray(pal.convert("RGB"), dtype=np.int16)
        diff = np.abs(before - after)

        colours = base.getcolors(maxcolors=MAX_COLOURS)
        if colours is not None:
            # <= 256 Farben: die Palette haelt jede einzelne, das muss also Pixel fuer
            # Pixel identisch sein. Ist es das nicht, stimmt etwas an der Annahme nicht
            # und das Ergebnis wird verworfen, nicht geglaubt.
            if not diff.any():
                candidates.append((encode(pal), "Palette (verlustfrei)"))
        elif diff.mean() <= MAE_LIMIT and np.percentile(diff, 99.9) <= P999_LIMIT:
            candidates.append((encode(pal), f"Palette (mae {diff.mean():.2f})"))

    return min(candidates, key=lambda c: len(c[0]))


def process(path: pathlib.Path, max_width: int | None, dry_run: bool) -> tuple[int, int, str]:
    """Gibt (Bytes vorher, Bytes nachher, Notiz) zurueck."""
    before = path.stat().st_size
    with Image.open(path) as im:
        im.load()
        note = ""

        if max_width and im.width > max_width:
            h = round(im.height * max_width / im.width)
            im = im.resize((max_width, h), Image.LANCZOS)
            note = f"{max_width}px"

        data, how = best_encoding(im)

    note = f"{note}, {how}" if note else how
    gain = before - len(data)
    if gain < MIN_GAIN_BYTES or gain < before * MIN_GAIN_RATIO:
        return before, before, note  # nicht wert, die Datei dafuer neu zu schreiben
    if not dry_run:
        path.write_bytes(data)
    return before, len(data), note


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--max-width", type=int, default=None)
    ap.add_argument(
        "--check",
        action="store_true",
        help="melden und mit 1 enden, wenn noch etwas zu holen ist; nichts aendern",
    )
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    files: list[pathlib.Path] = []
    for p in args.paths:
        path = pathlib.Path(p)
        files += sorted(path.rglob("*.png")) if path.is_dir() else [path]

    # MyST versieht Artefaktnamen mit einem Fingerabdruck, die Karte heisst also
    # social-card.png in images/ und social-card-<32 hex>.png im Build. Dieselbe Datei.
    skipped = [f for f in files if unfingerprint(f.name) in GENERATED]
    files = [f for f in files if unfingerprint(f.name) not in GENERATED]
    for f in skipped:
        print(f"  uebersprungen {f.name}: erzeugtes Artwork, siehe GENERATED in dieser Datei")

    total_before = total_after = 0
    shrunk: list[tuple[str, int, int, str]] = []

    for f in files:
        try:
            before, after, note = process(f, args.max_width, args.check)
        except Exception as exc:  # eine kaputte oder exotische PNG darf den Bau nicht faellen
            print(f"WARNUNG: {f}: {exc}")
            continue
        total_before += before
        total_after += after
        if after < before:
            shrunk.append((str(f), before, after, note))

    if not args.quiet:
        for name, b, a, note in sorted(shrunk, key=lambda r: r[1] - r[2], reverse=True)[:12]:
            print(f"  {b:>9,} -> {a:>9,}  ({100 - 100 * a / b:>2.0f}%)  {note:24} {name}")

    saved = total_before - total_after
    verb = "zu holen" if args.check else "gespart"
    print(
        f"optimize_images: {len(files)} PNG, {len(shrunk)} verbessert, "
        f"{saved / 1048576:.1f} MB von {total_before / 1048576:.1f} MB {verb} "
        f"({100 * saved / total_before:.0f}%)"
        if total_before
        else "optimize_images: keine PNG gefunden"
    )

    if args.check and shrunk:
        print(
            "FEHLER: die Bilder sind nicht optimiert; "
            f"`python3 tools/optimize_images.py {' '.join(args.paths)}"
            + (f" --max-width {args.max_width}" if args.max_width else "")
            + "` laufen lassen und das Ergebnis committen"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
