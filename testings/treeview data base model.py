import json, os
import sys, sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.Qt import Qt, QFont, QStandardItem, QStandardItemModel, QHeaderView
from PyQt5.QtGui import QColor, QIcon

class Modelitem(QStandardItem):
    def __init__(self, text, * ,type_ = "collection"):
        super(Modelitem, self).__init__()

        font = QFont('verdana', 11)
        font.setItalic(True)

        if type_ == "collection":
            image = QIcon("../images/sys_images/coll_img1.png")
        else:
            image = QIcon("../images/sys_images/book_small.png")
        self.setData(image, Qt.DecorationRole)

        self.setText(text)
        self.setFont(font)


class View(QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        self.setWindowTitle("Tree View for collection tree model")
        self.resize(500, 600)

        header_view = QHeaderView(Qt.Horizontal)

        self.treeView = QTreeView()
        self.treeView.setIndentation(70)
        self.treeView.setHeader(header_view)
        self.treeView.header().setStretchLastSection(True)

        self.treeView.expandAll()
        # open the data base file
        connect = sqlite3.connect("../db/data.db")
        cursor = connect.cursor()

        cursor.execute("SELECT path ,name FROM collection_table")
        self.data = cursor.fetchall()

        self.book = []
        self.loadBooks()

        connect.close()

        # create the model
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Name", "Date", "Time"])
        rootNode = model.invisibleRootItem()
        self.parent_path = "/"



        self.buildModel(self.parent_path, rootNode)
        self.treeView.setModel(model)

        self.treeView.expandAll()

        model.item(1).setCheckable(False)

        self.setCentralWidget(self.treeView)
        self.show()

    def loadBooks(self):

        connection = sqlite3.connect("../db/data.db")
        cursor = connection.cursor()

        cursor.execute("SELECT book_id, path FROM book_table")
        data = cursor.fetchall()

        connection.close()

        user_data = []
        with open("../db/book.json") as file:
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


if __name__ == "__main__":
    app = QApplication([])
    window = View()

    app.setStyle("Fusion")

    app.setStyleSheet("""
                            QTreeView {background : none;
                                    color : white;
                                    padding : 2px;}
                                    
                            QTreeView::item {background-color : rgb(25, 25, 25);}
                            
                            QTreeView::item:hover {background-color : rgb(200, 0, 0)}
                            
                            QTreeView:closed {background-color : rgb(0, 0, 50)}
                            
                            QTreeView:opened {background-color : rgb(0, 0, 80)}
                            
                            QTreeView::branch {background-color  : rgb(0, 0, 40);
                                                border-right : 1px solid red;}
                            """)


    app.exec_()






