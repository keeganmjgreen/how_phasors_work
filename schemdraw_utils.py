from __future__ import annotations

import abc
from copy import deepcopy
import dataclasses
from enum import Enum, auto

import schemdraw
import schemdraw.elements as elm


class _Direction(Enum):
    POSITIVE = auto()
    NEGATIVE = auto()

    @property
    def opposite(self) -> _Direction:
        return {
            _Direction.POSITIVE: _Direction.NEGATIVE,
            _Direction.NEGATIVE: _Direction.POSITIVE,
        }[self]


class _Axis(Enum):
    HORIZONTAL = auto()
    VERTICAL = auto()

    @property
    def opposite(self) -> _Axis:
        return {
            _Axis.HORIZONTAL: _Axis.VERTICAL,
            _Axis.VERTICAL: _Axis.HORIZONTAL,
        }[self]


@dataclasses.dataclass(unsafe_hash=True)
class _Orientation:
    direction: _Direction
    axis: _Axis

    @property
    def cardinal(self) -> Cardinal:
        cardinal_by_orientation = {
            cardinal.orientation: cardinal for cardinal in Cardinal.__members__.values()
        }
        return cardinal_by_orientation[self]  # type: ignore

    @property
    def with_opposite_direction(self) -> _Orientation:
        copy = deepcopy(self)
        copy.direction = self.direction.opposite
        return copy


class Cardinal(Enum):
    UP = _Orientation(_Direction.POSITIVE, _Axis.VERTICAL)
    RIGHT = _Orientation(_Direction.POSITIVE, _Axis.HORIZONTAL)
    DOWN = _Orientation(_Direction.NEGATIVE, _Axis.VERTICAL)
    LEFT = _Orientation(_Direction.NEGATIVE, _Axis.HORIZONTAL)

    @property
    def orientation(self) -> _Orientation:
        return self.value

    @property
    def cw(self) -> Cardinal:
        return {
            Cardinal.UP: Cardinal.RIGHT,
            Cardinal.RIGHT: Cardinal.DOWN,
            Cardinal.DOWN: Cardinal.LEFT,
            Cardinal.LEFT: Cardinal.UP,
        }[self]

    @property
    def ccw(self) -> Cardinal:
        return self.cw.orientation.with_opposite_direction.cardinal


@dataclasses.dataclass
class _ParallelLines(abc.ABC):
    d: schemdraw.Drawing
    w: float

    @abc.abstractmethod
    def draw_element(
        self, elm_class: type[elm.Element2Term], cardinal: Cardinal
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def draw_lines(self, cardinal: Cardinal, length: float) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def draw_node(self) -> None:
        raise NotImplementedError


class SinglePhaseLines(_ParallelLines):
    def draw_element(
        self, elm_class: type[elm.Element2Term], cardinal: Cardinal
    ) -> None:
        self._draw_cap(cardinal)
        self.d.push()
        self._half_w_move(cardinal.orientation)
        self._half_w_move(cardinal.ccw.orientation)
        getattr(
            elm_class().length(self.w), cardinal.cw.orientation.cardinal.name.lower()
        )()
        self.d.pop()

    def _draw_cap(self, cardinal: Cardinal) -> None:
        self.d.push()
        self._half_w_move(cardinal.orientation)
        self._half_w_move(cardinal.ccw.orientation)
        getattr(
            elm.Line().length(self.w),
            cardinal.orientation.with_opposite_direction.cardinal.name.lower(),
        )()
        self.d.pop()

    def draw_lines(self, cardinal: Cardinal, length: float) -> None:
        self.d.push()
        self._half_w_move(Cardinal.UP.value)
        self._half_w_move(Cardinal.LEFT.value)
        line = elm.Line().length(length)
        getattr(line, cardinal.name.lower())()
        self.d.pop()
        self._half_w_move(Cardinal.DOWN.value)
        self._half_w_move(Cardinal.RIGHT.value)
        line = elm.Line().length(length)
        getattr(line, cardinal.name.lower())()
        self._half_w_move(Cardinal.UP.value)
        self._half_w_move(Cardinal.LEFT.value)

    def draw_node(self) -> None:
        self.d.push()
        self._half_w_move(Cardinal.UP.value)
        self._half_w_move(Cardinal.LEFT.value)
        elm.Dot()
        self.d.pop()
        self.d.push()
        self._half_w_move(Cardinal.DOWN.value)
        self._half_w_move(Cardinal.RIGHT.value)
        elm.Dot()
        self.d.pop()

    def _half_w_move(self, orientation: _Orientation) -> None:
        self._move(orientation, dist=(self.w / 2))

    def _move(self, orientation: _Orientation, dist: float) -> None:
        match orientation.cardinal:
            case Cardinal.UP:
                self.d.move(0, dist)
            case Cardinal.RIGHT:
                self.d.move(dist, 0)
            case Cardinal.DOWN:
                self.d.move(0, -1 * dist)
            case Cardinal.LEFT:
                self.d.move(-1 * dist, 0)
            case _:
                raise ValueError
