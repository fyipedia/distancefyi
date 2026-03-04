"""MCP server for distancefyi — distance tools for AI assistants.

Requires: pip install distancefyi[mcp]

Configure in claude_desktop_config.json::

    {
        "mcpServers": {
            "distancefyi": {
                "command": "python",
                "args": ["-m", "distancefyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("distancefyi")


@mcp.tool()
def calculate_distance(
    lat1: float, lon1: float, lat2: float, lon2: float, same_continent: bool = True
) -> str:
    """Calculate great-circle distance between two coordinates.

    Returns distance in km/miles/nautical miles, bearing, midpoint,
    and estimated travel times (flight, drive, walk).

    Args:
        lat1: Latitude of point 1 (e.g., 37.5665 for Seoul).
        lon1: Longitude of point 1 (e.g., 126.978 for Seoul).
        lat2: Latitude of point 2 (e.g., 35.6762 for Tokyo).
        lon2: Longitude of point 2 (e.g., 139.6503 for Tokyo).
        same_continent: Set False for cross-ocean pairs (disables drive time).
    """
    from distancefyi import compute_distance, format_distance, format_duration

    r = compute_distance(lat1, lon1, lat2, lon2, same_continent)

    lines = [
        f"## Distance: {format_distance(r.distance_km)}",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Distance | {r.distance_km:,} km ({r.distance_miles:,} mi, {r.distance_nm:,} NM) |",
        f"| Bearing | {r.bearing_degrees}\u00b0 {r.compass_direction} |",
        f"| Midpoint | {r.midpoint_lat}, {r.midpoint_lon} |",
        f"| Flight Time | {format_duration(r.flight_time_minutes)} |",
    ]
    if r.drive_time_minutes:
        lines.append(f"| Drive Time | {format_duration(r.drive_time_minutes)} |")
    if r.walk_time_minutes:
        lines.append(f"| Walk Time | {format_duration(r.walk_time_minutes)} |")

    return "\n".join(lines)


@mcp.tool()
def get_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
    """Get the initial bearing and compass direction between two points.

    Args:
        lat1: Latitude of origin.
        lon1: Longitude of origin.
        lat2: Latitude of destination.
        lon2: Longitude of destination.
    """
    from distancefyi import bearing, compass_direction, compass_direction_full

    brng = bearing(lat1, lon1, lat2, lon2)
    return f"Bearing: {brng:.1f}\u00b0 {compass_direction(brng)} ({compass_direction_full(brng)})"


@mcp.tool()
def get_midpoint(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
    """Calculate the geographic midpoint between two coordinates.

    Args:
        lat1: Latitude of point 1.
        lon1: Longitude of point 1.
        lat2: Latitude of point 2.
        lon2: Longitude of point 2.
    """
    from distancefyi import midpoint

    mid_lat, mid_lon = midpoint(lat1, lon1, lat2, lon2)
    return f"Midpoint: {mid_lat}, {mid_lon}"


@mcp.tool()
def get_flight_time(distance_km: int) -> str:
    """Estimate flight time for a given distance.

    Uses variable speed by distance band (600-850 km/h) plus
    30-minute overhead for takeoff/landing.

    Args:
        distance_km: Distance in kilometers.
    """
    from distancefyi import estimate_flight_time, format_duration

    minutes = estimate_flight_time(distance_km)
    return f"Estimated flight time for {distance_km:,} km: {format_duration(minutes)}"


@mcp.tool()
def convert_distance(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between distance units (km, miles, nautical miles).

    Args:
        value: Numeric value to convert.
        from_unit: Source unit ('km', 'mi', or 'nm').
        to_unit: Target unit ('km', 'mi', or 'nm').
    """
    from distancefyi import km_to_miles, km_to_nautical_miles, miles_to_km
    from distancefyi.engine import KM_TO_NAUTICAL_MILES

    km_value: int
    if from_unit in ("km", "kilometers"):
        km_value = round(value)
    elif from_unit in ("mi", "miles"):
        km_value = miles_to_km(round(value))
    elif from_unit in ("nm", "nautical-miles", "nmi"):
        km_value = round(value / KM_TO_NAUTICAL_MILES)
    else:
        return f"Unknown unit: {from_unit}. Use km, mi, or nm."

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
        return f"Unknown unit: {to_unit}. Use km, mi, or nm."

    return f"{value} {from_unit} = {result:,} {symbol}"


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
