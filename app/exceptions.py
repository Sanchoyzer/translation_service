class BaseError(Exception):
    pass


class ClientError(BaseError):
    pass


class MistakeInWordError(ClientError):
    pass


class ServerError(BaseError):
    pass
