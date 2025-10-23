import email
import re

class Request:
    # this should be revisited
    COOKIE_RE = re.compile("(\\w+)=(\\w+)")
    def __init__(self):
        self.body = None
        self.query = None
        self.form = None
        self.headers = None
        self.method = None
        self.path = None
        self.cookies = None

    def setPath(self, path: str) -> None:
        self.path = path

    def getPath(self) -> str:
        return self.path

    def setMethod(self, method: str) -> None:
        self.method = method

    def getMethod(self) -> str:
        return self.method

    def setHeaders(self, headers: email.message.Message) -> None:
        self.cookies = None
        self.headers = headers

    def getHeaders(self) -> str:
        return self.headers

    def getHeader(self, header: str) -> str:
        return self.headers.get(header)

    def getCookies(self) -> str:
        return self.headers.get("Cookie")

    def getCookie(self, cookie_name) -> str | None:
        if self.cookies is None:
            cookies = self.getCookies()
            if cookies is None:
                return None
            self.cookies = dict()
            matches = Request.COOKIE_RE.findall(cookies)
            for match in matches:
                self.cookies[match[0]] = match[1]

        return self.cookies.get(cookie_name)

    def setForm(self, form: dict[str, str]) -> None:
        self.form = form

    def getForm(self) -> dict[str, str]:
        return self.form

    def setQuery(self, query: dict[str, str]) -> None:
        self.query = query

    def getQuery(self) -> dict[str, str]:
        return self.query

    def setBody(self, body: str) -> None:
        self.body = body

    def getBody(self) -> str:
        return self.body