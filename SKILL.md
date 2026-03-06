---
name: distance-tools
description: Compute great-circle distances using the Haversine formula, initial bearings, midpoints, and travel time estimates for flight, driving, and walking. Use when calculating distance between coordinates, navigation, or travel planning.
license: MIT
metadata:
  author: fyipedia
  version: "0.1.1"
  homepage: "https://distancefyi.com/"
---

# DistanceFYI -- Distance Tools for AI Agents

Pure Python distance engine. Compute Haversine great-circle distances, bearings with 16-point compass directions, geographic midpoints, great circle arcs, antipodal points, and travel time estimates -- all with zero dependencies.

**Install**: `pip install distancefyi` -- **Web**: [distancefyi.com](https://distancefyi.com/) -- **API**: [REST API](https://distancefyi.com/developers/) -- **npm**: `npm install distancefyi`

## When to Use

- User asks for the distance between two locations (given coordinates)
- User needs a bearing or compass direction between two points
- User wants to estimate flight, driving, or walking time
- User needs the geographic midpoint between two coordinates
- User asks to convert between km, miles, and nautical miles

## Tools

### `haversine_distance(lat1, lon1, lat2, lon2) -> int`

Great-circle distance between two points in kilometers (rounded).

```python
from distancefyi import haversine_distance

haversine_distance(37.5665, 126.978, 35.6762, 139.6503)  # 1159 (Seoul to Tokyo)
haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)  # 5570 (NYC to London)
```

### `compute_distance(lat1, lon1, lat2, lon2, same_continent) -> DistanceResult`

Full computation returning distance, bearing, midpoint, and travel times in one call.

```python
from distancefyi import compute_distance

result = compute_distance(37.5665, 126.978, 35.6762, 139.6503)
result.distance_km          # 1159
result.distance_miles       # 720
result.distance_nm          # 626
result.bearing_degrees      # 108.6
result.compass_direction    # 'ESE'
result.midpoint_lat         # 36.82...
result.midpoint_lon         # 133.36...
result.flight_time_minutes  # 123
result.drive_time_minutes   # 870 (or 0 if cross-ocean)
result.walk_time_minutes    # 0 (> 100km)
```

### `bearing(lat1, lon1, lat2, lon2) -> float`

Initial bearing from point 1 to point 2 in degrees (0-360, where 0=North, 90=East).

```python
from distancefyi import bearing

bearing(37.5665, 126.978, 35.6762, 139.6503)  # 108.6 (ESE)
bearing(40.7128, -74.0060, 51.5074, -0.1278)  # 51.2 (NE)
```

### `compass_direction(bearing_deg) -> str`

Convert bearing to 16-point compass abbreviation.

```python
from distancefyi import compass_direction, compass_direction_full

compass_direction(108.6)       # 'ESE'
compass_direction_full(108.6)  # 'east-southeast'
compass_direction(51.2)        # 'NE'
```

### `midpoint(lat1, lon1, lat2, lon2) -> tuple[float, float]`

Geographic midpoint between two coordinates.

```python
from distancefyi import midpoint

midpoint(37.5665, 126.978, 35.6762, 139.6503)  # (36.82..., 133.36...)
```

### `great_circle_points(lat1, lon1, lat2, lon2, num_points) -> list[tuple[float, float]]`

Generate waypoints along the great circle arc for route visualization.

```python
from distancefyi import great_circle_points

points = great_circle_points(40.7128, -74.0060, 51.5074, -0.1278, num_points=10)
# List of 11 (lat, lon) tuples along the NYC-London arc
```

### `antipodal_point(lat, lon) -> tuple[float, float]`

Point on the exact opposite side of Earth.

```python
from distancefyi import antipodal_point

antipodal_point(40.7128, -74.0060)  # (-40.7128, 105.994)
```

### `estimate_flight_time(distance_km) -> int`

Estimated flight time in minutes (includes 30-min takeoff/landing overhead).

```python
from distancefyi import estimate_flight_time

estimate_flight_time(1159)   # 123 minutes (Seoul-Tokyo)
estimate_flight_time(5570)   # 423 minutes (NYC-London)
```

### `estimate_drive_time(distance_km, same_continent) -> int`

Estimated driving time in minutes (1.3x road factor, variable speed). Returns 0 for cross-ocean.

```python
from distancefyi import estimate_drive_time

estimate_drive_time(500)                       # ~520 minutes
estimate_drive_time(5570, same_continent=False) # 0 (cross-ocean)
```

### `estimate_walk_time(distance_km) -> int`

Estimated walking time in minutes at 5 km/h. Returns 0 for distances over 100km.

```python
from distancefyi import estimate_walk_time

estimate_walk_time(10)   # 120 minutes
estimate_walk_time(200)  # 0 (over 100km limit)
```

### `km_to_miles(km) -> int` / `km_to_nautical_miles(km) -> int` / `miles_to_km(miles) -> int`

Unit conversions between distance units.

```python
from distancefyi import km_to_miles, km_to_nautical_miles, miles_to_km

km_to_miles(1159)           # 720
km_to_nautical_miles(1159)  # 626
miles_to_km(720)            # 1159
```

### `format_distance(km) -> str` / `format_duration(minutes) -> str`

Human-readable formatting helpers.

```python
from distancefyi import format_distance, format_duration

format_distance(12345)   # '12,345 km'
format_duration(123)     # '2h 03m'
format_duration(1500)    # '1d 1h'
```

## REST API (No Auth Required)

```bash
curl "https://distancefyi.com/api/distance/?lat1=37.57&lon1=126.98&lat2=35.68&lon2=139.65"
curl https://distancefyi.com/api/city/seoul/tokyo/
curl https://distancefyi.com/api/cities/
```

Full spec: [OpenAPI 3.1.0](https://distancefyi.com/api/openapi.json)

## Distance Reference

| Route | km | miles | nmi | Flight | Bearing |
|-------|-----|-------|-----|--------|---------|
| Seoul -- Tokyo | 1,159 | 720 | 626 | ~2h | ESE |
| NYC -- London | 5,570 | 3,461 | 3,007 | ~7h | NE |
| NYC -- LA | 3,944 | 2,451 | 2,130 | ~5h | WSW |
| London -- Paris | 344 | 214 | 186 | ~1h | SSE |
| Sydney -- Tokyo | 7,823 | 4,861 | 4,224 | ~9.5h | NNW |

## Demo

![DistanceFYI demo](https://raw.githubusercontent.com/fyipedia/distancefyi/main/demo.gif)

## Utility FYI Family

Part of the [FYIPedia](https://fyipedia.com) ecosystem: [UnitFYI](https://unitfyi.com), [TimeFYI](https://timefyi.com), [HolidayFYI](https://holidayfyi.com), [NameFYI](https://namefyi.com), [DistanceFYI](https://distancefyi.com).
