#-- importing Qt modules
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


#-- Widget Button
class AddBtn(QPushButton):
    """It's the blue button on Bottom Right Conner
    
    When clicked, it'll open the `src.channel.ChannelDialog` Window
    """

    #-- Init
    def __init__(self, parent, mainWin):
        # parent = Container(QWidget)
        super().__init__(parent)

        #-- class' variable
        self.mainWin = mainWin
        """It's the `src.Window` instance"""
        
        #-- Configuring
        self.config()
        #-- Action
        self.action()


    #-- Configuring
    def config(self):
        """It'll configure the button"""
        self.setText("+")
        self.setGeometry(740, 450, 50, 50)
        self.setStyleSheet(
            """
            color: #fff; background-color: #448aff;
            """)
        self.setCursor(QCursor(Qt.PointingHandCursor))


    #-- Action
    def action(self):
        """Defines the button act: create a `src.ui.channel.ChannelDialog`"""
        self.clicked.connect(self.mainWin.channelDialog)
