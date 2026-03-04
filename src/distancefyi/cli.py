"""Command-line interface for distancefyi.

Requires: pip install distancefyi[cli]

Usage::

    distancefyi calc --lat1 37.5665 --lon1 126.978 --lat2 35.6762 --lon2 139.6503
    distancefyi bearing --lat1 37.57 --lon1 126.98 --lat2 35.68 --lon2 139.65
    distancefyi midpoint --lat1 37.57 --lon1 126.98 --lat2 35.68 --lon2 139.65
    distancefyi convert 100 km mi
"""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="distancefyi",
    help="Distance calculations between coordinates.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def calc(
    lat1: float = typer.Option(..., help="Latitude of point 1"),
    lon1: float = typer.Option(..., help="Longitude of point 1"),
    lat2: float = typer.Option(..., help="Latitude of point 2"),
    lon2: float = typer.Option(..., help="Longitude of point 2"),
    same_continent: bool = typer.Option(True, help="Same continent (enables drive time)"),
) -> None:
    """Calculate distance between two coordinates."""
    from distancefyi import compute_distance, format_distance, format_duration

    result = compute_distance(lat1, lon1, lat2, lon2, same_continent)

    table = Table(title="Distance Result")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Distance", format_distance(result.distance_km))
    table.add_row("Miles", f"{result.distance_miles:,} mi")
    table.add_row("Nautical Miles", f"{result.distance_nm:,} NM")
    table.add_row("Bearing", f"{result.bearing_degrees}\u00b0 {result.compass_direction}")
    table.add_row("Midpoint", f"{result.midpoint_lat}, {result.midpoint_lon}")
    table.add_row("Flight Time", format_duration(result.flight_time_minutes))
    if result.drive_time_minutes:
        table.add_row("Drive Time", format_duration(result.drive_time_minutes))
    if result.walk_time_minutes:
        table.add_row("Walk Time", format_duration(result.walk_time_minutes))

    console.print(table)


@app.command("bearing")
def bearing_cmd(
    lat1: float = typer.Option(..., help="Latitude of origin"),
    lon1: float = typer.Option(..., help="Longitude of origin"),
    lat2: float = typer.Option(..., help="Latitude of destination"),
    lon2: float = typer.Option(..., help="Longitude of destination"),
) -> None:
    """Calculate bearing between two coordinates."""
    from distancefyi import bearing, compass_direction, compass_direction_full

    brng = bearing(lat1, lon1, lat2, lon2)
    console.print(f"[cyan]Bearing:[/] {brng:.1f}\u00b0")
    console.print(f"[cyan]Direction:[/] {compass_direction(brng)} ({compass_direction_full(brng)})")


@app.command("midpoint")
def midpoint_cmd(
    lat1: float = typer.Option(..., help="Latitude of point 1"),
    lon1: float = typer.Option(..., help="Longitude of point 1"),
    lat2: float = typer.Option(..., help="Latitude of point 2"),
    lon2: float = typer.Option(..., help="Longitude of point 2"),
) -> None:
    """Calculate geographic midpoint between two coordinates."""
    from distancefyi import midpoint

    mid_lat, mid_lon = midpoint(lat1, lon1, lat2, lon2)
    console.print(f"[cyan]Midpoint:[/] {mid_lat}, {mid_lon}")


@app.command()
def antipode(
    lat: float = typer.Option(..., help="Latitude"),
    lon: float = typer.Option(..., help="Longitude"),
) -> None:
    """Find the antipodal point (opposite side of Earth)."""
    from distancefyi import antipodal_point

    anti_lat, anti_lon = antipodal_point(lat, lon)
    console.print(f"[cyan]Antipodal point:[/] {anti_lat}, {anti_lon}")


@app.command()
def convert(
    value: float = typer.Argument(help="Value to convert"),
    from_unit: str = typer.Argument(help="Source unit (km, mi, nm)"),
    to_unit: str = typer.Argument(help="Target unit (km, mi, nm)"),
) -> None:
    """Convert between distance units (km, mi, nm)."""
    from distancefyi import km_to_miles, km_to_nautical_miles, miles_to_km

    km_value: int
    if from_unit in ("km", "kilometers"):
        km_value = round(value)
    elif from_unit in ("mi", "miles"):
        km_value = miles_to_km(round(value))
    elif from_unit in ("nm", "nautical-miles", "nmi"):
        km_value = round(value / KM_TO_NAUTICAL_MILES)
    else:
        console.print(f"[red]Unknown unit: {from_unit}. Use km, mi, or nm.[/]")
        raise typer.Exit(1)

    if to_unit in ("km", "kilometers"):
        result = km_value
        symbol = "km"
    elif to_unit in ("mi", "miles"):
        result = km_to_miles(km_value)
        symbol = "mi"
    elif to_unit in ("nm", "nautical-miles", "nmi"):
        result = km_to_nautical_miles(km_value)
        symbol = "NM"
    else:
        console.print(f"[red]Unknown unit: {to_unit}. Use km, mi, or nm.[/]")
        raise typer.Exit(1)

    console.print(f"[green]{value} {from_unit} = {result:,} {symbol}[/]")


# Import here to avoid circular — only used in convert command
from distancefyi.engine import KM_TO_NAUTICAL_MILES  # noqa: E402
