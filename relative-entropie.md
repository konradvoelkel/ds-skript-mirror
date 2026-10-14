---
title: "Relative Entropie und Kullback-Leibler-Divergenz"
short_title: "Relative Entropie"
description: "Warum in der Informationstheorie der Logarithmus auftaucht, Definition und Eigenschaften der relativen Entropie, dazu Verbundentropie und stetige Entropie."
---

[Vorlesungsaufzeichnung Relative und stetige Entropie](https://media.hhu.de/channel/video/data-science-vl-22-relative-und-stetige-entropie/5dcf4a4c1f44569d78493f65d76a735f/167)

## Logarithmen

Die elementaren Eigenschaften des Logarithmus — Definition, Basiswechsel, bit und nat — stehen im Einschub im Kapitel [Erwartungswert und Varianz](erwartungswert.md). Hier geht es um die Frage, warum in der Informationstheorie ausgerechnet der Logarithmus auftaucht und keine andere Funktion.

:::{admonition} Lemma
Sei $l \colon \{1,\dots\} = \mathbb{N}_{>0} \to \mathbb{R}$ eine Funktion mit
1. $l(ab) = l(a) + l(b)$ -- "vollständig additiv"
2. $l(n+1) \geq l(n)$ -- "monoton wachsend"
Dann existiert eine Konstante $c \in \mathbb{R}$ sodass $l(n) = c \ln(n)$.
:::

:::{admonition} Bemerkung
Aufgrund der Formel

$$
\ln(x) = \dfrac{\log_a(x)}{\log_a(e)}
$$

können wir die Konstante $c$ interpretieren als $c = \log_a(e)$,
d.h. die Funktion $l$ ist ein Logarithmus zur Basis $a$.
:::

Es ist auch gleich klar, dass das gleiche Lemma für $\log_2$ anstelle von $\ln$ gilt (lediglich die Konstante ist eine andere).

Wenn wir also etwas abzählen wollen, sodass der Zählwert eines Produkts die Summe der einzelnen Zählwerte ist, dann müssen wir das mit einem Logarithmus tun.

:::{admonition} Beweis
Wir wollen zeigen, dass für Funktionen $f,g \colon \mathbb{N}_{>0} \to \mathbb{R}$, die die Bedingungen aus dem Lemma erfüllen, stets

$$
f(n) g(2) = f(2) g(n)
$$

gilt, denn mit $g = \ln$ ist dann das Lemma bewiesen ($c=f(2)$).

Seien $n,k,m \in \mathbb{N}$ sodass $2^{m-1} \leq n^k \leq 2^m$.
Aus der Monotonie folgt dann

$$
f(2^{m-1}) \leq f(n^k) \leq f(2^m)
$$

und aus der Additivität

$$
(m-1)f(2) \leq kf(n) \leq mf(2)
$$

ebenso die gleiche Ungleichungskette für $g$ anstelle $f$, aber das multiplizieren wir noch mit $-1$:

$$
-mg(2) \leq -kg(n) \leq -(m-1)g(2).
$$

Die Summe dieser beiden Ungleichungsketten können wir nun vereinfachen zu

$$
-f(2)g(2) \leq k\left(f(n)g(2) - f(2)g(n)\right) \leq f(2)g(2)
$$

teilen wir durch $k$, und lassen dann $k \to \infty$ gehen, so sehen wir,
dass $f(n)g(2) - f(2)g(n) \to 0$ geht (für $k \to \infty$, wovon es gar nicht abhängt).
:::

:::{admonition} Lemma
Wenn eine stetige Funktion $F \colon \mathbb{R} \to \mathbb{R}$ die Funktionalgleichung $F(xy) = xF(y) + F(x)y$ erfüllt und $F(x)/x$ monoton wachsend ist, so existiert eine Konstante $c \in \mathbb{R}$ sodass $F(x) = -x\log(x)c$.
:::

:::{admonition} Beweis
Die Funktion $g(x) := F(x)/x$ erfüllt $g(xy) = g(x) + g(y)$ und ist nach Voraussetzung monoton, also gibt es $c'$ mit $g(x) = c'\log(x)$, und $c:=-c'$ funktioniert.
:::

:::{admonition} Bemerkung
Wir sehen also, dass der Entropie-Beitrag $-p\log(p)$ eines Ergebnisses mit Wahrscheinlichkeit $p$ eine sehr natürliche Größe ist. (Die *Information* $I(x) = -\log P(\{x\})$ aus dem Kapitel [Erwartungswert und Varianz](erwartungswert.md) ist der Faktor hinter dem $p$.)
:::

:::{admonition} Lemma
Der Logarithmus ist eine *konkave* Funktion, d.h. für eine Konvexkombination $\lambda x + \mu y$ (d.h. $\lambda + \mu = 1$ und $0 \leq \lambda, \mu \leq 1$) gilt

$$
\lambda \log(x) + \mu \log(y) \leq \log(\lambda x + \mu y)
$$
:::

:::{admonition} Beweis
**Idee:**
Die Ableitung von $\log(x)$ ist $\frac{1}{x}$ und das ist auf $(0,\infty)$ streng monoton fallend. Mit dem Mittelwertsatz kann man nun zeigen, dass $\log(x)$ streng konkav sein muss (also sogar $<$ statt $\leq$ in der Ungleichung oben).
:::

Wir haben vorher schon ein heuristisches Argument verwendet, aber nun können wir rigoros zeigen:

:::{admonition} Proposition
Wenn $p = (p_1,\dots,p_n)$ eine diskrete Verteilung auf $\Omega = \{1,\dots,n\}$ beschreibt, so gilt für die Entropie
$H(p) \leq \log(n)$ (die Entropie der Gleichverteilung).
:::

:::{admonition} Beweis
Wir nutzen aus, dass die Summe in der Definition der Entropie eine Konvexkombination ist, und dass der Logarithmus konkav ist:

$H(p) = \sum_{i=1, p_i\neq 0}^n p_i \log \frac{1}{p_i} $

$\leq \log \left( \sum_{i=1, p_i\neq 0}^n p_i \frac{1}{p_i} \right)$

$\leq \log\left( \sum_{i=1}^n 1 \right) = \log(n)$
:::


## Definition und Eigenschaften

:::{admonition} Definition
Seien $p,r \in \Delta_n$ (der Menge der Wahrscheinlichkeitsvektoren in $\mathbb{R}^n$, also Vektoren, deren Einträge zwischen $0$ und $1$ liegen und deren Summe über alle Einträge genau $1$ ist).
Die *Entropie* (auch: Kullback-Leibler-Divergenz $D_{KL}$) von $p$ relativ zu $r$ ist

$H(p \Vert r) := \sum_{i,\ p_i > 0}^n p_i \log \left( \frac{p_i}{r_i} \right) \in \mathbb{R} \cup \{\infty\}.$
:::

:::{admonition} Proposition
Schreibe $u_n = (\frac{1}{n}, \dots, \frac{1}{n}) \in \Delta_n$ für die Gleichverteilung auf $\{1,\dots,n\}$.
Dann ist

$$
H(p \Vert u_n) = H(u_n) - H(p) = \log(n) - H(p)
$$
:::

:::{admonition} Proposition
$$
H(p \Vert r) = 0 \text{ genau dann wenn } p=r
$$
(ohne Beweis)
:::

:::{admonition} Proposition
$$
H(p \Vert r) \geq 0
$$
:::

:::{admonition} Beweis
$H(p \Vert r) = \sum p_i \log \left( \dfrac{p_i}{r_i} \right) = -\sum p_i \log \left( \dfrac{r_i}{p_i} \right)$ (wegen $\log(a/b) = -\log(b/a)$)
$\geq - \log \left( \sum p_i \dfrac{r_i}{p_i} \right) \geq - \log \left( \sum r_i \right) = -\log 1 = 0$

dabei haben wir wieder die Konkavität des Logarithmus ausgenutzt.
:::

:::{admonition} Beispiel
Die relative Entropie ist nicht symmetrisch und kann unendlich groß werden. Sei $p_t := (t,\ 1-t)$ für $0 < t < 1$, eine Münze, die für kleines $t$ fast sicher auf $1$ fällt. In der einen Richtung ist

$$
H\left(u_2 \,\Vert\, p_t\right) = \frac{1}{2} \log \frac{1}{2t} + \frac{1}{2}\log \frac{1}{2(1-t)} \xrightarrow{t \to 0} \infty,
$$

denn der erste Summand wächst wie $-\frac12\log t$ über alle Grenzen. In der anderen Richtung liefert die Proposition oben

$$
H\left(p_t \,\Vert\, u_2\right) = \log(2) - H(p_t), \qquad H(p_t) = -t\log t - (1-t)\log(1-t) \xrightarrow{t \to 0} 0,
$$

also $H(p_t \Vert u_2) \to \log 2$: endlich, zur Basis $2$ genau ein Bit. Wer die fast sichere Münze $p_t$ für fair hält, zahlt höchstens ein Bit; wer umgekehrt die faire Münze für $p_t$ hält, wird von der Seite, die er für unmöglich hielt, unendlich überrascht.
:::

## Verbundentropie

:::{admonition} Definition
Die *Verbundentropie* von zwei diskreten Zufallsvariablen $X,Y$ ist

$$
H(X,Y) := \mathbb{E} I_{X,Y} = -\sum_{i=1}^n \sum_{j=1}^n P(X = z_i, Y=z_j) \log P(X=z_i, Y=z_j)
$$
:::

:::{admonition} Proposition
$$
H(X) + H(Y) \geq H(X,Y) \geq \max\left( H(X), H(Y) \right)
$$
:::

:::{admonition} Beispiel
$$
H(X,X) = H(X)
$$

denn in der Summe für den linken Ausdruck sind alle Summanden außerhalb der Diagonalen $0$.
:::

:::{admonition} Proposition
Wenn $X, Y$ unabhängige Zufallsvariablen sind, dann ist $H(X, Y) = H(X) + H(Y)$.
:::

:::{admonition} Beweis
Die Unabhängigkeit bedeutet für alle $i,j$:

$$
P(X = z_i, Y = z_j) = P(X = z_i)\cdot P(Y = z_j)
$$

das Logarithmieren wir:

$$
\log P(X = z_i, Y = z_j) = \log P(X = z_i) + \log P(Y = z_j)
$$

also haben wir insgesamt

\begin{align}
H(X,Y) &:= -\sum_{i=1}^n \sum_{j=1}^n P(X = z_i, Y = z_j) \log P(X = z_i, Y = z_j) \\
 &= -\sum_{i=1}^n \sum_{j=1}^n P(X = z_i)P(Y = z_j) \left( \log P(X = z_i) + \log P(Y = z_j) \right) \\
 &= -\sum_{i=1}^n \sum_{j=1}^n P(X = z_i)P(Y = z_j)\log P(X = z_i)\\
 &\phantom{=}\ \ -\sum_{i=1}^n \sum_{j=1}^n P(X = z_i)P(Y = z_j)\log P(Y = z_j) \\
 &= -\sum_{i=1}^n P(X = z_i)\log P(X = z_i)\\
 &\phantom{=}\ \ -\sum_{j=1}^n P(Y = z_j)\log P(Y = z_j) \\
 &= H(X) + H(Y)
\end{align}
:::

:::{admonition} Definition
Die *gemeinsame Information* (auch *Transinformation*, englisch *mutual information*) von zwei Zufallsvariablen $X,Y$ ist definiert als

$$
I(X;Y) := H(X)+H(Y)-H(X,Y)= H(X,Y  \Vert X\times Y)
$$

Hier steht $H(\cdot \Vert \cdot)$ für die relative Entropie der *Verteilung* von $(X,Y)$ zur Produktverteilung $P_X \times P_Y$, also der Verteilung, die $(X,Y)$ hätte, wenn $X$ und $Y$ unabhängig wären.

Ein sehr häufiger Anwendungsfall der gemeinsamen Information liegt im Clustering:
Wenn man zu einem Datensatz mit einer Methode der Wahl zu Clustern gekommen ist,
also eine geschätzte Klassenzugehörigkeit (etwa $1,2$ oder $3$ als Label),
und für einen Teildatensatz (zum Testen) von Hand eine Klasseneinteilung vorgenommen wurde,
können wir von diesen Klassenvariablen die gemeinsame Information berechnen um zu quantifizieren, wie gut die Klassenbildung auf dem Testdatensatz funktionierte.
Von Vorteil ist dabei, dass die konkreten Label nicht mehr relevant sind
(d.h. die Methode ist invariant unter Permutation der Klassenbezeichnungen).

Die *bedingte Entropie* von $X$ bedingt auf $Y$ ist definiert als

$$
H(X|Y) := H(X) - I(X;Y)
$$
:::

:::{admonition} Beispiel
Die gemeinsame Information von $X$ mit sich selbst ist genau die Entropie $I(X;X) = H(X)$.

Wenn $X,Y$ unabhängig sind, ist $I(X;Y) = H(X) + H(Y) - (H(X) + H(Y)) = 0$.
:::

:::{admonition} Proposition
$$
H(X|Y) = H(X,Y) - H(Y)
$$

und wenn $X,Y$ unabhängig sind, ist $H(X|Y) = H(X)$.
:::


:::{admonition} Satz
**Entropischer Satz von Bayes**

$$
H(X|Y) = H(Y|X) + H(X) - H(Y)
$$
:::

:::{admonition} Beispiel
Wenn $X$ vollständig von $Y$ abhängt (z.B. $Y$ ein Würfelwurf und $X = f(Y)$ mit $f = \mod 2$),
dann ist $H(X,Y) = H(Y)$ und $H(X|Y) = 0$.
:::

```{figure} images/1920px-Entropy-mutual-information-relative-entropy-relation-diagram.svg.png
:width: 480px
:align: center
:name: entropy-diagram

Entropie, bedingte Entropie, Verbundentropie und gemeinsame Information in einem Venn-Diagramm. Abbildung: [Wikimedia Commons, Benutzer KonradVoelkel](https://commons.wikimedia.org/wiki/File:Entropy-mutual-information-relative-entropy-relation-diagram.svg) (2010, gemeinfrei).
```


:::{admonition} Definition
Die *Kreuzentropie* von $X$ (verteilt nach $p \in \Delta_n$) und $Y$ (verteilt nach $r \in \Delta_n$) ist

$$
H(X; Y) = \mathbb{E}_X I(Y) = -\sum_{i,\ p_i > 0}^n p_i \log r_i \in \mathbb{R} \cup \{\infty\}.
$$
:::

Ein Summand mit $p_i > 0$ und $r_i = 0$ hat dabei den Wert $\infty$ (mit $\log 0 = -\infty$): Ein Ereignis, das nach $r$ unmöglich ist, aber nach $p$ vorkommt, kostet unendlich viel.

*Achtung*: Leider wird die Kreuzentropie von manchen Autoren auch mit $H(X, Y)$ notiert, was man also leicht mit der Verbundentropie verwechseln kann. Außerdem ähnelt die Notation $H(X;Y)$ der gemeinsamen Information $I(X;Y)$ von oben, die etwas ganz anderes ist.

:::{admonition} Proposition
$$
H(X; Y) = H(X) + H(X \Vert Y)
$$
:::

Wenn man $X$ festhält und $Y$ variiert, ist es das gleiche, ob man $H(X;Y)$ oder $H(X \Vert Y)$ minimiert, daher wird im maschinellen Lernen häufig das eine mit dem anderen substituiert. Die Maximum-Likelihood-Methode kann man auffassen als Minimierung einer Kreuzentropie und damit als Minimierung der relativen Entropie. Das erklärt, wie und wieso Entropie für maschinelles Lernen relevant ist.

:::{admonition} Bemerkung
Im Deep Learning begegnet man dieser Beobachtung unter drei Namen: *negative log-likelihood*, *Kreuzentropie* und *KL-Divergenz zu den Labels* bezeichnen dort dieselbe Loss-Funktion für Klassifikationsprobleme. Der Unterschied zwischen den letzten beiden ist nur die Konstante $H(X)$ aus der Proposition oben, die von den Modellparametern nicht abhängt. Die Vorlesung *Einführung in Deep Learning* setzt diesen Zusammenhang als bekannt voraus.
:::

Ansonsten ist die Kreuzentropie eine in der Theorie deutlich seltener verwendete Größe als die relative Entropie (die meist Kullback-Leibler-Divergenz $D_{KL}$ genannt wird).

## Stetige Entropie

:::{note}
Dieses Unterkapitel ist nicht klausurrelevant und greift auf Maßtheorie vor (Radon-Nikodym-Ableitung, invariante Maße), die wir im Kurs nicht behandeln. Beim ersten Lesen genügt es, die Kernaussage mitzunehmen: Im Stetigen ist Entropie nur *relativ* zu einem Bezugsmaß sinnvoll definiert, die relative Entropie ist also der eigentlich grundlegende Begriff.
:::

Man könnte meinen, dass sich die Formel $H(p) = -\sum p_i \log p_i$ verallgemeinert zu $H(P) = -\int \log P dP$, aber das ergibt so keinen Sinn. Man kann aber das folgende tun:

:::{admonition} Definition
Sei $P$ eine stetige Verteilung mit Dichtefunktion $f$, die auf einer Menge $\Omega \subseteq \mathbb{R}^n$ definiert ist.
Dann heißt

$$
h(X) := \mathbb{E}\left( -\log(f(X)) \right) = - \int_\Omega f(x) \log f(x) dx
$$

die *differentielle Entropie* von $X$ (definiert ebenfalls von Claude Shannon).
:::

Sie erfüllt bereits einige schöne Eigenschaften, die wir uns von einer stetigen Entropie vorstellen, z.B. Translationsinvarianz: $h(X) = h(X - v)$ für einen Vektor $v \in \mathbb{R}^n$.

Leider ist die differentielle Entropie nicht invariant unter beliebigen Transformationen, auch nicht Isomorphismen.

Jaynes hat vorgeschlagen, sich immer feiner werdende Histogramme vorzustellen, also eine Menge von $N$ diskreten Punkten $\{x_i\}$,
dann schreiben wir
$M(a,b) = \lim_{N \to \infty} \frac{1}{N} (\text{Anzahl } x_i : a < x_i < b)$
und eine Dichte $m$ mit $M(a,b) = \int_a^b m(x) dx$ nennen wir *invariantes Maß*.
Damit schreiben wir nun

$$
\lim_{N \to \infty} \log(N) - \int p(x) \log \dfrac{p(x)}{m(x)} dx
$$

aber weil $\lim_{N \to \infty} \log(N) = \infty$ ist, lassen wir den Teil einfach frech weg, und erhalten so eine Größe, die sich ähnlich wie $h(x)$ verhält, aber skaleninvariant ist:

$$
H(X) := - \int p(x) \log \dfrac{p(x)}{m(x)} dx
$$

Zum Einen wollen wir festhalten, dass die "diskrete Entropie" einer stetigen Verteilung eigentlich $\infty$ ist.
Zum Anderen, dass offensichtlich für einen sinnvollen Entropiebegriff zwangsläufig Bezug genommen werden muss auf eine weitere Verteilung (hier das "invariante Maß").

Wenn man vom theoretischen Standpunkt analysiert, was $h(X)$ und $H(X)$ sind, so kommt man zur allgemeinen relativen Entropie $H(P,Q)$, sodass $h(X) = -H(f\lambda \,\Vert\, \lambda)$ mit $\lambda$ dem Lebesgue-Maß und $f$ einer Dichte von $X$.

:::{admonition} Definition
Seien $P,R$ stetige Verteilungen. Die *relative Entropie* $H(P \Vert R)$ (auch: Kullback-Leibler-Divergenz $D_{KL}(P,R)$) ist

$$
H(P \Vert R) := - \int_\Omega \log \left( \dfrac{dR}{dP} \right) dP
$$

dabei ist $\dfrac{dR}{dP}$ die Radon-Nikodym-Ableitung eines Maßes bezüglich eines anderen.
:::

Das wollen wir jetzt auch nicht weiter diskutieren, sondern lieber festhalten, dass das für $P$ und $R$ mit Dichtefunktionen $p,r \colon \mathbb{R}^n \to [0,\infty)$ einfacher aussieht:

$$
H(P \Vert R) = \int_\Omega p(x) \log \frac{p(x)}{r(x)} dx
$$

Diesen Ausdruck wiederum dürfen wir (wenn die Dichtefunktionen hinreichend freundlich sind) über Riemann-Summen ausrechnen.
Wenn z.B. $n=1$ und $\Omega = \mathbb{R}$, dann können wir

$H(P \Vert R) = \int_{\mathbb{R}} p(x) \log \dfrac{p(x)}{r(x)} dx$
$= \sum_{k = -\infty}^{\infty} \int_{k}^{k+1} p(x) \log \dfrac{p(x)}{r(x)}dx$

betrachten und die Integralterme rechts durch Werte abschätzen, um so $H(P \Vert R)$ abzuschätzen. 

$$
H(P \Vert R) \approx \sum_{k = -\infty}^{\infty} p(k) \log \dfrac{p(k)}{r(k)}
$$

Die Unterteilung in Intervalle der Länge $1$ können wir natürlich beliebig feiner wählen, um die Approximation beliebig genau zu bekommen. Das Ersetzen einer stetigen Verteilung durch eine solche diskrete Verteilung ist analog der Bildung eines Histogramms.

Wenn Sie noch Zweifel daran haben, welche Relevanz die abstrakte Informationstheorie für die praktische Arbeit von Data Scientists und Machine Learning Entwicklern haben soll, ist eine [Reise in die Wikipedia-Seite zu Anwendungen der gemeinsamen Information bzw. bedingter Entropie](https://en.wikipedia.org/wiki/Mutual_information#Applications_2) ratsam.