"""HTTP API client for distancefyi.com REST endpoints.

Requires the ``api`` extra: ``pip install distancefyi[api]``

Usage::

    from distancefyi.api import DistanceFYI

    with DistanceFYI() as api:
        items = api.list_cities()
        detail = api.get_city("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class DistanceFYI:
    """API client for the distancefyi.com REST API.

    Provides typed access to all distancefyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://distancefyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://distancefyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_cities(self, **params: Any) -> dict[str, Any]:
        """List all cities."""
        return self._get("/api/v1/cities/", **params)

    def get_city(self, slug: str) -> dict[str, Any]:
        """Get city by slug."""
        return self._get(f"/api/v1/cities/" + slug + "/")

    def list_countries(self, **params: Any) -> dict[str, Any]:
        """List all countries."""
        return self._get("/api/v1/countries/", **params)

    def get_country(self, slug: str) -> dict[str, Any]:
        """Get country by slug."""
        return self._get(f"/api/v1/countries/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> DistanceFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
