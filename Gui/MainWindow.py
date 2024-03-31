import sys

from PyQt6 import QtWidgets, QtGui, QtCore


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 615)

        self._create_menubar()
        self._create_central()

        self.image_path = ""

        self.show()

    def _create_central(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QtWidgets.QVBoxLayout(central_widget)

        # create top widget
        top_widget = QtWidgets.QWidget(self)
        top_layout = QtWidgets.QHBoxLayout(top_widget)
        top_layout.addWidget(self._add_image_viewer(), stretch=5)
        top_layout.addWidget(self._add_side_panel(), stretch=1)

        central_layout.addWidget(top_widget, stretch=4)
        central_layout.addWidget(self._add_terminal(), stretch=1)

    def _add_image_viewer(self):
        self.image_viewer = QtWidgets.QLabel(self)
        self.image_viewer.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.image_viewer.setLineWidth(4)
        self.image_viewer.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        return self.image_viewer

    def _add_side_panel(self):
        side_widget = QtWidgets.QWidget(self)
        side_layout = QtWidgets.QVBoxLayout(side_widget)

        # thumbnail
        self.image_thumbnail = QtWidgets.QLabel(self)
        self.image_thumbnail.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        # self.image_thumbnail.setLineWidth(10)
        self.image_thumbnail.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        side_layout.addWidget(self.image_thumbnail, stretch=1)

        # controls
        self.controllers = QtWidgets.QWidget(self)
        side_layout.addWidget(self.controllers, stretch=4)

        return side_widget

    def _add_terminal(self):
        # Create a label for displaying messages
        self.terminal = QtWidgets.QLabel("", self)
        self.terminal.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.terminal.setLineWidth(10)
        self.terminal.setStyleSheet("""
                            QLabel {
                                font-family: 'Courier New', monospace;
                                font-size: 12px;
                                background-color: #1E1E1E;
                                color: #D4D4D4;
                                padding: 5px;
                            }
                        """)
        return self.terminal

    def _create_menubar(self):
        menubar = self.menuBar()

        menuCore_Operations = menubar.addMenu('&Core Operations')
        menuCore_Operations.addAction(QtGui.QAction('&Open File', self, triggered=self._open_file))
        menuCore_Operations.addSeparator()
        menuCore_Operations.addAction(QtGui.QAction('&Grayscale', self, triggered=self._open_file))
        menuCore_Operations.addAction(QtGui.QAction('Ordered &Dithering', self, triggered=self._open_file))
        menuCore_Operations.addAction(QtGui.QAction('&Auto Leveling', self, triggered=self._open_file))
        menuCore_Operations.addSeparator()
        menuCore_Operations.addAction(QtGui.QAction('&Huffman', self, triggered=self._open_file))
        menuCore_Operations.addSeparator()
        menuCore_Operations.addAction(QtGui.QAction('&Exit', self, triggered=self.close))

        menuOptional_Operations = menubar.addMenu('&Optional Operations')

    def _open_file(self):
        # Handle the file opening logic here
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open BMP File", "",
                                                             "BMP Files (*.bmp);;All Files (*)")
        if file_name:
            self.image_path = file_name
            self.terminal.setText(file_name)
            pixmap = QtGui.QPixmap(file_name)
            self.image_viewer.setPixmap(
                pixmap.scaled(self.image_viewer.size(), aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.image_thumbnail.setPixmap(
                pixmap.scaled(self.image_thumbnail.size(), aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec())
