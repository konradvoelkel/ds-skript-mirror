#!/usr/bin/env python3
"""Die Textdateien des Artefakts vorkomprimieren, damit Pages sie komprimiert ausliefert.

    python3 tools/precompress.py <html-dir>            # .gz-Geschwister schreiben
    python3 tools/precompress.py <html-dir> --check     # nachmessen statt schreiben


Warum ueberhaupt
----------------

GitLab Pages komprimiert nichts von sich aus. Am 2026-10-16 am Live-Stand gemessen: kein
`content-encoding` in der Antwort, auch nicht mit `Accept-Encoding: gzip, deflate, br`,
und im Browser `transferSize` 6.567 kB gegen `decodedBodySize` 6.580 kB -- die Seite geht
unkomprimiert ueber die Leitung, 6,5 MB je Seitenaufruf. Davon sind 4,87 MB JavaScript in
19 modulepreload-Chunks, der groesste 2,19 MB.

Was Pages statt dessen tut, steht in dessen Dokumentation: *vor* dem Ausliefern einer
Datei sieht es nach, ob daneben dieselbe Datei mit der Endung `.br` oder `.gz` liegt, und
liefert die, wenn der Browser die Kodierung akzeptiert. Das ist der ganze Mechanismus --
kein Schalter, keine Konfiguration, nur Dateien, die danebenliegen muessen.

Brotli waere noch einmal 15-20 % besser, braucht aber ein `apk add brotli` im Job
(Pythons Standardbibliothek kann es nicht). Erst messen, was gzip bringt; die Endung `.br`
nachzulegen ist danach eine Zeile.


Die Falle: eine veraltete Kopie ist unsichtbar
----------------------------------------------

Ab jetzt existiert jede Textdatei zweimal. Liegt die `.gz` daneben, ist sie das, was
praktisch jeder Leser bekommt -- Browser schicken alle `Accept-Encoding: gzip`. Eine
`.gz`, die nicht zum Original passt, liefert also die *alte* Seite an alle, waehrend ein
`curl` ohne `Accept-Encoding` und jeder Blick ins Artefakt die neue zeigt. Das ist
derselbe Fehlertyp wie die localhost-Sitemap und die Schriften hinter dem relativen
url(): gruen bei der naheliegenden Pruefung, falsch beim tatsaechlichen Abruf.

Zwei Dinge halten das in Schach:

1. **Dieser Schritt laeuft als letzter** im pages-Job, nach jeder Umschreibung von HTML,
   CSS und JS. Steht er vorher, ist er garantiert falsch.
2. **`--check` packt jede `.gz` wieder aus und vergleicht byteweise** mit dem Original,
   statt nur ihre Existenz zu pruefen. Nur das faellt auf, wenn ein spaeterer Schritt die
   Datei doch noch anfasst.

Zusaetzlich faellt eine `.gz` ohne Original auf: sie ist der Rest eines umbenannten
Fingerprints und ein Zeichen, dass das Artefakt nicht frisch gebaut wurde.


Was ausgelassen wird und warum
------------------------------

- **Alles Binaere**, insbesondere `ds-skript.pdf` (16 MB) und die PNG: schon komprimiert,
  gzip macht sie groesser und kostet nur Artefaktplatz.
- **Dateien unter 1 kB**: bei ihnen entscheidet der Round-Trip, nicht die Nutzlast.
- **Dateien, bei denen gzip nicht kleiner ist.** Dann ist die Abwesenheit der `.gz` die
  richtige Antwort, und `--check` muss sie genauso akzeptieren wie ihr Vorhandensein --
  sonst waere die Pruefung nicht erfuellbar. `--check` komprimiert dafuer selbst nach
  und verlangt eine `.gz` genau dann, wenn sie sich lohnt.

Idempotent: ein zweiter Lauf schreibt Dateien gleichen Inhalts (`mtime=0`, damit das auch
byteweise stimmt und ein Vergleich zweier Laeufe aussagekraeftig ist).
"""

from __future__ import annotations

import argparse
import gzip
import io
import pathlib
import sys

# Textendungen, die im Artefakt vorkommen. ".map" ist dabei, weil MyST Sourcemaps
# mitliefert und sie zu den groessten Einzeldateien gehoeren koennen.
TEXT_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".map",
    ".svg",
    ".json",
    ".txt",
    ".xml",
    ".md",
    ".xsl",
}

MIN_SIZE = 1024


def eligible(path: pathlib.Path) -> bool:
    return (
        path.is_file()
        and not path.is_symlink()
        and path.suffix.lower() in TEXT_SUFFIXES
        and path.stat().st_size >= MIN_SIZE
    )


def squeeze(raw: bytes) -> bytes:
    """gzip, Stufe 9, ohne Zeitstempel -- damit zwei Laeufe byteidentisch sind."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=9, mtime=0) as fh:
        fh.write(raw)
    return buf.getvalue()


def write_mode(root: pathlib.Path) -> int:
    n = kept = 0
    raw_total = gz_total = 0
    for f in sorted(root.rglob("*")):
        if not eligible(f):
            continue
        raw = f.read_bytes()
        gz = squeeze(raw)
        sibling = f.with_name(f.name + ".gz")
        if len(gz) >= len(raw):
            # Kein Gewinn: eine .gz hier waere nur eine zweite Wahrheit ohne Nutzen.
            if sibling.exists():
                sibling.unlink()
            kept += 1
            continue
        sibling.write_bytes(gz)
        n += 1
        raw_total += len(raw)
        gz_total += len(gz)

    if not n:
        print("precompress: keine Datei kam in Frage -- ist das der gebaute Ordner?")
        return 1
    saved = 100 * (1 - gz_total / raw_total)
    print(
        f"precompress: {n} Dateien vorkomprimiert, {raw_total / 1024:.0f} kB -> "
        f"{gz_total / 1024:.0f} kB auf der Leitung ({saved:.0f} % gespart); "
        f"{kept} ohne Gewinn uebersprungen"
    )
    return 0


def check_mode(root: pathlib.Path) -> int:
    problems: list[str] = []
    checked = missing = 0

    for f in sorted(root.rglob("*")):
        if f.suffix == ".gz":
            # Eine .gz ohne Original ist ein Ueberrest, kein Fund.
            if not f.with_name(f.name[:-3]).exists():
                problems.append(f"{f}: .gz ohne Originaldatei (veraltetes Artefakt?)")
            continue
        if not eligible(f):
            continue
        raw = f.read_bytes()
        sibling = f.with_name(f.name + ".gz")
        if not sibling.exists():
            # Erlaubt ist das nur, wenn gzip hier nichts gebracht haette.
            if len(squeeze(raw)) < len(raw):
                missing += 1
                problems.append(f"{f}: keine .gz, obwohl gzip kleiner waere")
            continue
        try:
            back = gzip.decompress(sibling.read_bytes())
        except OSError as exc:  # defekte .gz liefert Pages als Muell aus
            problems.append(f"{sibling}: laesst sich nicht entpacken ({exc})")
            continue
        if back != raw:
            problems.append(
                f"{sibling}: Inhalt weicht vom Original ab "
                f"({len(back)} gegen {len(raw)} Bytes) -- "
                "lief die Vorkompression vor einer Umschreibung?"
            )
            continue
        if len(sibling.read_bytes()) >= len(raw):
            problems.append(f"{sibling}: nicht kleiner als das Original")
            continue
        checked += 1

    if problems:
        print(f"FEHLER: {len(problems)} Problem(e) bei der Vorkompression:")
        for p in problems[:20]:
            print(f"  {p}")
        if len(problems) > 20:
            print(f"  ... und {len(problems) - 20} weitere")
        return 1

    if not checked:
        print("FEHLER: keine einzige vorkomprimierte Datei gefunden")
        return 1
    print(
        f"ok: {checked} vorkomprimierte Dateien, alle entpacken byteidentisch zum Original"
        + (f", {missing} ohne Gewinn" if missing else "")
    )
    return 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html_dir")
    ap.add_argument(
        "--check",
        action="store_true",
        help="nicht schreiben, sondern jede .gz auspacken und mit dem Original vergleichen",
    )
    args = ap.parse_args()

    root = pathlib.Path(args.html_dir)
    if not root.is_dir():
        sys.exit(f"FEHLER: {root} ist kein Verzeichnis")

    sys.exit(check_mode(root) if args.check else write_mode(root))


if __name__ == "__main__":
    main()
