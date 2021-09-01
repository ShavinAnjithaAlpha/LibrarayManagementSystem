import os, sys, json, sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QDialogButtonBox, QTextEdit, QCheckBox, QGridLayout)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QFont, QPixmap
from style_sheet import dark_style_sheet_for_status

class FullStatusWidget(QWidget):
    def __init__(self, coll_id):
        super(FullStatusWidget, self).__init__()
        self.collection_id = coll_id

        # defined the data dict of the widget
        self.data = {}
        self.getData()

        self.setStyleSheet(dark_style_sheet_for_status)
        self.initializeUI()

    def getData(self):

        # first get the basic data from the db
        connect = sqlite3.connect("db/data.db")
        cursor  = connect.cursor()

        cursor.execute(f" SELECT * FROM collection_table WHERE collection_id = '{self.collection_id}' ")
        data = cursor.fetchall()
        data = data[0]

        connect.close()

        self.data["title"] = data[3]
        self.data["path"] = data[2]
        self.data["started_date"] = data[4]
        self.data["started_time"] = data[5]
        self.data["pw"] = data[6]

        # get the favorite data fromm the json file
        fav_data = []
        with open("db/favorite.json") as file:
            fav_data = json.load(file)

        self.data["isFavorite"] = False
        for item in fav_data:
            if item["id"] == self.collection_id:
                self.data["isFavorite"] = True
                break

        # open the tracking collection json file
        track_data = []
        with open("db/collection_tracking.json") as file:
            track_data = json.load(file)
        self.data["count"] = 0

        self.data["last_opened_date"] = ""
        self.data["last_opened_time"] = ""
        for item in track_data:
            if item[0] == self.collection_id and item[-1] == "collection":
                self.data["last_opened_date"] = item[1]
                self.data["last_opened_time"] = item[2]
                self.data["count"] += 1

        # get the other data from the collection json file
        coll_data = {}
        with open("db/collection.json") as file:
            coll_data = json.load(file)

        self.data["description"] = coll_data.get(self.collection_id)["description"]
        self.data["image_dir"] = coll_data.get(self.collection_id)["image_dir"]




    def initializeUI(self):


        # create the image Label
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap(self.data["image_dir"]).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # create the title label
        self.titleLabel = QLabel(self.data["title"])
        self.titleLabel.setFont(QFont("Verdana", 18))

        # create the description label
        self.desLabel = QLabel(self.data['description'])
        self.desLabel.setFont(QFont('verdana', 13))

        # create the created time and date label
        self.createAtLabel = QLabel(f"Created On {self.data['started_date']} At {self.data['started_time']} ")
        self.createAtLabel.setFont(QFont('verdana', 13))

        # create the path name label
        self.pathLabel = QLabel(f"<i>Collection Path as the Numeric System is<i> <font color = 'blue' >{self.data['path']}</font>")
        self.pathLabel.setFont(QFont('verdana', 13))

        # create the favorite and secured status Labels
        favStatus = "Yes" if self.data["isFavorite"] else "No"
        self.favLabel = QLabel(f"<i>is Favorite Collection</i>    : <font color = 'blue' >{favStatus}</font>")
        self.favLabel.setFont(QFont("verdana", 13))

        # create the favorite and secured status Labels
        pwStatus = "Yes" if self.data["pw"] != "" else "No"
        self.pwLabel = QLabel(f"<i>is Secured Collection</i>    : <font color = 'blue' >{pwStatus}</font>")
        self.pwLabel.setFont(QFont('verdana', 13))

        # create the history label
        historyLabel = QLabel("History Of Collection <font color = 'blue' >{}</font>".format(self.data['title']))
        historyLabel.setObjectName("historyReferLabel")

        label1 = QLabel("Last Opened At  : ")
        label2 = QLabel("Number of opened times  : ")

        countLabel = QLabel(f"{self.data['count']}")
        lastOpenLabel = QLabel(f"{self.data['last_opened_date']} at {self.data['last_opened_time']}")

        for widget in [label1, label2, lastOpenLabel, countLabel]:
            widget.setFont(QFont('verdana', 12))
            widget.setObjectName("historyLabels")


        # create the grid for this
        grid = QGridLayout()
        grid.addWidget(historyLabel, 0, 0)
        grid.addWidget(label1, 1, 0)
        grid.addWidget(label2, 2, 0)
        grid.addWidget(lastOpenLabel, 1, 1)
        grid.addWidget(countLabel, 2, 1)

        # create the close button for this
        closeButton = QPushButton("Close")
        closeButton.setObjectName("closeButton")
        closeButton.pressed.connect(self.deleteLater)

        # create the layout for pak the widgets
        v_box1 = QVBoxLayout()
        v_box1.addWidget(self.imageLabel, alignment=Qt.AlignCenter)
        v_box1.addWidget(self.titleLabel, alignment=Qt.AlignCenter)
        v_box1.addWidget(self.desLabel, alignment=Qt.AlignCenter)
        v_box1.addSpacing(30)
        v_box1.addWidget(self.createAtLabel, alignment=Qt.AlignLeft)
        v_box1.addWidget(self.pathLabel, alignment=Qt.AlignLeft)
        v_box1.addSpacing(50)
        v_box1.addWidget(self.favLabel, alignment=Qt.AlignLeft)
        v_box1.addWidget(self.pwLabel, alignment=Qt.AlignLeft)
        v_box1.addSpacing(50)
        v_box1.addLayout(grid)
        v_box1.addWidget(closeButton, alignment=Qt.AlignRight)


        self.setLayout(v_box1)