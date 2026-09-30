# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

import csv
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from inspect_data import to_minutes

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "hko-sunrise-sunset-2026.csv"
OUT = HERE / "out" / "daylight-2026.png"

BAND_ALPHA = 0.25


def load_solar_times():
    """读取每日太阳时刻，并换算成小时。"""
    days = []
    sunrises = []
    noons = []
    sunsets = []

    with DATA.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            day = date.fromisoformat(row["YYYY-MM-DD"])
            sunrise = to_minutes(row["RISE"])
            noon = to_minutes(row["TRAN."])
            sunset = to_minutes(row["SET"])

            if not sunrise < noon < sunset:
                raise ValueError(f"Unexpected time order: {day}")

            days.append(day)
            sunrises.append(sunrise / 60)
            noons.append(noon / 60)
            sunsets.append(sunset / 60)

    return days, sunrises, noons, sunsets


def main():
    days, sunrises, noons, sunsets = load_solar_times()

    durations = [
        sunset - sunrise
        for sunrise, sunset in zip(sunrises, sunsets)
    ]

    fig, (upper, lower) = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    # 上图：太阳时刻与白昼色带。
    upper.fill_between(
        days,
        sunrises,
        sunsets,
        color="#f4ddb1",
        alpha=BAND_ALPHA,
    )

    upper.plot(
        days, sunrises,
        label="Sunrise", color="#bc6b32",
    )
    upper.plot(
        days, noons,
        label="Solar noon", color="#283b52", linestyle="--",
    )
    upper.plot(
        days, sunsets,
        label="Sunset", color="#a35b84",
    )

    upper.set_title("Hong Kong: sunrise to sunset, 2026")
    upper.set_ylabel("Hong Kong time (UTC+8)")
    upper.set_ylim(0, 24)
    upper.set_yticks(
        [0, 6, 12, 18, 24],
        ["00:00", "06:00", "12:00", "18:00", "24:00"],
    )
    upper.legend(loc="upper right", frameon=False)

    # 下图：每日白昼长度。
    lower.plot(days, durations, color="#b36b40")
    lower.axhline(
        12, color="gray", linestyle="--",
        linewidth=0.8, label="12-hour reference",
    )

    lower.set_ylabel("Daylight duration (hours)")
    lower.set_xlabel("Month")
    lower.set_ylim(10, 14)
    lower.set_yticks([10, 11, 12, 13, 14])
    lower.set_xlim(days[0], days[-1])
    lower.legend(frameon=False)

    lower.xaxis.set_major_locator(mdates.MonthLocator())
    lower.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    fig.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)

    print(f"Saved out/{OUT.name} using {len(days)} daily records.")


if __name__ == "__main__":
    main()