# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///

"""Plot every earthquake in September 2026: time vs magnitude, coloured by depth."""

import json
import datetime as dt
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

    times, mags, depths = [], [], []
    for when, mag, depth in quakes:
        times.append(when)
        mags.append(mag)
        depths.append(depth)
    print(f"{len(mags)} magnitudes, from {min(mags):.1f} to {max(mags):.1f}")
    print(f"depths from {min(depths):.0f} km to {max(depths):.0f} km")

    fig, ax = plt.subplots(figsize=(12, 5))
    scatter = ax.scatter(
        times, mags,
        c=depths, cmap="viridis_r",
        s=9, alpha=0.6, edgecolors="none",
    )

    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Magnitude")
    ax.set_title(f"Earthquakes in September 2026 (n={len(mags)})")
    ax.grid(alpha=0.3)

    cbar = fig.colorbar(scatter, ax=ax, shrink=1)
    cbar.set_label("Depth (km)")

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    fig.autofmt_xdate()
    fig.tight_layout()

    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / PICTURE, dpi=150)
    print(f"saved out/{PICTURE}")
    plt.show()


if __name__ == "__main__":
    main()