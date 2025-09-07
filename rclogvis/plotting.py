#
#   2025 Fabian Jankowski
#   Plotting related functions.
#

import matplotlib
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt


def use_custom_matplotlib_formatting():
    """
    Adjust the matplotlib configuration parameters for custom format.
    """

    matplotlib.rcParams["font.family"] = "sans"
    matplotlib.rcParams["font.size"] = 12.0
    matplotlib.rcParams["lines.markersize"] = 8
    matplotlib.rcParams["legend.frameon"] = False
    # make tickmarks more visible
    matplotlib.rcParams["xtick.major.size"] = 6
    matplotlib.rcParams["xtick.major.width"] = 1.5
    matplotlib.rcParams["xtick.minor.size"] = 4
    matplotlib.rcParams["xtick.minor.width"] = 1.5
    matplotlib.rcParams["ytick.major.size"] = 6
    matplotlib.rcParams["ytick.major.width"] = 1.5
    matplotlib.rcParams["ytick.minor.size"] = 4
    matplotlib.rcParams["ytick.minor.width"] = 1.5


def plot_time_series(df, fields, title=""):
    figsize = (6.4, 7.0)
    fig, axs = plt.subplots(figsize=figsize, nrows=len(fields), sharex=True)

    for i, _label in enumerate(fields):
        axs[i].plot(df["flighttime"], df[_label])
        axs[i].grid()

        _nice_label = _label.replace("(", "\n(")
        axs[i].set_ylabel(_nice_label)

    lastax = axs[len(fields) - 1]
    lastax.set_xlabel("Flight time (min)")

    fig.suptitle(title)

    fig.align_ylabels()
    fig.tight_layout()


def plot_gps_trajectory(df):
    fig = plt.figure()
    ax = fig.add_subplot()

    points = np.array(
        [
            (df["longitude"] - df["longitude"].iat[0]).values,
            (df["latitude"] - df["latitude"].iat[0]).values,
        ]
    ).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(df["Alt(m)"].min(), df["Alt(m)"].max())

    lc = LineCollection(segments, cmap="viridis", norm=norm)
    lc.set_array(df["Alt(m)"].astype(float).values)
    lc.set_linewidth(2)
    ax.add_collection(lc)

    plt.colorbar(lc, ax=ax, label="Altitude (m)")

    ax.autoscale()
    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")

    fig.tight_layout()
