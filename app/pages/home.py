import os
import sys

sys.path.append(".")
sys.path.append("app\pages")

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class HomePage(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("app/ui/home.ui", self)
        self.registerStudentBtn.clicked.connect(self.registerStudent)
    #     self.takeAttendanceBtn.clicked.connect(self.takeAttendance)
        self.viewAttendanceBtn.clicked.connect(self.viewAttendance)

    def registerStudent(self):
        from registerStudent import RegisterStudent

        self.registerStudent = RegisterStudent()
        self.registerStudent.show()
        self.close()

    # def takeAttendance(self):
    #     from take_attendance import TakeAttendance

    #     self.takeAttendance = TakeAttendance()
    #     self.takeAttendance.show()
    #     self.close()

    def viewAttendance(self):
        from viewAttendance import ViewAttendance

        self.viewAttendance = ViewAttendance()
        self.viewAttendance.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec())
