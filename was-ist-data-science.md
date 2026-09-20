# Was ist Data Science?

## Was ist "Data"?

Gerhard Goos, Vorlesungen über Informatik Band 1:

> Die Darstellung einer Mitteilung durch die zeitliche Veränderung einer physikalischen Größe heißt ein *Signal*.
Wenn wir bei der Darstellung und Weitergabe einer Mitteilung vom verwandten Medium und den Einzelheiten der Signale und Signalparameter abstrahieren, heißt die Mitteilung eine *Nachricht*.

> Die Kenntnisse, die man benötigt, um einer Nachricht Bedeutung zuzuordnen, nennen wir einen *Kontext* oder ein Bezugssystem.
Die zugeordnete Bedeutung heißt eine *Information*.
Man nennt das Paar <Nachricht, zugeordnete Information> ein *Datum*. Der Plural ist Daten (englisch data).

Eine CSV-Datei können wir also genau dann "Daten" nennen, wenn wir einen Kontext haben, um den darin enthaltenen Bitstrings Bedeutung zuzuordnen. Viel von diesem Kontext nehmen wir meist gar nicht wahr - wir gehen z.B. davon aus, dass sich eine CSV-Datei mit einem Texteditor öffnen lässt und die Inhalte so als Strings kodiert sind, dass wir durch blosses Betrachten die Datentypen erraten könnten. Welche Felder einer Tabelle aber genau wie kodiert sind, ist oft nicht der Tabelle selbst zu entnehmen, dafür braucht man Metadaten.

Wenn wir etwa die Antworten zu einer Single-Choice-Frage betrachten, so ist meist in der Nachricht erfasst, welche Nr. die gewählte Antwort hat, nicht aber der String der tatsächlichen Antwort. Diesen notiert man in einem *Code Book*, einer Kodierungstabelle. Um also die Antworten als Daten begreifen zu können, müssen wir auf die Kodierungstabelle zurückgreifen.


## Was ist ein Data Scientist?

> Nearly all \[...\] working data scientists make their daily bread and butter through data collection and data cleaning; building dashboards and reports; data visualization; statistical inference; communicating results to key stakeholders; and convincing decision makers of their results.
[Hugo Bowne-Anderson, Harvard Business Review, 2018](http://hbr.org/2018/08/what-data-scientists-really-do-according-to-35-data-scientists)

Kurz gesagt: Der größte Teil der täglichen Arbeit ist Datenbeschaffung, Datenbereinigung und Kommunikation der Ergebnisse, nicht die Modellierung, die in Kursen wie diesem den meisten Platz einnimmt.

> But how do you find data scientists? Whenever someone asks that question, I
refer them back to a more fundamental question: what makes a good data
scientist? Here is what I look for:
• Technical expertise: the best data scientists typically have deep expertise
in some scientific discipline.
• Curiosity: a desire to go beneath the surface and discover and distill a
problem down into a very clear set of hypotheses that can be tested.
• Storytelling: the ability to use data to tell a story and to be able to communicate it effectively.
• Cleverness: the ability to look at a problem in different, creative ways.
All the top data scientists share an innate sense of curiosity. Their curiosity is
broad, and extends well beyond their day-to-day activities. They are interested
in understanding many different areas of the company, business, industry, and
technology. As a result, they are often able to bring disparate areas together in
a novel way. For example, I’ve seen data scientists look at sales processes and
realize that by using data in new ways they can make the sales team far more
efficient. I’ve seen data scientists apply novel DNA sequencing techniques to
find patterns of fraud.
What unifies all these people? They all have strong technical backgrounds.
Most have advanced degrees (although I’ve worked with several outstanding
data scientists who haven’t graduated from college). But the real unifying
thread is that all have had to work with a tremendous amount of data before
starting to work on the “real” problem
[DJ Patil: Building Data Science Teams (2011), What Makes a Data Scientist? (p.11ff)](https://www.datascienceassn.org/sites/default/files/Building%20Data%20Science%20Teams.pdf)

Patil beschreibt also, woran man gute Data Scientists erkennt: an fachlicher Tiefe in irgendeiner Disziplin und vor allem an der Neugier, ein Problem so lange zu zerlegen, bis daraus überprüfbare Hypothesen werden.

Ein signifikanter Teil der Arbeit eines Data Scientist besteht in der Aufbereitung von Daten, dem sogenannten "Daten schrubben". Dabei kommen viele klassische Programmiertechniken zum Einsatz, etwa reguläre Ausdrücke und Kenntnis über Industriestandards bei Datentypen (GIS, Datumsangaben, Unicode und andere Encodings, CSV) und die Abweichung von Standards, die in der Praxis auftauchen. Das Handwerk dazu hat in diesem Buch ein eigenes Kapitel, [Daten putzen](data-cleaning.ipynb).
Auch im maschinellen Lernen, etwa beim Deep Learning, kann man durch Pflegen der Trainingsdaten erheblich bessere Ergebnisse erzielen.



## Weiterführendes



**Karriere in Data Science**

[Robinson und Nolis: Build a Career in Data Science](https://www.manning.com/books/build-a-career-in-data-science)

Dazu gibt es auch einen [einstündigen Podcast mit den Autorinnen](https://talkpython.fm/episodes/show/262/build-a-career-in-data-science).


**State of Data Science 2021**

Eine Stunde Podcast [State of Data Science in 2021 with Stan Seibert](https://talkpython.fm/episodes/show/333/state-of-data-science-in-2021)

**State of Data Science 2024**

Ein Blogpost vom IDE-Entwickler JetBrains [State of Data Science in 2024: 6 Key Data Science Trends](https://blog.jetbrains.com/pycharm/2024/12/the-state-of-data-science/)

Ein interessanter Kontrast ist dieser Artikel von Mike Loukides von O'Reilly: [What is data science?](http://radar.oreilly.com/2010/06/what-is-data-science.html) aus dem Jahr 2010. Man sieht schnell: die Werkzeuge und Softwarepakete sind im Wandel, und manches, was 2010 noch besonders spannend schien, ist heute schon vergessen. Man sieht aber auch: Data Science ist kein einfacher Hype, der bald vorüber zieht, sondern ein globaler Trend, der seit über 10 Jahren in der Entwicklung ist. Wenn Etiketten wie "Data Mining", "Big Data" und vielleicht auch "Data Science" im Laufe der Zeit an Bedeutung verlieren, so besteht doch kein Zweifel, dass statistische Methoden und maschinelles Lernen für lange Zeit eine wachsende Bedeutung in Informatik und Gesellschaft spielen werden.

## Ein erstes Beispiel: das Simpson-Paradoxon

Bevor wir im nächsten Kapitel die Sprache der Stochastik aufbauen, ein Beispiel, für das man nur Prozentrechnung braucht und das trotzdem zeigt, warum Datenanalyse mehr ist als Ausrechnen. Es stammt aus einer medizinischen Studie über zwei Behandlungen von Nierensteinen {cite}`charig1986`; wir nennen die Behandlungen einfach A und B. Beide wurden an je 350 Patient\*innen angewendet, und "Erfolg" ist das, was die Mediziner\*innen als Erfolg definiert haben.

| Behandlung | Patient\*innen | Erfolge | Erfolgsquote |
|---|---|---|---|
| A | 350 | 273 | 78 % |
| B | 350 | 289 | 83 % |

Stellen Sie sich vor, Sie haben Nierensteine. Welche Behandlung wählen Sie? Die meisten sagen B.

Nun gibt es aber nicht einfach Nierensteine, sondern kleine und große. Teilen wir die Tabelle danach auf:

| Behandlung | kleine Steine | große Steine |
|---|---|---|
| A | 81 von 87, also 93 % | 192 von 263, also 73 % |
| B | 234 von 270, also 87 % | 55 von 80, also 69 % |

Bei kleinen Steinen ist A besser, bei großen Steinen ist A besser. Wenn Sie kleine Steine haben, wollen Sie A; wenn Sie große Steine haben, wollen Sie A. Nur wenn Sie nicht wissen, wie groß Ihre Steine sind, wollen Sie B? Das kann nicht stimmen, denn Ihre Steine sind entweder klein oder groß.

Die Auflösung steckt in den absoluten Zahlen, nicht in den Prozenten. Behandlung A wurde fast nur bei großen Steinen eingesetzt (263 von 350), Behandlung B fast nur bei kleinen (270 von 350). Große Steine sind schwerer zu behandeln, also zieht die große Gruppe der schweren Fälle die Gesamtquote von A nach unten, während B von der großen Gruppe der leichten Fälle profitiert. Die Ärzt\*innen haben die Therapie nach der Steingröße gewählt, und die Steingröße bestimmt den Erfolg. Eine solche Variable, die sowohl die Gruppenzugehörigkeit als auch das Ergebnis beeinflusst, heißt **Confounder** (Störvariable). Die Pointe: B sollte man nur wählen, wenn man sich damit aussuchen darf, kleine Steine zu haben.

Dieses Phänomen heißt **Simpson-Paradoxon**: Ein Zusammenhang, der in der Gesamtheit gilt, kann sich in jeder einzelnen Untergruppe umkehren. Es tritt nicht nur bei Tabellen mit Prozenten auf, sondern genauso bei stetigen Merkmalen:

```{figure} images/simpson-paradoxon.png
:width: 560px
:align: center
:name: simpson-paradoxon

Simpson-Paradoxon mit stetigen Merkmalen: Innerhalb jeder Gruppe steigt $y$ mit $x$, über alle Punkte zusammen fällt der Trend.
```

Im Nierenstein-Beispiel kannten wir die Steingröße. Oft ist die Variable, die die Gruppen erzeugt, aber gar nicht in der Tabelle: Dann sehen wir nur die Punktwolke rechts, ohne Farben, und der fallende Trend sieht völlig überzeugend aus. Eine solche nicht beobachtete Variable heißt **latente Variable**. An dem Wort ist nichts Geheimnisvolles, es heißt nur "nicht beobachtet". Die Gesamtverteilung ist dann eine **Mischung** aus zwei Gruppenverteilungen, und die Frage, ob sich eine Punktwolke in solche Gruppen zerlegen lässt, wird uns durch das ganze Buch begleiten: bei der [kontaminierten Normalverteilung](wichtigste-stetige-verteilungen.ipynb), beim [Clustering mit k-Means](kmeans.ipynb) und schließlich bei den [gemischten Gaußschen Modellen](expectation-maximization.ipynb). Dass Kovarianz und Korrelation genau in diese Falle laufen, sehen wir im Kapitel [Kovarianz](kovarianz.md).

:::{admonition} Take-Home-Message
Bevor Sie eine Tabelle aggregieren oder einen Trend ablesen, fragen Sie, ob die Daten heimlich aus mehreren Stichproben zusammengesetzt sind. Wenn ja, rechnen Sie je Gruppe. Und rechnen Sie mit absoluten Zahlen nach, nicht nur mit Prozenten.
:::

:::{admonition} Aufgabe: Simpson im Iris-Datensatz
:class: tip
Der Iris-Datensatz (den wir ab dem Kapitel [Iris](iris.ipynb) oft benutzen) enthält für 150 Pflanzen aus drei Spezies unter anderem Kelchblattlänge und Kelchblattbreite. Bestimmen Sie den Zusammenhang zwischen den beiden Maßen einmal über alle 150 Pflanzen und einmal je Spezies. Was beobachten Sie?
:::

:::{admonition} Lösung
:class: dropdown
Über alle Pflanzen hinweg ist der Zusammenhang schwach negativ (Korrelationskoeffizient etwa $-0{,}12$): breitere Kelchblätter gehen mit kürzeren einher. Innerhalb jeder Spezies ist er deutlich positiv (setosa etwa $0{,}74$, versicolor $0{,}53$, virginica $0{,}46$). Die Spezies ist der Confounder: *setosa* hat kurze, breite Kelchblätter, die anderen beiden lange, schmale. Wer die Spezies nicht kennt, sieht einen Trend, der in keiner Gruppe gilt. Wie man die Zahlen berechnet, steht im Kapitel [Kovarianz](kovarianz.md).
:::

## Wie es weitergeht

Bevor wir mit Daten arbeiten, brauchen wir eine präzise Sprache für Zufall und Unsicherheit. Das nächste Kapitel liefert sie: Wahrscheinlichkeitsräume, Ereignisse, Zufallsvariablen. Es enthält zwei Exkurse zum Maßproblem, die als Hintergrund gedacht sind und beim ersten Lesen übersprungen werden können; der eigentliche Formalismus, den wir im ganzen Kurs verwenden, beginnt beim Abschnitt *Formalismus*.
