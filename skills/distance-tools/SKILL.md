---
name: distance-tools
description: Calculate Haversine distance, bearing, midpoint, travel times, and bounding boxes between geographic coordinates.
---

# Distance Tools

Geographic distance calculations powered by [distancefyi](https://distancefyi.com/) -- a pure Python Haversine engine with zero dependencies.

## Setup

Install the MCP server:

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

## Available Tools

| Tool | Description |
|------|-------------|
| `distance_calc` | Haversine distance between two coordinates (km, miles, nautical miles) |
| `bearing` | Initial and final bearing between two points |
| `midpoint` | Geographic midpoint between two coordinates |
| `travel_time` | Estimated travel times by car, train, and flight |
| `bounding_box` | Bounding box around a point at a given radius |

## When to Use

- Calculating distances between cities or coordinates
- Finding the bearing or direction between two points
- Estimating travel times for different transport modes
- Computing geographic midpoints for meeting locations
- Creating bounding boxes for geospatial queries

## Demo

![DistanceFYI CLI Demo](https://raw.githubusercontent.com/fyipedia/distancefyi/main/demo.gif)

## Links

- [Distance Calculator](https://distancefyi.com/) -- Calculate distances between any two places
- [API Documentation](https://distancefyi.com/developers/) -- Free REST API
- [PyPI Package](https://pypi.org/project/distancefyi/)
