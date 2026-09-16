# Statistische Modelle und Schätzer

Im Data Science Prozess, also dem Weg von den Daten zu einem Produkt (sei es ein Bericht, eine Vorhersage oder neue interessante Daten), modellieren wir die Daten. Genau genommen modellieren wir Teilaspekte, Ausschnitte der Daten (wie ja auch schon die Daten selbst nur ein Ausschnitt aus der Realität sind).
Dabei können wir zum einen daran interessiert sein, wie die Daten entstanden sind, zum anderen aber auch geleitet sein von dem Wunsch, etwas bestimmtes darüber sagen bzw. damit machen zu können. Es ist also hilfreich, sich klar zu machen, welche Art von Information man den Daten entlocken möchte, und dann darauf Modelle abzustimmen.
Oftmals ist es dabei möglich, verschiedene Ansätze zu wählen, um die gleiche Art von Information zu berechnen. Die Ergebnisse können sich dabei durchaus unterscheiden und häufig (im unsupervised learning) können wir die berechneten Ergebnisse nicht mit dem "richtigen" Ergebnis vergleichen. Es bleibt dann nur noch, den Informationsgehalt der Modelle zu vergleichen (die Entropie auszurechnen), alle Modell-Annahmen auf Plausibilität zu untersuchen und allgemeine Kriterien für die Güte von Modellen zu entwickeln. Letzteres wollen wir jetzt anpacken.

Der klassische (also historisch älteste) Zugang beginnt mit der Formalisierung der Modelle und der Aspekte, die man damit aus den Daten berechnen möchte.
Man spricht von einem **statistischen Modell**, einer **Statistik** und verschiedenen **Schätzern** für eine Statistik, die man vergleichen kann. Ein Kriterium ist dabei, ob ein Schätzer wenigstens für sehr große Stichproben in der Nähe des "richtigen" Ergebnisses liegt. Aber halt - wenn wir das richtige Ergebnis nicht kennen, wie können wir das dann überhaupt sagen?

Die Lösung ist, sich auf solche statistischen Modelle einzuschränken, wo wir die grobe Struktur des richtigen Ergebnisses für einen Schätzer soweit beschreiben können, dass man eben doch zu Aussagen kommen kann wie "im Grenzwert schätzt dieser Schätzer den Erwartungswert jener Statistik auf den Daten". Und dann kann man darüber reden, wie gut die Werte abseits vom Grenzwert, für etwas kleinere Samples aussehen. Wir lernen dabei noch einen für die Data Science und das Maschinelle Lernen sehr wichtigen Begriff kennen: Das **Maximum Likelihood**-Prinzip.

Ein sehr konkretes Beispiel vorab: Gegeben Daten, die als Vektor $x$ der Länge $n$ von reellen Zahlen ($\texttt{float}$) vorliegen, von denen wir wissen, dass sie als Stichprobe einer eindimensional normalverteilten Zufallsvariable $X$ mit Erwartungswert $\mu(X)$ und Varianz $\sigma^2(X)$ entstanden sind, wollen wir die Standardabweichung $\sigma(X)$ schätzen. Dazu findet man in den Büchern zwei verschiedene Formeln: $\sigma(x)$ und $\sigma^\ast(x)$, die sich nur durch den Nenner unterscheiden:

$$
\sigma(x)^2 = \dfrac{1}{n} \sum_{i=1}^n (x_i-\mu)^2,\qquad \sigma^\ast(x)^2 = \dfrac{1}{n-1} \sum_{i=1}^n (x_i-\mu)^2
$$

In diesen Formeln muss man nun etwas aufpassen, wenn man das praktisch implementieren will - denn was ist $\mu$?
In der Anwendung kenne ich $\mu(X)$ nicht, muss also $\mu(x)$ verwenden. Dann aber stellt sich heraus, dass die Information in $\{x_i-\mu(x)\}_{i=1}^{n-1}$ genügt, um $x_n - \mu(x)$ zu berechnen, denn nach Definition von $\mu(x)$ ist $x_n - \mu(x) = \sum_{i=1}^{n-1} (\mu(x) - x_i)$. Gewissermaßen gibt es also, wenn man $\mu(x)$ anstelle von $\mu(X)$ verwendet, einen Freiheitsgrad weniger als $n$. Wir werden gleich sehen, wie sich das auf die Eigenschaften dieser beiden Schätzer für $\sigma(X)$ auswirkt.

Wenn man statistische Modelle formal definiert hat, kann man auch sehr gut über Konfidenzintervalle und Hypothesentests sprechen, was wir dann gleich im Anschluss erledigen. Konfidenzintervalle erweitern des Ansatz des bloßen Schätzens einer Statistik um die Information, welchen Fehlerbereich man dieser Schätzung beimisst. Hypothesentests erweitern den Ansatz darum, schließlich zu Entscheidungen zu kommen. Bei der Diskussion um Hypothesentests ist es unvermeidlich, auch über den problematischen Begriff der **Signifikanz** zu sprechen. Aber eins nach dem anderen!

## Statistische Modelle

:::{admonition} Definition
Ein statistisches Modell ist ein Tripel $(\mathcal{X}, \mathcal{F}, P_\theta : \theta \in \Theta)$
aus einem **Stichprobenraum** $\mathcal{X}$, einer $\sigma$-Algebra $\mathcal{F}$ auf $\mathcal{X}$ und einer Klasse $\{P_\theta\}_{\theta \in \Theta}$ von Wahrscheinlichkeitsmaßen auf $(\mathcal{X}, \mathcal{F})$, die mindestens zwei Elemente enthält, also $|\Theta| > 1$.
Wir schreiben oft einfach $(\mathcal{X}, P_\theta : \theta \in \Theta)$.
:::

:::{admonition} Bemerkung
Bei einem statistischen Modell handelt es sich also noch nicht um das 'fertige Modell' mit dem wir im Sinne der Data Science klassifizieren bzw. Vorhersagen machen wollen, sondern um eine ganze Klasse von Modellen, die mit der Menge $\Theta$ parametrisiert werden. Diese Menge $\Theta$ kann beliebig wild sein, nur sollen es wenigstens zwei Elemente sein, damit sich der Begriff nicht im Fall $\Theta = \{\theta\}$ reduziert auf 'der Stichprobenraum und ein Wahrscheinlichkeitsmaß drauf'.
Wenn man im Kontext eines statistischen Modells von Erwartungswerten (also z.B. von Varianzen) spricht, muss man aufpassen und in der Notation am besten das $\theta$ mitführen, also $\mathbb{E}_\theta(Y)$ für den Erwartungswert einer Zufallsvariable $Y : \mathcal{X} \to \mathbb{R}$, denn dieser hängt von $\theta$ ab.
:::

:::{admonition} Definition
Ein statistisches Modell heißt **parametrisches Modell**, wenn die Parametermenge $\Theta$ eine Teilmenge eines $\mathbb{R}^d$ ist für ein $d \in \mathbb{N}$. Für $d=1$ sagt man auch **einparametriges Modell**.

Wenn die Stichprobenmenge $\mathcal{X}$ diskret ist (höchstens abzählbar), und $\mathcal{F} = \mathcal{P}(X)$, nennt man das Modell **diskret** und in dem Fall haben alle $P_\theta$ eine Zähldichte $p_\theta$, d.h. $p_\theta(x) = P_\theta({x})$.

Wenn die Stichprobenmenge $\mathcal{X}$ eine (Borel)-meßbare Teilmenge des $\mathbb{R}^n$ ist (z.B. eine offene Menge oder die Niveaumenge einer stetigen Funktion) und $\mathcal{F}$ eine Einschränkung der Borel-$\sigma$-Algebra von $\mathbb{R}^n$ ist, und außerdem jedes $P_\theta$ eine Dichtefunktion $f_\theta$ besitzt, dann heißt das statistische Modell ein **stetiges Modell**.

Ein statistisches Modell, welches entweder diskret oder stetig ist, nennt man auch **Standardmodell**.
:::

:::{admonition} Bemerkung
Den Stichprobenraum können wir uns in erster Näherung vorstellen wie die Menge der möglichen Ergebnisse bei Stichprobengröße $1$ (die Grundgesamtheit $\Omega$ lässt grüßen). Aber: man kann auch das mehrfache Wiederholen eines Experiments als eigentlich-ein-Experiment umetikettieren und eine Abfolge von Einzelergebnissen dann ein Ergebnis nennen, und so Stichprobengrößen größer $1$ modellieren. Zu jedem statistischen Modell lässt sich das **Produktmodell** konstruieren:

$$
(\mathcal{X}^N, \mathcal{F}^{\otimes N}, P_{\theta}^{\otimes N} : \theta \in \Theta).
$$

Die Projektionen $X_i \colon \mathcal{X}^N \to \mathcal{X}$ sind dann unabhängig identisch verteilte Zufallsvariablen bezüglich jeder Verteilung $P_\theta$. Die Notation $\mathcal{F}^{\otimes N}$ bezeichnet die offensichtliche Art, auf $\mathcal{X}^N$ eine $\sigma$-Algebra zu definieren (Sie dürfen das wie gewohnt ignorieren) und $P_\theta^{\otimes N}$ ordnet einem Ereignis in $\mathcal{X}^N$ von der Form $A_1 \times \cdots \times A_N$ das Produkt $\prod_{i=1}^N P_\theta(A_i)$ zu. Damit ist die $N$-fache Wiederholung modelliert.
:::

:::{admonition} Beispiel
Wir modellieren einen Würfelwurf eines potentiell unfairen Würfels mit einem diskreten Modell: $\mathcal{X} = \{1,\dots,6\}$ und $\Theta = \Delta_6$, die Menge aller möglichen diskreten Verteilungen auf einer sechselementigen Menge (geschrieben als Wahrscheinlichkeitsvektoren in $\mathbb{R}^6$), und $P_\theta(k) = \theta_k$. Konkret für $\theta = (\theta_1,\dots,\theta_n)$ ist also die Wahrscheinlichkeit, eine $6$ zu werfen im Modell mit Parameter $\theta$ gegeben durch $P_\theta(6) = \theta_6$.
:::

:::{admonition} Beispiel
Den zweifach wiederholten Würfelwurf modellieren wir also mit $\mathcal{X}^2$ (Ergebnisse sind Paare von Würfelaugen) und $\Theta = \Delta_6$ (denn der zweite Würfelwurf soll ja identisch verteilt modelliert werden wie der erste). Dabei ist $P_\theta^{\otimes 2}(5,6) = P_\theta(5)P_\theta(6) = \theta_5\theta_6$, wie man es von unabhängigen Ereignissen erwartet.
:::

:::{admonition} Beispiel
Wir können auch modellieren, ob beim zweifachen Wurf ein Pasch gewürfelt wurde oder nicht - und somit $\mathcal{X} = \{\text{Pasch}, \text{Keinpasch}\}$ als Stichprobenraum betrachten.
Dabei können wir einfach den Parameterraum $\Theta = \Delta_6$ beibehalten, das ist ein mögliches statistisches Modell.
Wir sehen allerdings, dass $P_\theta^{\otimes}(k,k) = \theta_k^2$ ist, also ist $P_\theta(\text{Pasch}) = \sum_{k=1}^6 \theta_k^2$,
also genügt uns eigentlich der Parameter $s = \sum_{k=1}^6 \theta_k^2$ und wir könnten uns also einen kleineren Parameterraum vorstellen.
Dann stellt sich allerdings die Frage, welche Verteilung $P_s$ wir dem Parameter $s$ zuordnen wollen. Eine konkret sinnvolle Wahl ist dabei die Verteilung $\theta$ mit maximaler Entropie, also eine Verteilung möglichst nah an der Gleichverteilung. Das wird nicht eindeutig, weil Permutationen von $\{1,\dots,6\}$ den Parameter $s$ und die Entropie $H(\theta)$ nicht ändern. Will man trotzdem ein irgendwie kanonisches Modell wählen, kann man z.B. eine Anordnung auf den $\theta$ fordern, also $\theta_k \geq \theta_{k+1}$.
Wir sehen hier also: ein 'zu großer' Parameterraum ist manchmal das einfachere Modell.
:::

:::{admonition} Beispiel
Stellen wir uns vor: Wir haben irgendwelche Daten $x$ in der Wildnis (lies: im WWW) gefunden, glauben nun, dass alle Instanzen $x_i$ Stichproben einer Zufallsvariablen $X$ mit Werten in $\Omega$ sind,
und modellieren also mit $\mathcal{X} = \Omega^n$.
Wenn wir merken, dass die Werte von $x$ irgendwelche `float`s sind, können wir uns das Histogramm anschauen. Vielleicht werden wir daraus nicht so schlau, und können nicht gut erkennen, ob es sich bei $X$ um eine auf $[-1,1]$ uniform verteilte Variable oder um eine Normalverteilung zentriert bei $0$ handelt oder gar um eine Exponentialverteilung. In der Realität könnte das z.B. der Fall sein, wenn $n$ sehr klein ist. Der Parameterraum wäre dann 

$$
\Theta = \{\text{uni}\} \times \{0\} \cup \{\text{norm}\} \times \{\sigma > 0\} \cup \{\text{exp}\} \times \{\lambda > 0\}.
$$

Die erste Komponente von $\Theta$ ist die Art der Verteilung $\{\text{uni, norm, exp}\}$, die zweite dann ein möglicher Parameter. So ein Modell ist kein parametrisches Modell! Wir können aber auf unnatürliche Weise eins draus machen, indem wir die kategorielle Variable $\{\text{uni, norm, exp}\}$ als Zahlen $\{1,2,3\}$ kodieren, und damit $\Theta$ als Teilmenge von $\mathbb{R}^2$ darstellen.
:::

:::{admonition} Beispiel
$\mathcal{X}=\mathbb{R}^N$ mit $\Theta = \mathbb{R} \times \mathbb{R}_{> 0}$ und $P_{\theta}^{\otimes N} = P_{\mu,\sigma}^{\otimes N}$ eine univariate Normalverteilung ist das Standardmodell einer Stichprobe der Größe $N$ einer univariaten Zufallsvariable, die normalverteilt ist.
:::

:::{admonition} Definition
Sei $(\mathcal{X}, P_\theta : \theta \in \Theta)$ ein statistisches Modell und $\Sigma$ ein weiterer Ereignisraum (d.h. eine Menge $\Sigma$ mit einer $\sigma$-Algebra darauf definiert). Dann heißt eine beliebige Zufallsvariable $S \colon \mathcal{X} \to \Sigma$ eine **Statistik** des statistischen Modells.
:::

:::{admonition} Bemerkung
Wie auch beim Begriff der Zufallsvariablen selbst stellt sich die Frage, warum wir einen neuen Namen einführen, ist doch eine Statistik nichts anderes als eine Zufallsvariable, die wiederum nichts anderes ist als eine meßbare Abbildung, im diskreten Fall ist also Statistik = Zufallsvariable = Abbildung.
Wir haben bisher sehr deutlich gesehen, dass wir mit Zufallsvariablen anders umgehen als mit Abbildungen, die wir Abbildung nennen. Genau so verhält es sich mit einer Statistik: wir verwenden eine Zufallsvariable anders, wenn wir diesen Begriff verwenden. Es ist wie ein API-Wrapper um die gleiche Datenstruktur, damit man leichter ohne Verwechslungsgefahr verschiedene Dinge damit tun kann. Denken Sie nur einmal daran, dass `String`s und `float`s ja auch irgendwie nur ein API-Wrapper um bitstrings sind. Das klappt so gut, dass wir das gleich nochmal tun wollen!
:::

## Schätzer

:::{admonition} Definition
Sei $(\mathcal{X}, P_\theta : \theta \in \Theta)$ ein statistisches Modell und $\Sigma$ ein weiterer Ereignisraum.
Sei $\tau \colon \Theta \to \Sigma$ eine beliebige Abbildung, die jedem $\theta \in \Theta$ eine Kenngröße $\tau(\theta) \in \Sigma$ zuordnet.
Dann nennen wir jede Statistik $T \colon \mathcal{X} \to \Sigma$ einen **Schätzer** (auch **Punktschätzer**) für $\tau$.
:::

:::{admonition} Bemerkung
Niemand hat gesagt, dass $T$ ein vernünftiger, guter Schätzer sein muss - tatsächlich muss $T$ erstmal nix mit $\tau$ zu tun haben außer dass Definitionsbereich und Wertebereich zum statistischen Modell bzw. $\tau$ passen müssen. Das gibt uns die Flexibilität, gute Schätzer und miserable Schätzer miteinander zu vergleichen. Als $\tau$ ist natürlich auch die Identität zulässig, also $\tau = id \colon \Theta \to \Theta$, $\tau(\theta)=\theta$ und die betrachteten Schätzer für $\tau$ sind dann Schätzer des Parameters $\theta \in \Theta$.
:::

:::{admonition} Beispiel
Im Standardmodell einer univariaten Normalverteilung mit Stichprobengröße $N$ ist die Projektion $\Theta \to \mathbb{R}$ auf die erste Komponente, also den Erwartungswert $\mu$ eine Abbildung $\tau$, deren Schätzer uns interessieren.
Ein möglicher Schätzer ist die Statistik $c \colon \mathbb{R}^N \to \mathbb{R}$, die konstant $0$ ist (eine sehr konservative Schätzung).
Ein anderer möglicher Schätzer ist das arithmetische Mittel $\texttt{mean} \colon \mathbb{R}^N \to \mathbb{R}$, für den tatsächlich gilt, dass $\texttt{mean}(x)$ für große $N$ beliebig nah an $\mu(X)$ herankommt, wenn $X$ die gesampelte normalverteilte Zufallsvariable ist.
:::

:::{admonition} Beispiel
In den meisten statistischen Modellen können wir die Abbildung $\sigma \colon \Theta \to \mathbb{R}_{\geq 0}$ betrachten, die einem Parameter $\theta$ die Standardabweichung $\sigma(P_\theta)$ der Verteilung $P_\theta$ zuordnet (es geht nur dann nicht, wenn das zweite Moment nicht existiert, also $\mathbb{V}(P_\theta)=\infty$ vorkommt). Dafür kennen wir die beiden Schätzer $\sigma,\ \sigma^\ast \colon \mathcal{X} \to \mathbb{R}_{\geq 0}$.
:::

### Erwartungstreue

:::{admonition} Definition
Ein Schätzer $T \colon \mathcal{X} \to \Sigma$ für $\tau \colon \Theta \to \Sigma$ heißt **erwartungstreu** wenn $\mathbb{E}_{\theta}( T ) = \tau(\theta)$ für alle $\theta \in \Theta$ gilt. Gilt das nicht, heißt der Schätzer **verzerrt** (biased) und die Differenz ist der **bias** $\mathbb{B}_\theta(T) := \mathbb{E}_{\theta}( T ) - \tau(\theta)$.

Der **mittlere quadratische Fehler** des Schätzers zum zu schätzenden Wert ist

$$
\texttt{mse}(T,\theta) := \mathbb{E}_\theta\left ( (T-\tau(\theta))^2 \right ) = \mathbb{V}_\theta(T) + (\mathbb{B}_\theta(T))^2
$$

Eine Folge von Schätzern $T_n \colon \mathcal{X}^n \to \Sigma$ für $\tau$ in $n$-fachen Produktmodellen heißt **konsistent** wenn für $n\to\infty$
der Schätzer stochastisch gegen $\tau$ konvergiert: $\lim_{n\to\infty} T_n \xrightarrow{P_\theta} \tau(\theta)$. Stochastische Konvergenz (auch: Konvergenz in Wahrscheinlichkeit) heißt $\forall \epsilon > 0 : \lim_{n\to\infty} P(|T_n - \tau(\theta)| > \epsilon) = 0$.

Die Folge $T_n$ heißt **asymptotisch erwartungstreu**, wenn $\lim_{n\to\infty} \mathbb{E}_{\theta}(T_n) = \tau(\theta)$.
:::

:::{admonition} Beispiel
Im Standardmodell einer $N$-fach wiederholten univariaten Normalverteilung ist das Stichprobenmittel $\texttt{mean}$ ein erwartungstreuer Schätzer für den Parameter $\mu$.
:::

:::{admonition} Beispiel
Für die Varianz ist der Schätzer $\sigma_N^2 = \frac{1}{N} \sum_{i=1}^N (X_i - \texttt{mean}(X_j))^2$ nicht erwartungstreu, denn $\mathbb{E}(\sigma_N^2) = \frac{N-1}{N}\sigma^2(X)$. Der Bias ist also $-\frac{\sigma^2(X)}{N}$, was für $N\to\infty$ verschwindet. Damit ist der Schätzer asymptotisch erwartungstreu.

Der 'korrigierte' Schätzer $\frac{N}{N-1} \sigma_N^2 = \frac{1}{N-1} \sum_{i=1}^N (X_i - \texttt{mean}(X_j))^2$ ist erwartungstreu.
:::

:::{admonition} Definition
Ein zu einer zu schätzenden Funktion $\tau \colon \Theta \to \mathbb{R}$ erwartungstreuer Schätzer $S$ mit endlicher Varianz heißt **gleichmäßig bester erwartungstreuer Schätzer** für $\tau$, wenn für jeden weiteren erwartungstreuen Schätzer $T$ für $\tau$ mit endlicher Varianz für alle $\theta \in \Theta$ gilt:
$\mathbb{V}_\theta(S) \leq \mathbb{V}_\theta(T)$
:::

Ein solcher Schätzer hat also minimale Streuung um den zu schätzenden Wert unter allen erwartungstreuen Schätzern.

**Ausblick**

Im Allgemeinen ist es sehr schwer, gleichmäßig beste erwartungstreue Schätzer zu bestimmen (es gibt sie im Allgemeinen nicht). Ausblick: Die *Cramer-Rao-Ungleichung* für *reguläre* statistische Modelle liefert eine Abschätzung der Varianz eines Schätzers durch die *Fisher-Information* (eine Größe, die sich auch aus der relativen Entropie berechnen lässt) und erlaubt so, gleichmäßig beste Schätzer daran zu erkennen, dass sie diese Varianzschranke nicht überschreiten. Für einen erwartungstreuen Schätzer $T$ eines reellen Parameters $\theta$ lautet sie

$$
\mathbb{V}_\theta(T) \geq \frac{1}{I(\theta)}, \qquad I(\theta) := \mathbb{E}_\theta\left[\left(\frac{\partial}{\partial\theta} \log p_\theta(X)\right)^2\right],
$$

wobei $I(\theta)$ die *Fisher-Information* ist. Ein erwartungstreuer Schätzer, der diese Schranke annimmt, ist also gleichmäßig bester Schätzer. Für Verteilungen aus einer sogenannten *Exponentialfamilie* (in gewissem Sinne eine gemeinsame Verallgemeinerung der Normalverteilung, Binomialverteilung, Gamma-Verteilung, etc.) lassen sich die gleichmäßig besten Schätzer damit direkt beschreiben.


### Maximum Likelihood

:::{admonition} Definition
Gegeben ein statistisches Standardmodell $(\mathcal{X}, P_\theta : \theta \in \Theta)$ mit Dichte $f_\theta$ für $P_\theta$ heißt $\rho \colon \mathcal{X} \times \Theta \to \mathbb{R}_{\geq 0}$ mit $\rho(x, \theta) := L_x(\theta) := f_\theta(x)$ die **Likelihood-Funktion** und für festes $x$ heißt $L_x =\rho(x, \cdot) \colon \Theta \to \mathbb{R}_{\geq 0}$ die **Likelihood**-Funktion zum Beobachtungswert $x$.
:::

Wenn wir also Daten $x$ gegeben haben, drückt die Likelihood-Funktion zu $x$ für jeden Parameter $\theta$ aus, wie die Wahrscheinlichkeitsdichte an der Stelle $x$ von $P_\theta$ ausfällt. Ist die Dichte groß, so ist $x$ eine Beobachtung, die unter dem Parameter $\theta$ wahrscheinlich ist. Ist die Dichte klein, so ist $x$ unter $\theta$ unwahrscheinlich. Zur Erinnerung: Wenn wir die Hypothese $H = ( \theta$ ist der wahre Parameter $)$ haben, und $D=x$ (für Daten) schreiben, so ist $P(D|H) = L_x(\theta) = f_\theta(x)$ die Likelihood (vgl. Abschnitt über den Satz von Bayes).

:::{admonition} Definition
Ein Schätzer $T \colon \mathcal{X} \to \Theta$ für den Parameter $\theta$ heißt **Maximum-Likelihood-Schätzer** (maximum likelihood estimator, MLE), wenn für alle $x \in \mathcal{X}$ gilt: $\rho(x, T(x)) = \max_{\theta \in \Theta} \rho(x, \theta)$, also wenn $T(x)$ die Likelihood von $x$ maximiert, für alle $x$. Man schreibt auch $T(x) = argmax L_x$.
:::

Ein erstes Beispiel dafür haben wir bereits gerechnet, ohne den Namen zu benutzen: Im Kapitel
[Wichtigste diskrete Verteilungen](wichtigste-diskrete-verteilungen.ipynb) haben wir zu $k$ Erfolgen
in $n$ Versuchen dasjenige $p$ bestimmt, unter dem diese Beobachtung am wahrscheinlichsten ist, und
$\hat p = \frac{k}{n}$ erhalten. In der Sprache dieses Kapitels ist das der Maximum-Likelihood-Schätzer
im Binomialmodell $\mathcal{X} = \{0,\dots,n\}$, $\Theta = [0,1]$, $P_p = \operatorname{Bin}(n,p)$.

:::{admonition} Beispiel
Im $N$-fachen univariat normalverteilten Modell ist $x \mapsto (\texttt{mean}(x), \sigma(x))$ ein Maximum-Likelihood-Schätzer für den Parameter $(\mu(X), \sigma(X))$. Der Schätzer $\sigma^\ast$ ist hingegen kein Maximum-Likelihood-Schätzer für $\sigma(X)$. Also können sich Erwartungstreue und Maximum-Likelihood-Prinzip gegenseitig ausschließen.
:::

:::{admonition} Bemerkung
Mit Hilfe der relativen Entropie lässt sich beweisen, dass unter schwachen Voraussetzungen ($\Theta$ ein Intervall, $P_\theta$ paarweise verschieden und eine etwas technische Bedingung) eine Folge von Maximum-Likelihood-Schätzern stets konsistent ist.

Das bedeutet: Schätzt man eine Verteilung so, dass die Wahrscheinlichkeit der Beobachtung unter der geschätzten Verteilung maximal ist (Maximum-Likelihood-Prinzip), so konvergiert der Schätzwert stochastisch gegen die tatsächliche Verteilung (mit wachsender Stichprobengröße).
:::

:::{admonition} Bemerkung
Wir sind also für eine Familie von Verteilungen $P_\theta$ mit Dichten $f_\theta$ daran interessiert, die Likelihood $f_\theta(x)$ einer Beobachtung $x$ in $\theta$ zu maximieren. Um Funktionen zu maximieren, betrachten wir gern die Ableitung (dazu sollte $f$ in $\theta$ differenzierbar sein). Schon am Beispiel der univariaten Normalverteilungsdichte $\phi_{\mu,\sigma}$ sehen wir, dass die Ableitung $\frac{d}{d\mu} \phi_{\mu,\sigma}(x) =\frac{(x-\mu)}{\sigma^2} \phi_{\mu,\sigma}(x)$ bei $x=\mu$ verschwindet.
Im Allgemeinen ist die Likelihood allerdings schwerer zu berechnen (man betrachte ein $n$-faches Produktmodell!) und man kann sich mit einem einfachen Trick behelfen:
:::

**Trick**

Anstatt die Likelihood von $x$ über alle möglichen $\theta$ zu maximieren, kann man auch den Logarithmus der Likelihood bilden, die sogenannte **log-Likelihood** $\log \rho(x,\theta)$ und diese maximieren. Wegen der Konkavität des Logarithmus ist ein Maximum der log-Likelihood auch ein Maximum der Likelihood.

Wenn z.B. $\rho$ die Form $e^{A}e^{B}$ hat (etwa bei einem $2$-fachen Produktmodell), hat $\log\rho$ die Form $A+B$ und Ableitungen gleich $0$ setzen wird deutlich einfacher. Auch mit diesem Trick lässt sich aber im Allgemeinen keine analytische geschlossene Lösung finden - also kann die Informatik mit Approximations-Algorithmen glänzen, wie z.B. den *Expectation Maximization Algorithmus*, den wir später in der Vorlesung noch behandeln.

:::{admonition} Beispiel
**Maximum Likelihood für die Exponentialverteilung.**
Wir beobachten $n$ unabhängige Wartezeiten $x_1,\dots,x_n \geq 0$ und modellieren sie als
$\operatorname{Exp}(\lambda)$-verteilt, mit Dichte $f_\lambda(x) = \lambda e^{-\lambda x}$.
Wegen der Unabhängigkeit ist die Likelihood das Produkt der Einzeldichten:

$$
L(\lambda) = \prod_{i=1}^n \lambda e^{-\lambda x_i} = \lambda^n e^{-\lambda \sum_{i=1}^n x_i}.
$$

Hier lohnt sich der Trick sofort — aus dem Produkt wird eine Summe:

$$
\ell(\lambda) := \log L(\lambda) = n\log\lambda - \lambda \sum_{i=1}^n x_i.
$$

Ableiten und gleich $0$ setzen liefert

$$
\ell'(\lambda) = \frac{n}{\lambda} - \sum_{i=1}^n x_i \overset{!}{=} 0
\qquad\Longleftrightarrow\qquad
\hat\lambda = \frac{n}{\sum_{i=1}^n x_i} = \frac{1}{\texttt{mean}(x)}.
$$

Wegen $\ell''(\lambda) = -\frac{n}{\lambda^2} < 0$ ist das tatsächlich ein Maximum.
Das Ergebnis ist wieder eingängig: Die Exponentialverteilung hat den Erwartungswert
$\frac{1}{\lambda}$, also schätzen wir $\frac{1}{\lambda}$ durch das Stichprobenmittel.
Für die Beobachtungen $1, 2, 3, 4$ etwa ist $\texttt{mean}(x) = 2{,}5$ und damit $\hat\lambda = 0{,}4$.
:::

:::{admonition} Proposition
Wenn $\theta_0$ der 'wahre' Parameter für $X$ ist (mit dem $x$ gesampelt wurde), so konvergiert der Maximum-Likelihood-Schätzwert $\hat{\theta}$ für eine Stichprobe der Größe $n$ gegen den Wert $\theta$, für den die relative Entropie zwischen $P_{\theta_0}$ und $P_{\theta}$ minimiert wird (wenn das Modell gut aufgesetzt ist, ist dieses Minimum genau $0$). Um das einzusehen, benutzt man den zuvor erwähnten Trick und das Gesetz der großen Zahlen und den Zusammenhang, dass der Erwartungswert der log-Likelihood gleich der negativen Kreuzentropie $-H(x;P_{\theta_0})$ ist.
:::

:::{admonition} Beispiel
Angenommen, wir betrachten Server-Logfiles einer Web-Anwendung, insbesondere die Zeitstempel. Daraus können wir die konsekutiven Abstände berechnen, also die Wartezeit zwischen zwei Aufrufen. Wir möchten gerne wissen, mit welcher Wartezeit wir im Mittel rechnen können (um zusammen mit der durchschnittlichen Laufzeit eines Aufrufs zu einer Einschätzung zu kommen, welche Last wir erwarten können). Die Wartezeiten sind exponentialverteilt mit Parameter $\lambda > 0$, den wir schätzen wollen. zur Erinnerung: Die Dichte einer Exponentialverteilung ist $f(x) = \lambda e^{-\lambda x}$ und der Erwartungswert ist $\frac{1}{\lambda}$.

Die Likelihood für eine Stichprobe der Größe $N$ ist $L_x(\lambda) = \prod_{i=1}^N \lambda e^{-\lambda x_i}$ und die log-Likelihood ist demnach

$$
l_x(\lambda) := \log L_x(\lambda) = \left( \sum_{i=1}^N \log\lambda - \lambda x_i\right) = n \left( \log\lambda - \lambda \texttt{mean}(x) \right).
$$

Die Ableitung nach $\lambda$ ist einfach $\frac{n}{\lambda} - n \texttt{mean}(x)$, eine Nullstelle liegt bei $\hat{\lambda} = \frac{1}{\texttt{mean}(x)}$. Die zweite Ableitung von $l_x$ ist $-\frac{n}{\lambda^2}$, was bei $\hat{\lambda}$ den Wert $-n{\texttt{mean}(x)}^2 < 0$ annimmt, also ist $\hat{\lambda}$ ein Maximum und wir haben den Maximum-Likelihood-Schätzer bestimmt.

Wir rechnen also mit einer mittleren Wartezeit zwischen den Server-Aufrufen von $\texttt{mean}(x)$, wenn $x$ die beobachteten Wartezeiten sind.
:::

:::{admonition} Beispiel
Der k-Means-Algorithmus (siehe das Kapitel [k-Means](kmeans.ipynb)) kann als Schätzer interpretiert werden:
das statistische Modell ist $\mathcal{X} = \mathbb{R}^{nN}$, wenn $n$ die Dimension der Daten ist (also bei $4$ reellen Variablen, etwa im Iris-Datensatz, $n=4$) und $N$ die Stichprobengröße (bei Iris ist $N=150$).

Der Parameterraum ist $\mathbb{R}^{nk}$ und die Verteilung zu einem Parameter $\theta = (c_1,\dots,c_k) \in \mathbb{R}^{nk}$ (mit $c_i \in \mathbb{R}^n$) ist ein gemischtes Modell aus multivariaten Normalverteilungen mit Erwartungswert $c_i$ und der $n\times n$-Einheitsmatrix als Kovarianzmatrix.

Die 'perfekte' k-Means-Lösung, also die Zentroide $(c_1,\dots,c_k)$, die der k-Means-Algorithmus versucht, zu bestimmen, sind diejenigen, für die die Summe der quadrierten euklidischen Abstände eines jeden Punktes $x_i$ eines Samples $x \in \mathcal{X}$ zu seinem nächsten Zentroid minimal ist. Das sind genau die Zentroide, für die die Likelihood der Daten unter der entsprechenden gemischten Verteilung maximal wird.
:::

Das führt uns auf eine offensichtliche Verallgemeinerung des k-Means-Verfahrens: wir könnten kompliziertere Kovarianzmatrizen erlauben, und damit die Likelihood weiter vergrößern. Das auftretende Problem ist dann allerdings, dass sich auch für die log-Likelihood keine geschlossene Form bestimmen lässt, und man sich einen neuen Algorithmus zur Schätzung überlegen muss!
