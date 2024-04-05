from PyQt6 import QtWidgets, QtCore, QtGui
import numpy as np


class ImageViewer(QtWidgets.QLabel):
    def __init__(self, parent, frame: tuple):
        super().__init__(parent)
        self.setFrameShape(frame[0])
        self.setLineWidth(frame[1])
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def display_colored(self, image: np.ndarray):
        height, width = image.shape[0], image.shape[1]
        qimage = QtGui.QImage(np.require(image, np.uint8, 'C').data, width, height, 3 * width,
                              QtGui.QImage.Format.Format_RGB888)
        self.setPixmap(
            QtGui.QPixmap.fromImage(qimage).scaled(int(self.width() * 0.9),
                                                   int(self.height() * 0.9),
                                                   aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                   transformMode=QtCore.Qt.TransformationMode.SmoothTransformation))

    def display_gray(self, image: np.ndarray):
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
