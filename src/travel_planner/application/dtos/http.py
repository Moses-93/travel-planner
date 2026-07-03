from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class HTTPRequest[T]:
    """A generic container for HTTP request data.
    """

    url: str
    body: dict[str, Any] | None = field(default=None)
    params: dict[str, Any] | None = field(default=None)
    headers: dict[str, Any] | None = field(default=None)


@dataclass(frozen=True, slots=True)
class HTTPResponse[T]:
    """A standardized, immutable container for HTTP response data.
    """

    status_code: int
    data: T
    headers: dict[str, str] = field(default_factory=dict[str, str])

    @property
    def is_success(self) -> bool:
        """Returns True if the status code indicates success (200-299)."""
        return 200 <= self.status_code < 300
