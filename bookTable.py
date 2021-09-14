import os.path
import random
import sys, json ,sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox
from PyQt5.QtGui import QFont, QColor, QImage, QIcon, QPixmap
from PyQt5.Qt import QSize, Qt, QAbstractTableModel , QModelIndex, QHeaderView
# import the book Space widgets
from book_space import BookArea

db_file = "db/data.db"
book_file = "db/book.json"
favorite_file = "db/favorite.json"

class bookTable(QWidget):

    def __init__(self):
        super(bookTable, self).__init__()
        self.setGeometry(0, 0, 2000, 1000)
        self.initializeUI()
        self.setUpToolBar()

    def initializeUI(self):

        # create the table view and set the table model
        self.table_view = QTableView()

        self.model = TableModel()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # hide the last column of h table view
        self.table_view.hideColumn(9)
        # set the signal slots for tableview
        self.table_view.verticalHeader().sectionDoubleClicked.connect(self.openBook)
        self.table_view.verticalHeader().sectionClicked.connect(self.displayBook)
        self.table_view.doubleClicked.connect(self.openBookFromCell)

        # table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # create the tool bar layout
        self.toolBarLyt = QGridLayout()
        self.toolBarLyt.setSpacing(0)

        # create the vbox layout
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addLayout(self.toolBarLyt)
        vbox.addWidget(self.table_view)

        self.setLayout(vbox)
        self.show()

    def setUpToolBar(self):


        # create the search bar for tableview Model
        self.searchBar = QLineEdit()
        self.searchBar.resize(250, 30)
        self.searchBar.textChanged.connect(self.searchBooks)

        searchLabel = QLabel("search books")

        # crate the sort combo box
        sortLabel = QLabel("Sort")
        self.sort_comboBox = QComboBox()
        self.sort_option = {"sort By Name" : 0,
                            "sort by Size" : 4,
                            "sor By Index" : 1,
                            "sort By Path" : 2,
                            "sort By added Date" : 3}
        for key, value in self.sort_option.items():
            self.sort_comboBox.addItem(key, value)
        self.sort_comboBox.currentTextChanged.connect(self.changeSortings)

        self.toolBarLyt.addWidget(searchLabel, 1, 0)
        self.toolBarLyt.addWidget(self.searchBar, 1, 1,1, 3)
        self.toolBarLyt.addWidget(self.sort_comboBox, 0, 3)
        self.toolBarLyt.addWidget(sortLabel, 0, 2)

    def searchBooks(self, text):

        for i, book in enumerate(self.model._data):
            name = book[1]
            if text.lower() not in name.lower():
                self.table_view.hideRow(i)
            else:
                self.table_view.showRow(i)

    def changeSortings(self, option : str):

        sort_id = self.sort_option.get(option)

        if sort_id == 0:
            self.model._data.sort(key = lambda e : e[1])
        elif sort_id == 1:
            self.model._data.sort(key = lambda e : e[0])
        elif sort_id == 2:
            self.model._data.sort(key = lambda e : e[2])
        elif sort_id == 3:
            self.model._data.sort(key = lambda e : e[5])
        elif sort_id == 4:
            self.model._data.sort(key = lambda e : e[3])
        self.model.layoutChanged.emit()

    def openBookFromCell(self, index : QModelIndex):

        row =index.row()
        self.openBook(row)

    def openBook(self, index : int):

        # get the sel.model row data
        row_data = self.model._data[index]
        book_id = row_data[-1]

        # create the new book area widget and show it
        self.book_area = BookArea(book_id)
        self.book_area.show()

    def displayBook(self, index):

        row_data = self.model._data[index]
        book_name = row_data[1]
        size = row_data[3]

        print(f"{book_name} size = {size}")



class TableModel(QAbstractTableModel):

    lock_image = "images/sys_images/lock.png"
    fav_image = "images/sys_images/fillStar.png"
    un_fav_image = "images/sys_images/nonFillStar.png"

    COLORS = ['#053061', '#2166ac', '#4393c3', '#92c5de', '#d1e5f0',
              '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b', '#67001f']

    # defined the levels colors
    level_color = [QColor(0, 0, 150), QColor(0, 0, 140), QColor(0, 0, 130), QColor(0, 0, 120), QColor(0, 0, 110), QColor(0, 0, 100)]

    def __init__(self):
        super(TableModel, self).__init__()
        self._data = []
        self.loadData()

    def loadData(self):

        # create the connection
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM book_table")
        db_data = cursor.fetchall()

        connection.close()

        # open the book json file
        book_json_data = []
        with open(book_file) as file:
            book_json_data = json.load(file)

        fav_data = []
        with open(favorite_file) as file:
            fav_data = json.load(file)

        # modify and filter the data and append to the self._data
        for i, item in enumerate(db_data):
            book_id = item[1]
            # get the book dir name
            dir = book_json_data.get(book_id).get("dir")
            name = os.path.split(dir)[1]
            date, time , path, pw = item[3], item[4], item[2], item[5]

            # get the os data of the book
            status_obj = os.stat(dir)
            size = TableModel.sizeInMB(status_obj.st_size)
            mod_date = status_obj.st_atime

            isFav = False
            for j in fav_data:
                if j["type"] == "book" and j["id"] == book_id:
                    isFav = True
                    break
            # append to the self._data
            self._data.append([i , name , path , size ,dir , f"{date} at {time}", mod_date , pw, isFav, book_id])


    @staticmethod
    def sizeInMB(size) -> float:
        return (size/1024)/1024

    def data(self, index: QModelIndex, role: int):

        row, column = index.row(), index.column()

        if role == Qt.DisplayRole:

            if column == 7:
                if self._data[row][column] == "":
                    return "UnSecured"
                else:
                    return "Secured"
            elif column == 8:

                if self._data[row][column]:
                    return "yes"
                else:
                    return "no"
            elif column == 3:
                return "{:.2f} MB".format(self._data[row][column])

            return  self._data[row][column]

        elif role == Qt.BackgroundRole:

            if column == 11:
                if self._data[row][column] == "":
                    return QColor(255, 0, 0)
                else:
                    return QColor(0, 255, 0)
            elif column == 2:
                level = len(self._data[row][column].split("/")) - 2
                return self.level_color[level]

            elif column == 0:
                return QColor(0, 0, random.randint(0, 100))

            elif column == 3:
                value = int(self._data[row][column])

                value = max(value, -5)
                value = min(value, 5)
                value += 5

                return QColor(self.COLORS[value])

        elif role == Qt.DecorationRole:

            if column == 7:
                if self._data[row][column] != "":
                    return QIcon(self.lock_image)
                else:
                    return QColor(200, 0, 0)

            elif column == 8:
                if self._data[row][column]:
                    return QIcon(self.fav_image)
                else:
                    return QIcon(self.un_fav_image)


    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._data)


    def columnCount(self, parent: QModelIndex) -> int:
        return len(self._data[0])


if __name__ == "__main__":
    app = QApplication([])
    window = bookTable()

    app.setStyleSheet("""
    
                    QTableView {background-color : rgb(20, 20, 20);
                                color : white;}
                                """)

    app.exec_()
