# Stetige Verteilungen

[Vorlesungsaufzeichnung Stetige Verteilungen](https://media.hhu.de/channel/video/data-science-vl-7-stetige-verteilungen-2024/1c1abcd6741c7c428fb6aa67827a06a3/167)

:::{admonition} Definition
Sei $X \colon \Omega \to \mathbb{R}$ eine Zufallsvariable, d.h. $\Omega$ ein Wahrscheinlichkeitsraum (eine Menge $\Omega$ zusammen mit einem Wahrscheinlichkeitsmaß $P_\Omega$) und $X$ eine Abbildung, sodass $P(X \in A) := P_\Omega(X^{-1}(A))$ für alle Ereignisse $A \subseteq \mathbb{R}$ definiert ist.

Wenn $\Omega$ kein diskreter Wahrscheinlichkeitsraum ist (z.B. weil $\Omega$ eine überabzählbar unendliche Menge ist, etwa $\Omega = \mathbb{R}^n$), und $X$ überabzählbar viele mögliche Werte annimmt, und wenn die Verteilung von $X$ eine *Dichte* besitzt (das definieren wir im nächsten Abschnitt), nennen wir $X$ eine *stetige Zufallsvariable*. Eine Zufallsvariable mit überabzählbar vielen Werten, aber ohne Dichte (etwa eine Mischung aus einer Dirac- und einer Normalverteilung), ist also weder diskret noch stetig.
:::

:::{admonition} Definition
Man nennt die kleinste Menge $A \subset \mathbb{R}$ mit $P(X \in A)=1$ den *Träger* von $X$ und schreibt auch

$$
\operatorname{supp}(X) = \overline{\bigcap \{ A \subseteq \mathbb{R} : P(X \in A) = 1 \}}
$$
:::

Der Träger ist auch für diskrete reelle Zufallsvariablen definiert - der offensichtliche Unterschied ist, dass per definitionem diskrete Zufallsvariablen einen diskreten Träger haben (d.h. eine Menge reeller Zahlen, die keinen Häufungspunkt hat, insbesondere kein Intervall enthält).

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
\int_{X^{-1}(A)} d\omega = P(X \in A) = P_X(A) = \int_A f(x) dx
$$

Dieses rechte Integral ist nun ein Integral im Wertebereich von $X$.
Analog können wir auch den Erwartungswert und die Varianz berechnen:

$$
\mathbb{E}(X) = \int_\Omega X(\omega) d \omega = \int_{\mathbb{R}} x f(x) dx = \int_{-\infty}^{\infty} xf(x) dx
$$

$$
\begin{aligned}
\mathbb{V}(X) &= \int_\Omega \left(X(\omega)-\mathbb{E}(X)\right)^2 d \omega \\
              &= \int_{-\infty}^{\infty} \left(x-\mathbb{E}(X)\right)^2 f(x) dx \\
              &= \int_{-\infty}^{\infty} x^2f(x) dx  - {\left( \mathbb{E}(X) \right)}^2.
\end{aligned}
$$

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

:::{admonition} Beispiel
Nicht jedes Wahrscheinlichkeitsmaß erlaubt eine Darstellung mit einer Dichte:
Betrachte auf $\mathbb{R}$ die Verteilung mit

$$
P(A) = \begin{cases} 1 & \text{ wenn } 0 \in A \\ 0 & \text{ sonst} \end{cases}
$$

Diese Verteilung heißt *Dirac-Verteilung* mit Masse bei $0$. Wenn man sich sehr viel Mühe gibt, so etwas ähnliches wie eine Dichte zu basteln, so muss man zur Theorie der Distributionen aus der Funktionalanalysis greifen (Physiker\*innen kennen das). Es gibt auch Verteilungen, da genügt auch keine Distribution.
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
F(x) = \int_{-\infty}^x f(x)dx.
$$
:::
