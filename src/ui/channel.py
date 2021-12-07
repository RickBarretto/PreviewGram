#-- importing Qt modules
from PySide6.QtWidgets import (
    QComboBox, QFormLayout,
    QLabel, QScrollArea,
    QStackedLayout, QVBoxLayout,
    QWidget, QPushButton,
    QDialog, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

#-- importing functools to partial connect
from functools import partial


#-- Update Page

class Update(QWidget):

    """Update channels Page."""

    #-- Initing
    def __init__(self, parent, mainWin):
        """Inits `Update`."""
        super().__init__(parent)

        #-- class' variables
        self.mainWin = mainWin
        """Is the `src.Window`."""
        self.chan = QLineEdit()
        """It's the channel's name input."""
        self.url = QLineEdit()
        """It's the channel's url input."""
        self.submitBtn = QPushButton("Submit")
        """It's the submit button."""

        self.layout = QFormLayout(self)
        """Configures the layout as QForm."""

        #-- Configuring
        self.input_config()
        self.config_layout()

        #-- Setting action
        self.action()


    #-- Config
    def input_config(self):
        """Configures inputs (`Update.chan`, `Update.url`) max length."""
        self.chan.setMaxLength(20)
        self.url.setMaxLength(256)

    def config_layout(self):
        """Adds widgets to `Update.layout`."""
        self.layout.addRow("Channel:", self.chan)
        self.layout.addRow("Url:", self.url)
        self.layout.addRow(self.submitBtn)
        self.layout.addRow(QLabel("Close this window to update!"))


    #-- Action
    def action(self):
        """Sends the inputs' text to `src.Window.check`."""
        self.submitBtn.clicked.connect(
            lambda: self.mainWin.check(self.chan.text(), self.url.text())
            )


#-- Remove Page

class Remove(QWidget):
    """Remove channels Page."""

    def __init__(self, parent, mainWin):
        """Inits `Remove`."""
        super().__init__(parent)

        #-- class's variables
        self.mainWin = mainWin
        """Is the `src.Window`."""

        self.channels = self.load_channels()
        """Updates and loads `src.Window.channels`."""

        #-- class' widgets variables
        self.layout = QVBoxLayout(self)
        """`Remove`'s layout."""
        self.wid = QWidget()
        """Main `Remove`'s widget."""
        self.wid_layout = QVBoxLayout()
        """`wid`'s layout."""
        self.scroll = QScrollArea()
        """`Remove`'s Scroll Area."""

        #-- generating layout
        self.gen_layout()
        self.wid.setLayout(self.wid_layout)

        #-- confinguring layout
        self.config_scroll()
        self.config_layout()
        self.layout.addWidget(self.scroll)


    #-- loading channels
    def load_channels(self):
        """Loads channels from database to `channels`."""
        self.mainWin.get_channels()
        """Updates the `src.Window.channels` from database."""
        channels = self.mainWin.channels
        """Loads the channels dict" from `src.Window.channels`."""
        return channels

    #-- generating layout
    def config_scroll(self):
        """Configures the Scroll Area."""
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.wid)

    def config_layout(self):
        """Configures the layout."""
        self.wid_layout.addStretch()

    #-- Generating and setting action
    def gen_layout(self):
        """
        Generates the widget layout.

        The buttons connects to `src.Window.delete_chan` and later to `destroy_self`.
        """
        for chan in self.channels:

            btn = QPushButton("Delete "+chan, self)
            btn.setMaximumHeight(300)
            btn.setMinimumHeight(50)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(partial(self.mainWin.delete_chan, chan))
            btn.clicked.connect(partial(self.destroy_self, btn))
            self.wid_layout.addWidget(btn, Qt.AlignBottom)

    #-- Action
    def destroy_self(btn):
        """Disable Button."""
        btn.setEnabled(False)



#-- Channel Dialog Window

class ChannelDialog(QDialog):
    """It's a Dialog Window to dial with database."""

    def __init__(self, parent):
        """Inits `ChannelDialog`."""
        super().__init__(parent)

        #-- class' variables
        self.mainWin = parent
        """It's the `src.Window` instance."""

        #-- WARNING! Important attribute
        self.config_att()

        #-- Configuring layout
        self.layout = QVBoxLayout(self)
        self.pageCombo = QComboBox()
        self.stackedLayout = QStackedLayout()

        #-- Sets widgets layout
        self.ui()


    def ui(self):
        """Configures UI components."""
        self.setWindowTitle("Channels")
        self.setSizeGripEnabled(True)
        self.combo_page()
        self.stacked_layout()
        self.layout.addWidget(self.pageCombo)
        self.layout.addLayout(self.stackedLayout)

    #-- WARNING: Important Attribute
    def config_att(self):
        """
        WARNING: don't remove it!

        Without it, the Application won't restart.
        """
        self.setAttribute(Qt.WA_DeleteOnClose, True)

    #-- Layouts
    def combo_page(self):
        """Create the Switch Button."""
        self.pageCombo.addItems(["Add", "Delete"])
        self.pageCombo.activated.connect(self.switch_page)


    def stacked_layout(self):
        """Create the Pagination layout."""
        self.stackedLayout.addWidget(Update(self, self.mainWin))
        self.stackedLayout.addWidget(Remove(self, self.mainWin))

    #-- Action
    def switch_page(self):
        """Changes the Page."""
        self.stackedLayout.setCurrentIndex(self.pageCombo.currentIndex())


