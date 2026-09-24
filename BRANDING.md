# Branding — datasciencebook

Beschlossen 2026-09-22, gemeinsam mit den anderen fünf Projekten (bubatzkarte,
laberampel, autokorrektur, datasciencebook, eidlbook, eipybook). Die Ledger-Fassung
steht in `~/files/personal/orga/boxes-ledger.html` § Farbsystem.

## Die Farbe dieses Projekts

| Rolle | Wert | OKLCH |
|---|---|---|
| Marke | `#007d7e` | `oklch(0.52 0.12 195)` |
| Fläche hell (Badges, Hinweise) | `#d8f5f5` | `oklch(0.95 0.03 195)` |
| Akzent im Dunkelmodus | `#2cc5c5` | `oklch(0.75 0.12 195)` |

Weiße Schrift auf der Markenfarbe erfüllt WCAG AA (5.0:1). Farbton 195° — petrol.

**Warum dieser Farbton:** Kühl und neben dem HHU-Blau von eipybook klar unterscheidbar; die drei Skripte bilden eine Reihe (petrol → blau → violett).

**Für dieses Projekt zu beachten:** HHU-Hausfarben (Blau #006AB3, Grün #8CB110, Rot #BE0A26, Orange #EE7F00) bleiben die Farben für Abbildungen und Diagramme. Die Markenfarbe ist der Akzent des Buches (Links, Titel, Admonitions), nicht die Datenfarbe.

## Die Regel dahinter

Alle sechs Projekte teilen Helligkeit und Buntheit und unterscheiden sich nur im
Farbton. Gearbeitet wird in OKLCH, weil dort gleiche L- und C-Werte auch gleich hell
und gleich bunt *aussehen* — in HSL tun sie das nicht.

- `L = 0.52` ist die Helligkeit, bei der weiße Schrift gerade AA erreicht (4.5:1).
- `C = 0.12` ist so bunt, wie sRGB es bei dieser Helligkeit für *jeden* Farbton kann.
- Die Farbtöne stehen mindestens 40° auseinander; darunter liest sich der Unterschied
  als Fehler statt als Absicht.
- Rot/Gelb/Grün sind in Oberflächen Signalfarben. Wo eine App sie als Signal braucht,
  ist ihre Marke keiner dieser drei Töne.

| Projekt | Farbton | Marke |
|---|---|---|
| bubatzkarte | 150° grün | `#287c42` |
| **datasciencebook** | 195° petrol | `#007d7e` |
| eipybook | 250° blau | `#286cab` |
| eidlbook | 295° violett | `#6f59a6` |
| laberampel | 345° magenta | `#984979` |
| autokorrektur | 55° orange | `#9c5313` |

Varianten werden abgeleitet, nicht erfunden: heller Grund `oklch(0.95 0.03 H)`,
Dunkelmodus-Akzent `oklch(0.75 0.12 H)`, immer derselbe Farbton H.

**Wenn etwas nicht passt:** L oder C für *alle sechs* ändern, nie einen einzelnen
Hexwert nachbessern. Sonst zerfällt das System in sechs Einzelfarben.

`oklch()` ist seit 2023 in allen Browsern nativ; in CSS direkt so schreiben, die
Hexwerte sind nur der Fallback für Android, LaTeX und Bildbearbeitung.
