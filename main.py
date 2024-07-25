import sys
import os
from PyQt6 import QtWidgets,QtGui
from template.m2 import Ui_mainWindow

if __name__ == "__main__":
    iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "./images/avatar/head.ico"))
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(iconPath))
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())
