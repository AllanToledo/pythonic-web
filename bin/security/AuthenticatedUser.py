class AuthenticatedUser:
    def __init__(self):
        self.credentials = list()
        self.username = None
        pass

    def setUsername(self, username: str) -> None:
        self.username = username

    def getUsername(self) -> str:
        return self.username

    def getCredentials(self) -> list[str]:
        return self.credentials

    def setCredentials(self, credentials: list[str]) -> None:
        self.credentials = credentials

    def getToken(self) -> str:
        return self.username