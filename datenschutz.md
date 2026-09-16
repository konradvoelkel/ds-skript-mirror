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