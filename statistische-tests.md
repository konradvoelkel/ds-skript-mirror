# Statistische Tests

Bei der explorativen Datenanalyse kommen wir zu Hypothesen, welche Zusammenhänge in den Daten stecken. Bei der Implementierung von Systemen mit maschinellem Lernen müssen wir zahlreiche Entscheidungen treffen, etwa ob wir eine Variable als Normalverteilt annehmen können, ob die Verteilung für zwei Gruppen oder Cluster etwa gleich oder sehr verschieden ist.

Genau genommen gehören statistische Tests nicht in das Gebiet "maschinelles Lernen", aber vom Ablauf der Vorlesung passt es hier ganz gut hin.

Ein Test lässt sich interpretieren als ein Schätzer, der keinen einzelnen Wert, sondern einen ganzen Bereich als mögliche Werte schätzt, gefolgt von einer Entscheidungsregel, die das Schätzergebnis interpretiert hinsichtlich einer Hypothese. Bevor wir uns mit dem Thema oberflächlich beschäftigen, damit wir einordnen können, was ein Test leisten könnte, und was die Grenzen der statistischen Tests sind, schauen wir uns noch an, was der Unterschied zwischen einzelnen Werten und Bereichen von Werten für die Kommunikation von wissenschaftlichen Ergebnissen bzw. Data Science Ergebnissen ausmacht.

## Prognoseintervalle

Wir betrachten zur Motivation die Grafik {ref}`warming-without-confidence` und setzen Sie danach in Bezug zu {ref}`warming-with-confidence`


```{figure} images/global_warming_without_confidence.png
:width: 280px
:align: center
:name: warming-without-confidence

Globale Erwärmung, Projektion (A2r Szenario bei 970 ppmv, IIASA 2009)
```

Gezeigt ist eine Projektion eines statistischen Modells zur Vorhersage der globalen Erwärmung (hier angegeben als Temperaturänderung relativ zum vorindustriellen Niveau, was definiert ist als Temperaturmittelwert der Jahre 1850 bis 1900) unter der Voraussetzung, dass der CO2-Gehalt der Atmosphäre auf 970 ppmv (parts per million by volume) ansteigt (vgl. 30.5.2022: 421 ppmv und 1900: 296 ppmv).
Kontext: das Pariser Klimaschutzabkommen schreibt eine Begrenzung auf 1.5°C bzw. 2°C fest - nicht bis 2040, sondern bis 2100.

Betrachten wir diese Grafik mit den Data Science Augen: was gäbe es daran zu kritisieren?

Ein häufiger Einwand gegenüber solchen Modellen und Grafiken ist, dass es so kommen könnte, genauso gut aber auch ganz anders, da es sich ja nur um theoretische Modelle handle. Die Grafik drückt eine große Sicherheit beim Verlauf der Kurve aus, die so nicht gegeben sein kann - damit ist die Aussage "es wird so kommen" von vornherein unglaubwürdig. Klar: kommuniziert werden soll "es könnte so kommen", aber das ist für sich genommen etwa so nützlich wie "es könnte regnen oder auch trocken bleiben".

Um Entscheidungen auf Grundlage einer statistischen Vorhersage treffen zu können, müssen wir auch wissen, mit welcher Plausibilität die Vorhersage getroffen werden kann. Betrachten wir zum Vergleich {ref}`warming-with-confidence`, eine Grafik aus dem IPCC (Weltklimarat) Bericht SR15, Summary for Policymakers, Figure 1 a) {cite}`sr15`:

```{figure} images/global_warming_with_confidence.png
:width: 480px
:align: center
:name: warming-with-confidence

Globale Erwärmung, Projektion (IPCC SR15, Fig.1)
```

Um diese Grafik richtig lesen zu können, müssen wir noch die *IPCC Calibrated Language* kennen, genau genommen die *Likelihood scale* (dabei beziehen sich AR4 und AR5 auf 'assessment reports', die vor dem Sonderbericht über 1.5°C erschienen sind):

```{figure} images/likelihood-scale.png
:width: 560px
:align: center
:name: likelihood-scale

IPCC Likelihood scale
```

Nun sehen wir, dass es sich beim grau schattierten Bereich um den Bereich handelt, in dem mit mind. $2/3$ Wahrscheinlichkeit die tatsächlichen Messwerte liegen werden (laut Modell). Anhand dieser Information kann man deutlich besser einschätzen, welche zukünftigen Erwärmungen zu erwarten sind, selbst wenn wir 'Glück haben' oder auch wie schlimm es werden könnte, wenn wir 'Pech haben'. Der grau schattierte Bereich ist genau genommen ein **Prognoseintervall**, in dem der tatsächliche Wert in Zukunft mit hoher Wahrscheinlichkeit vermutet wird. Eng verwandt ist ein **Konfidenzintervall**, welches der Bereich ist, in dem der tatsächliche Wert in (z.B.) 95\% der erwarteten Beobachtungen vermutet wird.

Wir verweisen für die mathematische Theorie von Bereichsschätzern / Konfidenzintervallen auf Vorlesungen über Statistik. Unser Ziel soll im Folgenden vor Allem sein, den Begriff des Tests so weit verstanden zu haben, dass wir einordnen können, ob eine angebliche Interpretation eines statistischen Tests seriös ist. Wenn wir das können, wollen wir außerdem in der Lage sein, zu identifizieren, in welchen Situationen ein Hypothesentest sinnvolle Erkenntnisse liefern kann. Dafür wird es vor allem wichtig sein, den Begriff der Signifikanz zu besprechen.


## Ausblick: Konfidenzintervalle

Hinweis: dieser Abschnitt ist vor Allem zum besseren Verständnis statistischer Tests hier, und wird für sich genommen nicht in der Klausur abgefragt.

:::{admonition} Definition
Sei $(\mathcal{X}, P_\theta : \theta \in \Theta)$ ein statistisches Modell, $\Sigma$ eine beliebige Menge und $\tau \colon \Theta \to \Sigma$ eine zu schätzende Größe in Abhängigkeit des Parameters $\theta$. Sei außerdem $0 < \alpha < 1$ eine reelle Zahl.
Eine Abbildung $C \colon \mathcal{X} \to \mathcal{P}(\Sigma)$, die jedem möglichen Beobachtungsergebnis $x \in \mathcal{X}$ eine Menge $C(x) \subseteq \Sigma$ zuordnet, heißt **Konfidenzbereich für $\tau$ zum Irrtumsniveau $\alpha$**, wenn

$$
\inf_{\theta \in \Theta} P_{\theta}\left( x \in \mathcal{X} \colon \tau(\theta) \in C(x) \right) \geq 1 - \alpha.
$$

Wenn außerdem $\Sigma = \mathbb{R}$ und jedes $C(x)$ ein Intervall ist, spricht man von einem **Konfidenzintervall**.
:::

:::{admonition} Beispiel
**Trivialer Fall:**
Der konstante Konfidenzbereich $C(x) := \Sigma$ erfüllt für alle $\theta$ stets $\tau(\theta) \in C(x)$, also ist $P_\theta\left(x \in \mathcal{X} : \tau(\theta) \in C(x)\right) = 1 \geq 1 - \alpha$ für alle $\alpha$.
Das können wir so interpretieren: wir sind uns sicher, dass der 'richtige' Schätzwert im Wertebereich von $\tau$ liegt.
Natürlich ist das kein besonders nützlicher Konfidenzbereich, stellt aber klar, dass der Bereich durchaus 'zu groß' sein darf. Es ist in unserem Interesse, ein $C$ zu finden, sodass die $C(x)$ möglichst klein sind, denn erst dann wird die Aussage interessant.
:::

:::{admonition} Beispiel
**Münzwurf:**
Der $n$-fach wiederholte Münzwurf einer unfairen Münze mit Erfolgswahrscheinlichkeit $p$ lässt sich modellieren mit dem **Binomialmodell**: $\mathcal{X} = \{1,\dots,n\}$ ist die Anzahl der Erfolge, der unbekannte Parameter ist $\theta = p \in \Theta = [0,1]$ und $P_\theta = Bin(n,\theta)$ (und $\tau = id$, also schätzen wir den Parameter $\theta$).

Wir bestimmen den Maximum-Likelihood-Schätzer für $\theta$:

$$
\begin{aligned}
L_x(\theta) &= P_\theta(x|n) = \binom{n}{x} \theta^x (1-\theta)^{n-x} \\
l_x(\theta) &= \log L_x(\theta) = \log\binom{n}{x} + x\log(\theta) + (n-x)\log(1-\theta) \\
l_x'(\theta) &= \dfrac{x}{\theta} - \dfrac{n-x}{1-\theta} \\
l_x'(\theta) &= 0 \implies x(1-\theta) = (n-x)\theta \\
             & \qquad \implies x - \theta x = \theta n - \theta x \\
             & \qquad \implies x = \theta n \\
             & \qquad \implies \theta = \frac{x}{n}.
\end{aligned}
$$

Ganz konkret: werfen wir die Münze $100$ mal und es kommt $45$ mal Zahl, so schätzen wir $\theta$ als $\frac{45}{100}$ (also insbesondere, dass die Münze wirklich unfair ist).
:::

Was aber ist unsere Konfidenz (unser Vertrauen)? Halten wir Werte weit weg von $\frac{x}{n}$ auch für halbwegs plausibel oder können wir einen sehr engen Bereich um $\frac{x}{n}$ bestimmen, den wir für plausibel halten? Im konkreten Beispiel mit der Schätzung $\theta = \frac{45}{100}$, wäre da auch $\theta = \frac{1}{2}$ halbwegs plausibel?

Wir wollen nun Intervalle $C(x) = (\frac{x}{n} - \epsilon, \frac{x}{n} + \epsilon)$ konstruieren mit möglichst kleinem $\epsilon > 0$ sodass die Konfidenzbereich-Bedingung aus der Definition erfüllt ist:

$$
\begin{aligned}
 & \inf_{\theta \in \Theta} P_{\theta}\left( x \in \mathcal{X} \colon \tau(\theta) \in C(x) \right) \geq 1 - \alpha \\
 \Leftrightarrow & \inf_{\theta \in [0,1]} P_{\theta}\left( x \in \mathcal{X} \colon \left|\theta - \frac{x}{n}\right| < \epsilon \right) \geq 1 - \alpha \\
  \Leftrightarrow & \inf_{\theta \in [0,1]} P_{\theta}\left( x \in \mathcal{X} \colon \left|\theta - \frac{x}{n}\right| \geq \epsilon \right) \leq \alpha \\
\end{aligned}
$$

Übersetzt: $\epsilon$ soll so bestimmt werden (in Abhängigkeit von $\alpha$ und auch möglichst klein), dass für einen Anteil von weniger als $\alpha$ der möglichen Stichproben $x$ gilt: $\left|\theta - \frac{x}{n}\right| \geq \epsilon$. Wenn konkret $\alpha = 0.05$ ist (eine häufige Wahl), bedeutet dass, dass unser Schätzfehler nur in 5\% der Stichproben größer als $\epsilon$ ausfällt.

Die Form der Ungleichung darf uns an die Tschebyscheff-Ungleichung erinnern, die wir direkt nach Einführung der Varianz angesehen hatten. Sie sagt uns hier für $T$ den Schätzer $T(x) = \frac{x}{n}$

$$
 P_{\theta}\left( \left|\mathbb{E}(T) - T\right| \geq c \right) \leq \dfrac{\mathbb{V}T}{c^2}
$$

Wir wollen natürlich gerne $c=\epsilon$ verwenden, und das $\epsilon$ in Abhängigkeit von $\alpha$ so wählen, dass auf der rechten Seite der Ungleichung nur noch $\alpha$ steht. Es ist $\mathbb{V}T = n\theta(1-\theta)$, was dummerweise noch von $\theta$ abhängt, welches wir ja nicht kennen!

Daher schätzen wir $\theta(1-\theta) \leq \frac{1}{4}$ ab (klar: bei $\theta = \frac{1}{2}$ gilt Gleichheit, sonst ist es eine echte Ungleichung).

Insgesamt erhalten wir also: $\epsilon$ ist gut gewählt, wenn

$$
\begin{aligned}
           & \dfrac{\mathbb{V}T}{\epsilon^2} \leq \alpha \\
\Leftarrow & \frac{1}{4 n \epsilon^2} \leq \alpha \\
\Leftrightarrow & \frac{1}{4 n \alpha} \leq \epsilon^2 \\
\Leftrightarrow & \frac{1}{2 \sqrt{n \alpha}} \leq \epsilon \\
\Leftarrow & \frac{1}{2 \sqrt{n \alpha}} =: \epsilon.
\end{aligned}
$$

Im konkreten Beispiel mit $\alpha = 0.05$ und $n=100$ erfüllt also $\epsilon := \frac{1}{2\sqrt{5}} \approx 0.2236$ unsere Wünsche.
Das bedeutet für uns: für die konkrete Beobachtung $k=45$ ist nicht nur die Punktschätzung $\frac{45}{100}$ plausibel, auch ungefähr $\frac{23}{100}$ und $\frac{67}{100}$ halten wir für plausibel. Die Münze könnte also durchaus fair sein, wir haben nur eine ungünstige Beobachtung erwischt.

Daran sehen wir, dass die Bestimmung von Konfidenzintervallen mit der Tschebyscheff-Ungleichung sehr große Intervalle liefert. Es gibt mehrere bessere (deutlich kompliziertere!) Methoden, um kleinere Intervalle zu erhalten.

Wir sehen aber auch einen einfachen Zusammenhang zwischen $\epsilon, n$ und $\alpha$: wenn wir $\alpha$ verkleinern (uns also noch sicherer sein wollen), wird $\epsilon$ größer. Wenn wir $n$ vergrößern (also größere Stichproben nehmen), wird $\epsilon$ kleiner.

Damit lässt sich z.B. berechnen, wie groß die Stichprobe ausfallen muss, um mit Gewissheit von mindestens $1-\alpha$ sagen zu können, dass unsere Münze nicht fair ist. Wir nehmen hier wieder konkret an, dass wir für eine Stichprobe $\theta = 0.45$ geschätzt haben.

$$
\begin{aligned}
 & 0.45 + \epsilon < 0.5 \\
\Leftrightarrow & 0.45 + \frac{1}{2 \sqrt{n \alpha}} < 0.5 \\
\Leftrightarrow & \frac{1}{2 \sqrt{n \alpha}} < 0.05 \\
\Leftrightarrow & 2 \sqrt{n \alpha} > \frac{100}{5} \\
\Leftrightarrow & \sqrt{n \alpha} > 10 \\
\Leftrightarrow & n \alpha > 100 \\
\Leftrightarrow & n > \frac{100}{\alpha}
\end{aligned}
$$

setzen wir noch $\alpha = 0.05$ ein, ergibt sich, dass die Stichprobe größer als $2000$ sein sollte, um verwerfen zu können, dass die Münze fair ist. Wenn wir ein clevereres Verfahren zur bestimmung kleinerer Konfidenzintervalle hätten, würde uns allerdings eine kleinere Stichprobe ausreichen.



:::{admonition} Beispiel
**Stichprobe einer Normalverteilung:**
Angenommen, die reelle Zufallsvariable $Z$ ist normalverteilt mit unbekanntem Erwartungswert $\mu$ und unbekannter Varianz $\sigma^2$.
Wir sampeln $Z$ unabhängig und identisch verteilt $n$ mal, und erhalten eine Zufallsvariable $X$ mit Werten in $\mathbb{R}^n$, also $X = (X_1,\dots,X_n)$, wobei $X_i \sim Z$ verteilt ist.

Wir bezeichnen mit $\texttt{mean}(X) = \sum_{i=1}^n \frac{X_i}{n}$ den Stichproben-Mittelwert (Achtung: das ist jetzt eine Zufallsvariable, die sich aus der zufälligen Stichprobe $X$ berechnet) und $S^\ast(X)^2 := \frac{1}{n-1} \sum_{i=1}^n (X_i - \texttt{mean}(X))^2$ die Stichprobenvarianz (mit Bessel-Korrektur, d.h. $n-1$ im Nenner, damit es keinen Bias gibt).
:::

Wir möchten nun wissen, wie gut wir mit $\texttt{mean}(X)$ denn $\mu(Z)$ abschätzen können - wo liegt unsere Konfidenz (unser Vertrauen)?

Die Zufallsvariable $\texttt{mean}(X)$ ist normalverteilt, mit Mittelwert $\mu(Z)$ und Standardabweichung $\dfrac{\sigma(Z)}{\sqrt{n}}$.
Der Schätzfehler, gemessen in der 'Einheit' Standardabweichung von $\texttt{mean}(X)$ ist

$$
\dfrac{\texttt{mean}(X) - \mu(Z)}{\sigma(Z)/\sqrt{n}}
$$

und das ist demnach standardnormalverteilt. Diese Größe hat noch das Problem, dass wir eigentlich $\sigma(Z)$ nicht kennen, aber trotzdem für unsere Schätzung von $\mu(Z)$ gerne den Fehler betrachten wollen. Daher müssen wir $\sigma(Z)$ noch durch unsere Schätzung $S^\ast(X)$ ersetzen.

Die Zufallsvariable 'Stichprobenvarianz' $S^\ast(X)^2$ ist so verteilt, dass $\dfrac{n-1}{\sigma(Z)} S^\ast(X)^2$ einer sogenannten **$\chi^2$-Verteilung** folgt (ein Spezialfall der Gamma-Verteilung).

Die Wahrscheinlichkeitsdichtefunktion der $\chi^2$-Verteilung ist für uns momentan nicht relevant (insbesondere nicht klausurrelevant), der Vollständigkeit halber:

$$
f(x) = \dfrac{1}{2^{\frac{k}{2}} \Gamma\left( \frac{k}{2} \right)} x^{ \frac{k}{2}-1}e^{-\frac{x}{2}}
$$


```{figure} images/chi-quadrat-verteilungen.png
:width: 420px
:align: center
:name: chiquadrat

Chi-Quadrat-Verteilungen mit verschiedenen Parametern (Freiheitsgraden)
```

Der Unterschied zwischen dem geschätzten Mittelwert und dem tatsächlichen Erwartungswert, gemessen in der 'Einheit' Stichprobenstandardabweichung, ist der geschätzte Schätzfehler $T$, eine Statistik, die wir nun betrachten:

$$
T = \dfrac{\texttt{mean}(X) - \mu(Z)}{S^\ast(X)/\sqrt{n}}.
$$

Die Zufallsvariable $T$ folgt einer sogenannten **Student t-Verteilung**, die zumindest auf den ersten Blick einer Normalverteilung ähnelt, aber größere *Tails* hat, also mit höherer Wahrscheinlichkeit Werte weiter weg vom Erwartungswert annimmt. Der einzige Parameter einer Student t-Verteilung ist die Anzahl an Freiheitsgraden $\nu > 0$, hier $\nu = n-1$. Für $\nu$ mindestens $3$ ist der Erwartungswert $0$ und die Varianz $\nu / (\nu - 2)$.

Die Wahrscheinlichkeitsdichtefunktion der Student t-Verteilung ist für uns erstmal nicht so wichtig, der Vollständigkeit halber - so sieht sie aus:

$$
f(t) = \dfrac{1}{\sqrt{\nu} B\left(\frac{1}{2}, \frac{\nu}{2}\right)} {\left( 1 + \dfrac{t^2}{\nu} \right)}^{-\frac{(\nu+1)}{2}}
$$

wobei $B(x,y) = \dfrac{\Gamma(x)\Gamma(y)}{\Gamma(x+y)}$ die Beta-Funktion ist, und die Gamma-Funktion $\Gamma$ auf ganz $\mathbb{R}$ definiert ist und $\Gamma(n+1)=n!$ so interpoliert, dass immer $\Gamma(x)x = \Gamma(x+1)$ gilt (das dürfen wir auch gleich wieder vergessen).

Für $n \to \infty$ konvergiert die Student t-Verteilung gegen die Standardnormalverteilung. Also kodiert die Abweichung der t-Verteilung von einer Normalverteilung genau die Unsicherheit bei kleiner Stichprobengröße.

```{figure} images/student-t-verteilungen.png
:width: 420px
:align: center
:name: studentt

Student t-Verteilungen mit verschiedenen Parametern (Freiheitsgraden)
```

Wir sind nun daran interessiert, wo die Wahrscheinlichkeit für einen großen Schätzfehler
$T = \dfrac{\texttt{mean}(X) - \mu(Z)}{S^\ast(X)/\sqrt{n}}$
klein ist. Nun hängt dieser Schätzfehler nicht von $\mu(Z)$ ab, genauer gesagt, $T$ ist unabhängig von $\mu(Z)$. Das mag unintuitiv sein, weil $\mu(Z)$ in der Formel auftaucht, ist aber dennoch wahr. Man spricht von **Verteilungsfreiheit**.

Zu $\alpha$ wählen wir nun $t$ als das $\frac{\alpha}{2}$-*Quantil* der $t$-Verteilung (mit $n-1$ Freiheitsgraden), das ist genau das kleinste $t$ sodass $P(T < t) \leq \frac{\alpha}{2}$ ist. So etwas hat man früher in Tabellen nachgeschlagen, heute benutzen wir einen Rechner.
Dann ist mit $\epsilon := t\frac{\sigma^\ast(x)}{\sqrt{n}}$ ein Konfidenzintervall für $\mu(Z)$ gegeben durch

$$
C(x) = (\texttt{mean}(x) - \epsilon, \texttt{mean}(x) + \epsilon).
$$

Wir sehen also, dass es schnell kompliziert werden kann, wenn man einen Konfidenzbereich konstruieren möchte. Auf der anderen Seite lässt sich das hier beschriebene Vorgehen (mit der Standardisierung und der Quantiltransformation) auch auf andere Situationen übertragen (was wir aber den Statistikern überlassen wollen).

Mit der Approximation der Binomialverteilung durch eine Normalverteilung und der hier besprochenen Methode, zu Konfidenzintervallen für eine Normalverteilung zu kommen, lassen sich auch bessere Konfidenzintervalle für eine Binomialverteilung finden -- wenngleich kompliziertere Verfahren nochmals deutlich bessere Intervalle liefern.

Uns soll genügen, dass wir nun wissen, wo die $\chi^2$-Verteilung und die Student t-Verteilung herkommen, und damit dürfen wir die konkrete Wahrscheinlichkeitsdichte auch wieder vergessen - das haben die Statistiker zum Glück für uns ausgerechnet und in unsere Python-Pakete implementiert. Wichtig ist vor Allem, dass die naive Annahme, der Schätzfehler sei wieder normalverteilt, im Allgemeinen nicht zutrifft. Wir begegnen diesen Verteilungen wieder bei der Diskussion statistischer Tests, die gewissermaßen auf der Konstruktion von Konfidenzintervallen aufbauen.


## Tests

:::{admonition} Definition
Sei $(\mathcal{X}, P_\theta : \theta \in \Theta)$ ein statistisches Modell und $\Theta = \Theta_0 \cup \Theta_1$ eine disjunkte Zerlegung des Parameterraums in **Nullhypothese** $\theta \in \Theta_0$ und **Alternative** $\theta \in \Theta_1$.
Jede Statistik $\phi \colon \mathcal{X} \to [0,1]$ (die wir als Entscheidungsregel interpretieren) heißt **Test** von $\Theta_0$ gegen $\Theta_1$.
Ein Test heißt **nichtrandomisiert**, wenn $\phi(x)=0$ oder $\phi(x)=1$ für alle $x \in \mathcal{X}$, andernfalls **randomisiert**.
:::

:::{admonition} Definition
Die Wahrscheinlichkeit für einen **Fehler erster Art**, das bedeutet Ablehnung der Nullhypothese (also $\phi(x)=1$) obwohl der wahre Parameter $\theta \in \Theta_0$ ist, ist $\sup_ {\theta \in \Theta_0} \mathbb{E}_\theta(\phi)$ und heißt auch **effektives Niveau** des Tests.
Für ein $\alpha$ größergleich dem effektiven Niveau spricht man auch von einem Test von Niveau $\alpha$.

Die Funktion $G_\phi \colon \Theta \to [0,1]$, gegeben durch $G_\phi(\theta) = \mathbb{E}_\theta(\phi)$, heißt **Gütefunktion** des Tests.
Es ist $1 - G_\phi(\theta)$ die Wahrscheinlichkeit für einen **Fehler zweiter Art**, das bedeutet Akzeptanz der Nullhypothese (also $\phi(x) < 1$) obwohl der wahre Parameter $\theta \in \Theta_1$ ist.
Für $\theta \in \Theta_1$ heißt $G_\phi(\theta)$ auch die **Macht** (oder Stärke, engl. power) von $\phi$ bei $\theta$.
:::

:::{admonition} Definition
Ein Test $\phi$ heißt **gleichmäßig bester Test zum Niveau $\alpha$**, wenn er vom Niveau $\alpha$ ist und jeder andere Test vom Niveau $\alpha$ eine geringere oder gleiche Macht hat.
:::

So ein gleichmäßig bester Test hat also höchstens $\alpha$ Wahrscheinlichkeit für einen Fehler erster Art und unter allen diesen Tests die geringste Wahrscheinlichkeit für einen Fehler zweiter Art.


## Ausblick: Vom Bereichsschätzer zum Test

Wir haben bereits bei der Diskussion eines Konfidenzintervalls für das Binomialmodell gesehen, dass uns dies helfen kann, zu einer Entscheidung zu kommen (konkret: soll ich eine Münze mit $45/100$ Erfolgen als 'unfair' ansehen, oder ist die Abweichung von $50/100$ mit einem Sampling Fehler zu erklären? Oder auch: wie viele weitere Stichproben benötige ich, um diese Frage eindeutig zu klären?)

Man kann diesen Zusammenhang systematisieren, und mit der Begrifflichkeit des Formparameters aus jedem Test einen Bereichsschätzer konstruieren. Wir sehen uns hier nur die andere Richtung an, nämlich wie aus einem Bereichsschätzer ein Test konstruiert wird.

Die Ausgangssituation soll (der Einfachhheit halber) ein parametrisches statistisches Modell $(\mathcal{X}, P_\theta : \theta \in \Theta)$ und ein Intervallschätzer (d.h. ein Konfidenzintervall) $C \colon \mathcal{X} \to \mathcal{P}(\Theta)$ für den Parameter $\theta$ gegeben sein. Stellen wir uns außerdem vor, dass wir einen ausgezeichneten Parameter $\hat{\theta} \in \Theta$ haben, z.B. gegeben durch einen Punktschätzer (etwa den Mittelpunkt des Intervalls $C(x)$).

Die Hypothese ist nun, dass dieser Parameter der wahre Parameter ist.
Während klar ist, dass diese Hypothese im strikten Sinne wahrscheinlich immer falsch ist, so sind wir doch daran interessiert, wann man die Hypothese *sicher* verwerfen kann. Wir setzen also $\Theta_0 := \{\hat{\theta}\}$ und $\Theta_1 := \Theta - \{\hat{\theta}\}$.

Daraus konstruieren wir den Test $T_C \colon \mathcal{X} \to [0,1]$ durch

$$
T_C := 1_{\{ x \in \mathcal{X} | \theta_0 \notin C(x) \}} \text{ (Indikatorfunktion)} 
$$

$$
T_C(x) = \begin{cases} 0 & \theta_0 \in C(x) \\ 1 & \theta_0 \notin C(x) \end{cases}
$$

Das Vorgehen ist also: wir schätzen den Parameter (z.B. mit einem Maximum-Likelihood-Schätzer) mit Hilfe der Daten $x \in \mathcal{X}$ auf $\hat{\theta}$, betrachten das Konfidenzintervall $C(x)$ und fragen, ob darin $\hat{\theta}$ liegt. Wenn ja, dann halten wir an der Hypothese '$\hat{\theta}$ ist der wahre Parameter' fest, ansonsten schlussfolgern wir '$\hat{\theta}$ kann nicht der wahre Parameter sein'.

Interessanter ist der Test natürlich, wenn wir eine andere Quelle für einen möglichen Wert $\hat{\theta}$ haben, z.B. wenn wir danach fragen, ob die Daten gleichverteilt bzw. normalverteilt sind, oder nicht.

## Ausblick: Beste einfache Tests

Wir haben bereits die Definition von Niveau und Macht gesehen, und das übliche Vorgehen, für festes Niveau nach dem mächtigsten Test zu suchen.

:::{admonition} Definition
Wenn es nur zwei mögliche Parameter gibt (man spricht von **einfachen Hypothesen**), also $\Theta_0 = \{\theta_0\}$ und $\Theta_1 = \{\theta_1\}$,
und $f_0$ und $f_1$ die Dichtefunktionen der Verteilungen zu diesen Parametern sind, nennt man

$$
R(x) := \dfrac{f_1(x)}{f_0(x)}
$$

den **Likelihood-Quotienten** und ein Test $\phi \colon \mathcal{X} \to [0,1]$ von der Form

$$
\phi(x) = \begin{cases}
           0 & R(x) < c \\
           1 & R(x) > c
\end{cases}
$$

mit $c \in \mathbb{R}$ heißt **Neyman-Pearson-Test** zum Schwellwert $c$.
:::

Warum heißt $R(x)$ Likelihoood-Quotient? Weil $f_1(x)$ ein Maß für die Wahrscheinlichkeit $P(D|H_1)$ ist und $f_0(x)$ ein Maß für die Wahrscheinlichkeit $P(D|H_0)$ ist, also ist $R$ der Quotient der Likelihoods. Wenn $f_0(x)=0$ ist, setzt man einfach $R = \infty$.

Der Fall $R(x) = c$ hat meist Wahrscheinlichkeit $0$, kann aber auch gesondert behandelt werden (mit einem geeigneten Wert für $\phi(x)$ zwischen $0$ und $1$).

Das **Neyman-Pearson-Lemma** besagt, dass es zu jeder einfachen Hypothese (also $\Theta$ zweielementig) und jedem Niveau $\alpha$ einen Neyman-Pearson-Test gibt (d.h. ein geeignetes $c \in \mathbb{R}$), der das Niveau voll ausschöpft (d.h. effektives Niveau $\alpha$ hat) und jeder solche Test ist ein gleichmäßig bester Test zum Niveau $\alpha$.

Das **Lemma von Stein** macht eine Aussage darüber, wie nützlich zusätzliche Samples sind, um einen Test aussagekräftiger zu machen. Sei ein Niveau $\alpha$ fixiert. Für eine Reihe von Beobachtungen mit jeweils zu jedem $n$ einen Neyman-Pearson-Test $\phi_n$ vom Niveau $\alpha$, der nur von den ersten $n$ Beobachtungen abhängt, strebt die Macht von $\phi_n$ mit zunehmenden Beobachtungen (also $n \to \infty$) gegen $1$, und zwar mit exponentieller Geschwindigkeit. Genauer:

$$
\lim_{n \to \infty} \frac{1}{n} \log\left( 1 - \mathbb{E}_1(\phi_n) \right) = -H(P_0 \Vert P_1)
$$

Je höher also die relative Entropie der beiden möglichen Verteilungen $H(P_0 \Vert P_1)$, desto mehr Macht liefert jedes einzelne zusätzliche Sample.

Der Zusammenhang liegt in der Definition von Neyman-Pearson-Tests und der relativen Entropie - in der Definition der stetigen relativen Entropie kommt der Ausdruck $-f_0(x) \log R(x) = f_0(x)\log \left( \frac{f_0(x)}{f_1(x)} \right)$ vor.

Die Take-Home-Message ist: für einfache Hypothesen gibt es immer beste Tests, und die relative Entropie erlaubt uns, zu quantifizieren, wie wir durch Vergrößern der Stichprobe die Wahrscheinlichkeit für einen Fehler 2ter Art drücken können.

## Der z-Test

Wenn man Daten hat, deren einzelne Datenpunkte unabhängig (und identisch verteilt) sind (also etwa als Stichprobe einer Zufallsvariable), die einer Normalverteilung folgen, und die Stichprobengröße $n$ ist deutlich über $30$, dann kann man einen **z-Test** (auch **Gauß-Test**) machen. Das ist die 'einfachere' Variante vom t-Test (s.u.), bei der man aufgrund der Größe der Stichprobe anstelle einer Student t-Verteilung mit einer Normalverteilung arbeitet.

Bei diesem Test möchte man herausfinden, ob ein Sample $x$ einer Normalverteilung mit Mittelwert $\mu_0$ folgt. Für $\mu_0 = \texttt{mean}(x)$ (den Maximum-Likelihood-Schätzer) ist nichts zu testen - wir schlussfolgern sofort, dass $\mu = \mu_0$ plausibel ist. Was aber ist mit Werten $\neq \texttt{mean}(x)$? Angenommen, unsere Stichprobe folgt *beinahe* einer Standardnormalverteilung - dann wäre es sinnvoll, einen Test zu machen, ob die Hypothese einer Standardnormalverteilung angenommen oder verworfen werden soll, auch wenn der Maximum-Likelihood-Schätzer etwas anderes als $0$ als $\mu$ schätzt.

Die **z-Statistik** ist

$$
Z(x) = \dfrac{\texttt{mean}(x) - \mu_0}{\sigma/\sqrt{n}}
$$

Aus $\mu_0$ berechnet man eine geschätzte Standardabweichung $\sigma$, wenn die exakte Standardabweichung nicht bekannt ist.
Die Zufallsvariable $Z$ ist standardnormalverteilt.

Bei einem beidseitigem z-Test ist die Nullhypothese $H_0 := (\mu = \mu_0)$, das entspricht $\Theta_0 = \{\mu_0\}$ und die Alternative ist $H_1 = (\mu \neq \mu_0)$, das entspricht $\Theta_1 = \mathbb{R} \setminus \{\mu_0\}$.

Wir wählen ein Niveau $\alpha$, z.B. $\alpha = 0.05$.
Da wir einen beidseitigen Test machen wollen, betrachten wir den z-Wert von $1 - \alpha/2$ (z.B. aus einer Tabelle mit z-Werten oder mit `scipy.stats.zscore`. Für $\alpha = 0.05$ ist der z-Wert $\pm 1.96$.
Der z-Wert $z(p)$ ist das $p$-Quantil einer Standardnormalverteilung, also $P(Z \leq z(p)) = p$,
hier konkret $P(Z \leq 1.96) = 0.975$.
Da die Standardnormalverteilung symmetrisch ist, gilt auch $P(Z \geq -1.96) = 0.975$ und $P(-1.96 \leq Z \leq 1.96) = 0.95$.

Wir berechnen also die z-Statistik unseres Samples und vergleichen das Ergebnis mit dem z-Wert $1.96$. Liegen wir dazwischen, also $-1.96 \leq Z(x) \leq 1.96$, so nehmen wir die Nullhypothese an. Liegt die z-Statistik außerhalb von $[-1.96, 1.96]$, so verwerfen wir die Hypothese.

## Der Student t-Test

Bei kleinen Stichproben macht sich die Verzerrung der geschätzten Parameter einer Normalverteilung bemerkbar und man muss mit der tatsächlichen Verteilung der **t-Statistik** rechnen. Wenn also $\mu_0$ der Parameter ist, auf den man testen möchte, so betrachtet man

$$
t(x) = \dfrac{\texttt{mean}(x) - \mu_0}{\sigma^\ast(x)/\sqrt{n}}
$$

Dabei ist $\sigma^\ast(x)$ der erwartungstreue Schätzer für $\sigma$.

Wie zuvor bei der Konstruktion von Konfidenzintervallen besprochen, folgt $t$ einer Student t-Verteilung. Um den Test durchzuführen zu einem Niveau $\alpha$ müssen wir daher den t-Wert zu diesem Niveau in einer Tabelle nachschlagen oder mit Python ausrechnen über `scipy.stats.t.ppf(p, n-1)` (ppf ist die **percent point function**, die uns das p-Quantil der t-Verteilung mit $n-1$ Freiheitsgraden ausgibt).

Wir berechnen die t-Statistik auf den Daten $x$ und vergleichen sie mit dem zuvor berechneten 'kritischen' t-Wert. Liegen wir mit der t-Statistik zwischen $\pm$ dem kritischen t-Wert, so nehmen wir die Hypothese an (dass $\mu_0$ der Erwartungswert der Verteilung ist).

Diesen beidseitigen t-Test können wir auch direkt mit SciPy ausrechnen lassen:
`scipy.stats.ttest_1samp(x, mu)`

Genau genommen kann dieser t-Test noch mehr: anstatt die Verteilung von $x$ mit einer Normalverteilung mit Mittelwert $\mu$ und der gleichen Varianz wie $x$ zu vergleichen, können wir auch zwei Samples $x,y$ vergleichen (die nicht gleich groß sein müssen), ob die Mittelwerte übereinstimmen (unter der Voraussetzung, dass beide Samples normalverteilt mit gleicher Varianz sind, und dass beide Samples voneinander unabhängig sind) mit `scipy.stats.ttest_ind(x, y)`. Davon ist $y = \texttt{mu}$ ein Spezialfall (aber der Aufruf mit eingesetztem $y$ wird nur `NaN`s zurückgeben - weil die Varianz eines einelementigen Samples $0$ ist; daher `ttest_1samp`).

Der Rückgabewert von SciPy's t-test ist ein `Ttest_indResult`, das ist definiert als `namedtuple('Ttest_indResult', ('statistic', 'pvalue'))`.
Ein `namedtuple` verhält sich zu `tuple` wie ein Dictionary zu einer Liste. Anders formuliert, ist ein named tuple eine immutable Version eines Dictionary.
Der Rückgabewert `statistic` ist die berechnete t-Statistik (da noch kein $\alpha$ involviert war, müsste man diese noch von Hand mit dem kritischen t-Wert vergleichen, um zum Testergebnis zu kommen).
Der Rückgabewert `pvalue` ist der **p-Wert** (auch: die **Signifikanz**) des Testergebnisses, das ist die Wahrscheinlichkeit $p = P(D|H_0) = P(X=x | H_0)$.
Der Name kommt von 'probabilitas' und das Wort 'Signifikanz' erweckt natürlich gewisse Assoziationen.
Wenn $p < \alpha$, so verwerfen wir die Nullhypothese, sonst nehmen wir sie an.

Intern verwendet SciPy die Methode
```python
ttest_ind_from_stats(mean1, std1, nobs1,
                     mean2, std2, nobs2,
                     equal_var=True,
                     alternative="two-sided")
```

und mit `alternative` wird kodiert, ob ein beidseitiger oder einseitiger (`less` oder `greater`) durchgeführt werden soll. Die Variable `nobs` ist die Anzahl an Beobachtungen. Wenn `equal_var` auf `False` gesetzt wird, fällt die Annahme gleicher Varianz weg, dann wird kein gewöhnlicher t-Test sondern Welch's t-Test durchgeführt, bei dem die Zahl der Freiheitsgrade anders berechnet wird.

Wenn die Grundannahme gleicher Varianz bei zwei Samples nicht zutrifft, kann eine Skalentransformation (etwa durch einen Logarithmus) diesen Zustand manchmal herbeiführen (wenigstens approximativ) und damit den t-Test auch in diesen Fällen nützlich machen. Wenn die Varianz deutlich abweicht, sollte man auch die Finger vom t-Test lassen, weil er nicht aussagekräftig ist.

## Ausblick: ANOVA

Eine Verallgemeinerung des t-Tests auf mehr als $2$ Stichprobengruppen ist ANOVA, das steht für **Analysis of Variance**. Die Voraussetzungen sind dabei die gleichen wie beim t-Test:

* Die Beobachtungen sind unabhängig voneinander
* Die Residuen (das sind die Differenzen $x_i-\texttt{mean}(x)$, eine Schätzung des tatsächlichen Samplingfehlers) sind normalverteilt
* Homoskedastizität - das bedeutet Varianzhomogenität, also dass die Varianzen der Stichprobengruppen gleich sind.

Die Anwendung ist in der Regel auf eine kategorielle Variable mit $k$ Ausprägungen, dann teilt man eine Stichprobe in $k$ Gruppen auf (je nach Ausprägung) und betrachtet ANOVA für diese Gruppen. Wenn dabei eine Signifikante Abweichung auftaucht (also ein p-Wert kleiner $0.05$), so verwerfen wir die Nullhypothese, dass die Gruppen gleiche Erwartungswerte haben - und schlußfolgern damit, dass vermutlich die kategorielle Variable einen Einfluss auf den Erwartungswert hat.

Wenn keine signifikante Abweichung auftaucht (p-Wert größergeich $0.05$), dann sehen wir zwar vielleicht eine Abweichung der verschiedenen Mittelwerte, aber eben nur so wenig, wie sich durch einen Samplingfehler gut erklären lässt - einen Einfluss der kategoriellen Variable kann man so nicht sehen.

Vorsicht: das bedeutet nicht, dass die kategorielle Variable keinen Einfluss auf die Mittelwerte hat! Es bedeutet nur, dass unsere Stichprobe nicht in der Lage ist, diesen von einem Stichprobenfehler zu unterscheiden.
'Wir wissen, dass wir nichts wissen'.

In Python benutzen wir `scipy.stats.f_oneway`.

## Signifikanz

Zur Publikation in wichtigen Fachzeitschriften müssen Studien oft Ergebnisse vorweisen, die statistischen Tests genügen, deren Signifikanz (p-Wert) unter dem Schwellwert $0.05$ liegt - man sagt, das Ergebnis ist signifikant.
Das Vorgehen dabei ist: man formuliert das, was man widerlegen (falsifizieren) will, als Nullhypothese. Bei einem p-Wert kleiner $0.05$ verwirft man diese Hypothese.
Nochmal zur Erinnerung: **Fehler erster Art** ist falsche Ablehnung der Nullhypothese. Kleine p-Werte verleiten also zum Fehler erster Art.

Das ist leider problematisch, denn

* auch signifikante Ergebnisse können völlig zufällig sein,
* es gibt Tricks, den p-Wert systematisch zu verkleinern ohne ernsthaft mehr Kenntnis über die Fragestellung zu erlangen (p-value hacking, vgl. {ref}`pvalue-hacking`),
* auch nichtsignifikante Ergebnisse können wissenschaftlich relevant sein,
* der p-Wert wird sehr häufig falsch interpretiert. {cite}`haller`

```{figure} images/xkcd-significant.png
:width: 300px
:align: center
:name: xkcd-significant

XKCD 882: Significant (So, uh, we did the green study again and got no link. It was probably a-- "RESEARCH CONFLICTED ON GREEN JELLY BEAN/ACNE LINK; MORE STUDY RECOMMENDED!")
```

**Most Published Research Findings Are False**

[Ioannidis JPA (2005) Why Most Published Research Findings Are False.
PLOS Medicine 2(8): e124.](https://doi.org/10.1371/journal.pmed.0020124)

> “the probability that a research finding is indeed true depends on the prior probability of it being true (before doing the study), the statistical power of the study, and the level of statistical significance”

Je unplausibler die Hypothese (niedrige prior probability), desto höher ist die Wahrscheinlichkeit, dass sich ein aufregender Befund als Fehlalarm entpuppt, unabhängig vom p-Wert.

Ein sehr wichtiger Baustein um p-value-hacking zu unterbinden ist die Vorregistrierung von Studien. So verhindert man, dass nicht-signifikante Ergebnisse systematisch unterdrückt werden.

```{figure} images/pvalue-hacking.png
:width: 600px
:align: center
:name: pvalue-hacking

[Zusammenstellung von Uri Simonsohn, 2015](http://datacolada.org/41)
```

## Was als Hypothese formulieren, was als Alternative?

Das übliche Vorgehen ist, dass man eine wissenschaftliche Erkenntnis, die man machen möchte, formuliert als das Verwerfen der Nullhypothese. Es macht einen Unterschied, welche Aussage man als Hypothese, welche als Alternative formuliert, denn wir haben beste Tests so definiert, dass der Fehler erster und zweiter Art unterschiedliche Rollen spielen - den Fehler erster Art halten wir genau auf dem Niveau $\alpha$ und minimieren unter dieser Randbedingung den Fehler zweiter Art.

:::{admonition} Beispiel
Stellen wir uns vor, wir hätten ein neues Medikament gefunden, von dem wir glauben, dass es schlauer macht. Um das zu zeigen, gehen wir so vor: wir konstruieren ein Experiment, mit dem sich widerlegen lässt, dass unser Medikament schlauer macht. Dazu operationalisieren wir "schlauer werden" z.B. über eine Prüfungssituation mit kognitiven Aufgaben. Die Probanden, wenigstens 30 an der Zahl, werden zufällig in zwei Gruppen aufgeteilt. Eine Gruppe bekommt ein Placebo, die andere das Medikament, sonst ist alles gleich und niemand (auch die Durchführenden nicht) weiß, wer in welcher Gruppe ist. Danach wertet man die Daten aus - Performance in der Prüfung ist eine Variable, Gruppenzugehörigkeit die andere.

Die Nullhypothese ist nun: das Medikament wirkt nicht. Die Alternative ist, dass das Medikament schlauer macht. Wenn wir die Performance als normalverteilt annehmen, können wir einen zwei-Sample-t-Test machen. Wenn $p < 0.05$ ist, verwerfen wir die Nullhypothese, schließen also, dass diese Beobachtung kein Zufall sein kann, sondern die Variable 'Gruppenzugehörigkeit' einen signifikanten Einfluss auf die Performance hat.
:::

Wenn $p < 0.05$ ist, kann natürlich immer noch ein Fehler erster Art auftreten, denn $0.05 \neq 0$.
Die Nullhypothese war $\mu_1 = \mu_2$, wenn $\mu_i$ die Mittelwerte aus den beiden Gruppen sind. Die Alternative $\mu_1 \neq \mu_2$. In unserer Herleitung vom t-Test haben wir die t-Statistik aufgestellt und dabei den Mittelwert des Samples mit einem fixen $\mu_0$ verglichen. Dabei lässt sich die Rolle von Hypothese und Alternative nicht vertauschen!

Man sieht diese Nicht-Vertauschbarkeit auch bei der natürlichsprachlich formulierten Hypothese: "das Medikament wirkt nicht" ist eigentlich die Aussage "das Medikament einzunehmen oder nicht hat keinen Einfluss auf die Testperformance". Wir formalisiert man "hat einen Einfluss auf die Testperformance" mathematisch?

Was man wiederum machen kann ist ein Test auf einen explizit beschriebenen Zusammenhang, z.B. die Hypothese, dass man nach Einnahme des Medikaments genau 10 Punkte mehr im Test macht, also die Gleichung $\mu_1 + 10 = \mu_2$. Man beachte, dass dies wieder eine Gleichung ist, hingegen $\mu_1 \neq \mu_2$ nicht ebenso getestet werden kann.



## Ausblick: Anwendung weiterer nützlicher Tests

Wir könnten noch eine ganze Reihe Tests benötigen, und deren Voraussetzungen, und wie man diese mit Python auf einem Pandas Datensatz durchführt. Die Anwendungen liegen in der explorativen Datenanalyse (wie ist eine Variable verteilt?), dem Daten putzen (wo liegen Ausreißer? Welche Variablen sind so stark korreliert, dass ich nur eine davon behalte?), der Datenanalyse (welche statistischen Abhängigkeiten lassen sich modellieren?) und der Vorhersage (Kann ich eine Variable - die Targetvariable - durch die anderen ausdrücken? Das ist supervised learning).

**Ein Sample untersuchen**

* Shapiro-Wilk:
  $H_0$: Das Sample ist normalverteilt
  Voraussetzung: Sample ist iid
  `scipy.stats.shapiro`

**Zwei Samples vergleichen**

* Pearson's Korrelation:
  $H_0$: Die zwei Samples sind unabhängig
  Voraussetzung: beide Samples sind iid und normalverteilt mit gleicher Varianz
  `scipy.stats.pearsonr`
* Chi-Quadrat:
  $H_0$: Die zwei Samples sind unabhängig
  Voraussetzung: die untersuchte Variable ist kategoriell, wenigstens 25 Instanzen pro Eintrag in der Kontingenztabelle
  `scipy.stats.chi2_contingency`

  