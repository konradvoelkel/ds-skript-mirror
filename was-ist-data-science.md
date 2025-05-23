# Was ist Data Science?

## Was ist "Data"?

Gerhard Goos, Vorlesungen über Informatik Band 1:

> Die Darstellung einer Mitteilung durch die zeitliche Veränderung einer physikalischen Größe heißt ein *Signal*.
Wenn wir bei der Darstellung und Weitergabe einer Mitteilung vom verwendetem Medium und den Einzelheiten der Signale und Signalparameter abstrahieren, heißt die Mitteilung eine *Nachricht*.

> Die Kenntnisse, die man benötigt, um einer Nachricht Bedeutung zuzuordnen, nennen wir einen *Kontext* oder ein Bezugssystem.
Die zugeordnete Bedeutung heißt eine *Information*.
Man nennt das Paar <Nachricht, zugeordnete Information> ein *Datum*. Der Plural ist Daten (englisch data).

Eine CSV-Datei können wir also genau dann "Daten" nennen, wenn wir einen Kontext haben, um den darin enthaltenen Bitstrings Bedeutung zuzuordnen. Viel von diesem Kontext nehmen wir meist gar nicht wahr - wir gehen z.B. davon aus, dass sich eine CSV-Datei mit einem Texteditor öffnen lässt und die Inhalte so als Strings kodiert sind, dass wir durch blosses Betrachten die Datentypen erraten könnten. Welche Felder einer Tabelle aber genau wie kodiert sind, ist oft nicht der Tabelle selbst zu entnehmen, dafür braucht man Metadaten.

Wenn wir etwa die Antworten zu einer Single-Choice-Frage betrachten, so ist meist in der Nachricht erfasst, welche Nr. die gewählte Antwort hat, nicht aber der String der tatsächlichen Antwort. Diesen notiert man in einem *Code Book*, einer Kodierungstabelle. Um also die Antworten als Daten begreifen zu können, müssen wir auf die Kodierungstabelle zurückgreifen.


## Was ist ein Data Scientist?

> Nearly all \[...\] working data scientists make their daily bread and butter through data collection and data cleaning; building dashboards and reports; data visualization; statistical inference; communicating results to key stakeholders; and convincing decision makers of their results.
[Hugo Bowne-Anderson, Harvard Business Review, 2018](http://hbr.org/2018/08/what-data-scientists-really-do-according-to-35-data-scientists)

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

Ein signifikanter Teil der Arbeit eines Data Scientist besteht in der Aufbereitung von Daten, dem sogenannten "Daten schrubben". Dabei kommen viele klassische Programmiertechniken zum Einsatz, etwa reguläre Ausdrücke und Kenntnis über Industriestandards bei Datentypen (GIS, Datumsangaben, Unicode und andere Encodings, CSV) und die Abweichung von Standards, die in der Praxis auftauchen.
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
