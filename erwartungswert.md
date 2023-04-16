# Erwartungswert und Varianz

## Abweichung quantifizieren

Gegeben zwei Vektoren $x,y \in \mathbb{R}^n$ (wir stellen uns vor: $x$ sind unsere Daten, $y$ das, was wir erwarten),
ist die mittlere Abweichung interessant: $\sum \frac{x_i - y_i}{n}$.
Ein Problem dieser Größe ist, dass sich positive mit negativen Abweichungen herauskürzen.

### Absolute Abweichung

:::{admonition} Definition
Die *mittlere absolute Abweichung* (mean absolute error) ist
$\texttt{mae}(v,w) := \sum_{i=1}^n \dfrac{\left| v_i - w_i \right|}{n}$.

Für eine Zahl $c \in \mathbb{R}$ schreiben wir auch $\texttt{mae}(v,c):=\texttt{mae}(v,(c)_{i=1}^n)$.
:::

:::{admonition} Beispiel
Wenn $v = (1,2,3,4)$ und $c=2$, so ist $\texttt{mae}(v,c) = \sum_{i=1}^4 \dfrac{|i-2|}{4} = \dfrac{4}{4} = 1$.
:::

Es ist natürlich sofort für einen Vektor $v$ interessant, welcher Vektor $w$ die geringste mittlere absolute Abweichung hat. Wenn man an $w$ jedoch keine weiteren Bedingungen stellt, ist mit $w=v$ das Minimum schnell gefunden. Wir werden dieser Frage später wieder begegnen und begnügen uns jetzt damit, zu fragen, welches $c \in \mathbb{R}$ den Ausdruck $\texttt{mae}(v,c)$ minimiert. Graphisch können wir uns vorstellen, als $x$-Achse die Zahlen von $1$ bis $n$ zu verwenden, und dort jeweils die Werte $v_i$ aufzutragen. Dann entspricht die Wahl eines $c \in \mathbb{R}$ einer horizontalen Gerade, und wir fragen uns, welche solche Gerade den geringsten gemeinsamen Abstand zu allen Punkten hat.

:::{admonition} Definition
$\texttt{median}(v) := \min_{c \in \mathbb{R}} \texttt{mae}(v,c)$ ist \`\`der'' *Median* von $v$.
:::

Diese Definition mag ungewohnt sein, aber sie erfüllt die folgende Eigenschaft:

:::{admonition} Proposition
Wenn $v \in \mathbb{R}^n$ sortiert ist, also $v_i < v_j$ für $ < j$, dann ist mit $v' := (v_2,\dots,v_{n-1}) \in \mathbb{R}^n$ ein neuer (kürzerer) Vektor definiert, sodass für alle $c \in \mathbb{R}$ mit $v_1 \leq c \leq v_n$ gilt:

$\texttt{mae}(v,c) = \texttt{mae}(v',c) + \dfrac{v_n - v_1}{n}$.
:::

Da der zweite Summand nicht von $c$ abhängt, ist er für die Bestimmung des Minimums unerheblich.
Durch induktive Anwendung dieser Erkenntnis bleibt uns nur noch, $\texttt{mae}(v,c)$ für Vektoren der Länge $1$ und $2$ zu bestimmen.
Es ist $\texttt{mae}((v_1),c) = |v_1 - c|$, was für $c = v_1$ minimal wird,
und $\texttt{mae}((v_1,v_2),c) = \frac{v_2 - v_1}{2}$, was für jedes $c$ zwischen $v_1$ und $v_2$ minimal wird. Also hängt der Median (einer sortierten Liste) nur vom mittleren / von den zwei mittleren Werten ab. Man definiert meist den Median so, dass in diesem Fall die Wahl $\texttt{median}((v_1,v_2)) = \dfrac{v_1+v_2}{2}$ getroffen wird (und so wollen wir es im Folgenden auch handhaben).

:::{admonition} Beweis
$$
\texttt{mae}(v,c) &= \phantom{\dfrac{|v_1 - c|}{n} +\ } \sum_{i=1}^{n} \dfrac{|v_i -c |}{n} \\
                  &= \dfrac{|v_1 - c|}{n} + \sum_{i=2}^{n-1} \dfrac{|v_i -c |}{n} + \dfrac{|v_n - c|}{n} \\
                  &= \sum_{i=2}^{n-1} \dfrac{|v_i -c |}{n} + \dfrac{-(v_1 - c) + (v_n - c)}{n} \\
                  &= \texttt{mae}(v',c) + \dfrac{v_n - c + c - v_1}{n}.
$$
:::

Da der Median also relativ schlecht die Daten wiederspiegelt (von den meisten Daten ist er völlig unabhängig!), brauchen wir ein besseres Maß.
*Idee*: wir quadrieren die individuellen Fehlerterme in der Summe, damit große Fehler einen größeren Teil zur Summe beitragen. Praktisch: durch das Quadrieren muss man nicht mehr explizit den Absolutbetrag nehmen (das geschieht automatisch).

### Quadratische Abweichung

:::{admonition} Definition
Für Vektoren $v,w \in \mathbb{R}^n$ ist die *mittlere quadratische Abweichung* (mean squared error) definiert als

$$
\texttt{mse}(v,w) := \sum_{i=1}^n \dfrac{{\left(v_i - w_i\right)}^2}{n}
$$

und für $c \in \mathbb{R}^n$ schreiben wir $\texttt{mse}(v,c) := \texttt{mse}(v, (c)_{i=1}^n)$.
:::

:::{admonition} Proposition
Für einen Vektor $v \in \mathbb{R}^n$ minimiert der (arithmetische) *Mittelwert* von $v$ die mittlere quadratische Abweichung:

$\texttt{mean}(v) := \sum_{i=1}^n \dfrac{v_i}{n} = \min_{c \in \mathbb{R}} \texttt{mse}(v,c)$.
:::

:::{admonition} Beweis
Wir schreiben ein beliebiges $c \in \mathbb{R}$ als $c = \texttt{mean}(v) + \delta$ und zeigen dann, dass $\texttt{mse}(v,c)$ minimal wird für $\delta = 0$.
Dazu faktorisieren wir aus: $(v_i - \texttt{mean}(v) - \delta)^2 = (v_i - \texttt{mean}(v))^2 - 2\delta (v_i - \texttt{mean}(v)) + \delta^2$ und teilen die Summe entsprechend auf:

$$
\texttt{mse}(v,c) &= \texttt{mse}(v,\texttt{mean}(v) + \delta) = \sum_{i=1}^n \dfrac{(v - (\texttt{mean}(v) + \delta))^2}{n} \\
                  &= \dfrac{1}{n} \sum_{i=1}^n \left( {\left(v_i - \texttt{mean}(v)\right)}^2 - 2\delta \left(v_i - \texttt{mean}(v)\right) + \delta^2 \right) \\
                  &= \left( \dfrac{1}{n} \sum_{i=1}^n \left( (v_i - \texttt{mean}(v))^2 \right) \right) - 2\delta \left( \sum_{i=1}^n \frac{v_i}{n} - \texttt{mean}(v) \right) + \delta^2 \\
                  &= \texttt{mse}(v,\texttt{mean}(v)) - 2\delta(\texttt{mean}(v) - \texttt{mean}(v)) + \delta^2 \\
                  &= \texttt{mse}(v,\texttt{mean}(v)) + \delta^2
$$

und dieser Ausdruck wird nur für $\delta=0$ minimal, weil $\delta^2 \geq 0$.
:::


### Sample-Standardabweichung

:::{admonition} Definition
Sei $v \in \mathbb{R}^n$. Die Quadratwurzel der mittleren quadratischen Abweichung (root mean squared error) vom Mittelwert nennen wir $\texttt{rmse}$ (oder auch Sample-Standardabweichung):

$\texttt{rmse}(v) = \sqrt{\texttt{mse}\left( v, \texttt{mean}(v) \right)}$.
:::

:::{admonition} Proposition
Für $v \in \mathbb{R}^n$ mit $\texttt{mean}(v)=0$ (ein *zentriertes* Sample, etwa $v := w - (\texttt{mean}(w))_{i=1}^n$ für ein beliebiges $w \in \mathbb{R}^n$) 
ist $\texttt{rmse}(v)^2 = \texttt{mse}(v,0) = \frac{1}{n} \sum_{i=1}^n v_i^2$ und der Vektor $v' := {\left( \dfrac{v_i}{\texttt{rmse}(v)} \right)}_{i=1}^n$ erfüllt $\texttt{mean}(v')=0$ und $\texttt{rmse}(v')=1$ (ein *normiertes* Sample).
:::

:::{admonition} Beweis
Übungsaufgabe.
:::

### Informationsgehalt

Ob ein Vektor $v \in \mathbb{R}^n$ für uns Informationen enthält, hängt davon ab, wie viel wir über $v$ bereits wissen.
Wenn wir z.B. wissen, dass $v$ ein Sample einer auf $\{0,1\}$ gleichverteilten Zufallsvariablen ist, wird uns nicht überraschen, wenn $v$ auch so aussieht. Jeder Eintrag von $v$ entspricht genau einem Bit Information. Wenn aber die Zufallsvariable nicht gleichverteilt ist, sondern z.B. auf den Zahlen $\{1,\dots, 26\}$ der Verteilungshäufigkeit der Buchstaben in der deutschen Sprache entspricht (mit $1$ für "a", $26$ für "z" usw.), so enthält ein Eintrag von $v$ potentiell weniger Informationen. Das "e" ist so häufig, dass wir wenig überrascht sind, wenn wir eins sehen. Ein "x" hingegen würde uns sehr überraschen, aber das kommt ja auch nicht so oft vor. Der mittlere Informationsgehalt ist also geringer als bei einer Gleichverteilung.




## Momente einer Zufallsvariable

### Erwartungswert, allgemein

:::{admonition} Definition
Sei $X \colon \Omega \to \mathbb{R}$ eine reelle Zufallsvariable, dann ist der *Erwartungswert* definiert als

$\mathbb{E}X := \mathbb{E}(X) := \int_{\Omega} X dP = \int_{\Omega} X(\omega) d P(\omega) \in \mathbb{R}$

also als das Integral der Abbildung $X$ bezüglich des Maßes $P$.
:::

Dieses Integral existiert im Allgemeinen nicht, d.h. es gibt Zufallsvariablen, für die sich kein Erwartungswert bestimmen lässt.

### Erwartungswert, diskret

Wenn $X \colon \Omega \to \mathbb{R}$ eine diskrete reelle Zufallsvariable ist (also $\Omega$ ein diskreter Wahrscheinlichkeitsraum, höchstens abzählbar),
so ist $\mathbb{E}(X) = \sum_{\omega \in \Omega} X(\omega) P({\omega})$ (das Integral vereinfacht sich zu einer Summe).

Wenn man nicht "in $\Omega$" arbeiten möchte, kann man diese Summe auch umstellen und über alle Werte $\{x_i\}_{i\in I}$ summieren:
$\mathbb{E}(X) = \sum_{i \in I} x_i P(X = x_i)$.

:::{admonition} Beispiel
Der Erwartungswert einer Gleichverteilung auf $\Omega = \{1,\dots,n\}$ ist $\sum_{i=1}^n \frac{i}{n}$, also $\frac{n(n+1)}{2n} = \frac{n+1}{2}$.
:::

Es gibt einen inneren Zusammenhang zwischen dem Erwartungswert und den Stichproben einer Zufallsvariable:

:::{admonition} Satz
**Gesetz der großen Zahlen**

Ist eine unendliche Folge $(X_i)_{i \in \mathbb{N}}$ von Zufallsvariablen $\Omega \to \mathbb{R}$ gegeben, so sagt man, dass diese Folge einem *starken Gesetz der großen Zahlen* genügt, wenn die Mittelwert-Zufallsvariablen $\overline{X_n} := \dfrac{1}{n} \sum_{i=1}^n \left( X_i - \mathbb{E}(X_i) \right)$ gegen $0$ konvergieren, und zwar $P$-fast sicher (d.h. $P(\lim_{n\to\infty} \overline{X_n} = 0) = 1$).

Wenn die $X_i$ nun unabhängig und identisch verteilt sind ($X_i = X$ für festes $X$) mit existierendem Erwartungswert $\mathbb{E}(X)$,
dann genügen die $X_i$ einem starken Gesetz der großen Zahlen, d.h.
dann konvergiert $\overline{X_n}$, die Abweichung des arithmetischen Mittels einer Stichprobe von $X$ der Größe $n$ vom Erwartungswert, $P$-fast sicher gegen $0$.
Das bedeutet umgekehrt auch: Die Wahrscheinlichkeit, dass das Stichprobenmittel für beliebig große $n$ vom Erwartungswert abweicht, ist $0$.
:::

Aus der $P$-fast sicheren Konvergenz folgt auch die stochastische Konvergenz:
$\lim_{n\to\infty} P\left(|\overline{X_n}| \geq \epsilon \right) = 0$ für jedes $\epsilon > 0$.

Wir wollen uns im Folgenden nicht mehr über Konvergenzbegriffe der Stochastik den Kopf zerbrechen (das kann man bei Bedarf immer noch nachholen und das lohnt sich auch je nach Anwendung), sondern in gewohnter Tradition das gute Gefühl mitnehmen, dass der Erwartungswert eine geeignete Größe ist, um erwartungsvoll eine Stichprobe zu analysieren. Je größer die Stichprobe, desto geringer dürfte die Abweichung des Stichprobenmittels vom Erwartungswert sein - so will es das Gesetz. Umgekehrt findet man also zu jeder vorgegebenen Schranke $\epsilon > 0$ eine Stichprobengröße $n$ sodass das Stichprobenmittel einer zufällig gezogenen Stichprobe fast immer um weniger als $\epsilon$ vom Erwartungswert abweicht.


:::{admonition} Lemma
**Rechenregeln für den Erwartungswert:**

0 . Der Erwartungswert ist linear in $X$, also für $\alpha,\beta \in \mathbb{R}$ und $X,Y \colon \Omega \to \mathbb{R}$ Zufallsvariable ist

$$
\mathbb{E}\left( \alpha X + \beta Y \right) = \alpha \mathbb{E} X + \beta \mathbb{E}Y.
$$

1. Der Erwartungswert ist monoton in $X$, also für $X \leq Y$ ist $\mathbb{E}X \leq \mathbb{E}Y$.

2. $\sigma$-Additivität: für eine Folge $X_i \geq 0$ ist $\mathbb{E}(\sum_{i \geq 1} X_i) = \sum_{i \geq 1} \mathbb{E}(X_i)$.

3. Produktregel: Sind $X$ und $Y$ unabhängig, so ist $\mathbb{E}(XY) = \mathbb{E}(X)\mathbb{E}(Y)$.

**Ohne Beweis**
:::

Dabei haben wir noch nicht erklärt, was *unabhängig* bedeutet (unabhängig von den pmf im diskreten Fall), und werden das auch erst weiter unten behandeln.




### Varianz

:::{admonition} Definition
Sei $X \colon \Omega \to \mathbb{R}$ eine Zufallsvariable. Dann heißt

$\mathbb{V}X := \mathbb{V}(X) := Var(X) := \mathbb{E}\left( {\left(X - \mathbb{E}X\right)}^2 \right)$ die *Varianz* von $X$.
:::

:::{admonition} Proposition
Es ist $\mathbb{V}(X) = \mathbb{E}\left( X^2 \right) - {\left(\mathbb{E}X\right)}^2$.
:::

:::{admonition} Beweis
Es ist ${\left(X - \mathbb{E}X\right)}^2 = X^2 - 2X\mathbb{E}X + {\left(\mathbb{E}X\right)}^2$ und mit der Linearität des Erwartungswerts also

$$
\mathbb{V}(X) &= \mathbb{E}\left( {\left(X - \mathbb{E}X\right)}^2 \right) \\
              &= \mathbb{E}\left( X^2 \right) - 2\mathbb{E}\left( X \right)\mathbb{E}\left( X \right) + {\left(\mathbb{E}X\right)}^2 \mathbb{E}\left( 1 \right) \\
              &= \mathbb{E}\left( X^2 \right) - {\left(\mathbb{E}X\right)}^2.
$$
:::

Für eine zentrierte Zufallsvariable, d.h. mit $\mathbb{E}(X) = 0$, ist offensichtlich $\mathbb{V}(X) = \mathbb{E}(X^2)$.

:::{admonition} Definition
Man nennt allgemein auch $\mathbb{E}(X^n)$ das $n$-te *Moment* und $\mathbb{E}((X - \mathbb{E}X)^n)$ das $n$-te *zentrale Moment*.
Der Erwartungswert ist also das erste Moment und die Varianz das zweite zentrale Moment.
Das dritte zentrale Moment heißt auch *Schiefe* (skewness) und das fünfte *Wölbung*.
Die Schiefe ist ein Maß dafür, wie symmetrisch die Verteilung um den Erwartungswert ist.
Man nennt $\sigma(X) := \sqrt{\mathbb{V}(X)}$ die *Standardabweichung* von X.
:::

Die Varianz hilft uns bei der Einschätzung, wie wahrscheinlich gewisse Abweichungen vom Erwartungswert sind.

:::{admonition} Satz
**(Tschebyscheff-Ungleichung)**

Für $X$ eine reelle Zufallsvariable, $c \in \mathbb{R}$ ist

$$
P\left( | X - \mathbb{E} X | \geq c \right) \leq \dfrac{\mathbb{V}X}{c^2}.
$$

**ohne Beweis**.
:::

Dabei ist der Spezialfall $c=\sigma$ trivial, weil auf der rechten Seite nur $1$ steht, und jede Wahrscheinlichkeit $\leq 1$ ist.
Der Spezialfall $c = k\sigma$ mit $k \in \mathbb{N}$ vereinfacht sich allerdings zu

$$
P\left( | X - \mathbb{E} X | \geq k\sigma \right) \leq \dfrac{1}{k^2}.
$$

Daran sehen wir: Abweichungen von $2\sigma$ haben eine Wahrscheinlichkeit $\leq \frac{1}{4}$, und Abweichungen von $3\sigma$ bereits nur noch $\leq \frac{1}{9}$. Wenn wir also Abweichungen in Vielfachen von $\sigma$ messen, so ist die Wahrscheinlichkeit für so große Abweichungen näherungsweise umgekehrt quadratisch proportional (so steht's ja oben schon in der Ungleichung). Damit haben wir auch ein Kriterium zur Hand, um in Daten fehlerhafte Datenpunkte auszusortieren - wenn Abweichung größer $k\sigma$ mit $k > 1$ häufiger als erwartet zu sehen sind, dann gehören diese Datenpunkte zumindest nicht zu der Verteilung, die man erwartet.

Wendet man das Gesetz der großen Zahlen auf die Zufallsvariable ${\left(X-\mathbb{E}(X)\right)}^2$ an, so sieht man, dass auch die Standardabweichung gegen die Sample-Standardabweichung konvergiert. Damit ist also die Sample-Standardabweichung ein guter Ersatz, wenn sich die wahre Varianz der Zufallsvariable nicht bestimmen lässt.


### Entropie

:::{admonition} Definition
Bei einem diskreten Wahrscheinlichkeitsraum $\Omega$ nennen wir für $x \in \Omega$ die *Information* von $x$

$$
I(x) := -\log_b(P(\{x\}).
$$

Dabei ist die Basis $b$ des Logarithmus in der Regel $2$, aber letztlich nicht so wichtig.
Für eine Zufallsvariable $X \colon \Omega' \to \Omega$ können wir nun die Verkettung $I \circ X \colon \Omega' \to \mathbb{R}$ betrachten,
eine reelle Zufallsvariable. Ihr Erwartungswert ist die mittlere Information von $X$, wir sagen auch *Entropie*

$$
H(X) := \mathbb{E}\left( I(X) \right) &= \sum_{\omega' \in \Omega'} -\log_b(P(\{X(\omega')\})P(X(\omega')) \\
                                      &= - \sum_{\omega \in \Omega} \log_b(P(\{\omega\}))P(\{\omega\})
$$
:::

:::{admonition} Beispiel
Bei einer Gleichverteilung auf $\Omega = \{1,\dots,n\}$ ist für $x\in\Omega$ stets $P(\{x\}) = \frac{1}{n}$,
also $I(x) = -\log_2(P(\{x\})) = -\log_2\frac{1}{n} = \log_2(n)$ und somit
$H(X) = \sum_{i=1}^n \frac{\log_2(n)}{n} = \log_2(n)$.
Diese Zahl verrät uns, dass wir im Mittel $\log_2(n)$ bits an Information brauchen, um ein Sample der Größe $n$ zu rekonstruieren, wenn wir die Verteilung von $X$ kennen. Es gibt andere Verteilungen, die es erlauben mit im Mittel weniger Information ein Sample zu rekonstruieren. Genau genommen sogar jede, denn die Gleichverteilung hat maximale Entropie unter allen diskreten Verteilungen. Sie korrespondiert dazu, dass wir maximal wenig wissen und daher alle Ergebnisse als gleich wahrscheinlich annehmen.
:::

Am besten versteht man die Entropie als eine relative Größe, und das werden wir später noch tun.


### Unabhängigkeit

:::{admonition} Definition
Sei $\Omega$ ein Wahrscheinlichkeitsraum. Ereignisse $A,B \subseteq \Omega$ heißen *voneinander unabhängig*, wenn

$$
P(A\cap B) = P(A) \cdot P(B).
$$

Allgemeiner heißt eine Familie $(A_i)_{i\in I}$, $A_i \subseteq \Omega$ von Ereignissen *unabhängig*, wenn
für jede endliche Teilindexmenge $J \subseteq I$ gilt:

$$
P\left( \bigcap_{j \in J} A_j \right) = \prod_{j\in J} P(A_j).
$$
:::

Dabei macht es im Allgemeinen einen echten Unterschied, ob eine Familie unabhängig oder nur paarweise unabhängig ist, daher ist die Definition mit Familien wichtig.

:::{admonition} Definition
Sei $\Omega$ ein Wahrscheinlichkeitsraum.
Eine Familie von Zufallsvariablen $(Y_i)_{i \in I}$, $Y_i \colon \Omega \to \Omega_i$ heißt *unabhängig*, wenn
für beliebige Ereignisse $B_i \subseteq \Omega_i$ die Familie $\left( \{Y_i \in B_i\} \right)_{i \in I}$ unabhängig in $\Omega$ ist.
:::

:::{admonition} Beispiel
Für $I = \{1,\dots,n\}$ und $\Omega_i$ jeweils diskret ist $Y_1,\dots,Y_n$ unabhängig genau dann wenn für alle Ergebnisse $\omega_i \in \Omega_i$ gilt:

$$
P(Y_1=\omega_1, \dots, Y_n=\omega_n) = \prod_{i=1}^n P(Y_i = \omega_i).
$$
:::

In diesem Zusammenhang taucht auch sehr oft ein weiterer Begriff auf:

:::{admonition} Definition
Sei $\Omega$ ein Wahrscheinlichkeitsraum. Für Ereignisse $A,B \subseteq \Omega$ heißt

$$
P(A | B) := \dfrac{P(A\cap B)}{P(B)}
$$

die *bedingte Wahrscheinlichkeit* von $A$ bedingt $B$.
:::

Klar: $A$ und $B$ sind unabhängig voneinander genau dann wenn $P(A | B) = P(A)$.
Bedingte Wahrscheinlichkeiten treten also stets dann auf (bzw. sind besonders interessant), wenn zwei Ereignisse (bzw. Zufallsvariablen) nicht unabhängig sind.
