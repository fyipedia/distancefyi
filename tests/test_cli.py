"""Tests for the distancefyi CLI."""

from typer.testing import CliRunner

from distancefyi.cli import app

runner = CliRunner()


def test_calc_command() -> None:
    result = runner.invoke(
        app,
        [
            "calc",
            "--lat1",
            "37.5665",
            "--lon1",
            "126.978",
            "--lat2",
            "35.6762",
            "--lon2",
            "139.6503",
        ],
    )
    assert result.exit_code == 0
    assert "Distance" in result.output


def test_bearing_command() -> None:
    result = runner.invoke(
        app,
        ["bearing", "--lat1", "0", "--lon1", "0", "--lat2", "0", "--lon2", "10"],
    )
    assert result.exit_code == 0
    assert "Bearing" in result.output


def test_midpoint_command() -> None:
    result = runner.invoke(
        app,
        ["midpoint", "--lat1", "0", "--lon1", "0", "--lat2", "0", "--lon2", "10"],
    )
    assert result.exit_code == 0
    assert "Midpoint" in result.output


def test_antipode_command() -> None:
    result = runner.invoke(app, ["antipode", "--lat", "37.5665", "--lon", "126.978"])
    assert result.exit_code == 0
    assert "Antipodal" in result.output


def test_convert_km_to_mi() -> None:
    result = runner.invoke(app, ["convert", "100", "km", "mi"])
    assert result.exit_code == 0
    assert "62" in result.output
