# Zufallsvariablen und Verteilungen

[Vorlesungsaufzeichnung Zufallsvariablen und Verteilungen](https://media.hhu.de/channel/video/data-science-vl-2-wahrscheinlichkeitsmass-zufallsvariable-pmf-2025/d5149a6bce20e827dc30685847505f16/167)

Das typische 'Interface' für Wahrscheinlichkeitsverteilungen sind Zufallsvariablen.
Im Unterschied zu einer bloßen Verteilung spielt bei einer Zufallsvariable auch eine Rolle, welche konkreten Werte als Ergebnis eintreten können.

## Zufallsvariablen

Wir erinnern an die Definition, nun in der Notation, die wir im weiteren Verlauf verwenden möchten:

:::{admonition} Definition
Gegeben eine Menge $\Omega$ mit einem Wahrscheinlichkeitsmaß $P_\Omega$,
heißt eine Abbildung $X \colon \Omega \to \mathcal{X}$ in eine Menge $\mathcal{X}$
**Zufallsvariable**, wenn für jedes Ereignis $A \subseteq \mathcal{X}$ auch $X^{-1}(A) \subseteq \Omega$ ein Ereignis ist.
:::

Zur Erinnerung: Wenn $\Omega$ und $\mathcal{X}$ endliche Mengen sind, dann nennen wir jede Teilmenge Ereignis. Dann ist auch jede solche Abbildung eine Zufallsvariable.
Wir werden später sehen: der Begriff Zufallsvariable wird genau dann genutzt, wenn wir an Erwartungswerten oder höheren Momenten interessiert sind.

### Wo kommt der Zufall her?

Bevor wir weiterrechnen, eine Frage, die selten gestellt und noch seltener beantwortet wird: Woher kommt in einem Datensatz eigentlich der Zufall? Die kurze Antwort lautet: Er kommt nicht vor. Er ist eine Entscheidung von uns.

Eine Messung, die schon stattgefunden hat, ist nicht zufällig — der Würfel liegt, die Temperatur wurde abgelesen, die Zeile steht in der Datei. Auch die Erhebung selbst ist ein deterministischer Vorgang: Ein Sensor schreibt auf, was er misst. Zufall ist nichts, was wir in den Daten *finden*; er ist die Sprache, in der wir über das reden, was wir an den Daten nicht wissen oder nicht wissen wollen. Wir behandeln die beobachteten Häufigkeiten so, als wären sie Wahrscheinlichkeiten, und ziehen aus diesem Modell Schlüsse — der Zufall ist also ein Modellierungswerkzeug, kein Naturstoff.

An drei Stellen begegnet er uns trotzdem ganz konkret:

- **Bei der Auswahl.** Wenn wir aus vorhandenen Daten eine Teilmenge ziehen — eine Stichprobe, ein Mini-Batch, eine Aufteilung in Trainings- und Testdaten —, dann ist der Zufall der unsere. Wir ziehen absichtlich zufällig, damit die Auswahl keine Struktur mitbringt, die wir hinterher für ein Ergebnis halten.
- **Beim Sampling aus einem Modell.** Aus einer Modellverteilung zu ziehen, erzeugt synthetische Daten. Auch dieser Zufall ist unserer.
- **Im Rechner gar nicht.** Beides läuft auf einem deterministischen Gerät, das nur *Pseudozufall* erzeugt: eine Zahlenfolge, die zufällig aussieht, aber vollständig durch ihren Startwert (den *Seed*) bestimmt ist. Das ist kein Mangel, sondern der Grund, warum Auswertungen reproduzierbar sind (siehe [Stochastik programmieren](stochastik-programmieren.ipynb)).

Der Weg, den die Daten dabei nehmen, lässt sich in drei Bildern erzählen. Zuerst die Erhebung: Aus der Welt wird ein Ausschnitt gewählt, über den Rohdaten anfallen, und aus den Rohdaten werden durch Bereinigung die Daten, mit denen man arbeitet.

```{figure} images/dsprozess-simplified-1.png
:width: 480px
:align: center
:name: ds-prozess-erhebung

Erhebung: von der Welt über einen Ausschnitt und Rohdaten zu den Daten.
```

Dann die Modellierung. Aus den Daten wird ein Modell gebildet, und aus dem Modell lassen sich wieder Daten erzeugen — synthetische. Ob das Modell taugt, entscheidet sich daran, ob seine synthetischen Daten den echten ähneln.

```{figure} images/dsprozess-simplified-2.png
:width: 480px
:align: center
:name: ds-prozess-modell

Modellierung: von den Daten zum Modell und zurück zu synthetischen Daten.
```

Und schließlich der Weg zur Zielgröße, um die es eigentlich geht: Die Daten werden transformiert, und aus den transformierten Daten wird die eine Zahl berechnet, die wir wissen wollten.

```{figure} images/dsprozess-simplified-3.png
:width: 480px
:align: center
:name: ds-prozess-zielgroesse

Auswertung: von den Daten über transformierte Daten zur Zielgröße.
```

:::{admonition} Beispiel
**Ein Würfelwurf, ganz ausbuchstabiert.** Der *Weltausschnitt* ist ein Würfel auf einem Tisch. Als *Rohdaten* nehmen wir an, eine Kamera liefere für jeden Zeitpunkt die 3D-Koordinaten der acht Ecken, also $8 \cdot 3$ Zahlen je Bild. Nach dem Aussortieren unbrauchbarer Bilder sind das die *Daten*. Daraus rechnen wir *transformierte Daten*: Mittelpunkt und Rotationswinkel des Würfels, also $3 + 3$ Zahlen, denn mehr braucht man nicht, um die Lage eines Würfels zu beschreiben. Erst am Ende steht die *Zielgröße*, die uns tatsächlich interessiert: die Augenzahl oben, eine Zahl in $\{1,\dots,6\}$.

Der ganze Weg von der Welt zur Zielgröße ist genau das, was wir eine Zufallsvariable nennen: eine Abbildung $X \colon \Omega \to \{1,\dots,6\}$, wobei $\Omega$ die möglichen Weltzustände sind. Nichts an dieser Abbildung ist zufällig — sie ist eine lange, aber eindeutige Rechenvorschrift. Der Zufall steckt allein darin, dass wir nicht wissen, welches $\omega \in \Omega$ vorliegt, und deshalb $\Omega$ mit einem Wahrscheinlichkeitsmaß versehen. Die Aussage "der Würfel ist fair" heißt dann

$$
P(X = 6) := P_\Omega\left( \{ \omega \in \Omega : X(\omega) = 6 \} \right) = P_\Omega\left( X^{-1}(\{6\}) \right) = \dfrac{1}{6}.
$$

Die Schreibweise $P(X = 6)$ ist also eine Abkürzung: Gemeint ist die Wahrscheinlichkeit der Menge aller Weltzustände, in denen der Würfel am Ende eine Sechs zeigt. Genau diese Konstruktion — ein Maß auf $\Omega$ wird über $X$ zu einem Maß auf den Werten von $X$ — ist der Inhalt des nächsten Abschnitts.
:::

### Induziertes Wahrscheinlichkeitsmaß

:::{admonition} Definition
Gegeben eine Zufallsvariable $X \colon \Omega \to \mathcal{X}$
heißt das Wahrscheinlichkeitsmaß auf $\mathcal{X}$, das durch

$$P_X \colon A \mapsto P_\Omega\left( X^{-1}(A) \right)$$

gegeben ist, die **Verteilung von $X$**.
:::

:::{admonition} Proposition
Das ist tatsächlich immer ein Wahrscheinlichkeitsmaß.
:::

:::{admonition} Beweis
Wir prüfen die Axiome:
1. Es ist $X^{-1}(\mathcal{X}) = \Omega$, daher ist $P_X(\mathcal{X}) = P_\Omega\left( X^{-1}(\mathcal{X}) \right) = P_\Omega(\Omega) = 1$.
2. Seien $A_1,\dots$ eine Folge von paarweise disjunkten Ereignissen in $\mathcal{X}$, dann ist

$$X^{-1}\left(\bigcup_{i \geq 1} A_i\right) = \left\{\omega \in \Omega\ \mid\ X(\omega) \in A_i \text{ für ein } i \right\} = \bigcup_{i \geq 1} X^{-1}(A_i)$$

und damit 

$$P_X\left(\bigcup_{i\geq 1} A_i\right) = P_\Omega\left( X^{-1} \left(\bigcup_{i \geq 1} A_i\right) \right) = P_\Omega\left( \bigcup_{i \geq 1} X^{-1}(A_i) \right) $$

$$ = \sum_{i \geq 1} P_\Omega \left( X^{-1} A_i \right) = \sum_{i \geq 1} P_X(A_i).$$

:::

:::{admonition} Beispiel
In einem Raum spielen $30$ Kinder. Davon haben $10$ einen blauen Pulli an,
$10$ einen roten, $5$ einen gelben und weitere $5$ einen schwarzen Pulli an.
Wir modellieren $\Omega =$ Menge der Kinder, $X \colon \Omega \to \{r,g,b,s\}$ die Abbildung,
die jedes Kind auf den Anfangsbuchstaben der Pullifarbe abbildet.
Die Verteilung von $X$ ist nun definiert, es ist ein Wahrscheinlichkeitsmaß auf der Menge $\{r,g,b,s\}$.
Wir können beispielhaft berechnen:

$$P_X\left(\{b,r\}\right) = P_\Omega\left(X^{-1} \left(\{b,r\}\right) \right) = \frac{20}{30}$$

wobei wir implizit angenommen haben, dass wir die Kinder alle gleich behandeln,
also gleichverteilt ein Kind herausgreifen, dessen Pullifarbe wir betrachten,
wenn wir ein Ergebnis von $X$ betrachten.
:::

:::{admonition} Beispiel
**Verketten liefert neue Zufallsvariablen.** Sei $X$ der Wurf eines fairen Würfels, also $\Omega = \{1,\dots,6\}$ mit der Gleichverteilung und $X$ die Identität.

*(a)* Sei $g \colon \{1,\dots,6\} \to \{\text{gerade}, \text{ungerade}\}$ die Abbildung, die einer Augenzahl ihre Parität zuordnet. Dann ist

$$
P_g(\{\text{gerade}\}) = P_\Omega\left( g^{-1}(\{\text{gerade}\}) \right) = P_\Omega(\{2,4,6\}) = \dfrac{3}{6} = \dfrac{1}{2}.
$$

Dabei ist $g \circ X$ selbst wieder eine Zufallsvariable — die Verkettung einer Zufallsvariable mit einer Abbildung ist immer eine —, und ihre Verteilung ist $P_{g(X)} = P_g$. Man schreibt dafür kurz $g(X)$ und sagt „die Zufallsvariable *Parität des Wurfs*“.

*(b)* Sei $f$ die Abbildung, die angibt, ob die Augenzahl mindestens $5$ beträgt. Für die Antwort „nein“ zerlegen wir das Urbild in Elementarereignisse und benutzen die $\sigma$-Additivität:

$$
P_f(\{\text{nein}\}) = P_\Omega\left( \{1,2,3,4\} \right) = \sum_{i=1}^4 P_\Omega\left( \{i\} \right) = 4 \cdot \dfrac{1}{6} = \dfrac{2}{3}.
$$

Das ist der Normalfall beim Rechnen mit induzierten Maßen: Man sucht das Urbild, zerlegt es in disjunkte Stücke und addiert.

*(c)* Verkettet man mit $x \mapsto 2x$, so erhält man die Zufallsvariable $2X$ mit Werten in $\{2,4,6,8,10,12\}$, jeder mit Wahrscheinlichkeit $\frac16$. Mit Zufallsvariablen lässt sich also rechnen wie mit Zahlen — man darf sie verdoppeln, addieren, quadrieren —, und die Verteilung ändert sich dabei mit. Wie sich dabei Erwartungswert und Varianz verhalten, klärt das Kapitel [Erwartungswert und Varianz](erwartungswert.md) (Linearität des Erwartungswerts).
:::

Wenn uns nur die Verteilung $P_X$ interessiert, können wir $\Omega$ ignorieren,
denn die selbe Verteilung lässt sich auch mit anderen Mengen $\Omega$ erreichen,
auch mit Verteilungen, die keine Gleichverteilung sind.

## Wahrscheinlichkeitsmassefunktion

Im Alltag rechnet man mit Wahrscheinlichkeiten meist nicht über das Maß $P$ auf Ereignissen, sondern über eine Funktion $p(x)$, die jedem möglichen Wert $x$ direkt seine Wahrscheinlichkeit zuordnet. Im diskreten Fall, um den es in diesem Kapitel geht, heißt diese Funktion *Wahrscheinlichkeitsmassefunktion*; das stetige Gegenstück, die Dichte, lernen wir in einem späteren Kapitel kennen:

:::{admonition} Definition
Eine Funktion $p \colon \Omega \to [0,1]$ heißt *Wahrscheinlichkeitsmassefunktion* (*pmf*, probability mass function) einer Verteilung $P$ auf $\Omega$,
wenn für alle $\omega \in \Omega$ gilt: $p(\omega) = P(\{\omega\})$.
:::

:::{admonition} Beispiel
Im vorigen Beispiel haben wir $P_X(\{r\}) = \frac{10}{30}$, $P_X(\{g\}) = \frac{5}{30}$, $P_X(\{b\}) = \frac{10}{30}$, $P_X(\{s\}) = \frac{5}{30}$ und daher ist

$$p(r):=\frac{10}{30},\ p(g):=\frac{5}{30},\ p(b):=\frac{10}{30},\ p(s):=\frac{5}{30}$$

die Definition einer pmf für $P_X$. Man sagt auch, $p$ ist die pmf von $X$.
Ein anderer gebräuchlicher Name für die pmf ist *Zähldichte*.

Die pmf der Gleichverteilung auf $\Omega$ ist $p(\omega) = \frac{1}{|\Omega|}$.

Die pmf der Dirac-Verteilung mit Masse an einem festen $\xi \in \Omega$ (siehe [Formalismus der Stochastik](intro-stochastik.md)) ist

$$
p(\omega) = \begin{cases} 1 & \omega = \xi,\\ 0 & \text{sonst.} \end{cases}
$$

Beides setzt voraus, dass $\Omega$ höchstens abzählbar ist — für überabzählbares $\Omega$ ist jede einzelne Wahrscheinlichkeit $P(\{\omega\})$ typischerweise $0$, und an die Stelle der pmf tritt die Dichte.
:::

:::{admonition} Beispiel
Wir erwarten eine eingehende Nachricht der Länge $3$ Zeichen. Diese drei Zeichen modellieren wir als Zufallsvariablen X,Y und Z.
Wir wissen vorab, dass jedes Zeichen nur aus einem endlichen Zeichenvorrat kommen kann.
Für jede Zufallsvariable bezeichnen wir diesen Wertebereich jeweils mit $\mathcal{X},\mathcal{Y}$ und $\mathcal{Z}$.
Wir notieren die pmf jeweils mit $p(x),\ p(y),\ p(z)$ mit $x \in \mathcal{X}, y \in \mathcal{Y}$ und $z \in \mathcal{Z}$.

Wir können auch die ganze Nachricht als eine einzige Zufallsvariable auffassen: XYZ.
Dabei kann es nun passieren, dass gewisse Buchstabenfolgen wahrscheinlicher sind, als ihre Bestandteile.
Wenn $X=s$ und $Y=o$ sind, dann ist $Z=s$ sicher wahrscheinlicher, als wenn wir beliebige Werte für $X$ und $Y$ haben.
Insgesamt ist $XYZ=sos$ wahrscheinlicher als das Produkt der Ereignisse $X=s$, $Y=o$, $Z=s$.
Wenn wir, wie üblich, die pmf von $XYZ$ mit $p(x,y,z)$ notieren, so heißt das:

$$p(x,y,z) \neq p(x)p(y)p(z)$$

und wir sagen dazu auch: die Zufallsvariablen bzw. ihre Verteilungen sind nicht unabhängig.
:::

### Induziertes Wahrscheinlichkeitsmaß

:::{admonition} Proposition
Wenn $X \colon \Omega \to \mathcal{X}$ eine Zufallsvariable ist und $P_\Omega$ eine pmf $p_\Omega \colon \Omega \to [0,1]$ hat,
so ist $p_X(x) := \sum_{\omega \in X^{-1}\left(\{ x \}\right)} p_\Omega(\omega)$
eine pmf von $X$.
:::

## Wahrscheinlichkeitsvektor

:::{admonition} Beispiel
Wenn wir die Kinderpullifarben in eine Reihenfolge bringen,
also z.B. $r \mapsto 1,\ g \mapsto 2,\ b\mapsto 3,\ s \mapsto 4$,
dann haben wir damit eine Abbildung $c \colon \mathcal{X} = \{r,g,b,s\} \to \mathcal{C} = \{1,2,3,4\}$ definiert.
Die pmf der Zufallsvariable $c$ bzw. $c \circ X$ ist gegeben durch $p(i)$ für $i \in \mathcal{C}$.
Diese Information lässt sich auch als Vektor auffassen.
:::

:::{admonition} Proposition
Auf einer angeordneten endlichen Menge $\Omega = \{\omega_1, \dots, \omega_n\}$ ist ein Wahrscheinlichkeitsmaß
bereits durch den Vektor $p \in \mathbb{R}^n$ mit $p_i := p(\omega_i)$ eindeutig bestimmt.
:::

:::{admonition} Proposition
Sei $\Delta_n := \left\{p \in \mathbb{R}^n \ \mid\ 0 \leq p_i \leq 1 \text{ für alle } i=1,\dots,n,\ \text{ und } \sum_{i=1}^n p_i = 1 \right\}$
und $\Omega = \{\omega_1, \dots, \omega_n\}$ beliebig. 
Dann definiert jedes $p \in \Delta_n$ eine Wahrscheinlichkeitsverteilung auf $\Omega$.
:::

:::{admonition} Beispiel
Die Gleichverteilung entspricht $p \in \Delta_n$ mit $p_i = \frac{1}{n}$, das ist der geometrische Mittelpunkt von $\Delta_n$.

Die Dirac-Verteilung mit Masse an $\xi \in \Omega$ entspricht $p \in \Delta_n$ mit $p_i = 1$ falls $\omega_i = \xi$ und $p_i=0$ sonst.
Geometrisch ist das ein Eckpunkt von $\Delta_n$ (davon gibt es $n$ Stück).
:::

:::{admonition} Definition
Der Fall $n = 2$ hat einen eigenen Namen. Auf $\Omega = \{0,1\}$ ist ein Wahrscheinlichkeitsvektor durch eine einzige Zahl festgelegt, denn aus $p_0 + p_1 = 1$ folgt $p_0 = 1 - p_1$. Schreibt man $\pi := p_1$, so heißt die zugehörige Verteilung die **Bernoulli-Verteilung zum Parameter $\pi$**, und man notiert $X \sim \operatorname{Ber}(\pi)$ für eine Zufallsvariable mit dieser Verteilung. (Im Kapitel [Wichtigste diskrete Verteilungen](wichtigste-diskrete-verteilungen.ipynb) und in der Literatur heißt dieser Parameter meist $p$; hier schreiben wir $\pi$, weil $p$ in diesem Abschnitt schon der Wahrscheinlichkeitsvektor ist.)
:::

:::{admonition} Beispiel
Ein Münzwurf ist $\operatorname{Ber}(\pi)$ mit $\pi$ der Wahrscheinlichkeit für „Kopf“; jedes Ja/Nein-Merkmal in einem Datensatz („überlebt“, „geklickt“, „Nebenwirkung aufgetreten“) lässt sich so modellieren. Die beiden Sonderfälle von oben tauchen wieder auf: $\pi = \frac12$ ist die Gleichverteilung, $\pi = 0$ und $\pi = 1$ sind die beiden Dirac-Verteilungen.
:::

Geometrisch ist $\Delta_2$ eine Strecke: die Verbindung der beiden Eckpunkte $(1,0)$ und $(0,1)$, und $\pi$ sagt, wo auf dieser Strecke man sich befindet. Eine Bernoulli-Verteilung zu wählen heißt also, einen Punkt auf einer Strecke zu wählen.

Eine so gegebene Verteilung heißt auch *kategoriale Verteilung*; wir treffen sie im Kapitel
[Wichtigste diskrete Verteilungen](wichtigste-diskrete-verteilungen.ipynb) wieder, wo wir auch
ihren Erwartungswert und ihre Varianz ausrechnen.

Es ist also $\Delta_n$ der Raum aller möglichen Wahrscheinlichkeitsverteilungen auf einer $n$-elementigen Menge. Die niedrigen Fälle kann man sich gut vorstellen: $\Delta_2$ ist eine Strecke, $\Delta_3$ ein gefülltes Dreieck (zweidimensional, aber in $\mathbb{R}^3$ eingebettet), $\Delta_4$ ein gefülltes Tetraeder. Allgemein ist $\Delta_n$ ein $(n-1)$-dimensionales Objekt mit $n$ Ecken, das man einen **Simplex** nennt. Eine Dimension geht dabei immer verloren, weil sich die Einträge zu $1$ addieren müssen — genau das haben wir bei der Bernoulli-Verteilung ausgenutzt, als aus zwei Zahlen eine wurde.

:::{admonition} Bemerkung
Genau dieser Simplex $\Delta_n$ ist der Bildbereich der *Softmax*-Funktion, mit der neuronale Netze Klassenwahrscheinlichkeiten ausgeben: Aus $n$ beliebigen reellen Zahlen macht sie einen Vektor in $\Delta_n$. Die Vorlesung *Einführung in Deep Learning* baut darauf auf, dass Sie $\Delta_n$ als Raum der Verteilungen auf $n$ Werten kennen.
:::

:::{admonition} Beispiel
Wenn wir auf einer endlichen Menge $\Omega$ durch den Vektor $p \in \Delta_n$ eine Verteilung gegeben haben,
können wir ein Ereignis $A \subseteq \Omega$ ebenfalls durch einen Vektor charakterisieren,
die Bitmaske $\chi(A) \in \{0,1\}^n$ gegeben durch $\chi(A)_i = 1$ wenn $\omega_i \in A$, sonst $\chi(A)_i = 0$.
Die Wahrscheinlichkeit $P(A)$ ist dann gegeben als

$$P(A) = \sum_{i=1, \omega_i \in A}^n p(\omega_i) = \sum_{i=1}^n p(\omega_i) \chi(A)_i = p \cdot \chi(A).$$

:::

## Von Daten zu Modellen

Die einfachste Form, in der uns Daten vorliegen können, ist eine einzelne Zahl oder eine Folge von $N$ Zahlen. Das nennen wir gern einen $N$-dimensionalen Vektor oder wir stellen uns die Spalte einer Tabelle vor.
In der Statistik spricht man von einer Stichprobe der Größe $N$. Wir werden später auch noch mit Tabellen zu tun haben, die mehr als eine Spalte enthalten, sodass die Daten in Form von komplizierteren Zeilen vorliegen, aber zunächst wollen wir im einfacheren eindimensionalen Setting bleiben.

Schon eine einzelne solche Spalte trägt eine Wahrscheinlichkeitsverteilung mit sich, ganz ohne Modellannahme: Wir zählen einfach, wie häufig jeder Wert vorkommt.

:::{admonition} Definition
Sei $D = (x_1,\dots,x_N)$ ein Datensatz mit Werten in einer endlichen Menge $\Omega$. Dann ist durch

$$
P(\{x\}) := \dfrac{\left| \{ i : x_i = x \} \right|}{N},
$$

also durch die relative Häufigkeit des Wertes $x$ in $D$, ein Wahrscheinlichkeitsmaß auf $\Omega$ gegeben. Wir nennen es die **Verteilung der Daten** (auch *empirische Verteilung*).
:::

Dass das wirklich ein Wahrscheinlichkeitsmaß ist, ist genau die Aussage, dass sich die relativen Häufigkeiten zu $1$ addieren.

:::{admonition} Beispiel
Ein Datensatz mit einer einzigen Spalte $x$, die eine Farbe enthält:

| $i$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $x_i$ | blue | red | blue | green |

Hier ist $\Omega = \{\text{blue}, \text{red}, \text{green}\}$ und $N = 4$. Die Verteilung der Daten ist $P(\{\text{blue}\}) = \frac{2}{4}$, $P(\{\text{red}\}) = \frac{1}{4}$ und $P(\{\text{green}\}) = \frac{1}{4}$, als Wahrscheinlichkeitsvektor geschrieben also $p = \left(\frac{1}{2}, \frac{1}{4}, \frac{1}{4}\right)$.
:::

Wenn die Werte als Zahlen $0, 1, 2, \dots$ codiert sind, bekommt man diesen Vektor in einer Zeile: `np.bincount(daten) / len(daten)` (siehe [Numpy](numpy.ipynb), Abschnitt *Wahrscheinlichkeitsvektoren*).

Das folgende Beispiel ist der Spezialfall $\Omega = \{0,1\}$, in dem eine einzige Zahl die ganze Verteilung festlegt.

:::{admonition} Beispiel
Gegeben eine Stichprobe von $N$ Münzwürfen $(x_1,\dots,x_N) \in \{0,1\}^N$ können wir die Frage stellen:
'Welche Erfolgswahrscheinlichkeit $\pi$ lag der Münze zugrunde?'

Eine mögliche Schätzung wäre $\frac{1}{2}$, ohne die Daten zu betrachten.

Wenn wir die Stichprobe betrachten, können wir $e := \sum_{i=1}^n x_i$, die Anzahl der Erfolge, berechnen.
Dann ist $N-e$ die Anzahl der Misserfolge und $\hat{\pi} := \frac{e}{N}$ eine Schätzung für die Erfolgswahrscheinlichkeit $\pi$,
wenn wir davon ausgehen, dass immer die selbe Münze geworfen wurde.

In der Sprache von oben: Jeder einzelne Wurf ist $\operatorname{Ber}(\pi)$-verteilt, und $\hat{\pi}$ ist eine Schätzung für den Parameter dieser Verteilung — wir suchen also einen Punkt auf der Strecke $\Delta_2$.
:::

Damit haben wir schon alle Rollen der Statistik besetzt, auch wenn wir die Wörter erst später brauchen: Die Münze, die man beliebig oft werfen könnte, ist die **Population**, die $N$ Würfe sind eine **Stichprobe** daraus, und $\hat{\pi}$ ist eine Aussage über die Population, die man aus der Stichprobe gewonnen hat. Genauso ist eine Tüte Süßigkeiten die Population und eine Handvoll daraus die Stichprobe, aus der man die Farbverteilung in der Tüte schätzt. Was man vor dem Hineingreifen schon weiß oder vermutet (die Münze sieht normal aus, die Tüte ist eine Standardmischung), heißt später **Prior**. Dass der Schluss von der Stichprobe auf die Population nie sicher ist und wie man seine Unsicherheit beziffert, ist Thema der Kapitel [Erwartungswert und Varianz](erwartungswert.md) (Tschebyscheff-Ungleichung) und [Statistische Tests](statistische-tests.md).

Die Verteilung der Daten ist noch kein Modell — sie ist nur eine andere Schreibweise für die Daten selbst. Ein Modell entsteht erst, wenn eine Annahme dazukommt. Nehmen wir an, der Farbdatensatz von oben sei um einen fünften Eintrag gewachsen:

| $i$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $x_i$ | blue | red | blue | green | blue |

Die Verteilung der Daten ist jetzt $\left(\frac{3}{5},\frac{1}{5},\frac{1}{5}\right)$. Wenn wir aber annehmen, dass die Farben gleich häufig sind bis auf eine, die doppelt so oft vorkommt, dann wählen wir als Modell die Verteilung $p = \left(\frac{1}{2},\frac{1}{4},\frac{1}{4}\right)$ — obwohl die beobachteten relativen Häufigkeiten andere sind. Eine so gewählte Verteilung heißt **Modellverteilung**. Sie hat in aller Regel weniger Parameter als der Datensatz Einträge, sie ist glatter, und sie macht auch Aussagen über Werte, die in den Daten gar nicht vorkommen.

Ein Modell lässt sich in beide Richtungen benutzen. Aus Daten eine Modellverteilung zu bestimmen, ist das Schätzproblem, mit dem sich das Kapitel [Statistische Modelle und Schätzer](statistische-modelle.md) beschäftigt. Umgekehrt kann man aus einer Modellverteilung ziehen und erhält **synthetische Daten**: einen Datensatz, der aussieht wie ein echter, aber keiner ist. Synthetische Daten sind das Standardwerkzeug, um ein Auswertungsverfahren zu prüfen — denn hier kennt man die richtige Antwort und kann nachsehen, ob das Verfahren sie findet.

:::{admonition} Übung
Ziehen Sie $1000$ synthetische Farbwerte zur Modellverteilung $p = \left(\frac{1}{2},\frac{1}{4},\frac{1}{4}\right)$ und bestimmen Sie die Verteilung der so erzeugten Daten. Wie weit weicht sie von $p$ ab, und wie ändert sich das bei nur $10$ gezogenen Werten? In der Standardbibliothek zieht `random.choices(werte, weights=..., k=1000)`, in Numpy `rng.choice(werte, size=1000, p=...)` (siehe [Stochastik programmieren](stochastik-programmieren.ipynb)).
:::

Damit liegen zwei Verteilungen auf demselben $\Omega$ vor: die der Daten und die des Modells. Die nächste Frage ist die nach der Güte des Modells — sehen die Daten so aus, als wären sie aus dem Modell gezogen worden? Auf Englisch fragt man *how likely is that?*, und die Zahl, die das beantwortet, heißt **Likelihood**: die Wahrscheinlichkeit, genau die beobachteten Daten zu sehen, wenn das Modell stimmt. Ein Modell, das diese Zahl möglichst groß macht, ist nach dem **Maximum-Likelihood-Prinzip** das beste; dieses Prinzip zieht sich durch den Rest des Kurses und bekommt im Kapitel [Statistische Modelle und Schätzer](statistische-modelle.md) einen eigenen Abschnitt. Es ist nicht der einzige Weg, den Unterschied zwischen zwei Verteilungen zu beziffern: Das Kapitel [Erwartungswert und Varianz](erwartungswert.md) misst den Abstand zwischen Daten und synthetischen Daten direkt im Datenraum, und das Kapitel [Relative Entropie](relative-entropie.md) misst ihn zwischen den Verteilungen selbst.

Damit ist der Weg abgesteckt, den der Rest des Kurses geht, und der sich auch in {numref}`ds-prozess-modell` wiederfindet: einen Ausschnitt der Welt wählen, Daten erheben, sie putzen ([Daten putzen](data-cleaning.ipynb)) und in brauchbare Merkmale übersetzen — man sagt **Features** —, daraus Modelle bilden und die Modelle an den Daten messen. Alles Weitere ist die Ausarbeitung dieser fünf Schritte.


Nun werden wir Daten selten in Form von Bitfolgen mit völlig unabhängigen Bits interpretieren.
Zum Beispiel die menschliche Körpergröße, gemessen in Zentimetern, ist eine reelle Zahl größer $0$.
Gegeben eine Meßreihe, also eine Stichprobe der Größe $N$ von Körpergrößen, können wir ein statistisches Modell bilden.
Dabei reden wir hier nicht über Kausalität oder Korrelationen mit anderen Daten, wie z.B. Geschlecht oder Alter.
Trotzdem können wir Modelle bilden, die uns eine gewisse Vorhersage erlauben.
Ein Ansatz ist die zusammenfassende Statistik, die aus der Stichprobe eine einzelne Zahl extrahiert, die uns die Daten verlustbehaftet komprimieren lässt.
Welche Zahl die richtige ist, um Daten zusammenzufassen / zu modellieren, hängt von unserem Ziel ab.
Daher wollen wir uns im Folgenden mit Erwartungswert und Varianz aus einer datenzentrierten Perspektive befassen.
