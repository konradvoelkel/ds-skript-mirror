# Vorlesungsskript

[Link zur PDF-Version](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/ds-skript.pdf)

[Link zur Web-Version](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/)

## Aufzeichnungen

[Kanal mit Vorlesungsmitschnitten in der HHU-Mediathek](https://media.hhu.de/channel/Data-Science-SoSe-2025/167)

## Voraussetzungen

In diesem Text gehen wir davon aus, dass wir alle einmal 3 Semester Grundlagen der Mathematik gehört haben und wissen, was ein Vektor, eine Matrix und was die Ableitung einer Funktion in mehreren reellen Variablen sind. Außerdem haben wir alle bereits eine Programmiersprache gelernt und sind mit grundlegenden Datenstrukturen vertraut.

In der Schulzeit haben Sie womöglich bereits erste Kontakte mit Stochastik, Statistik, Wahrscheinlichkeitstheorie gemacht. Wir werden die Grundlagen zwar systematisch einführen, sodass hierbei keinerlei Vorkenntnisse über die 'Mathematik für Informatik' nötig sein müssten, aber wir werden das in für Mathematiker\*innen und Informatiker\*innen gewohnt zügigem Tempo tun. Wenn Sie also vorher noch einen Überblick gewinnen möchten, was Sie in der Schule hätten lernen können, ist dazu der [Online Mathematik Brückenkurs Plus Stochastik](https://www.ombplus.de/ombplus/link/OmbpluModuleStocha/Ueberb) eine sehr gute Adresse (frei, auf deutsch, didaktisch gut, in der gleichen Notation wie dieses Skript).

## Ziele

Unser Ziel ist eine Einführung in die "Data Science".
Sie soll Orientierung und Überblick geben und erste Anwendungen ermöglichen in deskriptiver, explorativer und inferentieller Datenanalyse, mit besonderem Blick auf das maschinelle Lernen.
Dabei kümmern wir uns um den notwendigen theoretischen Background in Stochastik und einige praktische Übungen in Python.
Darauf aufbauend ließe sich danach tiefer in die künstliche Intelligenz einsteigen. Dazu gibt es an der HHU das [Masterprogramm ,,Artificial Intelligence and Data Science''](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science).

Wenn Sie in der vollen Breite als Data Scientist arbeiten können wollen, sollten Sie zusätzlich zu dieser Vorlesung auch noch die Inhalte von Vorlesungen über Statistik, Datenbanken und Machine Learning kennen und einige Übung in konkreten Projekten haben. Je nach Einsatzbereich brauchen Sie noch Kenntnisse über Algorithmen für verteilte Systeme (Data Science 2) oder Deep Learning. Um flexibel in anderen Projekten mitarbeiten zu können, sollten Sie in der Lage sein, R Code zu lesen (und auch Julia könnte in der Zukunft wichtiger werden); zur Vertiefung der Programmierung selbst gibt es die Vorlesung *Einführung in Python* mit eigenem Skript, [Einführung in Python](https://eipy-skript-7dd28c.pages.cs.uni-duesseldorf.de/) (in Aufbau befindlich).
Das alles ist aber noch nicht notwendig für "Junior Data Analyst"-Jobs, die sich im Wesentlichen mit der Anwendung einfacher Statistik beim Erstellen von Reports und Dashboards befassen - dazu lernen Sie das Handwerkszeug in dieser Vorlesung und müssen lediglich je nach Anwendung konkrete Softwarepakete dazu lernen und üben.

Wir werden immer wieder auf zusätzliche Quellen stoßen, um einzelne Themen weiter zu vertiefen oder aus einer anderen Perspektive zu betrachten.
In der ersten Vorlesung haben wir uns einen Überblick verschafft, was Data Science ist und was wir machen werden.


**Kompetenzen**
Studierende sollen nach Absolvierung der Lehrveranstaltungen grundlegende Konzepte aus der Wahrscheinlichkeitsrechnung kompetent anwenden können, Kompetenzen in den Grundlagen der Wahrscheinlichkeitsrechnung für Machine Learning erlangen, ein Machine-Learning-Problem detailliert ausarbeiten können und grundlegende Machine-Learning-Algorithmen anwenden können. Sie sollen nach dem erfolgreichen Abschluss dieses Moduls in der Lage sein,
1. einen Datensatz explorativ zu analysieren,
1. Daten zur Weiterverarbeitung zu transformieren,
1. Teildatensätze zur Weiterverarbeitung zu wählen,
1. geeignete Datensätze zusammenzuführen,
1. Erkenntnisse in Daten zu beschreiben und zu visualisieren,
1. statistische Modelle anhand von Daten aufzustellen,
1. die Güte von Modellen zu bewerten,
1. und zur Klassifikation und Vorhersage weiterer Daten zu nutzen.

Dazu sind Sie damit vertraut, wie sich diese Aufgaben mit Python lösen lassen.

**Weitergehende Ziele.** Hinter dieser Liste steht ein einfacheres Bild davon, was Sie am Ende können sollen: einen Datensatz in die Hand nehmen und dazu sofort Fragestellungen formulieren *und* beantworten können. Teil der explorativen Datenanalyse ist genau dieses Generieren von Forschungsfragen. Dazu kommt, Fachartikel und Berichte lesen zu können, in denen statistisch argumentiert wird — und zu erkennen, wenn darin etwas nicht stimmt.

Beruflich öffnet das mehrere Türen. Die naheliegende ist eine Bewerbung als „Junior Data Scientist“ oder „Junior Data Analyst“; die zweite ist der Master [Artificial Intelligence and Data Science](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science), auf den dieser Kurs vorbereitet. Die dritte wird oft übersehen: Data-Science-Techniken sind auch dort nützlich, wo niemand diese Stellenbezeichnung trägt — in der Produktentwicklung (*data-driven design*), bei der Optimierung laufender Systeme anhand von Logfiles, bei Performancevergleichen als Grundlage für Entscheidungen (*data-driven decision making*), in der Qualitätskontrolle und überall dort, wo eine Komponente mit maschinellem Lernen in ein größeres System eingebaut werden soll.

**Was diese Vorlesung nicht ist**
Diese Vorlesung behandelt keine Data Science auf verteilten Systemen, das ist Thema von Data Science 2. Sie ist keine Einführung in Deep Learning, dafür gibt es die Vorlesung „Einführung in Deep Learning“. Sie führt nicht in R/RStudio oder andere Werkzeuge ein. Sie reduziert Data Science nicht auf den Aufruf von `model.fit()`: Wir programmieren Schätzer und Algorithmen selbst nach, um zu verstehen, was dabei passiert. Und sie ist kein Programmierkurs, Python-Vorkenntnisse werden aber nicht vorausgesetzt; was wir brauchen, steht im Kapitel [Einführung in Python](intro-python.ipynb).

Bei der Auswahl und Verarbeitung von Daten sowie der Bewertung von Modellen stellen sich auch ethische Fragen. Dieses Skript behandelt davon den rechtlichen Rahmen des Datenschutzes in einem eigenen Kapitel, als Glossar der wichtigsten Begriffe; die weitergehende ethische Diskussion ist nicht Teil des Skripts.


## Aufbau der Vorlesung

Die Vorlesung ruht auf drei Säulen. Die erste ist der *Background aus der Statistik*: Wahrscheinlichkeitsräume, Zufallsvariablen und Verteilungen, Erwartungswert und Varianz, Schätzer und Tests. Ohne diese Sprache lässt sich nicht sagen, was ein statistisches Modell behauptet und wann man ihm trauen darf.

Die zweite Säule ist die *Programmierübung mit Python*. Wir arbeiten mit Spielzeugdaten, die klein genug sind, um sie ganz zu überblicken, und lernen daran Numpy, Scipy, Matplotlib, Pandas und Scikit-Learn kennen. Die Übungsblätter sind der Ort, an dem aus dem Lesen ein Können wird.

Die dritte Säule sind *Algorithmen und Datenstrukturen*: Wir programmieren die wichtigsten Schätzer und Lernverfahren selbst nach, damit wir verstehen, was passiert, wenn man `model.fit()` aufruft.

Die Kapitel des Skripts folgen dieser Reihenfolge; das Inhaltsverzeichnis unten listet sie einzeln auf. Als zweite Sicht zeigt das folgende Diagramm, wie die Teile aufeinander aufbauen.

```{mermaid}
flowchart TB
  subgraph E["Einführung"]
    direction LR
    E1["Was ist Data Science?"] --> E2["Stochastik"] --> E3["Python"]
  end
  subgraph D["Diskrete Stochastik und Numpy"]
    direction LR
    D1["Zufallsvariablen, Verteilungen,<br/>Erwartungswert"] --> D2["Numpy"] --> D3["Diskrete Verteilungen,<br/>erste Exploration"]
  end
  subgraph S["Stetige Stochastik und Scipy"]
    direction LR
    S1["Stetige Verteilungen,<br/>Normalverteilung, Scipy"]
  end
  subgraph X["Explorative Datenanalyse"]
    direction LR
    X1["Deskriptive Statistik,<br/>Beispiele, Iris"] --> X2["Pandas, Daten putzen"]
  end
  subgraph M["Multivariate Stochastik"]
    direction LR
    M1["Kovarianz, multivariate<br/>Normalverteilung, relative Entropie"]
  end
  subgraph P["Datenschutz"]
    direction LR
    P1["Datenschutz-Glossar"]
  end
  subgraph L["Maschinelles Lernen"]
    direction LR
    L1["Clustering,<br/>Dimensionsreduktion"] --> L2["Statistische Modelle,<br/>Regression, Kernel"] --> L3["Tests, Modellwahl,<br/>Expectation Maximization"]
  end
  E --> D --> S --> X --> M --> P --> L
```

## Skript und Vorlesung

Alle Grundlagen der Mathematik, die Sie zur Bearbeitung der Übungsaufgaben benötigen, sind in diesem Skript enthalten (oder in den Eingangsvoraussetzungen der Vorlesung).

**Wozu ein Skript**
könnte man auch fragen. Hauptsächlich dient uns das Skript als Referenz und Leitfaden für die Übungsaufgaben. Es gibt in der Tat hervorragende MOOCs (massive open online courses) frei im WWW, vor allem wenn man gut Englisch spricht. Dieses Skript begleitet allerdings, im Gegensatz zu MOOCs, eine Präsenzlehrveranstaltung mit Übungsaufgaben. Es ist für den Lernerfolg entscheidend, die Übungsaufgaben engagiert zu bearbeiten und sich rege mit Kommiliton\*innen auszutauschen. Lehrpersonen können nur lehren, das Lernen müssen die Student\*innen noch selbst machen.

**KI-Werkzeuge**
Bei den Übungsblättern dürfen Sie KI-Werkzeuge wie Chatbots und Code-Assistenten benutzen, müssen das aber kennzeichnen: Schreiben Sie zur Abgabe dazu, welches Werkzeug Sie wofür eingesetzt haben. In der Klausur und im Midterm sind KI-Werkzeuge nicht erlaubt. Der Grund ist derselbe, aus dem es die Übungsaufgaben überhaupt gibt: Probieren Sie es erst einmal selbst, sonst lernt nur der Chatbot dazu.


## Lizenz

Dieses Vorlesungsskript steht unter der [Creative Commons Lizenz Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.de). <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de"><img src="https://mirrors.creativecommons.org/presskit/buttons/80x15/png/by-sa.png" height="20"/></a> Jeglicher Code außerdem unter der GPL3.

Davon ausgenommen sind gekennzeichnete Fremdinhalte, die unter ihrer jeweils eigenen Lizenz stehen: die eingebundenen xkcd-Comics (CC BY-NC 2.5), das Venn-Diagramm von Drew Conway (CC BY-NC 3.0) und der Melbourne-Housing-Datensatz von Anthony Pino (CC BY-NC-SA 4.0). Bei jedem dieser Inhalte steht die Quelle an Ort und Stelle.

## Inhaltsverzeichnis

```{tableofcontents}
```

## Quellen

Nichts in diesem Buch ist neu, bis auf die Reihenfolge und sicherlich der ein oder andere Tippfehler.
Die Hauptquellen für dieses Skript sind {cite}`georgii2015stochastik` für die Wahrscheinlichkeitstheorie,
und {cite}`joelgrusdsfs` für den Python-Teil.
In beiden Büchern ist Stoff für mehr als eine Vorlesung und die Zielgruppen sind nicht deckungsgleich mit unserer Vorlesung.
Ein lesenswertes ergänzendes Buch mit einigen weiteren Mathematik-Grundlagen (gerade lineare Algebra) ist {cite}`Deisenroth2020`.
Wer nicht gern in Paket-Dokumentationen stöbert, ist für Numpy, Pandas und Matplotlib vielleicht glücklicher mit dem Buch von Jake VanderPlas, welches sich sogar umsonst online lesen lässt {cite}`pythondsh`.
