# This is a sample Python script
import json
import os, sqlite3
import sys, random
from style_sheet import dark_style_sheet

from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow , QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QRadioButton,
                             QGroupBox, QScrollArea, QDialog, QFileDialog, QTabWidget, QComboBox, QListView)
from PyQt5.Qt import QFont, Qt, QSize, QTime, QDate, QPropertyAnimation, QEasingCurve, QModelIndex
from librarayWidgets import boxCollectionWidget, listCollectionWidget, switchButton, collectionWidget, rootCollectionWidget ,StatusWidget, favoriteListModel, RecentItemModel,listBookWidget, boxBookWidget
from dialogs import newCollectionDialog
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap
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

        # create the path history stack
        self.pathHistory = list()
        self.currentIndex = None

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

    def addPath(self, path : str):
        if len(self.pathHistory) != 0:
            if self.pathHistory[-1] != path:
                self.pathHistory.append(path)
                self.currentIndex = len(self.pathHistory) - 1
        else:
            self.pathHistory.append(path)
            self.currentIndex = 0

    def goBackward(self) -> str:
        # remove the lat item in the history
        if self.currentIndex > 0:
            self.currentIndex -= 1
        return self.pathHistory[self.currentIndex]

    def goForward(self) -> str:

        if self.currentIndex < len(self.pathHistory) - 1:
            self.currentIndex += 1
        return self.pathHistory[self.currentIndex]

    def canBackward(self):

        if self.currentIndex:
            if self.currentIndex > 0:
                return True
        return False

    def canForward(self):
        if self.currentIndex:
            if self.currentIndex < len(self.pathHistory) - 1:
                return True
        return False

    def clearHistory(self):
        self.pathHistory.clear()


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

        if not os.path.exists("db/favorite.json"):
            with open("db/favorite.json", "w") as file:
                json.dump([], file, indent=4)

        if not os.path.exists("db/collection_tracking.json"):
            with open("db/collection_tracking.json", "w") as file:
                json.dump([], file, indent=4)



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
        self.width = self.screen().size().width()
        self.height = self.screen().size().height()
        # first consider about the
        self.setWindowTitle("Library Management System v0.0.1")
        self.setGeometry(0, 0, self.width, self.height)
        # self.showFullScreen()

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
        self.reminderWidget.setMaximumWidth(int(self.width * 0.15))
        self.reminderWidget.setObjectName("reminderWidget")

        # create the other h box for pack them
        hbox2 = QHBoxLayout()
        hbox2.setSpacing(0)
        hbox2.addWidget(self.stageWidget)
        hbox2.addWidget(self.reminderWidget)

        spaceWidget.setLayout(hbox2)

        # configure the above widget then
        self.setUpTitleBarWidget()
        self.setUpBarWidget()
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

    def setUpBarWidget(self):

        # create the two main widgets for favorites and quick access
        self.favoriteWidget = QWidget()
        self.favoriteWidget.setContentsMargins(0, 0, 0, 0)

        # recent access
        self.recentaccessWidget = QWidget()
        self.recentaccessWidget.setContentsMargins(0, 0, 0, 0)

        # create the vbox for pack the widgets
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addWidget(self.favoriteWidget)
        vbox.addWidget(self.recentaccessWidget)
        vbox.addStretch()

        self.barWidget.setLayout(vbox)

        self.setUpFavoriteBar()
        self.setUpRecentAccessBar()

    def setUpFavoriteBar(self):

        # create the title label
        titleLabel = QLabel("Favorites")
        titleLabel.setObjectName("favoriteTitleLabel")

        # create the favorite lis view model
        self.favoriteModel = favoriteListModel()

        # create the list view
        self.favoriteListWidget = QListView()
        self.favoriteListWidget.setMinimumHeight(400)
        self.favoriteListWidget.setModel(self.favoriteModel)
        self.favoriteListWidget.clicked.connect(self.goToFavorite)

        # create the vbox for favorite bar
        vbox = QVBoxLayout()
        vbox.addWidget(titleLabel)
        vbox.addWidget(self.favoriteListWidget)
        vbox.addStretch()

        self.favoriteWidget.setLayout(vbox)

    def goToFavorite(self, index : QModelIndex):

        # get the data from the model
        data = self.favoriteModel.todos[index.row()]

        # open the new page
        self.openNewPage(data["path"], data["id"])
        # clear the selection of the list view
        self.favoriteListWidget.clearSelection()

    def updateFavoriteModel(self, data : list):

        if data[3]:
            # get the data from the signal and update the model list
            self.favoriteModel.todos.append({"title" : data[0], "path" : data[1], "id" : data[2], "type" : data[4]})
            # fire the model layout changed signal
            self.favoriteModel.layoutChanged.emit()
            # clear the selection of the list
            self.favoriteListWidget.clearSelection()
        else:
            # remove the selected item from the model
            for item in self.favoriteModel.todos:
                if item["path"] == data[1]:
                    self.favoriteModel.todos.remove(item)

            # fire the signal
            self.favoriteModel.layoutChanged.emit()
            self.favoriteListWidget.clearSelection()

    def setUpRecentAccessBar(self):

        # create the title label
        titleLabel = QLabel("Recent Access")
        titleLabel.setObjectName("recentTitleLabel")

        # create the list view for recent item,s
        self.recentListView = QListView()
        self.recentListView.setObjectName("recentListView")
        self.recentListView.setMinimumHeight(700)

        # create the recent model to set to the list view
        self.recentModel = RecentItemModel()
        self.recentListView.setModel(self.recentModel)

        # create the vbox for favorite bar
        vbox = QVBoxLayout()
        vbox.addWidget(titleLabel)
        vbox.addWidget(self.recentListView)
        vbox.addStretch()

        self.recentaccessWidget.setLayout(vbox)

    def setUpToolBarWidget(self):

        # create the search bar for library system
        self.searchBar = QLineEdit()
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setMinimumSize(QSize(500, 50))
        # self.searchBar.setMaximumSize(QSize(500, 60))
        self.searchBar.setPlaceholderText("search anything")
        self.searchBar.setAlignment(Qt.AlignRight)
        self.searchBar.textChanged.connect(self.searchThings)

        # create the label with search icon
        searchIcon = QLabel()
        searchIcon.setPixmap(QPixmap("images/sys_images/search_icon.png").scaled(QSize(45, 45), Qt.KeepAspectRatio,
                                                                                 Qt.SmoothTransformation))

        # create the box for pack the search items
        hboxSearch = QHBoxLayout()
        hboxSearch.setSpacing(10)
        hboxSearch.addWidget(searchIcon)
        hboxSearch.addWidget(self.searchBar)
        # create the grid layout for pack the searchBar

        grid_lyt = QGridLayout()
        grid_lyt.setSpacing(10)

        grid_lyt.addLayout(hboxSearch, 1, 1, 1, 3)

        # create the group box for pack the radio buttons
        group_box = QGroupBox()
        group_box.setMaximumSize(QSize(700, 50))

        # create the radio buttons
        searchOptions = ["Only Books", "Only Collections", "Both of them", "From Everything"]
        self.searchOptionRadioButtons = []
        # create the v box layout
        h_box_radios = QHBoxLayout()
        for item in searchOptions:
            # create the radio button and pack to the layout
            radio_new = QRadioButton(item)
            radio_new.setObjectName("searchOptionRadioButton")
            # add to the layout
            h_box_radios.addWidget(radio_new)
            # add to teh list
            self.searchOptionRadioButtons.append(radio_new)

        # set the layout ot the group box
        group_box.setLayout(h_box_radios)
        grid_lyt.addWidget(group_box, 0, 1, 1, 2)

        # create the button for new collection or add book
        self.addButton = QPushButton("+")
        self.addButton.setObjectName("addButton")
        self.addButton.setFont(QFont("verdana", 25))
        self.addButton.pressed.connect(self.addNewItem)


        # create the theme box
        self.themeBox = switchButton("list theme" , "box theme", "list", "box")
        self.themeBox.switchSignal.connect(self.refreshPage)

        # create the combo box for sorting options
        self.sortingBox = QComboBox()
        self.sortingBox.addItems(["A to Z", "Z to A", "Oldest to Latest", "Latest to Oldest", "Size"])
        self.sortingBox.setObjectName("sortingComboBox")

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.themeBox)
        hbox2.addWidget(self.sortingBox)

        grid_lyt.addLayout(hbox2, 0, 0)

        # create the refresh button
        refreshButton = QPushButton()
        refreshButton.setIcon(QIcon("images/sys_images/refresh_icon.png"))
        refreshButton.setIconSize(QSize(45, 45))
        refreshButton.setObjectName("refreshButton")
        refreshButton.pressed.connect(self.refreshPage)
        grid_lyt.addWidget(refreshButton, 0, 3)

        # backward button
        self.backwardButton =  QPushButton()
        self.backwardButton.setIcon(QIcon("images/sys_images/backward_icon.png"))
        self.backwardButton.setIconSize(QSize(45, 45))
        self.backwardButton.setObjectName("backwardButton")
        self.backwardButton.setEnabled(False)
        self.backwardButton.pressed.connect(self.goBack)

        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon("images/sys_images/forward_icon.png"))
        self.forwardButton.setIconSize(QSize(45, 45))
        self.forwardButton.setObjectName("forwardButton")
        self.forwardButton.setEnabled(False)
        self.forwardButton.pressed.connect(self.goForward)

        # create the small h box
        buttonHBox = QHBoxLayout()
        buttonHBox.setSpacing(10)
        buttonHBox.addWidget(self.addButton)
        buttonHBox.addSpacing(20)
        buttonHBox.addWidget(self.backwardButton)
        buttonHBox.addWidget(self.forwardButton)
        buttonHBox.addStretch()
        # add to the grid
        grid_lyt.addLayout(buttonHBox, 1, 0, 1, 2)




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
        # add the current path to the history
        self.currentStage.addPath(self.currentPath)

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

        # create the hide and show button
        self.hideButton = QPushButton(">")
        self.hideButton.setObjectName("hideButton")
        self.hideButton.pressed.connect(self.hideStatusPanel)

        self.showButton = QPushButton("<")
        self.showButton.setObjectName("showButton")
        self.showButton.hide()
        self.showButton.pressed.connect(self.showStatusPanel)

        rootLabel = QLabel("Root")
        rootLabel.setFont(QFont("verdana", 15))

        # create the h box for buttons
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.hideButton)
        hbox.addWidget(self.showButton)


        # create the vbox for tab
        self.reminderLyt = QVBoxLayout()
        self.reminderLyt.addLayout(hbox)
        self.reminderLyt.addWidget(self.reminderTab)
        self.reminderLyt.addWidget(rootLabel)

        # create the scroll area
        scroll_area_for_reminder = QScrollArea()
        scroll_area_for_reminder.setWidgetResizable(True)
        scroll_area_for_reminder.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area_for_reminder.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area_for_reminder.setMaximumWidth(self.reminderWidget.width())

        # create the another  widget
        anotherWidget = QWidget()
        anotherWidget.setLayout(self.reminderLyt)
        scroll_area_for_reminder.setWidget(anotherWidget)

        vbox = QVBoxLayout()
        vbox.addWidget(scroll_area_for_reminder)
        vbox.addSpacing(50)

        self.reminderWidget.setLayout(vbox)

        self.setUpStatusWidget()

    def hideStatusPanel(self):

        # create the animation to hide the panel
        self.hideAnimation = QPropertyAnimation(self.reminderWidget, b"maximumWidth")
        self.hideAnimation.setStartValue(self.reminderWidget.width())
        self.hideAnimation.setEndValue(int(self.width * 0.05))
        self.hideAnimation.setDuration(500)
        self.hideAnimation.start()

        self.showButton.show()
        self.hideButton.hide()

    def showStatusPanel(self):

        # create the animation to hide the panel
        self.showAnimation = QPropertyAnimation(self.reminderWidget, b"maximumWidth")
        self.showAnimation.setStartValue(self.reminderWidget.width())
        self.showAnimation.setEndValue(int(self.width * 0.15))
        self.showAnimation.setDuration(500)
        self.showAnimation.start()

        self.showButton.hide()
        self.hideButton.show()


    def setUpStatusWidget(self):

        # create the new status widget and pack to the StatusWidget
        self.statusBox = StatusWidget()

        # create the layout and pack to them
        self.status_vbox = QVBoxLayout()
        self.status_vbox.addWidget(self.statusBox)


        self.statusWidget.setLayout(self.status_vbox)

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

    def searchThings(self, text : str):

        # add the search criterias

        if self.searchOptionRadioButtons[0].isChecked():
            # hide the all of collections
            for widget in self.currentStage.collectionWidgets:
                widget.hide()

            for widget in self.currentStage.bookWidgets:
                if text.lower() in widget.title.lower():
                    widget.show()
                else:
                    widget.hide()

        elif self.searchOptionRadioButtons[1].isChecked():
            # hide the all of collections
            for widget in self.currentStage.bookWidgets:
                widget.hide()

            for widget in self.currentStage.collectionWidgets:
                if text.lower() in widget.title.lower():
                    widget.show()
                else:
                    widget.hide()

        else:

            # search the items
            for widget in self.currentStage.collectionWidgets:
                if text.lower() in widget.title.lower():
                    widget.show()
                else:
                    widget.hide()

            for widget in self.currentStage.bookWidgets:
                if text.lower() in widget.title.lower():
                    widget.show()
                else:
                    widget.hide()

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
                self.addNewBooks(files)

    def addNewBooks(self, files : list):

        # calculate the time and date
        date = QDate.currentDate().toString("dd:MM:yyyy")
        time = QTime.currentTime().toString("hh:mm:ss A")

        # create the connection and open the cursor
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        # get the book json file data
        books_data = {}
        with open("db/book.json", "r") as file:
            books_data = json.load(file)

        path = self.currentPath
        for file in files:
            # generate the new book id code
            book_id = self.generateID("book")


            cursor.execute(f""" INSERT INTO book_table(book_id , path, date ,time, pw) VALUES ('{book_id}', '{path}', '{date}', '{time}', '') """)
            books_data[book_id] = {"dir" : file}
            # create the book widget based on the theme

            if self.getTheme() == "list":
                # create the list book widget
                widget = listBookWidget(os.path.split(file)[1], book_id, path)
                # add to the layout
                self.stageLayout.insertWidget(0, widget)
            else:
                widget = boxBookWidget(os.path.split(file)[1], book_id, path)
                count = self.currentStage.WidgetCount()
                self.stageLayout.addWidget(widget, count//4, count%4)
            # connect to the slots th widget
            widget.favoriteSignal.connect(self.updateFavoriteModel)

            # update the stage
            self.currentStage.addBook(widget, {"title" : os.path.split(file),
                                               "path" : path,
                                               "dir" : file,
                                               "book_id" : book_id})



        # save the changes and close the connection
        connection.commit()
        connection.close()

        with open("db/book.json", "w") as file:
            json.dump(books_data, file, indent=4)


    def addNewCollection(self, data : dict):

        title = data["title"]
        des = data["description"]
        img = data["image_dir"]
        # get the current time and date
        current_time = QTime.currentTime().toString("hh:mm:ss A")
        current_date = QDate.currentDate().toString("dd:MM:yyyy")

        # generate the id
        id_code = self.generateID("collection")
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
            collection_widget = listCollectionWidget(title, des, img, path, id_code)
        else:
            collection_widget = boxCollectionWidget(title, des, img, path, id_code)

        info_data = {"title": title,
                     "description": des,
                     "path": path,
                     "image_dir": img,
                     "date": current_date,
                     "time": current_time}
        self.currentStage.addCollection(collection_widget, info_data)

        # set the event handler
        collection_widget.mouseDoubleClickEvent = (lambda a, e = collection_widget.path,
                                                          i = collection_widget.collection_id : self.openNewPage(e, i))
        collection_widget.mousePressEvent = (lambda a, e = collection_widget : self.setSelectedWidget(e))
        collection_widget.favoriteSignal.connect(self.updateFavoriteModel)



        # add to the layout
        if self.getTheme() == "list":
            self.stageLayout.insertWidget(0, collection_widget)
        else:
            # get the length of widgets
            count = self.currentStage.WidgetCount() - 1
            self.stageLayout.addWidget(collection_widget, count//4, count%4)

    def openNewPage(self, newPath : str, id : str):

        # set the new path as the newPath
        self.currentPath = newPath
        # delete the all of widgets
        for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
            widget.deleteLater()

        # clear the stage
        self.currentStage.clear()
        # add the new path to the stage history
        self.currentStage.addPath(self.currentPath)

        # render the new page
        self.renderNewPageForCollection(self.currentPath)
        self.renderNewPageForBook(self.currentPath)
        # set the back and forward settings
        self.setBackForwardState()

        # update the tracking informations
        self.saveCollectionTrackings(id)
        # set the root collection widget informations
        try:
            self.rootCollectionBox.deleteLater()
        except:
            pass
        self.rootCollectionBox = rootCollectionWidget(id)
        self.reminderLyt.addWidget(self.rootCollectionBox)

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
        self.renderNewPageForBook(self.currentPath)

    def goBack(self):

        # clear the widgets and stage
        for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
            widget.deleteLater()
        self.currentStage.clear()

        # set the new path
        self.currentPath = self.currentStage.goBackward()
        # reload the page
        self.renderNewPageForCollection(self.currentPath)
        self.renderNewPageForBook(self.currentPath)

        # set the backward button options
        self.setBackForwardState()

    def goForward(self):

        # clear the widgets and stage
        for widget in [*self.currentStage.collectionWidgets, *self.currentStage.bookWidgets]:
            widget.deleteLater()
        self.currentStage.clear()

        # set the new path
        self.currentPath = self.currentStage.goForward()
        # reload the page
        self.renderNewPageForCollection(self.currentPath)
        self.renderNewPageForBook(self.currentPath)

        # set the backward button options
        self.setBackForwardState()

    def setBackForwardState(self):

        if self.currentStage.canBackward():
            self.backwardButton.setEnabled(True)
        else:
            self.backwardButton.setEnabled(False)

        if self.currentStage.canForward():
            self.forwardButton.setEnabled(True)
        else:
            self.forwardButton.setEnabled(False)

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
                            "time" : data[i][5],
                            "id" : data[i][1]}
                filter_data.append(new_dict)

        self.addCollectionWidgets(filter_data)

    def renderNewPageForBook(self, path : str):

        # get the need books data
        books_data = self.getNeedBooks(path)

        # modified the data used the json file data
        json_data = {}
        with open("db/book.json", "r") as file:
            json_data = json.load(file)
        # filter the code data
        id_data = [item[1] for item in books_data]

        filter_json_data = []
        for item in json_data.keys():
            if item in id_data:
                filter_json_data.append([item, json_data[item]["dir"]])

        # merge the lists
        originalData = []
        for i in range(len(books_data)):
            # create the new dictionary for this
            new_dict = {"title" : os.path.split(filter_json_data[i][1])[1],
                        "path" : books_data[i][2],
                        "dir" : filter_json_data[i][1],
                        "id" : books_data[i][1]}
            originalData.append(new_dict)

        # create the new book used the original Data list
        self.addNewBookWidgets(originalData)

    def addNewBookWidgets(self, filterData : list):

        for data in filterData:
            # create the widget base on the theme
            if self.getTheme() == "list":
                widget = listBookWidget(data["title"], data["id"], data["path"])
                self.stageLayout.insertWidget(0, widget)
            else:
                widget = boxBookWidget(data["title"], data["id"], data["path"])
                count = self.currentStage.WidgetCount()
                self.stageLayout.addWidget(widget, count//4, count%4)
            # update the stage area
            self.currentStage.addBook(widget, data)
            # connect to the slots of the widget
            widget.favoriteSignal.connect(self.updateFavoriteModel)


    def addCollectionWidgets(self, FilterData : list):


        for data in FilterData:
            # create the new widget
            if self.getTheme() == "list":
                widget = listCollectionWidget(data["title"], data["description"], data["image_dir"], data["path"], data["id"])
                self.stageLayout.addWidget(widget)
            else:
                widget = boxCollectionWidget(data["title"], data["description"], data["image_dir"], data["path"], data["id"])
                count = self.currentStage.WidgetCount()
                self.stageLayout.addWidget(widget, (count) // 4, (count) % 4)

            widget.mouseDoubleClickEvent = (lambda a, e = widget.path, i = widget.collection_id : self.openNewPage(e, i))
            widget.mousePressEvent = (lambda a, e = widget : self.setSelectionWidget(e))
            widget.favoriteSignal.connect(self.updateFavoriteModel)
            # add the widget to stage
            self.currentStage.addCollection(widget, data)
        if isinstance(self.stageLayout, QVBoxLayout):
            self.stageLayout.addStretch()

    def saveCollectionTrackings(self, id):

        # get the current time and date
        time = QTime.currentTime().toString("hh:mm:ss A")
        date = QDate.currentDate().toString("dd/MM/yyyy")

        with open("db/collection_tracking.json", "r") as file:
            user_data = json.load(file)

        # update the use data with current item
        user_data.append([id, date, time, "collection"])

        # save the changes
        with open("db/collection_tracking.json", "w") as file:
            json.dump(user_data, file ,indent=4)



    def setSelectionWidget(self, widget):

        if self.currentStage.selected_widget:
            self.currentStage.selected_widget.isSelected = 'false'
        # set thr stage selected widget as the this
        if isinstance(widget, boxCollectionWidget) or isinstance(widget , listCollectionWidget):
            self.currentStage.selected_widget = widget
            # set the selected id to True
            widget.isSelected = 'true'
            # update the status
            self.setCollectionStatus()

    def setCollectionStatus(self):

        # get the current selected widget
        widget = self.currentStage.selected_widget


        # open the data base
        connect = sqlite3.connect(self.db_file)
        cursor = connect.cursor()

        cursor.execute(f" SELECT * FROM collection_table WHERE collection_id = '{widget.collection_id}' ")
        data = cursor.fetchall()

        # close the connection
        connect.close()
        data = data[0]

        # open the json file
        with open("db/collection.json", "r") as file:
            user_data = json.load(file)
        des = user_data.get(widget.collection_id)["description"]

        if des == "":
            des = "No Description"

        # get the widget basic data
        widget_data = {"title" : widget.title,
                "path" : widget.path,
                "id" : widget.collection_id,
                "des" : des,
                "date" : data[4],
                "time" : data[5]}

        # first cleat the status box
        try:
            self.statusBox.deleteLater()
        except:
            pass
        # create the new status box
        self.statusBox = StatusWidget()
        self.status_vbox.addWidget(self.statusBox)
        # fill the status box
        self.statusBox.addLine("Title : ", widget_data["title"], wrap = True)
        self.statusBox.addLine("Description : ", widget_data["des"], wrap=True)
        self.statusBox.addSeperator()
        # add the created date and time
        self.statusBox.addLabel(f"Created On\n {widget_data['date']}\nAt {widget_data['time']}")


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

    def getNeedBooks(self, rootPath):

        # create the connection
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute(f""" SELECT * FROM book_table WHERE path='{rootPath}' """)
        data = cursor.fetchall()

        # close the connection and return the data
        connection.close()
        return data

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

    def generateID(self, type : str):

        # generate the 5 digits code for collection
        # first create the connection and get the current ids
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        if type == "collection":
            cursor.execute("SELECT collection_id FROM collection_table")
            data = cursor.fetchall()
        else:
            cursor.execute("SELECT book_id FROM book_table")
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
