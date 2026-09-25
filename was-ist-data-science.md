# Was ist Data Science?

## Vorab: ein Tabellenblatt, das Europa sparen ließ

Im Jahr 2010 veröffentlichten die Harvard-Ökonomen Carmen Reinhart und Kenneth Rogoff eine Auswertung von zwei Jahrhunderten Staatsschulden und Wirtschaftswachstum {cite}`reinhart2010`. Ihr Befund: Sobald die Schulden eines Landes 90 % seiner Wirtschaftsleistung übersteigen, schrumpft die Wirtschaft im Mittel, um 0,1 % pro Jahr. Die Zahl machte Karriere. Sie stand im Haushaltsentwurf des US-Kongresses, der EU-Währungskommissar zitierte sie, und sie war ein Argument für die Sparpolitik in Europa nach der Finanzkrise.

Drei Jahre später bekam Thomas Herndon, Doktorand in Amherst, in einem Seminar die Aufgabe, eine bekannte Studie nachzurechnen. Er bat um das Tabellenblatt und fand darin einen markierten Zellbereich, der fünf Zeilen zu kurz war: Australien, Österreich, Belgien, Kanada und Dänemark fehlten im Mittelwert, alles Länder mit hohen Schulden und ordentlichem Wachstum. Dazu kamen ausgelassene Jahre und eine ungewöhnliche Gewichtung. Mit allen drei Korrekturen wurden aus $-0{,}1\,\%$ Wachstum $+2{,}2\,\%$ {cite}`herndon2014`. Die Klippe bei 90 % gab es nicht.

Daran ist alles drin, worum es in diesem Kurs geht. Die Rohzahlen waren echt und öffentlich; die Auswertung war eine Handvoll Mittelwerte; und trotzdem lag das Ergebnis daneben, weil niemand nachgesehen hatte, welche Zeilen eigentlich in der Rechnung stecken, und weil eine Tabellenkalkulation so etwas nicht zeigt. Es brauchte keine bessere Mathematik, um den Fehler zu finden, sondern jemanden, der die Daten noch einmal von vorn anfasst. Genau das üben wir: Daten laden, statt sie anzuklicken; jede Kennzahl mit dem Blick auf die Zeilen prüfen, aus denen sie entsteht; und Rechnungen so aufschreiben, dass andere sie wiederholen können. Deshalb arbeiten wir in diesem Kurs mit Python und nicht mit Excel, und deshalb hat das Kapitel [Daten putzen](data-cleaning.ipynb) den Grundsatz, jede Änderung an den Daten zu protokollieren.

## Was ist "Data"?

Gerhard Goos, Vorlesungen über Informatik Band 1:

> Die Darstellung einer Mitteilung durch die zeitliche Veränderung einer physikalischen Größe heißt ein *Signal*.
Wenn wir bei der Darstellung und Weitergabe einer Mitteilung vom verwandten Medium und den Einzelheiten der Signale und Signalparameter abstrahieren, heißt die Mitteilung eine *Nachricht*.

> Die Kenntnisse, die man benötigt, um einer Nachricht Bedeutung zuzuordnen, nennen wir einen *Kontext* oder ein Bezugssystem.
Die zugeordnete Bedeutung heißt eine *Information*.
Man nennt das Paar <Nachricht, zugeordnete Information> ein *Datum*. Der Plural ist Daten (englisch data).

Eine CSV-Datei können wir also genau dann "Daten" nennen, wenn wir einen Kontext haben, um den darin enthaltenen Bitstrings Bedeutung zuzuordnen. Viel von diesem Kontext nehmen wir meist gar nicht wahr - wir gehen z.B. davon aus, dass sich eine CSV-Datei mit einem Texteditor öffnen lässt und die Inhalte so als Strings kodiert sind, dass wir durch blosses Betrachten die Datentypen erraten könnten. Welche Felder einer Tabelle aber genau wie kodiert sind, ist oft nicht der Tabelle selbst zu entnehmen, dafür braucht man Metadaten.

Wenn wir etwa die Antworten zu einer Single-Choice-Frage betrachten, so ist meist in der Nachricht erfasst, welche Nr. die gewählte Antwort hat, nicht aber der String der tatsächlichen Antwort. Diesen notiert man in einem *Code Book*, einer Kodierungstabelle. Um also die Antworten als Daten begreifen zu können, müssen wir auf die Kodierungstabelle zurückgreifen.

(ein-bunter-mix)=
## Ein bunter Mix

```{figure} images/conway_data_science_venn_diagram.png
:width: 400px
:align: center
:name: conway-venn

Das „Data Science Venn Diagram“ von Drew Conway (2013), CC BY-NC 3.0, Quelle: drewconway.com/zia/2013/3/26/the-data-science-venn-diagram
```

Drew Conway hat 2013 die bis heute meistzitierte Antwort auf die Frage gegeben, was Data Science ausmacht: die Schnittmenge von drei Kreisen. *Hacking Skills* heißt, mit Daten in beliebigen Formaten programmierend umgehen zu können, *Math & Statistics Knowledge* heißt, zu wissen, was eine Rechnung auf diesen Daten überhaupt aussagt, und *Substantive Expertise* ist die Fachkenntnis über den Bereich, aus dem die Daten stammen. Je zwei der Kreise ergeben etwas Bekanntes: Hacking und Statistik zusammen sind *Machine Learning*, Statistik und Fachkenntnis sind *Traditional Research*, so wie sie in den empirischen Wissenschaften seit langem betrieben wird. Hacking und Fachkenntnis ohne Statistik nennt Conway die *Danger Zone*: Wer Daten einlesen und ein Verfahren darauf loslassen kann und die Ergebnisse fachlich plausibel findet, wird sie auch glauben, ohne beurteilen zu können, ob sie mehr als Zufall sind. Das Tabellenblatt vom Anfang dieses Kapitels ist ein Beispiel dafür, dass diese Zone auch für Expert\*innen gefährlich ist. Diese Vorlesung liefert den Statistik-Kreis und übt den Hacking-Kreis an kleinen Datensätzen; die Fachkenntnis bringen Sie später aus dem Bereich mit, in dem Sie arbeiten.

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

Ein signifikanter Teil der Arbeit eines Data Scientist besteht in der Aufbereitung von Daten, dem sogenannten "Daten schrubben". Dabei kommen viele klassische Programmiertechniken zum Einsatz, etwa reguläre Ausdrücke und Kenntnis über Industriestandards bei Datentypen und die Abweichungen von Standards, die in der Praxis auftauchen. Die Liste ist erstaunlich konkret: Zeit- und Datumsformate samt Zeitzonen und Sommerzeitumstellung, GIS-Datenformate für alles Räumliche, Ländercodes (von denen es mehrere konkurrierende Systeme gibt), Unicode und die Encodings, die es ersetzen sollte, und die gängigen Abweichungen vom CSV-Standard — Trennzeichen, Anführungszeichen, Zeilenumbrüche mitten im Feld. Das Handwerk dazu hat in diesem Buch ein eigenes Kapitel, [Daten putzen](data-cleaning.ipynb).

Drei Punkte dieser Liste lernt man allerdings in keiner Vorlesung: Geduld, Übung und Fachkenntnisse über das Anwendungsgebiet. Ob ein Blutdruckwert von $400$ ein Messfehler ist oder ein Alter von $0$ ein fehlender Wert, steht in keinem Datenformat — das weiß nur, wer das Gebiet kennt oder jemanden fragt, der es kennt.
Auch im maschinellen Lernen, etwa beim Deep Learning, kann man durch Pflegen der Trainingsdaten erheblich bessere Ergebnisse erzielen.



## Weiterführendes



**Karriere in Data Science**

[Robinson und Nolis: Build a Career in Data Science](https://www.manning.com/books/build-a-career-in-data-science)

Dazu gibt es auch einen [einstündigen Podcast mit den Autorinnen](https://talkpython.fm/episodes/show/262/build-a-career-in-data-science).


**State of Data Science 2021**

Eine Stunde Podcast [State of Data Science in 2021 with Stan Seibert](https://talkpython.fm/episodes/show/333/state-of-data-science-in-2021)

**State of Data Science 2024**

Ein Blogpost vom IDE-Entwickler JetBrains [State of Data Science in 2024: 6 Key Data Science Trends](https://blog.jetbrains.com/pycharm/2024/12/the-state-of-data-science/)

Ein interessanter Kontrast ist dieser Artikel von Mike Loukides von O'Reilly: [What is data science?](http://radar.oreilly.com/2010/06/what-is-data-science.html) aus dem Jahr 2010. Man sieht schnell: die Werkzeuge und Softwarepakete sind im Wandel, und manches, was 2010 noch besonders spannend schien, ist heute schon vergessen. Man sieht aber auch: Data Science ist kein einfacher Hype, der bald vorüber zieht, sondern ein globaler Trend, der seit über 10 Jahren in der Entwicklung ist, und Conways drei Kreise aus dem Abschnitt [Ein bunter Mix](#ein-bunter-mix) beschreiben ihn noch immer treffend. Wenn Etiketten wie "Data Mining", "Big Data" und vielleicht auch "Data Science" im Laufe der Zeit an Bedeutung verlieren, so besteht doch kein Zweifel, dass statistische Methoden und maschinelles Lernen für lange Zeit eine wachsende Bedeutung in Informatik und Gesellschaft spielen werden.

## Wie es weitergeht

Bevor wir mit Daten arbeiten, brauchen wir eine präzise Sprache für Zufall und Unsicherheit. Das nächste Kapitel liefert sie: Wahrscheinlichkeitsräume, Ereignisse, Zufallsvariablen. Es enthält zwei Exkurse zum Maßproblem, die als Hintergrund gedacht sind und beim ersten Lesen übersprungen werden können; der eigentliche Formalismus, den wir im ganzen Kurs verwenden, beginnt beim Abschnitt *Formalismus*.
