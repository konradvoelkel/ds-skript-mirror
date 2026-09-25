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

## Vorgeschichte der DSGVO

Die DSGVO ist 2018 nicht aus dem Nichts entstanden. Vier Stationen erklären, warum sie so aussieht, wie sie aussieht:

- **Recht auf informationelle Selbstbestimmung**: Das Bundesverfassungsgericht entwickelte es im *Volkszählungsurteil* vom 15. Dezember 1983 (1 BvR 209/83 u. a.) aus dem allgemeinen Persönlichkeitsrecht. Der Kernsatz ist bis heute die beste Kurzfassung des Schutzzwecks: Mit dem Selbstbestimmungsrecht wäre eine Gesellschaftsordnung nicht vereinbar, „in der Bürger nicht mehr wissen können, wer was wann und bei welcher Gelegenheit über sie weiß“. Anlass war eine geplante Volkszählung — ein Datenschutzproblem entsteht also nicht erst durch Computer, sondern durch Zusammenführung.
- **Bundesdatenschutzgesetz (BDSG)**: 1977 erstmals erlassen, 1990 grundlegend neu gefasst, um das Volkszählungsurteil umzusetzen. Es gilt bis heute, seit 2018 aber nur noch ergänzend zur DSGVO, dort wo diese den Mitgliedstaaten Spielraum lässt (etwa beim Beschäftigtendatenschutz).
- **Richtlinie 95/46/EG** vom 24. Oktober 1995: die unmittelbare Vorläuferin der DSGVO. Sie enthielt bereits die Grundsätze, die Rechtsgrundlagen und die Betroffenenrechte, war als Richtlinie aber auf Umsetzung in nationales Recht angewiesen — mit entsprechend unterschiedlichen Ergebnissen in den Mitgliedstaaten. Die DSGVO hob sie auf und regelte dasselbe als unmittelbar geltende Verordnung.
- **ePrivacy-Richtlinie 2002/58/EG**: Sonderregeln für elektronische Kommunikation, Nachfolgerin der Richtlinie 97/66/EG, geändert durch 2009/136/EG. Aus ihr stammt die Pflicht, über die Speicherung von Informationen auf Endgeräten zu informieren und eine Ablehnung zu ermöglichen — also das, was heute jede Website als *Cookie-Banner* anzeigt. Eine ablösende ePrivacy-Verordnung wird seit 2017 verhandelt.

## Zentrale Begriffe

- **Anwendungsbereich** (Art. 2 Abs. 1 DSGVO): Die Verordnung gilt für die ganz oder teilweise automatisierte Verarbeitung personenbezogener Daten sowie für die nichtautomatisierte Verarbeitung solcher Daten, die in einem Dateisystem gespeichert sind oder gespeichert werden sollen. Der Zettelkasten fällt also darunter, der einzelne Notizzettel nicht.
- **Verarbeitung**: Jeder Vorgang im Zusammenhang mit personenbezogenen Daten – von der Erhebung über Speicherung und Nutzung bis zur Löschung.
- **Verantwortlicher**: Die Stelle, die über Zwecke und Mittel der Datenverarbeitung entscheidet.
- **Auftragsverarbeiter**: Eine dritte Partei, die im Auftrag des Verantwortlichen Daten verarbeitet – z. B. ein externer Dienstleister. Der Auftragsverarbeiter ist an die Weisungen des Verantwortlichen gebunden, und das Verhältnis muss in einem **Auftragsverarbeitungsvertrag (AVV)** nach Art. 28 DSGVO schriftlich festgehalten werden: Gegenstand, Dauer, Art und Zweck der Verarbeitung, Kategorien betroffener Personen, Pflichten und Rechte beider Seiten.
- **Einwilligung**: Eine freiwillige, informierte und eindeutige Zustimmung der betroffenen Person zur Datenverarbeitung. Freiwillig heißt auch: ohne Abhängigkeitsverhältnis. Eine Schule in Skellefteå ließ Schüler\*innen per Gesichtserkennung die Anwesenheit erfassen, mit Einwilligung der Eltern; die schwedische Aufsicht hielt die Einwilligung wegen des Machtgefälles zwischen Schule und Familien für unwirksam ([ETid-67](https://www.enforcementtracker.com/ETid-67), 2019, rund 18.600 €). Die Telefonliste des Kindergartens dagegen ist mit Einwilligung der Eltern in Ordnung.

Beispiel für Verantwortlicher und Auftragsverarbeiter: Ein Onlineshop ist verantwortlich für die Kundendaten; der Paketdienst, der die Lieferadresse bekommt, und der Cloud-Anbieter, auf dessen Servern die Datenbank liegt, sind Auftragsverarbeiter. Beide brauchen einen Vertrag mit dem Shop, und der Shop bleibt in der Pflicht.

## Grundprinzipien der DSGVO (Art. 5)

1. **Rechtmäßigkeit, Verarbeitung nach Treu und Glauben, Transparenz** (Art. 5 Abs. 1 lit. a) – „auf rechtmäßige Weise, nach Treu und Glauben und in einer für die betroffene Person nachvollziehbaren Weise“
2. **Zweckbindung** (lit. b) – Nutzung nur zu „festgelegten, eindeutigen und legitimen Zwecken“
3. **Datenminimierung** (lit. c) – „dem Zweck angemessen und erheblich sowie auf das notwendige Maß beschränkt“
4. **Richtigkeit** (lit. d) – „sachlich richtig und erforderlichenfalls auf dem neuesten Stand“; unrichtige Daten sind zu berichtigen oder zu löschen
5. **Speicherbegrenzung** (lit. e) – in identifizierbarer Form nur so lange, „wie es für die Zwecke … erforderlich ist“
6. **Integrität und Vertraulichkeit** (lit. f) – Schutz vor „unbefugter oder unrechtmäßiger Verarbeitung und vor unbeabsichtigtem Verlust“

Dazu kommt in Art. 5 Abs. 2 die **Rechenschaftspflicht**: Der Verantwortliche muss die Einhaltung dieser Grundsätze nicht nur gewährleisten, sondern auch nachweisen können. Das ist der Grund, warum Datenschutz in der Praxis so viel Dokumentation bedeutet.

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

- **Privacy by Design** (Art. 25 Abs. 1): Datenschutz muss schon bei der Konzeption von Systemen mitgedacht werden, nicht nachträglich angebaut. Drei Leitsätze fassen zusammen, was das praktisch heißt:
  1. Was technisch unmöglich gemacht wird, muss nicht überwacht werden. Ein Feld, das es nicht gibt, kann nicht missbraucht werden.
  2. Geschäftsabläufe funktional trennen und so früh wie möglich anonymisieren — je später im Prozess ein Personenbezug besteht, desto kleiner ist der Kreis derer, die ihn sehen.
  3. Die Architektur datenschutzfreundlich auslegen, physisch wie elektronisch: getrennte Systeme, getrennte Zugriffsrechte, getrennte Räume.
- **Privacy by Default** (Art. 25 Abs. 2): Die Voreinstellungen müssen die datensparsamen sein. Der Grund ist empirisch und nicht juristisch: Menschen setzen ihren erklärten Datenschutzwunsch im Alltag oft nicht um — aus Bequemlichkeit, Unkenntnis oder weil sie im Einzelfall anders abwägen. Wer bei jedem Cookie-Banner „alle akzeptieren“ klickt, hat damit nicht seine Präferenz geäußert, sondern den Weg des geringsten Widerstands genommen. Deshalb entscheidet die Voreinstellung faktisch über das Ergebnis.

Beispiele: Voreinstellungen dürfen keine unnötige Datenerhebung zulassen. Ein Cookie-Banner, bei dem alle Häkchen schon gesetzt sind, verstößt gegen Privacy by Default. TikTok stellte Konten von Kindern standardmäßig öffentlich und bekam dafür 345 Mio. € ([ETid-2032](https://www.enforcementtracker.com/ETid-2032), 2023).

## Datensparsamkeit

Ein zentrales Prinzip im Datenschutz. Es bedeutet:
- Keine Erhebung irrelevanter Daten
- Verzicht auf optionale Angaben (z. B. Alter bei Bestellung, wenn nicht erforderlich)
- Hinweis auf Freiwilligkeit und Voreinstellung auf "nicht erheben"

Die praktische Regel für Data-Science-Projekte lautet: Bei jedem personenbezogenen Feld fragen, warum man es speichern muss. Wenn es keine Antwort gibt, weglassen. Wenn es eine gibt, notieren, das ist die Rechtsgrundlage. Für alles andere die Einwilligung einholen.


## Weiterführende Begriffe und Konzepte

- **Pseudonymisierung**: Verarbeitung in einer Weise, dass Daten ohne zusätzliche Informationen nicht einer Person zugeordnet werden können.
- **Selbstgenerierter Code** (Längsschnittstudien): Bei Mehrfachbefragungen will man die Antworten derselben Person über mehrere Erhebungen zusammenführen, ohne sie der Person zuordnen zu können. Die befragte Person bildet dazu aus stabilen persönlichen Merkmalen selbst einen Code — etwa dem ersten und letzten Buchstaben der Vornamen der Eltern und dem Tag des eigenen Geburtsdatums — und gespeichert wird nur dessen Hash. Weil dieselbe Person denselben Code reproduzieren kann, lassen sich die Wellen verknüpfen; weil die Erhebenden den Code nicht kennen, können sie ihn nicht zurückrechnen. Die Verfahren und ihre Fehlerquoten sind gut untersucht {cite}`poege2011`. Ein Pseudonym bleibt es trotzdem: Wer die Bildungsregel und genug Hintergrundwissen über die Befragten hat, kann Kandidaten durchprobieren — gehashte Daten sind also nicht automatisch anonym.
- **Rechte Betroffener**: Kapitel III der DSGVO gibt der betroffenen Person sieben Rechte, die der Verantwortliche auf Verlangen erfüllen muss — in der Regel binnen eines Monats und unentgeltlich:
  - **Auskunft** (Art. 15): Welche Daten werden verarbeitet, zu welchem Zweck, woher stammen sie, an wen gehen sie, wie lange werden sie gespeichert — nebst einer Kopie der Daten. Das umfasst auch Videoaufnahmen: Die ungarische Tochter von Deichmann verweigerte einer Kundin die Herausgabe der Aufnahmen aus dem Laden und zahlte 54.800 € ([ETid-430](https://www.enforcementtracker.com/ETid-430), 2020).
  - **Berichtigung** (Art. 16): unrichtige Daten korrigieren, unvollständige vervollständigen.
  - **Löschung** (Art. 17), auch „Recht auf Vergessenwerden“: etwa wenn der Zweck entfallen ist oder die Einwilligung widerrufen wurde.
  - **Einschränkung der Verarbeitung** (Art. 18): der Mittelweg, solange etwa die Richtigkeit der Daten geprüft wird — die Daten bleiben gespeichert, dürfen aber nicht weiterverwendet werden.
  - **Mitteilungspflicht** (Art. 19): Berichtigung, Löschung und Einschränkung muss der Verantwortliche allen Empfängern mitteilen, an die er die Daten weitergegeben hat.
  - **Datenübertragbarkeit** (Art. 20): die eigenen Daten in einem gängigen maschinenlesbaren Format erhalten und zu einem anderen Anbieter mitnehmen.
  - **Widerspruch** (Art. 21): gegen eine Verarbeitung, die auf berechtigtem Interesse beruht; bei Direktwerbung ohne jede Abwägung und jederzeit.

  Dazu kommt die **Haftung** (Art. 82): Wer durch einen Verstoß einen materiellen oder immateriellen Schaden erleidet, hat Anspruch auf Schadenersatz. Der Verantwortliche entlastet sich nur, wenn er nachweist, dass er in keinerlei Hinsicht für den Schaden verantwortlich ist.
- **Meldepflicht bei Datenpannen** (Art. 33): Verletzungen des Schutzes personenbezogener Daten sind innerhalb von 72 Stunden der Aufsicht zu melden. Twitter meldete eine Panne zu spät und unvollständig, 450.000 € ([ETid-485](https://www.enforcementtracker.com/ETid-485), 2020); Knuddels (oben) meldete sofort und wurde dafür milder behandelt.
- **Datenübermittlung in Drittländer**: Nur bei angemessenem Datenschutzniveau zulässig. Der einfachste Weg dorthin ist ein **Angemessenheitsbeschluss** der Kommission nach Art. 45: Stellt sie für ein Land ein angemessenes Schutzniveau fest, darf man dorthin übermitteln wie innerhalb der EU. Für die USA ist das eine Posse in mehreren Akten:
  - **Safe Harbor** (Entscheidung der Kommission vom 26.7.2000) — vom EuGH im Urteil *Schrems I* am 6.10.2015 für ungültig erklärt.
  - **EU-US Privacy Shield** (Durchführungsbeschluss (EU) 2016/1250) — vom EuGH im Urteil *Schrems II* am 16.7.2020 für ungültig erklärt, jeweils weil US-Behörden auf die Daten zugreifen können und Betroffene aus der EU dagegen keinen wirksamen Rechtsbehelf haben.
  - **EU-U.S. Data Privacy Framework** (Durchführungsbeschluss (EU) 2023/1795, seit Juli 2023) — der dritte Anlauf, rechtlich von Anfang an umstritten. Er steht und fällt mit der Unabhängigkeit der US-Aufsicht; Stand September 2026 ist genau die wieder fraglich, und eine erneute Klage ist angekündigt. Wer heute eine US-Cloud einplant, sollte also einkalkulieren, dass die Grundlage wieder wegfallen kann. Meta übertrug Facebook-Daten trotzdem weiter in die USA und bekam mit 1,2 Mrd. € das bisher höchste DSGVO-Bußgeld ([ETid-1844](https://www.enforcementtracker.com/ETid-1844), 2023). Die von Schrems gegründete Organisation [noyb](https://noyb.eu) erreichte außerdem, dass die österreichische Aufsicht 2022 den Einsatz von Google Analytics als rechtswidrig einstufte, ohne Bußgeld, aber mit Folgen für fast jede Website. Wer Daten in eine US-Cloud legt, muss diese Geschichte kennen.

## Bußgelder und Durchsetzung

Die Neuerung der DSGVO gegenüber der Richtlinie von 1995 sind weniger die Grundsätze als die Sanktionen. Durchgesetzt wird sie von unabhängigen **Aufsichtsbehörden** (Art. 51 ff.) — in Deutschland je eine pro Bundesland plus die Bundesbeauftragte. Ihr Katalog an **Abhilfebefugnissen** (Art. 58 Abs. 2) reicht weit über Geld hinaus: Warnung vor geplanten Verarbeitungen, Verwarnung nach einem Verstoß, Anweisung, Anträgen betroffener Personen zu entsprechen, Anordnung von Berichtigung oder Löschung, Widerruf einer Zertifizierung, Aussetzung von Übermittlungen in Drittländer — und, als schärfstes Mittel, die vorübergehende oder endgültige **Beschränkung oder das Verbot** einer Verarbeitung. Für ein datengetriebenes Geschäftsmodell ist das die eigentliche Drohung; ein Bußgeld ist bezahlbar, ein Verarbeitungsverbot nicht.

**Geldbußen** (Art. 83) sollen „wirksam, verhältnismäßig und abschreckend“ sein und kommen in zwei Stufen: bis 10 Mio. € oder 2 % des weltweiten Vorjahresumsatzes für Verstöße gegen Pflichten des Verantwortlichen (etwa Art. 25 Privacy by Design, Art. 33 Meldepflicht), bis 20 Mio. € oder 4 % für Verstöße gegen die Grundsätze, die Betroffenenrechte oder die Regeln zur Drittlandübermittlung — jeweils der höhere Betrag. Bei der Zumessung zählen unter anderem Art, Schwere und Dauer des Verstoßes, Vorsatz oder Fahrlässigkeit, ergriffene Abhilfemaßnahmen, frühere Verstöße und der Grad der Zusammenarbeit mit der Aufsicht.

Neben der Aufsicht steht die Selbstregulierung: **Verhaltensregeln** (Art. 40) sind branchenspezifische Regelwerke, die Verbände ausarbeiten und von der Aufsicht genehmigen lassen. Wer sich daran hält, hat es leichter, die Rechenschaftspflicht aus Art. 5 Abs. 2 zu erfüllen.

Zwei Missverständnisse sind damit erledigt: Datenschutz ist weder zu kompliziert, um sich damit zu befassen, noch folgenlos, wenn man ihn ignoriert. Zugleich gilt: Die kleinen Bußgelder kosten kein Startup das Leben. Mercedes zahlte in Spanien 3.000 € für mangelnde Kooperation mit der Aufsicht ([ETid-885](https://www.enforcementtracker.com/ETid-885), 2021); das interessiert einen Konzern erst, weil frühere Verstöße das nächste Bußgeld erhöhen.

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

## Rechtsrahmen der EU jenseits der DSGVO

Die DSGVO schützt personenbezogene Daten. Seit 2020 verfolgt die EU mit der **Europäischen Datenstrategie** (Mitteilung der Kommission vom 19. Februar 2020) ein zweites, ergänzendes Ziel: Daten sollen innerhalb Europas leichter geteilt und genutzt werden können, und zwar unter europäischen Regeln. Daraus ist eine Reihe von Verordnungen entstanden, die nebeneinander gelten und die man auseinanderhalten sollte — grob nach drei Stoßrichtungen: Schutz der Betroffenen (DSGVO), Regeln für Märkte und Plattformen (DMA, DSA), Zugang zu und Teilen von Daten (DGA, Data Act, AI Act).

- **KI-Verordnung / AI Act** ([Verordnung (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)): erster umfassender Rechtsrahmen für KI-Systeme, vorgeschlagen im April 2021, verabschiedet 2024. Der Ansatz ist risikobasiert — verbotene Praktiken (etwa Social Scoring durch Behörden), Hochrisiko-Anwendungen mit umfangreichen Pflichten (Medizin, Personalauswahl, Strafverfolgung), Transparenzpflichten für den Rest. Wer ein Modell in ein Produkt einbaut, wird hier selbst zum Adressaten.
- **Digital Markets Act (DMA)** ([Verordnung (EU) 2022/1925](https://eur-lex.europa.eu/eli/reg/2022/1925/oj)): Pflichten für sehr große Plattformen, die als *Gatekeeper* benannt sind — etwa Interoperabilität von Messengern und das Verbot, eigene Dienste zu bevorzugen.
- **Digital Services Act (DSA)** ([Verordnung (EU) 2022/2065](https://eur-lex.europa.eu/eli/reg/2022/2065/oj)): Verantwortung für Inhalte, Meldewege, Transparenz von Empfehlungssystemen und Werbung.
- **Data Governance Act (DGA)** ([Verordnung (EU) 2022/868](https://eur-lex.europa.eu/eli/reg/2022/868/oj)): Rahmen für die Weiterverwendung geschützter Daten der öffentlichen Hand, für Datenvermittlungsdienste und für *Datenaltruismus* — also das freiwillige Bereitstellen eigener Daten für gemeinwohlorientierte Zwecke.
- **Data Act** ([Verordnung (EU) 2023/2854](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)): Zugang zu den Daten, die vernetzte Geräte erzeugen — wer eine Maschine kauft, soll auch an ihre Daten kommen und den Anbieter wechseln können.

Für die tägliche Arbeit mit Daten bleibt die DSGVO der Maßstab; die übrigen Verordnungen entscheiden darüber, welche Daten überhaupt verfügbar sind und unter welchen Bedingungen ein Modell in Verkehr gebracht werden darf.

## Weiterführende Ressourcen

- [DSGVO in einfachen Worten](https://eu-datenschutz-grundverordnung.net/eu-dsgvo/)
- [Volltext der DSGVO (EUR-Lex)](http://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:32016R0679)
- [Checkliste für technische & organisatorische Maßnahmen (BayLDA)](https://www.lda.bayern.de/media/checkliste/baylda_checkliste_tom.pdf)
- [Film: *Democracy – Im Rausch der Daten* (bpb)](https://www.bpb.de/mediathek/254194/democracy-im-rausch-der-daten)
- [GDPR Enforcement Tracker](https://www.enforcementtracker.com) der Kanzlei CMS: alle in diesem Kapitel genannten Bußgeldfälle mit Datum, Betrag und Quelle (CC BY-NC-SA 4.0)
- Alfred Spector, Peter Norvig, Chris Wiggins, Jeannette M. Wing: *Data Science in Context* {cite}`spector2022` — Data Science ohne Formeln und ohne Code, dafür sehr gut über das, was um die Technik herum passiert; Ethik ist darin kein Anhang, sondern ein durchgehendes Thema.