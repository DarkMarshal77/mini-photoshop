import sys
from PyQt6 import QtWidgets

from Gui import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow.MyMainWindow()
    sys.exit(app.exec())
