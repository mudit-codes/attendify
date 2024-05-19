import sys
import qdarkstyle

from app.pages.login import LoginPage

from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api="pyqt5"))

    window = LoginPage()
    window.show()
    sys.exit(app.exec())
