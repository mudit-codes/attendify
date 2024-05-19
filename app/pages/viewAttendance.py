import os
import sys
import pdfkit

sys.path.append(".")
sys.path.append("app/utils")

import config
import pandas as pd
import numpy as np

from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QApplication,
    QHeaderView,
    QMessageBox,
    QFileDialog,
)


class ViewAttendance(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("app/ui/viewAttendance.ui", self)

        self.filterComboBox.activated[str].connect(self.filter)
        self.searchBtn.clicked.connect(self.search)
        self.saveAsPdfBtn.clicked.connect(self.saveAsPdf)
        self.backBtn.clicked.connect(self.back)

        self.attendance = config.ATTENDANCE_PATH

        self.df = pd.read_csv(self.attendance, index_col=0)
        self.displayTable()

    def search(self):
        self.df = pd.read_csv(self.attendance, index_col=0)
        if self.searchText.text() == "":
            self.showDialog(
                icon=QMessageBox.Warning,
                displayText="Enter student fullname",
                windowTitle="Search Name",
            )
        else:
            name = self.searchText.text().replace(" ", "_")
            self.df = self.df[self.df["names"] == name]
            if len(self.df) == 0:
                self.showDialog(
                    icon=QMessageBox.Warning,
                    displayText="{} is not registered".format(name),
                    windowTitle="Search Name",
                )
            else:
                self.displayTable()

    def filter(self, selected):
        self.df = pd.read_csv(self.attendance, index_col=0)
        if selected == "Good":
            attend_frac = self.df.sum(axis=1) / self.df.count(axis=1, numeric_only=True)
            self.df = self.df[attend_frac >= 0.9]
        elif selected == "Warning":
            attend_frac = self.df.sum(axis=1) / self.df.count(axis=1, numeric_only=True)
            self.df = self.df[(attend_frac >= 0.8) & (attend_frac < 0.9)]
        elif selected == "Danger":
            attend_frac = self.df.sum(axis=1) / self.df.count(axis=1, numeric_only=True)
            self.df = self.df[attend_frac < 0.8]
        else:
            self.df = pd.read_csv(self.attendance, index_col=0)
        self.searchText.setText("")
        self.displayTable()

    def displayTable(self):
        counts = list(
            round(
                (self.df.sum(axis=1) / self.df.count(axis=1, numeric_only=True)) * 100,
                2,
            )
        )
        colorMap = {
            "Good": QtGui.QColor(0, 255, 0, 150),
            "Warning": QtGui.QColor(255, 255, 0, 150),
            "Danger": QtGui.QColor(255, 0, 0, 150),
        }

        self.df["attend_percent"] = counts
        self.df["names"] = self.df["names"].str.replace("dataset/", "")
        df = self.df.loc[:, ["names", "attend_percent"]]
        df = df.rename(
            {"names": "Student Name", "attend_percent": "Attendance Percentage"}, axis=1
        )

        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)
        self.table.horizontalHeader().setStretchLastSection(True)

        for i, row in enumerate(df.values):
            if counts[i] >= 80:
                color = colorMap["Good"]
            elif counts[i] >= 60:
                color = colorMap["Warning"]
            else:
                color = colorMap["Danger"]

            for j, data in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(data)))
                self.table.item(i, j).setBackground(color)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.clicked.connect(self.detailAttendance)

    def detailAttendance(self):
        from detailAttendance import DetailAttendance

        self.detailAttendancePage = DetailAttendance(self.df, self.table.currentRow())
        self.detailAttendancePage.show()
        self.close()

    def saveAsPdf(self):
        try:
            # Read and process the CSV file
            df = pd.read_csv(self.attendance, index_col=0)
            df = df.replace({0: "absent", 1: "present", None: "excused"})
            df = df.rename({"names": "Student Name"}, axis=1)

            # Get output directory from file dialog
            dlg = QFileDialog(self)
            dlg.setFileMode(QFileDialog.Directory)
            outputPath = dlg.getExistingDirectory()

            if not outputPath:
                print("No directory selected.")
                return

            now = pd.Timestamp.now()

            # Construct file names and paths
            baseFilename = f"attendance_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
            pdfFilename = baseFilename + ".pdf"
            pdfFilePath = os.path.join(outputPath, pdfFilename)

            # Save DataFrame to HTML
            htmlContent = df.to_html()

            # Convert HTML to PDF
            configuration = pdfkit.configuration(wkhtmltopdf=config.PDF_PATH)
            pdfkit.from_string(htmlContent, pdfFilePath, configuration=configuration)
            print(f"PDF successfully created at {pdfFilePath}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def back(self):
        from home import HomePage

        self.homePage = HomePage()
        self.homePage.show()
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
    window = ViewAttendance()
    window.show()
    sys.exit(app.exec())
