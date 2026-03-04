# distancefyi

Pure Python distance engine — Haversine great-circle distance, bearing, midpoint, travel time estimates, and unit conversions. Zero dependencies.

## Install

```bash
pip install distancefyi              # Core (zero deps)
pip install "distancefyi[cli]"       # + CLI (typer, rich)
pip install "distancefyi[mcp]"       # + MCP server
pip install "distancefyi[all]"       # Everything
```

## Quick Start

```python
from distancefyi import haversine_distance, bearing, midpoint, compute_distance

# Seoul → Tokyo
haversine_distance(37.5665, 126.978, 35.6762, 139.6503)  # 1159 km
bearing(37.5665, 126.978, 35.6762, 139.6503)              # 108.6°
midpoint(37.5665, 126.978, 35.6762, 139.6503)             # (36.82..., 133.36...)

# Full computation
result = compute_distance(37.5665, 126.978, 35.6762, 139.6503)
result.distance_km          # 1159
result.distance_miles       # 720
result.compass_direction    # "ESE"
result.flight_time_minutes  # 123
```

## Features

- **Haversine distance** — great-circle distance in km, miles, nautical miles
- **Bearing** — initial bearing with 16-point compass direction
- **Midpoint** — geographic midpoint between two coordinates
- **Great circle arc** — generate points along the shortest path
- **Antipodal point** — opposite side of Earth
- **Travel time estimates** — flight, drive, walk time with realistic models
- **Unit conversion** — km ↔ miles ↔ nautical miles
- **Formatting** — human-readable distance and duration strings

## CLI

```bash
distancefyi calc --lat1 37.5665 --lon1 126.978 --lat2 35.6762 --lon2 139.6503
distancefyi bearing --lat1 37.57 --lon1 126.98 --lat2 35.68 --lon2 139.65
distancefyi midpoint --lat1 37.57 --lon1 126.98 --lat2 35.68 --lon2 139.65
distancefyi convert 100 km mi
```

## MCP Server

Add to your Claude Desktop config:

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

Tools: `calculate_distance`, `get_bearing`, `get_midpoint`, `get_flight_time`, `convert_distance`

## API Client

```python
from distancefyi.api import DistanceFYI

with DistanceFYI() as client:
    result = client.distance("seoul", "tokyo")
```

## License

MIT
