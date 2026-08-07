from __future__ import annotations

import abc
from dataclasses import dataclass, field
from math import atan2, cos, degrees, pi, radians, sin
from typing import Self

from sympy import Symbol, nsolve


@dataclass
class Phasor:
    magnitude: float
    phase_deg: float = 0.0

    @classmethod
    def from_complex(cls, value: complex) -> Self:
        return cls(
            magnitude=abs(value), phase_deg=degrees(atan2(value.real, value.imag))
        )

    @property
    def phase_rad(self) -> float:
        return radians(self.phase_deg)

    def to_complex(self) -> complex:
        return self.magnitude * (cos(self.phase_deg) + 1j * sin(self.phase_deg))


@dataclass(kw_only=True)
class Symbolic:
    value: Phasor | None = None

    @property
    def variable(self) -> Symbol:
        return Symbol(str(self))


@dataclass
class Voltage(Symbolic):
    node: Node

    def __str__(self) -> str:
        return f"({self.node} voltage)"


@dataclass
class Current(Symbolic):
    terminal: Term

    def __str__(self) -> str:
        return f"({self.terminal} current)"


@dataclass
class Node:
    name: str
    is_ground: bool = False
    voltage: Voltage = field(init=False)
    connected_terminals: list[Term] = field(init=False)

    def __post_init__(self):
        self.voltage = Voltage(node=self)
        # Appended to by `BaseComponent.__post_init__`s:
        self.connected_terminals = []

    def __str__(self) -> str:
        return f"node {self.name}"

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def currents(self) -> list[Current]:
        return [t.current for t in self.connected_terminals]

    @property
    def equations(self):
        if self.is_ground:
            equations = [self.voltage.variable]
        else:
            equations = [sum(c.variable for c in self.currents)]  # type: ignore
        return equations


@dataclass
class Term:
    """A component terminal."""

    connected_node: Node

    current: Current = field(init=False)

    # Set by `BaseComponent._name_terminals`:
    name: str = field(init=False)
    # Set by `BaseComponent.__post_init__`s:
    component: BaseComponent = field(init=False)

    def __post_init__(self):
        self.current = Current(terminal=self)

    def __str__(self) -> str:
        return f"{self.component.name} {self.name} terminal"

    def __repr__(self) -> str:
        return f"({self})"

    @property
    def voltage(self) -> Voltage:
        return self.connected_node.voltage


@dataclass(repr=False)
class BaseComponent(abc.ABC):
    name: str
    negative: Term
    positive: Term

    def __repr__(self) -> str:
        return f"({type(self)} {self.name})"

    @property
    def terminals(self) -> list[Term]:
        return [self.negative, self.positive]

    @property
    def _connected_nodes(self) -> list[Node]:
        return [t.connected_node for t in self.terminals]

    @property
    def currents(self) -> list[Current]:
        return [t.current for t in self.terminals]

    def __post_init__(self):
        self._name_terminals()
        for terminal in self.terminals:
            terminal.component = self
        for terminal in self.terminals:
            terminal.connected_node.connected_terminals.append(terminal)

    def _name_terminals(self) -> None:
        self.negative.name = "negative"
        self.positive.name = "positive"

    def all_equations(self, frequency_rad_per_s: float):
        return [
            sum(c.variable for c in self.currents),  # type: ignore
            *self._equations(frequency_rad_per_s),
        ]

    @abc.abstractmethod
    def _equations(self, frequency_rad_per_s: float):
        raise NotImplementedError

    @property
    def _current(self) -> Current:
        """A positive value indicates current flowing from the `positive` terminal to the `negative`
        terminal.
        """
        return self.negative.current

    @property
    def _voltage_difference(self):
        return self.positive.voltage.variable - self.negative.voltage.variable  # type: ignore

    @property
    def _voltage_difference_value(self) -> float | None:
        return (
            None
            if self.positive.voltage.value is None
            else (self.positive.voltage.value - self.negative.voltage.value)  # type: ignore
        )


@dataclass(repr=False)
class VoltageSource(BaseComponent):
    voltage: Phasor

    def _equations(self, frequency_rad_per_s: float):
        return [self._voltage_difference - self.voltage.to_complex()]


@dataclass(repr=False)
class CurrentSource(BaseComponent):
    current: Phasor

    def _equations(self, frequency_rad_per_s: float):
        return [self._current.variable - self.current.to_complex()]  # type: ignore


@dataclass(repr=False)
class Resistor(BaseComponent):
    resistance_ohm: float

    def _equations(self, frequency_rad_per_s: float):
        return [
            self._voltage_difference - self._current.variable * self.resistance_ohm  # type: ignore
        ]


@dataclass(repr=False)
class Inductor(BaseComponent):
    inductance_h: float

    def _equations(self, frequency_rad_per_s: float):
        return [
            self._voltage_difference
            - self._current.variable * (1j * frequency_rad_per_s * self.inductance_h)  # type: ignore
        ]


@dataclass(repr=False)
class Capacitor(BaseComponent):
    capacitance_f: float

    def _equations(self, frequency_rad_per_s: float):
        return [
            self._voltage_difference
            - self._current.variable * -1j / (frequency_rad_per_s * self.capacitance_f)  # type: ignore
        ]


@dataclass
class AcCircuitSolver:
    frequency_hz: float
    components: list[BaseComponent]
    _symbolics: list[Symbolic] = field(init=False)

    def __post_init__(self):
        self._symbolics = self._get_symbolics()

    def _get_symbolics(self) -> list[Symbolic]:
        symbolics: list[Symbolic] = []
        for n in self._connected_nodes:
            symbolics.append(n.voltage)
        for c in self.components:
            for terminal in c.terminals:
                symbolics.append(terminal.current)
        return symbolics

    @property
    def _connected_nodes(self) -> list[Node]:
        nodes: list[Node] = []
        for component in self.components:
            nodes += component._connected_nodes
        return list(set(nodes))

    def solve(self):
        unknowns = [s.variable for s in self._symbolics]
        initial_guess = [0.0 for s in self._symbolics]
        solution = nsolve(self._equations, unknowns, initial_guess)
        for unknown, solved_value in zip(self._symbolics, solution):
            unknown.value = Phasor.from_complex(complex(solved_value))

    @property
    def _equations(self):
        equations = []
        for n in self._connected_nodes:
            equations += n.equations
        for c in self.components:
            equations += c.all_equations(
                frequency_rad_per_s=(2 * pi * self.frequency_hz)
            )
        return equations


def main() -> None:
    vs1p = Node("vs1p")
    vs1n = Node("vs1n", is_ground=True)
    a = Node("vs2p")
    b = Node("vs2n")
    solver = AcCircuitSolver(
        frequency_hz=(3 / (2 * pi)),
        components=[
            vs1 := VoltageSource(
                "Vs1", Term(vs1n), Term(vs1p), voltage=Phasor(magnitude=1)
            ),
            vs2 := VoltageSource("Vs2", Term(b), Term(a), voltage=Phasor(magnitude=2)),
            r1 := Resistor("R1", Term(b), Term(vs1p), resistance_ohm=4),
            r2 := Resistor("R2", Term(vs1n), Term(a), resistance_ohm=5),
            l := Inductor("L", Term(a), Term(vs1p), inductance_h=6),
            c := Capacitor("C", Term(vs1n), Term(b), capacitance_f=7),
        ],
    )
    solver.solve()
    print(f"{a.voltage.value = }")
    print(f"{b.voltage.value = }")


if __name__ == "__main__":
    main()
