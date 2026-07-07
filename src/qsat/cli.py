from datetime import datetime, timedelta, timezone

import typer
from rich.console import Console
from rich.table import Table

from qsat.config import DATA_DIR
from qsat.domain.models import Target
from qsat.orbits.access import find_access_windows
from qsat.orbits.tle import fetch_tle_group

app = typer.Typer(help="QSAT Scheduler - satellite pass planner")
console = Console()

@app.command() # decorator registers func as a subcommand CLI / routing
def passes(
        group: str  = typer.Option("stations", help="CelesTrak group name"),
        sat_name: str = typer.Option("ISS (ZARYA)", "--sat", help="Satellite name"),
        lat: float= typer.Option(..., help="Observer latitude"),
        lon: float = typer.Option(..., help="Observer longitude"),
        hours: int = typer.Option(24, help="Look-ahead window in hours")
) -> None:
    """ Show upcoming passes of SAT over a ground location. """
    sats = fetch_tle_group(group, DATA_DIR / "tle")
    matches = [s for s in sats if sat_name.upper() in s.name.upper()]
    if not matches:
        typer.echo(f"Satellite '{sat_name}' not found in group '{group}'")
        raise typer.Exit(1)

    sat = matches[0]
    target = Target(name="observer", lat=lat, lon=lon, value=1.0)
    start = datetime.now(timezone.utc)
    end = start + timedelta(hours=hours)
    windows = find_access_windows(sat, target, start, end)

    table = Table(title=f"{sat.name} passes - next {hours}h")
    table.add_column("Rise UTC")
    table.add_column("Culminate UTC")
    table.add_column("Set UTC")
    table.add_column("Max El")

    for w in windows:
        table.add_row(
            w.rise.strftime("%H:%M:%S"),
            w.culminate.strftime("%H:%M:%S"),
            w.set_.strftime("%H:%M:%S"),
            f"{w.max_elevation_deg:.1f}"
        )

    console.print(table)

