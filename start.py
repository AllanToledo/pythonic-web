from http import HTTPStatus

from bin.App import App
from bin.filters.InitFilter import InitFilter
from bin.filters.AuthFilter import AuthFilter
from bin.filters.RenderErrorFilter import RenderErrorFilter

if __name__ == "__main__":

    renderErrorFilter = RenderErrorFilter()
    renderErrorFilter.setErrorPage(HTTPStatus.NOT_FOUND, "/error/404.wpy")
    renderErrorFilter.setErrorPage(HTTPStatus.UNAUTHORIZED, "/error/401.wpy")

    initFilter = InitFilter()

    App.setDevelopmentMode(True)
    App.setRootFolderPath("./www")
    App.addFilter(renderErrorFilter)
    App.addFilter(initFilter)

    App.run()
