import re
from http import HTTPStatus
from typing import Callable

from bin.filters.Filter import Filter
from bin.exceptions.HttpException import HttpException
from bin.models.Request import Request
from bin.models.Response import Response


class InitFilter(Filter):
    __PATH_ALLOWED_RE__ = re.compile(r"^/(\w+)?(/\w+)?(\.(html|wpy|css|js))?$")

    def doFilter(self, request: Request, response: Response, filter_chain: Callable[[Request, Response], None]) -> None:
        match = InitFilter.__PATH_ALLOWED_RE__.match(request.getPath())
        if match is None:
            raise HttpException(HTTPStatus.NOT_FOUND, "")

        if request.getPath().endswith("/"):
            request.setPath(request.getPath() + "index.wpy")

        if '.' not in request.getPath().split('/')[-1]:
            request.setPath(request.getPath() + ".wpy")

        filter_chain(request, response)
