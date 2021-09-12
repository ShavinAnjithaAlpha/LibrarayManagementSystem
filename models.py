import json
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt5.QtGui import QImage, QFont, QColor
from PyQt5.QtCore import QSize



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



class favoriteListModel(QAbstractListModel):

    json_file = "db/favorite.json"
    collectionImage = QImage("images/sys_images/coll_img1.png").scaled(QSize(35, 35), Qt.KeepAspectRatio, Qt.FastTransformation)
    bookImage = QImage("images/sys_images/book_small.png").scaled(QSize(35, 35), Qt.KeepAspectRatio, Qt.FastTransformation)

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
