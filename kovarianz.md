---
title: "Multivariate Statistik: Kovarianz und Abhängigkeit"
short_title: "Kovarianz und Abhängigkeit"
description: "Gemeinsame Verteilung, Marginalverteilung und der Satz von Bayes, dann die Kovarianz: wie sie sich wie ein Skalarprodukt verhält und warum der Korrelationskoeffizient ein Kosinus ist."
---

[Vorlesungsaufzeichnung Kovarianz und Korrelation (VL 11)](https://media.hhu.de/channel/video/data-science-vl-11-kovarianz-korrelation-2025/92283e63495a6413e5e1b55a17ed31fb/167)

## Gemeinsame Verteilung und Bayes

:::{admonition} Definition
Sind $X \colon \Omega_1 \to \mathbb{R}$ und $Y \colon \Omega_2 \to \mathbb{R}$ zwei Zufallsvariablen, so können wir das **Produkt** bilden:

$$
X \times Y \colon \Omega_1 \times \Omega_2 \to \mathbb{R}^2,\ (a,b) \mapsto (X(a),Y(b)).
$$
:::

:::{admonition} Definition
Wenn $X,Y \colon \Omega \to \mathbb{R}$ zwei Zufallsvariablen mit dem selben Definitionsbereich sind, können wir die **gemeinsame Verteilung** bilden:

$$
(X, Y) := (X \times Y) \circ \Delta \colon \Omega \to \mathbb{R}^2,\ a \mapsto (X(a),Y(a)).
$$

Dabei ist $\Delta \colon \Omega \to \Omega \times \Omega$ die *Diagonalabbildung* $a \mapsto (a,a)$.
:::

:::{admonition} Definition
Zu einer Zufallsvariable $X \colon \Omega \to \mathbb{R}^n$ können wir $X = (X_1,\dots,X_n)$ schreiben mit $X_i \colon \Omega \to \mathbb{R}$ gegeben als $\pi_i \circ X$, wobei $\pi_i \colon \mathbb{R}^n \to \mathbb{R}$ die $i$-te Koordinatenprojektion ist.
Die Verteilungen der $X_i$ heißen **Randverteilungen** oder **Marginalverteilungen** von $X$.
:::

Allgemeiner wird auch z.B. $(X_1,X_3,X_9)$ als Marginalverteilung von $X$ bezeichnet,
oder auch jede Verkettung von $X$ mit einer linearen Projektion $\pi \colon \mathbb{R}^n \to \mathbb{R}^m$, nicht notwendig auf die Koordinaten(hyper)ebene(n) der Standardbasis in $\mathbb{R}^n$.

:::{admonition} Bemerkung
Die Verteilung von $X_i$ ist $P(X_i \in A) = P(X \in \pi_i^{-1}(A))$.

Zu einer Zufallsvariable $(X,Y) \colon \Omega \to \mathbb{R}^2$ können wir die Verteilung von $Y$ berechnen als
$P(Y \in A) = \sum_{x \in X(\Omega)} P((X,Y) \in \{x\} \times A)$ im diskreten Fall (und mit einem entsprechenden Integral im stetigen Fall), wobei wir $\pi_2^{-1}(A) = X(\Omega)\times A$ in disjunkte Teilmengen zerlegt haben.
:::

:::{admonition} Bemerkung
Zu einer Zufallsvariable $(X,Y) \colon \Omega \to \mathbb{R}^2$ ist

$$
P((X,Y) = (x,y)) = P(X = x, Y=y) = P(Y = y | X = x)P(X = x)
$$

nach Definition der bedingten Wahrscheinlichkeit.

In der Notation mit pmf schreiben wir auch

$$
p(x,y) = p(y|x)p(x)
$$

wobei das als Definition zu verstehen ist:

$$
p(y|x) = \frac{p(x,y)}{p(x)}
$$

Genauer schreibt man die Verteilungen mit ihren Zufallsvariablen im Index, wenn mehrere im Spiel sind:

$$
p_{X,Y}(x,y) = p_{Y|X}(y \mid x)\, p_X(x),
$$

wobei $p_{Y|X}(\cdot \mid x)$ für jedes feste $x$ mit $p_X(x) > 0$ die pmf der bedingten Verteilung von $Y$ ist (im stetigen Fall ebenso, mit Dichten statt pmf). Diese Formel heißt **Produktregel**; die **Summenregel** ist die Bemerkung davor, das Aufsummieren über die nicht interessierende Variable.
:::

:::{admonition} Proposition
Seien $X, Y \colon \Omega \to \mathbb{R}$ diskrete Zufallsvariablen. Dann sind äquivalent:

1. $X$ und $Y$ sind unabhängig (im Sinne des Kapitels [Erwartungswert und Varianz](erwartungswert.md), Abschnitt *Unabhängigkeit*);
2. die gemeinsame pmf faktorisiert: $p_{X,Y}(x,y) = p_X(x)\, p_Y(y)$ für alle $x,y$;
3. bedingen ändert nichts: $p_{Y|X}(y \mid x) = p_Y(y)$ für alle $x$ mit $p_X(x) > 0$ und alle $y$.
:::

:::{admonition} Beweis
Die Unabhängigkeit von $X$ und $Y$ bedeutet $P(X = x, Y = y) = P(X = x)\,P(Y = y)$ für alle $x,y$, und das ist wörtlich Aussage 2. Für die Äquivalenz von 2 und 3 setzen wir die Definition $p_{Y|X}(y \mid x) = \frac{p_{X,Y}(x,y)}{p_X(x)}$ ein: Gilt 2, so kürzt sich $p_X(x) > 0$ heraus und es bleibt $p_{Y|X}(y\mid x) = p_Y(y)$. Gilt umgekehrt 3, so ist $p_{X,Y}(x,y) = p_{Y|X}(y\mid x)\,p_X(x) = p_Y(y)\,p_X(x)$ für alle $x$ mit $p_X(x) > 0$; für $x$ mit $p_X(x) = 0$ sind beide Seiten $0$.
:::

Aussage 3 ist die Verallgemeinerung von $P(A \mid B) = P(A)$ aus dem Kapitel [Erwartungswert und Varianz](erwartungswert.md): Wissen über $X$ verschiebt die Verteilung von $Y$ nicht. Im stetigen Fall gilt dieselbe Äquivalenz mit Dichten, allerdings nur "fast überall" — Dichten sind ja nur bis auf Nullmengen bestimmt (siehe [Stetige Verteilungen](stetige-verteilungen.md)).

:::{admonition} Satz
**von Bayes:**
Gegeben zwei Ereignisse $A,B \subseteq \Omega$ ist

$$
P(A|B) = \dfrac{P(B|A)P(A)}{P(B)}.
$$
:::

:::{admonition} Beispiel
**Warum die Basisrate zählt.** Ein Test erkennt eine seltene Krankheit zuverlässig: $99\,\%$ der Kranken werden erkannt, und nur $1\,\%$ der Gesunden bekommen fälschlich ein positives Ergebnis. Trotzdem ist bei einem positiven Test die Wahrscheinlichkeit, tatsächlich krank zu sein, klein. Der Grund ist die *Basisrate* $P(A)$: Ist nur einer von tausend krank, so kommen auf einen richtig erkannten Kranken etwa zehn fälschlich positive Gesunde — die kleine Fehlerrate von $1\,\%$ wirkt auf eine tausendmal größere Gruppe. In der Sprache der Konfusionsmatrix aus dem Kapitel [Titanic EDA](explorative-analyse-mit-numpy.ipynb): Der Test ist ein Klassifikator, die $99\,\%$ sind sein Recall (die *Sensitivität*), das $1\,\%$ seine Falsch-Positiv-Rate, und gesucht ist seine Precision, der Anteil der Kranken unter den positiv Getesteten. Mit $A$ = „krank“ und $B$ = „Test positiv“ rechnet der Satz von Bayes genau diese Gewichtung aus:

$$
P(A|B) = \dfrac{0{,}99 \cdot 0{,}001}{0{,}99 \cdot 0{,}001 + 0{,}01 \cdot 0{,}999} = \dfrac{0{,}00099}{0{,}00099 + 0{,}00999} \approx 0{,}09.
$$

$P(A|B)$ ist eben nicht $P(B|A)$, sondern $P(B|A)$ *mal* das Verhältnis $P(A)/P(B)$, und $P(B)$ wird von der großen Gruppe der Gesunden dominiert. Wer die beiden bedingten Wahrscheinlichkeiten verwechselt, begeht den *Basisratenfehler* — der ist so häufig, dass er einen eigenen Namen hat. Bei der Titanic-Regel „Frauen überleben“ lagen Recall $0{,}68$ und Precision $0{,}74$ nahe beieinander, weil Überlebende und Frauen ähnlich häufig sind; hier liegt zwischen $0{,}99$ und $0{,}09$ eine Basisrate von einem Promille. (Woher der Nenner kommt, klärt der Satz von der totalen Wahrscheinlichkeit unten.)
:::

:::{admonition} Beweis
Die Definition der bedingten Wahrscheinlichkeit ist
$P(A|B) = \dfrac{P(A \cap B)}{P(B)}$
und das wenden wir auch auf vertauschte Rollen von $A$ und $B$ an.
:::

Um den Nenner $P(B)$ auszurechnen, hilft oft der folgende Satz:

:::{admonition} Satz
**von der totalen Wahrscheinlichkeit:**
Ist $\Omega = A_1 \cup \dots \cup A_n$ eine Zerlegung in paarweise disjunkte Ereignisse mit $P(A_i) > 0$, so gilt für jedes Ereignis $B$

$$
P(B) = \sum_{i=1}^n P(B|A_i)\,P(A_i).
$$
:::

:::{admonition} Beweis
Die Mengen $B \cap A_i$ sind paarweise disjunkt und ihre Vereinigung ist $B$, also ist $P(B) = \sum_i P(B \cap A_i)$ (endliche Additivität), und nach Definition der bedingten Wahrscheinlichkeit ist $P(B \cap A_i) = P(B|A_i)\,P(A_i)$.
:::

Im Satz von Bayes kann man den Nenner also durch $P(B) = P(B|A)P(A) + P(B|A^c)P(A^c)$ ersetzen, wenn man nur $A$ und sein Gegenteil kennt.

:::{admonition} Satz
**von Bayes, Fassung 2:**
Gegeben zwei Zufallsvariablen $X,Y \colon \Omega \to \mathbb{R}^n$ ist

$$
P(X=x | Y=y) = \dfrac{ P(Y=y|X=x)P(X=x) }{P(Y=y)}.
$$
:::

Das wenden wir häufig so an: $Y$ ist 'bekannt' und $X$ ist das vorläufige Modell.
Dabei nennen wir $Y=y$ die *Daten* $D$ und $X=x$ die *Hypothese* $H$.

Gegeben Daten und Hypothese erhalten wir so

:::{admonition} Satz
**von Bayes, Fassung 3:**

$$
P(H|D) = \dfrac{ P(D|H) P(H) }{ P(D) }
$$

Dabei heißt $P(H)$ der **Prior** (die a priori Wahrscheinlichkeit der Hypothese),
$P(D)$ die **Evidenz**, $P(D|H)$ die **Likelihood** und $P(H|D)$ der **Posterior** (die a posteriori Wahrscheinlichkeit der Hypothese). Man merkt sich: Die Likelihood beantwortet die Frage 'Wie wahrscheinlich sind die Daten, wenn die Hypothese wahr wäre?'.
Im Gegensatz zu $P(H)$ ist die Likelihood $P(D|H)$ zumindest im Prinzip berechenbar.
:::

:::{admonition} Beispiel
**Wie man eine Likelihood ausrechnet.** Bisher waren $H$ und $D$ Ereignisse mit endlich vielen Ausgängen. In der Praxis ist die Hypothese meist eine ganze Verteilung. Nehmen wir an, wir haben $n$ Messwerte $D = (x_1,\dots,x_n)$ und rechnen mit Normalverteilungen: Die Hypothese $H$ lautet, dass die Daten aus einer $\mathcal{N}(\mu,\sigma^2)$ mit $\mu = 0$ und $\sigma = 2$ stammen. Die Likelihood $P(D \mid H)$ ist dann die Wahrscheinlichkeit(sdichte), genau diese $n$ Werte zu sehen, wenn die Hypothese stimmt — und weil die Messungen unabhängig sein sollen, faktorisiert die gemeinsame Dichte nach der Proposition oben in ein Produkt:

$$
P(D \mid H) = \prod_{i=1}^n p_{\mu,\sigma}(x_i) = \prod_{i=1}^n \dfrac{1}{\sqrt{2\pi}\,\sigma} \exp\left( -\dfrac{(x_i - \mu)^2}{2\sigma^2} \right) \quad \text{mit } \mu = 0,\ \sigma = 2.
$$

Drei Rollen sind dabei sauber zu trennen: die *datenerzeugende Verteilung*, die es in der Welt gibt und die wir nicht kennen; die *beobachteten Daten* $D$, die wir haben; und die *Modellverteilung*, die wir zur Hypothese erklären. Die Likelihood vergleicht die zweite mit der dritten. Lässt man $\mu$ und $\sigma$ variieren, statt sie festzuhalten, wird aus der Zahl eine Funktion $L(\mu,\sigma) := \prod_{i=1}^n p_{\mu,\sigma}(x_i)$, und die Parameter zu suchen, die sie maximieren, ist das Maximum-Likelihood-Prinzip — siehe [Statistische Modelle und Schätzer](statistische-modelle.md), wo aus dem Produkt durch Logarithmieren eine Summe wird.
:::

:::{admonition} Satz
**von Bayes, Fassung 4:**

$$
\text{Posterior} = \dfrac{ \text{Likelihood} \cdot \text{Prior} }{ \text{Evidenz} }.
$$
:::

:::{admonition} Beispiel
**Bayessches Updaten.** Der Posterior von heute ist der Prior von morgen. Im Krankheitstest-Beispiel war die Wahrscheinlichkeit, nach einem positiven Test krank zu sein, etwa $0{,}09$. Wird der Test ein zweites Mal gemacht, unabhängig vom ersten, so ist $0{,}09$ jetzt der Prior $P(H)$, die Likelihood eines positiven Ergebnisses bleibt $0{,}99$ bei Kranken und $0{,}01$ bei Gesunden, und die Evidenz rechnet man wieder mit der totalen Wahrscheinlichkeit aus:

$$
P(H|D) = \dfrac{0{,}99 \cdot 0{,}09}{0{,}99 \cdot 0{,}09 + 0{,}01 \cdot 0{,}91} \approx 0{,}91.
$$

Zwei positive Tests hintereinander machen aus einem Promille erst neun Prozent und dann einundneunzig. Jede neue Beobachtung schiebt den Posterior weiter, und das Ergebnis hängt vom ersten Prior ab: Wer mit $P(H) = 0{,}001$ startet, braucht zwei Tests, wer mit $0{,}5$ startet (etwa, weil schon Symptome vorliegen), ist nach einem Test bei $0{,}99$. Diesen Prozess nennt man *Bayessches Updaten*; das Kapitel [Statistische Modelle](statistische-modelle.md) macht aus der Likelihood ein allgemeines Schätzverfahren.
:::

## Kovarianz

Vorab eine Warnung, die wir schon aus dem Kapitel [Deskriptive Statistik](deskriptive-statistik.md) kennen: Kovarianz und Korrelation messen einen Zusammenhang über *alle* Datenpunkte. Zerfallen die Daten in Gruppen, kann der Zusammenhang in jeder Gruppe das umgekehrte Vorzeichen haben, siehe das [Simpson-Paradoxon](deskriptive-statistik.md). Die Zahlen in diesem Kapitel sind also erst dann aussagekräftig, wenn man weiß, dass die Stichprobe aus einer Population stammt.

:::{admonition} Definition
Gegeben zwei Zufallsvariablen $X,Y \colon \Omega \to \mathbb{R}$ ist die **Kovarianz**
definiert als

$$
\operatorname{Cov}(X,Y) := \mathbb{E}\left( \left( X - \mathbb{E}X \right) \left( Y - \mathbb{E}Y \right) \right).
$$
:::

Insbesondere ist $\mathbb{V}(X) = \operatorname{Cov}(X,X)$.

Die Kovarianz hat die gleiche Krankheit wie die Varianz: sie ist skalenabhängig. Zur Heilung normiert man mit den Standardabweichungen:

:::{admonition} Definition
Der (Pearsonsche) **Korrelationskoeffizient** ist

$$
\rho(X,Y) := \dfrac{\operatorname{Cov}(X,Y)}{\sigma(X)\sigma(Y)}.
$$

Klar: $\rho(X,Y)=0$ genau dann wenn $\operatorname{Cov}(X,Y)=0$.

Man sagt, $X$ und $Y$ sind **positiv korreliert**, wenn $\rho(X,Y) > 0$ ist,
**negativ korreliert** (oder antikorreliert), wenn $\rho(X,Y) < 0$ ist,
und **unkorreliert**, wenn $\rho(X,Y)=0$ ist.
:::

:::{admonition} Bemerkung
**Für Daten.** Liegen $x, y \in \mathbb{R}^n$ als zwei Spalten einer Tabelle vor, so ersetzt man in den Definitionen den Erwartungswert durch den Mittelwert und erhält die *empirische Kovarianz* und den *empirischen Korrelationskoeffizienten*

$$
\operatorname{Cov}(x,y) := \frac{1}{n} \sum_{i=1}^n (x_i - \bar x)(y_i - \bar y) = \frac{1}{n}\, \tilde x \cdot \tilde y, \qquad r := \frac{\operatorname{Cov}(x,y)}{\sigma(x)\,\sigma(y)} = \frac{\tilde x \cdot \tilde y}{\lVert \tilde x \rVert \, \lVert \tilde y \rVert},
$$

mit den zentrierten Vektoren $\tilde x, \tilde y$ aus dem Kapitel [Erwartungswert und Varianz](erwartungswert.md). Der Korrelationskoeffizient von Daten ist also wörtlich der Kosinus des Winkels zwischen den zentrierten Spalten. Das ist die Zahl, die `np.corrcoef(x, y)[0, 1]` im Kapitel [Titanic EDA](explorative-analyse-mit-numpy.ipynb) ausgibt; `np.cov(x, y, ddof=0)` liefert die Kovarianzmatrix in der $n$-Version (ohne `ddof=0` teilt Numpy hier, anders als bei `np.var`, durch $n-1$). Für die Iris-Aufgabe aus dem Kapitel [Deskriptive Statistik](deskriptive-statistik.md) rechnet man einmal über alle Zeilen und einmal je Spezies:

```python
x = datasets.load_iris().data; y = datasets.load_iris().target
print(np.corrcoef(x[:, 0], x[:, 1])[0, 1])                          # -0.118
for s in range(3):
    print(s, np.corrcoef(x[y == s, 0], x[y == s, 1])[0, 1])         # 0.743, 0.526, 0.457
```
:::

:::{admonition} Proposition
Die Kovarianz ist symmetrisch: $\operatorname{Cov}(X,Y) = \operatorname{Cov}(Y,X)$

Die Kovarianz ist bilinear: $\operatorname{Cov}(aX+bY, Z) = a\operatorname{Cov}(X,Z) + b\operatorname{Cov}(Y,Z)$ für $a,b \in \mathbb{R}$.

Die Kovarianz ist positiv (semi)definit: $\operatorname{Cov}(X,X) = \mathbb{V}(X) \geq 0$, und $\operatorname{Cov}(X,X) = 0$ gilt genau dann, wenn $X$ fast sicher konstant ist.
:::

:::{admonition} Beweis
Symmetrie und Semidefinitheit liest man direkt an der Definition ab ($\operatorname{Cov}(X,X) = \mathbb{E}((X-\mathbb{E}X)^2) \geq 0$). Für die Bilinearität ist $aX + bY - \mathbb{E}(aX+bY) = a(X - \mathbb{E}X) + b(Y - \mathbb{E}Y)$ nach der Linearität des Erwartungswerts; Ausmultiplizieren mit $(Z - \mathbb{E}Z)$ und nochmals Linearität liefern die Behauptung. Für den Gleichheitsfall: $\mathbb{E}((X-\mathbb{E}X)^2) = 0$ bedeutet, dass die nichtnegative Zufallsvariable $(X-\mathbb{E}X)^2$ Erwartungswert $0$ hat, also fast sicher $0$ ist.
:::

Aus Symmetrie und Bilinearität folgen die Rechenregeln, die man in der Praxis ständig braucht:

:::{admonition} Proposition
**Rechenregeln der Kovarianz.** Für Zufallsvariablen $X, Y$ und eine Konstante $\beta \in \mathbb{R}$ gilt

1. $\mathbb{V}(X+Y) = \mathbb{V}(X) + \mathbb{V}(Y) + 2\operatorname{Cov}(X,Y)$,
2. $\operatorname{Cov}(X, \beta) = 0$,
3. $\operatorname{Cov}(X+\beta, Y) = \operatorname{Cov}(X,Y)$,
4. $\operatorname{Cov}(X,Y) = \mathbb{E}(XY) - \mathbb{E}(X)\,\mathbb{E}(Y)$.
:::

:::{admonition} Beweis
(1) $\mathbb{V}(X+Y) = \operatorname{Cov}(X+Y, X+Y) = \operatorname{Cov}(X,X) + \operatorname{Cov}(X,Y) + \operatorname{Cov}(Y,X) + \operatorname{Cov}(Y,Y)$ nach Bilinearität, und die beiden mittleren Terme sind nach Symmetrie gleich.
(2) Die konstante Zufallsvariable $\beta$ hat Erwartungswert $\beta$, also ist $\beta - \mathbb{E}\beta = 0$ und $\operatorname{Cov}(X,\beta) = \mathbb{E}((X - \mathbb{E}X) \cdot 0) = 0$.
(3) Bilinearität und (2): $\operatorname{Cov}(X+\beta, Y) = \operatorname{Cov}(X,Y) + \operatorname{Cov}(\beta, Y) = \operatorname{Cov}(X,Y)$.
(4) Ausmultiplizieren der Definition und Linearität des Erwartungswerts:

$$
\mathbb{E}\big(XY - X\,\mathbb{E}Y - Y\,\mathbb{E}X + \mathbb{E}X\,\mathbb{E}Y\big) = \mathbb{E}(XY) - 2\,\mathbb{E}X\,\mathbb{E}Y + \mathbb{E}X\,\mathbb{E}Y = \mathbb{E}(XY) - \mathbb{E}X\,\mathbb{E}Y.
$$

Regel (4) ist das Gegenstück zur Formel $\mathbb{V}(X) = \mathbb{E}(X^2) - (\mathbb{E}X)^2$ aus dem Kapitel [Erwartungswert und Varianz](erwartungswert.md); für $X = Y$ fallen beide zusammen. Aus (1) folgt außerdem $\mathbb{V}(X_1 + \dots + X_n) = \sum_i \mathbb{V}(X_i)$, sobald die $X_i$ paarweise unkorreliert sind.
:::

:::{admonition} Satz
**Unabhängige Zufallsvariablen sind unkorreliert.** Sind $X$ und $Y$ unabhängig (im Sinne des Kapitels [Erwartungswert und Varianz](erwartungswert.md), Abschnitt Unabhängigkeit) und haben sie endliche Varianz, so gilt $\mathbb{E}(XY) = \mathbb{E}(X)\,\mathbb{E}(Y)$ und damit $\operatorname{Cov}(X,Y) = 0$.
:::

:::{admonition} Beweis
Im diskreten Fall ist die gemeinsame pmf wegen der Unabhängigkeit ein Produkt, $p(x,y) = p_X(x)\,p_Y(y)$, und die Doppelsumme zerfällt:

$$
\mathbb{E}(XY) = \sum_{x}\sum_{y} x\,y\,p_X(x)\,p_Y(y) = \Big(\sum_x x\,p_X(x)\Big)\Big(\sum_y y\,p_Y(y)\Big) = \mathbb{E}(X)\,\mathbb{E}(Y).
$$

Im stetigen Fall ersetzt man die Summen durch Integrale über die gemeinsame Dichte $p(x,y) = p_X(x)\,p_Y(y)$ (gemeinsame Dichten führen wir im nächsten Kapitel ein); die Rechnung ist dieselbe. Mit Regel (4) folgt $\operatorname{Cov}(X,Y) = \mathbb{E}(XY) - \mathbb{E}X\,\mathbb{E}Y = 0$.
:::

:::{admonition} Bemerkung
Die Umkehrung gilt nicht: Unkorrelierte Zufallsvariablen können abhängig sein. Ein Beispiel ist $X$ gleichverteilt auf $[-1,1]$ und $Y = X^2$: Dann ist $\mathbb{E}(XY) = \mathbb{E}(X^3) = 0 = \mathbb{E}X\,\mathbb{E}Y$, also $\operatorname{Cov}(X,Y) = 0$, aber $Y$ ist eine Funktion von $X$. Die Kovarianz misst nur *lineare* Zusammenhänge. Für gemeinsam normalverteilte $(X,Y)$ gilt die Umkehrung dagegen doch, wie wir im nächsten Kapitel sehen.
:::

Damit verhält sich die Kovarianz wie ein Skalarprodukt — allerdings nur „modulo Konstanten“, denn konstante Zufallsvariablen haben Kovarianz $0$ mit allem, auch mit sich selbst. Man kann das rigoros machen, und die Kovarianz als Skalarprodukt in einem $\mathcal{L}^2$-Raum von Zufallsvariablen auffassen, in dem man zwei Zufallsvariablen identifiziert, die sich nur um eine Konstante unterscheiden. Der Korrelationskoeffizient spielt dann die Rolle des Kosinus des Winkels zwischen zwei Zufallsvariablen. Für Daten ist es wörtlich so (siehe die Bemerkung *Für Daten* oben); die im maschinellen Lernen verbreitete 'cosine similarity' ist derselbe Kosinus, nur ohne das Zentrieren.

Man kann etwas üben, in einem Scatterplot zweier Variablen den Korrelationskoeffizienten zu 'sehen',
etwa mit dem Spiel ['Guess the Correlation' von Omar Wagih](https://www.guessthecorrelation.com).

```{figure} images/normalmarginal.png
:width: 480px
:align: center
:name: bivariate-randhistogramme

Eine Stichprobe aus einer bivariaten Normalverteilung mit den beiden Randhistogrammen.
```

Das Bild zeigt, warum man die Korrelation nicht an den einzelnen Variablen ablesen kann. Die beiden Randhistogramme sind je eine unauffällige Glockenkurve; sie sähen genauso aus, wenn die Korrelation das umgekehrte Vorzeichen hätte oder wenn sie $0$ wäre, denn die Marginalverteilungen hängen nicht von ihr ab. Sichtbar wird der Zusammenhang allein im gemeinsamen Streudiagramm, an der Schräglage der Punktwolke. Das ist dieselbe Beobachtung wie oben bei der gemeinsamen Verteilung: Aus den Einzelverteilungen lässt sich die gemeinsame nicht rekonstruieren.

Was Kovarianz und Korrelation geometrisch bedeuten, sehen wir im nächsten Kapitel an der multivariaten Normalverteilung: Dort beschreibt die Kovarianzmatrix Form und Lage der Ellipsen, die die Dichte als Höhenlinien hat.
