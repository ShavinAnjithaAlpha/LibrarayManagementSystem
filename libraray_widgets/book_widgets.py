import json, sqlite3, random, fitz
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QFormLayout, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
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

    def keyPressEvent(self, event : QKeyEvent) -> None:

        if event.key() == Qt.Key_D:
            print("press delete")
            warning = QMessageBox.warning(self , "Delete Warning", "Are You Sure to Delete ?")

            if warning == QMessageBox.StandardButton.Yes:
                # delete the widget and from the data base
                connect = sqlite3.connect(db_file)
                cursor = connect.cursor()

                cursor.execute(f" DELETE FROM book_table WHERE book_id = '{self.book_id}' ")
                connect.commit()
                connect.close()
                # delete the widget
                self.deleteLater()

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
        with open(favorite_file, "w") as file:
            json.dump(user_data, file, indent=4)
        # set the current button state
        self.setState()

    @staticmethod
    def getIdentifire():

        length = 7
        index_str = ""

        for i in range(length):
            index_str += random.choice(chrs)

        return index_str


class boxBookWidget(bookWidget):
    def __init__(self, title, book_id, path):
        super(boxBookWidget, self).__init__(title, book_id, path)

        # set the widget size settings
        self.setMaximumSize(QSize(600, 400))

        self.coverImageLabel.setFixedSize(QSize(250, 300))

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
            # set the pix map
            self.coverImageLabel.setPixmap(
                QPixmap(self.default_cover_imageDir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))




class listBookWidget(bookWidget):
    def __init__(self, title, book_id, path):
        super(listBookWidget, self).__init__(title, book_id, path)

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

            print("2")
            pic.save(image_dir)
            print("2")
            # close the document
            doc.close()

            self.coverImageLabel.setPixmap(
                QPixmap(image_dir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
        except:
            # set the pix map
            self.coverImageLabel.setPixmap(
                QPixmap(self.default_cover_imageDir).scaled(self.coverImageLabel.size(), Qt.KeepAspectRatio,
                                                            Qt.FastTransformation))
