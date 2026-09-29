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


def load_daylight():
    """读取日期，并计算每天的白昼小时数。"""
    days = []
    hours = []

    with DATA.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            day = date.fromisoformat(row["YYYY-MM-DD"])
            sunrise = to_minutes(row["RISE"])
            sunset = to_minutes(row["SET"])

            days.append(day)
            hours.append((sunset - sunrise) / 60)

    return days, hours


def main():
    days, hours = load_daylight()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(days, hours)

    ax.set_title("Hong Kong daylight duration, 2026")
    ax.set_xlabel("Month")
    ax.set_ylabel("Daylight duration (hours)")
    ax.set_xlim(days[0], days[-1])

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    fig.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)

    print(f"Saved out/{OUT.name} using {len(days)} daily records.")


if __name__ == "__main__":
    main()