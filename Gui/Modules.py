from collections import deque
import numpy as np
from PyQt6 import QtWidgets, QtCore, QtGui


class ImageViewer(QtWidgets.QLabel):
    def __init__(self, parent, frame: tuple):
        super().__init__(parent)
        self.setFrameShape(frame[0])
        self.setLineWidth(frame[1])
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def set_image(self, image: np.ndarray):
        if len(image.shape) == 3:
            self._display_colored(image)
        else:
            self._display_gray(image)

    def _display_colored(self, image: np.ndarray):
        height, width = image.shape[0], image.shape[1]
        qimage = QtGui.QImage(np.require(image, np.uint8, 'C').data, width, height, 3 * width,
                              QtGui.QImage.Format.Format_RGB888)
        self.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.width() * 0.9),
                                                   int(self.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def _display_gray(self, image: np.ndarray):
        height, width = image.shape[0], image.shape[1]
        qimage = QtGui.QImage(np.require(image, np.uint8, 'C').data, width, height, 1 * width,
                              QtGui.QImage.Format.Format_Grayscale8)
        self.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.width() * 0.9),
                                                   int(self.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))


class Error(QtWidgets.QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)

    def error(self, message):
        self.setWindowTitle("Error")
        self.setText(message)
        self.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        self.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self.exec()


class State(deque):
    def __init__(self, max_len: int):
        super().__init__(maxlen=max_len)
        self.idx = 0

    def reset(self):
        self.clear()
        self.idx = 0

    def add_state(self, s):
        while self.idx < self.__len__():
            self.pop()
        self.append(s)
        self.idx = min(self.idx + 1, self.__len__())

    def get_state(self):
        return self.__getitem__(self.idx - 1)

    def redo(self):
        self.idx = min(self.idx + 1, self.__len__())
        return self.__getitem__(self.idx - 1)

    def undo(self):
        self.idx = max(self.idx - 1, 1)
        return self.__getitem__(self.idx - 1)
