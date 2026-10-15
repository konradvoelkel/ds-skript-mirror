"""Erzeugt die OpenGraph-Vorschaukarte: images/social-card.png, 1200x630.

Die Karte liegt fertig im Repositorium; dieses Skript existiert, damit sie bei einer
Änderung von Titel oder Markenfarbe neu erzeugt und nicht von Hand nachgemalt werden
muss. Es läuft **nicht** in der CI — die CI kopiert nur das eingecheckte PNG.

    python3 tools/social_card.py            # images/social-card.png schreiben
    python3 tools/social_card.py --check    # scheitern, wenn die Datei veraltet ist

Warum überhaupt eine Karte: MyST hat keine projektweite OpenGraph-Grafik. Es nimmt das
erste Bild einer Seite, und wo eine Seite keines hat, greift es auf das erste Bild des
Projekts zurück — das war der CC-BY-SA-Knopf aus dem Lizenzabschnitt der Landingpage,
267x50. Das liegt unter den 200x200, die Facebook und LinkedIn verlangen (empfohlen sind
1200x630), also wurde auf 18 von 32 Seiten *gar keine* Vorschaukarte gerendert. Mit
`thumbnail:` in `myst.yml` greift stattdessen diese Karte; Seiten mit eigener Abbildung
behalten ihre.

Das ist die deutsche Fassung von `tools/social_card.py` aus `../ds-en` (gleiche Geometrie,
andere Texte) — wer hier am Layout dreht, sollte dort mitdrehen.

Markenfarbe und die AA-Zusage für Weiß auf Petrol stehen in BRANDING.md
(#007d7e = oklch(0.52 0.12 195), weiße Schrift 5,0:1).
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "social-card.png"

W, H = 1200, 630
BRAND = (0, 125, 126)        # #007d7e
TINT = (216, 245, 245)       # #d8f5f5, die helle Fläche desselben Farbtons
WHITE = (255, 255, 255)

# DejaVu liegt auf dem System und deckt "Völkel" ab; das Inter der Seite ist ein Webfont
# und hier nicht nötig, weil die Karte einmal gerendert und als PNG eingecheckt wird.
FONTS = Path("/usr/share/fonts/truetype/dejavu")


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def draw_card() -> Image.Image:
    img = Image.new("RGB", (W, H), BRAND)
    d = ImageDraw.Draw(img)

    pad = 76

    # Augenbraue: sagt "Lehrbuch", nicht "Mitschrift einer bestimmten Vorlesung".
    f_eyebrow = font("DejaVuSans-Bold.ttf", 23)
    d.text((pad, pad), "OFFENES VORLESUNGSSKRIPT  ·  CC BY-SA 4.0", font=f_eyebrow,
           fill=TINT)

    # Titel, zwei Zeilen; die zweite leichter, damit die erste als Name gelesen wird.
    f_t1 = font("DejaVuSans-Bold.ttf", 82)
    f_t2 = font("DejaVuSans.ttf", 46)
    d.text((pad, pad + 66), "Data Science", font=f_t1, fill=WHITE)
    d.text((pad, pad + 176), "von der Stochastik zum", font=f_t2, fill=WHITE)
    d.text((pad, pad + 232), "Machine Learning mit Python", font=f_t2, fill=WHITE)

    # Das Versprechen, das dieses Buch von einem Werkzeugkurs unterscheidet, in den
    # Worten, nach denen jemand suchen würde.
    f_claim = font("DejaVuSans-Bold.ttf", 34)
    y = pad + 330
    d.rectangle([pad, y, pad + 92, y + 5], fill=TINT)
    d.text((pad, y + 34), "Stochastik  ·  Numpy  ·  selbst programmiert",
           font=f_claim, fill=TINT)

    # Signatur am Fuß: der Autor gehört hierhin, nicht in den Titel. Absichtlich die
    # eigene Domain und nicht die Adresse der Seite — die Ausgabe zieht um, und eine in
    # ein PNG gebackene URL veraltet stillschweigend.
    f_foot = font("DejaVuSans.ttf", 26)
    d.text((pad, H - pad - 30), "Konrad Völkel   ·   konradvoelkel.com",
           font=f_foot, fill=TINT)

    return img


def main() -> int:
    img = draw_card()
    if "--check" in sys.argv:
        if not OUT.exists():
            print(f"✗ {OUT.relative_to(ROOT)} fehlt; tools/social_card.py ausführen")
            return 1
        from io import BytesIO
        buf = BytesIO()
        img.save(buf, "PNG")
        if buf.getvalue() != OUT.read_bytes():
            print(f"✗ {OUT.relative_to(ROOT)} ist veraltet; tools/social_card.py ausführen")
            return 1
        print(f"✓ {OUT.relative_to(ROOT)} passt zu tools/social_card.py")
        return 0
    img.save(OUT, "PNG")
    print(f"✓ {OUT.relative_to(ROOT)} geschrieben ({OUT.stat().st_size} Bytes, {W}x{H})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
