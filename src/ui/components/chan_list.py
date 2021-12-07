#-- importing Qt modules
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QScrollArea)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt

#-- importing functools to partial connect
from functools import partial


#-- ChannelList Widget (SideBar)

class ChannelList(QWidget):
    
    """
    It's the application SideBar,
    that will load the channel List,
    creating buttons to change the `src.ui.components.engine.Engine` current url.
    """
    #-- Init
    def __init__(self, parent, channels:dict) -> None:
        """Inits `ChannelList`."""
        super().__init__(parent)

        #-- class' variables
        self.channels = channels
        """It's the channel list loaded from `src.Window.channels`."""
        self.parent = parent
        """It's the `src.Window` instance."""

        #-- class' widgets variables
        self.layout = QVBoxLayout(self)
        """`ChannelList`'s Layout as QHBox."""
        self.wid = QWidget()
        """`ChannelList`'s main Widget."""
        self.wid_layout = QVBoxLayout()
        """`wid`'s layout as QVBox."""
        self.scroll = QScrollArea()
        """Scroll Area."""

        #-- generating layout
        self.gen_buttons()
        self.wid.setLayout(self.wid_layout)

        #-- configuring layout
        self.config_scroll()
        self.config_layout()
        self.layout.addWidget(self.scroll)


    def config_scroll(self):
        """Configures the Scroll Area."""
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.wid)

    def config_layout(self):
        """Configures the layout."""
        self.wid_layout.addStretch()

    def __gen_fixed_buttons(self):
        """
        The first button: "Test privacy" opens https://www.whatismybrowser.com/.

        The second button: "Official Channel" opens https://t.me/s/previewgram.
        """
        btn_test = QPushButton("Test privacy!", self)
        btn_test.setMaximumHeight(300)
        btn_test.setMinimumHeight(50)
        btn_test.setStyleSheet("background-color: #448aff; color: #fff")
        btn_test.setCursor(QCursor(Qt.PointingHandCursor))
        btn_test.clicked.connect(partial(self.parent.open_url, "https://www.whatismybrowser.com/"))

        official_channel = QPushButton("Official Channel", self)
        official_channel.setMaximumHeight(300)
        official_channel.setMinimumHeight(50)
        official_channel.setStyleSheet("background-color: #448aff; color: #fff")
        official_channel.setCursor(QCursor(Qt.PointingHandCursor))
        official_channel.clicked.connect(partial(self.parent.open_url, "https://t.me/s/previewgram"))

        self.wid_layout.addWidget(btn_test, Qt.AlignBottom)
        self.wid_layout.addWidget(official_channel, Qt.AlignBottom)

    def gen_buttons(self):
        """Generates the Dynamic buttons and fixed buttons."""
        self.__gen_fixed_buttons()

        for chan in self.channels:

            btn = QPushButton(chan, self)
            btn.setMaximumHeight(300)
            btn.setMinimumHeight(50)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(partial(self.parent.open_url, self.channels[chan]))
            self.wid_layout.addWidget(btn, Qt.AlignBottom)