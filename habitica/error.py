class HabiticaError(Exception):
    def __init__(self, message: str):
        self.message = message


class NotFoundError(HabiticaError):
    pass


class BadRequestError(HabiticaError):
    pass


class NotAuthorizedError(HabiticaError):
    pass


class TooManyRequestsError(HabiticaError):
    pass
