from bin.App import App
from bin.filters.InitFilter import InitFilter

if __name__ == "__main__":

    initFilter = InitFilter()

    App.setDevelopmentMode(True)
    App.setRootFolderPath("./www")
    App.addFilter(initFilter)

    App.run()
