# Vorlesungsskript

## Voraussetzungen

In diesem Text gehen wir davon aus, dass wir alle einmal 3 Semester Grundlagen der Mathematik gehört haben und wissen, was ein Vektor, eine Matrix und was die Ableitung einer Funktion in mehreren reellen Variablen sind. Außerdem haben wir alle bereits eine Programmiersprache gelernt und sind mit grundlegenden Datenstrukturen vertraut.

In der Schulzeit haben Sie womöglich bereits erste Kontakte mit Stochastik, Statistik, Wahrscheinlichkeitstheorie gemacht. Wir werden die Grundlagen zwar systematisch einführen, sodass hierbei keinerlei Vorkenntnisse über die 'Mathematik für Informatik' nötig sein müssten, aber wir werden das in für Mathematiker\*innen und Informatiker\*innen gewohnt zügigem Tempo tun. Wenn Sie also vorher noch einen Überblick gewinnen möchten, was Sie in der Schule hätten lernen können, ist dazu der [Online Mathematik Brückenkurs Plus Stochastik](https://www.ombplus.de/ombplus/link/OmbpluModuleStocha/Ueberb) eine sehr gute Adresse (frei, auf deutsch, didaktisch gut, in der gleichen Notation wie dieses Skript).

## Ziele

Unser Ziel ist eine Einführung in die "Data Science".
Sie soll Orientierung und Überblick geben und erste Anwendungen ermöglichen in deskriptiver, explorativer und inferentieller Datenanalyse, mit besonderem Blick auf das maschinelle Lernen.
Dabei kümmern wir uns um den notwendigen theoretischen Background in Stochastik und einige praktische Übungen in Python.
Darauf aufbauend ließe sich danach tiefer in die künstliche Intelligenz einsteigen. Dazu gibt es an der HHU das [Masterprogramm ,,Artificial Intelligence and Data Science''](https://www.heicad.hhu.de/lehre/masters-programme-ai-and-data-science).

Wenn Sie in der vollen Breite als Data Scientist arbeiten können wollen, sollten Sie zusätzlich zu dieser Vorlesung auch noch die Inhalte von Vorlesungen über Statistik, Datenbanken und Machine Learning kennen und einige Übung in konkreten Projekten haben. Je nach Einsatzbereich brauchen Sie noch Kenntnisse über Algorithmen für verteilte Systeme (Data Science 2) oder Deep Learning. Um flexibel in anderen Projekten mitarbeiten zu können, sollten Sie in der Lage sein, R Code zu lesen (und auch Julia könnte in der Zukunft wichtiger werden).
Das alles ist aber noch nicht notwendig für "Junior Data Analyst"-Jobs, die sich im Wesentlichen mit der Anwendung einfacher Statistik beim Erstellen von Reports und Dashboards befassen - dazu lernen Sie das Handwerkszeug in dieser Vorlesung und müssen lediglich je nach Anwendung konkrete Softwarepakete dazu lernen und üben.

Wir werden immer wieder auf zusätzliche Quellen stoßen, um einzelne Themen weiter zu vertiefen oder aus einer anderen Perspektive zu betrachten.
In der ersten Vorlesung haben wir uns einen Überblick verschafft, was Data Science ist und was wir machen werden.


**Kompetenzen**
Studierende sollen nach Absolvierung der Lehrveranstaltungen grundlegende Konzepte aus der Wahrscheinlichkeitsrechnung kompetent anwenden können, Kompetenzen in den Grundlagen der Wahrscheinlichkeitsrechnung für Machine Learning erlangen, ein Machine-Learning-Problem detailliert ausarbeiten können und grundlegende Machine-Learning-Algorithmen anwenden können.

Sie sollen nach dem erfolgreichen Abschluss dieses Moduls in der Lage sein,
1. einen Datensatz explorativ zu analysieren,
1. Daten zur Weiterverarbeitung zu transformieren,
1. Teildatensätze zur Weiterverarbeitung zu wählen,
1. geeignete Datensätze zusammenzuführen,
1. Erkenntnisse in Daten zu beschreiben und zu visualisieren,
1. statistische Modelle anhand von Daten aufzustellen,
1. die Güte von Modellen zu bewerten,
1. und zur Klassifikation und Vorhersage weiterer Daten zu nutzen.

Dazu sind Sie damit vertraut, wie sich diese Aufgaben mit Python lösen lassen.

Bei der Auswahl und Verarbeitung von Daten sowie der Bewertung von Modellen stellen sich drängende ethische Fragen, nicht nur zum Datenschutz, und Sie sollten sich dieser Problematik bewusst werden und die neu erworbenen Kompetenzen verantwortungsvoll einsetzen können.

Teil der explorativen Datenanalyse ist das Generieren von Forschungsfragen.



## Skript und Vorlesung

Alle Grundlagen der Mathematik, die Sie zur Bearbeitung der Übungsaufgaben benötigen, sind in diesem Skript enthalten (oder in den Eingangsvoraussetzungen der Vorlesung).

**Wozu ein Skript**
könnte man auch fragen. Hautpsächlich dient uns das Skript als Referenz und Leitfaden für die Übungsaufgaben. Es gibt in der Tat hervorragende MOOCs (massive open online courses) frei im WWW, vor Allem wenn man gut Englisch spricht. Dieses Skript begleitet allerdings, im Gegensatz zu MOOCs, eine Präsenzlehrveranstaltung mit Übungsaufgaben. Es ist für den Lernerfolg entscheidend, die Übungsaufgaben engagiert zu bearbeiten und sich rege mit Kommiliton\*innen auszutauschen. Lehrpersonen können nur Lehren, das Lernen müssen die Student\*innen noch selbst machen.


## Lizenz

Dieses Vorlesungsskript steht unter der [Creative Commons Namensnennung Lizenz 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). <a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://mirrors.creativecommons.org/presskit/buttons/80x15/png/by.png" height="20"/></a> Jeglicher Code außerdem unter der GPL3.

## Inhaltsverzeichnis

```{tableofcontents}
```

## Quellen

Nichts in diesem Buch ist neu, bis auf die Reihenfolge und sicherlich der ein oder andere Tippfehler.
Die Hauptquellen für dieses Skript sind {cite}`georgii2015stochastik` für die Wahrscheinlichkeitstheorie,
und {cite}`joelgrusdsfs` für den Python-Teil.
In beiden Büchern ist Stoff für mehr als eine Vorlesung und die Zielgruppen sind nicht deckungsgleich mit unserer Vorlesung.
Ein lesenswertes ergänzendes Buch mit einigen weiteren Mathematik-Grundlagen (gerade lineare Algebra) ist {cite}`Deisenroth2020`.

```{bibliography}
```
