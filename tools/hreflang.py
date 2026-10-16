#!/usr/bin/env python3
"""Die deutsche Hälfte des Sprachpaars: hreflang-Tags in das gebaute HTML schreiben.

    python3 tools/hreflang.py --fetch <ziel.json>
    python3 tools/hreflang.py <public-verzeichnis> <filemap.json> <de-site> <en-site>
    python3 tools/hreflang.py --verify <public-verzeichnis> <filemap.json>

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

**Die Rückfallebene.** `hreflang/filemap.json` liegt eingecheckt im Repo. Der Job
`hreflang-map` frischt sie auf und legt sie als Artefakt unter demselben Pfad ab, überschreibt
die ausgecheckte Fassung also. Scheitert der Abruf — GitHub ist zwei Minuten weg, und GitLab
reicht Artefakte nur innerhalb derselben Pipeline weiter —, bleibt die eingecheckte Karte
stehen und das Sprachpaar bleibt vollständig. Ohne diese Ebene hieße ein Aussetzer: eine
Ausgabe ganz ohne hreflang, beide Jobs grün, und weil ein einseitiges hreflang von Google
ignoriert wird, fällt die englische Hälfte mit — aus 30/30 würde 0/30 auf beiden Seiten, ohne
ein einziges rotes Signal.

**Deshalb zusätzlich `--verify`**, das nach dem Einhängen am gebauten `public/` nachzählt und
abbricht, wenn die Zahlen nicht stimmen. Melden allein genügt hier nicht: ein Log liest niemand,
und genau dieser Fehlertyp ist im Browser unsichtbar und nur durch Nachmessen zu finden —
derselbe wie seinerzeit die localhost-Sitemap.

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

FILEMAP_URL = "https://raw.githubusercontent.com/konradvoelkel/ds-en/main/sync/filemap.json.ABSICHTLICH-KAPUTT-TEST"

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
    committed = target.read_bytes() if target.exists() else None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    print(f"✓ {target} ({len(raw)} Bytes): {len(fmap)} Eintraege, "
          f"{paired} mit englischem Gegenstueck, {len(fmap) - paired} ohne")
    if committed is None:
        print("!" * 78)
        print("! Im Repo lag keine Karte. Die geholte Fassung bitte einchecken -- sie ist die")
        print("! Rueckfallebene, wenn GitHub beim naechsten Lauf nicht antwortet.")
        print("!" * 78)
    elif committed != raw:
        old_map = json.loads(committed)["map"]
        dazu = sorted(set(fmap) - set(old_map))
        weg = sorted(set(old_map) - set(fmap))
        geaendert = sorted(k for k in set(fmap) & set(old_map) if fmap[k] != old_map[k])
        print("!" * 78)
        print("! Die geholte Karte weicht von der eingecheckten ab -- ein Commit ist faellig.")
        for label, items in (("neu", dazu), ("entfallen", weg), ("geaendert", geaendert)):
            if items:
                print(f"!   {label}: {', '.join(items)}")
        print("! Dieser Lauf benutzt die frische Fassung; das Repo haelt noch die alte vor.")
        print("!" * 78)
    else:
        print("✓ identisch mit der eingecheckten Rueckfallebene")
    return 0


def tags(en_url: str, de_url: str) -> str:
    return (
        f'<link rel="alternate" hreflang="de" href="{de_url}"/>'
        f'<link rel="alternate" hreflang="en" href="{en_url}"/>'
        f'<link rel="alternate" hreflang="x-default" href="{en_url}"/>'
    )


def inject(public: Path, filemap: Path, de_site: str, en_site: str) -> int:
    if not filemap.exists():
        print(f"✗ {filemap} fehlt. Die Datei liegt eingecheckt im Repo und wird von")
        print("  hreflang-map nur aufgefrischt -- fehlt sie, stimmt etwas Grundsaetzliches")
        print("  nicht. Ohne sie waere die Ausgabe ohne Sprachpaar, und weil ein einseitiges")
        print("  hreflang ignoriert wird, faellt die englische Haelfte mit.")
        return 1

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


def verify(public: Path, filemap: Path) -> int:
    """Am gebauten public/ nachzaehlen -- nicht am Log glauben.

    Die Sollwerte kommen aus der filemap, nicht aus einer Konstante: kommt ein Kapitel
    dazu, waechst die Erwartung von selbst mit. Hart abbrechen statt melden, weil dieser
    Fehlertyp im Browser unsichtbar ist.
    """
    if not filemap.exists():
        print(f"✗ {filemap} fehlt -- es laesst sich nicht einmal sagen, was erwartet waere")
        return 1
    fmap = json.loads(filemap.read_text(encoding="utf-8"))["map"]
    paired = {stem(de) for de, en in fmap.items() if en}
    unpaired = {stem(de) for de, en in fmap.items() if not en}

    pages = sorted(public.rglob("index.html"))
    seen_en: dict[str, str] = {}
    with_tags = without = tags = 0
    bad: list[str] = []
    for page in pages:
        rel = page.parent.relative_to(public).as_posix()
        name = ROOT_STEM if rel == "." else rel
        html = page.read_text(encoding="utf-8", errors="replace")
        alt = dict(re.findall(r'<link rel="alternate" hreflang="([a-z-]+)" href="([^"]+)"', html))
        tags += len(alt)
        if name in unpaired:
            without += 1
            if alt:
                bad.append(f"{name}: hat {len(alt)} Tags, obwohl ohne englisches Gegenstueck")
            continue
        if name not in paired:
            bad.append(f"{name}: steht in keiner Haelfte der filemap")
            continue
        with_tags += 1
        if set(alt) != {"de", "en", "x-default"}:
            bad.append(f"{name}: Tags {sorted(alt) or 'keine'} statt de/en/x-default")
            continue
        if alt["x-default"] != alt["en"]:
            bad.append(f"{name}: x-default zeigt nicht auf dieselbe URL wie hreflang=en")
        if alt["en"] in seen_en:
            bad.append(f"{name}: beansprucht {alt['en']}, das schon {seen_en[alt['en']]} gehoert")
        seen_en[alt["en"]] = name
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        if not canonical or canonical.group(1) != alt["de"]:
            got = canonical.group(1) if canonical else "keiner"
            bad.append(f"{name}: Canonical {got} != Selbstverweis {alt['de']}")

    soll = 3 * len(paired)
    print(f"  {len(pages)} Seiten, {with_tags} mit drei Tags, {without} bewusst ohne, "
          f"{tags} Tags gesamt (Soll {soll})")
    if tags != soll or with_tags != len(paired) or without != len(unpaired):
        bad.append(f"Zahlen stimmen nicht: {tags} Tags auf {with_tags} Seiten, "
                   f"erwartet {soll} auf {len(paired)}")
    for b in bad:
        print(f"  ✗ {b}")
    if bad:
        print("✗ Das Sprachpaar ist nicht vollstaendig. Ein einseitiges hreflang wird")
        print("  ignoriert -- das zoege die englische Haelfte mit herunter.")
        return 1
    print(f"✓ {tags} hreflang-Tags, jede englische Ziel-URL genau einmal vergeben")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] == "--verify":
        if len(argv) != 3:
            print(__doc__)
            return 2
        return verify(Path(argv[1]), Path(argv[2]))
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
