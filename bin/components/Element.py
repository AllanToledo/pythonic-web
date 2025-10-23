class Element:
    NEXT_ID = 0

    @staticmethod
    def getNextID() -> str:
        Element.NEXT_ID += 1
        return str(Element.NEXT_ID)

    def __init__(self):
        self.id = Element.getNextID()
        pass

    def setId(self, id: str) -> None:
        self.id = id

    def getId(self) -> str:
        return self.id

    def render(self) -> str:
        return f'<span id="{self.id}">Override this method</span>'

    def __str__(self):
        return self.render()

