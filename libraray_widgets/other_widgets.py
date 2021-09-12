import json
import random
import shutil
import sqlite3
import os
import  fitz

from style_sheet import dark_style_sheet_for_widgets, dark_style_sheet_for_Collection, status_style_sheet_dark, root_collection_dark_style_sheet
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QFormLayout, QMenu,
                             QAction, QInputDialog, QFileDialog, QPlainTextEdit, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon

db_file = "db/data.db"
collection_file  = "db/collection.json"

class switchButton(QWidget):

    # defined the new signal
    switchSignal = pyqtSignal()

    def __init__(self, textLeft, textRight, key1, key2):
        super(switchButton, self).__init__()
        self.textLeft , self.textRight = textLeft, textRight
        self.keys = {textLeft : key1,
                     textRight : key2}
        self.initializeUI()

        self.setStyleSheet(dark_style_sheet_for_widgets)

    def initializeUI(self):

        self.setContentsMargins(0, 0, 0, 0)
        # create the two buttons
        self.buttonLeft = QPushButton(self.textLeft)
        self.buttonLeft.setObjectName("switchButtonLeft")
        self.buttonLeft.setCheckable(True)
        self.buttonLeft.setChecked(True)

        self.buttonRight = QPushButton(self.textRight)
        self.buttonRight.setObjectName("switchButtonRight")
        self.buttonRight.setCheckable(True)
        self.buttonRight.setChecked(False)

        # set the button slots
        self.buttonLeft.clicked.connect(lambda a, e = "left" : self.setButtonState(e, a))
        self.buttonRight.clicked.connect(lambda a, e = "right" : self.setButtonState(e, a))

        # create the h box
        h_box = QHBoxLayout()
        h_box.setSpacing(0)
        h_box.addWidget(self.buttonLeft)
        h_box.addWidget(self.buttonRight)

        self.setLayout(h_box)


    def setButtonState(self, button , state):

        if button == "left":
            self.buttonLeft.setChecked(True)
            self.buttonRight.setChecked(False)
        elif button == "right":
            self.buttonRight.setChecked(True)
            self.buttonLeft.setChecked(False)

        # fire the signal
        self.switchSignal.emit()

    def getState(self):

        if self.buttonLeft.isChecked():
            return self.keys.get(self.buttonLeft.text())
        else:
            return self.keys.get(self.buttonRight.text())


class StatusWidget(QWidget):
    def __init__(self):
        super(StatusWidget, self).__init__()

        # create the form layout and configure it
        self.form = QFormLayout()
        self.form.setFormAlignment(Qt.AlignLeft)
        self.form.setLabelAlignment(Qt.AlignLeft)
        self.form.setObjectName("status_form")
        self.form.setVerticalSpacing(10)


        self.setMaximumHeight(300)

        self.setStyleSheet(status_style_sheet_dark)
        self.setLayout(self.form)

    def addLine(self, title, data, wrap = False):

        # create the title label
        title_label = QLabel(f"{title} : ")
        title_label.setObjectName("titleLabel")
        # create the data label
        dataLabel = QLabel(data)
        dataLabel.setWordWrap(wrap)
        dataLabel.setObjectName("dataLabel")

        self.form.addWidget(title_label)
        self.form.addWidget(dataLabel)

    def addTextArea(self, title, data):

        # create th text area
        textArea = QPlainTextEdit()
        textArea.setObjectName("plainTextEdit")
        textArea.setPlainText(data)
        textArea.setReadOnly(True)
        textArea.setFixedSize(QSize(200, 70))
        textArea.setFont(QFont('verdana', 9))
        textArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        textArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        textArea.setContentsMargins(0, 0, 0, 0)

        # title Label
        titleLabel = QLabel(f"{title} : ")
        titleLabel.setObjectName("titleLabel")

        self.form.addWidget(titleLabel)
        self.form.addWidget(textArea)

    def addLabel(self, data):

        # created label and set to the form
        label = QLabel(data)
        label.setWordWrap(True)
        label.setObjectName("titleLabel")
        self.form.setFormAlignment(Qt.AlignHCenter)
        self.form.addWidget(label)

        self.form.setFormAlignment(Qt.AlignLeft)

    def addSpace(self):
        self.form.addWidget(QLabel(""))


    def addSeperator(self):

        # create the seperator label
        sepLabel = QLabel()
        sepLabel.setObjectName("sepLabel")
        sepLabel.setMinimumWidth(int(self.width() * 0.8))
        sepLabel.setMaximumWidth(int(self.width() * 0.8))
        # add to the form layout
        self.form.addWidget(sepLabel)

    def clearBox(self):
        # remove the all of the item in the staus widget
        self.form.deleteLater()

        # create the new form layout
        self.form = QFormLayout()
        self.form.setFormAlignment(Qt.AlignLeft)
        self.form.setLabelAlignment(Qt.AlignLeft)
        self.form.setObjectName("status_form")

        self.setLayout(self.form)

class rootCollectionWidget(QWidget):
    def __init__(self, collection_id):
        super(rootCollectionWidget, self).__init__()
        self.collection_id = collection_id
        # first fetch the data about the collection from the json file
        self.fetchData()

        self.setStyleSheet(root_collection_dark_style_sheet)

        self.initializeUI()

    def fetchData(self):

        user_data = {}
        with open(collection_file) as file:
            user_data = json.load(file)

        self.data = user_data.get(self.collection_id)

        # create the connection
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute(f" SELECT date, time FROM collection_table WHERE collection_id = '{self.collection_id}' ")
        data = cursor.fetchall()

        connection.close()

        self.date = data[0][0]
        self.time = data[0][1]

    def initializeUI(self):

        # create the root label
        rootLabel = QLabel("Root")
        rootLabel.setObjectName("rootLabel")
        rootLabel.setFont(QFont("verdana", 17))

        # create the cover image label
        self.coverImageLabel = QLabel()
        self.coverImageLabel.setFixedSize(QSize(100, 80))
        self.coverImageLabel.setPixmap(QPixmap(self.data["image_dir"]).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # create the title label
        self.titleLabel = QLabel(self.data["title"])
        self.titleLabel.setObjectName("titleLabel")

        # create the description label
        self.descriptionLabel = QPlainTextEdit()
        self.descriptionLabel.setFont(QFont('verdana', 9))
        self.descriptionLabel.setFixedSize(QSize(200, 70))
        self.descriptionLabel.setPlainText(self.data["description"])
        self.descriptionLabel.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.descriptionLabel.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # create the date and time label
        dateTimeLabel = QLabel(f"Created On {self.date}\n at {self.time}")
        dateTimeLabel.setFont(QFont('verdana' , 9))

        # create the v box for pack the widgets
        vBox = QVBoxLayout()
        vBox.addWidget(rootLabel)
        vBox.addWidget(self.coverImageLabel, alignment=Qt.AlignLeft)
        vBox.addWidget(self.titleLabel, alignment=Qt.AlignLeft)
        vBox.addWidget(self.descriptionLabel, alignment=Qt.AlignLeft)
        vBox.addWidget(dateTimeLabel, alignment=Qt.AlignCenter)

        self.setLayout(vBox)






if __name__ == "__main__":
    app = QApplication([])

    app.setStyleSheet(""" QWidget {background-color : rgb(20, 20, 20)}""")
    app.exec_()

