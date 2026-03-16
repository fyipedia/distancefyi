# distancefyi

[![PyPI version](https://agentgif.com/badge/pypi/distancefyi/version.svg)](https://pypi.org/project/distancefyi/)
[![Python](https://img.shields.io/pypi/pyversions/distancefyi)](https://pypi.org/project/distancefyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure Python distance engine for developers. Compute [Haversine great-circle distances](https://distancefyi.com/tools/distance-calculator/), initial bearings with 16-point compass directions, geographic midpoints, great circle arcs, antipodal points, and realistic travel time estimates -- all with zero dependencies.

> **Explore distances between world cities at [distancefyi.com](https://distancefyi.com/)** -- [distance calculator](https://distancefyi.com/tools/distance-calculator/), city-to-city routes, and travel time estimates.

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/distancefyi/main/demo.gif" alt="distancefyi CLI demo" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [Understanding Distance Calculation](#understanding-distance-calculation)
- [Navigation & Bearing](#navigation--bearing)
- [Travel Time Estimates](#travel-time-estimates)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
  - [Core Distance](#core-distance)
  - [Midpoint & Great Circle](#midpoint--great-circle)
  - [Travel Time](#travel-time)
  - [Unit Conversion & Formatting](#unit-conversion--formatting)
- [Features](#features)
- [Learn More About Distance](#learn-more-about-distance)
- [Utility FYI Family](#utility-fyi-family)
- [License](#license)

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

| Distance Unit | Abbreviation | Relative to 1 km | Common Use |
|---------------|-------------|-------------------|------------|
| Kilometer | km | 1.0 | Worldwide standard |
| Mile (statute) | mi | 0.6214 | US, UK road distances |
| Nautical mile | nmi | 0.5400 | Aviation, maritime navigation |
| Meter | m | 1,000 | Walking, urban distances |
| Foot | ft | 3,280.84 | US/UK altitude, short distances |

```python
from distancefyi import haversine_distance, km_to_miles, km_to_nautical_miles

# Great-circle distance between New York and London
km = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)  # NYC to London
miles = km_to_miles(km)                # 3,459 statute miles
nm = km_to_nautical_miles(km)          # 3,005 nautical miles (used in aviation)
```

For sub-meter precision (surveying, geodesy), you would need Vincenty's formula on the WGS84 ellipsoid, which accounts for the Earth's equatorial bulge. The Haversine formula treats the Earth as a perfect sphere, so it slightly underestimates distances near the equator and overestimates near the poles.

Learn more: [Distance Calculator](https://distancefyi.com/tools/distance-calculator/) · [Browse Cities](https://distancefyi.com/city/) · [Browse Countries](https://distancefyi.com/country/)

## Navigation & Bearing

The initial bearing (forward azimuth) is the compass direction you would face when starting a journey along the great-circle route. Unlike a rhumb line (constant compass bearing), a great-circle route's bearing changes continuously along the path -- this is why flight paths on a Mercator map appear curved.

| Compass Direction | Abbreviation | Degree Range |
|-------------------|-------------|-------------|
| North | N | 348.75 -- 11.25 |
| North-Northeast | NNE | 11.25 -- 33.75 |
| Northeast | NE | 33.75 -- 56.25 |
| East-Northeast | ENE | 56.25 -- 78.75 |
| East | E | 78.75 -- 101.25 |
| East-Southeast | ESE | 101.25 -- 123.75 |
| Southeast | SE | 123.75 -- 146.25 |
| South-Southeast | SSE | 146.25 -- 168.75 |
| South | S | 168.75 -- 191.25 |
| South-Southwest | SSW | 191.25 -- 213.75 |
| Southwest | SW | 213.75 -- 236.25 |
| West-Southwest | WSW | 236.25 -- 258.75 |
| West | W | 258.75 -- 281.25 |
| West-Northwest | WNW | 281.25 -- 303.75 |
| Northwest | NW | 303.75 -- 326.25 |
| North-Northwest | NNW | 326.25 -- 348.75 |

```python
from distancefyi import bearing, compass_direction, great_circle_points, antipodal_point

# Initial bearing from New York to London (great-circle route)
b = bearing(40.7128, -74.0060, 51.5074, -0.1278)  # 51.2 degrees
compass_direction(b)                                 # "NE" (Northeast)

# Generate waypoints along the great-circle arc for route visualization
points = great_circle_points(40.7128, -74.0060, 51.5074, -0.1278, num_points=10)

# Antipodal point -- diametrically opposite location on Earth
lat, lon = antipodal_point(40.7128, -74.0060)  # (-40.7128, 105.994)
```

The 16-point compass rose divides 360 degrees into directions: N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW. Each sector spans 22.5 degrees.

Learn more: [Distance Calculator](https://distancefyi.com/tools/distance-calculator/) · [City Routes](https://distancefyi.com/city/)

## Travel Time Estimates

Travel time estimates use realistic speed models that account for acceleration, deceleration, rest stops, and real-world conditions rather than simple distance-over-speed division.

| Travel Mode | Average Speed | Includes | Best For |
|-------------|--------------|----------|----------|
| Flight | 850 km/h cruise | Taxi, climb, descent, approach | Distances > 300 km |
| Driving | 80 km/h average | Rest stops, speed variation | 50 -- 2,000 km |
| Walking | 5 km/h | Steady pace, no stops | < 30 km |

| Distance Band | Flight Time | Drive Time | Walk Time |
|---------------|------------|------------|-----------|
| 500 km | ~70 min | ~6 h | ~4 days |
| 1,000 km | ~110 min | ~12.5 h | ~8 days |
| 5,000 km | ~390 min | ~62.5 h | ~42 days |
| 10,000 km | ~740 min | ~125 h | ~83 days |

```python
from distancefyi import estimate_flight_time, estimate_drive_time, estimate_walk_time

# Seoul to Tokyo distance in kilometers
km = 1159

# Realistic flight time with taxi, climb, cruise, and descent phases
estimate_flight_time(km)   # ~123 minutes (cruising at 850 km/h)

# Driving time with average highway speed and rest stops
estimate_drive_time(km)    # ~870 minutes (average 80 km/h)

# Walking time at a steady 5 km/h pace
estimate_walk_time(km)     # ~13,908 minutes
```

Learn more: [Flight Time Calculator](https://distancefyi.com/tools/flight-time/) · [City Distance Routes](https://distancefyi.com/city/) · [Country Distances](https://distancefyi.com/country/)

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

## Learn More About Distance

- **Tools**: [Distance Calculator](https://distancefyi.com/) · [Flight Time Calculator](https://distancefyi.com/tools/flight-time/)
- **Browse**: [Cities](https://distancefyi.com/city/) · [Countries](https://distancefyi.com/country/)
- **Guides**: [Glossary](https://distancefyi.com/glossary/) · [Blog](https://distancefyi.com/blog/)
- **API**: [REST API Docs](https://distancefyi.com/developers/) · [OpenAPI Spec](https://distancefyi.com/api/openapi.json)

## Utility FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — everyday developer reference and conversion tools.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| unitfyi | [PyPI](https://pypi.org/project/unitfyi/) | [npm](https://www.npmjs.com/package/unitfyi) | Unit conversion, 220 units -- [unitfyi.com](https://unitfyi.com/) |
| timefyi | [PyPI](https://pypi.org/project/timefyi/) | [npm](https://www.npmjs.com/package/timefyi) | Timezone ops & business hours -- [timefyi.com](https://timefyi.com/) |
| holidayfyi | [PyPI](https://pypi.org/project/holidayfyi/) | [npm](https://www.npmjs.com/package/holidayfyi) | Holiday dates & Easter calculation -- [holidayfyi.com](https://holidayfyi.com/) |
| namefyi | [PyPI](https://pypi.org/project/namefyi/) | [npm](https://www.npmjs.com/package/namefyi) | Korean romanization & Five Elements -- [namefyi.com](https://namefyi.com/) |
| **distancefyi** | [PyPI](https://pypi.org/project/distancefyi/) | [npm](https://www.npmjs.com/package/distancefyi) | Haversine distance & travel times -- [distancefyi.com](https://distancefyi.com/) |

## License

MIT
