from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt

from qsat.domain.models import Satellite, Target
from qsat.orbits.propagate import subpoint


def ground_track(
        sat: Satellite,
        start: datetime,
        end: datetime,
        step_s: float = 60
) -> tuple[list[float, float]]:
    """ Returns (lons, lats) of sat groud track from start to end """
    lats, lons = [], []
    t = start
    while t <= end:
        lat, lon, _ = subpoint(sat, t)
        lats.append(lat)
        lons.append(lon)
        t += timedelta(seconds=step_s)
    return lons, lats


def plot_ground_track(
        lons: list[float],
        lats: list[float],
        targets: list[Target],
        out_path: Path
) -> None:
    """ Save a lat/lon ground track plot with targets to out_path """
    fig, ax = plt.subplots(figsize=(12,6))

    ax.set_xlim(-180,180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("Longitude °")
    ax.set_ylabel("Latitude °")
    ax.grid(True, alpha=0.3)

    # satellite ground track
    ax.plot(lons, lats,"b-", linewidth=1, label="Ground track")

    # target dots
    for t in targets:
        ax.plot(t.lon, t.lat, "r*", markersize=10)
        ax.annotate(t.name, (t.lon, t.lat), textcoords="offset points", xytext=(5,5))

    ax.legend()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)