#!/usr/bin/env python3
"""Schreibt die Alternativtexte aus alt-texte.yml in die Notebooks — und prüft sie.

    python3 tools/alt_texts.py --apply    # Texte in die .ipynb schreiben
    python3 tools/alt_texts.py --check    # meckern, wenn etwas fehlt oder abweicht
    python3 tools/alt_texts.py            # Stand berichten

**Warum das so umständlich ist.** MyST nimmt als `alt` eines Bildes aus einer
Notebook-Ausgabe die `text/plain`-Darstellung derselben Ausgabe. Matplotlib legt dort
`<Figure size 640x480 with 1 Axes>` ab, und genau das landete bisher in 156 von 228
`alt`-Attributen: nicht leer, sondern **schlimmer als leer**, weil eine Prüfung auf
„fehlt `alt`?" glatt durchgeht, während ein Screenreader Unsinn vorliest und die
Bildersuche nichts findet.

Alle naheliegenden Wege wurden durchprobiert und funktionieren in dieser MyST-Version
**nicht**: Zell-Metadaten (`myst.image.alt`, `myst.figure.alt`, `mystnb.image.alt`,
`image.alt`, `alt`) werden ignoriert; ein `:alt:` an einer `{figure}`-Direktive, die eine
beschriftete Code-Zelle einbettet, wird ebenfalls ignoriert (die `:caption:` dagegen
wirkt). Übrig bleibt, die `text/plain`-Ausgabe selbst zu setzen — das wirkt.

**Deshalb liegt die Wahrheit in `alt-texte.yml` und nicht im Notebook.** Ein erneutes
Ausführen eines Notebooks überschreibt `text/plain` wieder mit dem Matplotlib-Repr. Der
Ablauf ist also: Notebook ausführen, dann `--apply`, dann committen. `--check` läuft im
CI-Job `check-structure` mit und schlägt an, wenn jemand den zweiten Schritt vergisst.

Geschlüsselt wird nach der **Zell-ID** (nbformat 4.5), nicht nach der Position: Zellen
verschieben sich, IDs nicht. Mehrere Bilder in einer Zelle bekommen mehrere Einträge in
der Reihenfolge ihrer Ausgabe.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXTS = ROOT / "alt-texte.yml"
REPR_PREFIX = "<Figure size"


def load_texts() -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML fehlt; mit `uv run --with pyyaml python tools/alt_texts.py …`")
    return yaml.safe_load(TEXTS.read_text(encoding="utf-8"))


def figures(nb: dict):
    """(Zelle, Ausgabe) für jede Bildausgabe, in Dokumentreihenfolge."""
    for cell in nb["cells"]:
        for out in cell.get("outputs", []):
            if "image/png" in out.get("data", {}):
                yield cell, out


def run(mode: str) -> int:
    texts = load_texts()
    applied = missing = drifted = extra = 0
    notes: list[str] = []

    for nbname, by_cell in texts.items():
        path = ROOT / nbname
        if not path.exists():
            notes.append(f"✗ {nbname} gibt es nicht mehr, steht aber in alt-texte.yml")
            continue
        nb = json.loads(path.read_text(encoding="utf-8"))
        ids = {c["id"] for c in nb["cells"]}
        for cid in by_cell:
            if str(cid) not in ids:
                notes.append(f"✗ {nbname}: Zelle {cid} gibt es nicht mehr")
        changed = False
        for cell in nb["cells"]:
            wanted = by_cell.get(cell["id"])
            outs = [o for o in cell.get("outputs", []) if "image/png" in o.get("data", {})]
            if wanted is None:
                for o in outs:
                    if "".join(o["data"].get("text/plain", [])).strip().startswith(REPR_PREFIX):
                        missing += 1
                        notes.append(f"✗ {nbname}: Zelle {cell['id']} hat ein Bild ohne Text")
                continue
            if len(wanted) != len(outs):
                notes.append(f"✗ {nbname}: Zelle {cell['id']} hat {len(outs)} Bilder, "
                             f"aber {len(wanted)} Texte")
                continue
            for out, text in zip(outs, wanted):
                current = "".join(out["data"].get("text/plain", []))
                if current == text:
                    continue
                if mode == "apply":
                    out["data"]["text/plain"] = [text]
                    changed = True
                    applied += 1
                else:
                    drifted += 1
                    why = ("noch das Matplotlib-Repr" if current.strip().startswith(REPR_PREFIX)
                           else "ein anderer Text")
                    notes.append(f"✗ {nbname}: Zelle {cell['id']} trägt {why}")
        if changed:
            path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
                            encoding="utf-8")

    # Bilder, die in keinem Eintrag vorkommen
    for p in sorted(ROOT.glob("*.ipynb")):
        if "local-widgets" in p.name or p.name in texts:
            continue
        nb = json.loads(p.read_text(encoding="utf-8"))
        for _, out in figures(nb):
            if "".join(out["data"].get("text/plain", [])).strip().startswith(REPR_PREFIX):
                extra += 1

    if mode == "apply":
        print(f"✓ {applied} Alternativtexte geschrieben")
        return 0

    bad = missing + drifted + len([n for n in notes if n.startswith("✗")]) - missing - drifted
    for n in notes:
        print("  " + n)
    if missing or drifted or bad:
        print(f"✗ {missing} Bilder ohne Text, {drifted} abweichend. "
              f"Nach dem Ausführen eines Notebooks: python3 tools/alt_texts.py --apply")
        return 1
    total = sum(len(v) for by in texts.values() for v in by.values())
    out = f"✓ {total} Alternativtexte stehen in {len(texts)} Notebooks und stimmen"
    if extra:
        out += f"; {extra} Bilder außerhalb des Buchs ohne Text (nicht gebaut)"
    print(out)
    return 0


def main() -> int:
    if "--apply" in sys.argv:
        return run("apply")
    if "--check" in sys.argv or len(sys.argv) == 1:
        return run("check")
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
