import os
import sys
import sqlite3

sys.path.append(".")
sys.path.append("./app/pages")

# pages
# from signup import SignupPage
# from home import HomePage

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit


class LoginPage(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("app/ui/login.ui", self)
        self.loginBtn.clicked.connect(self.login)
        self.signupBtn.clicked.connect(self.signup)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)

    def login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()

        if len(username) == 0 or len(password) == 0:
            displayText = "Required fields cannot be empty."
            self.showDialog(
                icon=QMessageBox.Warning, displayText=displayText, windowTitle="Signup"
            )
        else:
            try:
                connection = sqlite3.connect("db/login.db")
                results = connection.execute(
                    "SELECT * FROM USERS WHERE USERNAME = ? AND PASSWORD = ?",
                    (username, password),
                )
                if len(results.fetchall()) > 0:
                    # self.homePage = HomePage()
                    # self.homePage.show()
                    self.close()
                else:
                    displayText = "Invalid username and password"
                    self.showDialog(
                        icon=QMessageBox.Warning,
                        displayText=displayText,
                        windowTitle="Signup",
                    )
                connection.close()
            except:
                displayText = "Error connecting to database"
                self.showDialog(
                    icon=QMessageBox.Warning,
                    displayText=displayText,
                    windowTitle="Signup",
                )

    def signup(self):
        # self.signupPage = SignupPage()
        # self.signupPage.show()
        self.close()

    def showDialog(self, icon, displayText, windowTitle):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(displayText)
        msg.setWindowTitle(windowTitle)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())
