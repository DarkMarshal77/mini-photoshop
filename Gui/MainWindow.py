from PyQt6 import QtWidgets, QtGui, QtCore

from Core import File, Color, Misc, Enhancement, Geometry
from Gui import Modules

MAX_DITHER_LEVEL = 5
MAX_FILTER_DEGREE = 5


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
        self._grayscale()

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
        menuOptional_Operations.addAction(QtGui.QAction('&Blur', self, triggered=self._blur))
        menuOptional_Operations.addAction(QtGui.QAction('&Histogram Equalization', self, triggered=self._hist_equal))
        menuOptional_Operations.addSeparator()
        menuOptional_Operations.addAction(QtGui.QAction('&Adjust Brightness', self, triggered=self._brightness))
        menuOptional_Operations.addAction(QtGui.QAction('&Adjust Contrast', self, triggered=self._contrast))
        menuOptional_Operations.addAction(QtGui.QAction('&Adjust Color', self, triggered=self._color_balance))
        menuOptional_Operations.addSeparator()
        menuFlip = menuOptional_Operations.addMenu('&Rotate')
        menuFlip.addAction(QtGui.QAction('90 Clockwise', self, triggered=lambda: self._rot(True)))
        menuFlip.addAction(QtGui.QAction('90 Counter-Clockwise', self, triggered=lambda: self._rot(False)))
        menuFlip = menuOptional_Operations.addMenu('&Flip')
        menuFlip.addAction(QtGui.QAction('&Vertical', self, triggered=lambda: self._flip(True)))
        menuFlip.addAction(QtGui.QAction('&Harizontal', self, triggered=lambda: self._flip(False)))

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
        file_name = "input/image2.bmp"
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

    def _blur(self):
        def perform(degree):
            if self.raw_img is not None:
                self.image_viewer.display_colored(Misc.blur(self.raw_img, degree))
                self.terminal.setText(f"Blur degree {degree // 2}")
            else:
                self.error_handler.error("Please choose an image first!")

        self._clear_layout(self.controllers_layout)

        # Create a slider widget
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        slider.setRange(1, MAX_FILTER_DEGREE)
        slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(1)
        slider.setValue(MAX_FILTER_DEGREE // 2 + 1)

        # Create a horizontal layout for the tick value labels
        ticks_layout = QtWidgets.QHBoxLayout()
        for i in range(1, MAX_FILTER_DEGREE + 1):
            label = QtWidgets.QLabel(str(i))
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align text
            ticks_layout.addWidget(label, stretch=1)

        # Create a button widget
        button = QtWidgets.QPushButton('OK')
        button.clicked.connect(lambda: perform(slider.value() * 2 + 1))

        # spacer
        verticalSpacer = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Expanding)

        # Add the slider and button to the grid layout
        self.controllers_layout.addWidget(slider, 0, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addLayout(ticks_layout, 1, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addWidget(button, 2, 0)  # Add button at row 1, column 0
        self.controllers_layout.addItem(verticalSpacer)

    def _brightness(self):
        def perform(factor):
            if self.raw_img is not None:
                self.image_viewer.display_colored(Color.adjust_brightness(self.raw_img, factor))
            else:
                self.error_handler.error("Please choose an image first!")

        self._clear_layout(self.controllers_layout)

        # Create a slider widget
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        slider.setRange(0, 200)
        slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(50)
        slider.setValue(100)

        # Create a horizontal layout for the tick value labels
        ticks_layout = QtWidgets.QHBoxLayout()
        for i in range(-100, 101, 100):
            label = QtWidgets.QLabel(f'{i}%')
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align text
            ticks_layout.addWidget(label, stretch=1)

        # Create a button widget
        button = QtWidgets.QPushButton('OK')
        button.clicked.connect(lambda: perform(slider.value() / 100))

        # spacer
        verticalSpacer = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Expanding)

        # Add the slider and button to the grid layout
        self.controllers_layout.addWidget(slider, 0, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addLayout(ticks_layout, 1, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addWidget(button, 2, 0)  # Add button at row 1, column 0
        self.controllers_layout.addItem(verticalSpacer)

    def _contrast(self):
        def perform(factor):
            if self.raw_img is not None:
                self.image_viewer.display_colored(Color.adjust_contrast(self.raw_img, factor))
            else:
                self.error_handler.error("Please choose an image first!")

        self._clear_layout(self.controllers_layout)

        # Create a slider widget
        slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        slider.setRange(0, 200)
        slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        slider.setTickInterval(50)
        slider.setValue(100)

        # Create a horizontal layout for the tick value labels
        ticks_layout = QtWidgets.QHBoxLayout()
        for i in range(-100, 101, 100):
            label = QtWidgets.QLabel(f'{i}%')
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align text
            ticks_layout.addWidget(label, stretch=1)

        # Create a button widget
        button = QtWidgets.QPushButton('OK')
        button.clicked.connect(lambda: perform(slider.value() / 100))

        # spacer
        verticalSpacer = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Expanding)

        # Add the slider and button to the grid layout
        self.controllers_layout.addWidget(slider, 0, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addLayout(ticks_layout, 1, 0)  # Add slider at row 0, column 0
        self.controllers_layout.addWidget(button, 2, 0)  # Add button at row 1, column 0
        self.controllers_layout.addItem(verticalSpacer)

    def _color_balance(self):
        def perform(r, g, b):
            if self.raw_img is not None:
                self.image_viewer.display_colored(Color.adjust_color_balance(self.raw_img, r, g, b))
            else:
                self.error_handler.error("Please choose an image first!")

        self._clear_layout(self.controllers_layout)

        # Create a slider widget
        sliders, ticks_layouts, labels = [], [], ['R', 'G', 'B']
        for _ in range(3):
            sliders.append(QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self))
            sliders[-1].setRange(0, 200)
            sliders[-1].setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
            sliders[-1].setTickInterval(50)
            sliders[-1].setValue(100)

            # Create a horizontal layout for the tick value labels
            ticks_layouts.append(QtWidgets.QHBoxLayout())
            for i in range(-100, 101, 100):
                label = QtWidgets.QLabel(f'{i}%')
                label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align text
                ticks_layouts[-1].addWidget(label, stretch=1)

        # Create a button widget
        button = QtWidgets.QPushButton('OK')
        button.clicked.connect(lambda: perform(*tuple([s.value() / 100 for s in sliders])))

        # spacer
        verticalSpacer = QtWidgets.QSpacerItem(20, 220, QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Expanding)

        # Add the sliders and button to the grid layout
        for i in range(3):
            self.controllers_layout.addWidget(QtWidgets.QLabel(labels[i]), i * 2, 0)
            self.controllers_layout.addWidget(sliders[i], i * 2, 1)
            self.controllers_layout.addLayout(ticks_layouts[i], i * 2 + 1, 1)
        self.controllers_layout.addWidget(button, 6, 0, 1, 0)
        self.controllers_layout.addItem(verticalSpacer)

    def _rot(self, clockwise: bool):
        if self.raw_img is not None:
            self._clear_layout(self.controllers_layout)
            self.image_viewer.display_colored(Geometry.rotate(self.raw_img, clockwise))
        else:
            self.error_handler.error("Please choose an image first!")

    def _flip(self, v: bool):
        if self.raw_img is not None:
            self._clear_layout(self.controllers_layout)
            self.image_viewer.display_colored(Geometry.flip(self.raw_img, v))
        else:
            self.error_handler.error("Please choose an image first!")

    def _grayscale(self):
        if self.raw_img is not None:
            self._clear_layout(self.controllers_layout)
            self.gray_img = Color.convert_to_grayscale(self.raw_img)
            self.image_viewer.display_gray(self.gray_img)
        else:
            self.error_handler.error("Please choose an image first!")

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
        slider.setValue(4)

        # Create a horizontal layout for the tick value labels
        ticks_layout = QtWidgets.QHBoxLayout()
        for i in range(1, MAX_DITHER_LEVEL + 1):
            label = QtWidgets.QLabel(str(i))
            label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align text
            ticks_layout.addWidget(label, stretch=1)

        # Create a button widget
        button = QtWidgets.QPushButton('OK')
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
