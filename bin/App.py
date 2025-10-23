from http import HTTPStatus
from http.server import ThreadingHTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from bin.filters.Filter import Filter
from bin.engine.RenderEngine import __render__
from bin.models.Response import Response
from bin.models.Request import Request
from bin.security.AuthenticatedUser import AuthenticatedUser


def __parse_path__(path: str) -> str:
    pos = path.find('?')
    if pos > 0:
        return path[0:pos]
    return path


def __parse_query__(path: str) -> dict[str, str]:
    params: dict[str, str] = dict()
    query = urlparse(path).query
    for key, values in parse_qs(query).items():
        params[key] = values[-1]
    return params


def __parse_form__(body: str) -> dict[str, str]:
    params: dict[str, str] = dict()
    for key, values in parse_qs(body).items():
        params[key] = values[-1]
    return params

class WebPythonHandler(BaseHTTPRequestHandler):
    def do(self):
        try:

            env = self.environment()

            iterator = iter(App.FILTERS)
            def filter_chain(request: Request, response: Response):
                try:
                    app_filter = next(iterator)
                    app_filter.doFilter(request, response, filter_chain)
                except StopIteration:
                    response.setBody(__render__(request.getPath(), env))
                    response.setHeader("content-type", "text/html; charset=utf-8")

            filter_chain(env.get("REQUEST"), env.get("RESPONSE"))
            App.clearSession()

            response: Response = env.get("RESPONSE")
            status = response.getStatus()

            self.send_response(status if not status is None else HTTPStatus.OK)
            for header in response.getHeaders().items():
                self.send_header(header[0], str(header[1]))
            for cookie in response.getCookies():
                self.send_header("set-cookie", str(cookie))
            self.end_headers()
            self.wfile.write(response.getBody().encode("utf-8"))

        except Exception as e:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.log_error(str(e))

    def environment(self):
        if App.ENV is None:
            # self.log_message("App.ENV is None")
            environment = dict()
        else:
            environment = App.ENV.copy()

        def write(x: any) -> None:
            if hasattr(x, '__iter__') and not isinstance(x, str):
                for i in x:
                    environment["__buffer__"] += str(i)
            else:
                environment["__buffer__"] += str(x)

        environment["write"] = write
        environment["print"] = self.log_message
        environment["__buffer__"] = ""

        request = Request()
        request.setMethod(self.command)
        request.setHeaders(self.headers)
        request.setPath(__parse_path__(self.path))

        content_len_header = self.headers.get('content-length')
        if not content_len_header is None:
            content_len = int(content_len_header)
            body = self.rfile.read(content_len).decode()
            request.setBody(body)

        query_params_map = __parse_query__(self.path)
        request.setQuery(query_params_map)

        if request.getHeader("content-type") == "application/x-www-form-urlencoded":
            form_params_map = __parse_form__(request.getBody())
            request.setForm(form_params_map)

        self.path = urlparse(self.path).path

        environment["REQUEST"] = request
        environment["RESPONSE"] = Response()

        return environment

    def do_GET(self):
        self.do()

    def do_POST(self):
        self.do()

class App:
    ENV: dict[str,any] = None
    DEV: bool = False
    FOLDER_ROOT = "./www"
    USER = None
    FILTERS: list[Filter] = list()

    @staticmethod
    def setDevelopmentMode(debug: bool) -> None:
        App.DEV = debug

    @staticmethod
    def setEnvironment(env: dict[str, any]) -> None:
        App.ENV = env

    @staticmethod
    def run(host = '127.0.0.1', port = 80) -> None:
        print(f"SERVER STARTED AT {host}:{port}")

        httpd = ThreadingHTTPServer((host, port), WebPythonHandler)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt as e:
            print("Shutting down server.")
        except Exception as e:
            print(e)
        finally:
            httpd.server_close()

    @staticmethod
    def setRootFolderPath(path):
        App.FOLDER_ROOT = path

    @staticmethod
    def getAuthenticatedUser() -> AuthenticatedUser | None:
        return App.USER

    @staticmethod
    def setAuthenticatedUser(user: AuthenticatedUser | None) -> None:
        App.USER = user

    @staticmethod
    def clearSession() -> None:
        App.USER = None

    @staticmethod
    def addFilter(new_filter: Filter) -> None:
        App.FILTERS.append(new_filter)
