from PyQt6 import QtWidgets, QtGui, QtCore

from Core import File, Color, Misc, Enhancement

MAX_DITHER_LEVEL = 5


# noinspection PyUnresolvedReferences
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 615)
        self.installEventFilter(self)

        self._create_menubar()
        self._create_central()

        self.raw_img = None
        self.gray_img = None

        self.show()
        self._open_file()
        self._blur()

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
            self.raw_img, height, width = File.open_image(file_name)
            qimage = QtGui.QImage(self.raw_img, width, height, 3 * width, QtGui.QImage.Format.Format_RGB888)

            self.image_viewer.setPixmap(
                QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
                                                       int(self.image_viewer.height() * 0.9),
                                                       aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                       transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))
            self.image_thumbnail.setPixmap(
                QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_thumbnail.width() * 0.9),
                                                       int(self.image_thumbnail.height() * 0.9),
                                                       aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                       transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    # def _handle_colored_op(self, f):
    #     self._clear_layout(self.controllers_layout)
    #
    #     result, height, width = f(self.raw_img)
    #     qimage = QtGui.QImage(result, width, height, 3 * width, QtGui.QImage.Format.Format_RGB888)
    #     self.image_viewer.setPixmap(
    #         QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
    #                                                int(self.image_viewer.height() * 0.9),
    #                                                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
    #                                                transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))
    #
    # def _handle_gray_op(self, f):
    #     self._clear_layout(self.controllers_layout)
    #
    #     if not self.gray_img:
    #         self.gray_img, _, _ = Color.convert_to_grayscale(self.raw_img)
    #     result, height, width = f(self.gray_img)
    #     qimage = QtGui.QImage(result, width, height, 1 * width, QtGui.QImage.Format.Format_Grayscale8)
    #     self.image_viewer.setPixmap(
    #         QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
    #                                                int(self.image_viewer.height() * 0.9),
    #                                                aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
    #                                                transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def _grayscale(self):
        self._clear_layout(self.controllers_layout)

        self.gray_img, height, width = Color.convert_to_grayscale(self.raw_img)
        qimage = QtGui.QImage(self.gray_img, width, height, 1 * width, QtGui.QImage.Format.Format_Grayscale8)

        self.image_viewer.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
                                                   int(self.image_viewer.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def _auto_level(self):
        self._clear_layout(self.controllers_layout)

        leveled, height, width = Enhancement.auto_level(self.raw_img)
        qimage = QtGui.QImage(leveled, width, height, 3 * width, QtGui.QImage.Format.Format_RGB888)

        self.image_viewer.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
                                                   int(self.image_viewer.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def _hist_equal(self):
        self._clear_layout(self.controllers_layout)

        leveled, height, width = Enhancement.histogram_equalization(self.raw_img)
        qimage = QtGui.QImage(leveled, width, height, 3 * width, QtGui.QImage.Format.Format_RGB888)

        self.image_viewer.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
                                                   int(self.image_viewer.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def _blur(self):
        self._clear_layout(self.controllers_layout)

        if not self.gray_img:
            self.gray_img, _, _ = Color.convert_to_grayscale(self.raw_img)
        leveled, height, width = Misc.blur(self.raw_img)
        qimage = QtGui.QImage(leveled, width, height, 3 * width, QtGui.QImage.Format.Format_RGB888)

        self.image_viewer.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
                                                   int(self.image_viewer.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def dummy(self, a):
        print(a)

    def _dithering(self):
        def perform(level):
            if not self.gray_img:
                self.gray_img, _, _ = Color.convert_to_grayscale(self.raw_img)
            dithered, height, width = Misc.ordered_dither(self.gray_img, level)
            qimage = QtGui.QImage(dithered, width, height, 1 * width, QtGui.QImage.Format.Format_Grayscale8)

            self.image_viewer.setPixmap(
                QtGui.QPixmap.fromImage(qimage).scaled(int(self.image_viewer.width() * 0.9),
                                                       int(self.image_viewer.height() * 0.9),
                                                       aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                       transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))
            self.terminal.setText(f"Dithering level {level}")

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
        self._clear_layout(self.controllers_layout)

        if not self.gray_img:
            self.gray_img, _, _ = Color.convert_to_grayscale(self.raw_img)
        entropy, code_len = Misc.huffman_encode(self.gray_img)
        self.terminal.setText(f"Entropy: {entropy:.3f}\nAverage Huffman Code Length: {code_len:.3f}")

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
