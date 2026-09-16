# Datenschutz

[Vorlesungsaufzeichnung Datenschutz](https://media.hhu.de/channel/video/data-science-vl-15-datenschutz-2025/4912a23e7ad45d8389135220db07bc47/167)

In der Informatik ist der **verantwortungsvolle Umgang mit personenbezogenen Daten** zentral – sowohl rechtlich als auch ethisch. Dieses Kapitel bietet einen Überblick über die wichtigsten Begriffe und Prinzipien des Datenschutzes im Kontext der Europäischen Datenschutzgrundverordnung (DSGVO, en. GDPR).

Das Kapitel steht an dieser Stelle, weil wir ab dem nächsten Kapitel mit echten Datensätzen Modelle trainieren. Bevor personenbezogene Daten als Trainingsmaterial dienen, sollten die Begriffe geklärt sein, mit denen der Umgang mit solchen Daten geregelt ist. Es ist bewusst ein Begriffsglossar ohne Mathematik und Code.

## Personenbezogene Daten

**Personenbezogene Daten** sind alle Informationen, die sich auf eine identifizierte oder identifizierbare natürliche Person beziehen. Eine Person gilt als identifizierbar, wenn sie direkt oder indirekt, z. B. durch Namen, Standortdaten oder Online-Kennungen, identifiziert werden kann.

Auch **pseudonymisierte**, **verschlüsselte** oder **anonymisierte Daten**, die wieder einer Person zugeordnet werden können, fallen unter den Schutz der DSGVO.

## Zentrale Begriffe

- **Verarbeitung**: Jeder Vorgang im Zusammenhang mit personenbezogenen Daten – von der Erhebung über Speicherung und Nutzung bis zur Löschung.
- **Verantwortlicher**: Die Stelle, die über Zwecke und Mittel der Datenverarbeitung entscheidet.
- **Auftragsverarbeiter**: Eine dritte Partei, die im Auftrag des Verantwortlichen Daten verarbeitet – z. B. ein externer Dienstleister.
- **Einwilligung**: Eine freiwillige, informierte und eindeutige Zustimmung der betroffenen Person zur Datenverarbeitung.

## Grundprinzipien der DSGVO (Art. 5)

1. **Rechtmäßigkeit, Transparenz**  
2. **Zweckbindung** – Nutzung nur zu legitim festgelegten Zwecken  
3. **Datenminimierung** – nur so viel wie nötig  
4. **Richtigkeit** – unrichtige Daten sind zu berichtigen  
5. **Speicherbegrenzung** – Daten nur solange wie erforderlich speichern  
6. **Integrität & Vertraulichkeit** – Schutz vor unbefugtem Zugriff und Verlust  

## Rechtsgrundlagen (Art. 6) und besondere Kategorien (Art. 9)

- **Rechtsgrundlage**: Eine Verarbeitung personenbezogener Daten ist nur rechtmäßig, wenn mindestens eine der sechs Voraussetzungen aus Art. 6 Abs. 1 DSGVO erfüllt ist:
  1. Einwilligung der betroffenen Person,
  2. Erfüllung eines Vertrags mit der betroffenen Person (oder vorvertragliche Maßnahmen auf ihre Anfrage),
  3. Erfüllung einer rechtlichen Verpflichtung,
  4. Schutz lebenswichtiger Interessen,
  5. Wahrnehmung einer Aufgabe im öffentlichen Interesse oder in Ausübung öffentlicher Gewalt,
  6. berechtigtes Interesse des Verantwortlichen oder eines Dritten, sofern nicht die Interessen oder Grundrechte der betroffenen Person überwiegen.

  Die Einwilligung ist also nur *eine* von sechs möglichen Grundlagen – ein Onlineshop braucht für die Lieferadresse keine gesonderte Einwilligung, denn die Verarbeitung ist zur Vertragserfüllung erforderlich.

- **Besondere Kategorien personenbezogener Daten** (Art. 9 DSGVO, umgangssprachlich „sensible Daten“): Daten, aus denen die rassische oder ethnische Herkunft, politische Meinungen, religiöse oder weltanschauliche Überzeugungen oder die Gewerkschaftszugehörigkeit hervorgehen, sowie genetische Daten, biometrische Daten zur eindeutigen Identifizierung, Gesundheitsdaten und Daten zum Sexualleben oder zur sexuellen Orientierung. Ihre Verarbeitung ist **grundsätzlich untersagt** (Art. 9 Abs. 1) – aber nicht absolut: Art. 9 Abs. 2 zählt abschließend Ausnahmen auf, etwa die ausdrückliche Einwilligung, Pflichten aus dem Arbeits- und Sozialrecht, Daten, die die betroffene Person offensichtlich selbst öffentlich gemacht hat, die Gesundheitsversorgung oder die wissenschaftliche Forschung unter Schutzmaßnahmen. Die Religionszugehörigkeit darf also verarbeitet werden, wenn eine dieser Ausnahmen greift; ohne eine solche Ausnahme reicht auch keine der sechs Rechtsgrundlagen aus Art. 6.

## Privacy by Design und by Default

- **Privacy by Design**: Datenschutz muss schon bei der Konzeption von Systemen mitgedacht werden.
- **Privacy by Default**: Systeme sollen standardmäßig datensparsame Einstellungen haben.

Beispiel: Voreinstellungen dürfen keine unnötige Datenerhebung zulassen.

## Datensparsamkeit

Ein zentrales Prinzip im Datenschutz. Es bedeutet:
- Keine Erhebung irrelevanter Daten
- Verzicht auf optionale Angaben (z. B. Alter bei Bestellung, wenn nicht erforderlich)
- Hinweis auf Freiwilligkeit und Voreinstellung auf "nicht erheben"


## Weiterführende Begriffe und Konzepte

- **Pseudonymisierung**: Verarbeitung in einer Weise, dass Daten ohne zusätzliche Informationen nicht einer Person zugeordnet werden können.
- **Rechte Betroffener**: z. B. Auskunft, Löschung, Berichtigung, Widerspruch
- **Datenübermittlung in Drittländer**: Nur bei angemessenem Datenschutzniveau zulässig

## Weiterführende Ressourcen

- [DSGVO in einfachen Worten](https://eu-datenschutz-grundverordnung.net/eu-dsgvo/)
- [Volltext der DSGVO (EUR-Lex)](http://eur-lex.europa.eu/legal-content/DE/TXT/PDF/?uri=CELEX:32016R0679)
- [Checkliste für technische & organisatorische Maßnahmen (BayLDA)](https://www.lda.bayern.de/media/checkliste/baylda_checkliste_tom.pdf)
- [Film: *Democracy – Im Rausch der Daten* (bpb)](https://www.bpb.de/mediathek/254194/democracy-im-rausch-der-daten)