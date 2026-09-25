# Änderungsliste für die Folien

_Abgleich der Beamer-Folien mit dem Vorlesungsskript, Stand 25. September 2026. Geprüft wurden die
15 Decks mit LaTeX-Quelle (VL 01–10, 15–17, 19, 20) in der Fassung von Konrad Völkel (Dateien vom
April bis Juli 2026); spätere Bearbeitungen sind nicht berücksichtigt. Die Liste ist zum Lesen und
Abarbeiten gedacht; an den Folien selbst wurde für die Liste nichts geändert._

**Das Buch** ist das Vorlesungsskript unter <https://voelkel.pages.cs.uni-duesseldorf.de/ds-skript/>.
Kapitel werden mit Titel und Adressteil genannt, etwa „Erwartungswert und Varianz (erwartungswert)“
für die Seite `…/ds-skript/erwartungswert`. Das Buch ist im September 2026 gründlich durchgesehen
worden und an einigen Stellen genauer als die Folien; wo Buch und Folie sich widersprechen, gilt
unten das Buch.

**Schweregrade**

- **A** sachlich falsch: eine Formel, Zahl oder Aussage, die so gelernt falsch wäre.
- **B** unpräzise, uneinheitlich oder im Widerspruch zum Buch; sollte angeglichen werden.
- **C** Kleinkram: Tippfehler, Notation, Datum, Kosmetik.

## 0. Überblick

| Deck | A | B | C | Kern |
|---|---|---|---|---|
| VL 01 | 1 | – | 2 | Cox-Jaynes: „unvereinbar“ statt „unabhängig“ |
| VL 02 | – | – | 2 | nur Tippfehler |
| VL 03 | – | – | 1 | Jahreszahl |
| VL 04 | 1 | – | – | mittlerer Fehler 7 ist die Summe, nicht das Mittel |
| VL 05 | 1 | 1 | 4 | Definition unabhängiger Zufallsvariablen auf getrennten Räumen |
| VL 06 | 1 | 2 | 4 | Stellenzahl per ⌈log⌉, „Verteilungsfunktion“ für die pmf, Poisson-Grenzwert |
| VL 07 | 1 | 1 | 4 | Trägerdefinition, cdf mit offenem Intervall |
| VL 08 | – | 3 | 1 | Z_N statt S_N, Berry-Esseen-Konstante, Max-Entropie-Tabelle |
| VL 09 | – | – | 4 | nichts Sachliches; „Dispersion precedes location“ ist korrekt |
| VL 10 | 3 | 1 | 3 | Summen- statt Produktregel, π₁ statt π₂, unsymmetrisches Σ im Code |
| VL 15 | – | – | 5 | Notation |
| VL 16 | 1 | 1 | 3 | k-Means minimiert quadrierte Abstände; log-Trick wegen Monotonie |
| VL 17 | – | 3 | 2 | Untertitel; Herleitung setzt symmetrisches M/A voraus |
| VL 19 | 2 | – | 2 | Klassifikator-Ungleichung verkehrt herum, mean(X) statt mean(y) |
| VL 20 | 2 | 2 | 1 | β₁x₂, `se`, „multilinear“ |
| **Summe** | **14** | **14** | **38** | dazu sieben Querschnittspunkte (Abschnitt 1) |

Reihenfolge fürs Abarbeiten: erst alle A, dann B, C nur beim Gelegenheitsbesuch im Deck.

## 1. Querschnitt (alle Decks)

**Q1 (C) Datumsangaben.** VL 03 trägt `\date{23.04.2025}` und VL 05 `\date{30.04.2025}` (Jahr),
VL 06 und VL 07 tragen beide `07.05.2026` (eines davon ist falsch). Für den nächsten Durchlauf
müssen ohnehin alle Daten neu; Vorschlag: `\date{}` weglassen oder nur das Semester eintragen.

**Q2 (C) Kopfzeile des Headers.** `Data Science 2026 header.tex` setzt Autor und Semester
(`\author[Sommersemester 2026]{Dr. Konrad Völkel, Sommersemester 2026}`) und im `\hypersetup`
`pdftitle={Data Science SoSe 2026 HHU}` und `pdfauthor`. Für eine andere Dozentin sind das drei
Stellen in einer Datei.

**Q3 (C) Notation n und N.** Das Buch benutzt N oder n für die Stichprobengröße, d für die Dimension,
k für Cluster und Regressoren. Auf den Folien wechselt der Buchstabe innerhalb eines Frames (VL 08
Berry-Esseen: N im Satz, n=30 im Text; VL 15 „Beispiel“ Varianz: N und n; VL 16 Server-Logfiles:
Σ bis N, davor n) und VL 16 nennt die Dimension n.

**Q4 (C) Operatoren in Formeln.** mae, mse, rmse, mean, median, argmin, Cov stehen in Formeln als
kursive Variablenketten (VL 04, 05, 10, 17, 20). Der Header kennt schon `\argmax` und `\supp`;
ergänzen um `\DeclareMathOperator*{\argmin}{argmin}`, `\DeclareMathOperator{\Cov}{Cov}` und für
mean, median, mae, mse, rmse entweder Operatoren oder `\texttt` wie im Buch.

**Q5 (–) Verweise auf das Buch.** Alle „Ab jetzt ins Notebook“-Verweise passen zu vorhandenen
Kapiteln (Stochastik programmieren, Dimensionsreduktion mit Animation, Lineare Regression mit
Overfitting/Melbourne/Pipelines/Regularisierung, Kernel-Methoden). Einzige Ausnahme: VL 07, siehe
VL07-6.

**Q6 (–) Umstellungen im Buch, die die Folien nicht nachziehen müssen.** Erwartungswert erst
diskret (VL 04), dann stetig (VL 07): passt schon. Das Simpson-Paradoxon steht im Buch vor der
Visualisierung, auf den Folien in der eigenen Sitzung VL 11: bleibt. Klassifikation und Gütemaße
stehen im Buch jetzt vor k-Means (Kapitel k-Means); die Frames „Klassifikation“ und „Klassifikation
vs. Clustering“ in VL 19 können als Wiederholung bleiben. Die neuen Beweise im Buch (Markov,
Tschebyscheff, schwaches Gesetz der großen Zahlen: VL 05 hat sie schon; Verschiebungssatz,
Transformationsformel: auf den Folien nur als Aussage, das reicht). Der Auftakt mit Reinhart-Rogoff
betrifft VL 00.

**Q7 (–) Bilder.** Für den Vortrag unproblematisch. Im öffentlichen Repositorium sind einige Bilder
der Folien als Fremdinhalte gekennzeichnet (Liste in `README.md` in diesem Ordner); ein Ersatz ist
nicht eilig.

## 2. Je Deck

Zu jedem Punkt: Folie (Frametitel), was dasteht, was stehen sollte, warum (mit Buchstelle).

### VL 01 „Herleitung des Wahrscheinlichkeitsbegriffs“ (16.04.2026)

**VL01-1 (A) Folie „Von Plausibilität zur Wahrscheinlichkeit“, Untertitel „Cox-Jaynes-Theorem“.**
Ist: „für eine Menge paarweiser **unabhängiger** Aussagen A₁,…,Aₙ gilt plausi(⋁Aᵢ) = Σ plausi(Aᵢ)“.
Soll: „paarweise **unvereinbarer** (sich gegenseitig ausschließender) Aussagen“. Additivität gilt für
disjunkte Ereignisse, nicht für unabhängige; für unabhängige A, B ist P(A∨B) = P(A)+P(B)−P(A)P(B).
Buch: Einführung in die Stochastik (intro-stochastik), Liste nach dem Cox-Jaynes-Absatz.

**VL01-2 (C) Folie „Beispiel“ (Ω = {R,G,T}), Problem 1.** Ist: `P(\{R\})+(\{G\})+(\{T\})`. Soll:
`P(\{R\})+P(\{G\})+P(\{T\})`; zweimal fehlt das P. Der Rest der Folie ist richtig
(2/3+1/6+1/3 = 7/6 > 1, deshalb 1/2).

**VL01-3 (C) Folie „Definition: Ereignisraum“, Punkt 3.** Ist: „A₁,…, ∈ 𝓕“. Soll: „A₁, A₂, … ∈ 𝓕“.

### VL 02 „Zufallsvariable, Zufall, pmf, Wahrscheinlichkeitsvektor“ (21.04.2026)

Inhaltlich deckungsgleich mit dem Kapitel Zufallsvariablen und Verteilungen
(zufallsvariablen-verteilungen); nichts Sachliches.

**VL02-1 (C) Folien „Messbare Abbildung“ und „Induziertes Maß (Bildmaß)“.** In der Urbild-Formel
steht `{ y \in Y : f(y) \in A }`, die Menge heißt aber 𝒴 (`\mathcal{Y}`), zweimal.

**VL02-2 (C) Folie „Menge aller Wahrscheinlichkeitsvektoren“.** „Für n=2 ist Δ₂ ein Intervall
(welches in der Ebene zwischen (0,1) und (1,0) verläuft.“ Die schließende Klammer fehlt.

### VL 03 „Einführung in Python“ (Datum 23.04.2025)

Inhalt passt zum Kapitel Einführung in Python (intro-python): dynamische Bindung, IEEE 754, `//` und
`%`, unveränderliche Schlüssel, `range`-Objekt, eigener Scope bei `def`.

**VL03-1 (C) Titelfolie.** `\date{23.04.2025}`, das Jahr stimmt nicht (siehe Q1).

### VL 04 „Daten, Stichprobe, Modell; Abweichungen und Mittel; Momente“ (28.04.2026)

Alle Zahlen im Körpergrößen-Beispiel nachgerechnet und richtig (d₁ = 16, d₂² = 86, mae 4, mse
21,5; Median 167, Mittelwert 166,75, mae 9,25, mse 90,6875 ≈ 9,523²), bis auf:

**VL04-1 (A) Folie „Beispielvergleich von Daten: einfacher Fall“ (konstantes Modell 165).** Ist:
„Der mittlere Fehler ist (13−5−10+9)/4 = 7, eine trügerisch geringe Zahl.“ Soll: „… = 7/4 = 1,75,
eine trügerisch geringe Zahl.“ 7 ist die Summe der Abweichungen, der mittlere Fehler ist 1,75 (und
die Pointe wird dadurch sogar stärker: 1,75 gegenüber mae 9,25). Buch: Erwartungswert und Varianz
(erwartungswert), Abschnitt zum konstanten Modell.

Sonst nur Q4 (kursive Operatoren `argmin`, `mae`, `mse`, `median`, `mean`).

### VL 05 „Unabhängigkeit; Markov, Tschebyscheff, große Zahlen“ (Datum 30.04.2025)

**VL05-1 (A) Folie „Unabhängige Zufallsvariablen“.** Ist: „Sei Ω ein Wahrscheinlichkeitsraum, dann
heißen zwei Zufallsvariablen X: Ω′_X → Ω_X, Y: Ω′_Y → Ω_Y unabhängig, wenn …“, und die gemeinsame
Verteilung wird als (X,Y): Ω′_X × Ω′_Y → Ω_X × Ω_Y erklärt. So können X und Y gar nicht abhängig
sein: auf dem Produktraum mit Produktmaß faktorisiert jede solche gemeinsame Verteilung automatisch.
Abhängigkeit setzt einen **gemeinsamen** Definitionsbereich voraus. Soll: „X: Ω → Ω_X und Y: Ω → Ω_Y
heißen unabhängig, wenn für alle A ⊆ Ω_X, B ⊆ Ω_Y gilt P(X∈A, Y∈B) = P(X∈A)·P(Y∈B); dabei ist
P(X∈A, Y∈B) := P((X,Y) ∈ A×B) für die gemeinsame Verteilung von (X,Y): Ω → Ω_X × Ω_Y.“ Die
pmf-Zeile darunter (P(X=x, Y=y) = p(x)q(y) für alle x, y) bleibt. Buch: Erwartungswert und Varianz
(erwartungswert), Definition „Familie von Zufallsvariablen (Y_i), Y_i: Ω → Ω_i heißt unabhängig …“
und die Bemerkung dazu (X, Y: Ω → ℝ, gemeinsame Verteilung als eine Zufallsvariable mit Werten in ℝ²).

**VL05-2 (B) Folie „Beispiel zur Unabhängigkeit“ (zwei Würfel).** Ist: P(A∩B) wird als P(A)·P(B) =
1/12 „berechnet“, danach „Da A und B sich auf unterschiedliche Würfel beziehen, sind sie unabhängig.“
Das ist zirkulär, wenn die Folie Unabhängigkeit *zeigen* soll. Soll: A∩B = {(2,6),(4,6),(6,6)}
auszählen, P(A∩B) = 3/36 = 1/12, und **dann** feststellen, dass 1/12 = 1/2 · 1/6 gilt, also
unabhängig. Buch: Erwartungswert und Varianz (erwartungswert), Beispiel zwei Würfel (Auszählen zuerst).

**VL05-3 (C) Titelfolie.** `\date{30.04.2025}`, Jahr.

**VL05-4 (C) Folie „Markov“, Beweis.** Ist: Σ von x = −∞ bis ∞ und Σ von x = a bis ∞ als wären es
ganzzahlige Laufindizes. Soll: Σ über x ∈ X(Ω) und Σ über x ≥ a (Buch: Beweis der
Markov-Ungleichung im Kapitel Erwartungswert und Varianz).

**VL05-5 (C) Folie „Tschebyscheff“, Beweis.** Ist: „Die Ungleichung P((·)² ≤ (·)²) auf der linken
Seite ist äquivalent zu P(|·| ≤ |·|).“ Im Beweis steht aber ≥. Soll: beide Zeichen auf ≥ (oder
„gilt für ≤ wie für ≥“).

**VL05-6 (C) Folie „Korrelation“.** „Korrelation misst man mit dem Korrelationskoeffizienten, der
Kovarianz.“ Soll: „… mit dem Korrelationskoeffizienten bzw. der Kovarianz.“

**VL05-7 (C, optional) Folie „Gesetz der großen Zahlen“.** Die Folie schreibt die
Mittelwert-Abweichung als X̄ₙ − 𝔼X, das Buch als $\overline{X_n^\ast}$. Beides ist richtig; wenn
angeglichen werden soll, eher die Folie, weil die Studierenden das Buch lesen.

### VL 06 „Entropie; Diskrete Verteilungen; Numpy“ (07.05.2026)

**VL06-1 (A) Folie „Logarithmus zur Erinnerung“, letzter Punkt.** Ist: „⌈log₁₀(y)⌉ ist also die
Anzahl der Stellen.“ Das stimmt nicht bei Zehnerpotenzen: ⌈log₁₀(100)⌉ = 2, aber 100 hat drei
Stellen. Soll: „⌊log₁₀(y)⌋ + 1 ist die Anzahl der Dezimalstellen (zur Basis 2 entsprechend die
Binärstellen).“ Buch: Erwartungswert und Varianz (erwartungswert), Einschub Logarithmus.

**VL06-2 (B) Folien „Das Setting: eine Nachricht“ (zweite) und „Konvention“.** Ist: „p: Σ → [0,1]
die **Verteilungsfunktion** von X, d.h. p(z) = P({z})“ und in der Konvention „heißt pmf,
Verteilungsfunktion, Zähldichte von P“. Im Buch ist „Verteilungsfunktion“ für die cdf F(x) = P(X ≤ x)
reserviert, und das Kapitel Wichtigste diskrete Verteilungen (wichtigste-diskrete-verteilungen) sagt
ausdrücklich, dass es den Namen für die pmf nicht verwendet. Soll: „die pmf
(Wahrscheinlichkeitsfunktion, Zähldichte) von X, d.h. p(z) = P(X = z)“; in der Konvention „pmf,
Zähldichte“ (allenfalls: „manche sagen Verteilungsfunktion; wir reservieren das Wort für die cdf“).

**VL06-3 (B) Folie „Poisson-Binomialverteilung“, Grenzübergang.** Ist: „… die pᵢ schnell genug
kleiner werden (i → ∞), genauer lim_{i→∞} i·pᵢ = λ > 0“, danach eine Formel mit pₙ. Der Index im
Text (i) ist nicht der der Formel (n), und lim i·pᵢ beschreibt nicht die Binomialverteilung mit n
Versuchen. Soll: „Binomialverteilung mit n Versuchen und pₙ = λ/n, allgemeiner n·pₙ → λ; dann …“
Buch: Wichtigste diskrete Verteilungen, Satz zum Grenzübergang („(pₙ) mit n·pₙ → λ“).

**VL06-4 (C) Folie „Konvention“, letzter Punkt.** Ist: „H(X) = −Σ p(ω) log₂ p(ω)“. Das ist die
Entropie der Verteilung auf Ω; sie stimmt mit H(X) nur überein, wenn X injektiv ist. Soll:
„H(X) = −Σₓ p_X(x) log₂ p_X(x)“, passend zur Zeile davor mit p_X.

**VL06-5 (C) Folie „Logarithmus' freundliche Eigenschaften“.** „log₂(77) ≈ 6.266“: der Wert ist
6,2668, gerundet also 6,267 (Buch: ≈ 6,27).

**VL06-6 (C) Folie „Diskrete Gleichverteilung“.** „p(ω) = 1/n“ ohne Angabe von Ω; die Formeln
𝔼(X) = (n+1)/2 und 𝕍(X) = (n²−1)/12 gelten für die Werte 1,…,n. Ein „auf {1,…,n}“ in der ersten
Zeile genügt.

**VL06-7 (C) Folie „Das Setting: eine Nachricht“ (erste).** Das Alphabet soll Σ = {a, b, …, z, ␣}
heißen, im PDF steht aber „{a, b, …, z, }“: die Schrift Source Sans Pro hat das Zeichen ␣
(`\textvisiblespace`) nicht, LuaLaTeX lässt es kommentarlos weg (Log: „Missing character“).
Soll: `\textvisiblespace` aus einer Schrift nehmen, die es hat (etwa `{\ttfamily\textvisiblespace}`
mit Source Code Pro), oder schlicht „Leerzeichen“ schreiben.

Geprüft und richtig: Selbstinformation und 32 Zeichen = 5 bit; 77 = 1001101₂; 4,7 bit je Zeichen
bei 26 Buchstaben; Bernoulli-Ableitung −log₂(p/(1−p)); Varianz der Poisson-Binomialverteilung.

### VL 07 „Stetige Zufallsvariablen“ (Datum 07.05.2026, wie VL 06)

**VL07-1 (A) Folie „Träger einer Zufallsvariable“, Definition.** Ist: `\supp(P) := \bigcap
\overline{\{ A \subseteq \Omega : P(A) = 1 \}}`, also der Abschluss (oder ein Überstrich über die
Familie) des Schnitts aller Mengen vom Maß 1. Dieser Schnitt ist für jede Verteilung mit Dichte leer
(für U([0,1]) hat [0,1]∖{x} für jedes x noch Maß 1), sein Abschluss also auch. Soll:
`\supp(P) := \bigcap \{ A \subseteq \Omega \text{ abgeschlossen} : P(A) = 1 \}` (der Schnitt läuft
nur über **abgeschlossene** Mengen vom Maß 1). Der Klammertext „(die kleinste [abgeschlossene]
Menge, für die P(supp P) = 1 gilt)“ passt dann. Buch: Stetige Verteilungen (stetige-verteilungen),
Definition Träger und der Absatz „Das Wort abgeschlossen ist dabei keine Dekoration“. Diese Stelle
war im Buch bis September 2026 ebenfalls falsch; das Buch ist inzwischen korrigiert.

**VL07-2 (B) Folie „Kumulativ“ (erste, für ein Maß P).** Ist: „c ↦ P((−∞, c))“, offenes
Intervall. Die zweite „Kumulativ“-Folie und das Buch definieren P(X ≤ c), also (−∞, c]. Für
Verteilungen mit Dichte ist das egal, für diskrete nicht (Sprungstellen; das Buch zeichnet die cdf
der Dirac-Verteilung). Soll: „c ↦ P((−∞, c])“.

**VL07-3 (C) Folie „Träger einer Zufallsvariable“, Zusatz.** „Für diskrete Verteilungen gilt
supp(P) = {x ∈ Ω : p(x) > 0}.“ Gilt für endliches Ω; bei abzählbar unendlich vielen Werten kommen
die Häufungspunkte dazu (Buch: „bei unendlich vielen Werten kommen noch deren Häufungspunkte dazu“).
Ein „(für endliches Ω)“ reicht.

**VL07-4 (C) Folien „Kumulativ“.** „also F eine Stammfunktion von f und f die Ableitung von F“:
Soll: „… und f = F′ überall dort, wo f stetig ist“.

**VL07-5 (C) Titelfolie.** Gleiches Datum wie VL 06 (07.05.2026); siehe Q1.

**VL07-6 (C) Folie „Weiter geht's …“.** Verweist auf die Notebooks „Normalverteilung“ und
„wichtigste stetige Verteilungen und Scipy.Stats“. Die Kapitel heißen „Normalverteilung“ und
„Wichtigste stetige Verteilungen“ (Buchteil „Stetige Stochastik und Scipy“).

Geprüft und richtig: die Definition „stetig = überabzählbares Bild und Dichte“ (das Buch ist darauf
angeglichen); „Teilmenge M ⊂ ℝⁿ heißt abgeschlossen“ (das Buch definiert Abgeschlossenheit ebenfalls
in ℝⁿ); Beispiel auf [5,8); Momente der Gleichverteilung auf [0,1] und [a,b].

### VL 08 „Die Gaußsche Normalverteilung“ (19.05.2026)

**VL08-1 (B) Folie „Der zentrale Grenzwertsatz (CLT)“.** Ist: die standardisierte Summe heißt Sₙ
(genauer S_N := (1/(σ√N)) Σ Xᵢ), auf der zweiten Folie des Decks ist Sₙ := Σ Xᵢ aber schon die
**unnormierte** Binomialsumme. Soll: Z_N für die standardisierte Summe, wie im Buch (Kapitel
Normalverteilung (normalverteilung): „Z_N … die auf Erwartungswert 0 und Varianz 1 normierte Version
der Summe S_N“). Dasselbe in „Konvergenzgeschwindigkeit (Berry-Esseen)“.

**VL08-2 (B) Folie „Konvergenzgeschwindigkeit (Berry-Esseen)“.** Ist: „Es existiert eine Konstante
C > 0,4409 mit der Eigenschaft …“. Eine **untere** Schranke für C macht den Satz leer (mit jedem
größeren C gilt die Ungleichung erst recht); brauchbar ist die obere Schranke. Soll: „Es existiert
eine Konstante C mit 0,41 ≤ C ≤ 0,48 und der Eigenschaft …“ (Buch, Satz von Berry-Esseen; Stand der
Forschung: Esseen 1956 untere, Shevtsova 2011 obere Schranke 0,4748). Dazu „reicht n=30“ → N (Q3).

**VL08-3 (B) Folie „Ausblick: Maximale Entropie bei anderem Träger“, letzter Punkt.** Ist: „Träger
[a,b], feste Varianz σ² bekannt ⇒ gestutzte Normalverteilung“. Buch (Tabelle im Kapitel
Normalverteilung): „[a,b], Erwartungswert **und** Varianz ⇒ gestutzte Normalverteilung
(`scipy.stats.truncnorm`)“. Ohne festen Erwartungswert ist die Aussage so nicht richtig. Soll: „fester
Erwartungswert μ und feste Varianz σ² bekannt“.

**VL08-4 (C) Folie „Praxisbeispiel: Der N ≥ 30-Mythos“.** „reicht n=30 bei Weitem nicht“: N wie im
Rest des Decks.

Geprüft und richtig: de Moivre-Laplace, Gauß-Integral samt Beweis, 𝔼 = μ, Standardisierung,
Summe unabhängiger Normalverteilungen, Satz maximale Entropie mit Träger ℝ (das Buch formuliert ihn
genauso), Laplace-Bedingung Np ≥ 10 und N(1−p) ≥ 10 (wie im Buch).

### VL 09 „Deskriptive Statistik“ (21.05.2026)

Die Folie „Dispersion precedes location“ ist **korrekt** (Mittelwert minimiert die mittlere
quadratische Abweichung, Bereichsmitte die maximale absolute Abweichung); eine ältere Notiz hatte das
in Zweifel gezogen.

**VL09-1 (C) Folie „Skalen“, Intervallskala.** Ist: „… es gibt ein Abstandsmaß und einen
festgelegten Nullpunkt“. Soll: „einen **willkürlich** festgelegten Nullpunkt“ (Abgrenzung zur
Verhältnisskala mit absolutem Nullpunkt; Buch: „der Nullpunkt ist aber willkürlich festgelegt“).
Außerdem ist „Kardinalskala“ der Oberbegriff für Intervall- und Verhältnisskala, nicht ein Synonym für
Intervallskala; das Buch schreibt „Intervallskala (eine Kardinalskala)“.

**VL09-2 (C) Folie „Explorative Datenanalyse vs Data Mining“.** „Visualsierung“ → „Visualisierung“.

**VL09-3 (C) Folie „Linienplots“.** `np.linspace(0, 6.28, 360)`: mit `2*np.pi` schließt sich der
Kreis; so bleibt eine kleine Lücke.

**VL09-4 (C) Folie „Geschichte“ (Grammatik der Grafiken).** Die Liste steht im Buch (Deskriptive
Statistik (deskriptive-statistik), Abschnitt Grammatik der Grafiken) wortgleich, also an beiden
Stellen prüfen: Bertin, Sémiologie graphique, ist von 1967 (englische Ausgabe 1983); „The Grammar of
Graphics“ ist von Wilkinson allein, 1999 (2. Auflage 2005); „Wilkinson, Anand, Grossman“ ist die
Autorengruppe eines anderen Papers (Scagnostics, 2005); `ggplot2` erschien 2007 (der Vorläufer
`ggplot` 2005). „2010: Wickham: A Layered Grammar of Graphics“ stimmt.

Geprüft und richtig: Skalenniveaus und Beispiele (Likert und Pegelstand stehen auch im Buch bei der
Intervallskala), Lagemaße, Streuungsmaße, Farbsehschwächen (jeder 12. Mann, jede 200. Frau).

### VL 10 „Multivariate Stochastik“ (26.05.2026)

**VL10-1 (A) Folie „Bedingte und gemeinsame Verteilung“.** Ist: „… folgt die **Summenregel**:
P(X=x, Y=y) = P(Y=y|X=x) P(X=x)“. Das ist die **Produktregel**; die Summenregel ist das
Aufsummieren über die nicht interessierende Variable (Folie davor). Buch: Kovarianz und Abhängigkeit
(kovarianz): „Diese Formel heißt Produktregel; die Summenregel ist die Bemerkung davor“.

**VL10-2 (A) Folie „Marginalverteilungen berechnen“.** Ist: „Dabei haben wir π₁⁻¹(A) = X(Ω) × A in
disjunkte Teilmengen zerlegt.“ Berechnet wird die Verteilung von Y, der zweiten Koordinate; das
Urbild X(Ω) × A gehört zu π₂. Soll: π₂⁻¹(A). Buch: Kovarianz und Abhängigkeit, gleiche Stelle mit
π₂ (dort im September 2026 korrigiert).

**VL10-3 (A) Folie „Visualisierung einer bivariaten Verteilung“ (Code) und das Bild danach.**
Ist: `Sigma = [[1,2],[0,1]]`. Das ist keine Kovarianzmatrix (nicht symmetrisch); SciPy liest nur eine
Dreieckshälfte, das Bild zeigt also etwas anderes als der Code behauptet. Soll: z.B.
`Sigma = [[1, 0.7], [0.7, 1]]` wie im Buch, Bild `figures/normalmarginal.png` neu erzeugen und dabei
das leere Panel `axs[1,0]` ausblenden (`axs[1,0].axis("off")`). Buch: Kovarianz und Abhängigkeit,
Multivariate Normalverteilung (multivariate-normalverteilung).

**VL10-4 (B) Folie „Die Likelihood in der Praxis“.** Ist: „Denken wir an die 3 Verteilungen:
Datenerzeugung X → Daten D → Modell Y. Die Likelihood P(X=D | Y=D) …“ und später „P(X=D | H)“.
„X = D“ und „Y = D“ sind keine Ereignisse in dem Sinn, in dem die Folie davor P(Y=y | X=x) benutzt.
Soll: durchgehend P(D | H) (Wahrscheinlichkeit der Daten unter der Hypothese) bzw. für die
Normalverteilung L(μ,σ) = Π p_{μ,σ}(x); die letzten zwei Zeilen der Folie sagen das schon richtig.
Buch: Kovarianz und Abhängigkeit, Absatz zur Likelihood in der Praxis.

**VL10-5 (C) Folie „Der Satz von Bayes“.** „Aus dem **Beweis** P(A|B) := P(A∩B)/P(B) folgt“ →
„Aus der **Definition** …“.

**VL10-6 (C) Folie „Marginalverteilungen“.** „Diese Xᵢ heißen Randverteilungen“ → „Die Verteilungen
der Xᵢ heißen Randverteilungen oder Marginalverteilungen“ (Buch, Kovarianz und Abhängigkeit).

**VL10-7 (C) Folie „Eigenschaften der Kovarianz“.** „Cov(X,X) = 0 nur für konstantes X“ →
„fast sicher konstantes X“.

### VL 15 „Schätztheorie“ (16.06.2026)

Deckungsgleich mit dem Kapitel Statistische Modelle und Schätzer (statistische-modelle); nur Notation.

**VL15-1 (C) Folie „Parametrische Modelle, Standardmodelle“, zweite Definition.** „𝓕 = 𝒫(X)“ →
„𝓕 = 𝒫(𝒳)“.

**VL15-2 (C) Folie „Beispiel“ (Würfel).** „Konkret für θ = (θ₁,…,θₙ)“ → „θ = (θ₁,…,θ₆)“.

**VL15-3 (C) Folie „Folgen von Schätzern“.** „lim_{n→∞} Tₙ →^{P_θ} τ(θ)“ vermischt Limes und
Konvergenzpfeil. Soll: „Tₙ →^{P_θ} τ(θ) für n → ∞“.

**VL15-4 (C) Folie „Beispiel“ (Varianz-Schätzer).** Erst N (σ²_N, Σ bis N), dann „Bias −σ²(X)/n,
für n → ∞“: ein Buchstabe (Q3).

**VL15-5 (C) Folie „Statistik – als mathematischer Begriff“.** „Σ ein weiterer Ereignisraum (d.h.
eine Ergebnismenge)“: Ereignisraum und Ergebnismenge sind in VL 01 verschieden definiert; gemeint
ist eine Menge mit σ-Algebra, also „ein weiterer Ereignisraum (Σ, 𝓕_Σ)“.

### VL 16 „Maximum Likelihood“ (18.06.2026)

**VL16-1 (A) Folie „Beispiel k-Means“ (zweite).** Ist: „… die Zentroide, für die die Summe der
euklidischen Abstände eines jeden Punktes xᵢ eines Samples minimal sind.“ k-Means minimiert die
Summe der **quadrierten** Abstände zum jeweils **nächsten** Zentroid (die Trägheit); die Summe der
unquadrierten Abstände gehört zu einem anderen Verfahren (k-Medoids/k-Medians). Soll: „die Summe der
quadrierten euklidischen Abstände eines jeden Punktes xᵢ zu seinem nächsten Zentroid minimal ist“.
Buch: Statistische Modelle und Schätzer, Beispiel k-Means; k-Means (kmeans), Trägheit
J = Σᵢ minⱼ ‖xᵢ − cⱼ‖².

**VL16-2 (B) Folie „Trick“.** Ist: „log konkav ⇒ ein Maximum der log-Likelihood ist auch ein Max.
der Likelihood.“ Der Grund ist die strenge **Monotonie** des Logarithmus (jede streng monotone
Transformation erhält die Maximalstellen), nicht die Konkavität. Soll: „log streng monoton wachsend ⇒
Likelihood und log-Likelihood haben dieselben Maximalstellen.“ Buch: Statistische Modelle und
Schätzer, Absatz zur log-Likelihood („Weil der Logarithmus streng monoton wächst …“).

**VL16-3 (C) Folien „Beispiel Server-Logfiles“ und „(pt. 2)“.** In derselben Formel Σ bis N und
davor n(log λ − λ mean(x)); ein Buchstabe (Q3).

**VL16-4 (C) Folie „Beispiel k-Means“ (erste).** „wenn n die Dimension der Daten ist“: das Buch
nennt die Dimension d; n/N ist die Stichprobengröße (Q3).

**VL16-5 (C) Folie „Bemerkung“ (Konsistenz).** „das heisst dass die Schätzwerte“ → „das heißt, dass
…“.

Geprüft und richtig: Likelihood- und MLE-Definition, Beispiel Normalverteilung (mean, σ; σ* ist kein
MLE), Ableitung nach μ, Exponentialverteilung samt zweiter Ableitung.

### VL 17 „Dimensionsreduktion mit PCA“ (23.06.2026)

**VL17-1 (B) Titelfolie.** Untertitel „Maximum Likelihood“ (aus VL 16 kopiert). Soll:
„Dimensionsreduktion mit PCA“ (so heißt die Section).

**VL17-2 (B) Folie „Beispiel“ (Kreis, Ellipse, beliebige Matrix M).** Ist: „… die Richtungen, die
von M am stärksten gestreckt werden. Dass wäre ein Vektor v mit Mv = λv für das größte solche λ.“
Für eine beliebige invertierbare Matrix (etwa Drehung plus Streckung) gibt es solche reellen
Eigenvektoren nicht unbedingt; die am stärksten gestreckte Richtung ist die des größten
Singulärwerts. Soll: „Für **symmetrisches** M ist das ein Vektor v mit Mv = λv für das größte λ (für
beliebiges M die Richtung des größten Singulärwerts, das lösen wir gleich über die
Kovarianzmatrix).“ Dazu „Dass“ → „Das“. Buch: Dimensionsreduktion (dimensionsreduktion), gleiche
Stelle mit dem Zusatz „Für symmetrisches M“.

**VL17-3 (B) Folie „Zutaten zusammensetzen“.** Ist: „Die empirische Kovarianzmatrix schätzt die
Kovarianzmatrix C ein, deren Wurzel A ist, also A² = C.“ Allgemein gilt C = A·Aᵀ; A² = C nur für
symmetrisches A. Die Folie „Letzter Schritt“ rettet das Ergebnis (Eigenvektor von C), aber die
Zwischenschritte („größter Eigenwert von A“) setzen die Symmetrie stillschweigend voraus. Soll: in
der Vorstellung „X = AY“ ein „mit symmetrischem A (reine Streckung)“ ergänzen; Buch:
Dimensionsreduktion, Zusammenfassung der Herleitung („wegen Σ = Σᵀ ist ΣΣᵀ = Σ²“).

**VL17-4 (C) Folie „Beobachtung“.** „Sample-Kovarianz Cov(x,y) = (1/n) Σ xᵢyᵢ“ gilt für zentrierte
Daten; ein „(zentrierte Daten)“ genügt.

**VL17-5 (C) Folie „Matrixwurzel“.** „Kovarianzmatrizen sind positiv definit“: allgemein positiv
**semi**definit (Buch definiert beides); positiv definit, wenn die Daten keinen echten Unterraum
aufspannen. Für die Wurzel reicht semidefinit.

Geprüft und richtig: die drei Schritte fit/transform/Reduktion, Orthonormalmatrix, Inverses =
Transponierte, Eigenvektor von C als Richtung größter Varianz, Optimierungszugang.

### VL 19 „Regression“ (25.06.2026)

**VL19-1 (A) Folie „Beispiel zur Klassifikation“.** Ist: Label Setosa = 0, Versicolor = 1, und
„Möglicher Klassifikator: prediction = [petal_length < 2.5]“. Diese Regel liefert 1 (= Versicolor)
genau für die kurzen Blütenblätter, also für Setosa; sie ist verkehrt herum. Soll: „prediction =
[petal_length ≥ 2.5]“ (oder die Label tauschen). Buch: k-Means (kmeans), Klassifikator in einer
Zeile: dort ist `prediction = (petal_length < 2.5)` die Regel „unter 2,5 cm, dann *setosa*“, mit
Wahrheitswert „ist es setosa?“, also die umgekehrte Kodierung.

**VL19-2 (A) Folie „Regression als Schätzer“, Beispiel.** Ist: „Y = β + ε (ein konstantes
Modell). Mögliche Lösung: β = mean(X).“ Das konstante Modell benutzt X gar nicht; die
kleinste-Quadrate-Lösung ist der Mittelwert der **Zielgröße**. Soll: „β = mean(y)“. Buch: Lineare
Regression (lineare-regression), Beispiel konstante Funktionen („β₁ = mean(y)“).

**VL19-3 (C) Folie „Regressionsmodell, formal (Herleitung)“.** „ε := predicted_petal_width −
petal_width“, zwei Folien später „Residuen εᵢ = yᵢ − yᵢ^pred“. Vorzeichen vereinheitlichen auf
yᵢ − yᵢ^pred (Buch: Residuum = yᵢ − f(xᵢ, β)).

**VL19-4 (C, optional) Folie „Beispiel zur Regression“.** „Breite ungefähr die halbe Länge minus 1“
ist als grobe Regel gemeint; kleinste Quadrate liefern ≈ 0,42·Länge − 0,36 (Buch). Ein „grob“ oder
„aus dem Bild geschätzt“ nimmt der Formel den Anschein einer Rechnung.

### VL 20 „Lineare Regression“ (30.06.2026)

**VL20-1 (A) Folie „Beispiel zur Linearen Regression“.** Ist: „f(x₁,x₂;β₀,β₁,β₂) := β₁x₂ + β₂x₂ +
β₀“. Soll: „β₁x₁ + β₂x₂ + β₀“.

**VL20-2 (A) Folie „Lineare Regression mit Scipy.Stats“.** Ist: „`se` der quadrierte Fehler
(squared error), also das mittlere Residuenquadrat“. `stderr` ist laut SciPy der **Standardfehler
der Steigungsschätzung** β₁ (das Objekt hat zusätzlich `intercept_stderr`). Soll: „`se` der
Standardfehler der geschätzten Steigung“. Buch: Lineare Regression, Erklärung der
`linregress`-Rückgabewerte.

**VL20-3 (B) Folie „Multilineare Regression“ (Titel und zweimal im Text).** Der übliche Name ist
**multiple lineare Regression**; „multilinear“ bezeichnet in der Mathematik etwas anderes
(Multilinearformen). Buch: Lineare Regression („einfache lineare Regression“ / „multiple lineare
Regression“).

**VL20-4 (B) Folie „Lineare Regression als Schätzer“.** „Der kleinste-Quadrate-Schätzer ist ein
Maximum-Likelihood-Schätzer.“ Soll: „… bei normalverteilten Störgrößen“ (Buch: „wenn man die
Störgrößen als normalverteilt annimmt“).

**VL20-5 (C) Folie „Lineare Regression, formal“.** „Y = f(X; w, w₀) + ε mit f(x;w) = wᵀx + w₀“:
die Argumentliste von f muss w₀ enthalten.

Geprüft und richtig: kleinste Quadrate von Hand (β₁ ohne und mit Achsenabschnitt), `curve_fit`,
Verwechslungsgefahr mit der Richtung maximaler Varianz, Basisfunktionserweiterung, polynomiale
Regression „linear in den Gewichten“.

## 3. Geprüft und ohne Befund

Damit niemand dieselbe Arbeit zweimal macht: diese Stellen aus früheren Notizen sind in Ordnung.

- VL 09 „Dispersion precedes location“ (siehe oben) und die Aussage über Tortendiagramme.
- VL 07 „Teilmenge M ⊂ ℝⁿ heißt abgeschlossen“: Buch ebenso in ℝⁿ.
- VL 08 Satz maximale Entropie mit Voraussetzung „Träger ganz ℝ“ und die Laplace-Bedingung ≥ 10.
- VL 05 Gesetz der großen Zahlen (stark, daraus stochastische Konvergenz) und die Beweisskizze.
- VL 04 sämtliche Zahlen außer VL04-1.
- VL 02 komplett, VL 03 komplett (bis auf das Datum).
- VL 06 Poisson-Binomialverteilung (Erwartungswert, Varianz, Entropievergleich), Entropie der
  deutschen Sprache, xkcd-Beispiel.
- Alle Verweise „ins Notebook“ zeigen auf existierende Kapitel (Q5).

## 4. Decks ohne LaTeX-Quelle

Entscheidung (September 2026): diese Decks bekommen keine LaTeX-Quelle. Zwei Gruppen:

### 4a. Buchausdrucke: neu aus dem aktuellen Buch drucken statt pflegen

Sechs „Decks“ sind Ausdrucke von Buchkapiteln aus älteren Builds. Ihre Fehler sind im Buch inzwischen
behoben; die Pflege besteht darin, sie beim nächsten Durchlauf neu zu drucken (Browser „In PDF
drucken“ oder die Seiten aus dem Buch-PDF) oder sie ganz wegzulassen und auf das Kapitel zu
verweisen. Was sich seit dem Ausdruck im Buch geändert hat:

| Datei | Kapitel | Seit dem Ausdruck im Buch geändert |
|---|---|---|
| VL 08 Zusatz | Wichtigste stetige Verteilungen | Weibull: Varianz ergänzt, Maximum-Entropie-Aussage korrigiert; ZGWS-Steckbrief mit Z_N; Gleichverteilung als U([a,b]); Achsenbeschriftung der Dirac-cdf; Lognormal-Plotfenster; f-Strings |
| VL 12 | Multivariate Normalverteilung | Q(x,y) war um 1/(1−ρ²) falsch skaliert; „Σ dreht“-Absatz ersetzt; Integrationsreihenfolge dy dx; \exp |
| VL 14 | k-Means | Klassifikator und Gütemaße stehen jetzt vor k-Means; NMI-Ausgabe korrigiert (I(P;C)/mean(H)); Kugel statt Sphäre; Blütenblattlänge und -breite |
| VL 18 (PCA part 2) | Dimensionsreduktion | NMI-Text korrigiert; `np.linalg.eigh`; Zelle „erklärte Varianz“; Herleitung mit „für symmetrisches M“ |
| VL 22 | Relative Entropie | Kreuzentropie-Vorzeichen; Asymmetrie-Beispiel neu (p_t = (t, 1−t)); Summe über pᵢ > 0 mit ∞-Fall; h(X) = −H(f‖λ); Abschnitt „Definition und Eigenschaften“ |
| VL 24 | Expectation Maximization | Responsibilities-Formel; Normierung 1/(√(2π)σⱼ); Ableitung nach μ mit σⱼ²; nⱼ im k-Means-Spezialfall; BIC-Zelle; Rückblick und Ausblick; nur noch eine H1 |

Die Druckversion `Data Science 2026 Alle Folien Druckversion.tex` schließt 12, 14, 18, 22, 24 und
„Zusatz“ ohnehin aus.

### 4b. Eigenständige Decks in anderen Formaten: bekannte Fehler nur dokumentiert

| Deck | Quelle | Bekannte Fehler (Notizen vom September 2026; die Decks wurden dafür nicht erneut durchgesehen) |
|---|---|---|
| VL 00 Einführung | nur PDF | keine sachlichen |
| VL 11 Simpsons, Pandas | **pptx vorhanden** (`Data Science 2026 VL 11 Simpsons, Pandas.pptx`) | keine notiert |
| VL 13 Data Cleaning | nur PDF | S. 5: `outliers = df[(np.abs(st.zscore(df)) < 3).all(axis=1)]` liefert die **Nicht**-Ausreißer (Ausreißer: `(np.abs(z) >= 3).any(axis=1)`); in pandas 3 entfernt bzw. veraltet: `fillna(method='pad')` (→ `ffill()`), `infer_datetime_format` (weglassen), `.dt.weekday_name` (→ `.dt.day_name()`), `Timestamp.utcfromtimestamp` (→ `fromtimestamp(..., tz="UTC")`); S. 26 „`.*?` matcht 0 Zeichen oder mehr“ (genauer: so wenige wie möglich); S. 44 fehlt `from datetime import datetime`, und „eine Zeitzone ist ein fixer Offset“ unterschlägt die Sommerzeit |
| VL 21 Tests und Signifikanz | **pptx vorhanden** (`slides25/Data Science 2025 VL 20 Tests und Signifikanz.pptx`; Ansatz in LaTeX: `slides25/ansatz-2026-vl-21-als-tex.tex`) | S. 24: p = P(|T| ≤ t | H₀) ist falsch herum, richtig P(|T| ≥ t | H₀); das Buch nennt „n > 30“ nicht mehr als Bedingung für den z-Test (falls die Folie das tut, ebenfalls streichen) |
| VL 23 Datenschutz | nur PDF | keine sachlichen; zeitabhängig: Stand des EU-U.S. Data Privacy Framework (Buch: „Stand September 2026“); Formulierung „aus Faulheit“ bei Privacy by Default im Buch neutraler gefasst |
