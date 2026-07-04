from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.plotting_utils import rm

LETTERS = "abcdefghijklmnopqrstuvwxyz"


def process_figure(
    fig: Figure,
    chapter: int,
    number: int,
    label_subfigures: bool = True,
) -> None:
    _label_fig(fig, label_subfigures)
    fig.savefig(f"img/fig_{chapter}_{number}.png", dpi=200)


def _label_fig(fig: Figure, label_subfigures: bool) -> None:
    if len(fig.axes) > 1:
        if label_subfigures:
            for ax, letter in zip(fig.axes, LETTERS):
                _label_ax(ax, f"({letter})", sep=" ")


def _label_ax(ax: Axes, prefix: str, sep: str) -> None:
    ax.set_title(_prefix_text(prefix, ax.title.get_text(), sep))


def _prefix_text(prefix: str, text: str, sep: str) -> str:
    if text:
        return rm(f"{prefix}{sep}{text}")
    else:
        return rm(prefix)
