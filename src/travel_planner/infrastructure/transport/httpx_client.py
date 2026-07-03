import json
from typing import Any, Literal, cast

import httpx

from travel_planner.application.dtos import HTTPRequest, HTTPResponse
from travel_planner.application.exceptions import (
    HttpClientConnectionError,
    HttpClientTimeoutError,
)
from travel_planner.application.interfaces import HTTPClient


class HTTPXClient(HTTPClient):
    def __init__(
        self,
        base_url: str = "",
        timeout: int | float | None = 10.0,
        headers: dict[str, str] | None = None,
        auth: Any | None = None,
        verify: bool | str = True,
        cookies: dict[str, str] | None = None,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers
        self.auth = auth
        self.verify = verify
        self.cookies = cookies
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers,
            auth=auth,
            cookies=cookies,
            verify=verify,
        )

    async def get[T](
        self,
        request: HTTPRequest[T],
    ) -> HTTPResponse[T]:
        response = await self._request(
            method="GET",
            url=request.url,
            headers=request.headers,
            params=request.params,
        )
        return self._map_response(response)

    async def post[T](
        self,
        request: HTTPRequest[T],
    ) -> HTTPResponse[T]:
        response = await self._request(
            method="POST",
            url=request.url,
            headers=request.headers,
            body=request.body,
        )
        return self._map_response(response)

    async def close(self) -> None:
        await self._client.aclose()

    async def _request(
        self,
        *,
        method: Literal["GET", "POST"],
        url: str,
        headers: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> httpx.Response:
        try:
            if method == "GET":
                return await self._client.get(
                    url=url,
                    params=params,
                    headers=headers,
                )

            return await self._client.post(
                url=url,
                json=body,
                headers=headers,
            )
        except httpx.TimeoutException as exc:
            raise HttpClientTimeoutError.request_timed_out(
                method=method,
                url=url,
                timeout_seconds=self.timeout,
                reason=str(exc),
            ) from exc
        except httpx.RequestError as exc:
            raise HttpClientConnectionError.request_failed(
                method=method,
                url=url,
                reason=str(exc),
            ) from exc

    def _map_response[T](self, response: httpx.Response) -> HTTPResponse[T]:  # pyright: ignore[reportInvalidTypeVarUse]
        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError):
            data = response.text or response.content
        return HTTPResponse(
            status_code=response.status_code,
            data=cast(T, data),
            headers=dict(response.headers),
        )
