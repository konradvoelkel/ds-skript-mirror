# Herleitung des mathematischen Formalismus der Stochastik

Sie haben bereits in Mathematik für Informatik 3 die Grundlagen der (diskreten) Wahrscheinlichkeitstheorie kennen gelernt. Wir werden diese auch noch im für uns nötigen Umfang wiederholen. In der Vorlesung werden wir vor allem die Begrifflichkeiten der Wahrscheinlichkeitsmassefunktion (für diskrete Zufallsvariablen) und Wahrscheinlichkeitsdichtefunktion (für stetige Zufallsvariablen) verwenden, die aber beide auf dem Begriff des Wahrscheinlichkeitsmaß aufbauen. An dieser Stelle gibt es einen kleinen Exkurs, um zu erklären, warum es eigentlich genau so gemacht wird, und wie man auf den Begriff des Wahrscheinlichkeitsmaßes kommen kann. Der Begriff der Sigma-Algebra ($\sigma$-Algebra) und der messbaren Funktionen sind essentiell, um in der Stochastik Beweise zu führen und auch um komplexere Begriffe (wie sie etwa in der Finanzmathematik oder in der Theorie des maschinellen Lernens benötigt werden) einzuführen - wir können uns hier damit begnügen, mitzunehmen, wann wir über diese Begriffe hinweglesen können.

Man kann Stochastik als Oberbegriff für Wahrscheinlichkeitstheorie und Statistik auffassen. Die Statistik beschäftigt sich mit stochastischen Modellen, die anhand von Beobachtungen entwickelt werden, und macht Schlussfolgerungen. Die Wahrscheinlichkeitstheorie beschäftigt sich mit der Untersuchung von Modellen und der Theorie dahinter.

Wie immer in der Informatik ist ein wesentliches Ziel, mit einem Modell einen Ausschnitt der Realität zu modellieren, d.h. von diesem Ausschnitt zu abstrahieren und mit dem Modell ein Stück der Realität vorherzusagen und das Modell an der Realität zu prüfen.

Wir kennen bereits logische Modelle der Realität: Wenn es regnet, wird der Rasen nass. Wenn ich hungrig bin, und dann viel esse, bin ich danach nicht mehr hungrig.
Statistische Modelle erweitern diese Alles-oder-nichts-Logik nun um verschiedene Grade von Plausibilität: wenn der Rasen nass ist, ist es plausible, anzunehmen, dass es vor kurzem regnete. Es ist ebenso plausibel, anzunehmen, dass jemand den Rasen gewässert hat mit einem Gartenschlauch. Was wir plausibler finden, hängt davon ab, was wir sonst über die Realität wissen. Durch längere Beobachtung des Rasens können wir feststellen, welche Gründe wie oft zu einem nassen Rasen führen, und daran unser Modell schärfen.

Um mit Plausibilität genau so rechnen zu können wie mit Boolescher Logik, und schließlich auch im Computer zu implementieren, müssen wir die Plausibilitätswerte mit Zahlen versehen. Eine geeignete Abstraktion sind reelle Zahlen, denn reelle Zahlen sind der einzige archimedisch angeordnete vollständige Körper, der die rationalen Zahlen enthält (und die darin enthaltene Unteralgebra der berechenbaren reellen Zahlen hat uns schon viele gute Dienste geleistet).

Wir wünschen uns außerdem, dass Plausibilitätslogik mit der klassischen Logik kompatibel ist, d.h. logisch äquivalente Aussagen sollten gleich plausibel sein und verschiedene Wege, um die Plausibilität einer Aussage zu bestimmen, sollten zum gleichen Ergebnis kommen (Konsistenz).
Um das in Mathematik zu formulieren, nennen wir nun eine endliche Menge von Aussagen, deren Plausibilität wir bewerten wollen, $\mathcal{A}$ und die Zuordnung der Plausibilität ist eine Abbildung $p \colon \mathcal{A} \to \mathbb{R}$.

Wenn man diese Forderungen präzisiert, kann man das [Cox-Jaynes-Theorem](https://en.wikipedia.org/wiki/Cox%27s_theorem) beweisen, dass besagt, dass es eine mathematische Abbildung $cj$ von den reellen Zahlen in das geschlossene Intervall $[0,1]$ gibt, die Plausibilitäten auf "Wahrscheinlichkeiten" abbildet, sodass (fast) alle Regeln der klassischen Wahrscheinlichkeitstheorie erfüllt sind. So erfüllt $P := cj \circ p \colon X \to [0,1]$ die Regeln
1. $P(WAHR) = 1$ und $P(FALSCH) = 0$.
1. Wenn $A_1,\dots,A_n$ eine endliche Menge paarweise unvereinbarer (sich gegenseitig ausschließender) Aussagen sind, dann gilt endliche Additivität:
$ P\left( \bigcup_{i=1} A_i \right) = \sum_{i=1}^n P(A_i) $

Wir werden uns nun der modernen Fassung des Wahrscheinlichkeitsbegriffs nähern. Dabei soll der Begriff der sigma-Algebra hier nur erwähnt werden, man darf ihn danach (für diese Vorlesung) wieder vergessen.

## Exkurs (optional): Das Maßproblem

:::{note}
Dieser und der folgende Exkurs sind reine Hintergrundlektüre und **nicht Teil des Kurses** (nicht klausurrelevant). Sie erklären, warum die Definitionen im Abschnitt *Formalismus* so aussehen, wie sie aussehen. Wer sie überspringt, kann direkt beim Abschnitt *Formalismus* weiterlesen.
:::

Bei einem Würfel oder einer Münze ist relativ klar, wie wir die Wahrscheinlichkeit modellieren und wie wir ein statistisches Modell aufstellen können, das wir auch implementieren können. In der Theorie stellt sich aber schnell die Frage, wie es z.B. mit einem unendlich oft wiederholten Experiment aussieht. Das ist keine rein theoretische Frage, denn wir sind an der Asymptotik interessiert, also wie sich ein hinreichend oft wiederholtes Experiment näherungsweise verhält.

Unendlich oft wiederholte Münzwürfe können wir wie eine unendliche Folge von $0$en und $1$en notieren, und bei näherer Betrachtung liefert uns das auch eine Darstellung für reelle Zahlen im Einheitsintervall $[0,1]$, die sich im Rechner eben so gut implementieren lässt, wie der Rechner eine Turingmaschine ist (in der Realität ist das Band endlich, aber wir können es ja immer wieder verlängern - bzw. der Speicher unserer Rechner ist beschränkt aber nicht auf einen festen Wert).

Wir möchten nun gerne jedem Ergebnis (jedem Versuchsausgang beim unendlich oft wiederholten Münzwurf) eine Wahrscheinlichkeit zuordnen, sodass $P(\Omega)=1$ ist, wobei $\Omega = \{0,1\}^{\mathbb{N}}$ der Ergebnisraum ist.
Außerdem soll für paarweise disjunkte Teilmengen $A_i \subseteq \Omega$ die endliche Additivität gelten:

$P\left( \bigcup_{i=1}^n A_i \right) = \sum_{i=1}^n P(A_i)$

Eine weitere natürliche Forderung ist die Flip-Invarianz, also dass es für die Wahrscheinlichkeit keinen Unterschied macht, ob ich den $n$-ten Münzwurf (das $n$-te bit) genau umdrehe. Man kann das formalisieren über einen Operator $F_n \colon \Omega \to \Omega$ mit

$F_n(\omega_1,\dots,\omega_{n-1},\omega_n,\omega_{n+1},\dots) =
     (\omega_1,\dots,\omega_{n-1},1-\omega_n,\omega_{n+1},\dots)$
     
Dann erwarten wir für jede Teilmenge $A \subseteq \Omega$ dass $P(F_n A) = P(A)$ gilt.

Im Jahr 1923 hat Banach mit Hilfe des Auswahlaxioms bewiesen, dass es zwar möglich ist, nicht-konstruktiv so eine Wahrscheinlichkeit $P$ zu definieren, dass es aber nicht eindeutig möglich ist!

Wenn wir eine unserer Forderungen verschärfen, nämlich von der endlichen Additivität zur $\sigma$-Additivität (man sagt Sigma-Additivität oder abzählbare Additivität), [hat schon 1905 Vitali bewiesen](https://de.wikipedia.org/wiki/Ma%C3%9Fproblem#Unl%C3%B6sbarkeit_des_Ma%C3%9Fproblems), dass es überhaupt keine solche Abbildung $P$ gibt, es also unmöglich ist, unendlichen Münzwürfen so Wahrscheinlichkeiten zuzuordnen. Woran liegt das, und was soll das mit der $\sigma$-Additivität?

## Exkurs (optional): Offene Mengen messen

Eine sehr praktische Definition für jede Menge $M$ auf der es einen Abstandsbegriff gibt (genauer: $M$ ein metrischer Raum) ist diese:
Eine Menge $U \subseteq M$ heißt *offen* wenn es um jeden Punkt $u \in U$ einen Abstand $\epsilon > 0$ gibt, sodass alle Punkte $x \in M$ mit Abstand $d(x,u) < \epsilon$ bereits gänzlich in $U$ liegen, also $x \in U$. Für $M=\mathbb{R}$ sind z.B. endliche Vereinigungen von offenen Intervallen solche offenen Mengen, daher der Name.

Man kann nun zeigen, dass die klassische $\epsilon$-$\delta$-Definition von Stetigkeit äquivalent ist zu: $f \colon X \to Y$ heißt *stetig* wenn die Urbilder offener Mengen $U \subseteq Y$ auch offene Mengen $f^{-1}(U) \subseteq M$ sind.

Wenn wir auf den Zahlen im Intervall $[0,1]$ eine Gleichverteilung definieren wollen (so wie im unendlichen Münzwurf-Beispiel), oder auch gleich auf allen reellen Zahlen, dann wissen wir eigentlich schon ganz genau, wie wir mit Intervallen verfahren wollen: für ein Intervall $[a,b]$ soll die Wahrscheinlichkeit / das Maß eben $b-a$ sein.

Da sich jede offene Menge in $\mathbb{R}$ als abzählbare Vereinigung von Intervallen schreiben lässt, wissen wir also, wie den offenen Mengen ein Maß zugeordnet werden kann: als abzählbare Summe über die Längen eben dieser Intervalle. Es stellt sich heraus, dass man so eine Gleichverteilung definieren kann, nur eben nicht für beliebige Teilmengen von $\mathbb{R}$ oder $[0,1]$ einen Wahrscheinlichkeitswert bestimmen. Man sagt, es gibt *nicht-messbare Mengen*.

Aus dieser Beobachtung leiten wir nun die Forderung ab, dass unsere Wahrscheinlichkeit $P$ nicht nur endlich additiv sein soll, sondern $\sigma$-additiv. Nach dem Satz von Vitali akzeptieren wir, dass nicht jede Teilmenge von $\mathbb{R}$ messbar ist und begnügen uns damit, eine Teilalgebra von $\mathcal{P}(\mathbb{R})$ auszuzeichen, die *messbaren Mengen*.

## Formalismus

:::{admonition} Definition
Sei $\Omega$ eine Menge. Dann heißt ein Mengensystem $\mathcal{F} \subseteq \mathcal{P}(\Omega)$ eine *$\sigma$-Algebra*, wenn
1. $\Omega \in \mathcal{F}$ "WAHR ist messbar"
1. $A \in \mathcal{F} \implies A^c := \Omega - A \in \mathcal{F}$ "logisches NICHT"
1. $A_1,\dots \in \mathcal{F} \implies \bigcup_{i\geq 1} A_i \in \mathcal{F}$ "logisches ODER"

Terminologie: wir nennen die Elemente von $\Omega$ die *Ergebnisse* und die Elemente von $\mathcal{F}$ die messbaren Teilmengen oder auch *Ereignisse*. Das Paar $(\Omega,\mathcal{F})$ ist ein *Ereignisraum*.
:::

:::{admonition} Beispiel
ein gewöhnlicher Würfel hat Zustandsraum $\Omega = \{1,2,3,4,5,6\}$ und die Potenzmenge $\mathcal{P}(\Omega)$ ist bereits eine $\sigma$-Algebra (es gibt also keine nicht-messbaren Mengen - das klappt für endliches $\Omega$ immer). Ein einzelner Würfelwurf liefert ein Ergebnis, die Augenzahl. Die Aussage "die Würfelaugen sind eine gerade Zahl" ist eine logische Aussage, die zu dem Ereignis $\{2,4,6\} \subseteq \Omega$ korrespondiert. In sehr vielen Fällen sind wir (notgedrungen) nicht an konkreten Ergebnissen interessiert, sondern an bestimmten Ereignissen.
:::

Merkregel: wenn unklar ist, was die $\sigma$-Algebra sein soll, ist es $\mathcal{P}(\Omega)$; mit anderen Worten: wenn unklar ist, was eine "messbare Menge" sein soll, ist einfach nur "Menge" gemeint.

:::{admonition} Definition
Eine Funktion $P \colon \mathcal{F} \to [0,1]$ von einer $\sigma$-Algebra auf einer Menge $\Omega$ in das Einheitsintervall heißt *Wahrscheinlichkeitsmaß* wenn
1. $P(\Omega) = 1$ (Normierung) und
1. Für paarweise disjunkte Ereignisse $A_i \in \mathcal{F}$ gilt $\sigma$-Additivität:
$P \left( \bigcup_{i\geq 1} A_i \right) = \sum_{i\geq 1} P(A_i)$

Das Tripel $(\Omega, \mathcal{F}, P)$ heißt *Wahrscheinlichkeitsraum*.
:::

Vergleichen Sie dazu im Skript "Mathematik für Informatik" Definition 12.2.5 sowie Bemerkung 12.2.8, in der als Spezialfall $\mathcal{F} = \mathcal{P}(\Omega)$ und $\Omega$ endlich angenommen werden.

:::{admonition} Beispiel
Auf einer endlichen Menge $\Omega$ von Kardinalität $N := |\Omega|$ (also Anzahl der Elemente $N$) ist mit $\mathcal{F} := \mathcal{P}(\Omega)$ und $P(A) := |A| / N$ ein Wahrscheinlichkeitsmaß definiert, dass wir *Gleichverteilung* nennen.
:::

:::{admonition} Beispiel
Für einen beliebigen Ereignisraum $(\Omega,\mathcal{F})$ und ein festes Element $\xi \in \Omega$ ist mit

$\delta_\xi := A \mapsto \begin{cases} 1 & \xi \in A,\\ 0 & \text{sonst} \end{cases}$

ein Wahrscheinlichkeitsmaß definiert, das *Dirac-Maß* mit Einheitsmasse am Punkt $\xi$.
:::

:::{admonition} Proposition
**Rechenregeln** für Wahrscheinlichkeitsmaße:
Für jeden Wahrscheinlichkeitsraum $(\Omega,\mathcal{F},P)$ mit $A,B \in \mathcal{F}$ gilt:
1. $P(\emptyset) = 0$
1. Endliche Additivität: $P(A \cup B) + P(A \cap B) = P(A) + P(B)$
1. Monotonie: $A \subseteq B \implies P(A) \leq P(B)$
1. $\sigma$-Subadditivität: $P \left( \bigcup_{i\geq 1} A_i \right) \leq \sum_{i\geq 1} P(A_i)$
   (wenn die $A_i \in \mathcal{F}$ nicht notwendig disjunkt sind)
:::

:::{admonition} Beweis
1. $1 = P(\Omega) = P(\emptyset \cup \Omega) = P(\emptyset) + P(\Omega) = P(\emptyset) + 1$
1. $P(A \cup B) = P(A \cup (B - A)) = P(A) + P(B - A)$ und
   $P(B - A) + P(A \cap B) = P((B - A) \cup (A \cap B)) = P(B)$ also
   $P(A \cup B) + P(A \cap B) = P(A) + P(B - A) + P(A \cap B) = P(A) + P(B)$
1. $A \subseteq B \implies B = A \cup (B - A)$
   $\phantom{A \subseteq B} \implies P(A) \leq P(A) + P(B - A) = P(A \cup (B - A)) = P(B)$
1. den Leser\*innen als Übung überlassen.
:::

:::{admonition} Definition
Eine Funktion $f \colon \Omega \to \Omega'$ zwischen Wahrscheinlichkeitsräumen $\Omega$ und $\Omega'$ (die $\sigma$-Algebren und Wahrscheinlichkeitsmaße notieren wir nicht mehr extra dazu) heißt *messbar* oder auch *Zufallsvariable* wenn für messbare Mengen $U \subseteq \Omega'$ die Urbilder $f^{-1}(U) \subseteq \Omega$ ebenfalls messbar sind.
:::

Merkregel: wenn unklar ist, was die $\sigma$-Algebren sein sollen, stellen wir uns jede Abbildung (=Funktion) als messbar vor. Das ist strenggenommen in der Regel falsch, sobald wir uns mit stetigen Zufallsvariablen beschäftigen - und wird uns doch in der Praxis nicht stören.

:::{admonition} Beispiel
Wenn wir auf $[0,1]$ die Gleichverteilung definieren, indem wir auf offenen Intervallen die Intervalllänge als Wahrscheinlichkeitsmaß festlegen, so ist jede stetige Funktion $f \colon [0,1] \to [0,1]$ auch messbar.
:::

Der Begriff Zufallsvariable ist sehr irreführend: es gibt hier keine Variable und keinen Zufall. Während der Begriff der messbaren Abbildung auch außerhalb der Wahrscheinlichkeitstheorie sinnvoll ist, hat der Begriff der Zufallsvariable aber eine andere typische Verwendung, andere syntaktische Gepflogenheiten. Wir dürfen uns diese begriffliche Überladung so vorstellen, wie einen API-Wrapper, der uns zusätzlichen syntaktischen Zucker gibt - eine Abbildung, die als Zufallsvariable daher kommt, lässt sich wie eine Variable einsetzen, die zufällige Werte annimmt. Wir werden diese Perspektive noch stärker nutzen und einüben.

Wir wollen uns im Folgenden nicht weiter mit der Maßtheorie beschäftigen, die einiges an Aufwand erfordert, um z.B. das allgemeine Lebesgue-Integral zu definieren. Aufgrund der Anwendungen in der Informatik, insbesondere im maschinellen Lernen wollen wir aber eins festhalten: während das Riemann-Integral durch Approximation mit Flächeninhalten von Rechtecken gebildet wird, bildet man das Lebesgue-Integral durch Approximation der Funktion selbst durch Treppenfunktionen.

:::{admonition} Definition
Eine Treppenfunktion ist eine messbare Funktion, die nur endlich viele verschiedene Werte annimmt.
:::

:::{admonition} Satz
Zu jeder $\sigma$-Algebra auf $\Omega$ und jeder messbaren Funktion $f \colon \Omega \to \mathbb{R}$ gibt es eine Folge von Treppenfunktionen $t_n \colon \Omega \to \mathbb{R}$, die gegen $f$ konvergiert: $t_n \to f$.
:::

Damit lassen sich sehr viele Aussagen beweisen, indem man sie für Treppenfunktionen beweist (so auch die Konstruktion des Lebesgue-Integrals). Man kann daraus auch weitreichende Universalitätsaussagen konstruieren, wenn ein Computermodell in der Lage ist, Treppenfunktionen beliebig genau zu approximieren. Damit lässt sich auch die Universalität von neuronalen Netzen einsehen; die Vorlesung *Einführung in Deep Learning* führt das aus (universelle Approximation).

Zuletzt soll nicht unerwähnt bleiben, dass es einen berechtigten Einwand gegenüber diesem Formalismus gibt: am Rechner lässt sich nur konstruktive Mathematik implementieren, der Satz vom ausgeschlossenen Dritten und das Auswahlaxiom sind nicht implementierbar. In dieser Logik aber (der konstruktivistischen / sogenannten intuitionistischen) lassen sich für einen metrischen Raum $X$ alle Mengen als messbar bezeichnen, weil die nicht-messbaren Teilmengen eben nicht konstruierbar sind. Damit wird manches einfacher, aber eben auch vieles unmöglich. Wir begnügen uns nun also damit, dass wir wissen, wie sich Texte lesen lassen, die den üblichen Formalismus verwenden, und außerdem eine gute Ausrede zur Hand haben, warum wir uns mit dem Formalismus nicht länger auseinander setzen werden.

Sie können also nun ein Stochastik-Buch in die Hand nehmen, dort einen Satz vorfinden "Sei X eine Menge mit einer $\sigma$-Algebra ..." und dabei den Teil mit der $\sigma$-Algebra für's erste überlesen, da Sie in der Praxis den nicht-messbaren Mengen (also denen, die nicht Teil des Mengensystems sind, welches $\sigma$-Algebra genannt wird) nicht über den Weg laufen. Mit anderen Worten: stellen Sie sich in erster Näherung vor, dass "messbar" keine Einschränkung ist. Was wir aber aus diesem Kapitel mindestens mitnehmen sollten ist der Begriff der Zufallsvariable, die Rechenregeln für Wahrscheinlichkeitsmaße $P$ und das wichtige Beispiel der Gleichverteilung.

Wenn Sie sich gern im weiteren Verlauf der Vorlesung mit interaktiven Spielchen der Stochastik nähern wollen, ist [Random Services](
https://randomservices.org/random/prob/index.html) genau das Richtige für Sie.
Wenn Sie es lieber elegant-visuell mögen, wird [Seeing Theory](https://seeing-theory.brown.edu/) Sie durch den Stochastik-Teil der Vorlesung begleiten.

[Wenn Sie in 6 Minuten den Würfelwurf (die Gleichverteilung, auch Laplace-Experiment) nochmal von jemand anderem erklärt haben möchten, können Sie das auf YouTube finden im Kanal musstewissen Mathe](https://www.youtube.com/watch?v=zPcjFWQa6Uc).