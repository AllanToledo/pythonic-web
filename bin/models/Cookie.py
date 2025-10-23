from datetime import datetime


class Cookie:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
        self.expires = None
        self.http_only = None
        self.secure = None

    def setName(self, name: str) -> None:
        self.name = name

    def getName(self) -> str:
        return self.name

    def setValue(self, value: str) -> None:
        self.value = value

    def getValue(self) -> str:
        return self.value

    def setHttpOnly(self, http_only: bool) -> None:
        self.http_only = http_only

    def getHttpOnly(self) -> bool:
        return self.http_only

    def setSecure(self, secure: bool) -> None:
        self.secure = secure

    def getSecure(self) -> bool:
        return self.secure

    def setExpires(self, expires: datetime) -> None:
        self.expires = expires

    def getExpires(self) -> datetime:
        return self.expires

    def __str__(self):
        cookie = f"{self.name}={self.value}; "
        if not self.expires is None:
            cookie += f"Expires={self.expires}; "
        if not self.secure is None and self.secure:
            cookie += "Secure; "
        if not self.http_only is None and self.http_only:
            cookie += "HttpOnly; "

        return cookie

