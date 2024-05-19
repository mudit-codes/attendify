import os
import cv2
import sys
import shutil
from imutils import paths

sys.path.append(".")
sys.path.append("app/widgets")
sys.path.append("app/utils")

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication

import config
from video_recorder import VideoRecorder
from face_detection_widget import FaceDetectionWidget
from face_recognizer.face_encoder import FaceEncoder


class RegisterStudent(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("app/ui/registerStudent.ui", self)
        self.setCentralWidget(self.RegistrationPage)
        self.videoFrame.setVisible(False)

        self.takeImagesBtn.clicked.connect(self.takeImages)
        self.captureBtn.clicked.connect(self.capture)
        self.quitBtn.clicked.connect(self.quit)
        self.uploadImagesBtn.clicked.connect(self.uploadImages)
        self.registerBtn.clicked.connect(self.register)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)
        self.backBtn.clicked.connect(self.back)

        self.capturedFaces = 0
        self.output = ""

        self.dataset = config.DATASET
        self.encodings = config.ENCODINGS_PATH
        self.attendance = config.ATTENDANCE_PATH
        self.prototxt = config.PROTOTXT_PATH
        self.model = config.MODEL_PATH

        self.capturedFacesCount = 0
        self.cameraOn = False

    def takeImages(self):
        if self.nameLineEdit.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter Student's Full Name",
                windowTitle="Student Name",
            )
        elif self.rollNumberLineEdit.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter Student Roll Number",
                windowTitle="Roll Number",
            )
        else:
            self.constructOutput()
            self.cameraOn = True
            self.videoFrame.setVisible(True)
            self.faceDetectionWidget = FaceDetectionWidget()
            self.videoRecorder = VideoRecorder()
            self.videoRecorder.startRecording()
            frameLayout = self.videoFrame.layout()
            frameLayout.replaceWidget(self.videoLabel, self.faceDetectionWidget)

            # connect the image data signal and slot together
            imageDataSlot = self.faceDetectionWidget.imageDataSlot
            self.videoRecorder.imageData.connect(imageDataSlot)
            self.videoLabel = self.faceDetectionWidget
            self.faceDetectionWidget.output = self.output

    def capture(self):
        self.faceDetectionWidget.capture = True
        self.capturedFacesCount += 1
        self.registerLabel.setText("Captured {} faces".format(self.capturedFacesCount))

    def quit(self):
        self.videoRecorder.camera.release()
        cv2.destroyAllWindows()
        self.cameraOn = False

        displayText = "{} faces captured".format(self.capturedFacesCount)
        self.showDialog(
            icon=QMessageBox.Information,
            displayText=displayText,
            windowTitle="Capture Images",
        )
        print(displayText)
        self.videoFrame.close()

    def uploadImages(self):
        if self.nameLineEdit.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter student fullname",
                windowTitle="Student Name",
            )
        elif self.rollNumberLineEdit.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter Student Roll Number",
                windowTitle="Roll Number",
            )
        else:
            self.constructOutput()
            dlg = QFileDialog(self)
            dlg.setFileMode(QFileDialog.Directory)
            facesDir = dlg.getExistingDirectory()
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            for imagePath in list(paths.list_images(facesDir)):
                shutil.copy(imagePath, self.output)

            uploadedFaces = len(list(paths.list_images(self.output)))
            displayText = "{} faces uploaded".format(uploadedFaces)
            self.showDialog(
                icon=QMessageBox.Information,
                displayText=displayText,
                windowTitle="Upload Images",
            )

    def register(self):
        if self.nameLineEdit.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter student fullname",
                windowTitle="Student Name",
            )
        elif self.rollNumberLineEdit.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter Student Roll Number",
                windowTitle="Roll Number",
            )
        elif not os.path.exists(self.output):
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Take or Upload face images for {}".format(
                    self.nameLineEdit.text()
                ),
                windowTitle="Face images doesn't exists",
            )
        else:
            if self.cameraOn:
                self.videoRecorder.camera.release()
                cv2.destroyAllWindows()
                self.cameraOn = False
                self.registerLabel.setText("Registering...")

            # encode faces
            self.face_encoder = FaceEncoder(
                self.output, self.encodings, self.attendance, self.prototxt, self.model
            )
            self.face_encoder.encode_faces()
            self.face_encoder.save_face_encodings()

            displayText = "{} successful registered".format(self.nameLineEdit.text())
            self.showDialog(
                icon=QMessageBox.Information,
                displayText=displayText,
                windowTitle="Register Student",
            )
            self.registerLabel.setText(displayText)

    def back(self):
        if self.cameraOn:
            self.videoRecorder.camera.release()
            cv2.destroyAllWindows()
        from home import HomePage

        self.homePage = HomePage()
        self.homePage.show()
        self.close()

    def viewAttendance(self):
        if self.cameraOn:
            self.videoRecorder.camera.release()
            cv2.destroyAllWindows()
        from viewAttendance import ViewAttendance

        self.ViewAttendance = ViewAttendance()
        self.ViewAttendance.show()
        self.close()

    def constructOutput(self):
        studentName = self.nameLineEdit.text()
        studentName = studentName.replace(" ", "_")
        self.output = "dataset/{}".format(studentName)

    def showDialog(self, icon, displayText, windowTitle):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(displayText)
        msg.setWindowTitle(windowTitle)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterStudent()
    window.show()
    sys.exit(app.exec())
