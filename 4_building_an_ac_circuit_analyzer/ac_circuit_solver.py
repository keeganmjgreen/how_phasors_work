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

    @property
    def phase_rad(self) -> float:
        return radians(self.phase_deg)

    @classmethod
    def from_complex(cls, value: complex) -> Self:
        return cls(
            magnitude=abs(value),
            phase_deg=degrees(atan2(value.real, value.imag)),
        )

    def to_complex(self) -> complex:
        return self.magnitude * (
            cos(self.phase_deg) + 1j * sin(self.phase_deg)
        )

    def __repr__(self) -> str:
        return f"{self.magnitude:.6f} @ {self.phase_deg:.3f}°"


@dataclass(kw_only=True)
class _Symbolic:
    value: Phasor | None = None

    @property
    def variable(self) -> Symbol:
        return Symbol(str(self))


@dataclass
class Voltage(_Symbolic):
    node_name: str

    def __str__(self) -> str:
        return f"(node {self.node_name} voltage)"


@dataclass
class Current(_Symbolic):
    """A positive value indicates current flowing from the
    `positive` terminal to the `negative` terminal.
    """

    component_name: str

    def __str__(self) -> str:
        return f"(component {self.component_name} current)"


@dataclass(repr=False)
class Node:
    name: str
    is_ground: bool = False
    voltage: Voltage = field(init=False)
    connected_components: list[_BaseComponent] = field(
        init=False
    )

    def __post_init__(self):
        self.voltage = Voltage(node_name=self.name)
        # Appended to by `BaseComponent.__post_init__`s:
        self.connected_components = []

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def equation(self):
        if self.is_ground:
            return self.voltage.variable
        else:
            return sum(
                c.current.variable
                * (1 if c.positive is self else -1)  # type: ignore
                for c in self.connected_components
            )


@dataclass(repr=False)
class _BaseComponent(abc.ABC):
    name: str
    negative: Node
    positive: Node
    current: Current = field(init=False)

    def __post_init__(self):
        self.current = Current(component_name=self.name)
        for node in self._connected_nodes:
            node.connected_components.append(self)

    @property
    def _connected_nodes(self) -> list[Node]:
        return [self.negative, self.positive]

    @abc.abstractmethod
    def equation(self, frequency_rad_per_s: float):
        raise NotImplementedError

    @property
    def voltage_difference(self):
        return (
            self.positive.voltage.variable
            - self.negative.voltage.variable
        )  # type: ignore

    # @property
    # def voltage_difference_value(self) -> Phasor | None:
    #     if (
    #         self.positive.voltage.value is None
    #         or self.negative.voltage.value is None
    #     ):
    #         return None
    #     return Phasor.from_complex(
    #         self.positive.voltage.value.to_complex()
    #         - self.negative.voltage.value.to_complex()
    #     )


@dataclass(repr=False)
class VoltageSource(_BaseComponent):
    value: Phasor

    def equation(self, frequency_rad_per_s: float):
        return self.voltage_difference - self.value.to_complex()


@dataclass(repr=False)
class CurrentSource(_BaseComponent):
    value: Phasor  # type: ignore

    def equation(self, frequency_rad_per_s: float):
        return self.current.variable - self.value.to_complex()  # type: ignore


@dataclass(repr=False)
class Resistor(_BaseComponent):
    resistance_ohm: float

    def equation(self, frequency_rad_per_s: float):
        return (
            self.voltage_difference
            - self.current.variable * self.resistance_ohm  # type: ignore
        )


@dataclass(repr=False)
class Inductor(_BaseComponent):
    inductance_h: float

    def equation(self, frequency_rad_per_s: float):
        reactance = 1j * frequency_rad_per_s * self.inductance_h
        return (
            self.voltage_difference
            - self.current.variable * reactance  # type: ignore
        )


@dataclass(repr=False)
class Capacitor(_BaseComponent):
    capacitance_f: float

    def equation(self, frequency_rad_per_s: float):
        admittance = 1j * (
            frequency_rad_per_s * self.capacitance_f
        )
        return (
            self.voltage_difference * admittance
            - self.current.variable
        )


@dataclass(repr=False)
class AcCircuitSolver:
    frequency_hz: float
    components: list[_BaseComponent]

    def solve(self) -> None:
        connected_nodes = self._get_connected_nodes()
        symbolics = self._get_symbolics(connected_nodes)
        equations = self._get_equations(connected_nodes)
        unknowns = [s.variable for s in symbolics]
        initial_guess = [0.0 for s in symbolics]
        solution = nsolve(equations, unknowns, initial_guess)
        for unknown, solved_value in zip(symbolics, solution):
            unknown.value = Phasor.from_complex(
                complex(solved_value)
            )

    def _get_symbolics(
        self, connected_nodes: list[Node]
    ) -> list[_Symbolic]:
        symbolics: list[_Symbolic] = []
        for n in connected_nodes:
            symbolics.append(n.voltage)
        for c in self.components:
            symbolics.append(c.current)
        return symbolics

    def _get_equations(self, connected_nodes: list[Node]):
        equations = []
        for n in connected_nodes:
            equations.append(n.equation)
        frequency_rad_per_s = 2 * pi * self.frequency_hz
        for c in self.components:
            equations.append(c.equation(frequency_rad_per_s))
        return equations

    def _get_connected_nodes(self) -> list[Node]:
        nodes: list[Node] = []
        for component in self.components:
            nodes += component._connected_nodes
        # Deduplicate (requires `Node.__hash__`):
        nodes = list(set(nodes))
        return nodes


def main() -> None:
    vs1p = Node("Vs1p")
    vs1n = Node("Vs1n", is_ground=True)
    a = Node("Vs2p")
    b = Node("Vs2n")

    vs1 = VoltageSource("Vs1", vs1n, vs1p, Phasor(magnitude=1))
    vs2 = VoltageSource("Vs2", b, a, Phasor(magnitude=2))
    r1 = Resistor("R1", b, vs1p, resistance_ohm=4)
    r2 = Resistor("R2", vs1n, a, resistance_ohm=5)
    l = Inductor("L", a, vs1p, inductance_h=6)
    c = Capacitor("C", vs1n, b, capacitance_f=7)

    solver = AcCircuitSolver(
        frequency_hz=(3 / (2 * pi)),
        components=[vs1, vs2, r1, r2, l, c],
    )
    solver.solve()
    print(f"{a.voltage.value = }")
    print(f"{b.voltage.value = }")


if __name__ == "__main__":
    main()
