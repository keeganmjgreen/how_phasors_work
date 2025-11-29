from typing import Literal

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from plotting_utils import rm

LETTERS = "abcdefghijklmnopqrstuvwxyz"
_DEFAULT_SEP = ": "
type _LabelSubfigures = Literal["no", "letter_only", "full"]


def process_figure(
    fig: Figure,
    chapter: int,
    number: int,
    label_subfigures: _LabelSubfigures = "full",
) -> None:
    _label_fig(fig, chapter, number, label_subfigures)
    fig.savefig(f"img/fig_{chapter}_{number}.png", dpi=200)


def _label_fig(
    fig: Figure, chapter: int, number: int, label_subfigures: _LabelSubfigures
) -> None:
    prefix = f"Figure {chapter}.{number}"
    if len(fig.axes) == 1:
        [ax] = fig.axes
        _label_ax(ax, prefix)
        assert not fig.get_suptitle()
    else:
        if label_subfigures == "no":
            fig.suptitle(_prefix_text(prefix, fig.get_suptitle()))
        else:
            if fig.get_suptitle() or label_subfigures == "letter_only":
                fig.suptitle(_prefix_text(prefix, fig.get_suptitle()))
                for ax, letter in zip(fig.axes, LETTERS):
                    _label_ax(ax, f"({letter})", sep=" ")
            else:
                for ax, letter in zip(fig.axes, LETTERS):
                    _label_ax(ax, f"{prefix}({letter})")


def _label_ax(ax: Axes, prefix: str, sep: str = _DEFAULT_SEP) -> None:
    ax.set_title(_prefix_text(prefix, ax.title.get_text(), sep))


def _prefix_text(prefix: str, text: str, sep: str = _DEFAULT_SEP) -> str:
    if text:
        return rm(f"{prefix}{sep}{text}")
    else:
        return rm(prefix)
