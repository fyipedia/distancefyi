"""HTTP API client for distancefyi.com REST endpoints.

Requires: pip install distancefyi[api]

Usage::

    from distancefyi.api import DistanceFYI

    with DistanceFYI() as client:
        result = client.distance("seoul", "tokyo")
        print(result["distance_km"])
"""

from __future__ import annotations

from typing import Any

import httpx


class DistanceFYI:
    """API client for the distancefyi.com REST API."""

    def __init__(
        self,
        base_url: str = "https://distancefyi.com/api",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    def distance(self, from_city: str, to_city: str) -> dict[str, Any]:
        """Get distance between two cities by slug.

        Args:
            from_city: City slug (e.g., "seoul", "new-york").
            to_city: City slug (e.g., "tokyo", "london").

        Returns:
            Dict with distance_km, distance_miles, bearing, etc.
        """
        return self._get(f"/distance/{from_city}-to-{to_city}/")

    def city(self, slug: str) -> dict[str, Any]:
        """Get city information.

        Args:
            slug: City slug (e.g., "seoul", "london").

        Returns:
            Dict with name, country, coordinates, timezone, etc.
        """
        return self._get(f"/city/{slug}/")

    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search for cities by name.

        Args:
            query: Search query string.
            limit: Maximum results to return.

        Returns:
            List of matching city dicts.
        """
        result = self._get("/search/", q=query, limit=limit)
        if isinstance(result, list):
            return list(result)
        results: list[dict[str, Any]] = result.get("results", [])
        return results

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> DistanceFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
