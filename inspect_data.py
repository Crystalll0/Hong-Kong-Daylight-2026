# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

import csv
from datetime import date, timedelta
from pathlib import Path

DATA = (
    Path(__file__).resolve().parent
    / "data"
    / "hko-sunrise-sunset-2026.csv"
)


def to_minutes(clock):
    """把 HH:MM 转换成午夜之后的分钟数。"""
    hour, minute = map(int, clock.split(":"))

    if not (0 <= hour < 24 and 0 <= minute < 60):
        raise ValueError(f"Invalid time: {clock}")

    return hour * 60 + minute


def main():
    with DATA.open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    expected_dates = [
        date(2026, 1, 1) + timedelta(days=i)
        for i in range(365)
    ]
    actual_dates = [
        date.fromisoformat(row["YYYY-MM-DD"])
        for row in rows
    ]

    if actual_dates != expected_dates:
        raise ValueError("Dates are missing, duplicated or out of order.")

    durations = []

    for row in rows:
        sunrise = to_minutes(row["RISE"])
        noon = to_minutes(row["TRAN."])
        sunset = to_minutes(row["SET"])

        if not sunrise < noon < sunset:
            raise ValueError(f"Unexpected time order: {row}")

        durations.append(sunset - sunrise)

    print(f"Checked {len(rows)} daily records.")
    print(f"First row: {rows[0]}")
    print(f"First daylight duration: {durations[0]} minutes.")
    print(f"Shortest: {min(durations)} minutes.")
    print(f"Longest: {max(durations)} minutes.")
    print(f"Difference: {max(durations) - min(durations)} minutes.")


if __name__ == "__main__":
    main()