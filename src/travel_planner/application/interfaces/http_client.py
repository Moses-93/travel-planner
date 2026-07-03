from typing import Protocol

from travel_planner.application.dtos import HTTPRequest, HTTPResponse


class HTTPClient(Protocol):
    """Defines the contract for HTTP client adapters.

    This interface ensures consistent request handling regardless of the
    underlying transport library.
    """

    async def get[T](self, request: HTTPRequest[T]) -> HTTPResponse[T]:
        """Performs an HTTP GET request using the provided request specification.

        Args:
            request (HTTPRequest[T]): The specification of the request to perform.

        Returns:
            HTTPResponse[T]: The standardized response object.

        Raises:
            HttpClientError: When an HTTP or network-related error occurs.
        """
        ...

    async def post[T](self, request: HTTPRequest[T]) -> HTTPResponse[T]:
        """Performs an HTTP POST request using the provided request specification.

        Args:
            request (HTTPRequest[T]): The specification of the request to perform.

        Returns:
            HTTPResponse[T]: The standardized response object.

        Raises:
            HttpClientError: When an HTTP or network-related error occurs.
        """
        ...

    async def close(self) -> None:
        """Closes the underlying HTTP client and releases resources (connections).
        """
        ...
