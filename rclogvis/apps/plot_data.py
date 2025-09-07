#
#   2025 Fabian Jankowski
#   Plot telemetry log data.
#

import argparse

import matplotlib
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


def parse_args():
    """
    Parse the commandline arguments.

    Returns
    -------
    args: populated namespace
        The commandline arguments.
    """

    parser = argparse.ArgumentParser(
        description="Plot telemetry log data.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("filename", type=str, help="Filename to process.")

    args = parser.parse_args()

    return args


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


#
# MAIN
#


def main():
    # handle command line arguments
    args = parse_args()

    use_custom_matplotlib_formatting()

    df = pd.read_csv(args.filename)

    print(df.columns)

    df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df["flighttime"] = (
        df["datetime"] - df["datetime"].iat[0]
    ).dt.total_seconds() / 60.0

    # convert to degrees
    df["Ptch(deg)"] = df["Ptch(rad)"] * 180.0 / np.pi
    df["Roll(deg)"] = df["Roll(rad)"] * 180.0 / np.pi
    df["Yaw(deg)"] = df["Yaw(rad)"] * 180.0 / np.pi

    # split into latitude and longitude
    df[["latitude", "longitude"]] = df["GPS"].str.split(" ", n=1, expand=True)
    df["latitude"] = pd.to_numeric(df["latitude"])
    df["longitude"] = pd.to_numeric(df["longitude"])

    # control link
    fields = [
        "1RSS(dB)",
        "RQly(%)",
        "RSNR(dB)",
        "TPWR(mW)",
        "TRSS(dB)",
        "TQly(%)",
        "TSNR(dB)",
    ]

    plot_time_series(df, fields, title="Control Link")

    # battery
    fields = ["RxBt(V)", "Curr(A)", "Capa(mAh)", "Bat%(%)", "FM"]

    plot_time_series(df, fields, title="Battery")

    # gps
    fields = ["GSpd(kmh)", "Hdg(°)", "Alt(m)", "Sats"]

    plot_time_series(df, fields, title="GPS")

    # attitude
    fields = ["Ptch(deg)", "Roll(deg)", "Yaw(deg)"]

    plot_time_series(df, fields, title="Attitude")

    # stick input
    fields = ["Rud", "Ele", "Thr", "Ail"]

    plot_time_series(df, fields, title="Stick input")

    # gps trajectory
    plot_gps_trajectory(df)

    plt.show()


if __name__ == "__main__":
    main()
