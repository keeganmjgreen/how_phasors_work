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
    """A positive value indicates current flowing from the `positive` terminal to the `negative`
    terminal.
    """

    component: BaseComponent

    def __str__(self) -> str:
        return f"({self.component} current)"


@dataclass
class Node:
    name: str
    is_ground: bool = False
    voltage: Voltage = field(init=False)
    connected_components: list[BaseComponent] = field(init=False)

    def __post_init__(self):
        self.voltage = Voltage(node=self)
        # Appended to by `BaseComponent.__post_init__`s:
        self.connected_components = []

    def __str__(self) -> str:
        return f"node {self.name}"

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def equation(self):
        if self.is_ground:
            return self.voltage.variable
        else:
            return sum(
                c.current.variable * (1 if c.positive is self else -1)  # type: ignore
                for c in self.connected_components
            )


@dataclass(repr=False)
class BaseComponent(abc.ABC):
    name: str
    negative: Node
    positive: Node
    current: Current = field(init=False)

    def __repr__(self) -> str:
        return f"({type(self)} {self.name})"

    @property
    def _connected_nodes(self) -> list[Node]:
        return [self.negative, self.positive]

    def __post_init__(self):
        self.current = Current(component=self)
        for node in self._connected_nodes:
            node.connected_components.append(self)

    @abc.abstractmethod
    def _equation(self, frequency_rad_per_s: float):
        raise NotImplementedError

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

    def _equation(self, frequency_rad_per_s: float):
        return self._voltage_difference - self.voltage.to_complex()


@dataclass(repr=False)
class CurrentSource(BaseComponent):
    current: Phasor  # type: ignore

    def _equation(self, frequency_rad_per_s: float):
        return super().current.variable - self.current.to_complex()  # type: ignore


@dataclass(repr=False)
class Resistor(BaseComponent):
    resistance_ohm: float

    def _equation(self, frequency_rad_per_s: float):
        return (
            self._voltage_difference - self.current.variable * self.resistance_ohm  # type: ignore
        )


@dataclass(repr=False)
class Inductor(BaseComponent):
    inductance_h: float

    def _equation(self, frequency_rad_per_s: float):
        return (
            self._voltage_difference
            - self.current.variable * (1j * frequency_rad_per_s * self.inductance_h)  # type: ignore
        )


@dataclass(repr=False)
class Capacitor(BaseComponent):
    capacitance_f: float

    def _equation(self, frequency_rad_per_s: float):
        return (
            self._voltage_difference
            - self.current.variable * -1j / (frequency_rad_per_s * self.capacitance_f)  # type: ignore
        )


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
            symbolics.append(Current(c))
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
            equations.append(n.equation)
        for c in self.components:
            equations.append(
                c._equation(frequency_rad_per_s=(2 * pi * self.frequency_hz))
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
            vs1 := VoltageSource("Vs1", vs1n, vs1p, voltage=Phasor(magnitude=1)),
            vs2 := VoltageSource("Vs2", b, a, voltage=Phasor(magnitude=2)),
            r1 := Resistor("R1", b, vs1p, resistance_ohm=4),
            r2 := Resistor("R2", vs1n, a, resistance_ohm=5),
            l := Inductor("L", a, vs1p, inductance_h=6),
            c := Capacitor("C", vs1n, b, capacitance_f=7),
        ],
    )
    solver.solve()
    print(f"{a.voltage.value = }")
    print(f"{b.voltage.value = }")


if __name__ == "__main__":
    main()
