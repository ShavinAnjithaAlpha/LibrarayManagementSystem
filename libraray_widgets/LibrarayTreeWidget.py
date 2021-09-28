import json, os
import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTreeView, QVBoxLayout
from PyQt5.Qt import Qt, QFont, QStandardItem, QStandardItemModel, QHeaderView
from PyQt5.QtGui import QColor, QIcon

db_file = "db/data.db"

class Modelitem(QStandardItem):
    def __init__(self, text, * ,type_ = "collection"):
        super(Modelitem, self).__init__()

        font = QFont('verdana', 11)
        font.setItalic(True)

        if type_ == "collection":
            image = QIcon("images/sys_images/smallCollIocn.png")
        else:
            image = QIcon("images/sys_images/smallBookIcon.png")
        self.setData(image, Qt.DecorationRole)

        self.setText(text)
        self.setFont(font)

class LibTreeView(QWidget):
    def __init__(self):
        super(LibTreeView, self).__init__()

        header_view = QHeaderView(Qt.Horizontal)

        self.treeView = QTreeView()
        self.treeView.setHeader(header_view)
        self.treeView.header().setStretchLastSection(True)

        # open the data base file
        connect = sqlite3.connect(db_file)
        cursor = connect.cursor()

        cursor.execute("SELECT path ,name FROM collection_table")
        self.data = cursor.fetchall()

        self.book = []
        self.loadBooks()

        connect.close()

        # create the model
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Item Name", ])
        rootNode = model.invisibleRootItem()
        self.parent_path = "/"



        self.buildModel(self.parent_path, rootNode)
        self.treeView.setModel(model)

        # create the vbox
        vbox = QVBoxLayout()
        vbox.addWidget(self.treeView)
        self.setLayout(vbox)

    def loadBooks(self):

        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT book_id, path FROM book_table")
        data = cursor.fetchall()

        connection.close()

        user_data = []
        with open("db/book.json") as file:
            user_data = json.load(file)

        for i in range(len(data)):
            name = user_data.get(data[i][0]).get("dir")
            path = data[i][1]

            self.book.append([name, path])


    def buildModel(self, parentRoot : str , parentItem : QStandardItem):

        # filter the data
        data = []
        books = []
        for i in self.data:
            path = i[0]
            if (path.startswith(parentRoot) and (len(path.split("/"))  - len(parentRoot.split("/"))) == 1):
                data.append(i)

        for i in self.book:
            path = i[1]
            if (path == parentRoot):
                books.append(i)

        if data != []:
            for item in data:
                # create the standard items
                model_item = Modelitem(item[1])
                model_item.setCheckable(True)
                self.buildModel(item[0], model_item)
                parentItem.appendRow(model_item)
        else:
            pass

        for item in books:
            book_item = Modelitem(os.path.split(item[0])[1], type_ = "book")
            parentItem.appendRow(book_item)

