# -- Importing basic QT modules
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl, Qt

# -- Importing Web QT modules
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile


# -- Widget


class Engine(QWebEngineView):
    """
    Widget that will render the html file.

    params:
    - parent: QWidget
    - url: QUrl
    """

    def __init__(self, parent: QWidget, mainWin, url: QUrl):
        """Inits `Engine`."""
        super().__init__(parent)

        # Setting parameters
        self.mainWin = mainWin
        """`src.Window` instance."""

        # Configuring Widget and Privacy
        self.privacy_config()
        self.config_widget()

        # Loading start page
        self.load(url)

        # Loading functions
        self.page().loadStarted.connect(self.loading)
        self.page().loadFinished.connect(self.loaded)
        self.page().linkHovered.connect(self.link_hover)
        self.page().urlChanged.connect(self.url_changed)

    # -- Configuring
    def config_widget(self):
        """Configures the Widget."""
        self.setMinimumWidth(600)

    # -- Privacy Config
    # -- WARNING: Important!
    def privacy_config(self):
        """
        Configures the `Engine` attributes to improve user privacy, blocking Js, cookies, trackers...
        It's the main Browser Privacy Feature, please add a Issue if you find.

        <a href="https://github.com/RickBarretto/PreviewGram/issues">Report a Issue</a>.
        """
        self.page().settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        self.page().profile().clearHttpCache()
        print("Off Record:" + str(self.page().profile().isOffTheRecord()))
        self.page().profile().setPersistentStoragePath("")
        self.page().profile().setPersistentCookiesPolicy(
            QWebEngineProfile.NoPersistentCookies
        )
        self.page().profile().setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        )

    # -- WARNING: Important!
    def clear_data(self):
        """Clears HttpsCache and VisitedLinks."""
        self.page().profile().clearHttpCache()
        self.page().profile().clearAllVisitedLinks()

    # -- Actions
    def update(self):
        """Reload the `Engine`'s page."""
        self.reload()

    def loading(self):
        """Clears HttpsCache and VisitedLinks and changes the cursor to `Qt.BusyCursor`."""
        self.mainWin.setCursor(QCursor(Qt.BusyCursor))

    def loaded(self):
        """Changes the cursor to `Qt.OpenHandCursor`."""
        self.clear_data()
        self.mainWin.setCursor(QCursor(Qt.OpenHandCursor))

    def link_hover(self):
        """Creates a tooltip, teachin how to open links."""
        self.setToolTip("[Right Mouse Button] > Copy Link Address")

    def url_changed(self):
        """
        Clears HttpsCache and VisitedLinks and checks current url.

        - Todo:
            - Change url checker to intercept()
        """
