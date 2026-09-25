# Erwartungswert und Varianz

[Vorlesungsaufzeichnung Erwartungswert und Varianz](https://media.hhu.de/channel/video/data-science-vl-3-erwartungswert-varianz-2025/a9c845841d79aa3c9d893280bbf7b5a7/167)
[Vorlesungsaufzeichnung Unabhängigkeit und Gesetz der großen Zahlen](https://media.hhu.de/channel/video/data-science-vl-4-grosse-zahlen-2025/83a373228e9c6999642f74ab85762b27/167) 

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

Die Summe ohne den Faktor $\frac1n$ ist die $1$-Norm der Differenz,

$$
d_1(v,w) := \sum_{i=1}^n \left| v_i - w_i \right| = \left\| v - w \right\|_1 = n \cdot \texttt{mae}(v,w),
$$

und der Faktor $\frac1n$ in der Definition ist genau das, was $\texttt{mae}$ von der Länge des Vektors unabhängig macht: $d_1$ wächst mit $n$, auch wenn das Modell gleich gut bleibt, $\texttt{mae}$ nicht. Vergleichen will man fast immer, also nimmt man fast immer den Mittelwert. (Zur Rolle der verschiedenen Normen siehe auch die Bemerkung zu $L_0$, $L_1$ und $L_2$ im Kapitel [Deskriptive Statistik](deskriptive-statistik.md) sowie die L1- und L2-Regularisierung im Kapitel [Regressionsanalyse](lineare-regression.ipynb).)

:::{admonition} Beispiel
Bis hierher war $w$ konstant. Es muss aber nicht konstant sein: Seien $v$ vier gemessene Körpergrößen in Zentimetern und $w$ das, was ein Modell für dieselben vier Personen vorhergesagt hat.

| $i$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $v_i$ (gemessen) | 178 | 160 | 155 | 174 |
| $w_i$ (vorhergesagt) | 178 | 155 | 150 | 180 |
| $v_i - w_i$ | 0 | 5 | 5 | −6 |

Es ist $d_1(v,w) = 0 + 5 + 5 + 6 = 16$ und damit $\texttt{mae}(v,w) = \frac{16}{4} = 4$: Im Mittel liegt das Modell um vier Zentimeter daneben.

Die mittlere Abweichung *ohne* Betrag, mit der wir diesen Abschnitt begonnen haben, ergibt dagegen $\frac{0 + 5 + 5 - 6}{4} = 1$ — trügerisch gering, weil sich die Fehler bei Person 4 gegen die bei den Personen 2 und 3 wegkürzen. Genau deshalb steht der Betrag da.
:::

Es ist natürlich sofort für einen Vektor $v$ interessant, welcher Vektor $w$ die geringste mittlere absolute Abweichung hat. Wenn man an $w$ jedoch keine weiteren Bedingungen stellt, ist mit $w=v$ das Minimum schnell gefunden. Wir werden dieser Frage später wieder begegnen und begnügen uns jetzt damit, zu fragen, welches $c \in \mathbb{R}$ den Ausdruck $\texttt{mae}(v,c)$ minimiert. Graphisch können wir uns vorstellen, als $x$-Achse die Zahlen von $1$ bis $n$ zu verwenden, und dort jeweils die Werte $v_i$ aufzutragen. Dann entspricht die Wahl eines $c \in \mathbb{R}$ einer horizontalen Gerade, und wir fragen uns, welche solche Gerade den geringsten gemeinsamen Abstand zu allen Punkten hat.

:::{admonition} Beispiel
Nehmen wir für die Körpergrößen $v = (178, 160, 155, 174)$ das konstante Modell $c = 165$, also die Behauptung „alle sind 165 cm groß“. Die Abweichungen sind $v_i - c = (13, -5, -10, 9)$, also

$$
d_1(v,165) = 13 + 5 + 10 + 9 = 37, \qquad \texttt{mae}(v,165) = \dfrac{37}{4} = 9{,}25.
$$

Ist $165$ die beste Wahl? Das ist genau die Frage nach dem Minimum, und sie hat, wie wir gleich sehen, eine überraschend einfache Antwort.
:::

:::{admonition} Definition
$\texttt{median}(v) := \arg\min_{c \in \mathbb{R}} \texttt{mae}(v,c)$ ist \`\`der'' *Median* von $v$.
:::

Das bedeutet also, der Median ist definiert als eine Zahl $c \in \mathbb{R}$ mit der Eigenschaft, dass die Zahl $\texttt{mae}(v,c)$ minimal wird.
Das bedeutet, für alle $c$ gilt $\texttt{mae}(v,c) \geq \texttt{mae}(v,\texttt{median}(v))$.
Achtung: So definiert können mehrere Zahlen 'der' Median sein. It's not a bug, it's a feature.

Diese Definition mag ungewohnt sein, aber sie erfüllt die folgende Eigenschaft:

:::{admonition} Proposition
Wenn $n \geq 3$ und $v \in \mathbb{R}^n$ sortiert ist, also $v_i < v_j$ für $i < j$, dann ist mit $v' := (v_2,\dots,v_{n-1}) \in \mathbb{R}^{n-2}$ ein neuer (kürzerer) Vektor definiert, sodass für alle $c \in \mathbb{R}$ mit $v_1 \leq c \leq v_n$ gilt:

$\texttt{mae}(v,c) = \texttt{mae}(v',c) + \dfrac{v_n - v_1}{n}$.
:::

Da der zweite Summand nicht von $c$ abhängt, ist er für die Bestimmung des Minimums unerheblich.
Durch induktive Anwendung dieser Erkenntnis bleibt uns nur noch, $\texttt{mae}(v,c)$ für Vektoren der Länge $1$ und $2$ zu bestimmen.
Es ist $\texttt{mae}((v_1),c) = |v_1 - c|$, was für $c = v_1$ minimal wird,
und $\texttt{mae}((v_1,v_2),c) = \frac{v_2 - v_1}{2}$, was für jedes $c$ zwischen $v_1$ und $v_2$ minimal wird. Also hängt der Median (einer sortierten Liste) nur vom mittleren / von den zwei mittleren Werten ab. Man definiert meist den Median so, dass in diesem Fall die Wahl $\texttt{median}((v_1,v_2)) = \dfrac{v_1+v_2}{2}$ getroffen wird (und so wollen wir es im Folgenden auch handhaben).
Überlegen Sie sich dazu, dass für jedes $c$ mit $a \leq c \leq b$ der mittlere Abstand zu $(a,b)$ stets $\frac{b-a}{2}$ ist, es also viele Mediane für den Vektor $v = (a,b)$ gibt.

:::{admonition} Beweis
$$
\begin{aligned}
\texttt{mae}(v,c) &= \phantom{\dfrac{|v_1 - c|}{n} +\ } \sum_{i=1}^{n} \dfrac{|v_i -c |}{n} \\
                  &= \dfrac{|v_1 - c|}{n} + \sum_{i=2}^{n-1} \dfrac{|v_i -c |}{n} + \dfrac{|v_n - c|}{n} \\
                  &= \sum_{i=2}^{n-1} \dfrac{|v_i -c |}{n} + \dfrac{-(v_1 - c) + (v_n - c)}{n} \\
                  &= \texttt{mae}(v',c) + \dfrac{v_n - c + c - v_1}{n}.
\end{aligned}
$$
:::

Da der Median also relativ schlecht die Daten widerspiegelt (von den meisten Daten ist er völlig unabhängig!), brauchen wir ein besseres Maß.
*Idee*: wir quadrieren die individuellen Fehlerterme in der Summe, damit große Fehler einen größeren Teil zur Summe beitragen. Praktisch: durch das Quadrieren muss man nicht mehr explizit den Absolutbetrag nehmen (das geschieht automatisch).

### Quadratische Abweichung

:::{admonition} Definition
Für Vektoren $v,w \in \mathbb{R}^n$ ist die *mittlere quadratische Abweichung* (mean squared error) definiert als

$$
\texttt{mse}(v,w) := \sum_{i=1}^n \dfrac{{\left(v_i - w_i\right)}^2}{n}
$$

und für $c \in \mathbb{R}$ schreiben wir $\texttt{mse}(v,c) := \texttt{mse}(v, (c)_{i=1}^n)$.
:::

Wie bei der absoluten Abweichung ist die Summe ohne $\frac1n$ eine Norm, diesmal die quadrierte $2$-Norm:

$$
d_2(v,w)^2 := \sum_{i=1}^n {\left( v_i - w_i \right)}^2 = \left\| v - w \right\|_2^2 = n \cdot \texttt{mse}(v,w).
$$

Der $\texttt{mse}$ hat gegenüber dem $\texttt{mae}$ die Einheit zum Quadrat — bei Körpergrößen in Zentimetern also Quadratzentimeter, was sich schlecht interpretieren lässt. Deshalb zieht man am Ende meist die Wurzel; das ist die Sample-Standardabweichung im nächsten Unterabschnitt.

:::{admonition} Proposition
Für einen Vektor $v \in \mathbb{R}^n$ minimiert der (arithmetische) *Mittelwert* von $v$ die mittlere quadratische Abweichung:

$\texttt{mean}(v) := \sum_{i=1}^n \dfrac{v_i}{n} = \arg\min_{c \in \mathbb{R}} \texttt{mse}(v,c)$.
:::

:::{admonition} Beweis
Wir schreiben ein beliebiges $c \in \mathbb{R}$ als $c = \texttt{mean}(v) + \delta$ und zeigen dann, dass $\texttt{mse}(v,c)$ minimal wird für $\delta = 0$.
Dazu faktorisieren wir aus: $(v_i - \texttt{mean}(v) - \delta)^2 = (v_i - \texttt{mean}(v))^2 - 2\delta (v_i - \texttt{mean}(v)) + \delta^2$ und teilen die Summe entsprechend auf:

$$
\begin{aligned}
\texttt{mse}(v,c) &= \texttt{mse}(v,\texttt{mean}(v) + \delta) = \sum_{i=1}^n \dfrac{(v_i - (\texttt{mean}(v) + \delta))^2}{n} \\
                  &= \dfrac{1}{n} \sum_{i=1}^n \left( {\left(v_i - \texttt{mean}(v)\right)}^2 - 2\delta \left(v_i - \texttt{mean}(v)\right) + \delta^2 \right) \\
                  &= \left( \dfrac{1}{n} \sum_{i=1}^n \left( (v_i - \texttt{mean}(v))^2 \right) \right) - 2\delta \left( \sum_{i=1}^n \frac{v_i}{n} - \texttt{mean}(v) \right) + \delta^2 \\
                  &= \texttt{mse}(v,\texttt{mean}(v)) - 2\delta(\texttt{mean}(v) - \texttt{mean}(v)) + \delta^2 \\
                  &= \texttt{mse}(v,\texttt{mean}(v)) + \delta^2
\end{aligned}
$$

und dieser Ausdruck wird nur für $\delta=0$ minimal, weil $\delta^2 \geq 0$.
:::

:::{admonition} Beispiel
Dieselben vier Körpergrößen, jetzt quadratisch gemessen. Für die Modellvorhersagen $w = (178, 155, 150, 180)$ ist

$$
d_2(v,w)^2 = 0^2 + 5^2 + 5^2 + (-6)^2 = 86, \qquad \texttt{mse}(v,w) = \dfrac{86}{4} = 21{,}5.
$$

Interessanter ist der Vergleich der konstanten Modelle. Der Mittelwert ist $\texttt{mean}(v) = \frac{667}{4} = 166{,}75$. Sortiert lautet der Vektor $(155, 160, 174, 178)$, und nach der Überlegung oben ist jede Zahl zwischen $160$ und $174$ ein Median; die übliche Konvention wählt die Mitte, also $\texttt{median}(v) = 167$. Die beiden Fehlermaße küren tatsächlich verschiedene Sieger:

| $c$ | $\texttt{mae}(v,c)$ | $\texttt{mse}(v,c)$ |
|---|---|---|
| $165$ | $9{,}25$ | $93{,}75$ |
| $\texttt{median}(v) = 167$ | $9{,}25$ | $90{,}75$ |
| $\texttt{mean}(v) = 166{,}75$ | $9{,}25$ | $\mathbf{90{,}6875}$ |

In der mittleren Spalte steht dreimal dasselbe: Jede Zahl zwischen $160$ und $174$ minimiert den $\texttt{mae}$, auch die $165$ — der Median ist eben nicht eindeutig. In der rechten Spalte gewinnt dagegen genau eine Zahl, und das ist der Mittelwert. Ein Fehlermaß auszuwählen heißt also, sich ein bestes Modell auszusuchen.
:::


### Sample-Standardabweichung

:::{admonition} Definition
Sei $v \in \mathbb{R}^n$. Die Quadratwurzel der mittleren quadratischen Abweichung (root mean squared error) vom Mittelwert nennen wir $\texttt{rmse}$ (oder auch Sample-Standardabweichung):

$\texttt{rmse}(v) = \sqrt{\texttt{mse}\left( v, \texttt{mean}(v) \right)}$.

Man schreibt dafür auch $\sigma(v)$, die *Standardabweichung* des Samples $v$. Die Schreibweise passt zu $\sigma(X)$ für Zufallsvariablen weiter unten.
:::

Zum Ausrechnen ist die Definition unpraktisch, weil man erst den Mittelwert bestimmen und dann noch einmal über alle Einträge gehen muss. Die folgende Umformung braucht nur die Summe der Einträge und die Summe ihrer Quadrate:

:::{admonition} Lemma
**(Verschiebungssatz)**

Für $v \in \mathbb{R}^n$ ist

$$
\texttt{rmse}(v)^2 = \texttt{mse}\left( v, \texttt{mean}(v) \right) = \texttt{mean}(v^2) - \texttt{mean}(v)^2,
$$

wobei $v^2 := {\left( v_i^2 \right)}_{i=1}^n$ komponentenweise zu lesen ist.
:::

:::{admonition} Beweis
Mit $m := \texttt{mean}(v)$ ist

$$
\texttt{mse}(v, m) = \dfrac{1}{n} \sum_{i=1}^n \left( v_i^2 - 2 m v_i + m^2 \right) = \texttt{mean}(v^2) - 2m \cdot \texttt{mean}(v) + m^2 = \texttt{mean}(v^2) - m^2.
$$
:::

:::{admonition} Proposition
Für $v \in \mathbb{R}^n$, $v \neq 0$, mit $\texttt{mean}(v)=0$ (ein *zentriertes* Sample, etwa $v := w - (\texttt{mean}(w))_{i=1}^n$ für ein beliebiges $w \in \mathbb{R}^n$) 
ist $\texttt{rmse}(v)^2 = \texttt{mse}(v,0) = \frac{1}{n} \sum_{i=1}^n v_i^2$ und der Vektor $v' := {\left( \dfrac{v_i}{\texttt{rmse}(v)} \right)}_{i=1}^n$ erfüllt $\texttt{mean}(v')=0$ und $\texttt{rmse}(v')=1$ (ein *normiertes* Sample).
:::

:::{admonition} Beweis
Das rechnet man direkt nach. Dass das zentrierte $v = w - (\texttt{mean}(w))_{i=1}^n$ wirklich Mittelwert $0$ hat, ist die Linearität des Mittelwerts: $\texttt{mean}(v) = \texttt{mean}(w) - \texttt{mean}(w) = 0$.
Wegen $\texttt{mean}(v) = 0$ ist $\texttt{rmse}(v)^2 = \texttt{mse}(v, \texttt{mean}(v)) = \texttt{mse}(v, 0) = \frac{1}{n} \sum_{i=1}^n v_i^2$, das ist der Verschiebungssatz mit $m = 0$.
Für $v'$ sei $s := \texttt{rmse}(v)$, und $s > 0$ wegen $v \neq 0$. Dann ist $\texttt{mean}(v') = \frac{1}{n} \sum_{i=1}^n \frac{v_i}{s} = \frac{\texttt{mean}(v)}{s} = 0$ und daher
$\texttt{rmse}(v')^2 = \texttt{mse}(v', 0) = \frac{1}{n} \sum_{i=1}^n \frac{v_i^2}{s^2} = \frac{\texttt{rmse}(v)^2}{s^2} = 1$.
:::

### Informationsgehalt

Ob ein Vektor $v \in \mathbb{R}^n$ für uns Informationen enthält, hängt davon ab, wie viel wir über $v$ bereits wissen.
Wenn wir z.B. wissen, dass $v$ ein Sample einer auf $\{0,1\}$ gleichverteilten Zufallsvariablen ist, wird uns nicht überraschen, wenn $v$ auch so aussieht. Jeder Eintrag von $v$ entspricht genau einem Bit Information. Wenn aber die Zufallsvariable nicht gleichverteilt ist, sondern z.B. auf den Zahlen $\{1,\dots, 26\}$ der Verteilungshäufigkeit der Buchstaben in der deutschen Sprache entspricht (mit $1$ für "a", $26$ für "z" usw.), so enthält ein Eintrag von $v$ potentiell weniger Informationen. Das "e" ist so häufig, dass wir wenig überrascht sind, wenn wir eins sehen. Ein "x" hingegen würde uns sehr überraschen, aber das kommt ja auch nicht so oft vor. Der mittlere Informationsgehalt ist also geringer als bei einer Gleichverteilung.

### Lagemaße zentraler Tendenz

Zu Median und Mittelwert gehört traditionell noch der **Modus**, der häufigste Wert. Er passt in dasselbe Muster: Der Median ist das beste konstante Modell für den absoluten Fehler, der Mittelwert für den quadratischen, und der Modus für den *Zählfehler*, der jede Abweichung gleich zählt, egal wie groß sie ist. Für ein nominales Merkmal, etwa die Spalte `Survived` der Titanic-Liste, ist das der einzige Fehler, der Sinn ergibt; das beste konstante Modell ist dann die häufigste Klasse, und der Anteil, in dem es richtig liegt, ist seine *Accuracy* (siehe [Titanic EDA](explorative-analyse-mit-numpy.ipynb)).
[Hier gibt es ein kurzes Erklärvideo (auf Englisch) vom Crash Course Statistics zu Mean, Median und Mode](https://www.youtube.com/watch?v=kn83BA7cRNM&list=PL8dPuuaLjXtNM_Y-bUAhblSAdWRnmBUcr). [Das in der Playlist folgende Video diskutiert die damit zusammenhängenden Begriffe für Streuung von Daten](https://www.youtube.com/watch?v=R4yfNi_8Kqw) (die Abweichung, mit der wir angefangen haben).



## Momente einer Zufallsvariable

### Vom Mittelwert zum Erwartungswert

Bis hierher haben wir mit Samples gerechnet: $\texttt{mean}(v)$ ist eine Zahl, die aus $n$ konkreten Messwerten entsteht. Jetzt drehen wir die Blickrichtung um und fragen, welche Zahl zu einer *Verteilung* gehört, also zu dem Modell, aus dem die Daten stammen könnten. Der Weg dahin ist kurz, und er erklärt, warum der Erwartungswert genau so aussieht, wie er aussieht.

Sei $X$ eine Zufallsvariable mit endlich vielen Werten $y_1,\dots,y_k$ und der Verteilung $p = (p_1,\dots,p_k)$, also $p_j = P(X = y_j)$. Nehmen wir für einen Moment an, die $p_j$ seien rationale Zahlen mit gemeinsamem Nenner $N$, sagen wir $p_j = \frac{a_j}{N}$ mit $a_1 + \dots + a_k = N$. Dann gibt es eine Stichprobe der Größe $N$, die diese Verteilung *exakt* trifft: die, in der der Wert $y_j$ genau $a_j$-mal vorkommt. Wir nennen sie das **idealisierte Sample** $\tilde{D}$ zu $p$ — die Stichprobe, die man bekäme, wenn der Zufall sich ein einziges Mal vollkommen an die Wahrscheinlichkeiten hielte.

Den Mittelwert dieses idealisierten Samples können wir direkt hinschreiben, denn wir wissen ja, wie oft jeder Wert vorkommt:

$$
\texttt{mean}(\tilde{D}) = \dfrac{1}{N} \sum_{j=1}^k a_j y_j = \sum_{j=1}^k \dfrac{a_j}{N} y_j = \sum_{j=1}^k p_j y_j.
$$

Rechts steht keine Stichprobe mehr, sondern nur noch die Verteilung. Damit ist auch die Annahme überflüssig geworden, dass die $p_j$ rational sein müssen: Die rechte Seite ergibt für jede Verteilung Sinn, und der Umweg über $\tilde{D}$ hat nur dazu gedient, die Formel zu finden. Genau diese Größe nennen wir den Erwartungswert von $X$.

:::{admonition} Beispiel
Ein fairer Würfel hat $p = \left(\frac16,\dots,\frac16\right)$, also $N = 6$ und $a_j = 1$ für alle $j$. Das idealisierte Sample ist $\tilde{D} = (1,2,3,4,5,6)$ — jede Augenzahl genau einmal — mit

$$\texttt{mean}(\tilde{D}) = \dfrac{1+2+3+4+5+6}{6} = \dfrac{21}{6} = 3{,}5.$$

Der Erwartungswert eines fairen Würfels ist also $3{,}5$, eine Zahl, die der Würfel selbst nie zeigt.

Ein gezinkter Würfel mit $p = \left(\frac{1}{10},\frac{1}{10},\frac{1}{10},\frac{1}{10},\frac{1}{10},\frac{5}{10}\right)$ hat $N = 10$, das idealisierte Sample $(1,2,3,4,5,6,6,6,6,6)$ und damit den Erwartungswert $\frac{45}{10} = 4{,}5$.
:::

Der Spezialfall $k = 1$ ist die Probe aufs Exempel: Eine Verteilung, die einen einzigen Wert $y_1$ mit Wahrscheinlichkeit $1$ annimmt — das Dirac-Maß $\delta_{y_1}$ aus dem Kapitel [Formalismus der Stochastik](intro-stochastik.md) — hat das idealisierte Sample $(y_1,\dots,y_1)$ und folglich den Erwartungswert $y_1$. Ein konstantes Modell und der Wert, den es vorhersagt, sind dasselbe. In der Sprache des vorigen Abschnitts: Das beste konstante Modell für den quadratischen Fehler war der Mittelwert der Daten, und als Verteilung gelesen ist ein konstantes Modell ein Dirac-Maß.

:::{admonition} Beispiel
Auf $\Omega = \{0,1,\dots,n-1\}$ — genau das, was `range(n)` in Python aufzählt — sei $P$ die Gleichverteilung. Für $Y(\omega) := \omega$ ist

$$\mathbb{E}(Y) = \sum_{\omega=0}^{n-1} \dfrac{\omega}{n} = \dfrac{1}{n}\cdot\dfrac{(n-1)n}{2} = \dfrac{n-1}{2},$$

für $X(\omega) := \omega + 1$ dagegen $\mathbb{E}(X) = \mathbb{E}(Y) + 1 = \frac{n+1}{2}$ (das ist die Linearität weiter unten). Für $n = 6$ sind das $2{,}5$ und $3{,}5$: Ob man die Würfelseiten bei $0$ oder bei $1$ zu zählen beginnt, macht genau einen Punkt aus. In Simulationen ist das die häufigste Quelle von Off-by-one-Fehlern.
:::

Damit können wir die Formel als Definition festhalten. Sie funktioniert wörtlich genauso, wenn $\Omega$ abzählbar unendlich ist; aus der endlichen Summe wird dann eine Reihe, und die muss nicht mehr konvergieren.

### Erwartungswert, diskret

:::{admonition} Definition
Sei $X \colon \Omega \to \mathbb{R}$ eine diskrete reelle Zufallsvariable (also $\Omega$ ein diskreter Wahrscheinlichkeitsraum, höchstens abzählbar). Dann ist der *Erwartungswert* von $X$ definiert als

$$
\mathbb{E}X := \mathbb{E}(X) := \sum_{\omega \in \Omega} X(\omega) P(\{\omega\}).
$$

Wenn man nicht "in $\Omega$" arbeiten möchte, kann man diese Summe auch umstellen und über alle Werte $\{x_i\}_{i\in I}$ summieren, die $X$ annimmt:
$\mathbb{E}(X) = \sum_{i \in I} x_i P(X = x_i)$.
:::

Der Erwartungswert ist also das mit den Wahrscheinlichkeiten gewichtete Mittel der Werte von $X$.

:::{admonition} Beispiel
Der Erwartungswert einer Gleichverteilung auf $\Omega = \{1,\dots,n\}$ ist $\sum_{i=1}^n \frac{i}{n}$, also $\frac{n(n+1)}{2n} = \frac{n+1}{2}$.
:::

Für endliches $\Omega$ ist die Summe endlich und existiert immer. Ist $\Omega$ abzählbar unendlich, so ist die Summe eine Reihe, und die muss nicht konvergieren: Es gibt Zufallsvariablen, für die sich kein Erwartungswert bestimmen lässt. Ein Beispiel: Auf $\Omega = \{1, 2, 3, \dots\}$ ist durch $P(\{k\}) := \frac{6}{\pi^2 k^2}$ ein Wahrscheinlichkeitsmaß gegeben (weil $\sum_{k \geq 1} \frac{1}{k^2} = \frac{\pi^2}{6}$), und für $X(k) := k$ wird die Reihe $\sum_{k \geq 1} k \cdot \frac{6}{\pi^2 k^2} = \frac{6}{\pi^2} \sum_{k \geq 1} \frac{1}{k}$ zur harmonischen Reihe, die divergiert. Diese Zufallsvariable hat keinen Erwartungswert.

Für stetige Zufallsvariablen, die überabzählbar viele Werte annehmen, tritt an die Stelle der Summe ein Integral über eine Dichte $f$: $\mathbb{E}(X) = \int x f(x)\,dx$. Diese Definition geben wir im Kapitel [Stetige Verteilungen](stetige-verteilungen.md), sobald wir Dichten kennen. Alles, was wir in diesem Kapitel über den Erwartungswert festhalten, gilt für stetige Zufallsvariablen genauso, mit Integralen an Stelle von Summen.

### Exkurs: Erwartungswert allgemein

::::{note}
**Exkurs (nicht klausurrelevant):** Summe und Dichte-Integral sind zwei Spezialfälle einer einzigen Definition, die für beliebige Zufallsvariablen funktioniert.

:::{admonition} Definition
Sei $X \colon \Omega \to \mathbb{R}$ eine reelle Zufallsvariable, dann ist der *Erwartungswert* definiert als

$\mathbb{E}X := \mathbb{E}(X) := \int_{\Omega} X dP = \int_{\Omega} X(\omega) d P(\omega) \in \mathbb{R}$

also als das Integral der Abbildung $X$ bezüglich des Maßes $P$.
:::

Dieses Integral (das Lebesgue-Integral bezüglich $P$) existiert im Allgemeinen nicht, d.h. es gibt Zufallsvariablen, für die sich kein Erwartungswert bestimmen lässt. Für diskretes $\Omega$ vereinfacht sich das Integral zur Summe $\sum_{\omega \in \Omega} X(\omega) P(\{\omega\})$ von oben, und hat $X$ eine Dichte $f$, so wird daraus das Integral $\int x f(x)\,dx$. Mit dieser allgemeinen Definition lassen sich die Rechenregeln unten für alle Zufallsvariablen auf einmal beweisen; das ist der Grund, warum sie in der Maßtheorie so gewählt wird.
::::

Es gibt einen inneren Zusammenhang zwischen dem Erwartungswert und den Stichproben einer Zufallsvariable:

:::{admonition} Satz
**Gesetz der großen Zahlen**

Ist eine unendliche Folge $(X_i)_{i \in \mathbb{N}}$ von Zufallsvariablen $\Omega \to \mathbb{R}$ gegeben, so sagt man, dass diese Folge einem *starken Gesetz der großen Zahlen* genügt, wenn die Mittelwert-Abweichungs-Zufallsvariablen $\overline{X_n^\ast} := \dfrac{1}{n} \sum_{i=1}^n \left( X_i - \mathbb{E}(X_i) \right)$ gegen $0$ konvergieren, und zwar $P$-fast sicher (d.h. $P(\lim_{n\to\infty} \overline{X_n^\ast} = 0) = 1$).

Wenn die $X_i$ nun unabhängig und identisch verteilt sind ($X_i = X$ für festes $X$) mit existierendem Erwartungswert $\mathbb{E}(X)$,
dann genügen die $X_i$ einem starken Gesetz der großen Zahlen, d.h.
dann konvergiert $\overline{X_n^\ast} = \overline{X_n} - \mathbb{E}X$, die Abweichung des arithmetischen Mittels einer Stichprobe von $X$ der Größe $n$ vom Erwartungswert, $P$-fast sicher gegen $0$.
Das bedeutet umgekehrt auch: Die Wahrscheinlichkeit, dass das Stichprobenmittel für beliebig große $n$ vom Erwartungswert abweicht, ist $0$.
:::

Aus der $P$-fast sicheren Konvergenz folgt auch die stochastische Konvergenz:
$\lim_{n\to\infty} P\left(|\overline{X_n}| \geq \epsilon \right) = 0$ für jedes $\epsilon > 0$.

Wir wollen uns im Folgenden nicht mehr über Konvergenzbegriffe der Stochastik den Kopf zerbrechen (das kann man bei Bedarf immer noch nachholen und das lohnt sich auch je nach Anwendung), sondern in gewohnter Tradition das gute Gefühl mitnehmen, dass der Erwartungswert eine geeignete Größe ist, um erwartungsvoll eine Stichprobe zu analysieren. Je größer die Stichprobe, desto geringer dürfte die Abweichung des Stichprobenmittels vom Erwartungswert sein - so will es das Gesetz. Umgekehrt findet man also zu jeder vorgegebenen Schranke $\epsilon > 0$ eine Stichprobengröße $n$ sodass das Stichprobenmittel einer zufällig gezogenen Stichprobe fast immer um weniger als $\epsilon$ vom Erwartungswert abweicht.

Damit schließt sich der Kreis zum idealisierten Sample vom Anfang des Abschnitts: Dort haben wir so getan, als hielte sich eine Stichprobe exakt an die Wahrscheinlichkeiten, um überhaupt auf die Formel zu kommen. Das Gesetz der großen Zahlen sagt, dass echte Stichproben das für große $n$ beliebig gut tun — der Umweg war also keiner.


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
**(Verschiebungssatz)**

Es ist $\mathbb{V}(X) = \mathbb{E}\left( X^2 \right) - {\left(\mathbb{E}X\right)}^2$.
:::

:::{admonition} Beweis
Es ist ${\left(X - \mathbb{E}X\right)}^2 = X^2 - 2X\mathbb{E}X + {\left(\mathbb{E}X\right)}^2$ und mit der Linearität des Erwartungswerts also

$$
\begin{aligned}
\mathbb{V}(X) &= \mathbb{E}\left( {\left(X - \mathbb{E}X\right)}^2 \right) \\
              &= \mathbb{E}\left( X^2 \right) - 2\mathbb{E}\left( X \right)\mathbb{E}\left( X \right) + {\left(\mathbb{E}X\right)}^2 \mathbb{E}\left( 1 \right) \\
              &= \mathbb{E}\left( X^2 \right) - {\left(\mathbb{E}X\right)}^2.
\end{aligned}
$$
:::

Das ist das Gegenstück zum Verschiebungssatz $\texttt{rmse}(v)^2 = \texttt{mean}(v^2) - \texttt{mean}(v)^2$ für Samples von oben.
Für eine zentrierte Zufallsvariable, d.h. mit $\mathbb{E}(X) = 0$, ist offensichtlich $\mathbb{V}(X) = \mathbb{E}(X^2)$.

:::{admonition} Definition
Man nennt allgemein auch $\mathbb{E}(X^n)$ das $n$-te *Moment* und $\mathbb{E}((X - \mathbb{E}X)^n)$ das $n$-te *zentrale Moment*.
Der Erwartungswert ist also das erste Moment und die Varianz das zweite zentrale Moment.
Das dritte zentrale Moment heißt auch *Schiefe* (skewness) und das vierte *Wölbung* (kurtosis).
Die Schiefe ist ein Maß dafür, wie symmetrisch die Verteilung um den Erwartungswert ist.
Man nennt $\sigma(X) := \sqrt{\mathbb{V}(X)}$ die *Standardabweichung* von X.
:::

Die Varianz hilft uns bei der Einschätzung, wie wahrscheinlich gewisse Abweichungen vom Erwartungswert sind. Der Schlüssel dazu ist eine Ungleichung, die zunächst nur den Erwartungswert benutzt:

:::{admonition} Satz
**(Markov-Ungleichung)**

Für $X$ eine reelle Zufallsvariable mit $X \geq 0$ und $c > 0$ ist

$$
P\left( X \geq c \right) \leq \dfrac{\mathbb{E}X}{c}.
$$
:::

:::{admonition} Beweis
Sei $1_{\{X \geq c\}} \colon \Omega \to \{0,1\}$ die Indikatorfunktion des Ereignisses $\{X \geq c\}$, also $1$ auf $\{X \geq c\}$ und $0$ sonst. Dann gilt punktweise $c \cdot 1_{\{X \geq c\}} \leq X$: Wo der Indikator $1$ ist, ist $X \geq c$, und wo er $0$ ist, ist $X \geq 0$ nach Voraussetzung. Der Erwartungswert einer Indikatorfunktion ist die Wahrscheinlichkeit des Ereignisses, im diskreten Fall $\mathbb{E}(1_A) = \sum_{\omega \in A} P(\{\omega\}) = P(A)$. Mit der Linearität und der Monotonie des Erwartungswerts (Rechenregeln oben) folgt

$$
c \cdot P(X \geq c) = \mathbb{E}\left( c \cdot 1_{\{X \geq c\}} \right) \leq \mathbb{E}X,
$$

und Teilen durch $c > 0$ liefert die Behauptung.
:::

Die Markov-Ungleichung ist grob, aber sie liefert sofort die Ungleichung, die wir eigentlich wollen:

:::{admonition} Satz
**(Tschebyscheff-Ungleichung)**

Für $X$ eine reelle Zufallsvariable, $c > 0$ ist

$$
P\left( | X - \mathbb{E} X | \geq c \right) \leq \dfrac{\mathbb{V}X}{c^2}.
$$
:::

:::{admonition} Beweis
Die Zufallsvariable $Y := {\left( X - \mathbb{E}X \right)}^2$ ist nichtnegativ, und nach Definition der Varianz ist $\mathbb{E}Y = \mathbb{V}X$. Die Markov-Ungleichung für $Y$ mit der Schranke $c^2 > 0$ ergibt

$$
P\left( {\left( X - \mathbb{E}X \right)}^2 \geq c^2 \right) \leq \dfrac{\mathbb{E}Y}{c^2} = \dfrac{\mathbb{V}X}{c^2}.
$$

Weil $c > 0$ ist, gilt ${\left( X - \mathbb{E}X \right)}^2 \geq c^2$ genau dann, wenn $|X - \mathbb{E}X| \geq c$. Die beiden Ereignisse sind also gleich, und das ist die Behauptung.
:::

Dabei ist der Spezialfall $c=\sigma$ trivial, weil auf der rechten Seite nur $1$ steht, und jede Wahrscheinlichkeit $\leq 1$ ist.
Der Spezialfall $c = k\sigma$ mit $k \in \mathbb{N}$ vereinfacht sich allerdings zu

$$
P\left( | X - \mathbb{E} X | \geq k\sigma \right) \leq \dfrac{1}{k^2}.
$$

Daran sehen wir: Abweichungen von $2\sigma$ haben eine Wahrscheinlichkeit $\leq \frac{1}{4}$, und Abweichungen von $3\sigma$ bereits nur noch $\leq \frac{1}{9}$. Wenn wir also Abweichungen in Vielfachen von $\sigma$ messen, so ist die Wahrscheinlichkeit für so große Abweichungen näherungsweise umgekehrt quadratisch proportional (so steht's ja oben schon in der Ungleichung). Damit haben wir auch ein Kriterium zur Hand, um in Daten fehlerhafte Datenpunkte auszusortieren - wenn Abweichung größer $k\sigma$ mit $k > 1$ häufiger als erwartet zu sehen sind, dann gehören diese Datenpunkte zumindest nicht zu der Verteilung, die man erwartet.

Die wichtigste Anwendung der Ungleichung ist das Stichprobenmittel selbst. Damit können wir das Gesetz der großen Zahlen von oben in einer schwächeren Form tatsächlich beweisen, und zwar genau mit den Werkzeugen, die wir jetzt haben:

:::{admonition} Satz
**(Schwaches Gesetz der großen Zahlen)**

Seien $X_1, \dots, X_n$ unabhängig und identisch verteilt wie $X$ (kurz: iid; jedes $X_i$ hat dieselbe Verteilung wie $X$), und $X$ habe endliche Varianz. Für das Stichprobenmittel $\overline{X_n} := \frac{1}{n} \sum_{i=1}^n X_i$ gilt dann für jedes $c > 0$

$$
P\left( | \overline{X_n} - \mathbb{E} X | \geq c \right) \leq \dfrac{\mathbb{V}X}{n c^2} \xrightarrow{n \to \infty} 0.
$$
:::

:::{admonition} Beweis
Nach der Linearität des Erwartungswerts ist $\mathbb{E}\overline{X_n} = \frac{1}{n} \sum_{i=1}^n \mathbb{E}X_i = \mathbb{E}X$, denn jedes $X_i$ hat denselben Erwartungswert wie $X$.
Nach den Rechenregeln für die Varianz (Abschnitt *Rechenregeln für die Varianz* weiter unten: $\mathbb{V}(aY) = a^2\,\mathbb{V}Y$, und die Varianz einer Summe unabhängiger Zufallsvariablen ist die Summe der Varianzen) ist

$$
\mathbb{V}\overline{X_n} = \dfrac{1}{n^2} \mathbb{V}\left( \sum_{i=1}^n X_i \right) = \dfrac{1}{n^2} \sum_{i=1}^n \mathbb{V}X_i = \dfrac{n\,\mathbb{V}X}{n^2} = \dfrac{\mathbb{V}X}{n}.
$$

Die Tschebyscheff-Ungleichung für $\overline{X_n}$ liefert nun $P(|\overline{X_n} - \mathbb{E}X| \geq c) \leq \mathbb{V}\overline{X_n} / c^2 = \mathbb{V}X / (n c^2)$, und dieser Ausdruck geht für $n \to \infty$ gegen $0$.
:::

Das ist genau die stochastische Konvergenz, die wir oben aus dem (unbewiesenen) starken Gesetz der großen Zahlen gefolgert hatten: Das schwache Gesetz ist die Form, die wir mit unseren Mitteln beweisen können; das starke Gesetz mit seiner fast sicheren Konvergenz braucht mehr Werkzeug, kommt dafür aber ohne die Voraussetzung endlicher Varianz aus.

Das schwache Gesetz ist außerdem das Gesetz der großen Zahlen mit einer Zahl dran: Die Wahrscheinlichkeit einer Abweichung um mehr als $c$ fällt wie $1/n$, oder anders gelesen, der typische Fehler des Stichprobenmittels schrumpft wie $1/\sqrt{n}$. Wer den Fehler halbieren will, braucht die vierfache Stichprobe. Die Schranke ist grob; das Kapitel [Normalverteilung](normalverteilung.ipynb) liefert mit dem zentralen Grenzwertsatz eine schärfere, und das Kapitel [Statistische Tests](statistische-tests.md) macht daraus das Rezept, mit dem man von der Stichprobe auf die Population schließt.

:::{admonition} Bemerkung
Im Deep Learning ist der wahre Loss eines Modells der Erwartungswert der Loss-Funktion über die Verteilung der Daten, und den kann man nicht ausrechnen, weil man diese Verteilung nicht kennt. Ein Mini-Batch aus wenigen Datenpunkten liefert stattdessen ein Stichprobenmittel des Loss: billig, aber mit hoher Varianz, also genau die Situation des schwachen Gesetzes der großen Zahlen, und $\mathbb{V}X / n$ sagt, wie viel Rauschen ein Batch der Größe $n$ mitbringt. Die Vorlesung *Einführung in Deep Learning* baut darauf auf (stochastischer Gradientenabstieg).
:::

Wendet man das Gesetz der großen Zahlen auf die Zufallsvariable ${\left(X-\mathbb{E}(X)\right)}^2$ an, so sieht man, dass auch die Standardabweichung gegen die Sample-Standardabweichung konvergiert. Damit ist also die Sample-Standardabweichung ein guter Ersatz, wenn sich die wahre Varianz der Zufallsvariable nicht bestimmen lässt.


### Einschub: Logarithmus

Der nächste Abschnitt rechnet durchgehend mit Logarithmen. Weil die aus der Schule oft eine Weile her sind, hier das Nötige auf einer halben Seite.

:::{admonition} Definition
Für $b > 0$, $b \neq 1$, ist der *Logarithmus zur Basis $b$* die Umkehrung des Potenzierens: Aus $b^x = y$ folgt $x = \log_b(y)$, und umgekehrt. Er ist für $y > 0$ definiert.

Drei Basen haben eigene Namen: $\ln := \log_e$ (der *natürliche* Logarithmus, zur Basis $e \approx 2{,}718$), $\operatorname{lb} := \log_2$ (der *binäre* Logarithmus, auch $\operatorname{ld}$ geschrieben) und $\log_{10}$ (der *dekadische*).
:::

Der Logarithmus zählt Größenordnungen. Zur Basis $10$ kann man das direkt ablesen: $\log_{10}(100) = 2$ und $\log_{10}(1000) = 3$, und weil der Logarithmus streng monoton wächst, liegt $\log_{10}(y)$ für jede Zahl $y$ zwischen $100$ und $1000$ zwischen $2$ und $3$. Die Anzahl der Dezimalstellen einer natürlichen Zahl $y$ ist damit $\lfloor \log_{10}(y) \rfloor + 1$ — und zur Basis $2$ entsprechend die Anzahl der Binärstellen.

Die Rechenregeln folgen alle aus $e^{\ln(y)} = y$ und $\ln(e^x) = x$ sowie dem Potenzgesetz $(e^u)^v = e^{uv}$:

$$
\begin{aligned}
b^x &= \left( e^{\ln b} \right)^x = e^{\ln(b)\, x}, \\
\ln\left( b^x \right) &= x \ln(b), \\
\ln(y) &= \ln\left( b^{\log_b(y)} \right) = \ln(b) \log_b(y), \\
\text{also}\quad \log_b(y) &= \dfrac{\ln(y)}{\ln(b)}.
\end{aligned}
$$

Die letzte Zeile ist die *Basiswechselformel*: Logarithmen zu verschiedenen Basen unterscheiden sich nur um einen konstanten Faktor. Deshalb ist die Wahl der Basis bei der Entropie eine Frage der Maßeinheit und nicht der Sache — zur Basis $2$ misst man in **bit**, zur Basis $e$ in **nat**, und zwischen beiden liegt der Faktor $\ln(2) \approx 0{,}693$.

:::{admonition} Beispiel
Die Zahl $77$ ist binär $1001101_2$, also $64 + 8 + 4 + 1$, und braucht damit $7$ Binärstellen. Nachgerechnet: $\log_2(77) = \frac{\ln 77}{\ln 2} \approx 6{,}27$, und $\lfloor 6{,}27 \rfloor + 1$ sind die erwarteten $7$ Stellen. Die Umkehrung liest man genauso: Mit $7$ bit lassen sich $2^7 = 128$ verschiedene Dinge unterscheiden, mit $6$ bit nur $64$ — zu wenig für $77$.
:::

In Numpy heißen die drei Funktionen `np.log` (natürlich, *nicht* dekadisch — eine beliebte Fehlerquelle), `np.log2` und `np.log10`.

## Entropie

[Vorlesungsaufzeichnung Entropie](https://media.hhu.de/channel/video/data-science-vl-5-entropie-2024/8f216336cc82cdd8015ddb7a6c59c252/167)

:::{admonition} Definition
Bei einem diskreten Wahrscheinlichkeitsraum $\Omega$ nennen wir für $x \in \Omega$ die *Information* (auch *Selbstinformation*) von $x$

$$
I(x) := -\log_b(P(\{x\})).
$$

Dabei ist die Basis $b$ des Logarithmus in der Regel $2$, aber letztlich nicht so wichtig.
Für eine Zufallsvariable $X \colon \Omega' \to \Omega$ können wir nun die Verkettung $I \circ X \colon \Omega' \to \mathbb{R}$ betrachten,
eine reelle Zufallsvariable. Ihr Erwartungswert ist die mittlere Information von $X$, wir sagen auch *Entropie*

$$
\begin{aligned}
H(X) := \mathbb{E}\left( I(X) \right) &= \sum_{\omega' \in \Omega'} -\log_b(P(\{X(\omega')\})P(X(\omega')) \\
                                      &= - \sum_{\omega \in \Omega} \log_b(P(\{\omega\}))P(\{\omega\}).
\end{aligned}
$$
:::

:::{admonition} Beispiel
Bei einer Gleichverteilung auf $\Omega = \{1,\dots,n\}$ ist für $x\in\Omega$ stets $P(\{x\}) = \frac{1}{n}$,
also $I(x) = -\log_2(P(\{x\})) = -\log_2\frac{1}{n} = \log_2(n)$ und somit
$H(X) = \sum_{i=1}^n \frac{\log_2(n)}{n} = \log_2(n)$.
Diese Zahl verrät uns, dass wir im Mittel $\log_2(n)$ bits an Information brauchen, um ein Sample der Größe $n$ zu rekonstruieren, wenn wir die Verteilung von $X$ kennen. Es gibt andere Verteilungen, die es erlauben mit im Mittel weniger Information ein Sample zu rekonstruieren. Genau genommen sogar jede, denn die Gleichverteilung hat maximale Entropie unter allen diskreten Verteilungen. Sie korrespondiert dazu, dass wir maximal wenig wissen und daher alle Ergebnisse als gleich wahrscheinlich annehmen.
:::

Am anderen Ende der Skala steht die Dirac-Verteilung: Ist $P(\{\xi\}) = 1$ für ein einziges $\xi \in \Omega$
und $P(\{\omega\}) = 0$ für alle anderen, so ist $I(\xi) = -\log_2(1) = 0$ und damit $H(X) = 0$
(für die Summanden mit $P(\{\omega\}) = 0$ verwenden wir die übliche Konvention $0\log 0 = 0$).
Das ist der kleinstmögliche Wert, denn $H(X)$ ist eine Summe nichtnegativer Terme.
Auf einer endlichen Menge $\Omega$ gilt also stets $0 \leq H(X) \leq \log_2|\Omega|$,
wobei das Minimum genau von den Dirac-Verteilungen angenommen wird (davon gibt es $|\Omega|$ Stück, eine je Element)
und das Maximum ausschließlich von der Gleichverteilung.

Am besten versteht man die Entropie als eine relative Größe, und das werden wir später noch tun.


## Unabhängigkeit

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

:::{admonition} Beispiel
**Unabhängig: zwei Würfel.** Wir werfen zwei faire sechsseitige Würfel. Als Wahrscheinlichkeitsraum nehmen wir $\Omega = \{1,\dots,6\}^2$ mit der Gleichverteilung, also $36$ gleich wahrscheinliche Ergebnisse $(i,j)$. Sei $A$ das Ereignis „der erste Würfel zeigt eine gerade Zahl“ und $B$ das Ereignis „der zweite Würfel zeigt eine Sechs“. Dann ist

$$
P(A) = \dfrac{18}{36} = \dfrac{1}{2}, \qquad P(B) = \dfrac{6}{36} = \dfrac{1}{6}.
$$

Für den Schnitt zählen wir aus, statt eine Formel zu benutzen: $A \cap B = \{(2,6),(4,6),(6,6)\}$, also $P(A \cap B) = \frac{3}{36} = \frac{1}{12}$. Und tatsächlich ist $\frac12 \cdot \frac16 = \frac{1}{12}$, die beiden Ereignisse sind also unabhängig.

Dass wir ausgezählt haben, ist wichtig: Hätten wir $P(A\cap B)$ gleich als Produkt berechnet, hätten wir die Unabhängigkeit vorausgesetzt statt sie zu prüfen. Inhaltlich ist sie hier klar, weil sich $A$ und $B$ auf verschiedene Würfel beziehen.
:::

:::{admonition} Beispiel
**Abhängig: Bonbons ohne Zurücklegen.** In einer Tüte liegen drei Bonbons: ein rotes, ein grünes, ein blaues. Wir ziehen zwei davon nacheinander heraus, ohne das erste zurückzulegen. Der Wahrscheinlichkeitsraum ist die Menge der $6$ geordneten Paare verschiedener Farben,

$$
\Omega = \{(r,g),(r,b),(g,r),(g,b),(b,r),(b,g)\},
$$

wieder mit der Gleichverteilung. Sei $A$ das Ereignis „das erste Bonbon ist rot“ und $B$ das Ereignis „das zweite Bonbon ist grün“. Dann ist $A = \{(r,g),(r,b)\}$ mit $P(A) = \frac{2}{6} = \frac13$ und $B = \{(r,g),(b,g)\}$ mit $P(B) = \frac{2}{6} = \frac13$. Der Schnitt enthält nur ein einziges Ergebnis, $A \cap B = \{(r,g)\}$, also

$$
P(A \cap B) = \dfrac{1}{6} \neq \dfrac{1}{9} = P(A)\,P(B).
$$

Die beiden Ereignisse sind also *nicht* unabhängig. Das ist auch inhaltlich richtig: Wenn zuerst das rote Bonbon gezogen wurde, bleiben nur noch grün und blau übrig, und grün ist im zweiten Zug auf einmal wahrscheinlicher geworden — von $\frac13$ auf $\frac12$. Genau diese Zahl bekommt weiter unten einen Namen, sie ist die bedingte Wahrscheinlichkeit $P(B \mid A)$.

Ziehen ohne Zurücklegen ist in Python `random.sample`, Ziehen mit Zurücklegen `random.choices` (siehe [Stochastik programmieren](stochastik-programmieren.ipynb)) — der Unterschied zwischen den beiden Funktionen ist genau der Unterschied zwischen abhängig und unabhängig.
:::

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
Im Bonbon-Beispiel oben ist $P(B \mid A) = \frac{P(A \cap B)}{P(A)} = \frac{1/6}{1/3} = \frac12$, und das ist nicht $P(B) = \frac13$ — so sieht Abhängigkeit in Zahlen aus.
Bedingte Wahrscheinlichkeiten treten also stets dann auf (bzw. sind besonders interessant), wenn zwei Ereignisse (bzw. Zufallsvariablen) nicht unabhängig sind.

### Rechenregeln für die Varianz

Der Erwartungswert ist linear, die Varianz ist es nicht. Stattdessen gelten die folgenden beiden Regeln,
die wir im nächsten Kapitel ständig brauchen werden.

:::{admonition} Lemma
Sei $X \colon \Omega \to \mathbb{R}$ eine Zufallsvariable mit endlicher Varianz.

1. Für $a,b \in \mathbb{R}$ ist $\mathbb{V}(aX+b) = a^2\,\mathbb{V}(X)$.

2. Sind $X$ und $Y$ unabhängig, so ist $\mathbb{V}(X+Y) = \mathbb{V}(X) + \mathbb{V}(Y)$.
   Allgemeiner ist für paarweise unabhängige $X_1,\dots,X_n$

$$
\mathbb{V}\left( \sum_{i=1}^n X_i \right) = \sum_{i=1}^n \mathbb{V}(X_i).
$$
:::

:::{admonition} Beweis
(1) Nach der Linearität des Erwartungswerts ist $\mathbb{E}(aX+b) = a\,\mathbb{E}X + b$, also

$$
aX + b - \mathbb{E}(aX+b) = a\left( X - \mathbb{E}X \right)
$$

und damit $\mathbb{V}(aX+b) = \mathbb{E}\left( a^2 {\left( X - \mathbb{E}X \right)}^2 \right) = a^2\,\mathbb{V}(X)$.
Insbesondere ändert eine Verschiebung um $b$ die Varianz nicht.

(2) Wir multiplizieren aus und nutzen die Linearität:

$$
\begin{aligned}
\mathbb{V}(X+Y) &= \mathbb{E}\left( {\left( (X - \mathbb{E}X) + (Y - \mathbb{E}Y) \right)}^2 \right) \\
                &= \mathbb{E}\left( {(X - \mathbb{E}X)}^2 \right) + \mathbb{E}\left( {(Y - \mathbb{E}Y)}^2 \right)
                   + 2\,\mathbb{E}\left( (X - \mathbb{E}X)(Y - \mathbb{E}Y) \right) \\
                &= \mathbb{V}(X) + \mathbb{V}(Y) + 2\left( \mathbb{E}(XY) - \mathbb{E}(X)\mathbb{E}(Y) \right).
\end{aligned}
$$

Sind $X$ und $Y$ unabhängig, so ist der Klammerausdruck nach der Produktregel gleich $0$.
Der allgemeine Fall folgt per Induktion über $n$.
:::

Der Term $\mathbb{E}(XY) - \mathbb{E}(X)\mathbb{E}(Y)$, der hier gerade verschwindet, ist eine eigene interessante Größe:
Er heißt *Kovarianz* von $X$ und $Y$ und misst, wie stark die beiden Variablen linear zusammenhängen.
Im Kapitel [Kovarianz](kovarianz.md) nehmen wir ihn genauer unter die Lupe und beweisen die Regel dort noch einmal
in der allgemeinen Fassung, ohne die Voraussetzung der Unabhängigkeit.

Regel (2) ist der Grund dafür, dass sich die Varianz einer Summe unabhängiger Wiederholungen desselben Experiments
so einfach ausrechnen lässt — das nutzen wir im Kapitel
[Wichtigste diskrete Verteilungen](wichtigste-diskrete-verteilungen.ipynb)
bei der Binomialverteilung.
