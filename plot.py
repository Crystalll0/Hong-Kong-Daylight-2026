# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

import csv
from datetime import date, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
from matplotlib.patches import Circle, Wedge
import numpy as np

from inspect_data import to_minutes

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "hko-sunrise-sunset-2026.csv"
OUT = HERE / "out" / "daylight-2026.png"
SKY_ALPHA = 0.25


def load_solar_times():
    days, times = [], []
    with DATA.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            day = date.fromisoformat(row["YYYY-MM-DD"])
            rise = to_minutes(row["RISE"])
            noon = to_minutes(row["TRAN."])
            setting = to_minutes(row["SET"])
            if not rise < noon < setting:
                raise ValueError(f"Unexpected time order: {day}")
            days.append(day)
            times.append([rise, noon, setting])
    expected = [date(2026, 1, 1) + timedelta(days=i) for i in range(365)]
    if days != expected:
        raise ValueError("Expected all 365 dates of 2026 in order.")
    return days, np.array(times) / 60


def sky_image(times):
    """Colours are illustrative; only solar-time anchors come from data."""
    hours = np.linspace(0, 24, 721)
    colours = np.array([to_rgb(c) for c in [
        "#19294d", "#787398", "#efa47c", "#bcdde7", "#fff1bd",
        "#bcdde7", "#e99aaa", "#787398", "#19294d",
    ]])
    pixels = np.empty((len(hours), len(times), 3))
    for i, (rise, noon, setting) in enumerate(times):
        stops = [0, rise * 0.7, rise, (rise + noon) / 2, noon,
                 (noon + setting) / 2, setting,
                 setting + (24 - setting) * 0.35, 24]
        for channel in range(3):
            pixels[:, i, channel] = np.interp(hours, stops, colours[:, channel])
    return pixels


def add_sun(ax, x, y, colour, half=False):
    """Draw fixed-size sun symbols without image downloads or emoji fonts."""
    icon = DrawingArea(26, 26, 0, 0)
    if half:
        icon.add_artist(Wedge((13, 11), 6, 0, 180, color=colour))
        icon.add_artist(plt.Line2D([3, 23], [11, 11], color=colour, lw=1))
        angles = np.linspace(0, np.pi, 5)
    else:
        icon.add_artist(Circle((13, 11), 6, color=colour))
        angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for angle in angles:
        icon.add_artist(plt.Line2D(
            [13 + 8 * np.cos(angle), 13 + 11 * np.cos(angle)],
            [11 + 8 * np.sin(angle), 11 + 11 * np.sin(angle)],
            color=colour, lw=1,
        ))
    ax.add_artist(AnnotationBbox(icon, (x, y), frameon=False,
                                box_alignment=(0.5, 11 / 26)))


def main():
    days, times = load_solar_times()
    sunrises, noons, sunsets = times.T
    durations = sunsets - sunrises
    x = mdates.date2num(days)
    fig, (upper, lower) = plt.subplots(
        2, 1, figsize=(11, 8), sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )
    upper.imshow(
        sky_image(times), origin="lower", aspect="auto",
        extent=[x[0] - 0.5, x[-1] + 0.5, 0, 24],
        interpolation="nearest", alpha=SKY_ALPHA,
    )
    for values, label, colour, style, half in [
        (sunrises, "Sunrise", "#bc6b32", "-", True),
        (noons, "Solar noon", "#283b52", "--", False),
        (sunsets, "Sunset", "#a35b84", "-", True),
    ]:
        upper.plot(days, values, label=label, color=colour, linestyle=style)
        add_sun(upper, x[20], values[20], colour, half)
    upper.set_title("Hong Kong: a year of daylight, 2026")
    upper.set_ylabel("Hong Kong time (UTC+8)")
    upper.set_ylim(0, 24)
    upper.set_yticks([0, 6, 12, 18, 24],
                    ["00:00", "06:00", "12:00", "18:00", "24:00"])
    upper.legend(loc="upper right", frameon=True, facecolor="white")
    lower.plot(days, durations, color="#b36b40")
    lower.axhline(12, color="gray", linestyle="--", linewidth=0.8,
                  label="12-hour reference")
    lower.set_ylabel("Daylight duration (hours)")
    lower.set_xlabel("Month")
    lower.set_ylim(10, 14)
    lower.set_yticks([10, 11, 12, 13, 14])
    lower.set_xlim(days[0], days[-1])
    lower.legend(frameon=False)
    lower.xaxis.set_major_locator(mdates.MonthLocator())
    lower.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    fig.text(0.09, 0.045, "Source: Hong Kong Observatory | 365 daily records | Times to the minute", fontsize=9)
    fig.text(0.09, 0.02, "Sky colours are illustrative, not measured weather or twilight. Daylight is not bright sunshine.", fontsize=9)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"Saved out/{OUT.name} using {len(days)} daily records.")


if __name__ == "__main__":
    main()