import json
import shutil
import sqlite3
import os

from style_sheet import dark_style_sheet_for_widgets, dark_style_sheet_for_Collection, status_style_sheet_dark, root_collection_dark_style_sheet
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QListView, QFormLayout, QMenu,
                             QAction, QInputDialog, QFileDialog, QPlainTextEdit, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QAbstractListModel, QModelIndex
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

    def __init__(self, title, description, image_dir, path, pw, id):
        super(collectionWidget, self).__init__()
        self.title = title
        self.description = description
        self.image_dir = image_dir
        self.path = path
        self.collection_id = id
        self.pw = pw

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
        self.changeTitleAction = QAction("Change Title", self)
        self.changeTitleAction.triggered.connect(self.changeTitle)
        self.changeTitleAction.setToolTip("Change the Collection title you want")

        self.changeDesAction = QAction("Change Description", self)
        self.changeDesAction.triggered.connect(self.changeDescription)
        self.changeDesAction.setToolTip("Change the Collection Description you want")

        self.changeImageAction = QAction("Change Cover Image", self)
        self.changeImageAction.triggered.connect(self.changeImage)
        self.changeImageAction.setToolTip("Change the Collection Cover Image you want")

        self.changePasswordAction = QAction("Change Passwod", self)
        self.changePasswordAction.setToolTip("Chnange the collection passowrd or enter the new password")
        self.changePasswordAction.triggered.connect(self.changePassword)

        # add to the menu
        self.menu.addAction(self.changeTitleAction)
        self.menu.addAction(self.changeDesAction)
        self.menu.addAction(self.changeImageAction)
        self.menu.addAction(self.changePasswordAction)

        self.menuButton.setMenu(self.menu)

    def changePassword(self):

        check = False
        subCheck = False
        # get the new password from the text box
        if self.pw != "":
            # reconfirm the password
            pw , ok = QInputDialog.getText(self, "Password Prompt", "Enter the Password : ", echo=QLineEdit.Password)
            if ok and pw == self.pw:
                subCheck = True
            else:
                QMessageBox.warning(self, "Warning", "Password You Entered is Wrong! Plaese Enter Correct Password")

        else:
            subCheck = True

        # get the new pw from the user
        if subCheck:
            # get the new pw from the user
            new_pw, ok2 = QInputDialog.getText(self, "New Password Dialog", "Enter the New Password : ", echo=QLineEdit.Password)
            if ok2:
                # confirm the password from the user
                confirm_pw, ok3 = QInputDialog.getText(self, "Confirm Password Dialog", "Confirm the Password : ", echo=QLineEdit.Password)
                if ok3 and confirm_pw == new_pw:
                    check = True
                else:
                    QMessageBox.warning(self, "Warning", "Confirm Password is not correct...Please Enter the Correct Password")


        if check:
            # change the password from the data base and current widget
            self.pw = new_pw
            # create the connection to the data base
            connection = sqlite3.connect("db/data.db")
            cursor = connection.cursor()

            cursor.execute(
                f" UPDATE collection_table SET pw = '{self.pw}' WHERE collection_id = '{self.collection_id}'  ")
            # save the changes
            connection.commit()
            connection.close()

    def changeImage(self):

        # open the file dialog and change the image dir
        file, ok = QFileDialog.getOpenFileName(self, "Open the Cover Image", "", "JPG Files(*.jpg);; PNG Files(*.png)")
        if ok:

            # change the image dir to relative path
            new_path = os.path.join("images", os.path.split(file)[1])
            shutil.copyfile(file ,new_path)

            # save the changes
            user_data = {}
            with open("db/collection.json", "r") as file:
                user_data = json.load(file)

            user_data.get(self.collection_id)["image_dir"] = new_path

            with open("db/collection.json", "w") as file:
                json.dump(user_data, file, indent=4)

            # change the image
            self.imageLabel.setPixmap(QPixmap(new_path).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
            self.image_dir = new_path

    def changeTitle(self):

        text, ok = QInputDialog.getText(self, "Title Changed Dialog", "Enter the new title : ")

        if ok:
            # change the data base file title
            user_data = {}
            with open("db/collection.json") as file:
                user_data = json.load(file)

            user_data.get(self.collection_id)['title'] = text
            with open("db/collection.json", "w") as file:
                json.dump(user_data, file, indent=4)

            # change the favorites json file
            with open("db/favorite.json") as file:
                user_data = json.load(file)

            for item in user_data:
                if item["id"] == self.collection_id and item['type'] == "collection":
                    item["title"] = text

            with open("db/favorite.json", "w") as file:
                json.dump(user_data, file, indent=4)
            # end of the update the json files


            # update the database file
            connection = sqlite3.connect("db/data.db")
            cursor = connection.cursor()

            cursor.execute(f"UPDATE collection_table SET name = '{text}' WHERE collection_id = '{self.collection_id}'  ")
            connection.commit()

            # close the connection
            connection.close()

            # change the widget title
            self.titleLabel.setText(text)
            self.title = text

    def changeDescription(self):

        # prompt the text dialog for get the new description
        text, ok = QInputDialog.getMultiLineText(self, "New Description Dialog", "Description : ", text=self.description)
        if ok:
            # change the collection json file
            user_data = {}
            with open("db/collection.json", "r") as file:
                user_data = json.load(file)

            # find the code and change the description
            user_data.get(self.collection_id)["description"] = text
            # save the changes
            with open("db/collection.json", "w") as file:
                json.dump(user_data, file, indent=4)

            # change hte curren widget description
            self.descriptionLabel.setText(text)
            self.description = text

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
    def __init__(self, title, description, image_dir, path, pw ,id):
        super(boxCollectionWidget, self).__init__(title, description, image_dir, path, pw, id)
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
        self.gridLyt.addWidget(self.addFavoriteButton, 0, 3)
        self.gridLyt.addWidget(self.menuButton, 0, 2)

        self.baseWidget.setLayout(self.gridLyt)


class listCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path, pw, id):
        super(listCollectionWidget, self).__init__(title, description, image_dir, path, pw, id)
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
        self.grid_lyt.addWidget(self.addFavoriteButton, 0, 3)
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

            if self.todos.index(self.todos[index.row()]) % 2 == 0:
                return QColor(20, 20, 20)
            else:
                return QColor(30, 30, 30)

        elif role == Qt.FontRole:
            widget_type = self.todos[index.row()]["type"]

            if widget_type == "collection":
                return QFont("verdana", 10)
            else:
                return QFont("verdana", 9)

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

        # filter the duplicates
        user_data = RecentItemModel.filterDuplicates(user_data, 0)
        # limit the user data list
        if len(user_data) > 15:
            user_data = user_data[:15]

        self.todos = user_data

    @staticmethod
    def filterDuplicates(itemList : list, key = 0):

        # remove the duplicates and return the filtered list
        filtered_list = []
        itemList.reverse()

        for item in itemList:
            check = True
            for j in filtered_list:
                if j[key] == item[key]:
                    check = False
                    break

            # append to the new list based on the check boolean
            if check:
                filtered_list.append(item)

        return filtered_list


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
                return QColor(0, 0, 0)
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
        with open("db/collection.json") as file:
            user_data = json.load(file)

        self.data = user_data.get(self.collection_id)

        # create the connection
        connection = sqlite3.connect("db/data.db")
        cursor = connection.cursor()

        cursor.execute(f" SELECT date, time FROM collection_table WHERE collection_id = '{self.collection_id}' ")
        data = cursor.fetchall()

        connection.close()

        self.date = data[0][0]
        self.time = data[0][1]

    def initializeUI(self):

        # create the root label
        rootLabel = QLabel("Root")
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
    window = listBookWidget("pdf", "455sdsd", "1/2/5")
    window.show()

    # create the model
    model = RecentItemModel()
    view = QListView()
    view.setModel(model)
    view.show()

    app.exec_()

