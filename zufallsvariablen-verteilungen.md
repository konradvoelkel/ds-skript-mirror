# Zufallsvariablen und Verteilungen

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
$10$ einen roten, $5$ einen gelben und weitere $5$ einen schwarzeln Pulli an.
Wir modellieren $\Omega =$ Menge der Kinder, $X \colon \Omega \to \{r,g,b,s\}$ die Abbildung,
die jedes Kind auf den Anfangsbuchstaben der Pullifarbe abbildet.
Die Verteilung von $X$ ist nun definiert, es ist ein Wahrscheinlichkeitsmaß auf der Menge $\{r,g,b,s\}$.
Wir können beispielhaft berechnen:

$$P_X\left(\{b,r\}\right) = P_\Omega\left(X^{-1} \left(\{b,r\}\right) \right) = \frac{20}{30}$$

wobei wir implizit angenommen haben, dass wir die Kinder alle gleich behandeln,
also gleichverteilt ein Kind herausgreifen, dessen Pullifarbe wir betrachten,
wenn wir ein Ergebnis von $X$ betrachten.

Wenn uns nur die Verteilung $P_X$ interessiert, können wir $\Omega$ ignorieren,
denn die selbe Verteilung lässt sich auch mit anderen Mengen $\Omega$ erreichen,
auch mit Verteilungen, die keine Gleichverteilung sind.
:::

## Wahrscheinlichkeitsmassefunktion

Die typische Art, im Alltag mit Wahrscheinlichkeiten umzugehen, ist die der Wahrscheinlichkeitsdichtefunktion, oft mit $p(x)$ im Kontrast zu $P$ bezeichnet.
Für diskrete Verteilungen wird diese allerdings als Wahrscheinlichkeitsmassefunktion bezeichnet, ebenfalls mit der Notation $p(x)$:

:::{admonition} Definition
Eine Funktion $p \colon \Omega \to [0,1]$ heißt *Wahrscheinlichkeitsmassefunktion* (*pmf*, probability mass function) einer Verteilung $P$ auf $\Omega$,
wenn für alle $\omega \in \Omega$ gilt: $p(\omega) = P(\{\omega\})$.
:::

:::{admonition} Beispiel
Im vorigen Beispiel haben wir $P_X(\{r\}) = \frac{10}{30}$, $P_X(\{g\}) = \frac{5}{30}$, $P_X(\{b\}) = \frac{10}{30}$, $P_X(\{s\}) = \frac{5}{30}$ und daher ist

$$p(r):=\frac{10}{30},\ p(g):=\frac{5}{30},\ p(b):=\frac{10}{30},\ p(s):=\frac{5}{30}$$

die Definition einer pmf für $P_X$. Man sagt auch, $p$ ist die pmf von $X$.

Die pmf der Gleichverteilung auf $\Omega$ ist $p(\omega) = \frac{1}{|\Omega|}$.
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

Es ist also $\Delta_n$ der Raum aller möglichen Wahrscheinlichkeitsverteilungen auf einer $n$-elementigen Menge. Für $n=3$ kann man sich das zweidimensionale gefüllte Dreieck $\Delta_3 \subset \mathbb{R}^3$ noch gut vorstellen.

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

:::{admonition} Beispiel
Gegeben eine Stichprobe von $N$ Münzwürfen $(x_1,\dots,x_N) \in \{0,1\}^N$ können wir die Frage stellen:
'Welche Erfolgswahrscheinlichkeit $\pi$ lag der Münze zugrunde?'

Eine mögliche Schätzung wäre $\frac{1}{2}$, ohne die Daten zu betrachten.

Wenn wir die Stichprobe betrachten, können wir $e := \sum_{i=1}^n x_i$, die Anzahl der Erfolge, berechnen.
Dann ist $N-e$ die Anzahl der Misserfolge und $\hat{\pi} := \frac{e}{N}$ eine Schätzung für die Erfolgswahrscheinlichkeit $\pi$,
wenn wir davon ausgehen, dass immer die selbe Münze geworfen wurde.
:::


Nun werden wir Daten selten in Form von Bitfolgen mit völlig unabhängigen Bits interpretieren.
Zum Beispiel die menschliche Körpergröße, gemessen in Zentimetern, ist eine relle Zahl größer $0$.
Gegeben eine Meßreihe, also eine Stichprobe der Größe $N$ von Körpergrößen, können wir ein statistisches Modell bilden.
Dabei reden wir hier nicht über Kausalität oder Korrelationen mit anderen Daten, wie z.B. Geschlecht oder Alter.
Trotzdem können wir Modelle bilden, die uns eine gewisse Vorhersage erlauben.
Ein Ansatz ist die zusammenfassende Statistik, die aus der Stichprobe eine einzelne Zahl extrahiert, die uns die Daten verlustbehaftet komprimieren lässt.
Welche Zahl die richtige ist, um Daten zusammenzufassen / zu modellieren, hängt von unserem Ziel ab.
Daher wollen wir uns im Folgenden mit Erwartungswert und Varianz aus einer datenzentrierten Perspektive befassen.
