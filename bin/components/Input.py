from bin.models.Request import Request
from bin.components.Element import Element
from bin.utility import orEmpty

class Input(Element):

    def __init__(self, name: str, request: Request):
        super().__init__()
        self.classes = None
        self.placeholder = None
        self.label = name
        self.name = name
        self.type = "text"
        if request.getForm() is None:
            self.value = None
        else:
            self.value = request.getForm().get(self.name)


    def setLabel(self, label: str) -> None:
        self.label = label

    def getLabel(self) -> str:
        return self.label

    def setRawValue(self, value: str) -> None:
        self.value = value

    def getRawValue(self) -> str:
        return self.value

    def isValid(self) -> bool:
        return not self.value is None

    def getValue(self) -> any:
        return self.value

    def setPlaceholder(self, placeholder: str) -> None:
        self.placeholder = placeholder

    def getPlaceholder(self) -> str:
        return self.placeholder

    def setClasses(self, classes: str) -> None:
        self.classes = classes

    def getClasses(self) -> str:
        return self.classes

    def setType(self, type: str) -> None:
        self.type = type

    def getType(self) -> str:
        return self.type

    def render(self) -> str:
        return f"""
            <label for="{self.id}">{self.label}</label>
            <input id="{self.id}" type="{self.type}" class="{self.classes}" name="{self.name}" value="{orEmpty(self.value)}" placeholder="{orEmpty(self.placeholder)}"></input>
        """
