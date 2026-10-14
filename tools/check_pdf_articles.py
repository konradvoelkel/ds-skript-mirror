#!/usr/bin/env python3
"""Prüft, dass die Artikelliste des PDF-Exports zur toc des Projekts passt.

Warum es dieses Skript gibt: In `myst.yml` steht die Buchstruktur zweimal. Einmal als
`project.toc` (sie bestimmt die Web-Ausgabe) und einmal als `project.exports[].articles`
(sie bestimmt das PDF). Die Dopplung ist nicht schön, aber nötig: Ohne eine ausdrückliche
Artikelliste nimmt MyST einfach die ganze toc und lässt nur deren ersten Eintrag weg — es gibt
keine Möglichkeit, eine *einzelne* Seite vom PDF auszunehmen (weder per Frontmatter noch per
`exclude`, und eine Seite aus der toc zu nehmen heißt, dass sie auch im HTML nicht gebaut wird).
Setzt man die Artikelliste, muss man die Teil-Überschriften mit `title`/`level` selbst
nachbauen, sonst verliert das PDF seine Gliederung.

Die Gefahr dabei ist genau die, die dieses Buch schon einmal getroffen hat: Das PDF verliert
stillschweigend Inhalt, und niemand merkt es, weil niemand das PDF gegen die Web-Ausgabe hält.
Ein neues Kapitel in der toc, das in `articles` fehlt, wäre genau dieser Fall. Darum läuft
dieser Vergleich im CI mit und bricht den Build ab, statt ihn durchzuwinken.

Web-only sind bewusst zwei Seiten, siehe NUR_WEB.
"""

import sys
import pathlib

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML fehlt. Aufruf: uv run --with pyyaml python tools/check_pdf_articles.py\n"
        "(so laeuft es auch im CI; das Buch selbst bekommt dafuer keine Abhaengigkeit)."
    )

# Seiten, die absichtlich nur in der Web-Ausgabe stehen:
#   landing-page.md  Auftakt, Inhaltsverzeichnis, Lizenz. MyST liesse sie als ersten
#                    toc-Eintrag ohnehin weg; der Lizenzhinweis des Buchs steht deshalb im
#                    LaTeX-Template, nicht hier.
#   orga.md          Organisatorisches der HHU (Aufzeichnungen, Folien, KI-Regeln,
#                    Modulhandbuch). Gehört nicht ins gedruckte Buch.
NUR_WEB = {"landing-page.md", "orga.md"}


def toc_dateien(toc):
    for eintrag in toc:
        if "file" in eintrag:
            yield eintrag["file"]
        for kind in eintrag.get("children", []):
            yield from toc_dateien([kind])


def main():
    wurzel = pathlib.Path(__file__).resolve().parent.parent
    cfg = yaml.safe_load((wurzel / "myst.yml").read_text(encoding="utf-8"))
    projekt = cfg["project"]

    aus_toc = list(toc_dateien(projekt["toc"]))
    erwartet = [f for f in aus_toc if f not in NUR_WEB]

    pdf = [e for e in projekt.get("exports", []) if e.get("format") == "pdf"]
    if len(pdf) != 1:
        sys.exit(f"FEHLER: genau ein PDF-Export erwartet, {len(pdf)} gefunden.")
    artikel = pdf[0].get("articles")
    if not artikel:
        sys.exit(
            "FEHLER: der PDF-Export hat keine articles-Liste. Ohne sie nimmt MyST die ganze toc, "
            "und orga.md landet wieder im gedruckten Buch."
        )

    hat = [a["file"] for a in artikel if "file" in a]

    fehler = []
    nur_in_toc = [f for f in erwartet if f not in hat]
    if nur_in_toc:
        fehler.append(
            "Diese Seiten stehen in der toc, fehlen aber im PDF-Export — sie wären im "
            "gedruckten Buch unsichtbar:\n  " + "\n  ".join(nur_in_toc)
        )
    nur_in_export = [f for f in hat if f not in aus_toc]
    if nur_in_export:
        fehler.append(
            "Diese Seiten stehen im PDF-Export, aber nicht in der toc:\n  "
            + "\n  ".join(nur_in_export)
        )
    verboten = [f for f in hat if f in NUR_WEB]
    if verboten:
        fehler.append(
            "Diese Seiten sollen nur im Web stehen, sind aber im PDF-Export:\n  "
            + "\n  ".join(verboten)
        )
    if hat != erwartet and not fehler:
        fehler.append(
            "Die Reihenfolge im PDF weicht von der toc ab:\n  toc:    "
            + ", ".join(erwartet)
            + "\n  export: "
            + ", ".join(hat)
        )

    # Die Teil-Überschriften müssen mitgepflegt sein, sonst ist das PDF flach.
    teile_toc = [e["title"] for e in projekt["toc"] if "children" in e]
    teile_exp = [a["title"] for a in artikel if "title" in a]
    if teile_toc != teile_exp:
        fehler.append(
            "Die Teil-Überschriften stimmen nicht:\n  toc:    "
            + ", ".join(teile_toc)
            + "\n  export: "
            + ", ".join(teile_exp)
        )

    if fehler:
        print("myst.yml: toc und PDF-Export passen nicht zusammen.\n")
        for f in fehler:
            print(f + "\n")
        print(
            "Beim Hinzufügen oder Umsortieren eines Kapitels muss es an beiden Stellen "
            "geschehen. Soll eine Seite absichtlich nur im Web stehen, gehört sie in NUR_WEB "
            "in diesem Skript."
        )
        return 1

    print(
        f"myst.yml in Ordnung: {len(hat)} Kapitel in derselben Reihenfolge in toc und PDF, "
        f"{len(teile_toc)} Teil-Überschriften, web-only: {', '.join(sorted(NUR_WEB))}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
