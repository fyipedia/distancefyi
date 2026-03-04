"""Distance computation engine — pure Python, zero dependencies, <1ms.

Provides Haversine great-circle distance, bearing, midpoint, travel time
estimates, and unit conversions. All functions are stateless and thread-safe.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# Earth radius in km (WGS84 mean radius)
EARTH_RADIUS_KM = 6371.0088

# Unit conversion factors
KM_TO_MILES = 0.621371
KM_TO_NAUTICAL_MILES = 0.539957


@dataclass(frozen=True)
class DistanceResult:
    """Complete distance calculation result."""

    distance_km: int
    distance_miles: int
    distance_nm: int
    bearing_degrees: float
    compass_direction: str
    midpoint_lat: float
    midpoint_lon: float
    flight_time_minutes: int
    drive_time_minutes: int
    walk_time_minutes: int


# ── Core Distance ──────────────────────────────────────────────────


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """Great-circle distance using Haversine formula.

    Args:
        lat1: Latitude of point 1 in decimal degrees.
        lon1: Longitude of point 1 in decimal degrees.
        lat2: Latitude of point 2 in decimal degrees.
        lon2: Longitude of point 2 in decimal degrees.

    Returns:
        Distance in kilometers (rounded to integer).
    """
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(EARTH_RADIUS_KM * c)


# ── Bearing & Direction ────────────────────────────────────────────


def bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Initial bearing from point 1 to point 2.

    Args:
        lat1: Latitude of origin in decimal degrees.
        lon1: Longitude of origin in decimal degrees.
        lat2: Latitude of destination in decimal degrees.
        lon2: Longitude of destination in decimal degrees.

    Returns:
        Bearing in degrees (0-360), where 0=North, 90=East.
    """
    lat1_r, lat2_r = math.radians(lat1), math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    x = math.sin(dlon) * math.cos(lat2_r)
    y = math.cos(lat1_r) * math.sin(lat2_r) - math.sin(lat1_r) * math.cos(lat2_r) * math.cos(dlon)
    brng = math.degrees(math.atan2(x, y))
    return (brng + 360) % 360


_COMPASS_POINTS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]

_COMPASS_FULL: dict[str, str] = {
    "N": "north",
    "NNE": "north-northeast",
    "NE": "northeast",
    "ENE": "east-northeast",
    "E": "east",
    "ESE": "east-southeast",
    "SE": "southeast",
    "SSE": "south-southeast",
    "S": "south",
    "SSW": "south-southwest",
    "SW": "southwest",
    "WSW": "west-southwest",
    "W": "west",
    "WNW": "west-northwest",
    "NW": "northwest",
    "NNW": "north-northwest",
}


def compass_direction(bearing_deg: float) -> str:
    """Convert bearing to 16-point compass direction abbreviation.

    Args:
        bearing_deg: Bearing in degrees (0-360).

    Returns:
        Compass abbreviation (e.g., "NNE", "SW").
    """
    idx = round(bearing_deg / 22.5) % 16
    return _COMPASS_POINTS[idx]


def compass_direction_full(bearing_deg: float) -> str:
    """Convert bearing to full compass direction name.

    Args:
        bearing_deg: Bearing in degrees (0-360).

    Returns:
        Full direction name (e.g., "north-northeast", "southwest").
    """
    return _COMPASS_FULL.get(compass_direction(bearing_deg), "")


# ── Midpoint & Great Circle ────────────────────────────────────────


def midpoint(lat1: float, lon1: float, lat2: float, lon2: float) -> tuple[float, float]:
    """Geographic midpoint between two coordinates.

    Args:
        lat1: Latitude of point 1 in decimal degrees.
        lon1: Longitude of point 1 in decimal degrees.
        lat2: Latitude of point 2 in decimal degrees.
        lon2: Longitude of point 2 in decimal degrees.

    Returns:
        Tuple of (latitude, longitude) of the midpoint.
    """
    lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
    lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)
    bx = math.cos(lat2_r) * math.cos(lon2_r - lon1_r)
    by = math.cos(lat2_r) * math.sin(lon2_r - lon1_r)
    lat_m = math.atan2(
        math.sin(lat1_r) + math.sin(lat2_r),
        math.sqrt((math.cos(lat1_r) + bx) ** 2 + by**2),
    )
    lon_m = lon1_r + math.atan2(by, math.cos(lat1_r) + bx)
    return round(math.degrees(lat_m), 5), round(math.degrees(lon_m), 5)


def great_circle_points(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    num_points: int = 50,
) -> list[tuple[float, float]]:
    """Generate points along the great circle arc.

    Args:
        lat1: Latitude of point 1.
        lon1: Longitude of point 1.
        lat2: Latitude of point 2.
        lon2: Longitude of point 2.
        num_points: Number of intermediate points.

    Returns:
        List of (lat, lon) tuples along the arc.
    """
    lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
    lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)
    d = 2 * math.asin(
        math.sqrt(
            math.sin((lat2_r - lat1_r) / 2) ** 2
            + math.cos(lat1_r) * math.cos(lat2_r) * math.sin((lon2_r - lon1_r) / 2) ** 2
        )
    )
    if d < 1e-10:
        return [(lat1, lon1), (lat2, lon2)]
    points: list[tuple[float, float]] = []
    for i in range(num_points + 1):
        f = i / num_points
        a = math.sin((1 - f) * d) / math.sin(d)
        b = math.sin(f * d) / math.sin(d)
        x = a * math.cos(lat1_r) * math.cos(lon1_r) + b * math.cos(lat2_r) * math.cos(lon2_r)
        y = a * math.cos(lat1_r) * math.sin(lon1_r) + b * math.cos(lat2_r) * math.sin(lon2_r)
        z = a * math.sin(lat1_r) + b * math.sin(lat2_r)
        lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
        lon = math.degrees(math.atan2(y, x))
        points.append((round(lat, 5), round(lon, 5)))
    return points


def antipodal_point(lat: float, lon: float) -> tuple[float, float]:
    """Point on the exact opposite side of Earth.

    Args:
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.

    Returns:
        Tuple of (latitude, longitude) of the antipodal point.
    """
    anti_lon = lon + 180 if lon <= 0 else lon - 180
    return -lat, anti_lon


# ── Travel Time Estimates ──────────────────────────────────────────


def estimate_flight_time(distance_km: int) -> int:
    """Estimated flight time in minutes.

    Uses variable speed by distance band plus 30-minute overhead
    for takeoff/landing.

    Args:
        distance_km: Distance in kilometers.

    Returns:
        Estimated flight time in minutes.
    """
    if distance_km <= 0:
        return 0
    if distance_km < 500:
        speed = 600
    elif distance_km < 1500:
        speed = 750
    else:
        speed = 850
    return round(distance_km / speed * 60) + 30


def estimate_drive_time(distance_km: int, same_continent: bool = True) -> int:
    """Estimated driving time in minutes.

    Uses a 1.3x road distance factor and variable speed by distance.
    Returns 0 for cross-ocean pairs.

    Args:
        distance_km: Straight-line distance in kilometers.
        same_continent: Whether both points are on the same continent.

    Returns:
        Estimated driving time in minutes, or 0 if not drivable.
    """
    if not same_continent or distance_km <= 0:
        return 0
    road_distance = int(distance_km * 1.3)
    if road_distance < 50:
        speed = 40
    elif road_distance < 200:
        speed = 70
    elif road_distance < 1000:
        speed = 90
    else:
        speed = 100
    return round(road_distance / speed * 60)


def estimate_walk_time(distance_km: int) -> int:
    """Estimated walking time in minutes at 5 km/h.

    Returns 0 for distances over 100km.

    Args:
        distance_km: Distance in kilometers.

    Returns:
        Estimated walking time in minutes.
    """
    if distance_km > 100 or distance_km <= 0:
        return 0
    return round(distance_km / 5 * 60)


# ── Unit Conversion ────────────────────────────────────────────────


def km_to_miles(km: int) -> int:
    """Convert kilometers to miles (rounded)."""
    return round(km * KM_TO_MILES)


def km_to_nautical_miles(km: int) -> int:
    """Convert kilometers to nautical miles (rounded)."""
    return round(km * KM_TO_NAUTICAL_MILES)


def miles_to_km(miles: int) -> int:
    """Convert miles to kilometers (rounded)."""
    return round(miles / KM_TO_MILES)


# ── Formatting ─────────────────────────────────────────────────────


def format_distance(km: int) -> str:
    """Format distance with thousands separator (e.g., '12,345 km')."""
    return f"{km:,} km"


def format_duration(minutes: int) -> str:
    """Format duration as human-readable string.

    Examples: '45m', '2h 30m', '3d 5h'.
    """
    if minutes <= 0:
        return "\u2014"
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if hours < 24:
        return f"{hours}h {mins:02d}m" if mins else f"{hours}h"
    days = hours // 24
    remaining_hours = hours % 24
    return f"{days}d {remaining_hours}h"


# ── Full Computation ───────────────────────────────────────────────


def compute_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    same_continent: bool = True,
) -> DistanceResult:
    """Compute complete distance information between two coordinates.

    Single call that returns all distance, bearing, midpoint, and
    travel time data needed for display.

    Args:
        lat1: Latitude of point 1.
        lon1: Longitude of point 1.
        lat2: Latitude of point 2.
        lon2: Longitude of point 2.
        same_continent: Whether both points are on the same continent.

    Returns:
        DistanceResult with all computed fields.
    """
    dist_km = haversine_distance(lat1, lon1, lat2, lon2)
    brng = bearing(lat1, lon1, lat2, lon2)
    mid_lat, mid_lon = midpoint(lat1, lon1, lat2, lon2)
    return DistanceResult(
        distance_km=dist_km,
        distance_miles=km_to_miles(dist_km),
        distance_nm=km_to_nautical_miles(dist_km),
        bearing_degrees=round(brng, 1),
        compass_direction=compass_direction(brng),
        midpoint_lat=mid_lat,
        midpoint_lon=mid_lon,
        flight_time_minutes=estimate_flight_time(dist_km),
        drive_time_minutes=estimate_drive_time(dist_km, same_continent),
        walk_time_minutes=estimate_walk_time(dist_km),
    )
