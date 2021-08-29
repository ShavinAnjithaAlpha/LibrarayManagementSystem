import json
import sqlite3

from style_sheet import dark_style_sheet_for_widgets, dark_style_sheet_for_Collection, status_style_sheet_dark
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QListView, QFormLayout, QMenu,
                             QAction)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QObject, QAbstractListModel, QModelIndex, QAbstractItemModel
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QIcon


# create the book widget
class bookWidget(QWidget):

    default_cover_imageDir = "images/sys_images/book.png"
    # defined the new signal for book widget
    favoriteSignal = pyqtSignal(list)

    def __init__(self, title, book_id, path):
        super(bookWidget, self).__init__()
        # declare the instance variables
        self.title = title
        self.book_id = book_id
        self.path = path

        self.setStyleSheet(dark_style_sheet_for_Collection)

        # create the base widget
        self.baseWidget = QWidget()
        self.baseWidget.setObjectName("bookBaseWidget")

        # create the title label
        self.titleLabel = QLabel(self.title)
        self.titleLabel.setObjectName("bookTitleLabel")
        self.titleLabel.setWordWrap(True)

        # create the cover image label
        self.coverImageLabel = QLabel()
        self.coverImageLabel.setObjectName("bookImageLabel")

        # create the form layout for book other important data
        self.formLyt = QFormLayout()
        self.formLyt.setFormAlignment(Qt.AlignLeft)
        self.formLyt.setLabelAlignment(Qt.AlignLeft | Qt.AlignTop)

        # create the favorite button for this
        self.addFavoriteButton = QPushButton()
        self.addFavoriteButton.setObjectName("bookFavoriteButton")
        self.addFavoriteButton.clicked.connect(self.changeFavoriteState)
        self.addFavoriteButton.setCheckable(True)
        self.addFavoriteButton.setIconSize(QSize(30, 30))
        self.getInitialState()


        # create the vbox for pack the base widget
        vbox = QVBoxLayout()
        vbox.addWidget(self.baseWidget)
        self.setLayout(vbox)

    def getInitialState(self):

        user_data = []
        with open("db/favorite.json", "r") as file:
            user_data = json.load(file)

        for item in user_data:
            if item["id"] == self.book_id and item["type"] == "book":
                self.addFavoriteButton.setChecked(True)
                self.setState()
                return None

        self.addFavoriteButton.setChecked(False)
        self.setState()

    def setState(self):

        if self.addFavoriteButton.isChecked():
            self.addFavoriteButton.setIcon(QIcon("images/sys_images/fillStar.png"))
        else:
            self.addFavoriteButton.setIcon(QIcon("images/sys_images/nonFillStar.png"))

    def changeFavoriteState(self,state : bool):
        # connect to the favorite book json file and add the this book to this
        user_data = []
        with open("db/favorite.json", "r") as file:
            user_data = json.load(file)
        if state:

            # add the book to the file
            user_data.append({
                        "type" : "book",
                        "id" : self.book_id,
                        "title" : self.title,
                        "path" : self.path

            })
            # fire the signal
            self.favoriteSignal.emit([self.title, self.path, self.book_id, True, "book"])

        else:
            for item in user_data:
                if (item["type"] == "book" and item["id"] == self.book_id):
                    user_data.remove(item)
                    break

            # emit the signal
            self.favoriteSignal.emit([self.title, self.path, self.book_id, False, "book"])

        # save the changes
        with open("db/favorite.json", "w") as file:
            json.dump(user_data, file, indent=4)
        # set the current button state
        self.setState()


class boxBookWidget(bookWidget):
    def __init__(self, title, book_id, path):
        super(boxBookWidget, self).__init__(title, book_id, path)

        # set the widget size settings
        self.setMaximumSize(QSize(600, 400))

        self.coverImageLabel.setFixedSize(QSize(250, 300))
        # set the pix map
        self.coverImageLabel.setPixmap(
            QPixmap(self.default_cover_imageDir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio,
                                                        Qt.FastTransformation))
        self.titleLabel.setWordWrap(True)

        # create the v box for pack the title and form
        vbox = QVBoxLayout()
        vbox.addWidget(self.titleLabel)
        vbox.addLayout(self.formLyt)
        # create the grid
        gridLyt = QGridLayout()
        gridLyt.addWidget(self.coverImageLabel, 0, 0, 2, 1)
        gridLyt.addLayout(vbox, 0, 1, 2, 1)
        gridLyt.addWidget(self.addFavoriteButton, 0, 2)

        self.baseWidget.setLayout(gridLyt)

class listBookWidget(bookWidget):
    def __init__(self, title, book_id, path):
        super(listBookWidget, self).__init__(title, book_id, path)

        # set the widget size settings
        self.setMaximumHeight(150)

        self.coverImageLabel.setFixedSize(QSize(50, 50))
        # set the pix map
        self.coverImageLabel.setPixmap(
            QPixmap(self.default_cover_imageDir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio,
                                                        Qt.FastTransformation))
        # create the grid
        gridLyt = QGridLayout()
        gridLyt.addWidget(self.titleLabel, 0, 1)
        gridLyt.addWidget(self.coverImageLabel, 0, 0)
        # gridLyt.addLayout(self.formLyt, 1, 1)
        gridLyt.addWidget(self.addFavoriteButton, 0, 2)

        self.baseWidget.setLayout(gridLyt)


# create the collection widget
class collectionWidget(QWidget):

    # defined the new signal for change the favorite widgets of the model
    favoriteSignal = pyqtSignal(list)

    def __init__(self, title, description, image_dir, path, id):
        super(collectionWidget, self).__init__()
        self.title = title
        self.description = description
        self.image_dir = image_dir
        self.path = path
        self.collection_id = id

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
        self.imageLabel.setFixedSize(QSize(180, 170))
        self.imageLabel.setPixmap(
            QPixmap(self.image_dir).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

        # create the favorite button
        self.addFavoriteButton = QPushButton()
        self.addFavoriteButton.setObjectName("favoriteButton")
        self.addFavoriteButton.setIconSize(QSize(30, 30))
        self.addFavoriteButton.clicked.connect(self.changeFavoriteState)
        self.addFavoriteButton.setCheckable(True)
        self.setState()

        # create the menu button
        self.menuButton = QPushButton()
        self.menuButton.setObjectName("menuButton")

        self.setUpMenu()

    def setUpMenu(self):

        # create the menu
        self.menu = QMenu(self)

        # create the action
        self.changeTitleAction = QAction("change Title", self)
        self.changeTitleAction.triggered.connect(self.changeTitle)
        self.changeTitleAction.setToolTip("Change the Collection title you want")

        self.changeDesAction = QAction("change Description", self)
        self.changeDesAction.triggered.connect(self.changeDescription)
        self.changeDesAction.setToolTip("Change the Collection Description you want")

        # add to the menu
        self.menu.addAction(self.changeTitleAction)
        self.menu.addAction(self.changeDesAction)

        self.menuButton.setMenu(self.menu)

    def changeTitle(self):

        pass

    def changeDescription(self):

        pass

    def setIcon(self):

        if self.addFavoriteButton.isChecked():
            self.addFavoriteButton.setIcon(QIcon("images/sys_images/fillStar.png"))
        else:
            self.addFavoriteButton.setIcon(QIcon("images/sys_images/nonFillStar.png"))

    def setState(self):

        # open th json file
        user_data = []
        with open("db/favorite.json", "r") as file:
            user_data =json.load(file)

        for item in user_data:
            if item["path"]  == self.path and item["type"] == "collection":
                self.addFavoriteButton.setChecked(True)
                self.addFavoriteButton.setIcon(QIcon("images/sys_images/fillStar.png"))
                return None
        self.addFavoriteButton.setChecked(False)
        self.addFavoriteButton.setIcon(QIcon("images/sys_images/nonFillStar.png"))

    def changeFavoriteState(self, state):

        # get the id for this
        connection = sqlite3.connect("db/data.db")
        cursor = connection.cursor()

        cursor.execute(f""" SELECT collection_id FROM collection_table WHERE path = '{self.path}' """)
        data = cursor.fetchall()

        id = data[0][0]
        connection.close()

        # add to the favorite
        # open the json file
        user_data = []
        with open("db/favorite.json", "r") as file:
            user_data = json.load(file)

        if state:

            user_data.append({
                "type" : "collection",
                "id" : id,
                "title" : self.title,
                "path" : self.path,
            })

            # fire hte favorite signal
            self.favoriteSignal.emit([self.title, self.path, id, True, "collection"])

        else:
            # select the correct item and clear it
            for item in user_data:
                if item["path"] == self.path:
                    user_data.remove(item)
            # fire the signal
            self.favoriteSignal.emit([self.title, self.path, id, False, "collection"])

        # save the updated user_data
        with open("db/favorite.json", "w") as file:
            json.dump(user_data, file, indent=4)
        self.setIcon()

class boxCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path, id):
        super(boxCollectionWidget, self).__init__(title, description, image_dir, path, id)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(700, 400))

        # set the word wrapoption totitle ;abel
        self.titleLabel.setWordWrap(True)
        # create the grid layout for pack the items
        self.gridLyt  = QGridLayout()

        self.gridLyt.addWidget(self.titleLabel, 0, 0, 1, 2)
        self.gridLyt.addWidget(self.imageLabel, 1, 0, 1, 1)
        self.gridLyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)
        self.gridLyt.addWidget(self.addFavoriteButton, 0, 2)
        self.gridLyt.addWidget(self.menuButton, 0, 2)

        self.baseWidget.setLayout(self.gridLyt)


class listCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path, id):
        super(listCollectionWidget, self).__init__(title, description, image_dir, path, id)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumHeight(150)
        self.setMaximumHeight(220)

        self.titleLabel.setFont(QFont("verdana", 22))

        # create the grid lyt for pack items
        self.grid_lyt = QGridLayout()
        self.grid_lyt.addWidget(self.titleLabel, 0, 1, 1, 1)
        self.grid_lyt.addWidget(self.imageLabel, 0, 0, 2, 1)
        self.grid_lyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)
        self.grid_lyt.addWidget(self.addFavoriteButton, 0, 2)
        self.grid_lyt.addWidget(self.menuButton, 0, 2)


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
    bookImage = QImage("images/sys_images/book.png").scaled(QSize(35, 35), Qt.KeepAspectRatio, Qt.FastTransformation)

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
            else:
                return self.bookImage

        elif role == Qt.TextAlignmentRole:
            widgetType = self.todos[index.row()]["type"]

            if widgetType == "collection":
                return Qt.AlignLeft
            else:
                return Qt.AlignJustify

        elif role == Qt.BackgroundColorRole:
            widget_type = self.todos[index.row()]["type"]

            if widget_type == "collection":
                return QColor(0, 0, 30)
            else:
                return QColor(40, 0 , 0)

        elif role == Qt.FontRole:
            widget_type = self.todos[index.row()]["type"]

            if widget_type == "collection":
                return QFont("verdana", 12)
            else:
                return QFont("verdana", 11)

    def rowCount(self, index):
        return len(self.todos)

class RecentItemModel(QAbstractListModel):

    collectionImage = QImage("images/sys_images/collectionSmall.png").scaled(QSize(35, 35), Qt.KeepAspectRatio,
                                                                             Qt.FastTransformation)
    bookImage = QImage("images/sys_images/book.png").scaled(QSize(35, 35), Qt.KeepAspectRatio, Qt.FastTransformation)

    def __init__(self, *args, **kwargs):
        super(RecentItemModel, self).__init__(*args, **kwargs)
        self.todos = []

        self.coll_data = []
        with open("db/collection.json", "r") as file:
            self.coll_data = json.load(file)

        # fill the model with the data
        self.fillModel()

    def fillModel(self):

        # open the json file to open the recent json file
        user_data = []
        with open("db/collection_tracking.json", "r") as file:
            user_data = json.load(file)
        # limit the user data list
        if len(user_data) > 15:
            user_data = user_data[:15]

        self.todos = user_data

    def data(self, index: QModelIndex, role: int):

        if role == Qt.DisplayRole:
            # get the data item
            data = self.todos[index.row()]

            # return the text of the this
            try:
                return (self.coll_data.get(data[0]).get("title"))
            except:
                return "None"

        elif role  == Qt.DecorationRole:
            data = self.todos[index.row()]

            if data[-1] == "collection":
                return self.collectionImage
            else:
                return self.bookImage

        elif role == Qt.BackgroundColorRole:
            data = self.todos[index.row()]

            if data[-1] == "collection":
                return QColor(0, 50, 50)
            else:
                return QColor(50, 20, 0)

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.todos)


class StatusWidget(QWidget):
    def __init__(self):
        super(StatusWidget, self).__init__()

        # create the form layout and configure it
        self.form = QFormLayout()
        self.form.setFormAlignment(Qt.AlignLeft)
        self.form.setLabelAlignment(Qt.AlignLeft)
        self.form.setObjectName("status_form")
        self.form.setVerticalSpacing(30)

        self.setStyleSheet(status_style_sheet_dark)
        self.setLayout(self.form)

    def addLine(self, title, data, wrap = False):

        # create the new Label
        label = QLabel(data)
        if wrap:
            label.setWordWrap(True)
        # add the new line for the form
        self.form.addRow(title, label)

    def addLabel(self, data):

        # created label and set to the form
        label = QLabel(data)
        label.setWordWrap(True)
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


if __name__ == "__main__":
    app = QApplication([])
    window = listBookWidget("pdf", "455sdsd", "1/2/5")
    window.show()

    # create the model
    model = RecentItemModel()
    view = QListView()
    view.setModel(model)
    view.show()

    app.exec_()

