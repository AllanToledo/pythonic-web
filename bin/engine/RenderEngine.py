import re
from http import HTTPStatus

from bin.engine.Block import Block
from bin.exceptions.HttpException import HttpException

WebPage = tuple[Block, ...]

__WPY_RE__ = re.compile(r"(<python>|<py>)([\S\s]+?)(?=</python>|</py>)(</python>|</py>)")
__TABS_RE__ = re.compile(r"^( *)\S.+$")
__page_cache__: dict[str, WebPage] = dict()
__file_cache__: dict[str, str] = dict()


def __render__(path: str, environment: dict[str, any]) -> str:

    rendered_content = None
    if path.endswith(".wpy"):
        global __page_cache__
        cached_page: WebPage = __page_cache__.get(path)

        from bin.App import App
        if cached_page is None or App.DEV:
            __page_cache__[path] = __compile__(path)
            cached_page = __page_cache__.get(path)

        rendered_content = __run__(cached_page, environment)
    else:
        global __file_cache__
        cached_file: str = __file_cache__.get(path)

        from bin.App import App
        if cached_file is None or App.DEV:
            __file_cache__[path] = __get_file__(path)
            cached_file = __file_cache__.get(path)

        rendered_content = cached_file

    return rendered_content


def __get_file__(path: str) -> str:
    from bin.App import App
    try:
        with open(f"{App.FOLDER_ROOT}{path}", "r") as file:
            return ''.join(file.readlines())
    except FileNotFoundError as e:
        raise HttpException(HTTPStatus.NOT_FOUND, "")


def __evaluate__(block: Block, environment: dict[str, any]) -> str:
    if block.isHtml():
        return block.getHtml()

    environment["__buffer__"] = ""

    if block.isInline():
        return str(eval(block.getCode(), globals(), environment))

    exec(block.getCode(), globals(), environment)
    return environment["__buffer__"]


def __run__(page: WebPage, environment: dict[str, any]) -> str:
    return ''.join(map(lambda x: __evaluate__(x, environment), page))


def __compile__(path: str) -> WebPage:

    from bin.App import App
    try:
        with open(f"{App.FOLDER_ROOT}{path}", "r") as file:
            content = ''.join(file.readlines())
            parsed_content = __WPY_RE__.split(content)
    except FileNotFoundError as e:
        raise HttpException(HTTPStatus.NOT_FOUND, "")

    new_page: list[Block] = list()
    is_code_block = False
    inline = False
    for block in parsed_content:
        if is_code_block:
            is_code_block = False
            lines = block.splitlines()
            min_indent = 99999999
            for line in lines:
                match = __TABS_RE__.match(line)
                if match is None:
                    continue
                min_indent = min(min_indent, len(match.group(1)))

            lines = map(lambda x: x[min_indent:], lines)
            code = '\n'.join(lines)
            mode = "eval" if inline else "exec"
            try:
                compiled = compile(code, "<string>", mode)
            except Exception as e:
                print(block)
                raise e
            new_page.append(Block(None, compiled, inline))
            continue

        if block == "<python>" or block == "<py>":
            is_code_block = True
            inline = block == "<py>"
            continue

        if block == "</python>" or block == "</py>":
            continue

        new_page.append(Block(block, None))

    return tuple(new_page)
