import email
from http import HTTPStatus

from bin.models.Cookie import Cookie


class Response:
    def __init__(self):
        self.status = None
        self.headers = email.message.Message()
        self.body = None
        self.redirected_path = None
        self.cookies = list()

    def setHeaders(self, headers: email.message.Message) -> None:
        self.headers = headers

    def setHeader(self, name: str, value: str, **params):
        self.headers.add_header(name, value, **params)

    def getHeaders(self) -> email.message.Message:
        return self.headers

    def getHeader(self, header: str) -> str:
        return self.headers.get(header)

    def setBody(self, body: str) -> None:
        self.body = body

    def getBody(self) -> str:
        return self.body

    def setStatus(self, status: HTTPStatus) -> None:
        self.status = status

    def getStatus(self) -> HTTPStatus:
        return self.status

    def redirect(self, path: str) -> None:
        self.status = HTTPStatus.SEE_OTHER
        self.setHeader("location", path)
        self.redirected_path = path

    def setCookie(self, cookie: Cookie) -> None:
        self.cookies.append(cookie)

    def getCookies(self) -> list[Cookie]:
        return self.cookies

    def getRedirect(self) -> str | None:
        return self.redirected_path