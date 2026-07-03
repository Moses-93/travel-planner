class ErrorMessages:
    @staticmethod
    def service_unavailable() -> str:
        return "Service is currently unavailable."

    @staticmethod
    def constraint_violation() -> str:
        return "A data constraint violation occurred."

    @staticmethod
    def invalid_data() -> str:
        return "Invalid data encountered."

    @staticmethod
    def unexpected_error() -> str:
        return "An unexpected error occurred."
