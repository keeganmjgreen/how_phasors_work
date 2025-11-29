import warnings
from typing import Literal

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def configure_matplotlib(fontsize: int = 12) -> None:
    warnings.filterwarnings("ignore", category=UserWarning)
    plt.rcParams.update({"text.usetex": True, "font.size": fontsize})


def format_xaxis(
    ax: Axes, x_texts: bool = False, start_at: Literal[0, "-pi/2"] = "-pi/2"
) -> None:
    if start_at == "-pi/2":
        start = -1 * np.pi / 2
        xticklabels = [r"$- \pi / 2$", r"$0$", r"$\pi / 2$", r"$\pi$", r"$3 \pi / 2$"]
    else:
        start = 0
        xticklabels = ["$0$", r"$\pi / 2$", r"$\pi$", r"$3 \pi / 2$", r"$2 \pi$"]

    end = start + 2 * np.pi
    ax.set_xlim((start, end))
    delta = np.pi / 2
    ax.set_xticks(np.arange(start, end + delta, delta))
    if x_texts:
        ax.set_xticklabels(xticklabels)
    else:
        ax.set_xticklabels([])


def set_discrete_colors(ax: Axes) -> None:
    ax.set_prop_cycle(
        color=[
            # https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors
            "#1565C0",  # Blue 800.
            "#EF6C00",  # Orange 800.
            "#2E7D32",  # Green 800.
            "#C62828",  # Red 800.
            "#6A1B9A",  # Purple 800.
            # "#F9A825",  # Yellow 800.
        ]
    )


def rm(s: str) -> str:
    return rf"\rm {s}"
