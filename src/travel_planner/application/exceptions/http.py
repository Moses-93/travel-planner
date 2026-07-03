from .base import ApplicationException


class HttpClientError(ApplicationException):
    """Base exception for transport-level HTTP client errors."""


class HttpClientConnectionError(HttpClientError):
    """Raised when HTTP client cannot reach remote server."""

    @classmethod
    def request_failed(
        cls, *, method: str, url: str, reason: str
    ) -> "HttpClientConnectionError":
        return cls(f"HTTP {method} request to '{url}' failed: {reason}")


class HttpClientTimeoutError(HttpClientError):
    """Raised when HTTP client request times out."""

    @classmethod
    def request_timed_out(
        cls,
        *,
        method: str,
        url: str,
        timeout_seconds: int | float | None,
        reason: str,
    ) -> "HttpClientTimeoutError":
        timeout = (
            "without a timeout limit"
            if timeout_seconds is None
            else f"after {timeout_seconds}s"
        )
        return cls(f"HTTP {method} request to '{url}' timed out {timeout}: {reason}")
