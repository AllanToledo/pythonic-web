from http import HTTPStatus
from typing import Callable

from bin.App import App
from bin.filters.Filter import Filter, FilterChain
from bin.exceptions.HttpException import HttpException
from bin.models.Request import Request
from bin.models.Response import Response


class AuthFilter(Filter):
    def __init__(self):
        self.required_credentials: dict[str, set[str]] = dict()

    def addRequiredCredentials(self, path: str, credential: str) -> None:
        if self.required_credentials.get(path) is None:
            self.required_credentials[path] = set()

        register = self.required_credentials.get(path)
        register.add(credential)

    def doFilter(self, request: Request, response: Response, filter_chain: FilterChain) -> None:
        user = App.getAuthenticatedUser()
        path = request.getPath()
        credentials_needed = self.required_credentials.get(path)

        allowed = credentials_needed is None

        if not allowed and not user is None:
            for credential in user.getCredentials():
                if credential in credentials_needed:
                    allowed = True
                    break

        if allowed:
            filter_chain(request, response)
        else:
            raise HttpException(HTTPStatus.UNAUTHORIZED, "Requer Autenticação")
