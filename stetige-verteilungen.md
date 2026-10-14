---
title: "Stetige Verteilungen und Dichtefunktionen"
short_title: "Stetige Verteilungen"
description: "Von der Wahrscheinlichkeitsmassefunktion zur Dichte: warum einzelne Punkte Nullmengen sind, was eine Dichtefunktion leistet und wie sie mit der Verteilungsfunktion zusammenhängt."
---

[Vorlesungsaufzeichnung Stetige Verteilungen](https://media.hhu.de/channel/video/data-science-vl-7-stetige-verteilungen-2024/1c1abcd6741c7c428fb6aa67827a06a3/167)

:::{admonition} Definition
Sei $X \colon \Omega \to \mathbb{R}$ eine Zufallsvariable, d.h. $\Omega$ ein Wahrscheinlichkeitsraum (eine Menge $\Omega$ zusammen mit einem Wahrscheinlichkeitsmaß $P_\Omega$) und $X$ eine Abbildung, sodass $P(X \in A) := P_\Omega(X^{-1}(A))$ für alle Ereignisse $A \subseteq \mathbb{R}$ definiert ist.

Wenn $\Omega$ kein diskreter Wahrscheinlichkeitsraum ist (z.B. weil $\Omega$ eine überabzählbar unendliche Menge ist, etwa $\Omega = \mathbb{R}^n$), und $X$ überabzählbar viele mögliche Werte annimmt, und wenn die Verteilung von $X$ eine *Dichte* besitzt (das definieren wir im nächsten Abschnitt), nennen wir $X$ eine *stetige Zufallsvariable*. Eine Zufallsvariable mit überabzählbar vielen Werten, aber ohne Dichte (etwa eine Mischung aus einer Dirac- und einer Normalverteilung), ist also weder diskret noch stetig.
:::

:::{admonition} Definition
Der *Träger* von $X$ ist die kleinste **abgeschlossene** Menge $A \subseteq \mathbb{R}$ mit $P(X \in A) = 1$,

$$
\operatorname{supp}(X) = \bigcap \{ A \subseteq \mathbb{R} \text{ abgeschlossen} : P(X \in A) = 1 \}.
$$
:::

Das Wort *abgeschlossen* ist dabei keine Dekoration. Ohne es wäre der Schnitt für jede Verteilung mit Dichte leer: Für $X \sim U([0,1])$ hat $[0,1] \setminus \{x\}$ für jedes einzelne $x$ noch Wahrscheinlichkeit $1$ (einzelne Punkte sind Nullmengen, dazu gleich mehr), also läge kein Punkt in allen diesen Mengen. Verlangt man abgeschlossene Mengen, kommt $[0,1]$ heraus, wie es sein soll. (Dass der Schnitt selbst wieder Wahrscheinlichkeit $1$ hat, weil man mit abzählbar vielen der $A$ auskommt, benutzen wir nicht weiter.)

:::{admonition} Definition
Eine Menge $M \subseteq \mathbb{R}^n$ heißt *abgeschlossen*, wenn sie die Grenzwerte ihrer eigenen konvergenten Folgen enthält: Liegt eine Folge $(x_k)$ ganz in $M$ und konvergiert gegen $x$, so ist auch $x \in M$.
:::

Abgeschlossen sind zum Beispiel jedes Intervall der Form $[a,b]$, ganz $\mathbb{R}$ und jede endliche Menge. Nicht abgeschlossen ist dagegen $(0,1]$: Die Folge $\frac1k$ liegt darin, ihr Grenzwert $0$ nicht. Der Abschluss von $(0,1]$ ist $[0,1]$.

Für eine diskrete Verteilung mit pmf $p$ und endlich vielen Werten vereinfacht sich der Träger zu

$$
\operatorname{supp}(X) = \{\, x \ \mid\ p(x) > 0 \,\},
$$

also zu der Menge der Werte, die überhaupt vorkommen können (bei unendlich vielen Werten kommen noch deren Häufungspunkte dazu, denn der Träger ist abgeschlossen).

:::{admonition} Beispiel
Die Gleichverteilung auf $\Omega = \{1,\dots,n\}$ hat als Verteilung *auf $\Omega$* den Träger $\Omega$ selbst — dort ist jedes Element möglich.

Dieselbe Verteilung lässt sich aber auch als Verteilung auf $\mathbb{R}$ auffassen, indem man alle übrigen reellen Zahlen mit Wahrscheinlichkeit $0$ versieht. Dann ist der Träger $\{1,\dots,n\} \subset \mathbb{R}$, eine endliche und damit abgeschlossene Teilmenge der reellen Zahlen. Der Träger hängt also nicht nur von der Verteilung ab, sondern auch davon, als Verteilung *worauf* man sie liest.
:::

Der Träger ist auch für diskrete reelle Zufallsvariablen definiert - der offensichtliche Unterschied ist, dass der Träger einer diskreten Zufallsvariable kein Intervall enthält.

## Dichtefunktionen

:::{admonition} Definition
Sei $D \subseteq \mathbb{R}^n$ und $f \colon D \to [0,\infty)$ eine integrierbare Funktion (bezüglich des Lebesgue-Maßes auf $\mathbb{R}^n$, Riemann-integrierbar ist ein hinreichendes Kriterium) mit $\int_D f(x) dx = 1$. Dann ist auf $D$ ein Wahrscheinlichkeitsmaß definiert durch:

$$
\text{für } A \subseteq D \text{ Ereignis } P(A) := \int_A f(x) dx
$$

Wir nennen für jedes Wahrscheinlichkeitsmaß $P$, welches sich so schreiben lässt, die Funktion $f$ eine *Wahrscheinlichkeitsdichtefunktion* (probability density function, pdf) oder kurz *Dichte* (nicht zu verwechseln mit der Wahrscheinlichkeitsmassefunktion, pmf, aus dem diskreten Fall).
:::

Gegeben eine reelle Zufallsvariable $X \colon \Omega \to \mathbb{R}$, deren Verteilung $P_X$ durch eine Dichte $f$ gegeben ist, gilt also für $A \subseteq \mathbb{R}$

$$
\int_{X^{-1}(A)} dP(\omega) = P(X \in A) = P_X(A) = \int_A f(x) dx
$$

Dieses rechte Integral ist nun ein Integral im Wertebereich von $X$.
Analog können wir auch den Erwartungswert und die Varianz berechnen:

:::{admonition} Definition
Sei $X$ eine stetige Zufallsvariable, deren Verteilung durch eine Dichte $f \colon D \to [0,\infty)$ gegeben ist. Dann heißt

$$
\mathbb{E}(X) = \int_\Omega X(\omega)\, dP(\omega) = \int_D x f(x) dx
$$

der *Erwartungswert* von $X$ und

$$
\mathbb{V}(X) = \int_\Omega \left(X(\omega)-\mathbb{E}(X)\right)^2 dP(\omega) = \int_D \left(x-\mathbb{E}(X)\right)^2 f(x) dx
$$

die *Varianz* von $X$, sofern diese Integrale existieren. Für $D = \mathbb{R}$ ist etwa $\mathbb{E}(X) = \int_{-\infty}^{\infty} x f(x) dx$.
:::

Das ist das stetige Gegenstück zur Summe über die Wahrscheinlichkeitsmassefunktion im Kapitel [Erwartungswert und Varianz](erwartungswert.md): An die Stelle der pmf tritt die Dichte, an die Stelle der Summe das Integral. Dass wir auch andere Funktionen von $X$ auf diese Weise integrieren dürfen, sagt der folgende Satz.

:::{admonition} Satz (Transformationsformel)
Sei $X$ eine stetige Zufallsvariable mit Dichte $f \colon D \to [0,\infty)$ und $g \colon D \to \mathbb{R}$ eine (messbare) Funktion. Dann ist

$$
\mathbb{E}(g(X)) = \int_D g(x) f(x) dx,
$$

sofern das Integral existiert. Für eine diskrete Zufallsvariable mit pmf $p$ lautet dieselbe Aussage $\mathbb{E}(g(X)) = \sum_x g(x)\, p(x)$.
:::

Wir beweisen den Satz nicht (er folgt aus dem Transformationssatz für Integrale), benutzen ihn aber ständig: Die Definition der Varianz ist gerade der Spezialfall $g(x) = (x - \mathbb{E}(X))^2$, und mit $g(x) = x^2$ erhalten wir wie im diskreten Fall

$$
\mathbb{V}(X) = \mathbb{E}(X^2) - {\left( \mathbb{E}(X) \right)}^2 = \int_D x^2 f(x) dx - {\left( \mathbb{E}(X) \right)}^2.
$$

Allgemein heißt $\mathbb{E}(X^k) = \int_D x^k f(x) dx$ das *$k$-te Moment* von $X$.

:::{admonition} Beispiel
Seien $a < b \in \mathbb{R}$. Mit $D = \mathbb{R}$ und $f \colon \mathbb{R} \to [0,\infty)$ gegeben durch

$$
f(x) = \begin{cases} \frac{1}{b-a}, & \text{ wenn } x \in [a,b] \\ 0 & \text{ sonst} \end{cases}
$$

ist ein Wahrscheinlichkeitsmaß auf $\mathbb{R}$ definiert, die *stetige Gleichverteilung* auf dem Intervall $[a,b]$.
Sei $X$ eine Zufallsvariable mit dieser Verteilung, wir schreiben $X \sim U([a,b])$.
Der Erwartungswert (wir nutzen $\int x dx = \frac{x^2}{2}$) ist $\mathbb{E}(X) =$

$$
\int_{-\infty}^{\infty} xf(x) dx = \int_a^b \frac{xdx}{b-a} = \frac{1}{b-a} \left[\frac{x^2}{2}\right]_a^b = \frac{b^2 -a^2}{2(b-a)} = \frac{(b+a)(b-a)}{2(b-a)} = \frac{a+b}{2}
$$

Das zweite Moment ist

$$
\mathbb{E}(X^2) = \int_{-\infty}^\infty x^2 f(x)dx = \left[ \frac{x^3}{3(b-a)} \right]_a^b = \frac{b^3-a^3}{3(b-a)} = \frac{a^2+ab+b^2}{3}
$$

Die Varianz ist

$$
\mathbb{V}(X) = \mathbb{E}(X^2) - {\left(\mathbb{E}(X)\right)}^2 =  \frac{a^2+ab+b^2}{3} - \frac{(a+b)^2}{4} = \frac{(a-b)^2}{12}
$$
:::

:::{admonition} Bemerkung
**Nullmengen.** Für $X \sim U([a,b])$ und $a \leq c < d \leq b$ ist $P(c \leq X \leq d) = \int_c^d \frac{dx}{b-a} = \frac{d-c}{b-a}$, und dasselbe Integral ergibt sich für $P(c < X < d)$, $P(c \leq X < d)$ und $P(c < X \leq d)$: Ob die Intervallgrenzen dazugehören oder nicht, ändert am Integral nichts. Insbesondere ist $P(X = c) = \int_c^c f(x) dx = 0$ für jeden einzelnen Punkt $c$, obwohl $f(c) = \frac{1}{b-a} \neq 0$ ist.

Das gilt für jede Verteilung mit Dichte: Einzelne Punkte haben Wahrscheinlichkeit $0$, wegen der endlichen Additivität also auch jede endliche Menge, und wegen der $\sigma$-Additivität aus dem Kapitel [Herleitung des mathematischen Formalismus der Stochastik](intro-stochastik.md) auch jede abzählbare Menge $A = \{a_1, a_2, \dots\}$, denn $P(X \in A) = \sum_{i} P(X = a_i) = 0$. Mengen mit Wahrscheinlichkeit $0$ nennt man *Nullmengen*. Ändert man eine Dichte $f$ auf einer Nullmenge ab (etwa an endlich vielen Stellen), so ändert sich kein einziges Integral $\int_A f(x) dx$, also auch nicht das zugehörige Wahrscheinlichkeitsmaß.
:::

:::{admonition} Beispiel
Die Menge $\mathbb{Q} \cap [0,1]$ der rationalen Zahlen zwischen $0$ und $1$ ist abzählbar, also für $X \sim U([0,1])$ eine Nullmenge: Eine gleichverteilte Zufallszahl aus $[0,1]$ ist mit Wahrscheinlichkeit $1$ irrational. Knobelaufgabe: Gibt es überhaupt eine Verteilung auf $[0,1]$, die jedem einzelnen Punkt positive Wahrscheinlichkeit gibt? (Nein: Für jedes $k$ gibt es höchstens $k$ Punkte mit Wahrscheinlichkeit mindestens $\frac{1}{k}$, also insgesamt höchstens abzählbar viele Punkte mit positiver Wahrscheinlichkeit.)
:::

:::{admonition} Beispiel
Nicht jedes Wahrscheinlichkeitsmaß erlaubt eine Darstellung mit einer Dichte:
Betrachte auf $\mathbb{R}$ die Verteilung mit

$$
P(A) = \begin{cases} 1 & \text{ wenn } 0 \in A \\ 0 & \text{ sonst} \end{cases}
$$

Diese Verteilung heißt *Dirac-Verteilung* mit Masse bei $0$. Eine Dichte $f$ kann es hier nicht geben: Die einpunktige Menge $\{0\}$ ist für jede Dichte eine Nullmenge, es wäre also $\int_{\{0\}} f(x) dx = 0 \neq 1 = P(\{0\})$. Dasselbe Argument trifft jede diskrete Verteilung auf $\mathbb{R}$: Sie konzentriert ihre gesamte Masse $1$ auf ihren abzählbaren Träger, und der ist für jede Dichte eine Nullmenge. Wenn man sich sehr viel Mühe gibt, so etwas ähnliches wie eine Dichte zu basteln, so muss man zur Theorie der Distributionen aus der Funktionalanalysis greifen (Physiker\*innen kennen das). Es gibt auch Verteilungen, da genügt auch keine Distribution.
:::

:::{admonition} Beispiel
Umgekehrt lässt sich aus einer diskreten Verteilung leicht eine stetige bauen. Sei $Y$ eine diskrete Zufallsvariable mit Werten in $\{5,6,7\}$ und $P(Y=5) = \frac{4}{7}$, $P(Y=6) = \frac{2}{7}$, $P(Y=7) = \frac{1}{7}$, und sei $Z \sim U([0,1))$ unabhängig von $Y$ (formal: $\Omega = \{5,6,7\} \times [0,1)$ mit dem Produktmaß, $X(y,z) = y + z$). Dann ist $X := Y + Z$ eine stetige Zufallsvariable mit Werten in $[5,8)$ und Dichte

$$
f(x) = \begin{cases} \frac{4}{7}, & \text{ wenn } x \in [5,6) \\ \frac{2}{7}, & \text{ wenn } x \in [6,7) \\ \frac{1}{7}, & \text{ wenn } x \in [7,8) \\ 0 & \text{ sonst,} \end{cases}
$$

denn für $x \in [5,6)$ ist $P(5 \leq X \leq x) = P(Y = 5) \cdot P(Z \leq x - 5) = \frac{4}{7}(x-5)$, und entsprechend auf den beiden anderen Teilintervallen. Die Dichte integriert sich zu $\frac{4}{7} + \frac{2}{7} + \frac{1}{7} = 1$; welchen Wert $f$ an den Stellen $6$ und $7$ hat, spielt nach der Nullmengen-Bemerkung keine Rolle. Zum Beispiel ist $P(5 \leq X \leq 6) = \int_5^6 f(x) dx = \frac{4}{7}$ und $P(6 \leq X \leq 6{,}5) = \frac{2}{7} \cdot \frac{1}{2} = \frac{1}{7}$. Der Erwartungswert ist

$$
\mathbb{E}(X) = \int_5^8 x f(x) dx = \frac{4}{7} \cdot \frac{11}{2} + \frac{2}{7} \cdot \frac{13}{2} + \frac{1}{7} \cdot \frac{15}{2} = \frac{85}{14} = 6 + \frac{1}{14},
$$

denn auf jedem Teilintervall $[k, k+1)$ ist $\int_k^{k+1} x\, dx = k + \frac{1}{2}$ (dasselbe ergibt $\mathbb{E}(Y) + \mathbb{E}(Z) = \frac{39}{7} + \frac{1}{2}$). Eine solche Verteilung, bei der zuerst eine diskrete Wahl getroffen wird und dann innerhalb der gewählten Klasse eine stetige, nennt man *Mischverteilung*; ein weiteres Beispiel ist die kontaminierte Normalverteilung im Kapitel [Wichtigste stetige Verteilungen](wichtigste-stetige-verteilungen.ipynb), wo auch genau diese Verteilung auf $[5,8)$ simuliert wird.
:::

:::{admonition} Definition
Sei $(\Omega, P)$ ein Wahrscheinlichkeitsraum, dann nennen wir für eine Zufallsvariable $X \colon \Omega \to \mathbb{R}$ die Funktion

$$
F \colon \mathbb{R} \to [0,1],\qquad x \mapsto P(X \leq x)
$$

die *kumulative Wahrscheinlichkeitsverteilungsfunktion* oder auch *Verteilungsfunktion* oder *cdf* (cumulative distribution function). Sie existiert immer, im Gegensatz zur Dichte (pdf).
:::

:::{admonition} Beispiel
Wenn $P_X$ eine Dichte $f \colon \mathbb{R} \to [0,\infty)$ hat,
also $P(a \leq X \leq b) = \int_a^b f(x)dx$, so ist

$$
F(x) = \int_{-\infty}^{x} f(t)dt.
$$

Ob man hier $P(X \leq x)$ oder $P(X < x)$ schreibt, macht nach der Nullmengen-Bemerkung keinen Unterschied; manche Bücher definieren die cdf mit $P(X < x)$, für Verteilungen mit Dichte ist das dieselbe Funktion.
:::

:::{admonition} Satz
Hat $P_X$ eine Dichte $f$, so ist die Verteilungsfunktion $F$ eine Stammfunktion von $f$: Nach dem Hauptsatz der Differential- und Integralrechnung ist $F$ an jeder Stelle $x$, an der $f$ stetig ist, differenzierbar mit $F'(x) = f(x)$. Für jede Zufallsvariable (mit oder ohne Dichte) liefert die cdf außerdem die Wahrscheinlichkeit von Intervallen,

$$
P(a < X \leq b) = F(b) - F(a),
$$

und mit Dichte ist das gerade $\int_a^b f(t)dt$.
:::

Die cdf steigt also genau dort steil an, wo die Dichte groß ist. Im Kapitel [Wichtigste stetige Verteilungen](wichtigste-stetige-verteilungen.ipynb) werden pdf und cdf jeweils gemeinsam geplottet; beobachten Sie das dort.
