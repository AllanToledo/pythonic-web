from typing import Callable

from bin.models.Request import Request
from bin.models.Response import Response

FilterChain = Callable[[Request, Response], None]

class Filter:
    def doFilter(self, request: Request, response: Response, filter_chain: FilterChain) -> None:
        filter_chain(request, response)
