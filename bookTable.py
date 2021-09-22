import os.path
import random, fitz
import sys, json ,sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QComboBox, QSplitter
from PyQt5.QtGui import QFont, QColor, QImage, QIcon, QPixmap
from PyQt5.Qt import QSize, Qt, QAbstractTableModel , QModelIndex, QHeaderView
# import the book Space widgets
from book_space import BookArea
from libraray_widgets.other_widgets import StatusWidget
from style_sheet import dark_theme_for_table

db_file = "db/data.db"
book_file = "db/book.json"
favorite_file = "db/favorite.json"

chrs = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class bookTable(QWidget):

    temp_imgs = []

    def __init__(self):
        super(bookTable, self).__init__()
        self.setGeometry(0, 0, 2000, 1000)
        self.initializeUI()
        self.setUpToolBar()

        self.setStyleSheet(dark_theme_for_table)

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
        self.table_view.clicked.connect(lambda e : self.displayBook(e.row()))

        # table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # create the tool bar layout
        self.toolBarLyt = QGridLayout()
        self.toolBarLyt.setSpacing(0)

        # create the vbox layout
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addLayout(self.toolBarLyt)
        vbox.addWidget(self.table_view)

        # create the two widget for table view and display view
        tableWidget = QWidget()
        displayWIdget = QWidget()
        # initiate the book data display widget
        self.book_data_display_widget = None
        # crate the display widget layout
        self.displayWidgetLyt = QVBoxLayout()

        tableWidget.setLayout(vbox)
        displayWIdget.setLayout(self.displayWidgetLyt)

        # create the splitter for split the table and display windowo
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(tableWidget)
        self.splitter.addWidget(displayWIdget)

        # create the parent layout
        parent_lyt = QHBoxLayout()
        parent_lyt.addWidget(self.splitter)
        self.setLayout(parent_lyt)
        self.show()

    def setUpToolBar(self):


        # create the search bar for tableview Model
        self.searchBar = QLineEdit()
        self.searchBar.resize(250, 50)
        self.searchBar.setTextMargins(5, 5, 5, 5)
        self.searchBar.setFont(QFont('verdana', 13))
        self.searchBar.textChanged.connect(self.searchBooks)

        searchLabel = QLabel("search books")

        # crate the sort combo box
        sortLabel = QLabel("Sort")
        self.sort_comboBox = QComboBox()
        self.sort_comboBox.setCurrentText("Sort")
        self.sort_option = {"Book Name" : 0,
                            "Size" : 1,
                            "Path" : 2,
                            "Added Date" : 3}
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
            self.model._data.sort(key = lambda e : e[0])
        elif sort_id == 1:
            self.model._data.sort(key = lambda e : e[2])
        elif sort_id == 2:
            self.model._data.sort(key = lambda e : e[1])
        elif sort_id == 3:
            self.model._data.sort(key = lambda e : e[4])

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
        book_path = row_data[3]
        book_name = row_data[0]
        size = row_data[2]
        path = row_data[1]

        try:
            self.book_data_display_widget.deleteLater()
        except:
            pass

        # create the new display widget
        self.book_data_display_widget = StatusWidget()
        self.book_data_display_widget.setMaximumHeight(1500)
        # add the image  and pass the image size
        self.book_data_display_widget.addImage(self.getImage(book_path), QSize(400, 800))
        # set the title
        self.book_data_display_widget.addLine("Book Name ", book_name, True)
        self.book_data_display_widget.addLine("Size ", "{:.2f} MB".format(size))
        # add the path of the book
        self.book_data_display_widget.addLine("Path ", path, wrap=True)
        self.book_data_display_widget.addLine("Sys Path ", book_path, wrap = True)

        # add to the display layout
        self.displayWidgetLyt.addWidget(self.book_data_display_widget)

    def getImage(self, doc_dir : str):

        document  = fitz.Document(doc_dir)
        page = document.load_page(0)

        coverImage = page.get_pixmap()
        # save the image and return the image path
        image_path = f"db/temp/tableViewCoverImage{bookTable.getIdentifire()}.png"
        self.temp_imgs.append(image_path)

        coverImage.save(image_path)
        return image_path

    @staticmethod
    def getIdentifire():

        length = 7
        index_str = ""

        for i in range(length):
            index_str += random.choice(chrs)

        return index_str

    def closeEvent(self, event) -> None:

        # remove the temp page images
        for path in self.temp_imgs:
            try:
                os.remove(path)
            except FileNotFoundError:
                print("Cannot find the File")
            except PermissionError:
                print("cannot delete the file bacause permission not getted")
            except OSError:
                print("OS error")
            except Exception:
                print("Cannot delete because another error")


# end of the UI Window

class TableModel(QAbstractTableModel):

    lock_image = "images/sys_images/lock.png"
    fav_image = "images/sys_images/fillStar.png"
    un_fav_image = "images/sys_images/nonFillStar.png"
    unlock_image = "images/sys_images/unlock.png"

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

        # load the path data from the collection table
        cursor.execute("SELECT path , name FROM collection_table")
        self.coll_data = cursor.fetchall()

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
            self._data.append([name , self.getStringPath(path) , size ,dir , f"{date} at {time}", mod_date , pw, isFav, book_id])




    @staticmethod
    def sizeInMB(size) -> float:
        return (size/1024)/1024

    def data(self, index: QModelIndex, role: int):

        row, column = index.row(), index.column()

        if role == Qt.DisplayRole:

            if column == 6:
                if self._data[row][column] == "":
                    return "UnSecured"
                else:
                    return "Secured"
            elif column == 7:

                if self._data[row][column]:
                    return "yes"
                else:
                    return "no"
            elif column == 2:
                return "{:.2f} MB".format(self._data[row][column])

            return  self._data[row][column]

        elif role == Qt.BackgroundRole:

            if column == 10:
                if self._data[row][column] == "":
                    return QColor(255, 0, 0)
                else:
                    return QColor(0, 255, 0)
            elif column == 1:
                level = len(self._data[row][column].split("/")) - 2
                return self.level_color[level]

            elif column == 0:
                return QColor(0, 0, random.randint(0, 100))

            elif column == 2:
                value = int(self._data[row][column])

                value = max(value, -5)
                value = min(value, 5)
                value += 5

                return QColor(self.COLORS[value])

        elif role == Qt.DecorationRole:

            if column == 6:
                if self._data[row][column] != "":
                    return QIcon(self.lock_image)
                else:
                    return QIcon(self.unlock_image)

            elif column == 7:
                if self._data[row][column]:
                    return QIcon(self.fav_image)
                else:
                    return QIcon(self.un_fav_image)


    def rowCount(self, parent: QModelIndex) -> int:
        return len(self._data)


    def columnCount(self, parent: QModelIndex) -> int:
        return len(self._data[0])

    def getStringPath(self, int_path : str):

        root_path = "/"
        str_path = ""

        split_path = int_path.split("/")
        for i in split_path:
            if i != "":
                root_path += f"{i}/"
                # get the coll data path
                for j in self.coll_data:
                    if j[0] == root_path:
                        plus_path = j[1]
                        break

                str_path += f"{plus_path}/"

        return str_path[:-1]

if __name__ == "__main__":
    app = QApplication([])
    window = bookTable()

    app.setStyleSheet("""
            
                    
                    QTableView {background-color : rgb(20, 20, 20);
                                color : white;}
                                """)

    app.exec_()
