"""Tests for the distancefyi API client."""

from distancefyi.api import DistanceFYI


def test_client_init() -> None:
    """Client initializes with default URL."""
    client = DistanceFYI()
    assert str(client._client.base_url).rstrip("/") == "https://distancefyi.com/api"
    client.close()


def test_client_custom_url() -> None:
    """Client accepts custom base URL."""
    client = DistanceFYI(base_url="https://custom.example.com/api")
    assert str(client._client.base_url).rstrip("/") == "https://custom.example.com/api"
    client.close()


def test_client_context_manager() -> None:
    """Client works as context manager."""
    with DistanceFYI() as client:
        assert client._client is not None
