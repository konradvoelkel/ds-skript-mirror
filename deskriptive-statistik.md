# Deskriptive Statistik und Visualisierung

[Vorlesungsaufzeichnung Deskriptive Statistik](https://media.hhu.de/channel/video/data-science-vl-9-stetige-verteilungen-2025/39016f5414ef3b8edd0dff941f802314/167?t=3244)

In {cite}`dds`, S.41 ist schematisch dargestellt, wie wir 'Data Science' betreiben:

```{figure} images/ds-process-oneill.png
:width: 480px
:align: center
:name: ds-process

Der "Data Science Prozess"
```

Fokus hier: Explorative Datenanalyse

Wir werden noch einmal wiederholen und in einen neuen Zusammenhang stellen, was wir bisher zur deskriptiven Statistik gelernt haben, insbesondere über summarische (zusammenfassende) Statistik und Visualisierung. 


Diese Wiederholung wird zugleich eine Vokabelstunde, denn wir wollen sowohl die Sprache der statistischen Datenanalyse als auch die des Machine Learning verstehen und übersetzen können.

## Statistik vs. Machine Learning

Es gibt zwei "Kulturen", die Statistik mit dem statistischen Lernen, und das Maschinelle Lernen mit dem vorhersagenden (prädiktiven) Modellieren.
Maschinelles Lernen ist ein Teilgebiet der künstlichen Intelligenz, Statistik ein Teilgebiet der Mathematik.

* Begriffskorrespondenz Statistik - maschinelles Lernen
  * Modell - Modell (beim Einsatz von neuronalen Netzen auch: das Netz)
  * Parameter - Gewichte
  * Fitten - Lernen
  * Testdatensatz-Performance - Generalisierung
  * Regression, Klassifikation - Supervised Learning
  * Dichteschätzung, Klassenbildung (clustering) - Unsupervised Learning
 
Die *explorative Datenanalyse* ist das Berechnen summarischer Statistik und Visualsierung (also deskriptiver Statistik), um eine bessere Einschätzung über die Informationen in einem Datensatz zu erlangen.
Beim *Data Mining* geht es darum, diesen Arbeitsschritt in einem Data Science Projekt zu automatisieren, also die automatische Entdeckung von Mustern und Zusammenhängen.

Man kann die verschiedenen Kulturen des Modellierens noch etwas feiner aufschlüsseln, wie es C. Molnar in dem Buch ``Modeling Mindsets: The Many Cultures Of Learning From Data'' getan hat {cite}`molnarmindsets`; dazu ist es aber hilfreich, bereits den Maximum-Likelihood-Ansatz und den Satz von Bayes zu kennen.



## Deskriptive Statistik

Die beschreibende (deskriptive) Statistik besteht aus den Datenanalysen, die *vor* der schließenden (inferentiellen) Statistik gemacht werden. Das besteht vor Allem in der Beschreibung der Daten durch verschiedene Maßzahlen.

* Stichprobe = Sample, hat einen Umfang = Länge = Anzahl der Elemente / Zeilen / Instanzen / Ergebnisse
  
  Abzugrenzen von der Stichprobe ist die *Population*, das ist die Grundgesamtheit aller möglichen Ergebnisse, mit einer gewissen Verteilung.
  
* Bei tabellarischen Daten heißen die Spalten auch Variablen, Attribute, Merkmale, Features während die Möglichen Werte *Ausprägungen* heißen.
  Je nach Art eines Merkmals unterscheidet man verschiedene Skalenarten:
  * Nominalskala: kategoriell, diskret, keine feste Reihenfolge (z.B. Geschlecht)
  * Ordinalskala: Werte können geordnet werden, aber ohne Abstandsmaß (z.B. Rangplätze)
  * Intervallskala (eine Kardinalskala): (diskrete oder stetige) Werte können geordnet und Abstände angegeben werden, ein Nullpunkt ist festgelegt (z.B. Temperatur, Jahresangaben)
  * Verhältnisskala: Kardinalskala mit natürlichem Nullpunkt, sodass das Verhältnis zwischen zwei Werten eine sinnvolle Größe ist (z.B. Alter, Einkommen).
* Univariate Beschreibungen

  sind Maßzahlen, die sich auf eine einzelne Variable beziehen, nicht jedoch auf den Bezug der Variablen zueinander. Diese Maßzahlen lassen sich weiter einteilen:
  * zentrale Tendenz (früher sagte man 'Mittelwerte')
  
    * Das arithmetische Mittel (unser Schätzwert für den Erwartungswert der zugrundeliegenden Verteilung)
    * Der Median (die Hälfte der Datenpunkte liegt über dem Median, insofern ist es die Mitte)
      Es gilt übrigens stets
      $|\texttt{median}(x) - \texttt{mean}(x)| \leq \sigma$
      Für eine Ordinalskala (wenn also Abstände zwischen den Werten nicht angegeben werden können) ist der Median eine sinnvolle Größe
      
    * Die Bereichsmitte (Mid-range) ist das arithmetische Mittel aus dem Maximum und dem Minimum.
    
    * Der Modus
    
      ist definiert als häufigster Wert. Der Begriff selbst ist wenig nützlich, wird aber häufig in dem Sinne verwendet, dass eine Verteilung unimodal oder bimodal ist. Unimodal bedeutet, dass es einen klar erkennbaren Modus gibt, der die Verteilung gut beschreibt. Bimodal bedeutet, dass die Verteilung eine gemischte Verteilung ist, deren zwei Komponenten verschiedene Moden haben. Das erkennt man dann an zwei Hochpunkten. Im Allgemeinen ist nicht klar, ob man einen Datensatz als unimodal oder bimodal (oder multimodal) verteilt ansehen sollte.
      
      Für Variablen auf einer Nominalskala ist der Modus ein sinnvoller Lageparameter
      
    * Zu mehreren Maßen der zentralen Tendenz gehört gewissermaßen ein Dispersionsmaß (siehe Dispersion), was man sich merken kann mit "dispersion precedes location". Dazu ist [der englische Wikipedia-Artikel 'Central tendency'](https://en.wikipedia.org/wiki/Central_tendency) zu empfehlen.
    
  * Dispersion, Spread (Streuung)
  
    Streumaße charakterisieren, inwiefern die Daten um einen Lageparameter streuen, d.h. davon mehr oder weniger stark abweichen. Da dies auch bedeutet, zu charakterisieren, inwiefern jeder einzelne Datenpunkt von den anderen abweicht, lassen sich Streumaße ohne direkten Bezug auf einen Lageparameter definieren.
    
    * Spannweite: maximaler Wert minus minimaler Wert
    * Variationsverhältnis: Anteil der Stichprobe, dessen Wert nicht der Modus ist
    * Quartile: analog zum Median ist das untere Quartil $Q1$ der Wert, sodass genau ein Viertel der Daten einen geringeren Wert hat. Das obere Quartil $Q3$ ist entsprechend der Wert, sodass genau ein Viertel der Daten einen höheren Wert hat. Der Median entspricht $Q2$. Analog definiert man Perzentile.
    * Stichprobenvarianz: mittlere quadratische Abweichung vom Mittelwert
    * Stichprobenstandardabweichung
    
      Wenn wir mit Einheiten rechnen, sehen wir ein Problem mit der Varianz: ist eine Zufallsvariable $X$ oder ein Vektor $x$ (etwa eine Spalte einer Tabelle) in der Einheit Meter (eine Verhältnisskala), so wird beim Berechnen der Varianz eine Summe bzw. ein Integral über Quadrate gebildet, somit ist die Varianz in der Einheit Quadratmeter. Man sieht daran auch, dass die Varianz generell skalenabhängig ist, d.h. beim Vergleich zweier Variablen, die eine in Meter, die andere in Zentimeter, ist die Varianz kein guter Vergleich. Daraus die Wurzel zu ziehen korrigiert den ersten Fehler, und liefert mit der Standardabweichung ein Maß in der gleichen Einheit wie den Erwartungswert.
      
      Achtung: es gibt zwei Formeln mit dem Namen "Stichprobenstandardabweichung", einmal mit $n$ im Nenner, einmal mit $n-1$. Diesen Umstand nennt man auch *Bessel-Korrektur* und wir befassen uns im Rahmen der Schätztheorie noch damit. Ohne weiteren Hinweis ist die $n$-Version die "richtige".
      
    * dispersion precedes location:
      
      * Der Modus ist das Minimum des Variationsverhältnisses ($L_0$-Norm)
      * Der Median ist das Minimum der mittleren absoluten Abweichung ($L_1$-Norm)
      * Der Mittelwert ist das Minimum der Standardabweichung ($L_2$-Norm)
      * Die Bereichsmitte ist das Minimum der absoluten Abweichung ($L_\infty$-Norm)
      
  
  * Form (Shape)
  
    * Schiefe (skewness) ist das dritte zentrale Moment, normiert auf die Standardabweichung ($\mu_3 / \sigma^3$)
    * Wölbung (kurtosis) ist das vierte zentrale Moment, normiert auf die Standardabweichung ($\mu_4/\sigma^4$)
    * Exzess ist die Differenz der Wölbung zur Wölbung einer Normalverteilung -- die unabhängig von den Parametern genau $3$ ist
  
* multivariate Beschreibungen:
  * Korrelationen
  
    Mit Kovarianz und Korrelation werden wir uns bald beschäftigen müssen. Die Kovarianz verhält sich zur Varianz wie ein Skalarprodukt zu einer Norm. Der (Pearson)-Korrelationskoeffizient wird so normiert, dass er skaleninvariant ist.

[Für eine kurze lockere Übersicht über einen Teil der Frage ``Was sind eigentlich Daten'', insb. der Frage der Skalen, gibt es ein Video vom HeiCAD-Programm ``KI für Alle''](https://www.youtube.com/watch?v=hJVOudzjnEI).
    
## Visualisierung

Wozu visualisieren?

[Alberto Cairo hat den 'Datasaurus' erfunden](http://www.thefunctionalart.com/2016/08/download-datasaurus-never-trust-summary.html) um auf den Unterschied zwischen zusammenfassender Statistik und Visualisierung hinzuweisen. [Justin Matejka und George Fitzmaurice haben die 'Datasaurus Dozen' entwickelt](https://dl.acm.org/doi/10.1145/3025453.3025912), eine Reihe von Datensätzen, die allesamt gleiche zusammenfassende Statistiken aufweisen, aber visuell sehr deutliche Unterschiede zeigen.

```{figure} images/AllDinosGrey_1.png
:width: 480px
:align: center
:name: datasaurus-dozen

The Datasaurus Dozen, inspiriert von Anscombe's Quartett.
```

* Wichtigste Arten von Plots

  * Histogramme ("historical diagram")
  
    Um die Häufigkeitsverteilung kardinal skalierter Merkmale zu visualisieren, kann man das Merkmal auf der x-Achse auftragen und nebeneinander liegende Rechtecke, deren Flächeninhalt der Häufigkeit einer Klasse darstellen, die durch Aufsummieren der Häufigkeit über das zugrunde liegende Intervall auf der x-Achse zustande kommen. Die Intervalllänge heißt Eimergröße (bucket size), binsize oder Klassengröße. Die Wahl der richtigen binsize ist eine Wissenschaft für sich und es gibt verschiedene Algorithmen zur Berechnung einer "guten" binsize.
    
    Histogramme sind also spezielle Bar charts / Column charts. Für nominal skalierte Merkmale lässt sich direkt der entsprechende Bar chart betrachten, der gleich breite Rechtecke mit Höhe entsprechend der Häufigkeit einer Ausprägung enthält. Dazu muss noch eine willkürliche Anordnung der Ausprägungen gewählt werden.
    
    Ein Histogramm besteht also eigentlich aus einer statistischen Transformation von stetigen (kardinal skalierten) Daten in diskrete Daten, die dann gebarchartet werden.
    
    Empfehlenswert: [Ein schöner Blogpost über Histogramme, ohne Code, von Mike Yi von Chartio](https://chartio.com/learn/charts/histogram-complete-guide/)

  * Scatterplot
  
    Eine Menge von Vektoren in $\mathbb{R}^2$ lässt sich darstellen indem an den Koordinaten ein Symbol dargestellt wird, etwa ein gefüllter Kreis.
    Typischerweise werden bei tabellarischen Daten zwei Variablen ausgewählt, je eine für x- und y-Achse.
    
  * Boxplot, auch Box-and-Whiskers-plot
  
    Werden wir beim Thema Konfidenzintervalle kennen lernen, denn das (und Quantile) kann man damit gut darstellen.
    
  * Linienplot
  
    Wenn man eine oder mehrere Funktionsgraphen plottet (so wie wir es mit den PDF getan haben), sind das Lininenplots. Man kann ebenso Daten auf Kardinalskalen mit einem Linienplot darstellen, aber das Verbinden von Punkten suggeriert eine Datenfülle, die nicht unbedingt vorliegt.
    
  * Tortendiagramm
  
    Generell hat sich herausgestellt, dass sich immer dann, wenn man ein Tortendiagramm verwenden kann, auch einen Barplot machen kann, der lesbarer ist. Tortendiagramme haben daher vor Allem einen Wert, wenn man einen Text auflockern will, ohne wesentlich auf die dargestellte Statistik einzugehen. Grundsätzlich geeignet sind Merkmale in Intervallskalen, da die Torte Anteile eines Ganzen darstellt.
    
  * Violinenplot
  
    Ähnlich einem Boxplot, aber anstelle eines Rechtecks wird die Dichteverteilung ausschnittsweise dargestellt. Ein Nachteil ist ihre seltene Verwendung, wodurch Leser\*innen diesen Plottyp nicht gewohnt sind.
    
  * Kartendarstellung
  
    Mit einem Bild einer Landkarte (oder anderer Karte, z.B. Netzwerktopologien) im Hintergrund lassen sich Merkmale räumlich darstellen, etwa als Farbe einer umgrenzten Fläche. Das ist ähnlich zu einem Histogramm, denn anstelle eines Scatterplots werden zweidimensionale Bereiche (anstatt Intervalle) zusammengefasst, bevor eine Darstellung der aggregierten Daten vorgenommen wird. Ein Spezialfall ist eine "Landkarte" die aus einem Raster besteht, in das nun Häufigkeiten aufgetragen werden, ein zweidimensionales Histogramm.
    
  * unzählige weitere, seltener gebrauchte oder nicht in diesem Schema kategorisierbare Visualisierungen - es kommt immer auf den Anwendungsfall an, was das geeigneteste Kommunikationsmittel ist.


* Wichtigste Werkzeuge zum Plotten mit Python

  * `matplotlib` - das verwenden wir, es ist das am häufigsten verwendete Paket für Python
  * Das objektorientierte Interface von `matplotlib` - empfohlen von den Entwickler\*innen
  * Seaborn - eine Schicht über `matplotlib`, die weitreichende Annahmen trifft, was gut aussehen könnte, mit einem Fokus auf Nutzerfreundlichkeit
  * Plotnine - eine Implementierung der Grammatik der Grafiken in Python, analog zu R's `ggplot2`
  * Bokeh - Interaktive Web-plots, z.B. [Demo zum IMDB-Datensatz](https://demo.bokeh.org/movies)
  * Pygal - generiert SVG-Dateien, die mit HTML5 ebenfalls für Animationen verwendet werden können.

* Die Grammatik der Grafiken

  * Geschichte
    
    1983: Bertin: Semiology of Graphics
    
    2000: Wilkinson, Anand, Grossman: The Grammar of Graphics
    
    2005: Wickham: `ggplot2` R Paket
    
    2010: Wickham: A Layered Grammar of Graphics
    
  * Schichten (Layer) der Grammatik
  
    * Daten -- Welche sollen visualisiert werden?
    * Ästhetik -- Achsen, Dimensionen
    * Skalen -- Werte skalieren? Nominal/Ordinal?
    * Geometrie -- Punkte, Linien, Polygone
    * Statistik -- z.B. Mittelwerte
    * Facetten -- Subplots
    * Koordinatensysteme -- kartesisch oder polar oder logarithmisch
    
  * Kombination der Teile:
  
    ![Einzeln](images/layers-einzeln.png) $\to$ ![Zusammen](images/layers-zusammen.png)

  * Eine Schicht besteht aus
  
    * Daten und ästhetische Zuordnungen (aes)
    * Statistischen Transformationen (stat)
    * Geometrischen Objekten (geom)
    * Positionsbestimmungen
    
  * Ein Plot besteht aus
  
    * Einem default-Datensatz und Zuordnungen von Variablen darin auf Ästhetiken
    * Ein oder mehrere Schichten (nicht notwendig mit zusätzlichen Daten)
    * Eine Skala pro Ästhetik-Zuordnung
    * Koordinatensystem
    * Facettenspezifikation
    
  * Eine statistische Transformation ist typischerweise eine *Zusammenfassung* von Daten.
  
    Beispiel: Glättung, die auf einer Menge von Punkten eine Kurve macht, die glatt (unendlich oft differenzierbar) ist.
    
    Die wichtigsten statistischen Transformationen, die in ggplot2 implementiert sind, haben wir teilweise schon kennen gelernt:
    
    * bin: Teile stetigen Bereich in Bins (Klassen) und zähle Punkte in jeder Klasse.
    * boxplot: Berechne Statistik für Boxplot
    * contour: Berechne Konturlinien
    * density: Berechne eindimensionale Dichteschätzung
    * identity: Identitätsabbildung, f (x) = x
    * jitter: Verändere jeden Wert mit einem kleinen Zufallswert
    * smooth: Geglätteter Mittelwert von y, gegeben x
    * summary: Summierte Werte von y für jedes x
    * unique: Entferne Duplikate

  * Eine Skala im Sinne der Grammatik der Grafiken kontrolliert die Zuordnung von Daten zu den ästhetischen Attributen.
  
    Beispiel: eine reelle Variable zwischen $0$ und $1$ lässt sich als Farbänderung von Blau zu Rot darstellen. Die Skala ist die Zuordnung aller Werte von $[0,1]$ auf Farbwerte. Die Umkehrfunktion dieser Zuordnung lässt sich zur Darstellung einer *Legende* nutzen.
    
    Beispiel: eine faktorielle Variable (etwa die Spezies im Iris-Datensatz) wird mit verschiedenen Symbolen dargestellt (etwa in einem Scatterplot). Die Zuordnung Ausprägung zu Symbol ist die Skala.
    
    Man kann auch mehrere Variablen auf eine Ästhetik abbilden, wenn man etwa im HSV-Farbmodell auf Saturation und Hue verschiedene Werte abbildet.
    
  * Farben
  
    Bei der Wahl von Farbskalen muss man auf die Unterscheidbarkeit achten, aber auch auf die späteren Betrachter\*innen der Plots:
    
    
```{figure} images/color-blind-friendly-palette-13.jpg
:width: 480px
:align: center
:name: color-friendly

Simulation der Farbwahrnehmung bei verschiedenen Arten der 'Sichtigkeit'
```

Eine Farbpalette, die auch bei eingeschränkter Farbwahrnehmung gut funktioniert, ist diese:
    
![Gute Palette](images/gute-palette.png)

Die Forschung über gut geeignete Farbpaletten ist nicht beendet - so gab es etwa auf der SciPy Konferenz 2022 den Vortrag [Development of Accessible, Aesthetically-Pleasing Color Sequences von Matthew Petroff](https://www.youtube.com/watch?v=Gapv8wR5DYU), dessen [Ergebnisse im Dezember 2024 in Matplotlib Version 3.10.0 eingeflossen sind](https://matplotlib.org/stable/users/prev_whats_new/whats_new_3.10.0.html#new-more-accessible-color-cycle).