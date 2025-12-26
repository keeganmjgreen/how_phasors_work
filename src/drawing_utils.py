from __future__ import annotations

import abc
from statistics import mean
from typing import Annotated, ClassVar, Literal, Self

import numpy as np
import pydantic
from matplotlib.axes import Axes


def clear_axes(ax: Axes) -> None:
    ax.axis("off")
    ax.set_aspect("equal")


class _Rotatable(abc.ABC):
    def rotated(self, angle: float) -> Self:
        raise NotImplementedError


class _Drawable(abc.ABC):
    def drawn(self, ax: Axes) -> Self:
        raise NotImplementedError


_HorizontalAlignment = Literal["left", "right", "center"]


class _Labelable(abc.ABC):
    def labeled(
        self,
        ax: Axes,
        text: str,
        offset: tuple[float, float] = (0, 0),
        ha: _HorizontalAlignment = "center",
    ) -> Self:
        raise NotImplementedError

    @staticmethod
    def _label(
        ax: Axes,
        loc: Point,
        text: str,
        offset: tuple[float, float],
        ha: _HorizontalAlignment,
    ):
        ax.annotate(
            text,
            xy=loc._xy,
            textcoords="offset points",
            xytext=offset,
            ha=ha,
        )


@pydantic.dataclasses.dataclass
class Point(_Drawable, _Labelable):
    x: float
    y: float

    @classmethod
    def from_point_like(cls: type[Point], point_like: _Pointy) -> Point:
        if isinstance(point_like, Point):
            return point_like
        else:
            return cls(*point_like)

    @property
    def _xy(self) -> tuple[float, float]:
        return self.x, self.y

    def drawn(self, ax: Axes) -> Self:
        ax.plot([self.x], [self.y], "k", linewidth=0, marker=".")
        return self

    def labeled(
        self,
        ax: Axes,
        text: str,
        offset: tuple[float, float] = (0, 0),
        ha: _HorizontalAlignment = "center",
    ) -> Self:
        self._label(ax, self, text, offset, ha)
        return self

    def __add__(self, other: Point) -> Point:
        return Point(
            x=(self.x + other.x),
            y=(self.y + other.y),
        )


_Pointy = Annotated[Point, pydantic.BeforeValidator(Point.from_point_like)]


@pydantic.dataclasses.dataclass
class Segment(_Rotatable, _Drawable):
    _arrowstyle: ClassVar[str] = "-"

    start: _Pointy
    end: _Pointy

    @classmethod
    def from_polar(
        cls: type[Segment], origin: Point, length: float, angle: float
    ) -> Segment:
        return cls(
            start=origin,
            end=Point(
                x=(origin.x + length * np.cos(angle)),
                y=(origin.y + length * np.sin(angle)),
            ),
        )

    @classmethod
    def horizontal(
        cls: type[Segment], y: float = 0.0, x1: float = 0.0, x2: float = 10.0
    ) -> Segment:
        return cls(start=Point(x1, y), end=Point(x2, y))

    @classmethod
    def vertical(
        cls: type[Segment], x: float = 0.0, y1: float = 0.0, y2: float = 10.0
    ) -> Segment:
        return cls(start=Point(x, y1), end=Point(x, y2))

    @property
    def length(self) -> float:
        return np.sqrt(self._dx**2 + self._dy**2)

    @property
    def angle(self) -> float:
        return np.atan2(self._dy, self._dx)

    @property
    def mid(self) -> Point:
        return Point(
            x=mean([self.start.x, self.end.x]),
            y=mean([self.start.y, self.end.y]),
        )

    @property
    def _dx(self) -> float:
        return self.end.x - self.start.x

    @property
    def _dy(self) -> float:
        return self.end.y - self.start.y

    def rotated(self, angle: float) -> Segment:
        return Segment(
            start=self.start,
            end=Point(
                x=(self.start.x + self._dx * np.cos(angle) - self._dy * np.sin(angle)),
                y=(self.start.y + self._dy * np.cos(angle) + self._dx * np.sin(angle)),
            ),
        )

    def drawn(self, ax: Axes, linewidth: float = 0.5) -> Self:
        ax.annotate(
            "",
            xytext=self.start._xy,
            xy=self.end._xy,
            arrowprops=dict(arrowstyle=self._arrowstyle, linewidth=linewidth),
        )
        return self


class Arrow(Segment):
    _arrowstyle: ClassVar[str] = "->"  # type: ignore


@pydantic.dataclasses.dataclass
class Arc(_Rotatable, _Drawable, _Labelable):
    vertex: _Pointy
    start_angle: float
    end_angle: float
    radius: float = 0.4
    label_radius: float = 0.55

    @classmethod
    def from_vertex_start_end(
        cls: type[Arc], vertex: _Pointy, start: _Pointy, end: _Pointy
    ) -> Arc:
        return cls(
            vertex=vertex,
            start_angle=Segment(start=vertex, end=start).angle,
            end_angle=Segment(start=vertex, end=end).angle,
        )

    @property
    def mid(self) -> Point:
        mid_angle = mean([self.start_angle, self.end_angle])
        return Point(
            self.vertex.x + self.label_radius * np.cos(mid_angle),
            self.vertex.y + self.label_radius * np.sin(mid_angle),
        )

    @property
    def angles(self) -> np.ndarray:
        return np.linspace(self.start_angle, self.end_angle)

    def rotated(self, angle: float) -> Arc:
        return Arc(
            vertex=self.vertex,
            start_angle=(self.start_angle + angle),
            end_angle=(self.end_angle + angle),
            radius=self.radius,
            label_radius=self.label_radius,
        )

    def drawn(self, ax: Axes, linewidth: float = 0.5) -> Self:
        ax.plot(
            self.vertex.x + self.radius * np.cos(self.angles),
            self.vertex.y + self.radius * np.sin(self.angles),
            "k",
            linewidth=linewidth,
        )
        return self

    def labeled(
        self,
        ax: Axes,
        text: str,
        offset: tuple[float, float] = (0, 0),
        ha: _HorizontalAlignment = "center",
    ) -> Self:
        self._label(ax, self.mid, text, offset, ha)
        return self
