# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""Plot every earthquake in September 2026: time vs magnitude."""

import json
import datetime as dt
from pathlib import Path

import matplotlib.pyplot as plt

FILE = "quakes_september.geojson"
PICTURE = "quakes_september.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def load_quakes(path):
    """Read the EMSC GeoJSON and return a list of (datetime, magnitude, depth_km)."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for feature in raw["features"]:
        props = feature["properties"]
        mag = props["mag"]
        t = props["time"]
        depth = props["depth"]
        if mag is None or t is None or depth is None:
            continue
        when = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
        rows.append((when, mag, depth))
    return rows


def main():
    quakes = load_quakes(DATA)
    print(f"{DATA.name}: {len(quakes)} quakes")

    times, mags = [], []
    for when, mag, depth in quakes:
        times.append(when)
        mags.append(mag)
    print(f"{len(mags)} magnitudes, from {min(mags):.1f} to {max(mags):.1f}")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(times, mags, s=12, alpha=0.5, color="#d6591d", edgecolors="none")

    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Magnitude")
    ax.set_title(f"Earthquakes in September 2026 (n={len(mags)})")
    ax.grid(alpha=0.3)

    fig.autofmt_xdate()
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"saved out/{PICTURE}")


if __name__ == "__main__":
    main()