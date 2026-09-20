# Datenschutz

[Vorlesungsaufzeichnung Datenschutz](https://media.hhu.de/channel/video/data-science-vl-15-datenschutz-2025/4912a23e7ad45d8389135220db07bc47/167)

In der Informatik ist der **verantwortungsvolle Umgang mit personenbezogenen Daten** zentral – sowohl rechtlich als auch ethisch. Dieses Kapitel bietet einen Überblick über die wichtigsten Begriffe und Prinzipien des Datenschutzes im Kontext der Europäischen Datenschutzgrundverordnung (DSGVO, en. GDPR).

Das Kapitel steht an dieser Stelle, weil wir ab dem nächsten Kapitel mit echten Datensätzen Modelle trainieren. Bevor personenbezogene Daten als Trainingsmaterial dienen, sollten die Begriffe geklärt sein, mit denen der Umgang mit solchen Daten geregelt ist. Es ist bewusst ein Begriffsglossar ohne Mathematik und Code. Zu den Begriffen gehören Beispiele und echte Fälle; die Bußgeldfälle stammen alle aus dem [GDPR Enforcement Tracker](https://www.enforcementtracker.com) der Kanzlei CMS und sind dort mit ihrer Nummer verlinkt, sodass sich jeder Fall mit Datum, Betrag und Quelle nachprüfen lässt.

## Personenbezogene Daten

**Personenbezogene Daten** sind alle Informationen, die sich auf eine identifizierte oder identifizierbare natürliche Person beziehen. Eine Person gilt als identifizierbar, wenn sie direkt oder indirekt, z. B. durch Namen, Standortdaten oder Online-Kennungen, identifiziert werden kann.

Auch **pseudonymisierte**, **verschlüsselte** oder **anonymisierte Daten**, die wieder einer Person zugeordnet werden können, fallen unter den Schutz der DSGVO.

Beispiele:
- Die Lieblingsfarbe von Gummibärchen ist kein personenbezogenes Datum. Dieselbe Angabe in einer Tabelle mit Matrikelnummer ist eins.
- Eine Längsschnittbefragung an Schulen will die Antworten derselben Kinder über Jahre verknüpfen, ohne Namen zu speichern. Ein Code aus den Anfangsbuchstaben der Elternnamen oder ein Hash des Namens mit festem Präfix ist ein **Pseudonym**: Wer die Regel kennt, kann zurückrechnen, also bleiben die Daten personenbezogen. Eine Nummer, die man den Kindern mitgibt, bringt im nächsten Jahr niemand mit, und ein Link mit kodierter Nummer zerstört das Vertrauen in die Anonymität.
- Ob Daten anonym sind, ist eine Frage der Information, nicht der Namen: Wer über eine Person genug Bits gesammelt hat (Postleitzahl, Geburtsdatum und Geschlecht reichen für die meisten Menschen), hat personenbezogene Daten, auch ohne Namen. Das ist die [Entropie](erwartungswert.md) aus dem Stochastik-Teil in juristischer Verkleidung.

## Zentrale Begriffe

- **Verarbeitung**: Jeder Vorgang im Zusammenhang mit personenbezogenen Daten – von der Erhebung über Speicherung und Nutzung bis zur Löschung.
- **Verantwortlicher**: Die Stelle, die über Zwecke und Mittel der Datenverarbeitung entscheidet.
- **Auftragsverarbeiter**: Eine dritte Partei, die im Auftrag des Verantwortlichen Daten verarbeitet – z. B. ein externer Dienstleister.
- **Einwilligung**: Eine freiwillige, informierte und eindeutige Zustimmung der betroffenen Person zur Datenverarbeitung. Freiwillig heißt auch: ohne Abhängigkeitsverhältnis. Eine Schule in Skellefteå ließ Schüler\*innen per Gesichtserkennung die Anwesenheit erfassen, mit Einwilligung der Eltern; die schwedische Aufsicht hielt die Einwilligung wegen des Machtgefälles zwischen Schule und Familien für unwirksam ([ETid-67](https://www.enforcementtracker.com/ETid-67), 2019, rund 18.600 €). Die Telefonliste des Kindergartens dagegen ist mit Einwilligung der Eltern in Ordnung.

Beispiel für Verantwortlicher und Auftragsverarbeiter: Ein Onlineshop ist verantwortlich für die Kundendaten; der Paketdienst, der die Lieferadresse bekommt, und der Cloud-Anbieter, auf dessen Servern die Datenbank liegt, sind Auftragsverarbeiter. Beide brauchen einen Vertrag mit dem Shop, und der Shop bleibt in der Pflicht.

## Grundprinzipien der DSGVO (Art. 5)

1. **Rechtmäßigkeit, Transparenz**  
2. **Zweckbindung** – Nutzung nur zu legitim festgelegten Zwecken  
3. **Datenminimierung** – nur so viel wie nötig  
4. **Richtigkeit** – unrichtige Daten sind zu berichtigen  
5. **Speicherbegrenzung** – Daten nur solange wie erforderlich speichern  
6. **Integrität & Vertraulichkeit** – Schutz vor unbefugtem Zugriff und Verlust  

Beispiele zu den Prinzipien:
- *Zweckbindung:* Wer für ein KI-generiertes Porträt den Nachnamen abfragt, hat dafür keinen Zweck. Wer zum Geburtstag einen Rabattcode verschickt, braucht das Geburtsdatum, aber nicht als Pflichtfeld bei jeder Bestellung.
- *Datenminimierung:* Ein Empfehlungsalgorithmus braucht Kaufhistorien, aber keine Adressen; die gehören in ein getrenntes System, im Extremfall auf einen Rechner ohne Netzverbindung (*Airgap*). Weniger gespeicherte Daten sind auch weniger Daten, die bei einer Panne abfließen.
- *Richtigkeit:* Ein falscher Schufa-Eintrag muss auf Antrag berichtigt werden; das Recht dazu steht in Art. 16.
- *Integrität und Vertraulichkeit:* Die Chat-Plattform Knuddels speicherte Passwörter im Klartext, wurde gehackt und bekam 20.000 € Bußgeld, das wegen der vorbildlichen Meldung und Aufarbeitung bewusst niedrig ausfiel ([ETid-25](https://www.enforcementtracker.com/ETid-25), 2018). Die AOK Baden-Württemberg nutzte Daten von Gewinnspielteilnehmer\*innen für Werbung, ohne die Einwilligung technisch sauber zu prüfen: 1,24 Mio. € ([ETid-306](https://www.enforcementtracker.com/ETid-306), 2020).

## Rechtsgrundlagen (Art. 6) und besondere Kategorien (Art. 9)

- **Rechtsgrundlage**: Eine Verarbeitung personenbezogener Daten ist nur rechtmäßig, wenn mindestens eine der sechs Voraussetzungen aus Art. 6 Abs. 1 DSGVO erfüllt ist:
  1. Einwilligung der betroffenen Person,
  2. Erfüllung eines Vertrags mit der betroffenen Person (oder vorvertragliche Maßnahmen auf ihre Anfrage),
  3. Erfüllung einer rechtlichen Verpflichtung,
  4. Schutz lebenswichtiger Interessen,
  5. Wahrnehmung einer Aufgabe im öffentlichen Interesse oder in Ausübung öffentlicher Gewalt,
  6. berechtigtes Interesse des Verantwortlichen oder eines Dritten, sofern nicht die Interessen oder Grundrechte der betroffenen Person überwiegen.

  Die Einwilligung ist also nur *eine* von sechs möglichen Grundlagen – ein Onlineshop braucht für die Lieferadresse keine gesonderte Einwilligung, denn die Verarbeitung ist zur Vertragserfüllung erforderlich, und die Weitergabe an den Paketdienst ebenfalls. Rechnungen zehn Jahre aufzubewahren ist eine rechtliche Verpflichtung aus dem Steuerrecht, dafür darf man die Löschung verweigern.

  Die teuersten Fälle in Deutschland entstanden aus fehlender Rechtsgrundlage gegenüber den eigenen Beschäftigten: H&M führte in einem Servicecenter in Nürnberg Notizen über private Lebensumstände und Krankheiten der Mitarbeiter\*innen und wertete sie aus, 35,3 Mio. € ([ETid-405](https://www.enforcementtracker.com/ETid-405), 2020). notebooksbilliger.de überwachte Beschäftigte dauerhaft per Video; die Aufsicht verhängte 10,4 Mio. €, das Gericht reduzierte auf 900.000 € ([ETid-519](https://www.enforcementtracker.com/ETid-519), 2021). Auch Einzelpersonen werden belangt: Ein Polizist, der die Telefonnummer einer Zeugin aus einer Akte für private Nachrichten nutzte, zahlte 1.400 € ([ETid-50](https://www.enforcementtracker.com/ETid-50), 2019).

- **Besondere Kategorien personenbezogener Daten** (Art. 9 DSGVO, umgangssprachlich „sensible Daten“): Daten, aus denen die rassische oder ethnische Herkunft, politische Meinungen, religiöse oder weltanschauliche Überzeugungen oder die Gewerkschaftszugehörigkeit hervorgehen, sowie genetische Daten, biometrische Daten zur eindeutigen Identifizierung, Gesundheitsdaten und Daten zum Sexualleben oder zur sexuellen Orientierung. Ihre Verarbeitung ist **grundsätzlich untersagt** (Art. 9 Abs. 1) – aber nicht absolut: Art. 9 Abs. 2 zählt abschließend Ausnahmen auf, etwa die ausdrückliche Einwilligung, Pflichten aus dem Arbeits- und Sozialrecht, Daten, die die betroffene Person offensichtlich selbst öffentlich gemacht hat, die Gesundheitsversorgung oder die wissenschaftliche Forschung unter Schutzmaßnahmen. Die Religionszugehörigkeit darf also verarbeitet werden, wenn eine dieser Ausnahmen greift; ohne eine solche Ausnahme reicht auch keine der sechs Rechtsgrundlagen aus Art. 6.

## Privacy by Design und by Default

- **Privacy by Design**: Datenschutz muss schon bei der Konzeption von Systemen mitgedacht werden.
- **Privacy by Default**: Systeme sollen standardmäßig datensparsame Einstellungen haben.

Beispiele: Voreinstellungen dürfen keine unnötige Datenerhebung zulassen. Ein Cookie-Banner, bei dem alle Häkchen schon gesetzt sind, verstößt gegen Privacy by Default. TikTok stellte Konten von Kindern standardmäßig öffentlich und bekam dafür 345 Mio. € ([ETid-2032](https://www.enforcementtracker.com/ETid-2032), 2023).

## Datensparsamkeit

Ein zentrales Prinzip im Datenschutz. Es bedeutet:
- Keine Erhebung irrelevanter Daten
- Verzicht auf optionale Angaben (z. B. Alter bei Bestellung, wenn nicht erforderlich)
- Hinweis auf Freiwilligkeit und Voreinstellung auf "nicht erheben"

Die praktische Regel für Data-Science-Projekte lautet: Bei jedem personenbezogenen Feld fragen, warum man es speichern muss. Wenn es keine Antwort gibt, weglassen. Wenn es eine gibt, notieren, das ist die Rechtsgrundlage. Für alles andere die Einwilligung einholen.


## Weiterführende Begriffe und Konzepte

- **Pseudonymisierung**: Verarbeitung in einer Weise, dass Daten ohne zusätzliche Informationen nicht einer Person zugeordnet werden können.
- **Rechte Betroffener**: z. B. Auskunft, Löschung, Berichtigung, Widerspruch. Das Auskunftsrecht (Art. 15) umfasst auch Videoaufnahmen: Die ungarische Tochter von Deichmann verweigerte einer Kundin die Herausgabe der Aufnahmen aus dem Laden und zahlte 54.800 € ([ETid-430](https://www.enforcementtracker.com/ETid-430), 2020).
- **Meldepflicht bei Datenpannen** (Art. 33): Verletzungen des Schutzes personenbezogener Daten sind innerhalb von 72 Stunden der Aufsicht zu melden. Twitter meldete eine Panne zu spät und unvollständig, 450.000 € ([ETid-485](https://www.enforcementtracker.com/ETid-485), 2020); Knuddels (oben) meldete sofort und wurde dafür milder behandelt.
- **Datenübermittlung in Drittländer**: Nur bei angemessenem Datenschutzniveau zulässig. Die Geschichte dazu ist eine Posse in mehreren Akten: Das *Safe-Harbor*-Abkommen mit den USA kippte der EuGH 2015 auf Klage von Max Schrems, das Nachfolgeabkommen *Privacy Shield* 2020 (Schrems II), jeweils weil US-Behörden auf die Daten zugreifen können. Meta übertrug Facebook-Daten trotzdem weiter in die USA und bekam mit 1,2 Mrd. € das bisher höchste DSGVO-Bußgeld ([ETid-1844](https://www.enforcementtracker.com/ETid-1844), 2023). Die von Schrems gegründete Organisation [noyb](https://noyb.eu) erreichte außerdem, dass die österreichische Aufsicht 2022 den Einsatz von Google Analytics als rechtswidrig einstufte, ohne Bußgeld, aber mit Folgen für fast jede Website. Wer Daten in eine US-Cloud legt, muss diese Geschichte kennen.

## Bußgelder und Durchsetzung

Die Neuerung der DSGVO gegenüber der Richtlinie von 1995 sind weniger die Grundsätze als die Sanktionen: bis zu 20 Mio. € oder 4 % des weltweiten Jahresumsatzes (Art. 83), und die Aufsichtsbehörden dürfen Verarbeitungen untersagen (Art. 58). Zwei Missverständnisse sind damit erledigt: Datenschutz ist weder zu kompliziert, um sich damit zu befassen, noch folgenlos, wenn man ihn ignoriert. Zugleich gilt: Die kleinen Bußgelder kosten kein Startup das Leben. Mercedes zahlte in Spanien 3.000 € für mangelnde Kooperation mit der Aufsicht ([ETid-885](https://www.enforcementtracker.com/ETid-885), 2021); das interessiert einen Konzern erst, weil frühere Verstöße das nächste Bußgeld erhöhen.

| Fall | Jahr | Betrag | Worum es ging | Tracker |
|---|---|---|---|---|
| Meta Platforms Ireland | 2023 | 1,2 Mrd. € | Datentransfer in die USA ohne gültige Grundlage | [ETid-1844](https://www.enforcementtracker.com/ETid-1844) |
| TikTok | 2023 | 345 Mio. € | Kinderkonten standardmäßig öffentlich | [ETid-2032](https://www.enforcementtracker.com/ETid-2032) |
| H&M, Nürnberg | 2020 | 35,3 Mio. € | Notizen über Privatleben und Krankheiten von Beschäftigten | [ETid-405](https://www.enforcementtracker.com/ETid-405) |
| AOK Baden-Württemberg | 2020 | 1,24 Mio. € | Gewinnspieldaten für Werbung ohne saubere Einwilligung | [ETid-306](https://www.enforcementtracker.com/ETid-306) |
| notebooksbilliger.de | 2021 | 900.000 € (nach Gericht) | Dauerhafte Videoüberwachung von Beschäftigten | [ETid-519](https://www.enforcementtracker.com/ETid-519) |
| Twitter | 2020 | 450.000 € | Datenpanne zu spät gemeldet | [ETid-485](https://www.enforcementtracker.com/ETid-485) |
| Deichmann, Ungarn | 2020 | 54.800 € | Auskunft über Videoaufnahmen verweigert | [ETid-430](https://www.enforcementtracker.com/ETid-430) |
| Knuddels | 2018 | 20.000 € | Passwörter im Klartext, vorbildlich gemeldet | [ETid-25](https://www.enforcementtracker.com/ETid-25) |
| Schule in Skellefteå | 2019 | 18.600 € | Gesichtserkennung mit unwirksamer Einwilligung | [ETid-67](https://www.enforcementtracker.com/ETid-67) |
| Polizist, Baden-Württemberg | 2019 | 1.400 € | Telefonnummer einer Zeugin privat genutzt | [ETid-50](https://www.enforcementtracker.com/ETid-50) |
| Mercedes, Spanien | 2021 | 3.000 € | Mangelnde Kooperation mit der Aufsicht | [ETid-885](https://www.enforcementtracker.com/ETid-885) |

Alltagsfälle ohne Bußgeld, die man kennen sollte: Eine Dashcam darf laut BGH (2018) als Beweismittel verwertet werden, das permanente Aufzeichnen des Verkehrs bleibt trotzdem unzulässig. Eine Rundmail an alle Kund\*innen mit offener Empfängerliste statt BCC ist eine meldepflichtige Datenpanne. Ein Anruf von "PayPal", der nach Zugangsdaten fragt, ist kein Datenschutzproblem, sondern Betrug; Datenschutz und IT-Sicherheit überschneiden sich, sind aber nicht dasselbe. Das [Open-Data-Portal Düsseldorf](https://opendata.duesseldorf.de) zeigt, wie man Daten veröffentlicht, ohne Personen preiszugeben.

:::{admonition} Aufgabe: Der Enforcement Tracker als Datensatz
:class: tip
Der Enforcement Tracker ist selbst eine Tabelle mit über 3000 Zeilen: Land, Behörde, Datum, Betrag, Unternehmen, Sektor, verletzte Artikel, Art des Verstoßes, Quelle. Laden Sie die Tabelle (die Seite bietet einen Export an, sonst hilft ein kleines Skript, das die eingebetteten Daten aus der Seite liest) und beantworten Sie mit den Mitteln aus dem Kapitel [Pandas](pandas.ipynb): Welche Länder verhängen die meisten Bußgelder, welche die höchsten? Wie hat sich die Zahl der Fälle je Jahr entwickelt? Welcher Verstoßtyp ist der häufigste, welcher der teuerste im Mittel? Und: Ist der Mittelwert oder der Median das passende Lagemaß für Bußgeldbeträge?
:::

:::{admonition} Lösungshinweis
:class: dropdown
Die Beträge sind extrem rechtsschief (wenige Fälle über 100 Mio. €, die meisten unter 50.000 €), der Median ist deshalb das aussagekräftigere Lagemaß, und ein Histogramm braucht eine logarithmische Achse. Nach Anzahl führt Spanien mit großem Abstand, nach Summe Irland wegen der Verfahren gegen die dort ansässigen US-Konzerne. Der häufigste Verstoßtyp ist "Insufficient legal basis for data processing", also Art. 6.
:::

## Weiterführende Ressourcen

- [DSGVO in einfachen Worten](https://eu-datenschutz-grundverordnung.net/eu-dsgvo/)
- [Volltext der DSGVO (EUR-Lex)](http://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:32016R0679)
- [Checkliste für technische & organisatorische Maßnahmen (BayLDA)](https://www.lda.bayern.de/media/checkliste/baylda_checkliste_tom.pdf)
- [Film: *Democracy – Im Rausch der Daten* (bpb)](https://www.bpb.de/mediathek/254194/democracy-im-rausch-der-daten)