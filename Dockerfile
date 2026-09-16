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

# Install mystmd globally
RUN npm install -g mystmd

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt
