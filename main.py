# This is a sample Python script
import json
import os, sqlite3
import sys, random
from style_sheet import dark_style_sheet

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow , QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QRadioButton,
                             QGroupBox, QScrollArea, QDialog, QFileDialog, QTabWidget, QTabBar)
from PyQt5.Qt import QFont, Qt, QSize, QTime, QDate
from librarayWidgets import boxCollectionWidget, listCollectionWidget, switchButton, collectionWidget
from dialogs import newCollectionDialog
from PyQt5.QtGui import QColor, QPalette
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

chrs = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class Stage:
    def __init__(self):
        self.bookWidgets = list()
        self.collectionWidgets = list()

        # create the info list
        self.books = list()
        self.collections = list()

        # set the selected widget
        self.selected_widget = None

    def addBook(self, bookWidget , bookInfo ):
        self.bookWidgets.append(bookWidget)
        self.books.append(bookInfo)

    def addCollection(self, collectionWidget, collectionInfo):
        self.collectionWidgets.append(collectionWidget)
        self.collections.append(collectionInfo)

    def WidgetCount(self):

        return len(self.collectionWidgets) + len(self.bookWidgets)

    def clear(self):

        self.collectionWidgets.clear()
        self.bookWidgets.clear()
        self.books.clear()
        self.collections.clear()

        self.selected_widget = None


class LibraryMangementSystem(QMainWindow):
    def __init__(self):
        # initilaize the class
        super(LibraryMangementSystem, self).__init__()
        # handle the file system and data bases
        self.setUpDataBases()
        self.initializeUI()

    def setUpDataBases(self):

        self.db_file = "db/data.db"
        # create hte db and images folder if doen not exist
        if not os.path.exists("db"):
            os.mkdir("db")
        if not os.path.exists("images"):
            os.mkdir("images")

        if not os.path.exists("db/collection.json"):
            with open("db/collection.json", "w") as file:
                json.dump({}, file, indent=4)

        if not os.path.exists("db/book.json"):
            with open("db/book.json", "w") as file:
                json.dump({}, file, indent=4)



        if not os.path.exists(self.db_file):
            # create the data base and json files for system
            # create the connection and add the data bases tables
            connection = sqlite3.connect("db/data.db")
            # create the cursor object
            cursor = connection.cursor()
            # execute the sqlite command for create the table
            cursor.execute(f""" CREATE TABLE collection_table (id INTEGER PRIMARY KEY AUTOINCREMENT  UNIQUE NOT NULL,
                                                                        collection_id TEXT UNIQUE NOT NULL,
                                                                        path TEXT NOT NULL,
                                                                        name TEXT NOT NULL,
                                                                        date TEXT NOT NULL,
                                                                        time TEXT NOT NULL,
                                                                        pw TEXT)""")
            cursor.execute("""CREATE TABLE book_table (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                                                book_id TEXT UNIQUE NOT NULL,
                                                                path TEXT NOT NULL,
                                                                date TEXT NOT NULL,
                                                                time TEXT NOT NULL,
                                                                pw TEXT NOT NULL)""")
            # save the changes
            connection.commit()
            connection.close()
            print("[INFO] data bases file created successfull...")


    def initializeUI(self):

        # set the windwo width and height
        self.width = 2000
        self.height = 1000

        # first consider about the
        self.setWindowTitle("Library Management System v0.0.1")
        self.setGeometry(0, 0, self.width, self.height)

        # create the mai widgets
        self.setUpWidgets()
        self.setStyleSheet(dark_style_sheet)

        # show the window in the screen
        self.show()

    def setUpWidgets(self):

        # create the various widgets and layout it
        # create the main widgets
        self.mainWidgets = QWidget()
        self.mainWidgets.setObjectName("mainWidget")
        self.mainWidgets.setContentsMargins(0, 0, 0, 0)
        # set as the central window
        self.setCentralWidget(self.mainWidgets)

        # create the sub widgets
        self.barWidget = QWidget()
        self.barWidget.setFixedWidth(int(self.width * 0.2))
        self.barWidget.setContentsMargins(0, 0, 0, 0)
        self.barWidget.setObjectName("barWidget")

        # create the barOther Widget
        barOtherWidget = QWidget(self.mainWidgets)
        barOtherWidget.setContentsMargins(0, 0, 0, 0)
        # create the layout and pack them
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)
        hbox1.addWidget(self.barWidget)
        hbox1.addWidget(barOtherWidget)

        self.mainWidgets.setLayout(hbox1)


        # create the top title bar widget
        self.titleBaridget = QWidget()
        self.titleBaridget.setFixedHeight(int(self.height * 0.08))
        self.titleBaridget.setObjectName("titleBarWidget")
        # create the tool bar widget
        self.toolBarWidget = QWidget()
        self.toolBarWidget.setFixedHeight(int(self.height * 0.18))
        self.toolBarWidget.setObjectName("toolBarWidget")
        # create the space widget
        spaceWidget = QWidget()
        spaceWidget.setObjectName("spaceWidget")
        spaceWidget.setContentsMargins(0, 0, 0, 0)

        # create the vbox for pack this widgets
        vbox1 = QVBoxLayout()
        vbox1.setSpacing(0)
        vbox1.addWidget(self.titleBaridget)
        vbox1.addWidget(self.toolBarWidget)
        vbox1.addWidget(spaceWidget)

        barOtherWidget.setLayout(vbox1)

        # create the stage widget and reminders widget
        self.stageWidget = QWidget()
        self.stageWidget.setObjectName("stageWidget")

        self.reminderWidget = QWidget()
        self.reminderWidget.setFixedWidth(int(self.width * 0.15))
        self.reminderWidget.setObjectName("reminderWidget")

        # create the other h box for pack them
        hbox2 = QHBoxLayout()
        hbox2.setSpacing(0)
        hbox2.addWidget(self.stageWidget)
        hbox2.addWidget(self.reminderWidget)

        spaceWidget.setLayout(hbox2)

        # configure the above widget then
        self.setUpTitleBarWidget()
        self.setUpToolBarWidget()
        self.setUpStageWidget()
        self.setUpRemiderWidget()

    def setUpTitleBarWidget(self):

        # crate the title label
        title_label = QLabel("Library Management System")
        title_label.setFont(QFont("verdana", 27))
        title_label.setAlignment(Qt.AlignRight)
        title_label.setObjectName("title_label")

        # create the h box for pack the label
        hbox = QHBoxLayout()
        hbox.addWidget(title_label)

        self.titleBaridget.setLayout(hbox)

    def setUpToolBarWidget(self):

        # create the search bar for library system
        self.searchBar = QLineEdit()
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setMinimumSize(QSize(400, 50))
        # self.searchBar.setMaximumSize(QSize(500, 60))
        self.searchBar.setPlaceholderText("search anything")
        self.searchBar.setAlignment(Qt.AlignRight)
        # create the grid layout for pack the searchBar

        grid_lyt = QGridLayout()
        grid_lyt.setSpacing(0)

        grid_lyt.addWidget(self.searchBar, 1, 1, 1, 4)

        # create the group box for pack the radio buttons
        group_box = QGroupBox()
        group_box.setMaximumSize(QSize(700, 50))

        # create the radio buttons
        searchOptions = ["Only Books", "Only Collections", "Both of them", "From Everything"]
        searchOptionRadioButtons = []
        # create the v box layout
        h_box_radios = QHBoxLayout()
        for item in searchOptions:
            # create the radio button and pack to the layout
            radio_new = QRadioButton(item)
            radio_new.setObjectName("searchOptionRadioButton")
            # add to the layout
            h_box_radios.addWidget(radio_new)
            # add to teh list
            searchOptionRadioButtons.append(radio_new)

        # set the layout ot the group box
        group_box.setLayout(h_box_radios)
        grid_lyt.addWidget(group_box, 0, 1, 1, 3)

        # create the button for new collection or add book
        self.addButton = QPushButton("+")
        self.addButton.setObjectName("addButton")
        self.addButton.setFont(QFont("verdana", 25))
        self.addButton.pressed.connect(self.addNewItem)
        # add to the grid
        grid_lyt.addWidget(self.addButton, 1, 0, 1, 1)

        # create the theme box
        self.themeBox = switchButton("list theme" , "box theme", "list", "box")
        self.themeBox.switchSignal.connect(self.refreshPage)
        grid_lyt.addWidget(self.themeBox, 0, 0)

        # create the refresh button
        refreshButton = QPushButton("refresh")
        refreshButton.pressed.connect(self.refreshPage)
        grid_lyt.addWidget(refreshButton, 0, 4)

        # set the toolBar widget ;layout as the grid_lyt
        self.toolBarWidget.setLayout(grid_lyt)

    def setUpStageWidget(self):
        # create the scroll widget
        scroll_area = QScrollArea()
        scroll_area.setObjectName("mainScrollArea")

        # create the stage area widget for scroll area
        self.stageArea = QWidget()
        self.stageArea.setObjectName("stageArea")
        scroll_area.setWidget(self.stageArea)
        scroll_area.setWidgetResizable(True)
        # create the layout base the theme
        if self.getTheme() == "list":
            self.stageLayout = QVBoxLayout()
        else:
            self.stageLayout = QGridLayout()

        self.stageArea.setLayout(self.stageLayout)
        # add scroll area to the stage widget
        vbox = QVBoxLayout()
        vbox.addWidget(scroll_area)

        self.stageWidget.setLayout(vbox)


        # set the important fileds for system
        self.currentPath = "/"
        self.currentStage = Stage()

        # render the root page
        self.renderNewPageForCollection(self.currentPath)

    def setUpRemiderWidget(self):

        # create the tab view for this widget
        self.reminderTab = QTabWidget()
        self.reminderTab.setObjectName("reminderTab")

        # create the two widgets for tab widgets
        self.statusWidget = QWidget()
        self.statusWidget.setObjectName("statusWidget")
        # create the reminders note widget
        self.reminderNoteWidget = QWidget()
        self.reminderNoteWidget.setObjectName("reminderNoteWidget")

        # add to the tab widget
        self.reminderTab.addTab(self.statusWidget, "Status")
        self.reminderTab.addTab(self.reminderNoteWidget, "Reminders")

        # create the vbox for tab
        vbox = QVBoxLayout()
        vbox.addWidget(self.reminderTab)
        self.reminderWidget.setLayout(vbox)

        self.setUpStatusWidget()

    def setUpStatusWidget(self):

        pass

    def addNewItem(self):

        # pop up the new dialog for choose the collection or book
        self.selectDialog = QDialog(self)
        self.selectDialog.setModal(True)
        self.selectDialog.resize(200, 200)
        self.selectDialog.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.selectDialog.setContentsMargins(0, 0, 0, 0)

        # create the two buttons
        button1 = QPushButton("add Collection")
        button2 = QPushButton("Add Book")

        button1.setObjectName("selectButton")
        button2.setObjectName("selectButton")

        button1.pressed.connect(lambda e = "collection" : self.responeOfSelectDialog(e))
        button2.pressed.connect(lambda e = "book" : self.responeOfSelectDialog(e))

        # create the lyt
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addWidget(button1)
        vbox.addWidget(button2)

        self.selectDialog.setLayout(vbox)
        self.selectDialog.show()

    def responeOfSelectDialog(self, text):

        # close the dialog box
        self.selectDialog.close()

        if text == "collection":
            # create the new collection dialog box
            dialogNew = newCollectionDialog(self)
            if dialogNew.exec_():
                # get the information from the dialog
                data = dialogNew.info_dict
                self.addNewCollection(data)

        else:
            # open the file dialog
            files , ok = QFileDialog.getOpenFileNames(self, "Choose Books", "", "PDF Files(*.pdf)")
            if ok:
                pass

    def addNewCollection(self, data : dict):

        title = data["title"]
        des = data["description"]
        img = data["image_dir"]
        # get the current time and date
        current_time = QTime.currentTime().toString("hh:mm:ss AA")
        current_date = QDate.currentDate().toString("dd:MM:yyyy")

        # generate the id
        id_code = self.generateCollectionID()
        path = f"{self.currentPath}{self.generatePath(self.currentPath)}/"

        # create the connection and open the cursor
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute(f""" INSERT INTO collection_table(collection_id, path, name, date, time, pw) VALUES('{id_code}', '{path}', '{title}'
                                                                                                            , '{current_date}', '{current_time}',
                                                                                                                    '') """)
        # save changes and close the connection
        connection.commit()
        connection.close()

        #now open the json file
        with open("db/collection.json", "r") as file:
            user_data = json.load(file)

        user_data[id_code] = {"title" : title,
                              "description" : des,
                              "image_dir" : img}

        with open("db/collection.json", "w") as file:
            json.dump(user_data, file, indent=4)

        # now create the new widget
        if self.getTheme() == "list":
            collection_widget = listCollectionWidget(title, des, img, path)
        else:
            collection_widget = boxCollectionWidget(title, des, img, path)
        # set the event handler
        collection_widget.mouseDoubleClickEvent = (lambda a, e = collection_widget.path : self.openNewPage(e))
        collection_widget.mousePressEvent = (lambda a, e = collection_widget : self.setSelectedWidget(e))

        info_data = {"title" : title,
                     "description" : des,
                     "path" : path,
                     "image_dir" : img,
                     "date" : current_date,
                     "time" : current_time}
        self.currentStage.addCollection(collection_widget, info_data)

        # add to the layout
        if self.getTheme() == "list":
            self.stageLayout.addWidget(collection_widget)
        else:
            # get the length of widgets
            count = self.currentStage.WidgetCount() - 1
            self.stageLayout.addWidget(collection_widget, count//4, count%4)

    def openNewPage(self, newPath : str):

        # set the new path as the newPath
        self.currentPath = newPath
        # delete the all of widgets
        for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
            widget.deleteLater()

        # clear the stage
        self.currentStage.clear()

        # render the new page
        self.renderNewPageForCollection(self.currentPath)

    def refreshPage(self):

        # clear the currentStage
        for widget in [*self.currentStage.collectionWidgets, *self.currentStage.bookWidgets]:
            widget.deleteLater()
        self.stageLayout.deleteLater()
        self.currentStage.clear()

        # set the layout based on the theme
        if self.getTheme() == "list":
            self.stageLayout = QVBoxLayout()
        else:
            self.stageLayout = QGridLayout()
        self.stageArea.setLayout(self.stageLayout)

        # render the page again
        self.renderNewPageForCollection(self.currentPath)

    def renderNewPageForCollection(self, path : str):

        # get the path you need to open
        filterPaths = self.getNeedPaths(path)

        # get the information about the paths
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM collection_table")
        data = cursor.fetchall()
        # close the connection
        cursor.close()

        # open the json file
        coll_data = {}
        with open("db/collection.json", "r") as file:
            coll_data = json.load(file)

        # generate the new dict for this
        filter_data = []
        for i in range(len(data)):
            if (data[i][2] in filterPaths):
                new_dict = {"title" : data[i][3],
                            "description" : coll_data.get(data[i][1])["description"],
                            "path" : data[i][2],
                            "image_dir" : coll_data.get(data[i][1])["image_dir"],
                            "date" : data[i][4],
                            "time" : data[i][5]}
                filter_data.append(new_dict)

        self.addCollectionWidgets(filter_data)

    def addCollectionWidgets(self, FilterData : list):


        for data in FilterData:
            # create the new widget
            if self.getTheme() == "list":
                widget = listCollectionWidget(data["title"], data["description"], data["image_dir"], data["path"])
                self.stageLayout.addWidget(widget)
            else:
                widget = boxCollectionWidget(data["title"], data["description"], data["image_dir"], data["path"])
                count = self.currentStage.WidgetCount()
                self.stageLayout.addWidget(widget, (count) // 4, (count) % 4)

            widget.mouseDoubleClickEvent = (lambda a, e = widget.path : self.openNewPage(e))

            # add the widget to stage
            self.currentStage.addCollection(widget, data)

    def setSelectionWidget(self, widget : collectionWidget):

        # set thr stage selected widget as the this
        self.currentStage.selected_widget = collectionWidget
        # update the status
        self.setStatus()

    def setStatus(self):

        pass


    def getNeedPaths(self, rootPath):

        # create trh connection
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT path FROM collection_table")
        data = cursor.fetchall()

        connection.close()

        data = [item[0] for item in data]
        # filter the paths that starts with given path
        newData = []
        for item in data:
            # print("{} -- {} >> {}".format(len(item.split("/")) , len(rootPath.split("/")), item))
            if not ((not item.startswith(rootPath)) or (len(item.split("/")) - len(rootPath.split("/")) != 1)):
                newData.append(item)



        # return the filtering oaths
        return newData

    def generatePath(self, path : str):

        # create the connection
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT path from collection_table")
        data = cursor.fetchall()
        connection.close()

        data = [item[0] for  item in data]
        # filter current paths
        tempData = []
        for item in data:
            if not (not item.startswith(path) or ((len(item.split("/")) - len(path.split("/"))) != 1)):
                tempData.append(item)
        data = tempData

        newData = []
        for item in data:
            newData.append(int(item.split("/")[-2]))

        if newData == []:
            return 0
        else:
            return max(newData) + 1

    def generateCollectionID(self):

        # generate the 5 digits code for collection
        # first create the connection and get the current ids
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT collection_id FROM collection_table")
        data = cursor.fetchall()

        data = [item[0] for item in data]
        # generate the new code
        code = ""
        for i in range(5):
            code += random.choice(chrs)

        while (code in data):
            code = ""
            for i in range(5):
                code += random.choice(chrs)

        connection.close()
        return code

    def getTheme(self):

        # call to the theme box get state method
        theme = self.themeBox.getState()
        return theme


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create the application object
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Shadow, QColor(25, 25, 25))
    palette.setColor(QPalette.Window, QColor(10, 10, 10))
    palette.setColor(QPalette.WindowText, QColor("white"))
    palette.setColor(QPalette.Base, QColor(10, 10, 10))
    palette.setColor(QPalette.AlternateBase, QColor(10, 10, 10))
    palette.setColor(QPalette.ToolTipBase, QColor('white'))
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(43, 43, 43))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.ColorRole.Dark, QColor(0, 0, 0))

    palette.setColor(QPalette.Highlight, QColor(250, 70, 8))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)

    window = LibraryMangementSystem()
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
