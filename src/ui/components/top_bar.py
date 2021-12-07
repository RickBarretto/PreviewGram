#-- importing system modules
import os, sys

#-- importing Qt modules
from PySide6.QtWidgets import (
    QLabel, QWidget, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


#-- Sets Title

class Title(QLabel):
    """Sets the Title."""

    #-- Init
    def __init__(self) -> None:
        """Inits `Title`."""
        super().__init__()
        self.size = 35
        self.setText("Private Previewgram")
        self.config()


    #-- Configuring
    def config(self):
        """Configures the `Title`."""
        self.setFixedHeight(35)
        self.setAlignment(Qt.AlignCenter)


#-- Sets Open on Github Button

class Github(QPushButton):
    """
    Creates a 'open Repository' Button.

    it'll open on <a href="https://github.com/RickBarretto/PreviewGram">GitHub</a>.
    """

    #-- Init
    def __init__(self) -> None:
        """Inits `Github`."""
        super().__init__()

        self.config()
        self.action()

    #-- Configuring
    def config(self):
        """Configures the `Github` button."""
        self.setText('Visit Us on Github!')
        self.setStyleSheet(
            "border: none;"+
            "background-color: #448aff; color: #fff;"+
            "padding: 0; margin: 0 36px 0 0;"
            )
        self.setCursor(QCursor(Qt.PointingHandCursor))


    #-- Action
    def action(self):
        """
        When clicked,
        Opens <a href="https://github.com/RickBarretto/PreviewGram">Github link</a>
        on system default browser.
        """
        self.clicked.connect(self.__openGithub)

    def __openGithub(self):
        """
        Opens <a href="https://github.com/RickBarretto/PreviewGram">Github link</a>
        on system default browser.
        """
        repo_link = "https://github.com/RickBarretto/PreviewGram"
        command = "explorer "+repo_link
        if sys.platform == "MacOSX":
            command = "open "+repo_link
        os.system(command)


#-- Sets the Close Window Button

class CloseBtn(QPushButton):
    """Closes the `Window` and ends the application."""

    #-- Init
    def __init__(self, mainWin) -> None:
        """Inits `Github`."""
        super().__init__()

        #-- class' variables
        self.mainWin = mainWin
        """`src.Window` instance."""
        self.size = 35
        """size to be configured."""

        self.config()
        self.action()


    #-- Configuring
    def config(self):
        """Configuring `CloseBtn`."""
        self.setText('X')
        self.setFixedSize(self.size, self.size)
        self.setStyleSheet(
            "background-color: red;"+
            "border: none;"+
            "color: white;"+
            "padding: 0;"+
            "margin: 0")
        self.setCursor(QCursor(Qt.PointingHandCursor))


    #-- Action
    def action(self):
        """Connects to `src.Window.closeWindow` to close Main Window."""
        self.clicked.connect(self.mainWin.closeWindow)


#-- Sets the Minimize Window Button

class MinBtn(QPushButton):
    """Minimize Button: Minimizes the `src.Window` when clicked."""

    #-- Init
    def __init__(self, mainWin) -> None:
        super().__init__()
        self.mainWin = mainWin
        """`src.Window` instance."""
        self.size = 35
        """size to be configured."""

        self.config()
        self.action()


    #-- Configuring
    def config(self):
        """Configuring `MinBtn`."""
        self.setText('_')
        self.setFixedSize(self.size, self.size)
        self.setStyleSheet(
            "border: none;"+
            "background-color: #448aff; color: #fff;"+
            "padding: 0;"+
            "margin: 0")
        self.setCursor(QCursor(Qt.PointingHandCursor))


    #-- Action
    def action(self):
        """Connects to `src.Window.minWindow` to minimize Main Window."""
        self.clicked.connect(self.mainWin.minWindow())



#-- Sets the Window's TopBar

class TopBar(QWidget):
    """
    It will change the default Windows's title bar.

    param:
    - parent: QWidget
    """

    #-- Init
    def __init__(self, parent:QWidget, mainWin) -> None:
        super().__init__(parent)

        self.mainWin = mainWin
        """`src.Window` instance."""

        self.layout = QHBoxLayout(self)
        """Sets layout as QHBox."""

        self.config_widget()
        self.add_widgets()
        self.config_layout()


    #-- Adding Widgets
    def add_widgets(self):
        """Adds Widgets: `Github`, `Title`, `MinBtn` and `CloseBtn`."""
        self.layout.addWidget(Github())
        self.layout.addWidget(Title())
        self.layout.addWidget(MinBtn(self.mainWin))
        self.layout.addWidget(CloseBtn(self.mainWin))


    #-- Configuring
    def config_widget(self):
        """Configures widget."""
        self.setFixedHeight(35)
        self.setWhatsThis("Hello")
        self.setStyleSheet("padding: 0 15px 0 0; margin: 0;")
        self.setContentsMargins(13, 0, 13, 0)

    def config_layout(self):
        """Configures layout."""
        self.layout.setContentsMargins(0, 0, 0, 10)

