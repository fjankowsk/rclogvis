#
#   2025 Fabian Jankowski
#   Plot telemetry log data.
#

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from rclogvis.plotting import (
    use_custom_matplotlib_formatting,
    plot_time_series,
    plot_gps_trajectory,
)


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
