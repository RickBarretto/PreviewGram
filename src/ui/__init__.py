"""Loads Widgets from `components` and creates the `Container` main Widget."""

# -- importing Qt modules
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

# -- importing components modules
from .widgets.side_bar import ChannelList as SideBar
from .widgets.top_bar import TopBar
from .widgets.engine import Engine
from .widgets.open_dialog import AddBtn


# -- SubWidget: shows the content


class Content(QWidget):
    """
    It's the content's container-

    It'll show the SideBar
    (src.ui.components.chan_list.ChannelList) and the Engine (`src.ui.components.engine.Engine`).

    > layout: `HBox`

    params:
    - parent: QWidget
    - channels: dict

    > ``channels`` must to be returned by the Model.get_channel()
    """

    def __init__(self, parent: QWidget, mainWin, channels: dict, path) -> None:
        """Inits the `Content`."""
        super().__init__(parent)

        self.channels = channels
        """`channels` is the channels loaded from database."""
        self.mainWin = mainWin
        """It's the main window instance."""
        self.path = path
        """It's the application path."""
        self.eng = Engine(
            self, self.mainWin, QUrl.fromLocalFile(self.path + "/data/index.html")
        )
        """Instances the WebEngine (`src.ui.components.engine.Engine`)."""

        self.add_btn = AddBtn(self, mainWin)
        """Adds the `AddBtn` to current Widget."""

        self.layout = QHBoxLayout()
        """Sets layout as Horizontal Box."""

        self.config_widget()
        self.config_layout()
        self.add_widgets()

        self.setLayout(self.layout)

    def config_widget(self):
        """Configures the `Content` Widget."""
        self.setAutoFillBackground(True)
        self.setWhatsThis("Hello")

    def config_layout(self):
        """Configures the `Content.layout`."""
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(1)

    def add_widgets(self):
        """Adds `SideBar` and `eng` to `Content.layout`."""
        self.layout.addWidget(SideBar(self, self.channels), 0)
        self.layout.addWidget((self.eng), 1)

    def open_url(self, url):
        """Opens a url on `src.ui.components.engine.Engine`."""
        print(f"handling url: {url}")
        self.eng.stop()
        self.eng.load(QUrl(url))


# -- Main Widget: show the Topbar and Content


class Container(QWidget):
    """
    It's the main container,
    that will show the TopBar and Content.

    > layout: `VBox`
    params:
    - parent: QMainWindow
    - channels: dict

    > ``channels`` must to be returned by the Model.get_channel()
    """

    def __init__(self, parent: QMainWindow, channels: dict, path) -> None:
        """Inits `Container`."""
        super().__init__(parent)

        # Channel param
        self.channels = channels
        """Defines channels to be loaded."""
        self.mainWin = parent
        """Get the `src.Window` instance."""
        self.path = path
        """Gets the Application Path `src.Window.path`."""

        # Init layout
        self.layout = QVBoxLayout(self)
        """Sets layout to QVBox."""

        # Configuring
        self.config_layout()
        self.add_widgets()

    def config_layout(self):
        """Configuring layout."""
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addStretch(1)

    def add_widgets(self):
        """Adding content."""
        self.layout.addWidget(TopBar(self, self.mainWin), Qt.AlignTop)
        self.layout.addWidget(
            Content(self, self.mainWin, self.channels, self.path), Qt.AlignTop
        )
