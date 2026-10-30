---
title: "Data Science: von der Stochastik zum Machine Learning mit Python"
short_title: "Vorlesungsskript"
description: "Vorlesungsskript Data Science: von Wahrscheinlichkeitsräumen bis zum maschinellen Lernen — mit Numpy und Pandas, und den Lernverfahren selbst programmiert."
# Nötig *zusätzlich* zum project.thumbnail in myst.yml: das Projekt-Thumbnail greift nur,
# wo eine Seite gar kein Bild hat. Diese Seite hat eines — den CC-Knopf im Lizenzabschnitt
# —, und ohne diese Zeile wäre ausgerechnet die Startseite die einzige, die weiter den
# 267x50-Knopf als Vorschaukarte anbietet (am gebauten HTML geprüft).
thumbnail: images/social-card.png
date: 2026-10-16
---

Dieses Skript ist eine Einführung in die Data Science, die bei der Stochastik anfängt und beim
maschinellen Lernen aufhört, ohne dazwischen eine Lücke zu lassen. Der Unterschied zu einem
Werkzeugkurs steckt in der dritten Säule unten: Die Verfahren werden hier nicht aufgerufen,
sondern nachprogrammiert. Wer wissen will, was `model.fit()` eigentlich tut, schreibt es einmal
selbst — k-Means, die Hauptkomponentenanalyse, die Regression, den EM-Algorithmus. Alles, was man
dafür braucht, steht in diesem Buch.

## Aufbau der Vorlesung

Die Vorlesung ruht auf drei Säulen. Die erste ist der *Background aus der Statistik*:
Wahrscheinlichkeitsräume, Zufallsvariablen und Verteilungen, Erwartungswert und Varianz, Schätzer
und Tests. Ohne diese Sprache lässt sich nicht sagen, was ein statistisches Modell behauptet und
wann man ihm trauen darf.

Die zweite Säule ist die *Programmierübung mit Python*. Wir arbeiten mit Spielzeugdaten, die klein
genug sind, um sie ganz zu überblicken, und lernen daran Numpy, Scipy, Matplotlib, Pandas und
scikit-learn kennen. Die Übungsblätter sind der Ort, an dem aus dem Lesen ein Können wird.

Die dritte Säule sind *Algorithmen und Datenstrukturen*: Wir programmieren die wichtigsten
Schätzer und Lernverfahren selbst nach, damit wir verstehen, was passiert, wenn man `model.fit()`
aufruft.

Die Kapitel des Skripts folgen dieser Reihenfolge; das Inhaltsverzeichnis unten listet sie einzeln
auf. Als zweite Sicht zeigt das folgende Diagramm, wie die Teile aufeinander aufbauen.

```{figure} images/course-structure.svg
:alt: Sieben Teile nacheinander, jeder führt zum nächsten: Einführung (Was ist Data Science?, Stochastik, Python); Diskrete Stochastik und Numpy (Zufallsvariablen, Verteilungen, Erwartungswert; Numpy; Diskrete Verteilungen, erste Exploration); Stetige Stochastik und Scipy (Stetige Verteilungen, Normalverteilung, Scipy); Explorative Datenanalyse (Deskriptive Statistik, Beispiele, Iris; Pandas, Daten putzen); Multivariate Stochastik (Kovarianz, multivariate Normalverteilung, relative Entropie); Datenschutz (Datenschutz-Glossar); Maschinelles Lernen (Clustering, Dimensionsreduktion; Statistische Modelle, Regression, Kernel; Tests, Modellwahl, Expectation Maximization).
:width: 100%

Wie die Teile der Vorlesung aufeinander aufbauen.
```

## Was Sie danach können

Unser Ziel ist eine Einführung in die „Data Science“. Sie soll Orientierung und Überblick geben
und erste Anwendungen ermöglichen in deskriptiver, explorativer und inferentieller Datenanalyse,
mit besonderem Blick auf das maschinelle Lernen. Dabei kümmern wir uns um den notwendigen
theoretischen Background in Stochastik und einige praktische Übungen in Python.

Hinter der Kompetenzliste des Modulhandbuchs (sie steht im
[Organisatorischen](orga.md)) steht ein einfacheres Bild davon, was Sie am Ende können sollen:
einen Datensatz in die Hand nehmen und dazu sofort Fragestellungen formulieren *und* beantworten
können. Teil der explorativen Datenanalyse ist genau dieses Generieren von Forschungsfragen. Dazu
kommt, Fachartikel und Berichte lesen zu können, in denen statistisch argumentiert wird — und zu
erkennen, wenn darin etwas nicht stimmt.

Beruflich öffnet das mehrere Türen. Die naheliegende ist eine Bewerbung als „Junior Data
Scientist“ oder „Junior Data Analyst“; die zweite ist der Master [Artificial Intelligence and Data
Science](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science), auf den dieser
Kurs vorbereitet. Die dritte wird oft übersehen: Data-Science-Techniken sind auch dort nützlich,
wo niemand diese Stellenbezeichnung trägt — in der Produktentwicklung (*data-driven design*), bei
der Optimierung laufender Systeme anhand von Logfiles, bei Performancevergleichen als Grundlage
für Entscheidungen (*data-driven decision making*), in der Qualitätskontrolle und überall dort, wo
eine Komponente mit maschinellem Lernen in ein größeres System eingebaut werden soll.

## Was diese Vorlesung nicht ist

Diese Vorlesung behandelt keine Data Science auf verteilten Systemen, das ist Thema von Data
Science 2. Sie ist keine Einführung in Deep Learning, dafür gibt es die Vorlesung „Einführung in
Deep Learning“. Sie führt nicht in R/RStudio oder andere Werkzeuge ein. Sie reduziert Data Science
nicht auf den Aufruf von `model.fit()`: Wir programmieren Schätzer und Algorithmen selbst nach, um
zu verstehen, was dabei passiert. Und sie ist kein Programmierkurs, Python-Vorkenntnisse werden
aber nicht vorausgesetzt; was wir brauchen, steht im Kapitel [Einführung in
Python](intro-python.ipynb).

Bei der Auswahl und Verarbeitung von Daten sowie der Bewertung von Modellen stellen sich auch
ethische Fragen. Dieses Skript behandelt davon den rechtlichen Rahmen des Datenschutzes in einem
eigenen Kapitel, als Glossar der wichtigsten Begriffe; die weitergehende ethische Diskussion ist
nicht Teil des Skripts.

## Voraussetzungen

In diesem Text gehen wir davon aus, dass wir alle einmal 3 Semester Grundlagen der Mathematik
gehört haben und wissen, was ein Vektor, eine Matrix und was die Ableitung einer Funktion in
mehreren reellen Variablen sind. Außerdem haben wir alle bereits eine Programmiersprache gelernt
und sind mit grundlegenden Datenstrukturen vertraut.

In der Schulzeit haben Sie womöglich bereits erste Kontakte mit Stochastik, Statistik,
Wahrscheinlichkeitstheorie gemacht. Wir werden die Grundlagen zwar systematisch einführen, sodass
hierbei keinerlei Vorkenntnisse über die 'Mathematik für Informatik' nötig sein müssten, aber wir
werden das in für Mathematiker\*innen und Informatiker\*innen gewohnt zügigem Tempo tun. Wenn Sie
also vorher noch einen Überblick gewinnen möchten, was Sie in der Schule hätten lernen können, ist
dazu der [Online Mathematik Brückenkurs Plus
Stochastik](https://www.ombplus.de/ombplus/link/OmbpluModuleStocha/Ueberb) eine sehr gute Adresse
(frei, auf deutsch, didaktisch gut, in der gleichen Notation wie dieses Skript).

Alle Grundlagen der Mathematik, die Sie zur Bearbeitung der Übungsaufgaben benötigen, sind in
diesem Skript enthalten (oder in den Eingangsvoraussetzungen der Vorlesung).

## Das Skript lesen

Sie lesen die Web-Ausgabe. Dasselbe Buch gibt es auch als
[PDF zum Herunterladen](https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/ds-skript.pdf).

Dieses Skript gibt es außerdem auf Englisch: [Data Science — lecture notes from stochastics to
machine learning with Python](https://datascience.konradvoelkel.com/). Die englische Ausgabe ist
eine Übersetzung dieses Originals und folgt ihm; wo beide auseinanderlaufen, gilt die deutsche
Fassung.

Dieses Skript ist eines von drei Vorlesungsskripten von [Konrad
Völkel](https://www.konradvoelkel.com/), die alle frei zu lesen sind. Die beiden anderen
sind [Einführung in Python](https://eipy-skript-7dd28c.pages.cs.uni-duesseldorf.de/), das
Python als zweite Programmiersprache einführt, und [Einführung in Deep
Learning](https://eidl-skript-131e30.pages.cs.uni-duesseldorf.de/), das an dieses Skript
anschließt. Alle drei stehen mit ihren PDF-Ausgaben und den Vorlesungsaufzeichnungen auf
seiner [Seite zur Lehre](https://www.konradvoelkel.com/teaching/).

Zum Betrieb der Vorlesung an der HHU — Aufzeichnungen, Folien, Übungsbetrieb und die Regeln für
KI-Werkzeuge — gibt es die Seite [Organisatorisches](orga.md).

Wir werden immer wieder auf zusätzliche Quellen stoßen, um einzelne Themen weiter zu vertiefen
oder aus einer anderen Perspektive zu betrachten. In der ersten Vorlesung haben wir uns einen
Überblick verschafft, was Data Science ist und was wir machen werden.

## Inhaltsverzeichnis

```{tableofcontents}
```

## Lizenz

Verfasst von [Dr. Konrad Völkel](https://www.konradvoelkel.com/), Heinrich-Heine-Universität Düsseldorf.

Dieses Vorlesungsskript steht unter der [Creative Commons Lizenz Namensnennung – Weitergabe unter gleichen Bedingungen 4.0 (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.de). <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de"><img src="https://mirrors.creativecommons.org/presskit/buttons/80x15/png/by-sa.png" height="20" alt="Lizenzknopf Creative Commons Namensnennung – Weitergabe unter gleichen Bedingungen 4.0"/></a> Jeglicher Code außerdem unter der GPL3.

Davon ausgenommen sind gekennzeichnete Fremdinhalte, die unter ihrer jeweils eigenen Lizenz stehen: die eingebundenen xkcd-Comics (CC BY-NC 2.5), das Venn-Diagramm von Drew Conway (CC BY-NC 3.0) und der Melbourne-Housing-Datensatz von Anthony Pino (CC BY-NC-SA 4.0). Bei jedem dieser Inhalte steht die Quelle an Ort und Stelle. Die [Vorlesungsfolien](folien.md) enthalten weitere Fremdbilder; sie sind in der README des Folienordners im Repositorium aufgeführt.

## Quellen

Nichts in diesem Buch ist neu, bis auf die Reihenfolge und sicherlich der ein oder andere Tippfehler.
Die Hauptquellen für dieses Skript sind {cite}`georgii2015stochastik` für die Wahrscheinlichkeitstheorie,
und {cite}`joelgrusdsfs` für den Python-Teil.
In beiden Büchern ist Stoff für mehr als eine Vorlesung und die Zielgruppen sind nicht deckungsgleich mit unserer Vorlesung.
Ein lesenswertes ergänzendes Buch mit einigen weiteren Mathematik-Grundlagen (gerade lineare Algebra) ist {cite}`Deisenroth2020`.
Wer nicht gern in Paket-Dokumentationen stöbert, ist für Numpy, Pandas und Matplotlib vielleicht glücklicher mit dem Buch von Jake VanderPlas, welches sich sogar umsonst online lesen lässt {cite}`pythondsh`.
