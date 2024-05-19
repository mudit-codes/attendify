import os
import cv2
import sys
import numpy as np

sys.path.append(".")

from PyQt5.QtCore import QObject, pyqtSignal, QBasicTimer


class VideoRecorder(QObject):
    imageData = pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QBasicTimer()

    def startRecording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if event.timerId() != self.timer.timerId():
            return

        read, image = self.camera.read()
        if read:
            self.imageData.emit(image)
