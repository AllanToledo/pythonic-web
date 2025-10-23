from types import CodeType


class Block:
    def __init__(self, html: str | None, code: CodeType | None, inline = False):
        self.html = html
        self.code = code
        self.inline = inline

    def isCode(self) -> bool:
        return not self.code is None

    def getCode(self) -> CodeType:
        return self.code

    def isHtml(self) -> bool:
        return not self.html is None

    def getHtml(self) -> str:
        return self.html

    def isInline(self) -> bool:
        return self.inline