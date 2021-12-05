"""
This module is the global module, dealing with submodules as model and ui.
Here is started the application, generating a `Window` (That is the Main Window) and running with `start_app` method. 

The Title Bar and movable Window from: https://stackoverflow.com/a/44249552

The QTTheme from: https://github.com/UN-GCPDS/qt-material

A lot of help was gave by Pinnaculum https://github.com/pinnaculum/

Thank you, yurisnm, UN-GCPDS and Pinnaculum!
"""

VERSION = 1.1

#-- importing system modules
import sys, os

#-- importing Qt modules
from PySide6.QtCore import (
    Qt, QPoint
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow,
    QMessageBox
)
from PySide6.QtGui import QCursor

#-- importing QtMaterial: by https://github.com/UN-GCPDS/qt-material under BSD-2-Clause License
from qt_material import apply_stylesheet

#-- importing application modules
from .model.db import Model
from .ui import *
from .ui.channel import ChannelDialog


#-- Main Window
class Window(QMainWindow):
    """
    It's the Main Window that is a QMainWindow
    """

    #-- init
    def __init__(self):
        super().__init__()

        #-- setting Window's variables
        self.pressing:bool = False
        """Is True when mouse is pressing the Window > for move Window"""
        self.start:QPoint = QPoint(0, 0)
        """Defines the initial Window position > for move Window"""
        self.channels:dict = {}
        """Loads channels from database"""
        self.path:str = str(os.path.dirname(os.path.realpath(__file__)))
        """Defines the current App file"""

        #-- updating channels variable
        self.get_channels()

        #-- Configuring and adding Main Widget to Window
        self.config_win()
        self.add_container()



    #-- Configuring
    def config_win(self):
        """Configures the `Window`"""

        self.setWindowTitle("Private Previewgram")
        self.setFixedWidth(830)
        self.setMinimumHeight(600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        
    def add_container(self):
        """Sets Container from `src.ui` module as Central Widget"""
        container = Container(self, self.channels, self.path)
        self.setCentralWidget(container)



    #-- Database
    def channelDialog(self):
        """Opens a Window Dialog that dials with the database (`src.model.db.Model`), adding and removing users..."""
        dial = ChannelDialog(self)
        dial.destroyed.connect(self.restart)
        dial.exec()

    def get_channels(self):
        """Gets channels fom database (Dialing with `src.model.db.Model`) and Updates Windows's `channels` variable"""
        self.channels = Model.get_channels()

    def add_chan(self, chan, url):
        """Adds channels to database (Dialing with `src.model.db.Model`) and alert the user calling `added_channel`"""
        Model.add_channel(chan, url)
        self.added_channel()

    def delete_chan(self, chan):
        """Deletes channels on database (Dialing with `src.model.db.Model`) and updates `channels` variable"""
        Model.del_channel(chan)
        self.get_channels()



    #-- Database :: checking
    def check(self, chan, url):
        """
        Checks if the user input to add a new channel is correct.

        If yes, it'll call `add_chan`,

        If not, it'll call `wrong_url`, that will show a alert.
        """
        
        if (
            url.startswith("@")
            or url.startswith("https://t.me/")
            or url.startswith("https://telegram.me/")
            ):
            result = True 
            print(result)
            self.add_chan(chan, url)
        else:
            result = False
            print(result)
            self.wrong_url()



    #-- Altering user
    def wrong_url(self):
        """Alerts the user with a `QMessageBox.critical` that the input to add a new channel is invalid"""
        m = QMessageBox.critical(
            self,
            "Use a valid channel url",
            "Examples are:\nhttps://t.me/channel, https://telegram.me/channel, @channel, https://t.me/s/channel",
            buttons=QMessageBox.Close,
            defaultButton=QMessageBox.Close)

    def added_channel(self):
        """Alerts the user with a `QMessageBox.critical` that the input to add a new channel is valid, and the channel was added on database"""
        m = QMessageBox.critical(
            self,
            "Info!",
            "Channel added to database",
            buttons=QMessageBox.Close,
            defaultButton=QMessageBox.Close)



    #-- Updating Window status
    def closeWindow(self):
        """Just close the window"""
        self.close()

    def minWindow(self):
        """Minimizes the window"""
        self.showMinimized()



    #-- Moving Window
    def mousePressEvent(self, event):
        """Wen mouse press the Window, `Window.pressing` is set as True and start is set as Global position based on current mouse position"""
        self.start = self.mapToGlobal(event.position())
        self.pressing = True
        
    def mouseMoveEvent(self, event):
        """
        When mouse is in movement and pressing, it'll set the cursor to `Qt.ClosedHandCursor` and move the window to final position
        
        If mouse is in movement but not pressing, it'll only set the cursor to a `Qt.OpenHandCursor`
        """
        if self.pressing:
            self.setCursor(QCursor(Qt.ClosedHandCursor))
            self.end = self.mapToGlobal(event.position())
            self.movement = self.end-self.start
            self.setGeometry(
                self.mapToGlobal(self.movement).x(),
                self.mapToGlobal(self.movement).y(),
                self.width(), self.height())
            self.start = self.end
        else:
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseReleaseEvent(self, QMouseEvent):
        """When mouse releases, the `Window.pressing` is setting as `False` and the cursor is set as a `Qt.OpenHandCursor`"""
        self.pressing = False
        self.setCursor(QCursor(Qt.OpenHandCursor))



    #-- Restart
    def restart (self):  
        """
        It'll restart the application for update channels on Window.
        
        It'll run when `ui.channel.ChannelDialog` is closed
        """   
        print("closed!")
        open_win()
        self.destroy()



def open_win():
    """
    Will instance and show a new Window
    
    It is used to update channels on ``Window``
    """
    window = Window()
    window.show()  



def start_app():
    """
    Inits the application!

    Applies the theme, Open a Window and executes!
    """

    app = QApplication(sys.argv)        
    apply_stylesheet(app, theme='dark_blue.xml')
    open_win()           
    app.exec()            



if __name__ == '__main__':
    
    start_app()