import json, sqlite3, random, fitz
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFormLayout, QMessageBox, QMenu, QAction, QLineEdit,
                             QInputDialog)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap, QIcon,  QKeyEvent
# import the styles
from style_sheet import dark_style_sheet_for_Collection

chrs = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9"]

db_file = "db/data.db"
book_file = "db/book.json"
favorite_file = "db/favorite.json"

class bookWidget(QWidget):

    default_cover_imageDir = "images/sys_images/book.png"
    # defined the new signal for book widget
    favoriteSignal = pyqtSignal(list)

    def __init__(self, title, book_id, path, pw = ""):
        super(bookWidget, self).__init__()
        # declare the instance variables
        self.title = title
        self.book_id = book_id
        self.path = path
        self.pw = pw

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


    def contextMenuEvent(self, event) -> None:

        # create the menu
        self.menu = QMenu(self)

        # create the menu option for this
        openAction = QAction("Open", self)
        openAction.triggered.connect(self.mouseDoubleClickEvent)

        pwAction = QAction("set password", self)
        pwAction.triggered.connect(self.changePassword)

        # create the delete action
        deleteAction = QAction("delete", self)
        deleteAction.triggered.connect(self.delete)

        self.menu.addAction(openAction)
        self.menu.addAction(pwAction)
        self.menu.addAction(deleteAction)

        self.menu.exec_(self.mapToGlobal(event.pos()))

    def changePassword(self):

        check = False
        subCheck = False
        # get the new password from the text box
        if self.pw != "":
            # reconfirm the password
            pw, ok = QInputDialog.getText(self, "Password Prompt", "Enter the Password : ", echo=QLineEdit.Password)
            if ok and pw == self.pw:
                subCheck = True
            else:
                QMessageBox.warning(self, "Warning", "Password You Entered is Wrong! Please Enter Correct Password")

        else:
            subCheck = True

        # get the new pw from the user
        if subCheck:
            # get the new pw from the user
            new_pw, ok2 = QInputDialog.getText(self, "New Password Dialog", "Enter the New Password : ",
                                               echo=QLineEdit.Password)
            if ok2:
                # confirm the password from the user
                confirm_pw, ok3 = QInputDialog.getText(self, "Confirm Password Dialog", "Confirm the Password : ",
                                                       echo=QLineEdit.Password)
                if ok3 and confirm_pw == new_pw:
                    check = True
                else:
                    QMessageBox.warning(self, "Warning",
                                        "Confirm Password is not correct...Please Enter the Correct Password")

        if check:
            # change the password from the data base and current widget
            self.pw = new_pw
            # create the connection to the data base
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()

            cursor.execute(
                f" UPDATE book_table SET pw = '{self.pw}' WHERE book_id = '{self.book_id}'  ")
            # save the changes
            connection.commit()
            connection.close()

    def keyPressEvent(self, event : QKeyEvent) -> None:
        print("Key Press")
        if event.key() == Qt.Key_Delete:
            self.delete()

    def getInitialState(self):

        user_data = []
        with open(favorite_file, "r") as file:
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
        with open(favorite_file, "r") as file:
            user_data = json.load(file)
        if state:

            # add the book to the file
            user_data.append({
                        "type" : "book",
                        "id" : self.book_id,
                        "title" : self.title,
                        "path" : self.path,
                        "pw" : self.pw

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
        with open(favorite_file, "w") as file:
            json.dump(user_data, file, indent=4)
        # set the current button state
        self.setState()

    def delete(self):

        check = True
        if self.pw != "":
            text, ok = QInputDialog.getText(self, "Password Dialog" ,"Type the Password : ", echo=QLineEdit.Password)
            if ok:
                if text != self.pw:
                    check = False
                    QMessageBox.warning(self, 'Password warning', "Wrong Password , Please Try again!")
            else:
                check = False

        message = QMessageBox.StandardButton.No
        if check:
            message = QMessageBox.warning(self, "Delete Message", f"Are you sure to Delete Book {self.title} ?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if message == QMessageBox.StandardButton.Yes:
            # remove from the book table
            connect = sqlite3.connect(db_file)
            cursor = connect.cursor()

            try:
                cursor.execute(f"DELETE FROM book_table WHERE book_id = '{self.book_id}' ")
            except:
                pass
            connect.commit()
            connect.close()

            # delete from the book json file
            book_data = {}
            with open(book_file) as file:
                book_data = json.load(file)

            book_data.pop(self.book_id)

            with open(book_file, 'w') as file:
                json.dump(book_data, file, indent=4)
            del book_data

            # remove from the favorite json file
            if self.addFavoriteButton.isChecked():
                fav_data = []
                with open(favorite_file) as file:
                    fav_data = json.load(file)

                for i in fav_data:
                    if i['type'] == 'book' and i['id'] == self.book_id:
                        fav_data.remove(i)
                        break

                with open(favorite_file, 'w') as file:
                    json.dump(fav_data, file, indent=4)

            # finnaly delete the widget
            self.deleteLater()
            print("[INFO] successfully delete the book from the system...")

    @staticmethod
    def getIdentifire():

        length = 7
        index_str = ""

        for i in range(length):
            index_str += random.choice(chrs)

        return index_str

    def loadCover(self):

        pass

class boxBookWidget(bookWidget):
    def __init__(self, title, book_id, path, pw = ""):
        super(boxBookWidget, self).__init__(title, book_id, path, pw)

        # set the widget size settings
        self.setMaximumSize(QSize(600, 400))

        self.coverImageLabel.setFixedSize(QSize(250, 300))

        self.titleLabel.setWordWrap(True)

        self.coverImageLabel.mousePressEvent = lambda e: self.popUpImage()

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

       # set the pix map
        self.coverImageLabel.setPixmap(
            QPixmap(self.default_cover_imageDir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

    def loadCover(self):

        try:
            # load the pdf cover image
            with open(book_file) as file:
                bookData = json.load(file)

            dir = bookData.get(self.book_id).get("dir")
            # load the document
            doc = fitz.Document(dir)
            page1 = doc.load_page(0)

            pic = page1.get_pixmap()
            self.image_dir = f"db/temp/image{bookWidget.getIdentifire()}.png"

            pic.save(self.image_dir)
            # close the document
            doc.close()

            self.coverImageLabel.setPixmap(
                QPixmap(self.image_dir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
        except:
            pass

    def popUpImage(self):

        return None
        # create the Image Label
        self._label = QLabel()
        self._label.setPixmap(
            QPixmap(self.image_dir).scaled(QSize(500, 400), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self._label.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._label.setGeometry(QRect(self.coverImageLabel.mapToGloabl(self.coverImageLabel.rect().bottomLeft()), QSize(500, 400)))
        self._label.show()


class listBookWidget(bookWidget):
    def __init__(self, title, book_id, path, pw = ""):
        super(listBookWidget, self).__init__(title, book_id, path, pw)

        # set the widget size settings
        self.setMaximumHeight(150)

        self.coverImageLabel.setFixedSize(QSize(50, 50))
        # create the grid
        gridLyt = QGridLayout()
        gridLyt.addWidget(self.titleLabel, 0, 1)
        gridLyt.addWidget(self.coverImageLabel, 0, 0)
        # gridLyt.addLayout(self.formLyt, 1, 1)
        gridLyt.addWidget(self.addFavoriteButton, 0, 2)

        self.baseWidget.setLayout(gridLyt)


        # set the pix map
        self.coverImageLabel.setPixmap(
            QPixmap(self.default_cover_imageDir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio,
                                                            Qt.FastTransformation))

    def loadCover(self):

        try:
            # load the pdf cover image
            with open(book_file) as file:
                bookData = json.load(file)

            dir = bookData.get(self.book_id).get("dir")
            # load the document
            doc = fitz.Document(dir)
            page1 = doc.load_page(0)

            pic = page1.get_pixmap()
            image_dir = f"db/temp/image{bookWidget.getIdentifire()}.png"

            pic.save(image_dir)
            # close the document
            doc.close()

            self.coverImageLabel.setPixmap(
                QPixmap(image_dir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
        except:
            pass
