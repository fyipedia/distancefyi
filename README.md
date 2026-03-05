# distancefyi

[![PyPI](https://img.shields.io/pypi/v/distancefyi)](https://pypi.org/project/distancefyi/)
[![Python](https://img.shields.io/pypi/pyversions/distancefyi)](https://pypi.org/project/distancefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python distance engine for developers. Compute [Haversine great-circle distances](https://distancefyi.com/tools/distance-calculator/), initial bearings with 16-point compass directions, geographic midpoints, great circle arcs, antipodal points, and realistic travel time estimates -- all with zero dependencies.

> **Explore distances between world cities at [distancefyi.com](https://distancefyi.com/)** -- [distance calculator](https://distancefyi.com/tools/distance-calculator/), city-to-city routes, and travel time estimates.

<p align="center">
  <img src="demo.gif" alt="distancefyi CLI demo" width="800">
</p>

## Install

```bash
pip install distancefyi              # Core engine (zero deps)
pip install "distancefyi[cli]"       # + Command-line interface
pip install "distancefyi[mcp]"       # + MCP server for AI assistants
pip install "distancefyi[api]"       # + HTTP client for distancefyi.com API
pip install "distancefyi[all]"       # Everything
```

## Quick Start

```python
from distancefyi import haversine_distance, bearing, midpoint, compute_distance

# Seoul to Tokyo
haversine_distance(37.5665, 126.978, 35.6762, 139.6503)  # 1159 km
bearing(37.5665, 126.978, 35.6762, 139.6503)              # 108.6 degrees
midpoint(37.5665, 126.978, 35.6762, 139.6503)             # (36.82..., 133.36...)

# Full computation with travel times
result = compute_distance(37.5665, 126.978, 35.6762, 139.6503)
result.distance_km          # 1159
result.distance_miles       # 720
result.compass_direction    # "ESE"
result.flight_time_minutes  # 123
```

## Understanding Distance Calculation

The Haversine formula computes the great-circle distance between two points on a sphere. It uses the Earth's mean radius (R = 6,371 km) as a spherical approximation, which introduces a maximum error of about 0.3% compared to the true ellipsoidal distance. For most applications -- route planning, city-to-city comparisons, flight distance estimation -- this is more than sufficient.

```python
from distancefyi import haversine_distance, km_to_miles, km_to_nautical_miles

# Distance in different units
km = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)  # NYC to London
miles = km_to_miles(km)                # 3,459 miles
nm = km_to_nautical_miles(km)          # 3,005 nautical miles
```

For sub-meter precision (surveying, geodesy), you would need Vincenty's formula on the WGS84 ellipsoid, which accounts for the Earth's equatorial bulge. The Haversine formula treats the Earth as a perfect sphere, so it slightly underestimates distances near the equator and overestimates near the poles.

## Navigation & Bearing

The initial bearing (forward azimuth) is the compass direction you would face when starting a journey along the great-circle route. Unlike a rhumb line (constant compass bearing), a great-circle route's bearing changes continuously along the path -- this is why flight paths on a Mercator map appear curved.

```python
from distancefyi import bearing, compass_direction, great_circle_points, antipodal_point

# Initial bearing from New York to London
b = bearing(40.7128, -74.0060, 51.5074, -0.1278)  # 51.2 degrees
compass_direction(b)                                 # "NE"

# Generate waypoints along the great-circle arc
points = great_circle_points(40.7128, -74.0060, 51.5074, -0.1278, num_points=10)

# Antipodal point (diametrically opposite on Earth)
lat, lon = antipodal_point(40.7128, -74.0060)  # (-40.7128, 105.994)
```

The 16-point compass rose divides 360 degrees into directions: N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW. Each sector spans 22.5 degrees.

## Travel Time Estimates

```python
from distancefyi import estimate_flight_time, estimate_drive_time, estimate_walk_time

km = 1159  # Seoul to Tokyo

# Realistic models with acceleration/deceleration phases
estimate_flight_time(km)   # ~123 minutes (cruising at 850 km/h + taxi/climb/descent)
estimate_drive_time(km)    # ~870 minutes (average 80 km/h with rest stops)
estimate_walk_time(km)     # ~13,908 minutes (5 km/h)
```

## Command-Line Interface

```bash
pip install "distancefyi[cli]"

distancefyi calc --lat1 37.5665 --lon1 126.978 --lat2 35.6762 --lon2 139.6503
distancefyi bearing --lat1 37.57 --lon1 126.98 --lat2 35.68 --lon2 139.65
distancefyi midpoint --lat1 37.57 --lon1 126.98 --lat2 35.68 --lon2 139.65
distancefyi convert 100 km mi
```

## MCP Server (Claude, Cursor, Windsurf)

Add distance tools to any AI assistant that supports [Model Context Protocol](https://modelcontextprotocol.io/).

```bash
pip install "distancefyi[mcp]"
```

Add to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "distancefyi": {
            "command": "python",
            "args": ["-m", "distancefyi.mcp_server"]
        }
    }
}
```

**Available tools**: `calculate_distance`, `get_bearing`, `get_midpoint`, `get_flight_time`, `convert_distance`

## REST API Client

```python
pip install "distancefyi[api]"
```

```python
from distancefyi.api import DistanceFYI

with DistanceFYI() as client:
    result = client.distance("seoul", "tokyo")
```

Full [API documentation](https://distancefyi.com/developers/) at distancefyi.com.

## API Reference

### Core Distance

| Function | Description |
|----------|-------------|
| `haversine_distance(lat1, lon1, lat2, lon2) -> int` | Great-circle distance in km |
| `compute_distance(lat1, lon1, lat2, lon2) -> DistanceResult` | Full computation with all metrics |
| `bearing(lat1, lon1, lat2, lon2) -> float` | Initial bearing in degrees (0-360) |
| `compass_direction(degrees) -> str` | 16-point compass abbreviation (e.g., "NE") |
| `compass_direction_full(degrees) -> str` | Full compass name (e.g., "Northeast") |

### Midpoint & Great Circle

| Function | Description |
|----------|-------------|
| `midpoint(lat1, lon1, lat2, lon2) -> tuple[float, float]` | Geographic midpoint |
| `great_circle_points(lat1, lon1, lat2, lon2, num_points) -> list` | Waypoints along the arc |
| `antipodal_point(lat, lon) -> tuple[float, float]` | Diametrically opposite point |

### Travel Time

| Function | Description |
|----------|-------------|
| `estimate_flight_time(km) -> int` | Flight time in minutes |
| `estimate_drive_time(km) -> int` | Drive time in minutes |
| `estimate_walk_time(km) -> int` | Walk time in minutes |

### Unit Conversion & Formatting

| Function | Description |
|----------|-------------|
| `km_to_miles(km) -> float` | Kilometers to miles |
| `km_to_nautical_miles(km) -> float` | Kilometers to nautical miles |
| `miles_to_km(miles) -> float` | Miles to kilometers |
| `format_distance(km) -> str` | Human-readable distance string |
| `format_duration(minutes) -> str` | Human-readable duration string |

## Features

- **Haversine distance** -- great-circle distance in km, miles, nautical miles
- **Bearing** -- initial bearing with 16-point compass direction
- **Midpoint** -- geographic midpoint between two coordinates
- **Great circle arc** -- generate waypoints along the shortest path
- **Antipodal point** -- diametrically opposite point on Earth
- **Travel time estimates** -- flight, drive, walk time with realistic models
- **Unit conversion** -- km, miles, nautical miles
- **Formatting** -- human-readable distance and duration strings
- **CLI** -- Rich terminal output with distance tables
- **MCP server** -- 5 tools for AI assistants (Claude, Cursor, Windsurf)
- **REST API client** -- httpx-based client for [distancefyi.com API](https://distancefyi.com/developers/)
- **Zero dependencies** -- core engine uses only `math` from stdlib
- **Type-safe** -- full type annotations, `py.typed` marker (PEP 561)

## FYIPedia Developer Tools

Part of the [FYIPedia](https://github.com/fyipedia) open-source developer tools ecosystem:

| Package | Description |
|---------|-------------|
| [colorfyi](https://pypi.org/project/colorfyi/) | Color conversion, [WCAG contrast](https://colorfyi.com/tools/contrast-checker/), harmonies, shades -- [colorfyi.com](https://colorfyi.com/) |
| [emojifyi](https://pypi.org/project/emojifyi/) | Emoji lookup, search, encoding -- [emojifyi.com](https://emojifyi.com/) |
| [symbolfyi](https://pypi.org/project/symbolfyi/) | Symbol encoding, Unicode properties -- [symbolfyi.com](https://symbolfyi.com/) |
| [unicodefyi](https://pypi.org/project/unicodefyi/) | Unicode character info, 17 encodings -- [unicodefyi.com](https://unicodefyi.com/) |
| [fontfyi](https://pypi.org/project/fontfyi/) | Google Fonts metadata, CSS, pairings -- [fontfyi.com](https://fontfyi.com/) |
| **[distancefyi](https://pypi.org/project/distancefyi/)** | **Haversine distance, bearing, travel times -- [distancefyi.com](https://distancefyi.com/)** |
| [timefyi](https://pypi.org/project/timefyi/) | Timezone ops, time differences, business hours -- [timefyi.com](https://timefyi.com/) |
| [namefyi](https://pypi.org/project/namefyi/) | Korean romanization, Five Elements -- [namefyi.com](https://namefyi.com/) |
| [unitfyi](https://pypi.org/project/unitfyi/) | Unit conversion, 200 units, 20 categories -- [unitfyi.com](https://unitfyi.com/) |
| [holidayfyi](https://pypi.org/project/holidayfyi/) | Holiday dates, Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |

## Links

- [Distance Calculator](https://distancefyi.com/tools/distance-calculator/) -- Calculate distances between cities
- [REST API Documentation](https://distancefyi.com/developers/) -- Free API
- [npm Package](https://www.npmjs.com/package/distancefyi) -- TypeScript version
- [Source Code](https://github.com/fyipedia/distancefyi) -- MIT licensed

## License

MIT
