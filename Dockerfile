FROM nikolaik/python-nodejs:python3.14-nodejs26-slim

# System dependencies. The TeX packages are what `myst build --pdf` needs:
# latexmk drives xelatex + bibtex, the texlive-* sets cover the packages used by
# the MyST book template (fontspec, listings, natbib, tcolorbox, ...).
# imagemagick lets MyST convert GIF/WebP figures to PNG for the LaTeX export.
#
# git: tools/freshness.py liest das Datum je Kapitel aus "git log" der Quelldatei, und
# zwar in build-web UND build-pdf (--stamp-source, vor dem Bau). Ohne git brechen beide
# ab -- nachgewiesen am 2026-10-16, Pipeline 183638 nach 97d04cc: build-web fiel nach
# 15 s, pages und notify-ds-en wurden uebersprungen, die Seite blieb auf dem Stand von
# 08:40 stehen. Der pages-Job installiert sein eigenes git nach, weil er in
# python:3.13-alpine laeuft und nicht in diesem Image.
#
# Der Kommentar steht absichtlich *vor* der Anweisung und nicht zwischen den Paketen:
# ein "#" in einer Zeilenfortsetzung haengt davon ab, dass der Parser Kommentarzeilen
# entfernt. Docker tut das (am 2026-10-16 geprueft), gebaut wird hier aber mit Kaniko.
# Tut er es nicht, kommentiert das "#" alle folgenden Pakete *und* das "&& rm -rf" aus,
# der Build ist gruen und das Image still ohne TeX und ohne git.
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    imagemagick \
    git \
    latexmk \
    texlive-xetex \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-bibtex-extra \
    texlive-lang-german \
    && rm -rf /var/lib/apt/lists/*

# Kein "npm install -g mystmd" mehr (entfernt 2026-10-15). Es war ungepinnt und wurde nie
# benutzt: die CI baut mit `uv run myst`, und das loest auf .venv/bin/myst auf -- den
# Python-Wrapper, den uv.lock festnagelt. Das globale npm-Paket war also eine zweite,
# treibende Kopie derselben Software, die bei einer Aenderung der PATH-Reihenfolge lautlos
# uebernommen haette. Node bleibt im Basis-Image, der Wrapper braucht es.

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt
