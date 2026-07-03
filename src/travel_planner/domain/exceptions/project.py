from .base import DomainException


class TravelProjectError(DomainException):
    """Base exception for TravelProject related domain errors."""

    pass


class CountPlacesError(TravelProjectError):
    """Raised when a project exceeds the maximum allowed places."""

    def __init__(self, message: str = "A travel project cannot have more than 10 places.") -> None:
        super().__init__(message)


class DuplicatePlaceError(TravelProjectError):
    """Raised when attempting to add a place that is already in the project."""

    def __init__(self, external_id: int) -> None:
        super().__init__(f"Place with external ID {external_id} is already in the project.")


class PlaceAlreadyVisitedError(TravelProjectError):
    """Raised when attempting an operation on a place that is already visited."""

    def __init__(self, message: str = "This place has already been visited.") -> None:
        super().__init__(message)


class ProjectHasVisitedPlacesError(TravelProjectError):
    """Raised when attempting to delete a project that has visited places."""

    def __init__(self, message: str = "Cannot delete a project that has visited places.") -> None:
        super().__init__(message)
