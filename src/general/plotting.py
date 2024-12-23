# from os import path

# import matplotlib.pyplot as plt
# from entanglement.data_handling import REPO_PATH

# plt.style.use(path.join(REPO_PATH, "src", "entanglement", "paper.mplstyle"))

# # Figure Sizes
# MM = 1 / 25.4
# COL = 86 * MM
# COL_DUB = 178 * MM
# FIT_KW = {"color": "black", "linestyle": "dashed"}
# DATA_KW = {"color": "darkblue"}

from os import path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from src.general.data_handling import REPO_PATH

plt.style.use(path.join(REPO_PATH, "src", "general", "paper.mplstyle"))

# Figure Sizes
MM = 1 / 25.4
COL = 72 * MM
COL_DUB = 150 * MM
## LATEX TEXTWIDTH = 15.917 cm = 159.17 mm
ALPHA_TRANSPARENT = 0.7
FIG_MARGIN = 1.5

# STANDARD PLOT SETTINGS
RED_TINTS = [
    (0.7647058823529411, 0.11764705882352941, 0.13725490196078433),
    (1.0, 0.35294117647058826, 0.3686274509803922),
    (0.6941176470588235, 0.8, 0.7725490196078432),
    (0.00392156862745098, 0.30196078431372547, 0.3058823529411765)
]
BLUE_TINTS = [
    "#2066a8", "#3594cc", "#8cc5e3"
]
HARVARD_COLORS = {
    "red": "#ed1b34",
    "salmon": "#ec8f9c",
    "black": "#000000",
    "gray": "#93a1ad",
    "green": "#4db848",
    "lime green": "#cbdb2a",
    "sky blue": "#95b5df",
    "warm yellow": "fcb315",
    "yellow": "ffde2d",
    "turquoise": "#00aaad",
    "aquamarine": "77ced9",
    "purple": "946eb7",
    "lavender": "bb89ca,"
}
DATA_COLOR = "#253b6e"
DATA_COLOR_TRANSPARENT = to_rgba(DATA_COLOR, ALPHA_TRANSPARENT)
DATA_KW = {"markeredgecolor": DATA_COLOR, "markerfacecolor": DATA_COLOR_TRANSPARENT}
DATA_SCATTER_KW = {"edgecolor": DATA_COLOR, "facecolor": DATA_COLOR_TRANSPARENT}
OPTIMAL_KW = {"color": "black", "linestyle": "dashed"}
FIT_KW = {"color": "k", "lw": 2, "zorder": 100, "alpha": 0.75}
COHERENCE_KW = {"linestyle": "-.", "color": "gray", "alpha": 0.5}
TRANSITION_DOWN_COLOR = "#9c1111"
TRANSITION_UP_COLOR = "#f7543b"
GREEN = "#1d7b3d"
GREEN_BLUE = "#00777a"
YELLOW = "#f1b71c"


def set_margins(fig, margin_mm=FIG_MARGIN):
    w = fig.get_figwidth() / MM
    h = fig.get_figheight() / MM
    fig.get_layout_engine().set(
        rect=[
            margin_mm / w,
            margin_mm / h,
            (w - 2 * margin_mm) / w,
            (h - 2 * margin_mm) / h,
        ]
    )
    fig.get_layout_engine().execute(fig)
    return fig