from http import HTTPStatus


class HttpException(Exception):
    def __init__(self, status: HTTPStatus, message: str):
        self.status = status
        self.message = message

    def getStatus(self) -> HTTPStatus:
        return self.status

    def getMessage(self) -> str:
        return self.message
