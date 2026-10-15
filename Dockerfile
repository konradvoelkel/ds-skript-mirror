FROM nikolaik/python-nodejs:python3.14-nodejs26-slim

# System dependencies. The TeX packages are what `myst build --pdf` needs:
# latexmk drives xelatex + bibtex, the texlive-* sets cover the packages used by
# the MyST book template (fontspec, listings, natbib, tcolorbox, ...).
# imagemagick lets MyST convert GIF/WebP figures to PNG for the LaTeX export.
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    imagemagick \
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
