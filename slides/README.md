# Vorlesungsfolien

Beamer-Folien zur Vorlesung „Data Science“ (HHU Düsseldorf, Bachelor Informatik), Stand
Sommersemester 2026. Das zugehörige Skript liegt im übergeordneten Ordner und unter
<https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/>; die Seite „Vorlesungsfolien“ dort verlinkt
alle PDFs aus diesem Ordner.

## Was hier liegt

- `Data Science 2026 VL NN.tex` und `.pdf`: 15 Decks mit LaTeX-Quelle (VL 01–10, 15–17, 19, 20).
- `Data Science 2026 VL NN *.pdf` ohne `.tex`: zehn weitere Decks. VL 11 hat eine `.pptx`-Quelle
  daneben, VL 21 eine im Archiv (`slides25/`). VL 08 Zusatz, 12, 14, 18, 22 und 24 sind Ausdrucke
  von Buchkapiteln aus älteren Fassungen des Skripts; das Kapitel ist jeweils die aktuellere Quelle.
- `Data Science 2026 header.tex`: gemeinsamer Vorspann (Dokumentklasse, Theme, Listings, Autor und
  Semester). Jedes Deck bindet ihn mit `\input{Data Science 2026 header}` ein.
- `hhu-beamer-theme/`: das Beamer-Theme im HHU-Design (inoffizielle Umsetzung, enthält die
  HHU-Logos).
- `figures/`: die Bilder der Decks.
- `Data Science 2026 Alle Folien Druckversion.tex`: baut per Lua-Skript eine Handout-Fassung aller
  Decks in einem PDF (die Buchausdrucke und der Zusatz sind ausgenommen).
- `aenderungsliste.md`: Abgleich der Folien mit dem Skript (September 2026), sortiert nach Deck und
  Schwere, mit Vorschlag je Punkt.
- Nicht im Git, nur lokal bzw. in Sciebo: `slides25/` (Folien des Vorjahres), die Sammel-PDFs
  „Alle Folien“, `auto/` und LaTeX-Hilfsdateien.

## Bauen

Gebaut wird mit LuaLaTeX (TeX Live 2024 oder neuer); der Header lädt die Schriften Source Sans Pro
und Source Code Pro über `fontspec`, beide sind in TeX Live enthalten. Das Theme wird aus dem
Unterordner geladen; falls LaTeX es nicht findet, den Ordner `hhu-beamer-theme` in den lokalen
`texmf`-Baum legen oder `TEXINPUTS` setzen.

```bash
lualatex -interaction=nonstopmode "Data Science 2026 VL 04.tex"
```

Zweimal ausführen, damit die Navigation stimmt. Die Druckversion braucht `--shell-escape`:

```bash
lualatex -interaction=nonstopmode --shell-escape "Data Science 2026 Alle Folien Druckversion.tex"
```

Die PDFs werden nicht automatisch gebaut. Wer eine `.tex`-Datei ändert, baut das PDF lokal neu und
checkt beide Dateien zusammen ein, so wie im Skript die Notebooks zusammen mit ihren Ausgaben
eingecheckt werden.

## Fremdinhalte

Das Skript steht unter CC BY-SA 4.0. Davon ausgenommen sind in diesem Ordner:

- `figures/xkcd_password_strength.png`: Randall Munroe, xkcd 936, CC BY-NC 2.5.
- `figures/conway_data_science_venn_diagram.png`: Drew Conway, CC BY-NC 3.0.
- `figures/datasaurus.png`, `figures/AllDinosGrey_1.png`: Justin Matejka und George Fitzmaurice,
  Autodesk Research 2017.
- `figures/this-is-fine.png` (KC Green), `figures/numpy_cheat_sheet.png` (DataCamp),
  `figures/claude_shannon_unicycle.png` (Foto, Rechte ungeklärt) und
  `figures/color-blind-friendly-palette-13.jpg` (Blog-Grafik, Quelle ungeklärt): urheberrechtlich
  geschützt bzw. ungeklärt, nur für den Vortrag gedacht; ein Ersatz steht auf der Liste.
- `figures/red_dice.jpg`, `coins_pile.jpg`, `raw_eggs.jpg`, `fried_egg.png`, `lion_pause.jpg`:
  Stock-Bilder, Herkunft ungeklärt.
- `hhu-beamer-theme/`: Theme und HHU-Logos; Nutzung im Rahmen der Lehre an der HHU.

`falling_dice.jpg`, `rat_climbing_code_mountain.jpg`, `psytrance_enlightenment.jpg`, `escher.jpg` und
`magician.jpg` sind KI-generiert (die Bildunterschriften auf den Folien sind die Prompts).
`gambling-dogs.png` (Coolidge, um 1900) ist gemeinfrei. Alle übrigen Bilder sind eigene Grafiken.
