"""Tests for the distancefyi engine."""

from distancefyi import (
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

# ── Seoul → Tokyo (well-known reference pair) ──


def test_haversine_seoul_tokyo() -> None:
    """Seoul to Tokyo is approximately 1,149 km."""
    dist = haversine_distance(37.5665, 126.978, 35.6762, 139.6503)
    assert 1140 <= dist <= 1160


def test_haversine_same_point() -> None:
    """Distance from a point to itself is 0."""
    assert haversine_distance(0, 0, 0, 0) == 0


def test_haversine_antipodal() -> None:
    """Distance to antipodal point is roughly half Earth's circumference."""
    dist = haversine_distance(0, 0, 0, 180)
    assert 20000 <= dist <= 20100  # ~20,015 km


# ── Bearing ──


def test_bearing_east() -> None:
    """Bearing from equator going east should be ~90°."""
    b = bearing(0, 0, 0, 10)
    assert 89 <= b <= 91


def test_bearing_north() -> None:
    """Bearing going due north should be ~0°."""
    b = bearing(0, 0, 10, 0)
    assert b < 1 or b > 359


def test_bearing_south() -> None:
    """Bearing going due south should be ~180°."""
    b = bearing(10, 0, 0, 0)
    assert 179 <= b <= 181


# ── Compass Direction ──


def test_compass_direction_north() -> None:
    assert compass_direction(0) == "N"
    assert compass_direction(360) == "N"


def test_compass_direction_east() -> None:
    assert compass_direction(90) == "E"


def test_compass_direction_south() -> None:
    assert compass_direction(180) == "S"


def test_compass_direction_full() -> None:
    assert compass_direction_full(45) == "northeast"
    assert compass_direction_full(225) == "southwest"


# ── Midpoint ──


def test_midpoint_equator() -> None:
    """Midpoint of two equatorial points."""
    lat, lon = midpoint(0, 0, 0, 10)
    assert abs(lat) < 0.01
    assert 4.9 <= lon <= 5.1


def test_midpoint_symmetric() -> None:
    """Midpoint should be symmetric."""
    m1 = midpoint(10, 20, 30, 40)
    m2 = midpoint(30, 40, 10, 20)
    assert abs(m1[0] - m2[0]) < 0.001
    assert abs(m1[1] - m2[1]) < 0.001


# ── Great Circle Points ──


def test_great_circle_points_count() -> None:
    points = great_circle_points(0, 0, 0, 10, num_points=10)
    assert len(points) == 11  # 10 intervals = 11 points


def test_great_circle_same_point() -> None:
    points = great_circle_points(0, 0, 0, 0)
    assert len(points) == 2


# ── Antipodal ──


def test_antipodal_origin() -> None:
    lat, lon = antipodal_point(0, 0)
    assert lat == 0
    assert lon == 180


def test_antipodal_seoul() -> None:
    lat, lon = antipodal_point(37.5665, 126.978)
    assert abs(lat - (-37.5665)) < 0.001
    assert abs(lon - (-53.022)) < 0.001


# ── Travel Time Estimates ──


def test_flight_time_zero() -> None:
    assert estimate_flight_time(0) == 0


def test_flight_time_short() -> None:
    """Short flight: 300km at 600km/h + 30min overhead."""
    minutes = estimate_flight_time(300)
    assert minutes == round(300 / 600 * 60) + 30


def test_flight_time_long() -> None:
    """Long flight: 5000km at 850km/h + 30min overhead."""
    minutes = estimate_flight_time(5000)
    assert minutes == round(5000 / 850 * 60) + 30


def test_drive_time_cross_ocean() -> None:
    assert estimate_drive_time(1000, same_continent=False) == 0


def test_drive_time_normal() -> None:
    minutes = estimate_drive_time(100)
    assert minutes > 0


def test_walk_time_short() -> None:
    assert estimate_walk_time(10) == 120  # 10km at 5km/h = 2h


def test_walk_time_too_far() -> None:
    assert estimate_walk_time(200) == 0


# ── Unit Conversion ──


def test_km_to_miles() -> None:
    assert km_to_miles(100) == 62


def test_km_to_nautical_miles() -> None:
    assert km_to_nautical_miles(100) == 54


def test_miles_to_km() -> None:
    assert miles_to_km(62) == 100


# ── Formatting ──


def test_format_distance() -> None:
    assert format_distance(12345) == "12,345 km"


def test_format_duration_minutes() -> None:
    assert format_duration(45) == "45m"


def test_format_duration_hours() -> None:
    assert format_duration(150) == "2h 30m"


def test_format_duration_days() -> None:
    assert format_duration(1500) == "1d 1h"


def test_format_duration_zero() -> None:
    assert format_duration(0) == "\u2014"


# ── Full Computation ──


def test_compute_distance() -> None:
    result = compute_distance(37.5665, 126.978, 35.6762, 139.6503)
    assert isinstance(result, DistanceResult)
    assert 1140 <= result.distance_km <= 1160
    assert result.distance_miles > 0
    assert result.distance_nm > 0
    assert 0 <= result.bearing_degrees <= 360
    assert result.compass_direction in ("E", "ESE", "ENE")
    assert result.flight_time_minutes > 0
