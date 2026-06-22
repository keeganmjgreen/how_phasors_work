# Grid Modeling

If the example circuits we've seen so far seem complex to analyze, then this pales in comparison to the complexity of analyzing and operating the electrical grid. The electrical grid may be just another circuit, but it has rapid, far-reaching, and expensive consequences if it fails. If the grid is operated incorrectly, its voltages and frequencies can be put in jeopardy in a matter of seconds or less, creating a risk of cascading failure. Understanding the grid and how it behaves depending on how it's operated is crucial to be able to control it correctly. Grid modeling allows operators to not only stay in control of grid voltages and frequencies, but also to dispatch generators in a way that is cost-optimal.

The grid is modeled as a network of $n$ electrical buses connected by branches. A bus is a shared point of connection that has minimal electrical impedance. Generators and loads are attached to the buses. Each pair of buses $(i, j)$ may be connected by a branch, such as a power line or transformer, which has nonzero impedance and can result in voltage and phase differences between the buses. In the grid, each bus has a specific nominal voltage, typically 4 kV to 765 kV per phase depending on whether it is in the transmission or distribution part of the grid.

For example, consider Figure 6.1. It shows a simple electrical grid with three buses, two generators (at buses 1 and 2), and a load (at bus 3). Buses 1 and 2 are connected by a line branch, and buses 2 and 3 are connected by a transformer branch. This type of diagram is called a *single-line diagram* because it depicts the parallel conductors in a single-phase system or balanced three-phase system&mdash;like the electrical grid&mdash;as single lines for the sake of simplicity.

```{figure} img/fig_6_1.png
:width: 64%
:label: fig_6_1

Single-line diagram of an example electrical grid. Note that the symbol for "Load" should not be confused with the symbol for electrical ground.
```

Figure 6.2 shows the circuit diagram that corresponds to this single-line diagram for a three-phase system. Each bus $i$ in the single-line diagram corresponds to a set of three nodes in the circuit (one per phase).

```{figure} img/fig_6_2.png
:label: fig_6_2

Circuit diagram of the example electrical grid in Figure 6.1.
```

Each branch has a known series impedance $Z_{i, j}$ and shunt impedance $Z_{i, j}^\mathrm{Sh}$ according to the $\Pi$ (Pi) branch model, so named because the single-phase version of the $\Pi$ branch model looks like the Greek letter $\Pi$, as shown in Figure 6.3.

<!-- Branch impedances and voltage ratios -->
<!-- Half of admittance, not impedance -->

```{figure} img/fig_6_3.png
:width: 64%
:label: fig_6_3

The $\Pi$ branch model.
```

Our circuit grid model (such as in Figure 6.1) currently has too many unknown variables to be able to solve it. We know the branch impedances, but we do not yet know how the loads should behave or how the bus voltages can be controlled. We now have a way to model the grid, but as-is, we cannot use this model to determine how power will flow through the grid. In the next section, we will narrow down the task from a generic exercise in AC circuit analysis to what is known as the power flow problem.

## The power flow problem

A grid operator must dispatch generators to serve the loads in its grid. Each load consists of a given active power $P^L$ and reactive power $Q^L$. A dispatch specifies the active power $P^G$ at which to operate each generator. Once a grid operator has decided the generator setpoints, they must be able to validate those setpoints. This consists of:

- Validating that power is able to flow through the grid according to the setpoints in a way that satisfies the loads.
- Validating that not too much power is flowing through a given line or transformer, to avoid overloading/overheating it.
- Validating that voltages are within acceptable margins for the sake of the loads.

The task of determining how power will flow through the grid and whether it will satisfy the loads is known as the power flow (PF) problem. Because the grid is a circuit, we can solve the power flow problem the same as we solve any other circuit, by doing nodal analysis and solving a system of KCL equations to determine the voltage at each bus, denoted $V_i = |V_i| \angle \delta_i$. In the three-phase case, the voltage magnitude $|V_i|$ can be assumed to be the same across the three phases at each bus, and the voltage angle $\delta_i$ can be taken for the first phase only, knowing that the other two phases will be $\pm 2 \pi / 3$ radians apart. The KCL equation for a bus $i$ is:

$$
\left( \frac{P_i + j Q_i}{|V_i| \angle \delta_i} \right)^{\!*} = \sum_{j \, \in \, \mathbf{K}_i} \frac{|V_i| \angle \delta_i - |V_j | \angle \delta_j}{Z_{i, j}}
$$

The LHS represents the current flow due to attached generators and/or loads. The RHS represents the sum of currents flowing out of bus $i$ to a connected bus $j \in \mathbf{K}_i$, where $\mathbf{K}_i$ is the set of buses connected to bus $i$.

Each bus and thus each KCL equation has four variables: voltage magnitude $|V_i|$, voltage angle $\delta_i$, active power $P_i$, and reactive power $Q_i$. Each of the $n$ KCL equations is a complex equation that can be split into one real equation and one imaginary equation, for a total of $2 n$ independent equations making up the system of equations. There are $4 n$ unique variables, so half of them must be fixed in order for the system of equations to have an exactly determined solution. The other half of the variables must be left as free variables that can take on whatever values are required to satisfy the system of equations. Which variables we fix and which variables we allow to vary depends on the type of each bus, as we will discuss. In order to support different numbers of buses of each type, half of the variables *at each bus* must be fixed and the other half free. At most buses, we don't care about the voltage angle, so we leave $\delta_i$ as a free variable.

**Load bus.** A bus to which only load(s) are attached is known as a load bus. At a load bus, $P_i$ and $Q_i$ are fixed based on the demands of the load (or loads). Although we wish we could fix $|V_i|$ to the exact nominal voltage of the bus for the sake of the attached load(s), this is not generally possible without making the system of equations under- or over-determined. Because of this, loads generally accept a voltage range, and system operators are required to keep $|V_i|$ within an even narrower range. Because only variables $P_i$ and $Q_i$ are fixed at a load bus, a load bus is also known as a **PQ bus**.

**Generator bus.** A bus to which only generator(s) are attached is known as a generator bus. At a generator bus, $P_i$ is fixed based on the generator setpoints and $|V_i|$ is fixed to the bus nominal voltage. $Q_i$ is allowed to vary at a generator bus to whatever value satisfies the system. Because only variables $P_i$ and $|V_i|$ are fixed at a generator bus, a generator bus is also known as a **PV bus** or **voltage-controlled bus**.

What if a bus has both generator(s) and load(s) attached? The net active power $P_i$ must be fixed because the active powers of both the generator(s) and loads(s) are fixed. The net reactive power $Q_i$ must be free to vary because, while the reactive powers of the load(s) are fixed, those of the generator(s) are not. And $|V_i|$ is fixed, just as in a generator bus. Indeed, if we were to model a combined generator/load bus as a separate generator bus $i$ and a separate load bus $j$, connected by a line $(i, j)$ with zero impedance, then $|V_i|$ would end up equalling $|V_j|$ anyway. So, a combined generator/load bus is treated as a generator bus.

And what if a bus has neither generators nor loads attached? In this case, the bus is treated as a load bus with fixed $P^L = 0$ and $Q^L = 0$.

**Slack bus.** So far, the classifications of variables as fixed versus free means that the number of free variables equals the number of equations. However, this does not necessarily mean that the system of equations has a solution that is feasible or that it has a solution that is unique. Indeed, with only the two bus types we've defined so far, there is a feasibility issue and a uniqueness issue. Firstly, active power losses due to electrical resistance in the power lines and transformers mean that the total power supplied by the generators does not necessarily equal the total power demanded by the loads plus the power losses. The deficit must be made up for by one or more generators at one or more buses, at which $P$ must thus be free to vary. Otherwise, there would not necessarily be a feasible solution. Secondly, voltage angles are relative, so at one bus, $\delta_i$ must be fixed to $0^\circ$ as a reference against which all other $\delta_i$s are measured. Otherwise, there would be no unique solution. By convention, both the feasibility issue and the uniqueness issue are solved by the same bus. This third type of bus is known as a slack bus, also known as a **swing bus**, **reference bus**, or **Vδ bus**.

The following table summarizes the bus types and their variable classifications.

| Bus type     | $P_i$             | $Q_i$         | $V_i$                               | $\delta_i$                   |
|--------------|-------------------|---------------|-------------------------------------|------------------------------|
| Load/PQ      | Fixed by load     | Fixed by load | Free                                | Free                         |
| Generator/PV | Fixed by dispatch | Free          | Fixed by grid operating requirement | Free                         |
| Slack/Vδ     | Free              | Free          | Fixed by grid operating requirement | Fixed to $0^\circ$ reference |

As an example of how these bus classifications would apply, consider the electrical grid of Figure 6.4. Buses 2 and 3 are both load buses (even though bus 2 has no attached load). Either of buses 1 and 4 can be a generator bus (even though bus 4 has an attached load), but one of them must be a slack bus.

```{figure} img/fig_6_4.png
:width: 64%
:label: fig_6_4

Single-line diagram of another example electrical grid. 
```

## Deriving the power flow equations

$$
\left( \frac{S_i}{V_i} \right)^{\!*} = \sum_{k \, \in \, \mathbf{K}_i} (V_i - V_k) \, y_{ik} + V_i \sum_{k \, \in \, \mathbf{K}_i} \frac{y_{ik}^\text{Sh}}{2}
$$

Taking the conjugate of both sides:

$$
\frac{S_i}{V_i} = \left\{ \, \sum_{k \, \in \, \mathbf{K}_i} (V_i - V_k) \, y_{ik} \right\}^{\!*} + V_i^* \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
$$

Multiplying both sides by $V_i$:

$$
S_i = V_i \left\{ \, \sum_{k \, \in \, \mathbf{K}_i} (V_i - V_k) \, y_{ik} \right\}^{\!*} + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
$$

Substituting $V_i = |V_i| \cos \delta_i + j \, |V_i| \sin \delta_i$ and $y_{ik} = g_{ik} + j b_{ik}$:

$$
\begin{aligned}
    S_i
    & = V_i \left\{ \, \sum_{k \, \in \, \mathbf{K}_i} (|V_i| \cos \delta_i + j \, |V_i| \sin \delta_i - |V_k| \cos \delta_k - j \, |V_k| \sin \delta_k) (g_{ik} + j b_{ik}) \right\}^{\!*} \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Expanding the parenthesized factors:

$$
\begin{aligned}
    S_i
    & = V_i \left\{ \, \sum_{k \, \in \, \mathbf{K}_i} \! \left(
    \begin{aligned}
        \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, g_{ik} - (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, b_{ik} \bigr] \\
        + \, j \, \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, b_{ik} + (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, g_{ik} \bigr]
    \end{aligned}
    \right) \right\}^{\!*} \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Substituting $V_i = |V_i| \cos \delta_i + j \, |V_i| \sin \delta_i$ and conjugating the first summation:

$$
\begin{aligned}
    S_i
    & = (|V_i| \cos \delta_i + j \, |V_i| \sin \delta_i) \sum_{k \, \in \, \mathbf{K}_i} \! \left(
    \begin{aligned}
        \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, g_{ik} - (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, b_{ik} \bigr] \\
        - \, j \, \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, b_{ik} + (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, g_{ik} \bigr] \\
    \end{aligned}
    \right) \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Expanding:

$$
\begin{aligned}
    S_i
    & = \sum_{k \, \in \, \mathbf{K}_i} \left(
    \begin{aligned}
        |V_i| \cos \delta_i \, \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, g_{ik} - (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, b_{ik} \bigr] & \\
        - \, j \, |V_i| \cos \delta_i \, \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, b_{ik} + (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, g_{ik} \bigr] & \\
        + \, j \, |V_i| \sin \delta_i \, \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, g_{ik} - (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, b_{ik} \bigr] & \\
        + \,\:\:\, |V_i| \sin \delta_i \, \bigl[ (|V_i| \cos \delta_i - |V_k| \cos \delta_k) \, b_{ik} + (|V_i| \sin \delta_i - |V_k| \sin \delta_k) \, g_{ik} \bigr] &
    \end{aligned}
    \right) \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Expanding further, grouping into real and imaginary parts, and grouping by $g_{ik}$ and $b_{ik}$ therewithin:

$$
\begin{aligned}
    S_i
    & = \sum_{k \, \in \, \mathbf{K}_i} \left(
    \begin{aligned}
        & \left[
        \begin{aligned}
            & \bigl[ |V_i|^2 \cos^2 \delta_i - |V_i| |V_k| \cos \delta_i \cos \delta_k + |V_i|^2 \sin^2 \delta_i - |V_i| |V_k| \sin \delta_i \sin \delta_k \bigr] g_{ik} \\
            & \bigl[ - |V_i|^2\sin \delta_i \cos \delta_i + |V_i| |V_k| \cos \delta_i \sin \delta_k + |V_i|^2\sin \delta_i \cos \delta_i - |V_i| |V_k| \sin \delta_i \cos \delta_k \bigr] b_{ik} \\
        \end{aligned}
        \right] \\
        & + \, j \! \left[
        \begin{aligned}
            & \bigl[ - |V_i|^2 \cos^2 \delta_i + |V_i| |V_k| \cos \delta_i \cos \delta_k - |V_i|^2 \sin^2 \delta_i + |V_i| |V_k| \sin \delta_i \sin \delta_k \bigr] b_{ik} \\
            & + \bigl[ - |V_i|^2\sin \delta_i \cos \delta_i + |V_i| |V_k| \cos \delta_i \sin \delta_k + |V_i|^2\sin \delta_i \cos \delta_i - |V_i| |V_k| \sin \delta_i \cos \delta_k \bigr] g_{ik}
        \end{aligned}
        \right]
    \end{aligned}
    \right) \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Applying $|V_i|^2 \sin^2 \delta_i + |V_i|^2 \cos^2 \delta_i = |V_i|^2$ via the Pythagorean identity, cancelling out the $|V_i|^2 \sin \delta_i \cos \delta_i$ terms, and grouping:

$$
\begin{aligned}
    S_i
    & = \sum_{k \, \in \, \mathbf{K}_i} \! \left(
    \begin{aligned}
        & |V_i|^2 \, g_{ik} - |V_i| |V_k| (\cos \delta_i \cos \delta_k + \sin \delta_i \sin \delta_k) \, g_{ik} + |V_i| |V_k| (\cos \delta_i \sin \delta_k - \sin \delta_i \cos \delta_k) \, b_{ik} \\
        & + j \, [- |V_i|^2 \, b_{ik} - |V_i| |V_k| (\cos \delta_i \cos \delta_k + \sin \delta_i \sin \delta_k) \, b_{ik} - |V_i| |V_k| (\sin \delta_i \cos \delta_k + \cos \delta_i \sin \delta_k) \, g_{ik}]
    \end{aligned}
    \right) \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Applying the angle-difference identities $\cos \alpha \cos \beta + \sin \alpha \sin \beta = \cos(\alpha - \beta)$ and $\sin \alpha \cos \beta - \cos \alpha \sin \beta = \sin(\alpha - \beta)$:

$$
\begin{aligned}
    S_i
    & = \sum_{k \, \in \, \mathbf{K}_i} \! \left(
    \begin{aligned}
        & |V_i|^2 \, g_{ik} - |V_i| |V_k| \cos(\delta_i - \delta_k) \, g_{ik} - |V_i| |V_k| \sin(\delta_k - \delta_i) \, b_{ik} \\
        & + j \, [- |V_i|^2 \, b_{ik} - |V_i| |V_k| \cos(\delta_i - \delta_k) \, b_{ik} + |V_i| |V_k| \sin(\delta_i - \delta_k) \, g_{ik}]
    \end{aligned}
    \right) \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \frac{(y_{ik}^\text{Sh})^*}{2}
\end{aligned}
$$

Simplifying $|V_i|^2 \, g_{ik} - j \, |V_i|^2 \, b_{ik}$ to $|V_i|^2 \, y_{ik}^*$, moving it from the first summation to the second, and factoring out $|V_i|$ and $|V_k|$ from the first:

$$
\begin{aligned}
    S_i
    & = |V_i| \sum_{k \, \in \, \mathbf{K}_i} \! \left[ \, |V_k| \left(
    \begin{aligned}
        & - \! \cos(\delta_i - \delta_k) \, g_{ik} - \sin(\delta_k - \delta_i) \, b_{ik} \\
        & + j \, [- \! \cos(\delta_i - \delta_k) \, b_{ik} + \sin(\delta_i - \delta_k) \, g_{ik}]
    \end{aligned}
    \right) \right] \\
    & + |V_i|^2 \sum_{k \, \in \, \mathbf{K}_i} \! \left( y_{ik}^* + \frac{(y_{ik}^\text{Sh})^*}{2} \right)
\end{aligned}
$$

The traditional power flow problem is typically formulated in a way that allows some complexity to be moved out of this equation. If we TODO
