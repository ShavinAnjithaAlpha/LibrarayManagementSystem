import json
import sqlite3

from style_sheet import dark_style_sheet_for_widgets, dark_style_sheet_for_Collection
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QListView)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject, QAbstractListModel, QModelIndex, QAbstractItemModel
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage

# create the collection widget
class collectionWidget(QWidget):

    # defined the new signal for change the favorite widgets of the model
    favoriteSignal = pyqtSignal(list)

    def __init__(self, title, description, image_dir, path):
        super(collectionWidget, self).__init__()
        self.title = title
        self.description = description
        self.image_dir = image_dir
        self.path = path

        # create the container base widget
        self.baseWidget = QWidget(self)
        self.baseWidget.setObjectName("collectionBaseWidget")
        # create the v boc for pack the base widget
        v_box = QVBoxLayout()
        v_box.addWidget(self.baseWidget)
        self.setLayout(v_box)

        self.setStyleSheet(dark_style_sheet_for_Collection)

        # create the title , description and image labels
        self.titleLabel = QLabel(self.title)
        self.titleLabel.setFont(QFont('verdana', 18))
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        self.titleLabel.setObjectName("collectionTitleLabel")

        self.descriptionLabel = QLabel(self.description)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setFont(QFont("Hack", 11))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setObjectName("collectionDescriptionLabel")

        if self.description == "":
            self.descriptionLabel.setText("No Description yet")

        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(QSize(180, 200))
        self.imageLabel.setPixmap(
            QPixmap(self.image_dir).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

        # create the favorite button
        self.addFavoriteButton = QPushButton()
        self.addFavoriteButton.setObjectName("favoriteButton")
        self.addFavoriteButton.clicked.connect(self.changeFavoriteState)
        self.addFavoriteButton.setCheckable(True)
        self.setState()

    def setState(self):

        # open th json file
        user_data = []
        with open("db/favorite.json", "r") as file:
            user_data =json.load(file)

        for item in user_data:
            if item["path"]  == self.path:
                self.addFavoriteButton.setChecked(True)
                return None
        self.addFavoriteButton.setChecked(False)

    def changeFavoriteState(self, state):

        # get the id for this
        connection = sqlite3.connect("db/data.db")
        cursor = connection.cursor()

        cursor.execute(f""" SELECT collection_id FROM collection_table WHERE path = '{self.path}' """)
        data = cursor.fetchall()

        id = data[0][0]
        connection.close()

        if state:
            # add to the favorite
            # open the json file
            user_data = []
            with open("db/favorite.json", "r") as file:
                user_data = json.load(file)


            user_data.append({
                "type" : "collection",
                "id" : id,
                "title" : self.title,
                "path" : self.path,
            })

            with open("db/favorite.json", "w") as file:
                json.dump(user_data, file, indent=4)
            # fire hte favorite signal
            self.favoriteSignal.emit([self.title, self.path, id, True])

        else:
            # remove the item from the favorites
            with open("db/favorite.json", "r") as file:
                user_data = json.load(file)

            # select the correct item and clear it
            for item in user_data:
                if item["path"] == self.path:
                    user_data.remove(item)

            # save the updated user_data
            with open("db/favorite.json", "w") as file:
                json.dump(user_data, file, indent=4)

            # fire the signal
            self.favoriteSignal.emit([self.title, self.path, id, False])

class boxCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path):
        super(boxCollectionWidget, self).__init__(title, description, image_dir, path)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumSize(QSize(300, 250))
        self.setMaximumSize(QSize(500, 350))

        # create the grid layout for pack the items
        self.gridLyt  = QGridLayout()

        self.gridLyt.addWidget(self.titleLabel, 0, 0, 1, 2)
        self.gridLyt.addWidget(self.imageLabel, 1, 0, 1, 1)
        self.gridLyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)
        self.gridLyt.addWidget(self.addFavoriteButton, 0, 2)

        self.baseWidget.setLayout(self.gridLyt)


class listCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path):
        super(listCollectionWidget, self).__init__(title, description, image_dir, path)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumHeight(200)
        self.setMaximumHeight(350)

        self.titleLabel.setFont(QFont("verdana", 22))

        # create the grid lyt for pack items
        self.grid_lyt = QGridLayout()
        self.grid_lyt.addWidget(self.titleLabel, 0, 1, 1, 1)
        self.grid_lyt.addWidget(self.imageLabel, 0, 0, 2, 1)
        self.grid_lyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)
        self.grid_lyt.addWidget(self.addFavoriteButton, 0, 2)


        self.baseWidget.setLayout(self.grid_lyt)


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


class favoriteListModel(QAbstractListModel):

    json_file = "db/favorite.json"
    collectionImage = QImage("images/sys_images/collectionSmall.png").scaled(QSize(35, 35), Qt.KeepAspectRatio, Qt.FastTransformation)

    def __init__(self, *args, todos = None,  **kwargs):
        super(favoriteListModel, self).__init__(*args, **kwargs)
        self.todos = [] or todos
        self.fillList()

    def fillList(self):

        try:
            # connect to the json file
            with open(self.json_file, "r") as file:
                user_data = json.load(file)

            # set the data as the todolist
            self.todos = user_data
            self.layoutChanged.emit()

        except:
            raise FileNotFoundError("Cannot find the Favorites Data File...")

    def data(self, index, role):

        if role == Qt.DisplayRole:
            # get the index data

            collection_data = self.todos[index.row()]
            # return the collection name
            return collection_data["title"]
        elif role == Qt.DecorationRole:
            collection_data = self.todos[index.row()]
            # get the type of the data
            widgetType = collection_data["type"]
            if widgetType == "collection":
                return self.collectionImage

        elif role == Qt.TextAlignmentRole:
            widgetType = self.todos[index.row()]["type"]

            if widgetType == "collection":
                return Qt.AlignLeft
            else:
                return Qt.AlignRight

        elif role == Qt.BackgroundColorRole:
            widget_type = self.todos[index.row()]["type"]

            if widget_type == "collection":
                return QColor(0, 0, 20)
            else:
                return QColor(20, 0 , 0)

        elif role == Qt.FontRole:
            widget_type = self.todos[index.row()]["type"]

            if widget_type == "collection":
                return QFont("verdana", 12)
            else:
                return QFont("verdana", 10)

    def rowCount(self, index):
        return len(self.todos)

if __name__ == "__main__":
    app = QApplication([])
    window = listCollectionWidget("Science", "this is the science section for get the some knowledges.....", "images/sys_images/coll_img1.jpg", "0/1/2")
    window.show()

    # create the list view
    model = favoriteListModel(todos=[{"title" : "len", "type" : "collection"}])
    model.layoutChanged.emit()
    listview = QListView()
    print(model.todos)
    listview.setModel(model)


    listview.show()

    app.exec_()

