from http import HTTPStatus
from typing import Callable

from bin.filters.Filter import Filter, FilterChain
from bin.exceptions.HttpException import HttpException
from bin.engine.RenderEngine import __render__
from bin.models.Request import Request
from bin.models.Response import Response


class RenderErrorFilter(Filter):
    def __init__(self):
        self.pages: dict[HTTPStatus, str] = dict()

    def setErrorPage(self, status: HTTPStatus, path: str) -> None:
        self.pages[status] = path

    def doFilter(self, request: Request, response: Response, filter_chain: FilterChain) -> None:
        try:
            filter_chain(request, response)
        except HttpException as e:
            response.setStatus(e.getStatus())
            page_path = self.pages.get(e.getStatus())
            if not page_path is None:
                response.setBody(__render__(page_path, None))
            else:
                response.setBody("Error")
