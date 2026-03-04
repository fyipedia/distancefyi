"""distancefyi — Pure Python distance engine for developers.

Compute great-circle distances, bearings, midpoints, and travel time
estimates using the Haversine formula. Zero dependencies.

Basic usage::

    >>> from distancefyi import haversine_distance, bearing, compute_distance
    >>> haversine_distance(37.5665, 126.978, 35.6762, 139.6503)
    1159
    >>> bearing(37.5665, 126.978, 35.6762, 139.6503)
    108.6
    >>> result = compute_distance(37.5665, 126.978, 35.6762, 139.6503)
    >>> result.distance_km
    1159
"""

from distancefyi.engine import (
    EARTH_RADIUS_KM,
    KM_TO_MILES,
    KM_TO_NAUTICAL_MILES,
    DistanceResult,
    antipodal_point,
    bearing,
    compass_direction,
    compass_direction_full,
    compute_distance,
    estimate_drive_time,
    estimate_flight_time,
    estimate_walk_time,
    format_distance,
    format_duration,
    great_circle_points,
    haversine_distance,
    km_to_miles,
    km_to_nautical_miles,
    midpoint,
    miles_to_km,
)

__version__ = "0.1.0"

__all__ = [
    # Data types
    "DistanceResult",
    # Constants
    "EARTH_RADIUS_KM",
    "KM_TO_MILES",
    "KM_TO_NAUTICAL_MILES",
    # Core distance
    "haversine_distance",
    # Bearing & direction
    "bearing",
    "compass_direction",
    "compass_direction_full",
    # Midpoint & great circle
    "midpoint",
    "great_circle_points",
    "antipodal_point",
    # Travel time estimates
    "estimate_flight_time",
    "estimate_drive_time",
    "estimate_walk_time",
    # Unit conversion
    "km_to_miles",
    "km_to_nautical_miles",
    "miles_to_km",
    # Formatting
    "format_distance",
    "format_duration",
    # Full computation
    "compute_distance",
]
