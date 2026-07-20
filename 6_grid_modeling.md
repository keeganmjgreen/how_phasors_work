# Grid Modeling

If the example circuits we've seen so far seem complicated to analyze, then this pales in comparison to the complexity of analyzing and operating the electrical grid. The electrical grid may be just another circuit, but it has rapid, far-reaching, and expensive consequences if it fails. If the grid is operated incorrectly, its voltages and frequencies can be put in jeopardy in a matter of seconds or less, creating a risk of cascading failure. Understanding the grid and how it behaves depending on how it's operated is crucial to be able to control it correctly. Grid modeling allows operators to not only stay in control of grid voltages and frequencies, but also to dispatch generators in a way that is cost-optimal.

The grid is modeled as a network of $N$ electrical buses connected by branches. A bus is a shared point of connection that has minimal electrical impedance. Generators and loads are attached to the buses. Each pair of buses $(i, k)$[^1] may be connected by a branch&mdash;such as a power line or transformer&mdash;which has nonzero impedance and can result in voltage and phase differences between buses $i$ and $k$. In the grid, each bus has a specific nominal voltage, typically 4 kV to 765 kV per phase depending on whether it is in the transmission or distribution part of the grid. The sets of buses and branches are denoted $\mathcal{N}$ and $\mathcal{L}$, respectively.

[^1]: Index $k$ is used instead of $j$ to distinguish it from the imaginary unit.

For example, consider {ref}`fig_6_1`. It shows a simple electrical grid with three buses $\mathcal{N} = \{1, 2, 3\}$, two generators (at buses $1$ and $2$), and a load (at bus $3$). Buses $1$ and $2$ are connected by a line branch, and buses $2$ and $3$ are connected by a transformer branch. This type of diagram is called a *single-line diagram* because it depicts the parallel conductors in a single-phase system or balanced three-phase system&mdash;like the electrical grid&mdash;as single lines for the sake of simplicity.

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

At any given time, a grid operator must dispatch generators to serve the loads in its grid. Each load $l$ consists of a given active power $P_l$ and reactive power $Q_l$. A dispatch specifies the active power $P_{\! g}$ at which to operate each generator $g$. Once a grid operator has decided the generator setpoints, they must be able to validate those setpoints subject to how power will flow through the grid. The grid operator must do this at regular operating intervals (typically 5-minute or 1-hour intervals) because the predicted load and available generation change over time. This consists of:

1. Validating that power generation will satisfy the loads.
2. Validating that not too much current is flowing through a given line or transformer. This is to avoid overloading/overheating it.
3. Validating that voltages are within acceptable margins. This is for the sake of the loads.

The task of determining how power will flow through the grid and whether it will satisfy the loads is known as the power flow (PF) problem.

Because the grid is a circuit, we can solve the power flow problem the same as we solve any other circuit, by doing nodal analysis and solving a system of KCL equations to determine the voltage at each bus, denoted $V_{\! i} = |V_{\! i}| \angle \delta_i$. In the three-phase case, the voltage magnitude $|V_{\! i}|$ can be assumed to be the same across the three phases at each bus, and the voltage angle $\delta_i$ can be taken for the first phase only, knowing that the other two phases will be $\pm 2 \pi / 3$ radians apart.

For generality, we will model all branches as transformer branches. For line branches, we can simply set $T_{ik} = 1$ and $\varphi_{ik} = 0$. We will call branch $ik$ an *$i$-forward branch* if bus $i$ is the tap bus, or an *$i$-reverse branch* if bus $i$ is the impedance bus. In this sense, the grid model becomes a directed graph rather than an undirected graph, and we must account for the forward and reverse branch directions distinctly. We do this by deriving the current $I_{ik}$ flowing into branch $ik$ from bus $i$ (that is, flowing directly into the ideal transformer), as well as the current $I_{ki}$ flowing into the branch from the opposite bus $k$. To determine $I_{ik}$, we apply KCL by summing the currents out of node $i'$ in {ref}`fig_6_4`:

$$
\begin{aligned}
& - \!\! I_{ik}' + V_{\! i}' \, \frac{y_{ik}^\text{Sh}}{2} + (V_{\! i}' - V_k) \, y_{ik} = 0 \\
& \implies I_{ik}' = V_{\! i}' \left( \frac{y_{ik}}{2} + y_{ik} \right) - V_k \, y_{ik} \\
& \implies I_{ik} a_{ik}^* = V_{\! i} \, \frac{1}{a_{ik}} \left( \frac{y_{ik}}{2} + y_{ik} \right) - V_k \, y_{ik} \\
& \implies I_{ik} = V_{ik} \, \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}}{2} + y_{ik} \right) - V_k \, \frac{1}{a_{ik}^*} y_{ik}
\end{aligned}
$$ (eq_I_ik)

And to determine $I_{ki}$, we apply KCL by summing the currents out of node $k'$:

$$
\begin{aligned}
& - \!\! I_{ki} + (V_k - V_{\! i}') \, y_{ik} + V_k \frac{y_{ik}^\text{Sh}}{2} = 0 \\
& \implies I_{ki} = V_k \left( y_{ik} + \frac{y_{ik}^\text{Sh}}{2} \right) - V_{\! i}' \, y_{ik} \\
& \implies I_{ki} = V_k \left( y_{ik} + \frac{y_{ik}^\text{Sh}}{2} \right) - V_{\! i} \, \frac{1}{a_{ik}} y_{ik}
\end{aligned}
$$ (eq_I_ki)

### The Bus Injection Model

To define the power flow problem, we need to formulate a set of power flow equations. The most common formulation is known as the *bus injection model*. We start with KCL, which tells us that at a bus $i$ with nominal voltage $V_{\! i}$, the current $(S_i / V_{\! i})^*$ injected due to attached generation and/or load $S_i$ must equal the sum of currents flowing out of the bus:

$$
\begin{aligned}
(S_i / V_{\! i})^*
& = \text{total current out of bus $i$ via $i$-forward branches} \\
& \, + \text{total current out of bus $i$ via $i$-reverse branches} \\
& = \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\!\! I_{ik} + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\!\! I_{ik}
\end{aligned}
$$

The subscript "$k \! : \! (i, k) \! \in \! \mathcal{L}$" means "for each bus $k$ to which bus $i$ is connected by an $i$-forward branch" and the subscript "$k \! : \! (k, i) \! \in \! \mathcal{L}$" means "for each bus $k$ to which bus $i$ is connected by an $i$-reverse branch". Substituting $I_{ik}$ and $I_{ki}$ from equations {eq}`eq_I_ik` and {eq}`eq_I_ki` gives us:

$$
\begin{aligned}
    (S_i / V_{\! i})^*
    & = \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\! \left( V_{\! i} \, \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) - V_k \, \frac{1}{a_{ik}^*} y_{ik} \right) \\
    & + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\! \left( V_{\! i} \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) - V_k \, \frac{1}{a_{ki}} y_{ki} \right)
\end{aligned}
$$

```{note}
Branch $ik$ is the same as a branch $ki$, admittance $y_{ik}$ is the same as $y_{ki}$, and transformer ratio $a_{ik}$ is the same as $a_{ki}$; the order of the subscript simply indicates whether the bus $i$ for which the KCL equation is written is considered the start or end of the branch.
```

Now we split up the summations such that $V_{\! i}$ can be factored out where possible:

$$
\begin{aligned}
    (S_i / V_{\! i})^*
    & = V_{\! i} \, \Biggl( \, \sum_{k : (i, k) \in \mathcal{L}} \!\! \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\! \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\!\! V_k \, \frac{1}{a_{ik}^*} y_{ik} - \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\!\! V_k \, \frac{1}{a_{ki}} y_{ki}
\end{aligned}
$$ (eq_sums_split_vi_extracted)

The bus injection model is typically expressed in a way that allows some complexity to be moved into a new $N \! \times \! N$ matrix $Y \!$, called the *admittance matrix*, which allows the above equation to be rewritten succinctly as:

$$
(S_i / V_{\! i})^* = \sum_{k \in \mathcal{N}} V_k \, Y_{ik}
$$ (eq_6_6)

Or, even more simply, as a matrix equation:

$$
S = (Y \!\: V)^* \circ V
$$

where "$\displaystyle\circ$" indicates element-wise vector multiplication and $Y$ is defined as having the following diagonal and off-diagonal elements:

$$
Y_{ii} = \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\! \frac{1}{\, |a_{ik}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\! \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right)
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

Just as how a branch admittance $y$ can be split into real and imaginary parts $g + j b$, where $g$ is conductance[^2] and $b$ is susceptance, the admittance matrix $Y \!$ can be split into $G + j B$, which we will leverage shortly.

[^2]: Not to be confused with generator index $g$.

The bus injection equations are typically arranged as equations for active and reactive power $P + j Q = S$. To describe the power at a given bus $i$, we take the conjugate of Equation {eq}`eq_6_6` and multiply both sides by $V_{\! i}$:

$$
P_i + j Q_i = \sum_{k \in \mathcal{N}} V_{\! i} \, V_k^* \, Y_{ik}^*
$$

Solver software often expects real-valued equations, so we work towards splitting this equation into a real part and an imaginary part. Furthermore, the bus injection model most commonly uses polar coordinates for voltage and rectangular coordinates for admittance. To satisfy this, we substitute $V = |V| \cos \delta + j \, |V| \sin \delta$ and $Y = G + j B$ in the above equation, giving us the following. We will eventually be able to take the imaginary unit $j$ out of the picture.

$$
P_i + j Q_i = \sum_{k \in \mathcal{N}} (|V_{\! i}| \cos \delta_i + j \, |V_{\! i}| \sin \delta_i) (|V_k| \cos \delta_k - j \, |V_k| \sin \delta_k) (G_{ik} - j B_{ik})
$$

Expanding the above equation yields:

$$
P_i + j Q_i = \sum_{k \in \mathcal{N}} \left(
\begin{aligned}
    & |V_{\! i}| |V_k| \cos \delta_i \cos \delta_k - j \, |V_{\! i}| |V_k| \cos \delta_i \sin \delta_k \\
    & + j \, |V_{\! i}| |V_k| \sin \delta_i \cos \delta_k + |V_{\! i}| |V_k| \sin \delta_i \sin \delta_k
\end{aligned}
\right) (G_{ik} - j B_{ik})
$$

Applying the angle-difference identities $\cos \alpha \cos \beta + \sin \alpha \sin \beta = \cos(\alpha - \beta)$ and $\sin \alpha \cos \beta - \cos \alpha \sin \beta = \sin(\alpha - \beta)$ gives us:

$$
P_i + j Q_i = |V_{\! i}| \sum_{k \in \mathcal{N}} |V_k| (\cos (\delta_i - \delta_k) + j \sin(\delta_i - \delta_k)) (G_{ik} - j B_{ik})
$$

Expanding once again yields:

$$
P_i + j Q_i = |V_{\! i}| \sum_{k \in \mathcal{N}} |V_k| \left(
\begin{aligned}
& G_{ik} \cos(\delta_i - \delta_k) - j B_{ik} \cos(\delta_i - \delta_k) \\
& + j G_{ik} \sin(\delta_i - \delta_k) + B_{ik} \sin(\delta_i - \delta_k)
\end{aligned}
\right)
$$

Finally, we are able to split this complex-valued equation into the following real-valued *power flow equations*, for each bus $i$. These are suitable for use with solver software.

$$
\boxed{
\begin{aligned}
    P_i & = |V_{\! i}| \sum_{k \in \mathcal{N}} |V_k| (G_{ik} \sin(\delta_i - \delta_k) - B_{ik} \cos(\delta_i - \delta_k)) \\
    Q_i & = |V_{\! i}| \sum_{k \in \mathcal{N}} |V_k| (G_{ik} \cos(\delta_i - \delta_k) + B_{ik} \sin(\delta_i - \delta_k))
\end{aligned}
}
$$ (eq_pf)

&nbsp;

&nbsp;

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

- It improves the problem's stability when solving using numerical methods.
- As we will see, it allows most transformer branches to be treated simply as line branches because the transformer voltage ratio becomes $1\!:\!1$ in the per-unit system.

To express the power flow equations in the per-unit system, we select the nominal bus voltage as the base voltage $V_{\! i}^\text{base}$ at each bus $i$, and an arbitrary value $S^\text{base}$ as the base power everywhere. We substitute $S_i^\text{pu} S^\text{base}$ for $S_i$ and $V_{\! i}^\text{pu} V_{\! i}^\text{base}$ for $V_{\! i}$ in Equation {eq}`eq_sums_split_vi_extracted` as follows. We also split the transformer voltage ratio $a_{ik}$ into nominal voltage ratio $V_{\! i}^\text{base} / V_k^\text{base}$ (which we denote $a_{ik}^\text{base}$) times an off-nominal factor (which we denote $a_{ik}^\text{pu}$). It is not typical to represent transformer voltage ratios in the per-unit system as such&mdash;they are dimensionless quantities to begin with&mdash;but we use the notation $a_{ik} = a_{ik}^\text{pu} a_{ik}^\text{base}$ nonetheless for consistency.

$$
\begin{aligned}
    & \left( \frac{S_i^\text{pu} S^\text{base}}{V_{\! i}^\text{pu} V_{\! i}^\text{base}} \right)^{\! *} \\
    & = V_{\! i}^\text{pu} V_{\! i}^\text{base} \, \Biggl( \, \sum_{k : (i, k) \in \mathcal{L}} \!\! \frac{1}{\, |a_{ik}^\text{pu} a_{ik}^\text{base}|^2} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\! \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\!\! V_k^\text{pu} V_k^\text{base} \frac{1}{(a_{ik}^\text{pu} a_{ik}^\text{base})^*} \, y_{ik} - \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\!\! V_k^\text{pu} V_k^\text{base} \frac{1}{a_{ki}^\text{pu} a_{ki}^\text{base}} \, y_{ki}
\end{aligned}
$$

Substituting $a_{ik}^\text{base} = V_{\! i}^\text{base} / V_k^\text{base}$, multiplying both sides by $V_{\! i}^\text{base} / S^\text{base}$ and simplifying:

$$
\begin{aligned}
    & \left( \frac{S_i^\text{pu}}{V_{\! i}^\text{pu}} \right)^{\! *} \\
    & = V_{\! i}^\text{pu} \Biggl( \, \sum_{k : (i, k) \in \mathcal{L}} \!\! \frac{1}{\, |a_{ik}^\text{pu}|^2} \frac{(V_k^\text{base})^2}{S^\text{base}} \left( \frac{y_{ik}^\text{Sh}}{2} + y_{ik} \right) + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\! \frac{(V_{\! i}^\text{base})^2}{S^\text{base}} \left( \frac{y_{ki}^\text{Sh}}{2} + y_{ki} \right) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\!\! V_k^\text{pu} \frac{(V_k^\text{base})^2}{S^\text{base}} \frac{1}{(a_{ik}^\text{pu})^*} \, y_{ik} - \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\!\! V_k^\text{pu} \frac{(V_k^\text{base})^2}{S^\text{base}} \frac{1}{a_{ki}^\text{pu}} \, y_{ki}
\end{aligned}
$$

We now apply the per-unit system to the admittances, defining $y_{ik} = y_{ik}^\text{pu} y_{ik}^\text{base}$. If we select $S^\text{base} / (V_k^\text{base})^2$ as the base admittance $y_{ik}^\text{base}$, all base terms conveniently cancel out, leaving something that looks exactly like Equation {eq}`eq_sums_split_vi_extracted`, but with "pu" scripts:

$$
\begin{aligned}
    \left( \frac{S_i^\text{pu}}{V_{\! i}^\text{pu}} \right)^{\! *}
    & = V_{\! i}^\text{pu} \Biggl( \, \sum_{k : (i, k) \in \mathcal{L}} \!\! \frac{1}{\, |a_{ik}^\text{pu}|^2} \, \Biggl( \frac{y_{ik}^\text{Sh,pu}}{2} + y_{ik}^\text{pu} \Biggr) + \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \! \Biggl( \frac{y_{ki}^\text{Sh,pu}}{2} + y_{ki}^\text{pu} \Biggr) \Biggr) \\
    & - \!\!\! \sum_{k : (i, k) \in \mathcal{L}} \!\!\! V_k^\text{pu} \frac{1}{(a_{ik}^\text{pu})^*} \, y_{ik}^\text{pu} - \!\!\! \sum_{k : (k, i) \in \mathcal{L}} \!\!\! V_k^\text{pu} \frac{1}{a_{ki}^\text{pu}} \, y_{ki}^\text{pu}
\end{aligned}
$$

When the voltage ratio of a transformer $ik$ is *nominal*&mdash;that is, equal to the ratio between the nominal voltage at bus $i$ and the nominal voltage at bus $k$, then $a_{ik}^\text{pu} = 1$ and the equation's terms concerning the transformer branch simplify to those of a line branch. This is because the differing bus voltages $V_{\! i}^\text{base} \neq V_k^\text{base}$ are now accounted for as part of $y_{ki}^\text{base} \neq y_{ik}^\text{base}$, respectively. The power flow problem is typically expressed in the per-unit system because of this advantage, as well as the advantage of improved numerical stability.

### Bus Classifications

Our grid model, expressed by the power flow equations, currently has too many unknown variables to be able to solve it. We know the branch admittances, but we do not yet know how the loads should behave or how the bus voltages can be controlled. We now have a model of the grid, but as-is, we cannot use this model to determine how power will flow through the grid. In this section, we will narrow down our definition of the power flow problem.

Each bus and thus each pair of $(P_i, Q_i)$ equations {eq}`eq_pf` has four variables: voltage magnitude $|V_{\! i}|$, voltage angle $\delta_i$, active power $P_i$, and reactive power $Q_i$. Each bus contributes two equations, for a total of $2 N$ independent equations making up the system of equations. There are $4 N$ unique variables, so half of them must be fixed in order for the system of equations to have an exactly determined solution. The other half of the variables must be left as free variables that can take on whatever values are required to satisfy the system of equations. Which variables we fix and which variables we allow to vary depends on the type of each bus, as we will discuss. In order to support different numbers of buses of each type, half of the variables *at each bus* must be fixed and the other half free. At most buses, we don't care about the voltage angle, so we leave $\delta_i$ as a free variable.

*Load bus.* A bus to which only load(s) are attached is known as a load bus. At a load bus, $P_i$ and $Q_i$ are fixed based on the demands of the load (or loads). Although we wish we could fix $|V_{\! i}|$ to the exact nominal voltage of the bus for the sake of the attached load(s), this is not generally possible without making the system of equations under- or over-determined. Because of this, loads generally accept a voltage range, and system operators are required to keep $|V_{\! i}|$ within an even narrower range. Because only variables $P_i$ and $Q_i$ are fixed at a load bus, a load bus is also known as a *PQ bus*.

*Generator bus.* A bus to which only generator(s) are attached is known as a generator bus. At a generator bus, $P_i$ is fixed based on the generator setpoints and $|V_{\! i}|$ is fixed to the bus nominal voltage. $Q_i$ is allowed to vary at a generator bus to whatever value satisfies the system. Because only variables $P_i$ and $|V_{\! i}|$ are fixed at a generator bus, a generator bus is also known as a *PV bus* or *voltage-controlled bus*.

What if a bus has both generator(s) and load(s) attached? The net active power $P_i$ must be fixed because the active powers of both the generator(s) and loads(s) are fixed. The net reactive power $Q_i$ must be free to vary because, while the reactive powers of the load(s) are fixed, those of the generator(s) are not. And $|V_{\! i}|$ is fixed, just as in a generator bus. Indeed, if we were to model a combined generator/load bus as a separate generator bus $i$ and a separate load bus $k$, connected by a line $ik$ with zero impedance, then $|V_{\! i}|$ would end up equalling $|V_k|$ anyway. So, a combined generator/load bus is treated as a generator bus.

And what if a bus has neither generators nor loads attached? In this case, the bus is treated as a load bus with fixed $P_i = 0$ and $Q_i = 0$.

*Slack bus.* So far, the classifications of variables as fixed versus free means that the number of free variables equals the number of equations. However, this does not necessarily mean that the system of equations has a solution that is feasible or that it has a solution that is unique. Indeed, with only the two bus types we've defined so far, there is a feasibility issue and a uniqueness issue. Firstly, active power losses due to electrical resistance in the power lines and transformers mean that the total power supplied by the generators does not necessarily equal the total power demanded by the loads plus the power losses. The deficit must be made up for by one or more generators at one or more buses, at which $P$ must thus be free to vary. Otherwise, there would not necessarily be a feasible solution. Secondly, voltage angles are relative, so at one bus, $\delta_i$ must be fixed to $0^\circ$ as a reference against which all other $\delta_i$s are measured. Otherwise, there would be no unique solution. By convention, both the feasibility issue and the uniqueness issue are solved by the same bus. This third type of bus is known as a slack bus, also known as a *swing bus*, *reference bus*, or *Vδ bus*.

{ref}`tab_6_1` summarizes the bus types and their variable classifications.

```{table}
:width: 100%
:label: tab_6_1

| Bus type     | $P_i$             | $Q_i$         | $V_{\! i}$                               | $\delta_i$                   |
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

<!-- ### Linearized Power Flow -->

<!-- ### Solving the Power Flow Problem -->

### Power Flow Validation

After solving the power flow problem, a grid operator is able to validate their generator dispatch according to the three requirements listed under [](#the-power-flow-pf-problem):

1. Validating that power generation will satisfy the loads. More specifically, validating that the slack generation&mdash;which is free to vary to whatever value is required to satisfy the loads&mdash;is within the maximum power of slack generator $g$:

    $$
    S_g \leq S_g^\text{max}
    $$ (pf_criterion_1)

2. Validating that not too much current is flowing through a given line or transformer:

    $$
    |I_{ik}| \leq I_{ik}^\text{max}
    $$ (pf_criterion_2)

3. Validating that voltages are within acceptable margins:

    $$
    V_{\! i}^\text{min} \leq |V_{\! i}| \leq V_{\! i}^\text{max}
    $$ (pf_criterion_3)

## The Economic Dispatch (ED) Problem

The power flow problem is intended to determine *whether* generator setpoints are valid, but it alone does not help determine *what* generator setpoints to use in the first place. When a grid operator decides how to dispatch generators, their goal&mdash;within the requirement of satisfying the grid's loads&mdash;is to minimize their operating cost incurred during a given operating interval. Different types of generators have different costs per MWh of electrical energy; for example, operating a hydroelectric generator is less expensive than fuel for a natural-gas-powered generator. Furthermore, a given generator $g$ can also have a cost per MWh that increases with the setpoint $P_{\! g}$, in MW, at which the generator is operated. Thus, each generator has its own cost function $C_g (P_{\! g})$, and the total operating cost for a given interval of time depends on both on *which* generators are dispatched, and *what setpoint* each of those generators is operated at.

The grid operator can achieve their goal of minimizing their operating cost by solving an optimization problem in which the objective function&mdash;to be minimized&mdash;is the total operating cost, and the decision variables are the generator setpoints. This optimization problem is what is known as the economic dispatch (ED) problem:

$$
\boxed{\min \sum_{g \in \mathcal{G}} C_g \bigl( P_{\! g} \bigr)}
$$

How the cost function $C_g$ is formulated depends on the application. If the application is research or planning purposes, then a quadratic fit is typically used to approximately model how the cost per MWh increases as $P_{\! g}$ increases. For day-to-day and real-time dispatch by the grid operator, a piecewise linear function is often used for greater accuracy.

So far, we have assumed that all generators are dispatchable (controllable power) and that all loads are non-dispatchable (uncontrollable power). There do exist non-dispatchable generators whose power production *cannot* be controlled, as well as dispatchable loads (such as smart thermostats and smart EV charging in some cases) whose power consumption *can* be controlled by the grid operator. However, this does not mean that the grid model discussed so far cannot represent these resources. Non-dis&shy;patchable generators can be modeled as loads whose fixed power is positive rather than negative. As for dispatchable loads, they can be modeled as generators whose maximum power is negative rather than positive, and with cost functions that intake and output negative values. This negative cost&mdash;associated with consuming, rather than producing&mdash;is called *utility* in economics. Utility quantifies the economic value delivered to consumers (loads) when they are dispatched by the grid operator, in contrast to the cost incurred by producers (generators) by being dispatched.[^3]

[^3]: To learn more about the economics of operating the electrical grid, see [How Electricity Markets Work](https://keeganmjgreen.github.io/ontario_electricity_market/).

## The Optimal Power Flow (OPF) Problem

Not just any solution to the economic dispatch problem will do. Operating costs cannot be minimized without ensuring that the setpoints are valid per the power flow equations {eq}`eq_pf` and the criteria in [the previous section](#power-flow-validation) (equations {eq}`pf_criterion_1`, {eq}`pf_criterion_2`, {eq}`pf_criterion_3`). These become equality and inequality constraints in the optimization problem, respectively. The result of pairing the objective function for economic dispatch with the power flow constraints is known as the optimal power flow (OPF) problem:

$$
\boxed{ \quad
\begin{aligned}
    & \\
    & \! \min_{\mathbf{P}} \sum_{g \in \mathcal{G}} C_g \bigl( P_{\! g} \bigr) \\
    & \text{subject to:} \\
    & P_i = |V_{\! i}| \sum_{k \in \mathcal{N}} |V_k| (G_{ik} \sin(\delta_i - \delta_k) - B_{ik} \cos(\delta_i - \delta_k)) && \!\! \forall \, i \in \mathcal{N} \\
    & Q_i = |V_{\! i}| \sum_{k \in \mathcal{N}} |V_k| (G_{ik} \cos(\delta_i - \delta_k) + B_{ik} \sin(\delta_i - \delta_k)) && \!\! \forall \, i \in \mathcal{N} \\
    & S_g^\text{min} \leq S_g \leq S_g^\text{max} && \!\! \forall \, g \in \mathcal{G} \\
    & |I_{ik}| \leq I_{ik}^\text{max} && \!\! \forall \, (i, k) \in \mathcal{L} \\
    & V_{\! i}^\text{min} \leq |V_{\! i}| \leq V_{\! i}^\text{max} && \!\! \forall \, i \in \mathcal{N} \\
    & \phantom{}
\end{aligned}
\quad }
$$ (eq_opf)

This OPF problem {eq}`eq_opf` must be solved for every operating interval, making a dispatch decision and minimizing the total cost incurred over that interval independent of any other interval. However, as we will see, there are OPF variants that require considering multiple intervals in one optimization problem, making a dispatch decision for every interval simultaneously and minimizing the total cost incurred over all intervals. For these purposes, we add an interval index $t$ to all time-variant quantities and denote the interval duration as $\Delta t$.

*Ramp rate limits.* The first multi-interval OPF variant that we will discuss involves limits on generators' ramp rates. How quickly a generator's power output (in MW) changes from one interval to the next is referred to as its *ramp rate* (e.g., in MW per minute). If the power output is analogous to velocity, then ramp rate's analog is acceleration, and there are limits to both. Some generators may not be able to change their power output very quickly. To keep the dispatch decision within such physical limitations, the following constraint is added to respect each generator's ramp rate limit when ramping up, $\dot{P}_g^\text{U}$, and when ramping down, $\dot{P}_g^\text{D}$:

$$
\dot{P}_g^\text{D} \leq \frac{P_{gt} - P_{g,\,t-1}}{\Delta t} \leq \dot{P}_g^\text{U}
$$

Ramp rate limits $\dot{P}_g^\text{U}$ and $\dot{P}_g^\text{D}$ are positive and negative values, respectively. For a given $t$, only one side of this two-sides inequality constraint can be active.

### The Unit Commitment Problem

The basic OPF problem {eq}`eq_opf` accounts for the power cost that is incurred by operating a generator at a certain setpoint (e.g., incurred due to fuel use). However, there are additional *standby* costs which depend on whether a generator is in a running state versus an off state over a given operating interval, and there are additional *startup* and *shutdown* costs which depend on whether the generator is transitioning from an off state to a running state (or vice versa) from one interval to the next. In order to account for these additional costs in our objective function, we must introduce additional binary decision variables, $w_{gt}$, specifying whether generator $g$ is running ($w_{gt} = 1$) or not ($w_{gt} = 0$) over interval $t$. This requires modifying constraint {eq}`pf_criterion_1` as:

$$
w_{gt} S_g^\text{min} \leq S_{gt} \leq w_{gt} S_g^\text{max}
$$

The variant of the OPF problem that includes standby, startup, and shutdown costs is thus a scheduling problem, and is known as the unit commitment (UC) problem. *Unit commitment* refers to whether a generating unit (that is, a generator) has committed to be running&mdash;and thus able to supply power&mdash;at a given time.

*Standby cost.* In addition to a power cost, a generator might have a cost that is incurred as long as it is running, regardless of the generator's setpoint. This is known as standby cost, $C_g^\text{SB}$, and it disincentivizes a generator from being run (and thus from generating *any* power) if there is a favorable alternative in terms of cost. For example, the grid operator may be willing to pay a disproportionately higher price to operate an already-running generator at a higher setpoint, rather than running a second generator to supply the extra power, if that second generator's standby cost is high. Accounting for standby cost, the objective function becomes:

$$
\min_{\mathbf{P}, \, \mathbf{w}} \sum_{t \in \mathcal{T}} \sum_{g \in \mathcal{G}} w_{gt} \left( C_g \bigl( P_{\! g} \bigr) + C_g^\text{SB} \right)
$$

*Startup and shutdown costs.* In addition to a power cost and a standby cost, a generator might have costs associated with starting up and shutting down, denoted $C_g^\text{SU}$ and $C_g^\text{SD}$, respectively. Startup and shutdown costs only matter if there are standby costs; if there were no standby costs, there would be no reason to shut down generators and thus no reason to incur startup or shutdown costs. Accounting for startup and shutdown costs in addition to standby cost, the objective function becomes:

$$
\sum_{t \in \mathcal{T}} \sum_{g \in \mathcal{G}} \left[ w_{gt} \left( C_g \bigl( P_{\! g} \bigr) + C_g^\text{SB} \right) + w_{gt} (w_{g,\,t-1} - 1) C_g^\text{SU} + (w_{gt} - 1) w_{g,\,t-1} C_g^\text{SD} \right]
$$

where $w_{gt} (w_{g,\,t-1} - 1)$ and $(w_{gt} - 1) w_{g,\,t-1}$ indicate whether a generator has started up or shut down from one interval to the next, respectively.

*Startup and shutdown ramp rate limits.* Some generators have ramp rate limits that apply specifically when starting up or shutting down, which can be accounted for using the following constraints:

$$
\begin{gathered}
\dot{P}_g^\text{SD} \leq w_{gt} (w_{g,\,t-1} - 1) \frac{P_{gt} - P_{g,\,t-1}}{\Delta t} \\
(w_{gt} - 1) w_{g,\,t-1} \frac{P_{gt} - P_{g,\,t-1}}{\Delta t} \leq \dot{P}_g^\text{SU}
\end{gathered}
$$

<!-- Seems these don't override regular ramp rate limits: https://docs.pypsa.org/v1.1.0/examples/unit-commitment/?h=ramp_limit_start_up#ramp-rate-limits

    ramp_limit_start_up=0.1,
    ramp_limit_up=0.2,
    ramp_limit_down=0.25,
    ramp_limit_shut_down=0.15, -->

*Minimum uptime and downtime.* It may be required that a generator be in a standby/running state, or in an off state, for a minimum number of operating intervals. This can be accounted for using the following constraints:

$$
\begin{gathered}
\text{minimum uptime} \leq \sum_{t \in \mathcal{T}} w_{gt} \\
\text{minimum downtime} \leq \sum_{t \in \mathcal{T}} (1 - w_{gt})
\end{gathered}
$$

<!-- ### The Security-Constrained Optimal Power Flow (SCOPF) Problem -->

<!-- ### Linearized Optimal Power Flow -->

<!-- https://www.pcienergysolutions.com/2024/05/01/understanding-the-differences-between-non-dispatchable-and-dispatchable-generation/ -->
