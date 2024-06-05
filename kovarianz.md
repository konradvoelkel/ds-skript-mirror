# Multivariate Statistik: Kovarianz und Abhängigkeit

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
Die Zufallsvariablen $X_i$ heißen **Randverteilungen** oder **Marginalverteilungen**.
:::

Allgemeiner wird auch z.B. $(X_1,X_3,X_9)$ als Marginalverteilung von $X$ bezeichnet,
oder auch jede Verkettung von $X$ mit einer linearen Projektion $\pi \colon \mathbb{R}^n \to \mathbb{R}^m$, nicht notwendig auf die Koordinaten(hyper)ebene(n) der Standardbasis in $\mathbb{R}^n$.

:::{admonition} Bemerkung
Die Verteilung von $X_i$ ist $P(X_i \in A) = P(X \in \pi_i^{-1}(A))$.

Zu einer Zufallsvariable $(X,Y) \colon \Omega \to \mathbb{R}^2$ können wir die Verteilung von $Y$ berechnen als
$P(Y \in A) = \sum_{x \in X(\Omega)} P((X,Y) \in \{x\} \times A)$ im diskreten Fall (und mit einem entsprechenden Integral im stetigen Fall), wobei wir $\pi_1^{-1}(A) = X(\Omega)\times A$ in disjunkte Teilmengen zerlegt haben.
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


:::

:::{admonition} Satz
**von Bayes:**
Gegeben zwei Ereignisse $A,B \subseteq \Omega$ ist

$$
P(A|B) = \dfrac{P(B|A)P(A)}{P(B)}.
$$
:::

:::{admonition} Beweis
Die Definition der bedingten Wahrscheinlichkeit ist
$P(A|B) = \dfrac{P(A \cap B)}{P(B)}$
und das wenden wir auch auf vertauschte Rollen von $A$ und $B$ an.
:::

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
$P(D)$ die **Evidenz**, $P(D|H)$ die **Likelihood** und $P(H|D)$ der **Posterior** (die a posteriori Wahrscheinlichkeit der Hypothese). Man merkt sich: 'how likely is the data, if the hypothesis were true?' = Likelihood.
Im Gegensatz zu $P(H)$ ist die Likelihood $P(D|H)$ zumindest im Prinzip berechenbar.
:::

:::{admonition} Satz
**von Bayes, Fassung 4:**

$$
\text{Posterior} = \dfrac{ \text{Likelihood} * \text{Prior} }{ \text{Evidenz} }.
$$
:::

:::{admonition} Beispiel
Die Hypothese $H$ ist, dass die Daten standardnormalverteilt sind. Dann lässt sich $P(D|H)$ berechnen und $P(H|D)$ ist ein Schätzwert für $P(H)$, der $D$ berücksichtigt. Wenn wir also $P(H)$ zunächst schätzen, und dann die Daten $D$ betrachten, erhalten wir eine bessere Schätzung (die aber auch von der vorherigen abhängt).
Diesen Prozess nennt man *Bayessches Updaten*.
:::

## Kovarianz

:::{admonition} Definition
Gegeben zwei Zufallsvariablen $X,Y \colon \Omega \to \mathbb{R}$ ist die **Kovarianz**
definiert als

$$
\operatorname{Cov}(X,Y) := \mathbb{E}\left( \left( X - \mathbb{E}X \right) \left( Y - \mathbb{E}Y \right) \right),
$$
:::

also auch $\mathbb{V}(X) = \operatorname{Cov}(X,X)$.

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

:::{admonition} Proposition
Die Kovarianz ist symmetrisch: $\operatorname{Cov}(X,Y) = \operatorname{Cov}(Y,X)$

Die Kovarianz ist bilinear: $\operatorname{Cov}(aX+bY, Z) = a\operatorname{Cov}(X,Z) + b\operatorname{Cov}(Y,Z)$ für $a,b \in \mathbb{R}$.

Die Kovarianz ist positiv (semi)definit: $\operatorname{Cov}(X,X) \geq 0$.
:::

Damit verhält sich die Kovarianz wie ein Skalarprodukt. Man kann das rigoros machen, und die Kovarianz als Skalarprodukt in einem $\mathcal{L}^2$-Raum von Zufallsvariablen auffassen. Der Korrelationskoeffizient spielt dann die Rolle des Kosinus des Winkels zwischen zwei Zufallsvariablen. Im diskreten Fall ist es genau das, weshalb im maschinellen Lernen oft auch 'cosine similarity' als Maß für die Korrelation angegeben wird.

Man kann etwas üben, in einem Scatterplot zweier Variablen den Korrelationskoeffizienten zu 'sehen',
etwa mit dem Spiel ['Guess the Correalation' von Omar Wagih](https://www.guessthecorrelation.com).