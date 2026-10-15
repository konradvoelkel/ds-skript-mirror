#!/usr/bin/env python3
"""Die deutsche Hälfte des Sprachpaars: hreflang-Tags in das gebaute HTML schreiben.

    python3 tools/hreflang.py --fetch <ziel.json>
    python3 tools/hreflang.py <public-verzeichnis> <filemap.json> <de-site> <en-site>

Die englische Ausgabe liefert ihre Hälfte seit dem 2026-10-15 aus. **Ein einseitiges
hreflang wird von Google ignoriert**, die englische Hälfte bringt also nichts, solange
diese hier fehlt — und umgekehrt. Drei Tags je Seite: die englische Entsprechung, ein
Selbstverweis (ohne ihn nennt sich die Seite nicht als Mitglied ihres eigenen Clusters)
und `x-default`. `x-default` zeigt auf die **englische** URL, genau wie drüben: beide
Seiten müssen denselben x-default nennen, sonst widersprechen sich die Cluster.

**Die Zuordnung wird nicht abgeschrieben.** Sie steht als eine Quelle der Wahrheit in
ds-en (`sync/filemap.json`) und wird im CI geholt. Die Slugs unterscheiden sich zwischen
den Ausgaben (`kovarianz` / `covariance`) — genau der Fall, für den es hreflang gibt.

**Zwei Seiten bekommen keine Tags:** `folien.md` und `orga.md` stehen in der filemap auf
`null`, haben also kein englisches Gegenstück. Eine Seite ohne Alternate gehört in keinen
Cluster, bekommt hier also *gar nichts* — auch keinen Selbstverweis.

**Wenn die filemap fehlt, wird nichts geschrieben und der Lauf geht weiter.** Eine kaputte
Hälfte ist schlechter als eine fehlende. Sichtbar wird das am Job `hreflang-map`, der dann
orange steht; hier steht eine laute Zeile im Log.

Gegenprobe nach dem Deploy, in ds-en:

    python3 tools/hreflang.py --verify https://datascience.konradvoelkel.com \\
        https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript

Das ist das eigentliche Erfolgskriterium. Alles hier ist nur Syntax.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from pathlib import Path

FILEMAP_URL = "https://raw.githubusercontent.com/konradvoelkel/ds-en/main/sync/filemap.json"

# Die Landingpage ist in beiden Ausgaben die Wurzel der Seite, nicht /landing-page/.
ROOT_STEM = "landing-page"


def stem(filename: str) -> str:
    """'kovarianz.md' -> 'kovarianz'. Der Slug ist der Dateiname ohne Endung."""
    return Path(filename).stem


def url_for(file_stem: str, site: str) -> str:
    """Die URL mit Schraegstrich am Ende -- die Form, die 200 liefert."""
    return f"{site}/" if file_stem == ROOT_STEM else f"{site}/{file_stem}/"


def fetch(target: Path) -> int:
    """Die filemap holen und pruefen, bevor sie als Artefakt weitergereicht wird."""
    print(f"Hole {FILEMAP_URL}")
    with urllib.request.urlopen(FILEMAP_URL, timeout=30) as r:
        raw = r.read()
    data = json.loads(raw)
    fmap = data["map"]
    if not isinstance(fmap, dict) or not fmap:
        raise SystemExit("✗ 'map' ist leer oder kein Objekt -- das kann nicht stimmen")
    paired = sum(1 for v in fmap.values() if v)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    print(f"✓ {target} ({len(raw)} Bytes): {len(fmap)} Eintraege, "
          f"{paired} mit englischem Gegenstueck, {len(fmap) - paired} ohne")
    return 0


def tags(en_url: str, de_url: str) -> str:
    return (
        f'<link rel="alternate" hreflang="de" href="{de_url}"/>'
        f'<link rel="alternate" hreflang="en" href="{en_url}"/>'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}"/>'
    )


def inject(public: Path, filemap: Path, de_site: str, en_site: str) -> int:
    if not filemap.exists():
        print("!" * 78)
        print("! Die filemap aus ds-en fehlt -- siehe Job 'hreflang-map' (steht dann orange).")
        print("! Es wird KEIN hreflang ausgeliefert. Das ist Absicht: eine kaputte Haelfte")
        print("! waere schlechter als eine fehlende. Der Rest des Deploys laeuft normal.")
        print("!" * 78)
        return 0

    fmap = json.loads(filemap.read_text(encoding="utf-8"))["map"]
    # Slug der deutschen Datei -> Slug der englischen Datei (oder None).
    by_stem = {stem(de): (stem(en) if en else None) for de, en in fmap.items()}

    pages = sorted(public.rglob("index.html"))
    seen_en: dict[str, str] = {}
    paired, unpaired = [], []

    for page in pages:
        rel = page.parent.relative_to(public).as_posix()
        if rel == ".":
            de_stem = ROOT_STEM
        elif "/" in rel:
            print(f"✗ {page}: unerwartet verschachtelt, das Layout der Seite hat sich geaendert")
            return 1
        else:
            de_stem = rel

        if de_stem not in by_stem:
            print(f"✗ {page}: '{de_stem}' fehlt in der filemap von ds-en. Entweder ist das "
                  f"Kapitel dort nachzutragen, oder diese Seite darf kein Alternate behaupten.")
            return 1

        en_stem = by_stem[de_stem]
        text = page.read_text(encoding="utf-8")

        if en_stem is None:
            # Kein Gegenstueck -> gar keine Tags, auch kein Selbstverweis.
            if "hreflang" in text:
                print(f"✗ {page} traegt hreflang, hat aber kein englisches Gegenstueck")
                return 1
            unpaired.append(de_stem)
            continue

        de_url = url_for(de_stem, de_site)
        en_url = url_for(en_stem, en_site)

        if en_url in seen_en:
            print(f"✗ {en_url} wird von {seen_en[en_url]} und {de_stem} zugleich beansprucht")
            return 1
        seen_en[en_url] = de_stem

        # Der Selbstverweis muss exakt die URL sein, die die Seite canonical nennt -- sonst
        # erklaert sich die Seite nicht zum Mitglied ihres eigenen Clusters. Deshalb laeuft
        # dieser Schritt *nach* dem Canonical.
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        if not canonical:
            print(f"✗ {page} hat noch keinen Canonical; hreflang muss danach laufen")
            return 1
        if canonical.group(1) != de_url:
            print(f"✗ {page}: Canonical ist {canonical.group(1)}, hreflang sagt {de_url}")
            return 1

        page.write_text(text.replace("</head>", tags(en_url, de_url) + "</head>", 1),
                        encoding="utf-8")
        paired.append(de_stem)

    print(f"✓ hreflang auf {len(paired)} Seiten ({3 * len(paired)} Tags), gepaart mit {en_site}")
    print(f"✓ {len(unpaired)} Seiten ohne englisches Gegenstueck und daher ohne Tags: "
          f"{', '.join(sorted(unpaired)) or '--'}")
    print(f"✓ {len(pages)} Seiten insgesamt, jede englische Ziel-URL genau einmal vergeben")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] == "--fetch":
        if len(argv) != 2:
            print(__doc__)
            return 2
        return fetch(Path(argv[1]))
    if len(argv) != 4:
        print(__doc__)
        return 2
    return inject(Path(argv[0]), Path(argv[1]), argv[2].rstrip("/"), argv[3].rstrip("/"))


if __name__ == "__main__":
    raise SystemExit(main())
