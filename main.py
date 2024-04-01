import sys
from PyQt6 import QtWidgets

from Core import FunctionHandler
from Gui import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MyMainWindow(FunctionHandler.Handler())
    sys.exit(app.exec())
