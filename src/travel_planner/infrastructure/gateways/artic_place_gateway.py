from travel_planner.application.dtos.http import HTTPRequest
from travel_planner.application.interfaces.http_client import HTTPClient
from travel_planner.application.interfaces.place_gateway import PlaceGateway


class ArticPlaceGateway(PlaceGateway):
    def __init__(self, http_client: HTTPClient) -> None:
        self._http_client = http_client

    async def validate_place(self, external_id: int) -> bool:
        url = f"/{external_id}?fields=id"
        request = HTTPRequest(url=url)

        response = await self._http_client.get(request)
        return response.status_code == 200
