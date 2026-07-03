from typing import Protocol


class PlaceGateway(Protocol):
    """Protocol for the external API to fetch and validate places."""

    async def validate_place(self, external_id: int) -> bool:
        """Validate if a place with the given external ID exists.

        Args:
            external_id (int): The external ID of the place to validate.

        Returns:
            bool: True if the place exists, False otherwise.

        Raises:
            HttpClientError: If a network or HTTP error occurs during the request.
        """
        ...
