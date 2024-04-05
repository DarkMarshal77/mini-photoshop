from PyQt6 import QtWidgets, QtGui, QtCore

from Core import File, Color, Misc, Enhancement
from Gui import Modules

MAX_DITHER_LEVEL = 5


# noinspection PyUnresolvedReferences
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 615)
        self.installEventFilter(self)

        self.raw_img = None
        self.gray_img = None
        self.error_handler = Modules.Error(self)
        self.image_viewer = Modules.ImageViewer(self, (QtWidgets.QFrame.Shape.Box, 4))
        self.image_thumbnail = Modules.ImageViewer(self, (QtWidgets.QFrame.Shape.StyledPanel, 0))

        self._create_menubar()
        self._create_central()

        self.show()
        self._open_file()
        self._auto_level()
        self._hist_equal()

    def _create_central(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        central_layout = QtWidgets.QVBoxLayout(central_widget)

        # create top widget
        top_widget = QtWidgets.QWidget(self)
        top_layout = QtWidgets.QHBoxLayout(top_widget)
        top_layout.addWidget(self.image_viewer, stretch=5)
        top_layout.addWidget(self._add_side_panel(), stretch=1)

        central_layout.addWidget(top_widget, stretch=4)
        central_layout.addWidget(self._add_terminal(), stretch=1)

    def _add_side_panel(self):
        side_widget = QtWidgets.QWidget(self)
        side_layout = QtWidgets.QVBoxLayout(side_widget)

        # thumbnail
        side_layout.addWidget(self.image_thumbnail, stretch=1)

        # controls
        controllers = QtWidgets.QWidget(self)
        self.controllers_layout = QtWidgets.QGridLayout(controllers)
        side_layout.addWidget(controllers, stretch=4)

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
        menuCore_Operations.addAction(QtGui.QAction('&Grayscale', self, triggered=self._grayscale))
        menuCore_Operations.addAction(QtGui.QAction('Ordered &Dithering', self, triggered=self._dithering))
        menuCore_Operations.addAction(QtGui.QAction('&Auto Leveling', self, triggered=self._auto_level))
        menuCore_Operations.addSeparator()
        menuCore_Operations.addAction(QtGui.QAction('&Huffman', self, triggered=self._huffman))
        menuCore_Operations.addSeparator()
        menuCore_Operations.addAction(QtGui.QAction('&Exit', self, triggered=self.close))

        menuOptional_Operations = menubar.addMenu('&Optional Operations')
        menuOptional_Operations.addAction(QtGui.QAction('&Histogram Equalization', self, triggered=self._hist_equal))
        menuOptional_Operations.addAction(QtGui.QAction('&Blur', self, triggered=self._blur))
        menuOptional_Operations.addAction(QtGui.QAction('&dummy', self, triggered=lambda: self.dummy(4)))
        menuOptional_Operations.addSeparator()

    def _clear_layout(self, layout: QtWidgets.QLayout):
        while layout.count():
            c = layout.takeAt(0)
            if c.widget():
                layout.removeWidget(c.widget())
            elif c.layout():
                self._clear_layout(c.layout())
            else:
                assert c.spacerItem()
                layout.removeItem(c.spacerItem())

    def _open_file(self):
        self._clear_layout(self.controllers_layout)
        # file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open BMP File", "",
        #                                                      "BMP Files (*.bmp);;All Files (*)")
        file_name = "input/image1.bmp"
        if file_name:
            self.gray_img = None
            self.raw_img = File.open_image(file_name)

            self.image_viewer.display_colored(self.raw_img)
            self.image_thumbnail.display_colored(self.raw_img)

    def _auto_level(self):
        if self.raw_img is not None:
            self._clear_layout(self.controllers_layout)
            self.image_viewer.display_colored(Enhancement.auto_level(self.raw_img))
        else:
            self.error_handler.error("Please choose an image first!")

    def _hist_equal(self):
        if self.raw_img is not None:
            self._clear_layout(self.controllers_layout)
            self.image_viewer.display_colored(Enhancement.histogram_equalization(self.raw_img))
        else:
            self.error_handler.error("Please choose an image first!")

    def _grayscale(self):
        if self.raw_img is not None:
            self._clear_layout(self.controllers_layout)
            self.gray_img = Color.convert_to_grayscale(self.raw_img)
            self.image_viewer.display_gray(self.gray_img)
        else:
            self.error_handler.error("Please choose an image first!")

    def _blur(self):
        if self.gray_img is not None:
            self._clear_layout(self.controllers_layout)
            self.image_viewer.display_gray(Misc.blur(self.gray_img))
        else:
            self.error_handler.error("Please produce gray image first!")

    def _dithering(self):
        def perform(level):
            if self.gray_img is not None:
                self.image_viewer.display_gray(Misc.ordered_dither(self.gray_img, level))
                self.terminal.setText(f"Dithering level {level}")
            else:
                self.error_handler.error("Please produce gray image first!")

        self._clear_layout(self.controllers_layout)

        # Create a slider widget
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        slider.setRange(1, MAX_DITHER_LEVEL)
        slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(1)

        # Create a horizontal layout for the tick value labels
        ticks_layout = QtWidgets.QHBoxLayout()
        for i in range(1, MAX_DITHER_LEVEL + 1):
            label = QtWidgets.QLabel(str(i))
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align text
            ticks_layout.addWidget(label, stretch=1)

        # Create a button widget
        button = QtWidgets.QPushButton('Click Me')
        button.clicked.connect(lambda: perform(slider.value()))

        # spacer
        verticalSpacer = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Expanding)

        # Add the slider and button to the grid layout
        self.controllers_layout.addWidget(slider, 0, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addLayout(ticks_layout, 1, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addWidget(button, 2, 0)  # Add button at row 1, column 0
        self.controllers_layout.addItem(verticalSpacer)

    def _huffman(self):
        if self.gray_img is not None:
            self._clear_layout(self.controllers_layout)
            entropy, code_len = Misc.huffman_encode(self.gray_img)
            self.terminal.setText(f"Entropy: {entropy:.3f}\nAverage Huffman Code Length: {code_len:.3f}")
        else:
            self.error_handler.error("Please produce gray image first!")

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.Resize:
            self.image_viewer.setPixmap(
                self.image_viewer.pixmap().scaled(
                    int(self.image_viewer.width() * 0.9), int(self.image_viewer.height() * 0.9),
                    aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))
            self.image_thumbnail.setPixmap(
                self.image_thumbnail.pixmap().scaled(
                    int(self.image_thumbnail.width() * 0.9), int(self.image_thumbnail.height() * 0.9),
                    aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        return super().eventFilter(obj, event)
