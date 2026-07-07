# Grid Modeling

If the example circuits we've seen so far seem complicated to analyze, then this pales in comparison to the complexity of analyzing and operating the electrical grid. The electrical grid may be just another circuit, but it has rapid, far-reaching, and expensive consequences if it fails. If the grid is operated incorrectly, its voltages and frequencies can be put in jeopardy in a matter of seconds or less, creating a risk of cascading failure. Understanding the grid and how it behaves depending on how it's operated is crucial to be able to control it correctly. Grid modeling allows operators to not only stay in control of grid voltages and frequencies, but also to dispatch generators in a way that is cost-optimal.

The grid is modeled as a network of $N$ electrical buses connected by branches. A bus is a shared point of connection that has minimal electrical impedance. Generators and loads are attached to the buses. Each pair of buses $(i, k)$[^1] may be connected by a branch&mdash;such as a power line or transformer&mdash;which has nonzero impedance and can result in voltage and phase differences between buses $i$ and $k$. In the grid, each bus has a specific nominal voltage, typically 4 kV to 765 kV per phase depending on whether it is in the transmission or distribution part of the grid. The sets of buses and branches are denoted $\mathbf{N}$ and $\mathbf{L}$, respectively.

[^1]: Index $k$ is used instead of $j$ to distinguish it from the imaginary unit.

For example, consider {ref}`fig_6_1`. It shows a simple electrical grid with three buses $\mathbf{N} = \{1, 2, 3\}$, two generators (at buses $1$ and $2$), and a load (at bus $3$). Buses $1$ and $2$ are connected by a line branch, and buses $2$ and $3$ are connected by a transformer branch. This type of diagram is called a *single-line diagram* because it depicts the parallel conductors in a single-phase system or balanced three-phase system&mdash;like the electrical grid&mdash;as single lines for the sake of simplicity.

```{figure} img/fig_6_1.png
:width: 64%
:label: fig_6_1

Single-line diagram of an example electrical grid. (The symbol for "Load" should not be confused with the symbol for electrical ground.)
```

{ref}`fig_6_2` shows the circuit diagram that corresponds to the above single-line diagram for a three-phase system. Each bus in the single-line diagram corresponds to a set of three nodes in the circuit (one per phase).

```{figure} img/fig_6_2.png
:label: fig_6_2
:width: 100%

Circuit diagram of the example electrical grid in {ref}`fig_6_1`.
```

Each branch $ik$ has a known series impedance $z_{ik}$ and shunt impedance $z_{ik}^\mathrm{Sh}$ according to the $\Pi$ (Pi) branch model. In grid modeling, these parameters are often expressed as *admittance*: series admittance $y_{ik} = 1 / z_{ik}$ and shunt admittance $y_{ik}^\text{Sh} = 1 / z_{ik}^\text{Sh}$. The $\Pi$ branch model applies the shunt admittance in equal parts on the left and right sides, as shown in {ref}`fig_6_3`. This results in a single/per-phase circuit diagram that looks like the Greek letter $\Pi$, hence the name.

```{figure} img/fig_6_3.png
:width: 64%
:label: fig_6_3

Per-phase power line model (the $\Pi$ branch model).
```

Transformer branches build upon this in order to model nonideal transformers. Transformer branches are modeled as ideal transformers paired with the $\Pi$ branch model, as shown in {ref}`fig_6_4`. A complex-valued voltage ratio $a_{ik}$ is used to model both the transformer's voltage ratio $T_{ik} = |a_{ik}|$ and, in the case of a phase-shifting transformer such as a zigzag transformer, its phase shift $\varphi_{ik} = \arg(a_{ik})$. With the ideal transformer adjacent to bus $i$, bus $i$ is known as the *tap bus* and bus $k$ as the *impedance bus* or *$Z$ bus*.

```{figure} img/fig_6_4.png
:width: 64%
:label: fig_6_4

Per-phase transformer model (the $\Pi$ branch model + ideal transformer).
```

## The Power Flow (PF) Problem

A grid operator must dispatch generators to serve the loads in its grid. Each load consists of a given active power $P^L$ and reactive power $Q^L$. A dispatch specifies the active power $P^G$ at which to operate each generator. Once a grid operator has decided the generator setpoints, they must be able to validate those setpoints. This consists of:

- Validating that power is able to flow through the grid according to the setpoints in a way that satisfies the loads.
- Validating that not too much power is flowing through a given line or transformer, to avoid overloading/overheating it.
- Validating that voltages are within acceptable margins for the sake of the loads.

The task of determining how power will flow through the grid and whether it will satisfy the loads is known as the power flow (PF) problem. Because the grid is a circuit, we can solve the power flow problem the same as we solve any other circuit, by doing nodal analysis and solving a system of KCL equations to determine the voltage at each bus, denoted $V_i = |V_i| \angle \delta_i$. In the three-phase case, the voltage magnitude $|V_i|$ can be assumed to be the same across the three phases at each bus, and the voltage angle $\delta_i$ can be taken for the first phase only, knowing that the other two phases will be $\pm 2 \pi / 3$ radians apart.

For generality, we will model all branches as transformer branches. For line branches, we can simply set $T_{ik} = 1$ and $\varphi_{ik} = 0$. We will call branch $ik$ an *$i$-forward branch* if bus $i$ is the tap bus, or an *$i$-reverse branch* if bus $i$ is the impedance bus. In this sense, the grid model becomes a directed graph rather than an undirected graph, and we must account for the forward and reverse branch directions distinctly. We do this by deriving the current $I_{ik}$ flowing into branch $ik$ from bus $i$ (that is, flowing directly into the ideal transformer), as well as the current $I_{ki}$ flowing into the branch from the opposite bus $k$. To determine $I_{ik}$, we apply KCL by summing the currents out of node $i'$ in {ref}`fig_6_4`:

$$
\begin{aligned}
& - \!\! I_{ik}' + V_i' \, \frac{y_{ik}^\text{Sh}}{2} + (V_i' - V_k) \, y_{ik} = 0 \\
& \implies I_{ik}' = V_i' \left( \frac{y_{ik}}{2} + y_{ik} \right) - V_k \, y_{ik} \\
& \implies I_{ik} a_{ik}^* = V_i \, \frac{1}{a_{ik}} \left( \frac{y_{ik}}{2} + y_{ik} \right) - V_k \, y_{ik} \\
& \implies I_{ik} = V_{ik} \, \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}}{2} + y_{ik} \right) - V_k \, \frac{1}{a_{ik}^*} y_{ik}
\end{aligned}
$$ (eq_I_ik)

And to determine $I_{ki}$, we apply KCL by summing the currents out of node $k'$:

$$
\begin{aligned}
& - \!\! I_{ki} + (V_k - V_i') \, y_{ik} + V_k \frac{y_{ik}^\text{Sh}}{2} = 0 \\
& \implies I_{ki} = V_k \left( y_{ik} + \frac{y_{ik}^\text{Sh}}{2} \right) - V_i' \, y_{ik} \\
& \implies I_{ki} = V_k \left( y_{ik} + \frac{y_{ik}^\text{Sh}}{2} \right) - V_i \, \frac{1}{a_{ik}} y_{ik}
\end{aligned}
$$ (eq_I_ki)

### The Bus Injection Model

To define the power flow problem, we need to formulate a set of power flow equations. The most common formulation is known as the *bus injection model*. We start with KCL, which tells us that at a bus $i$ with nominal voltage $V_i$, the current $(S_i / V_i)^*$ injected due to attached generation and/or load $S_i$ must equal the sum of currents flowing out of the bus:

$$
\begin{aligned}
(S_i / V_i)^*
& = \text{total current out of bus $i$ via $i$-forward branches} \\
& \, + \text{total current out of bus $i$ via $i$-reverse branches} \\
& = \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\!\! I_{ik} + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\!\! I_{ik}
\end{aligned}
$$

The subscript "$k \! : \! (i, k) \! \in \! \mathbf{L}$" means "for each bus $k$ to which bus $i$ is connected by an $i$-forward branch" and the subscript "$k \! : \! (k, i) \! \in \! \mathbf{L}$" means "for each bus $k$ to which bus $i$ is connected by an $i$-reverse branch". Substituting $I_{ik}$ and $I_{ki}$ from equations {eq}`eq_I_ik` and {eq}`eq_I_ki` gives us:

$$
\begin{aligned}
    (S_i / V_i)^*
    & = \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\! \left( V_i \, \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) - V_k \, \frac{1}{a_{ik}^*} y_{ik} \right) \\
    & + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\! \left( V_i \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) - V_k \, \frac{1}{a_{ki}} y_{ki} \right)
\end{aligned}
$$

```{note}
Branch $ik$ is the same as a branch $ki$, admittance $y_{ik}$ is the same as $y_{ki}$, and transformer ratio $a_{ik}$ is the same as $a_{ki}$; the order of the subscript simply indicates whether the bus $i$ for which the KCL equation is written is considered the start or end of the branch.
```

Now we split up the summations such that $V_i$ can be factored out where possible:

$$
\begin{aligned}
    (S_i / V_i)^*
    & = V_i \, \Biggl( \, \sum_{k : (i, k) \in \mathbf{L}} \!\! \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\! \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\!\! V_k \, \frac{1}{a_{ik}^*} y_{ik} - \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\!\! V_k \, \frac{1}{a_{ki}} y_{ki}
\end{aligned}
$$ (eq_sums_split_vi_extracted)

The bus injection model is typically expressed in a way that allows some complexity to be moved into a new $N \! \times \! N$ matrix $Y \!$, called the *admittance matrix*, which allows the above equation to be rewritten succinctly as:

$$
(S_i / V_i)^* = \sum_{k \in \mathbf{N}} V_k \, Y_{ik}
$$ (eq_6_6)

Or, even more simply, as a matrix equation:

$$
(S / V)^* = Y \!\: V
$$

Where $Y$ is defined as having the following diagonal and off-diagonal elements:

$$
Y_{ii} = \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\! \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\! \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right)
$$

$$
Y_{ik} =
\begin{cases}
- y_{ik} / a_{ik}^* & \text{if branch $ik$ is an $i$-forward branch} \\
- y_{ki} / a_{ki} & \text{if branch $ik$ is an $i$-reverse branch} \\
\,\,\,\; 0 & \text{if branch $ik$ does not exist (no branch)}
\end{cases}
$$

```{note}
Although $y_{ik}$ is the same as $y_{ki}$, $Y_{ik}$ is not necessarily equal to $Y_{ki}$.
```

Thus, the admittance matrix does not only specify the admittance values between buses in its off-diagonal elements. Its off-diagonal elements additionally specify whether a branch is present between any $ik$-pair of buses ($Y_{ik} \neq 0$), whether a branch is a transformer ($a_{ik} \neq 1$), and its voltage ratio if it is a transformer ($T_{ik} \neq 1$), and even its phase shift if it is also a phase-shifting transformer ($\varphi_{ik} \neq 0$). Furthermore, the diagonal elements specify, for each bus, the shunt admittances of neighboring branches.

Just as how a branch admittance $y$ can be split into real and imaginary parts $g + j b$, where $g$ is conductance and $b$ is susceptance, the admittance matrix $Y \!$ can be split into $G + j B$, which we will leverage shortly.

The bus injection equations are typically arranged as equations for active and reactive power $P + j Q = S$. To describe the power at a given bus $i$, we take the conjugate of Equation {eq}`eq_6_6` and multiply both sides by $V_i$:

$$
P_i + j Q_i = \sum_{k \in \mathbf{N}} V_i \, V_k^* \, Y_{ik}^*
$$

Solver software often expects real-valued equations, so we work towards splitting this equation into a real part and an imaginary part. Furthermore, the bus injection model most commonly uses polar coordinates for voltage and rectangular coordinates for admittance. To satisfy this, we substitute $V = |V| \cos \delta + j \, |V| \sin \delta$ and $Y = G + j B$ in the above equation, giving us the following. We will eventually be able to take the imaginary unit $j$ out of the picture.

$$
P_i + j Q_i = \sum_{k \in \mathbf{N}} (|V_i| \cos \delta_i + j \, |V_i| \sin \delta_i) (|V_k| \cos \delta_k - j \, |V_k| \sin \delta_k) (G_{ik} - j B_{ik})
$$

Expanding the above equation yields:

$$
P_i + j Q_i = \sum_{k \in \mathbf{N}} \left(
\begin{aligned}
    & |V_i| |V_k| \cos \delta_i \cos \delta_k - j \, |V_i| |V_k| \cos \delta_i \sin \delta_k \\
    & + j \, |V_i| |V_k| \sin \delta_i \cos \delta_k + |V_i| |V_k| \sin \delta_i \sin \delta_k
\end{aligned}
\right) (G_{ik} - j B_{ik})
$$

Applying the angle-difference identities $\cos \alpha \cos \beta + \sin \alpha \sin \beta = \cos(\alpha - \beta)$ and $\sin \alpha \cos \beta - \cos \alpha \sin \beta = \sin(\alpha - \beta)$ gives us:

$$
P_i + j Q_i = |V_i| \sum_{k \in \mathbf{N}} |V_k| (\cos (\delta_i - \delta_k) + j \sin(\delta_i - \delta_k)) (G_{ik} - j B_{ik})
$$

Expanding once again yields:

$$
P_i + j Q_i = |V_i| \sum_{k \in \mathbf{N}} |V_k| \left(
\begin{aligned}
& G_{ik} \cos(\delta_i - \delta_k) - j B_{ik} \cos(\delta_i - \delta_k) \\
& + j G_{ik} \sin(\delta_i - \delta_k) + B_{ik} \sin(\delta_i - \delta_k)
\end{aligned}
\right)
$$

Finally, we are able to split this complex-valued equation into the following real-valued **power flow equations**, for each bus $i$. These are suitable for use with solver software.

$$
\boxed{
\begin{aligned}
    P_i & = |V_i| \sum_{k \in \mathbf{N}} |V_k| (G_{ik} \sin(\delta_i - \delta_k) - B_{ik} \cos(\delta_i - \delta_k)) \\
    Q_i & = |V_i| \sum_{k \in \mathbf{N}} |V_k| (G_{ik} \cos(\delta_i - \delta_k) + B_{ik} \sin(\delta_i - \delta_k))
\end{aligned}
}
$$ (eq_pf)

### Applying the Per-Unit System

The per-unit system is the practice in electrical engineering of normalizing quantities like voltage and power to a dimensionless value between 0 and 1. Each quantity $x$ is expressed as a fraction, denoted $x^\text{pu}$, of some base quantity, $x^\text{base}$, such that $x = x^\text{pu} x^\text{base}$. This can be done with many electrical engineering quantities:

$$
\begin{gathered}
V = V^\text{pu} V^\text{base} \qquad
S = S^\text{pu} S^\text{base} \qquad
I = I^\text{pu} I^\text{base} \\
y = y^\text{pu} y^\text{base} \qquad
Z = Z^\text{pu} Z^\text{base} \qquad
\end{gathered}
$$

For example, in the per-unit system with a base of $S^\text{base} = 100 \ \mathrm{MV\!A}$, a quantity of $S = 90 \ \mathrm{MV\!A}$ would become $S^\text{pu} = 0.9 \ \mathrm{per \ unit}$ or $0.9 \ \mathrm{pu}$.

The per-unit system makes it easier to interpret quantities relative to the voltage and power ratings of equipment such as buses and generators. And when applied to the power flow problem, the per-unit system offers additional advantages:

- It improves the problem's conditioning when solving using numerical methods.
- As we will see, it allows most transformer branches to be treated simply as line branches because the transformer voltage ratio becomes $1\!:\!1$ in the per-unit system.

To express the power flow equations in the per-unit system, we select the nominal bus voltage as the base voltage $V_i^\text{base}$ at each bus $i$, and an arbitrary value $S^\text{base}$ as the base power everywhere. We substitute $S_i^\text{pu} S^\text{base}$ for $S_i$ and $V_i^\text{pu} V_i^\text{base}$ for $V_i$ in Equation {eq}`eq_sums_split_vi_extracted` as follows. We also split the transformer voltage ratio $a_{ik}$ into nominal voltage ratio $V_i^\text{base} / V_k^\text{base}$ (which we denote $a_{ik}^\text{base}$) times an off-nominal factor (which we denote $a_{ik}^\text{pu}$). It is not typical to represent transformer voltage ratios in the per-unit system as such&mdash;they are dimensionless quantities to begin with&mdash;but we use the notation $a_{ik} = a_{ik}^\text{pu} a_{ik}^\text{base}$ nonetheless for consistency.

$$
\begin{aligned}
    & \left( \frac{S_i^\text{pu} S^\text{base}}{V_i^\text{pu} V_i^\text{base}} \right)^{\! *} \\
    & = V_i^\text{pu} V_i^\text{base} \, \Biggl( \, \sum_{k : (i, k) \in \mathbf{L}} \!\! \frac{1}{\, |a_{ik}^\text{pu} a_{ik}^\text{base}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\! \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\!\! V_k^\text{pu} V_k^\text{base} \frac{1}{(a_{ik}^\text{pu} a_{ik}^\text{base})^*} \, y_{ik} - \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\!\! V_k^\text{pu} V_k^\text{base} \frac{1}{a_{ki}^\text{pu} a_{ki}^\text{base}} \, y_{ki}
\end{aligned}
$$

Substituting $a_{ik}^\text{base} = V_i^\text{base} / V_k^\text{base}$, multiplying both sides by $V_i^\text{base} / S^\text{base}$ and simplifying:

$$
\begin{aligned}
    & \left( \frac{S_i^\text{pu}}{V_i^\text{pu}} \right)^{\! *} \\
    & = V_i^\text{pu} \Biggl( \, \sum_{k : (i, k) \in \mathbf{L}} \!\! \frac{1}{\, |a_{ik}^\text{pu}|^2} \frac{(V_k^\text{base})^2}{S^\text{base}} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\! \frac{(V_i^\text{base})^2}{S^\text{base}} \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\!\! V_k^\text{pu} \frac{(V_k^\text{base})^2}{S^\text{base}} \frac{1}{(a_{ik}^\text{pu})^*} \, y_{ik} - \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\!\! V_k^\text{pu} \frac{(V_k^\text{base})^2}{S^\text{base}} \frac{1}{a_{ki}^\text{pu}} \, y_{ki}
\end{aligned}
$$

We now apply the per-unit system to the admittances, defining $y_{ik} = y_{ik}^\text{pu} y_{ik}^\text{base}$. If we select $S^\text{base} / (V_k^\text{base})^2$ as the base admittance $y_{ik}^\text{base}$, all base terms conveniently cancel out, leaving something that looks exactly like Equation {eq}`eq_sums_split_vi_extracted`, but with "pu" scripts:

$$
\begin{aligned}
    \left( \frac{S_i^\text{pu}}{V_i^\text{pu}} \right)^{\! *}
    & = V_i^\text{pu} \Biggl( \, \sum_{k : (i, k) \in \mathbf{L}} \!\! \frac{1}{\, |a_{ik}^\text{pu}|^2} \, \Biggl( \frac{y_{ik}^\text{Sh,pu}}{2} + y_{ik}^\text{pu} \Biggr) + \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \! \Biggl( \frac{y_{ki}^\text{Sh,pu}}{2} + y_{ki}^\text{pu} \Biggr) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathbf{L}} \!\!\! V_k^\text{pu} \frac{1}{(a_{ik}^\text{pu})^*} \, y_{ik}^\text{pu} - \!\!\! \sum_{k : (k, i) \in \mathbf{L}} \!\!\! V_k^\text{pu} \frac{1}{a_{ki}^\text{pu}} \, y_{ki}^\text{pu}
\end{aligned}
$$

This per-unit version of Equation {eq}`eq_sums_split_vi_extracted` is how the power flow problem is typically formulated. When the voltage ratio of a transformer $ik$ is *nominal*&mdash;that is, equal to the ratio between the nominal voltage at bus $i$ and the nominal voltage at bus $k$, then $a_{ik}^\text{pu} = 1$ and the equation's terms concerning the transformer branch simplify to those of a line branch. This is because the differing bus voltages $V_i^\text{base} \neq V_k^\text{base}$ are now accounted for as part of $y_{ki}^\text{base} \neq y_{ik}^\text{base}$, respectively.

### Bus Classifications

Our grid model, expressed by the power flow equations, currently has too many unknown variables to be able to solve it. We know the branch admittances, but we do not yet know how the loads should behave or how the bus voltages can be controlled. We now have a model of the grid, but as-is, we cannot use this model to determine how power will flow through the grid. In this section, we will narrow down our definition of the power flow problem.

Each bus and thus each pair of $(P_i, Q_i)$ equations {eq}`eq_pf` has four variables: voltage magnitude $|V_i|$, voltage angle $\delta_i$, active power $P_i$, and reactive power $Q_i$. Each bus contributes two equations, for a total of $2 N$ independent equations making up the system of equations. There are $4 N$ unique variables, so half of them must be fixed in order for the system of equations to have an exactly determined solution. The other half of the variables must be left as free variables that can take on whatever values are required to satisfy the system of equations. Which variables we fix and which variables we allow to vary depends on the type of each bus, as we will discuss. In order to support different numbers of buses of each type, half of the variables *at each bus* must be fixed and the other half free. At most buses, we don't care about the voltage angle, so we leave $\delta_i$ as a free variable.

**Load bus.** A bus to which only load(s) are attached is known as a load bus. At a load bus, $P_i$ and $Q_i$ are fixed based on the demands of the load (or loads). Although we wish we could fix $|V_i|$ to the exact nominal voltage of the bus for the sake of the attached load(s), this is not generally possible without making the system of equations under- or over-determined. Because of this, loads generally accept a voltage range, and system operators are required to keep $|V_i|$ within an even narrower range. Because only variables $P_i$ and $Q_i$ are fixed at a load bus, a load bus is also known as a **PQ bus**.

**Generator bus.** A bus to which only generator(s) are attached is known as a generator bus. At a generator bus, $P_i$ is fixed based on the generator setpoints and $|V_i|$ is fixed to the bus nominal voltage. $Q_i$ is allowed to vary at a generator bus to whatever value satisfies the system. Because only variables $P_i$ and $|V_i|$ are fixed at a generator bus, a generator bus is also known as a **PV bus** or **voltage-controlled bus**.

What if a bus has both generator(s) and load(s) attached? The net active power $P_i$ must be fixed because the active powers of both the generator(s) and loads(s) are fixed. The net reactive power $Q_i$ must be free to vary because, while the reactive powers of the load(s) are fixed, those of the generator(s) are not. And $|V_i|$ is fixed, just as in a generator bus. Indeed, if we were to model a combined generator/load bus as a separate generator bus $i$ and a separate load bus $j$, connected by a line $(i, j)$ with zero impedance, then $|V_i|$ would end up equalling $|V_j|$ anyway. So, a combined generator/load bus is treated as a generator bus.

And what if a bus has neither generators nor loads attached? In this case, the bus is treated as a load bus with fixed $P^L = 0$ and $Q^L = 0$.

**Slack bus.** So far, the classifications of variables as fixed versus free means that the number of free variables equals the number of equations. However, this does not necessarily mean that the system of equations has a solution that is feasible or that it has a solution that is unique. Indeed, with only the two bus types we've defined so far, there is a feasibility issue and a uniqueness issue. Firstly, active power losses due to electrical resistance in the power lines and transformers mean that the total power supplied by the generators does not necessarily equal the total power demanded by the loads plus the power losses. The deficit must be made up for by one or more generators at one or more buses, at which $P$ must thus be free to vary. Otherwise, there would not necessarily be a feasible solution. Secondly, voltage angles are relative, so at one bus, $\delta_i$ must be fixed to $0^\circ$ as a reference against which all other $\delta_i$s are measured. Otherwise, there would be no unique solution. By convention, both the feasibility issue and the uniqueness issue are solved by the same bus. This third type of bus is known as a slack bus, also known as a **swing bus**, **reference bus**, or **Vδ bus**.

{ref}`tab_6_1` summarizes the bus types and their variable classifications.

```{table}
:width: 100%
:label: tab_6_1

| Bus type     | $P_i$             | $Q_i$         | $V_i$                               | $\delta_i$                   |
|--------------|-------------------|---------------|-------------------------------------|------------------------------|
| Load/PQ      | Fixed by load     | Fixed by load | Free                                | Free                         |
| Generator/PV | Fixed by dispatch | Free          | Fixed by grid operating requirement | Free                         |
| Slack/Vδ     | Free              | Free          | Fixed by grid operating requirement | Fixed to $0^\circ$ reference |

Bus types and their variable classifications.
```

As an example of how these bus classifications would apply, consider the electrical grid of {ref}`fig_6_4`. Buses 2 and 3 are both load buses (even though bus 2 has no attached load). Either of buses 1 and 4 can be a generator bus (even though bus 4 has an attached load), but one of them must be a slack bus.

```{figure} img/fig_6_5.png
:width: 64%
:label: fig_6_5

Single-line diagram of another example electrical grid. 
```

<!-- ### Power Flow Constraints -->

<!-- ## The Optimal Power Flow (OPF) Problem -->
