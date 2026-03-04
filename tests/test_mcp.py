"""Tests for the distancefyi MCP server."""

from distancefyi.mcp_server import (
    calculate_distance,
    convert_distance,
    get_bearing,
    get_flight_time,
    get_midpoint,
)


def test_calculate_distance() -> None:
    result = calculate_distance(37.5665, 126.978, 35.6762, 139.6503)
    assert "1,149" in result or "1,150" in result or "1,148" in result
    assert "km" in result
    assert "Bearing" in result


def test_get_bearing() -> None:
    result = get_bearing(0, 0, 0, 10)
    assert "90" in result
    assert "east" in result.lower()


def test_get_midpoint() -> None:
    result = get_midpoint(0, 0, 0, 10)
    assert "Midpoint" in result
    assert "5.0" in result


def test_get_flight_time() -> None:
    result = get_flight_time(1000)
    assert "flight time" in result.lower()
    assert "km" in result


def test_convert_distance_km_to_mi() -> None:
    result = convert_distance(100, "km", "mi")
    assert "62" in result


def test_convert_distance_unknown_unit() -> None:
    result = convert_distance(100, "furlongs", "km")
    assert "Unknown" in result
