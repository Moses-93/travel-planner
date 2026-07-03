from typing import Annotated

from fastapi import Depends

from travel_planner.application.interfaces.http_client import HTTPClient
from travel_planner.application.interfaces.place_gateway import PlaceGateway
from travel_planner.infrastructure.gateways.artic_place_gateway import ArticPlaceGateway
from travel_planner.infrastructure.transport.httpx_client import HTTPXClient


def get_artic_http_client() -> HTTPClient:
    return HTTPXClient(base_url="https://api.artic.edu/api/v1/artworks", timeout=10.0)


ArticHTTPClientDependency = Annotated[HTTPClient, Depends(get_artic_http_client)]


def get_place_gateway(http_client: ArticHTTPClientDependency) -> PlaceGateway:
    return ArticPlaceGateway(http_client=http_client)


PlaceGatewayDependency = Annotated[PlaceGateway, Depends(get_place_gateway)]
