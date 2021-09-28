# this is the main file in the project

import json
import os, sqlite3
import shutil
import sys, random, threading

import fitz
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow , QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QRadioButton,
                             QGroupBox, QScrollArea, QDialog, QFileDialog, QTabWidget, QComboBox, QInputDialog ,QListView, QMenuBar, QMenu,
                             QAction, QMessageBox, QStackedLayout, QDesktopWidget, QSplitter)

from PyQt5.Qt import QFont, Qt, QSize, QTime, QDate, QPropertyAnimation, QEasingCurve, QModelIndex, QTextEdit, QRect, QThread
import PyQt5.QtCore as Core
from PyQt5.QtGui import QColor, QPalette, QIcon, QPixmap, QKeyEvent
# import the custom modules
from dialogs import newCollectionDialog
from style_sheet import dark_style_sheet, dark_style_sheet_for_Collection
from libraray_widgets.status_widgets import FullStatusWidget
from book_space import BookArea
# import the widgets modules
from models import favoriteListModel, RecentItemModel
from libraray_widgets.book_widgets import listBookWidget, boxBookWidget
from libraray_widgets.collection_widgets import listCollectionWidget, boxCollectionWidget
from libraray_widgets.other_widgets import *
from libraray_widgets.status_widgets import *
from libraray_widgets.LibrarayTreeWidget import LibTreeView
from libraray_widgets.task_widgets import TaskAndReminderOpen
from bookTable import bookTable

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

chrs = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y", "z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def refreshDataBase(db_file):
    # create the connection and get the cursor ibject
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("SELECT book_id FROM book_table")

    ids = cursor.fetchall()
    ids = [id[0] for id in ids]

    # open the book json file
    with open("db/book.json") as file:
        user_data = json.load(file)



    for i, pdf in enumerate(user_data.keys()):
        if os.path.exists(user_data.get(pdf).get('dir')):
            # remove from the ids first
            ids.remove(pdf)
        #progress_bar.setValue(int(i / len(user_data.keys())))

    #with open("db/book.json", "w") as file:
    #    json.dump(user_data, file, indent=4)

    for id in ids:
        cursor.execute(f"DELETE FROM book_table WHERE book_id = '{id}' ")

    # refresh the favorites json file
    with open("db/favorite.json") as file:
        favorites = json.load(file)

    newFavorites = []
    for item in favorites:
        if not(item['type'] == "book" and item['id'] in  ids):
            newFavorites.append(item)

    with open("db/favorite.json", "w") as file:
        json.dump(newFavorites, file, indent=4)

    # save the changes and close the connection
    connection.commit()
    connection.close()
    print('[INFO] successfully removed the undefined pdf files from the data base')

class LibNms:
    OPEN = 1
    RENAME = 2
    CHNDES = 3
    INFO = 4
    CHNIMG = 5
    CHNPW = 6
    DELETE = 7

class bookCoverLoader(QThread):
    def __init__(self, bookList : list = [] ):
        super(bookCoverLoader, self).__init__()
        self.bookWidgetList = bookList

    def run(self) -> None:

        # load the indivigual images of the each books
        for bookWidget in self.bookWidgetList:
            bookWidget.loadCover()

        print("[INFO] cover load successfull...")


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
        if not os.path.exists("images/sys_images"):
            os.mkdir("images/sys_images")
        if not os.path.exists("db/temp"):
            os.mkdir("db/temp")

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

        # get the desktop widget
        desktop = QDesktopWidget()
        desk_geo = desktop.geometry()
        # set the window width and height
        self.width = desk_geo.width()
        self.height = desk_geo.height()
        # first consider about the
        self.setWindowTitle("eLibrary Management System v0.0.1")
        self.setGeometry(desk_geo)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("mainWindowWidget")

        # create the mai widgets
        self.setUpWidgets()
        self.setStyleSheet(dark_style_sheet)


        # show the window in the screen
        self.show()

    def keyPressEvent(self, event : QKeyEvent) -> None:

        if event.key() == Qt.Key_Delete:
            # delete the seleted widget if the seleted item exists
            if self.currentStage.selected_widget:
                self.currentStage.selected_widget.delete()

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
        self.barWidget.setMaximumWidth(int(self.width * 0.2))
        self.barWidget.setContentsMargins(0, 0, 0, 0)
        self.barWidget.setObjectName("barWidget")

        # create the barOther Widget
        barOtherWidget = QWidget(self.mainWidgets)
        barOtherWidget.setContentsMargins(0, 0, 0, 0)
        # create the layout and pack them
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)
        hbox1.setContentsMargins(0, 0, 0, 0)


        # create the splitter for this
        splitter  = QSplitter(Qt.Horizontal)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.addWidget(self.barWidget)
        splitter.addWidget(barOtherWidget)
        hbox1.addWidget(splitter)

        self.mainWidgets.setLayout(hbox1)


        # create the top title bar widget
        self.titleBaridget = QWidget()
        self.titleBaridget.setFixedHeight(int(self.height * 0.08))
        self.titleBaridget.setObjectName("titleBarWidget")

        # create the stack layout for setUp the varius stack layouts
        self.toolStackLyt = QStackedLayout()
        # create the collection widget tool bar widgets
        self.collectionToolBar = QWidget()
        self.collectionToolBar.setMaximumHeight(int(self.height * 0.18))
        self.collectionToolBar.setContentsMargins(0, 0, 0, 0)

        # create the tool bar widget
        self.toolBarWidget = QWidget()
        self.toolBarWidget.setMaximumHeight(int(self.height * 0.18))
        self.toolBarWidget.setObjectName("toolBarWidget")
        # add to the stack layout
        self.toolStackLyt.addWidget(self.toolBarWidget)
        self.toolStackLyt.addWidget(self.collectionToolBar)
        self.toolStackLyt.setContentsMargins(0, 0, 0, 0)
        # create the space widget
        spaceWidget = QWidget()
        spaceWidget.setObjectName("spaceWidget")
        spaceWidget.setContentsMargins(0, 0, 0, 0)

        # create the vbox for pack this widgets
        vbox1 = QVBoxLayout()
        vbox1.setSpacing(0)
        vbox1.setContentsMargins(0, 0, 0, 0)
        vbox1.addWidget(self.titleBaridget)
        vbox1.addLayout(self.toolStackLyt)
        vbox1.addWidget(spaceWidget, 10)

        barOtherWidget.setLayout(vbox1)

        # create the stage widget and reminders widget
        self.stageWidget = QWidget()
        self.stageWidget.setObjectName("stageWidget")
        self.stageWidget.setContentsMargins(0, 0, 0, 0)

        self.reminderWidget = QWidget()
        self.reminderWidget.setContentsMargins(0, 0, 0, 0)
        self.reminderWidget.setMaximumWidth(int(self.width * 0.15))
        self.reminderWidget.setObjectName("reminderWidget")

        # create the other h box for pack them
        hbox2 = QHBoxLayout()
        hbox2.setSpacing(0)
        hbox1.setContentsMargins(0, 0, 0, 0)
        hbox2.addWidget(self.stageWidget)
        hbox2.addWidget(self.reminderWidget)

        spaceWidget.setLayout(hbox2)

        # configure the above widget then
        self.setUpTitleBarWidget()
        self.setUpBarWidget()
        self.setUpToolBarWidget()
        self.setUpCollectionToolBarWidget()
        self.setUpStageWidget()
        self.setUpRemiderWidget()

        # create the menu bar
        self.menuBar = QMenuBar()
        self.setMenuBar(self.menuBar)

        self.setUpMenu()

    def setUpMenu(self):

        # create the menu foro file
        self.fileMenu = QMenu("File")
        self.menuBar.addMenu(self.fileMenu)

        # create the actions for file menu
        self.exitAction = QAction("Exit")
        self.exitAction.setShortcut("Alt + F4")
        self.exitAction.setStatusTip("Quit the Application")
        self.exitAction.triggered.connect(self.close)

        # create the reset option
        self.resetAction = QAction("Reset System")
        self.resetAction.setShortcut("Shift + D")
        self.resetAction.setStatusTip("Reset the Entire System")
        self.resetAction.triggered.connect(self.resetSystem)

        # create the refresh action
        self.refreshAction = QAction("Refresh DataBase", self)
        self.refreshAction.setStatusTip("Refresh the Data Base files and all of the data files with removing the unwanted files")
        self.refreshAction.triggered.connect(self.refreshDataBase)

        # add to the file menu
        self.fileMenu.addAction(self.resetAction)
        self.fileMenu.addAction(self.refreshAction)
        self.fileMenu.addAction(self.exitAction)



        # create hte view menu
        self.view_menu = QMenu("View")
        self.menuBar.addMenu(self.view_menu)

        # create the action for view menu
        self.viewFavoriteAction = QAction("Show Favorite JSON File (for developing purpose)", self)
        self.viewFavoriteAction.triggered.connect(self.viewFavoriteJSON)

        self.openBookTableAction = QAction("Open Book Store as TableView", self)
        self.openBookTableAction.triggered.connect(self.openTableView)

        self.view_menu.addAction(self.viewFavoriteAction)
        self.view_menu.addAction(self.openBookTableAction)

    def resetSystem(self):

        # delete the all of the system files
        # clear the current stage widget and favorites and recent bars
        message = QMessageBox.warning(self, "Reset Warning", "Do you want to Reset System. It Will be remove the all of the data basese and other files form the system", QMessageBox.StandardButton.Ok|QMessageBox.StandardButton.Cancel)

        if message == QMessageBox.StandardButton.Ok:
            # remove the all of the data base folder files
            os.rmdir("db")
            # remove the all of the images files
            for file in os.listdir("images"):
                if file != "sys_images":
                    os.remove(file)

            # prompt the message box
            msg = QMessageBox.information(self, "Reset System Message Box", "System Reset Successfully finished.", QMessageBox.StandardButton.Ok)
            # update the current path and open new home page
            self.currentPath = ""
            self.openNewPage(self.currentPath)

    def openTableView(self):

        self.newTable = bookTable()
        self.newTable.show()

    def setUpTitleBarWidget(self):

        # crate the title label
        title_label = QLabel("eLibrary Management System")
        title_label.setFont(QFont("verdana", 27))
        title_label.setAlignment(Qt.AlignRight)
        title_label.setObjectName("title_label")
        title_label.setContentsMargins(0, 0, 0, 0)

        # create the h box for pack the label
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.addWidget(title_label)

        self.titleBaridget.setLayout(hbox)

    def setUpBarWidget(self):

        # create the h box for setup the side bar
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        button_v_box = QVBoxLayout()
        button_v_box.setContentsMargins(0, 0, 0, 0)

        # create the hide button and show button
        barHideShowButton = QPushButton()
        barHideShowButton.pressed.connect(self.hideOrShowBar)
        barHideShowButton.setObjectName("barHideButton")
        barHideShowButton.setIcon(QIcon('images/sys_images/expandIocn.png'))
        barHideShowButton.setIconSize(QSize(25, 25))
        button_v_box.addWidget(barHideShowButton)

        # create the button for navigate through the stack layout widgets
        favoriteNavButton = QPushButton()
        favoriteNavButton.setIcon(QIcon("images/sys_images/yellowStar.png"))
        recentNavButton = QPushButton()
        recentNavButton.setIcon(QIcon("images/sys_images/quickArrowIcon.png"))
        treeviewNavButton = QPushButton()
        treeviewNavButton.setIcon(QIcon("images/sys_images/branch.png"))

        nav_slots = ["fav", "rec", "tree"]

        self.navButton = [favoriteNavButton, recentNavButton, treeviewNavButton]
        for i, button in enumerate(self.navButton):
            button.setMaximumWidth(50)
            button.setCheckable(True)
            button.setIconSize(QSize(35, 35))
            button.setObjectName("navigateButton")
            # connect the slots for this button
            button.pressed.connect(lambda e =  nav_slots[i] : self.navigateWidget(e))
            button_v_box.addWidget(button, alignment=Qt.AlignTop)
        favoriteNavButton.setChecked(True)
        button_v_box.addStretch()

        # create the stack layout for widgets
        self.barStackLyt = QStackedLayout()
        self.barStackLyt.setContentsMargins(0, 0, 0, 0)



        # create the two main widgets for favorites and quick access
        self.favoriteWidget = QWidget()
        self.favoriteWidget.setContentsMargins(0, 0, 0, 0)

        # recent access
        self.recentaccessWidget = QWidget()
        self.recentaccessWidget.setContentsMargins(0, 0, 0, 0)

        # create the tree view and add th the stack layout
        #self.treeView = LibTreeView()
        #self.setContentsMargins(0, 0, 0, 0)
        self.treeView = None

        self.barStackLyt.addWidget(self.favoriteWidget)
        self.barStackLyt.addWidget(self.recentaccessWidget)
        # self.barStackLyt.addWidget(self.treeView)

        # create the widget for pack the stack laout
        self.navWidget = QWidget()
        self.navWidget.setContentsMargins(0, 0, 0, 0)
        self.navWidget.setLayout(self.barStackLyt)

        hbox.addLayout(button_v_box)
        hbox.addWidget(self.navWidget)
        self.barWidget.setLayout(hbox)

        self.setUpFavoriteBar()
        self.setUpRecentAccessBar()

    def navigateWidget(self, key : str):


        if key == "fav":
            self.navButton[1].setChecked(False)
            self.navButton[2].setChecked(False)
            # set the stack layout index
            self.barStackLyt.setCurrentIndex(0)
        elif key == "rec":
            self.navButton[0].setChecked(False)
            self.navButton[2].setChecked(False)
            self.barStackLyt.setCurrentIndex(1)
        elif key == "tree":
            self.navButton[0].setChecked(False)
            self.navButton[1].setChecked(False)
            # create the tree view and view it
            if not self.treeView:
                self.treeView = LibTreeView()
                self.barStackLyt.addWidget(self.treeView)

            self.barStackLyt.setCurrentIndex(2)

    def hideOrShowBar(self):

        # create the hide and show animation object
        self.barAniamtion = QPropertyAnimation(self.barWidget, b'maximumWidth')
        self.barAniamtion.setStartValue(self.barWidget.maximumWidth())
        self.barAniamtion.setCurrentTime(800)

        if (self.navWidget.isHidden()):
            self.barAniamtion.setEndValue(int(self.width * 0.50))
            self.barAniamtion.setEasingCurve(QEasingCurve.OutCurve)
            # start the animation
            self.barAniamtion.start(QPropertyAnimation.DeleteWhenStopped)
            # show the widgets
            self.navWidget.show()
        else:
            self.barAniamtion.setEndValue(50)
            self.barAniamtion.setEasingCurve(QEasingCurve.InBounce)
            # start the animation
            self.barAniamtion.start(QPropertyAnimation.DeleteWhenStopped)
            # hide the widgets
            self.navWidget.hide()



    def setUpFavoriteBar(self):

        # create the title label
        titleLabel = QLabel("Favorites")
        titleLabel.setObjectName("favoriteTitleLabel")

        # create the favorite lis view model
        self.favoriteModel = favoriteListModel()

        # create the list view
        self.favoriteListWidget = QListView()
        self.favoriteListWidget.setContentsMargins(0, 0, 0, 0)
        self.favoriteListWidget.setAlternatingRowColors(True)
        self.favoriteListWidget.setMinimumHeight(1000)
        self.favoriteListWidget.setModel(self.favoriteModel)
        self.favoriteListWidget.clicked.connect(self.goToFavorite)

        # create the vbox for favorite bar
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        # add the widgets
        vbox.addWidget(titleLabel)
        vbox.addWidget(self.favoriteListWidget)
        vbox.addStretch()

        self.favoriteWidget.setLayout(vbox)

    def goToFavorite(self, index : QModelIndex):

        # get the data from the model
        data = self.favoriteModel.todos[index.row()]


        if data["type"] == "collection":
            try:
                # open the data base for get the password
                connect = sqlite3.connect(self.db_file)
                cursor = connect.cursor()

                cursor.execute(f" SELECT pw FROM collection_table WHERE collection_id = '{data['id']}' ")
                pw = cursor.fetchall()
                connect.close()

                pw = pw[0][0]
                # open the new page
                self.openNewPage(data["path"], data["id"], pw = pw)
                # clear the selection of the list view
                #self.favoriteListWidget.clearSelection()
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Something was Error to Open this Collection , sometime deletion error")
                msg.setWindowFlags(Qt.FramelessWindowHint)
                msg.exec_()

        else:
            # get the pasowrd from the favorite list
            pw = data.get("pw", "")
            # create the new book widge
            self.openBookSpace(data["id"], pw)

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
        self.recentListView.setMinimumHeight(1000)


        # create the recent model to set to the list view
        self.recentModel = RecentItemModel()
        self.recentListView.setModel(self.recentModel)

        self.recentListView.clicked.connect(self.clickedRecent)

        # create the vbox for favorite bar
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(titleLabel)
        vbox.addWidget(self.recentListView)
        vbox.addStretch()

        self.recentaccessWidget.setLayout(vbox)

    def clickedRecent(self, index):


        # get the collection id and path of the clicked item
        if self.recentModel.todos[index.row()][-1] == "collection":
            try:
                coll_id = self.recentModel.todos[index.row()][0]

                # get the path and pw from the data base
                connect = sqlite3.connect(self.db_file)
                cursor = connect.cursor()

                cursor.execute(f" SELECT path, pw FROM collection_table WHERE collection_id = '{coll_id}' ")
                data = cursor.fetchall()
                connect.close()

                self.openNewPage(data[0][0], coll_id, pw=data[0][1])
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Something was Error to Open this Collection , sometime deletion error")
                msg.setWindowFlags(Qt.FramelessWindowHint)
                msg.exec_()

    def perfomeCollAction(self, action):

        # get the selectted widget from the stage
        widget  = self.currentStage.selected_widget

        if (widget and (isinstance(widget, listCollectionWidget) or isinstance(widget, boxCollectionWidget))):
            # perfome theh aciton
            if action == LibNms.OPEN:
                widget.mouseDoubleClickEvent(None)
            elif action == LibNms.RENAME:
                widget.changeTitle()
            elif action == LibNms.CHNDES:
                widget.changeDescription()
            elif action == LibNms.CHNPW:
                widget.changePassword()
            elif action == LibNms.INFO:
                widget.statusSignal.emit(widget.collection_id)
            elif action == LibNms.CHNIMG:
                widget.changeImage()
            elif action == LibNms.DELETE:
                widget.delete()

    def setUpCollectionToolBarWidget(self):
        # create the hbox and pack the buttons for this
        hbox = QHBoxLayout()
        hbox.setSpacing(0)

        # create the this buttons
        openButton = QPushButton("Open")
        openButton.setIcon(QIcon("images/sys_images/openIcon.png"))
        openButton.pressed.connect(lambda e = LibNms.OPEN : self.perfomeCollAction(e))

        renameButton = QPushButton("Rename")
        renameButton.setIcon(QIcon("images/sys_images/renameIcon.png"))
        renameButton.pressed.connect(lambda e = LibNms.RENAME : self.perfomeCollAction(e))

        changeDesButton = QPushButton("Change Description")
        changeDesButton.setIcon(QIcon("images/sys_images/changeDesIocn.png"))
        changeDesButton.pressed.connect(lambda e  = LibNms.CHNDES : self.perfomeCollAction(e))

        changePwButton = QPushButton("Change Password")
        changePwButton.setIcon(QIcon("images/sys_images/changePwIcon.png"))
        changePwButton.pressed.connect(lambda e = LibNms.CHNPW : self.perfomeCollAction(e))

        changeImageButton = QPushButton("Change Cover Image")
        changeImageButton.setIcon(QIcon("images/sys_images/changeImageIcon.png"))
        changeImageButton.pressed.connect(lambda e = LibNms.CHNIMG : self.perfomeCollAction(e))

        deleteButton = QPushButton("Delete")
        deleteButton.setIcon(QIcon('images/sys_images/close.png'))
        deleteButton.pressed.connect(lambda e = LibNms.DELETE : self.perfomeCollAction(e))

        informationButton = QPushButton("Informations")
        informationButton.setIcon(QIcon("images/sys_images/infoIcon.png"))
        informationButton.pressed.connect(lambda e = LibNms.INFO : self.perfomeCollAction(e))

        self.collectionToolBarButton = [openButton, renameButton, changeDesButton, changePwButton, changeImageButton,
                                        deleteButton ,informationButton]

        for button in self.collectionToolBarButton:
            button.setDisabled(True)
            button.setIconSize(QSize(100, 120))
            button.setObjectName("collectionToolBarButton")
            hbox.addWidget(button)

        # create the stack Change Button
        stackChangeButton = QPushButton(">")
        stackChangeButton.setObjectName("stackChangeButton")
        stackChangeButton.pressed.connect(lambda : self.toolStackLyt.setCurrentIndex(0))
        hbox.addWidget(stackChangeButton)

        # create the hbox for pathWidget
        hbox2 = QHBoxLayout()
        hbox2.setContentsMargins(0, 0, 0, 0)
        # create the path widget
        self.pathWidget = pathWidget("/")
        self.pathWidget.pathSignal.connect(lambda e : self.openNewPage(*e))
        hbox2.addWidget(self.pathWidget)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        self.collectionToolBar.setLayout(vbox)


    def setUpToolBarWidget(self):

        # create the search bar for library system
        self.searchBar = QLineEdit()
        self.searchBar.setObjectName("searchBar")
        self.searchBar.setMinimumSize(QSize(450, 40))
        # self.searchBar.setMaximumSize(QSize(500, 60))
        self.searchBar.setPlaceholderText("search anything")
        self.searchBar.setAlignment(Qt.AlignRight)
        self.searchBar.textChanged.connect(self.searchThings)
        self.searchBar.mouseDoubleClickEvent = self.advancedSearchPopUp

        # create the label with search icon
        searchIcon = QLabel()
        searchIcon.setPixmap(QPixmap("images/sys_images/searchIcon.png").scaled(QSize(45, 45), Qt.KeepAspectRatio,
                                                                                 Qt.SmoothTransformation))

        # create the box for pack the search items
        hboxSearch = QHBoxLayout()
        hboxSearch.setSpacing(10)
        hboxSearch.addWidget(searchIcon)
        hboxSearch.addWidget(self.searchBar)
        # create the grid layout for pack the searchBar

        grid_lyt = QGridLayout()
        grid_lyt.setSpacing(10)

        grid_lyt.addLayout(hboxSearch, 1, 1, 1, 5)

        # create the group box for pack the radio buttons
        group_box = QGroupBox()
        group_box.setMaximumSize(QSize(700, 50))

        # create the radio buttons
        searchOptions = ["Only Books", "Only Collections", "Both of them"]
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
        self.searchOptionRadioButtons[0].setChecked(True)

        # set the layout ot the group box
        group_box.setLayout(h_box_radios)
        grid_lyt.addWidget(group_box, 0, 1, 1, 2)

        # create the button for new collection or add book
        self.addButton = QPushButton("+")
        self.addButton.setObjectName("addButton")
        self.addButton.setFont(QFont("verdana", 25))
        self.addButton.pressed.connect(lambda e = self.addButton : self.addNewItem(e))


        # create the show and hide buttons
        self.toolBarHideButton = QPushButton()
        self.toolBarHideButton.setIcon(QIcon("images/sys_images/up_arrow.png"))
        self.toolBarHideButton.pressed.connect(self.hideToolBar)
        self.toolBarHideButton.setObjectName("toolBarHideButton")

        self.toolBarShowButton = QPushButton()
        self.toolBarShowButton.setIcon(QIcon("images/sys_images/down_arraow.png"))
        self.toolBarShowButton.pressed.connect(self.showToolBar)
        self.toolBarShowButton.hide()
        self.toolBarShowButton.setObjectName("toolBarHideButton")

        # create the theme box
        self.themeBox = switchButton("list theme" , "box theme", "list", "box")
        self.themeBox.switchSignal.connect(self.refreshPage)

        # create the combo box for sorting options
        self.sortingBox = QComboBox()
        self.sortingBox.addItems(["A to Z", "Z to A", "Oldest to Latest", "Latest to Oldest", "Size"])
        self.sortingBox.setObjectName("sortingComboBox")
        self.sortingBox.currentIndexChanged.connect(self.sortWidgets)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.toolBarHideButton)
        hbox2.addWidget(self.toolBarShowButton)
        hbox2.addWidget(self.themeBox)
        hbox2.addWidget(self.sortingBox)

        grid_lyt.addLayout(hbox2, 0, 0)

        # create the refresh button
        refreshButton = QPushButton()
        refreshButton.setIcon(QIcon("images/sys_images/refresh_icon.png"))
        refreshButton.setIconSize(QSize(45, 45))
        refreshButton.setObjectName("refreshButton")
        refreshButton.pressed.connect(self.refreshPage)
        grid_lyt.addWidget(refreshButton, 0, 4)

        # backward button
        self.backwardButton =  QPushButton()
        self.backwardButton.setIcon(QIcon("images/sys_images/backward_icon.png"))
        self.backwardButton.setIconSize(QSize(45, 45))
        self.backwardButton.setObjectName("backwardButton")
        self.backwardButton.setEnabled(False)
        self.backwardButton.pressed.connect(lambda e = True : self.goBackOrForward(e))

        self.forwardButton = QPushButton()
        self.forwardButton.setIcon(QIcon("images/sys_images/forward_icon.png"))
        self.forwardButton.setIconSize(QSize(45, 45))
        self.forwardButton.setObjectName("forwardButton")
        self.forwardButton.setEnabled(False)
        self.forwardButton.pressed.connect(lambda e = False : self.goBackOrForward(e))

        # create the home button
        homeButton = QPushButton()
        homeButton.pressed.connect(self.gotoHome)
        homeButton.setIconSize(QSize(45, 45))
        homeButton.setIcon(QIcon('images/sys_images/homeIcon.png'))
        homeButton.setObjectName("homeButton")

        # create the small h box
        buttonHBox = QHBoxLayout()
        buttonHBox.setSpacing(10)
        buttonHBox.addWidget(self.addButton)
        buttonHBox.addSpacing(20)
        buttonHBox.addWidget(homeButton)
        buttonHBox.addWidget(self.backwardButton)
        buttonHBox.addWidget(self.forwardButton)
        buttonHBox.addStretch()
        # add to the grid
        grid_lyt.addLayout(buttonHBox, 1, 0, 1, 2)

        # create the stack lyt change button
        stackChangeButton = QPushButton(">")
        stackChangeButton.setObjectName("stackChangeButton")
        stackChangeButton.pressed.connect(lambda : self.toolStackLyt.setCurrentIndex(1))
        grid_lyt.addWidget(stackChangeButton, 0, 5)

        # create the task widget
        taskWidget = TaskAndReminderOpen()
        grid_lyt.addWidget(taskWidget, 0, 3)

        # create the list for tool bar items
        self.toolBarItems = [self.searchBar, self.backwardButton, self.forwardButton, refreshButton, searchIcon, group_box,
                             self.addButton, self.themeBox, self.sortingBox, homeButton, taskWidget]

        # set the toolBar widget ;layout as the grid_lyt
        self.toolBarWidget.setLayout(grid_lyt)


    def hideToolBar(self):

        # create the animation for hide the tool bar
        self.toolBarHidingAnimation = QPropertyAnimation(self.toolBarWidget, b'maximumHeight')
        self.toolBarHidingAnimation.setEasingCurve(QEasingCurve.InCurve)
        self.toolBarHidingAnimation.setDuration(900)
        self.toolBarHidingAnimation.setStartValue(self.toolBarWidget.height())
        self.toolBarHidingAnimation.setEndValue(50)
        self.toolBarHidingAnimation.start(QPropertyAnimation.DeleteWhenStopped)

        self.toolBarHideButton.hide()
        self.toolBarShowButton.show()

        self.titleBaridget.hide()

        for widget in [*self.toolBarItems, *self.collectionToolBarButton, self.pathWidget]:
            widget.hide()

    def showToolBar(self):

        # create the animation for hide the tool bar
        self.toolBarShowingAnimation = QPropertyAnimation(self.toolBarWidget, b'maximumHeight')
        self.toolBarShowingAnimation.setEasingCurve(QEasingCurve.OutCubic)
        self.toolBarShowingAnimation.setDuration(1000)
        self.toolBarShowingAnimation.setStartValue(self.toolBarWidget.height())
        self.toolBarShowingAnimation.setEndValue(int(self.height * 0.18))
        self.toolBarShowingAnimation.start(QPropertyAnimation.DeleteWhenStopped)

        self.toolBarHideButton.show()
        self.toolBarShowButton.hide()

        self.titleBaridget.show()

        for widget in [*self.toolBarItems, *self.collectionToolBarButton, self.pathWidget]:
            widget.show()

    def setUpStageWidget(self):

        # create the tab widget for stage
        self.stageTab = QTabWidget()
        self.stageTab.setObjectName("stageTab")
        self.stageTab.tabBar().setObjectName("stageTabBar")
        self.stageTab.setContentsMargins(0, 0, 0, 0)
        self.stageTab.setTabsClosable(True)
        # set the tab closable slot
        self.stageTab.tabCloseRequested.connect(lambda e : self.stageTab.removeTab(e))
        vbox1 = QVBoxLayout()
        vbox1.setContentsMargins(0, 0, 0, 0)
        vbox1.addWidget(self.stageTab)

        self.stageWidget.setLayout(vbox1)

        # create the scroll widget
        scroll_area = QScrollArea()
        scroll_area.setObjectName("mainScrollArea")
        scroll_area.setContentsMargins(0, 0, 0, 0)

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
        #vbox = QVBoxLayout()
        #vbox.addWidget(scroll_area)

        #self.stageWidget.setLayout(vbox)
        self.stageTab.addTab(scroll_area, "Main")


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
        self.reminderTab.setTabBarAutoHide(True)

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
        self.hideButton = QPushButton()
        self.hideButton.setIcon(QIcon('images/sys_images/expandIocn.png'))
        self.hideButton.setObjectName("hideButton")
        self.hideButton.pressed.connect(self.hideStatusPanel)

        self.showButton = QPushButton()
        self.showButton.setIcon(QIcon('images/sys_images/expandIocn.png'))
        self.showButton.setObjectName("showButton")
        self.showButton.hide()
        self.showButton.pressed.connect(self.showStatusPanel)

        # create the h box for buttons
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.hideButton)
        hbox.addWidget(self.showButton)


        # create the vbox for tab
        self.reminderLyt = QVBoxLayout()
        self.reminderLyt.setContentsMargins(0, 0, 0, 0)
        self.reminderLyt.addLayout(hbox)
        self.reminderLyt.addWidget(self.reminderTab)

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

        self.reminderWidget.setLayout(self.reminderLyt)

        self.setUpStatusWidget()
        self.setUpReminderNoteWidget()


    def hideStatusPanel(self):

        # create the animation to hide the panel
        self.hideAnimation = QPropertyAnimation(self.reminderWidget, b"maximumWidth")
        self.hideAnimation.setStartValue(self.reminderWidget.width())
        self.hideAnimation.setEndValue(int(self.width * 0.03))
        self.hideAnimation.setDuration(500)
        self.hideAnimation.start(QPropertyAnimation.DeleteWhenStopped)

        self.showButton.show()
        self.hideButton.hide()

        try:
            self.statusWidget.hide()
            self.rootCollectionBox.hide()
            self.reminderTab.hide()
        except:
            pass


    def showStatusPanel(self):

        # create the animation to hide the panel
        self.showAnimation = QPropertyAnimation(self.reminderWidget, b"maximumWidth")
        self.showAnimation.setStartValue(self.reminderWidget.width())
        self.showAnimation.setEndValue(int(self.width * 0.15))
        self.showAnimation.setDuration(500)
        self.showAnimation.start(QPropertyAnimation.DeleteWhenStopped)

        self.showButton.hide()
        self.hideButton.show()

        try:
            self.statusWidget.show()
            self.rootCollectionBox.show()
            self.reminderTab.show()
        except:
            pass

    def setUpReminderNoteWidget(self):

        # crete the vbox for pack the buttons and note widgets
        reminderAddButton = QPushButton("add Note")
        reminderAddButton.setObjectName("reminderAddButton")
        reminderAddButton.pressed.connect(self.addNote)

        # create the vox for add the reminder notes
        self.reminderNotesLyt = QVBoxLayout()
        # add the button to the vbox
        self.reminderNotesLyt.addWidget(reminderAddButton)

        # create the scroll area for this
        scroll_area = QScrollArea()
        # create the scroll widget
        scrollWidget = QWidget()
        scrollWidget.setLayout(self.reminderNotesLyt)

        scroll_area.setWidget(scrollWidget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # create the temp v box for pack  the scroll_rae
        vbox = QVBoxLayout()
        vbox.addWidget(scroll_area)

        self.reminderNoteWidget.setLayout(vbox)

    def addNote(self):

        # create the new note widget
        noteWidget = QTextEdit()
        noteWidget.setMaximumWidth(300)
        noteWidget.setObjectName("reminderNote")

        self.reminderNotesLyt.addWidget(noteWidget, alignment=Qt.AlignTop)

    def setUpStatusWidget(self):

        # create the new status widget and pack to the StatusWidget
        self.statusBox = StatusWidget()

        # create the layout and pack to them
        self.status_vbox = QVBoxLayout()
        self.status_vbox.insertWidget(0, self.statusBox)
        self.status_vbox.addStretch()

        self.statusWidget.setLayout(self.status_vbox)

    def addNewItem(self, button : QPushButton):

        # pop up the new dialog for choose the collection or book
        self.selectDialog = QDialog(self)
        self.selectDialog.setObjectName("selectedDialog")
        self.selectDialog.setWindowOpacity(0.5)
        self.selectDialog.setModal(True)
        self.selectDialog.setWindowFlags(Qt.WindowType.FramelessWindowHint)

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

        button_right = button.mapToGlobal(button.rect().bottomRight())

        self.selectDialog.setLayout(vbox)
        self.selectDialog.setGeometry(QRect(button_right.x(), button_right.y() , 200, 200))
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
        date = QDate.currentDate().toString("dd MMM yyyy")
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
            widget.mouseDoubleClickEvent = lambda e, a = widget.book_id, b = widget.pw : self.openBookSpace(a, b)
            widget.mousePressEvent = lambda e, a = widget : self.setSelectionWidget(a)

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
        current_date = QDate.currentDate().toString("dd MMM yyyy")

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
            collection_widget = listCollectionWidget(title, des, img, path, "" ,id_code)
        else:
            collection_widget = boxCollectionWidget(title, des, img, path, "" , id_code)

        info_data = {"title": title,
                     "description": des,
                     "path": path,
                     "image_dir": img,
                     "date": current_date,
                     "time": current_time}
        self.currentStage.addCollection(collection_widget, info_data)

        # set the event handler
        collection_widget.mouseDoubleClickEvent = (lambda a, e = collection_widget.path,
                                                          i = collection_widget.collection_id , p = collection_widget.pw : self.openNewPage(e, i, p))
        collection_widget.mousePressEvent = (lambda a, e = collection_widget : self.setSelectedWidget(e))
        collection_widget.favoriteSignal.connect(self.updateFavoriteModel)
        collection_widget.statusSignal.connect(self.buildStatusWidget)



        # add to the layout
        if self.getTheme() == "list":
            self.stageLayout.insertWidget(0, collection_widget)
        else:
            # get the length of widgets
            count = self.currentStage.WidgetCount() - 1
            self.stageLayout.addWidget(collection_widget, count//4, count%4)

    def openNewPage(self, newPath : str, id : str, pw : str = ""):

        if pw != "":
            pw_text, ok = QInputDialog.getText(self, "Password Dialog", "Enter the Password : ", echo=QLineEdit.Password)
            if ok and pw_text == pw:
                check = True
            elif pw_text != pw and ok:
                check = False
                QMessageBox.warning(self, "Warning", "Password Incorrect! Please Try Again!")
            else:
                check = False
        else:
            check = True

        if check:
            # set the new path as the newPath
            self.currentPath = newPath
            # delete the all of widgets
            for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
                try:
                    widget.deleteLater()
                except:
                    pass

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
            self.status_vbox.insertWidget(1, self.rootCollectionBox)

            # disabled the collection tool bar actions
            for widget in self.collectionToolBarButton:
                widget.setDisabled(True)

            # set the path widget UI
            self.pathWidget.update(newPath)

            # create the thread and run the thread
            self.bookCoverLoadThread = bookCoverLoader(self.currentStage.bookWidgets)
            # start the book widget loader
            self.bookCoverLoadThread.start()
            if (self.bookCoverLoadThread.isFinished()):
                self.bookCoverLoadThread.deleteLater()

    def sortWidgets(self):

        # delete the all of widgets
        for widget in [*self.currentStage.collectionWidgets, *self.currentStage.bookWidgets]:
            try:
                widget.deleteLater()
            except:
                pass

        # clear the stage
        self.currentStage.clear()
        # add the new path to the stage history
        self.currentStage.addPath(self.currentPath)

        # render the new page
        self.renderNewPageForCollection(self.currentPath)
        self.renderNewPageForBook(self.currentPath)


    def refreshPage(self):

        # clear the currentStage
        for widget in [*self.currentStage.collectionWidgets, *self.currentStage.bookWidgets]:
            try:
                widget.deleteLater()
            except:
                pass

        self.stageLayout.deleteLater()
        del self.stageLayout
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

        # create the thread and run the thread
        self.bookCoverLoadThread = bookCoverLoader(self.currentStage.bookWidgets)
        # start the book widget loader
        self.bookCoverLoadThread.start()
        if (self.bookCoverLoadThread.isFinished()):
            self.bookCoverLoadThread.deleteLater()

    def gotoHome(self):

        self.currentPath = "/"
        for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
            try:
                widget.deleteLater()
            except:
                pass

        self.currentStage.clear()
        self.renderNewPageForCollection(self.currentPath)
        self.renderNewPageForBook(self.currentPath)


    def goBackOrForward(self, back : bool):

        # clear the widgets and stage
        for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
            try:
                widget.deleteLater()
            except:
                pass
        self.currentStage.clear()

        # set the new path
        if back:
            self.currentPath = self.currentStage.goBackward()
        else:
            self.currentPath =  self.currentStage.goForward()
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
                            "id" : data[i][1],
                            "pw" : data[i][6]}
                filter_data.append(new_dict)

        filter_data = self.sortCollection(filter_data)

        self.addCollectionWidgets(filter_data)

    def renderNewPageForBook(self, path : str):

        # get the need books data
        books_data = self.getNeedBooks(path)

        # generate the password dict
        pw_dict = {}
        for i in books_data:
            pw_dict[i[1]] = i[-1]
        # modified the data used the json file data
        json_data = {}
        with open("db/book.json", "r") as file:
            json_data = json.load(file)

        # filter the code data
        id_data = [item[1] for item in books_data]

        filter_json_data = []
        for item in json_data.keys():
            if item in id_data:
                pw = pw_dict.get(item , "")
                filter_json_data.append([item, json_data[item]["dir"], pw])


        # merge the lists
        originalData = []
        for i in range(len(books_data)):
            # create the new dictionary for this
            new_dict = {"title" : os.path.split(filter_json_data[i][1])[1],
                        "path" : books_data[i][2],
                        "dir" : filter_json_data[i][1],
                        "id" : books_data[i][1],
                        "pw" : filter_json_data[i][2]}
            originalData.append(new_dict)

        # create the new book used the original Data list
        self.addNewBookWidgets(originalData)

    def addNewBookWidgets(self, filterData : list):

        for data in filterData:
            # create the widget base on the theme
            if self.getTheme() == "list":
                widget = listBookWidget(data["title"], data["id"], data["path"], data["pw"])
                self.stageLayout.insertWidget(0, widget)
            else:
                widget = boxBookWidget(data["title"], data["id"], data["path"], data["pw"])
                count = self.currentStage.WidgetCount()
                self.stageLayout.addWidget(widget, count//4, count%4)

            # update the stage area
            self.currentStage.addBook(widget, data)
            # connect to the slots of the widget
            widget.favoriteSignal.connect(self.updateFavoriteModel)
            widget.mouseDoubleClickEvent = lambda e, a = widget.book_id , b = widget.pw : self.openBookSpace(a, b)
            widget.mousePressEvent = lambda e , a = widget : self.setSelectionWidget(a)




    def addCollectionWidgets(self, FilterData : list):

        for data in FilterData:
            # create the new widget
            if self.getTheme() == "list":
                widget = listCollectionWidget(data["title"], data["description"], data["image_dir"], data["path"], data["pw"] ,data["id"])
                self.stageLayout.addWidget(widget)
            else:
                widget = boxCollectionWidget(data["title"], data["description"], data["image_dir"], data["path"], data["pw"] ,data["id"])
                count = self.currentStage.WidgetCount()
                self.stageLayout.addWidget(widget, (count) // 4, (count) % 4)


            widget.mouseDoubleClickEvent = (lambda a, e = widget.path, i = widget.collection_id , p = widget.pw : self.openNewPage(e, i, p))
            widget.mousePressEvent = (lambda a, e = widget : self.setSelectionWidget(e))
            widget.favoriteSignal.connect(self.updateFavoriteModel)
            widget.statusSignal.connect(self.buildStatusWidget)
            # add the widget to stage
            self.currentStage.addCollection(widget, data)
        if isinstance(self.stageLayout, QVBoxLayout):
            self.stageLayout.addStretch()

    def buildStatusWidget(self, id : str):

        # create the new status widget
        newStatusWidget = FullStatusWidget(id)
        # add to the stage Tab
        self.stageTab.addTab(newStatusWidget, f"Tab {self.stageTab.currentIndex()}")

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

        if self.currentStage.selected_widget and (isinstance(self.currentStage.selected_widget, listCollectionWidget) or
                                                    isinstance(self.currentStage.selected_widget, boxCollectionWidget)):
            self.currentStage.selected_widget.baseWidget.setObjectName("collectionBaseWidget")
            self.currentStage.selected_widget.setStyleSheet(dark_style_sheet_for_Collection)
        # set thr stage selected widget as the this

        if isinstance(widget, boxCollectionWidget) or isinstance(widget , listCollectionWidget):
            self.currentStage.selected_widget = widget
            self.currentStage.selected_widget.baseWidget.setObjectName("collectionBaseWidgetSelected")
            self.currentStage.selected_widget.setStyleSheet(dark_style_sheet_for_Collection)
            # update the status
            self.setCollectionStatus()
        elif isinstance(widget, listBookWidget) or isinstance(widget, boxBookWidget):
            self.currentStage.selected_widget = widget
            self.setBookStatus()


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
        self.status_vbox.insertWidget(0, self.statusBox)
        # fill the status box
        self.statusBox.addLine("Title  ", widget_data["title"], wrap = True)
        self.statusBox.addTextArea("Description ", widget_data["des"])
        self.statusBox.addSeperator()
        # add the created date and time
        self.statusBox.addLabel(f"Created On\n {widget_data['date']}\nAt {widget_data['time']}")

        # set the colelction tool bar button as activate
        for button in self.collectionToolBarButton:
            button.setDisabled(False)

    def setBookStatus(self):

        book_widget = self.currentStage.selected_widget

        if isinstance(book_widget, listBookWidget) or isinstance(book_widget, boxBookWidget):
            # create the new status widget and append to the layout
            try:
                self.statusBox.deleteLater()
            except:
                pass
            # create the new status widget
            self.statusBox = StatusWidget()

            # book directory
            book_id = book_widget.book_id
            with open("db/book.json") as file:
                book_data = json.load(file)

            dir = book_data.get(book_id).get("dir")
            del book_data

            # get the book cover image
            cover_image = self.getCoverImage(dir)

            self.statusBox.addImage(cover_image)

            self.statusBox.addLabel("Name ")
            self.statusBox.addLabel(book_widget.title)

            self.statusBox.addLabel("Size ")
            self.statusBox.addLabel("{:.2f} MB".format((os.stat(dir).st_size/1024/1024)))

            self.status_vbox.insertWidget(0, self.statusBox)

    def openBookSpace(self, book_id : str, pw  : str = ""):

        check = False
        if (pw == ""):
            check = True
        else:
            # ask the password from the user
            text, ok  = QInputDialog.getText(self, "Password Dialog", "Enter the Password : ", echo=QLineEdit.Password)
            if ok:
                if pw == text:
                    check = True
                else:
                    QMessageBox.warning(self, "Incorrect Password", "Password is InCorrect , try Again!", QMessageBox.StandardButton.Ok)

        if check:
            # create the new book space
            newBookSpace = BookArea(book_id)

            # add to the stage tab bar
            newBookSpace.show()

    def advancedSearchPopUp(self, event):

        # first get the search bar rect object
        searchBarRect = self.searchBar.rect()
        # create the line edit for advanced search bar
        self.advancedSearchBar = QLineEdit()
        self.advancedSearchBar.setGeometry(QRect(self.searchBar.mapToGlobal(searchBarRect.bottomLeft()), QSize(searchBarRect.width(), 60)))
        self.advancedSearchBar.setFont(QFont('Hack', 14))
        self.advancedSearchBar.setTextMargins(10, 10, 10, 10)
        self.advancedSearchBar.setPlaceholderText("Advanced Search Bar")

        self.advancedSearchBar.setFocus()
        self.advancedSearchBar.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # set the search bar enter event
        self.advancedSearchBar.returnPressed.connect(self.advancedSearchTextPass)

        self.advancedSearchBar.show()

    def advancedSearchTextPass(self):

        self.advancedSearchBar.close()
        # get the serach text
        search_text = self.advancedSearchBar.text()
        self.advancedSearchBar.deleteLater()

        if search_text != "":
            # pass to the get the data from the data bases
            self.advancedSearchData(search_text)

    def advancedSearchData(self, text):

        connect = sqlite3.connect(self.db_file)
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM collection_table")
        data = cursor.fetchall()
        connect.close()

        new_data = []
        for coll in data:
            if text.lower() in coll[3].lower():
                new_data.append(coll)

        del data

        # reshape the data
        coll_data = {}
        with open("db/collection.json", "r") as file:
            coll_data = json.load(file)

        # generate the new dict for this
        shaped_data = []
        for i in new_data:
            new_dict = {"title": i[3],
                            "description": coll_data.get(i[1])["description"],
                            "path": i[2],
                            "image_dir": coll_data.get(i[1])["image_dir"],
                            "date": i[4],
                            "time": i[5],
                            "id": i[1],
                            "pw": i[6]}
            shaped_data.append(new_dict)
        del coll_data

        self.renderAdvancedSearchWidgets(shaped_data)

    def renderAdvancedSearchWidgets(self, data):

        for widget in [*self.currentStage.collectionWidgets , *self.currentStage.bookWidgets]:
            try:
                widget.deleteLater()
            except:
                pass

        self.currentStage.addPath(self.currentPath)
        # pass to the add collection widget method
        self.addCollectionWidgets(data)
        self.setBackForwardState()

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

    def getCoverImage(self, dir):

        doc = fitz.Document(dir)
        pix = doc.load_page(0).get_pixmap()

        image_dir = f"db/temp/coverImage{LibraryMangementSystem.getIdentifire()}.png"
        pix.save(image_dir)

        return image_dir

    @staticmethod
    def getIdentifire():

        length = 7
        index_str = ""

        for i in range(length):
            index_str += random.choice(chrs)

        return index_str

    def getTheme(self):

        # call to the theme box get state method
        theme = self.themeBox.getState()
        return theme

    def sortCollection(self, data):

        def dateObj(date_txt) :
            a, b, c = date_txt.split(":")
            return  QDate(int(c), int(b), int(a))

        # first get the sort option from the sortBox
        sort_option = self.sortingBox.currentIndex()

        if sort_option == 0:
            # filter the data based the title
            data.sort(key = lambda a: a["title"])
            return data
        elif sort_option == 1:
            data.sort(key=lambda a: a["title"], reverse=True)
            return data
        elif sort_option == 2:
            data.sort(key  = lambda a : dateObj(a['date']))
            return data
        elif sort_option == 3:
            data.sort(key = lambda a : dateObj(a['date']), reverse=True)

        return data


    def refreshDataBase(self):

        # create the new thread and remove the undefined pdf from the data base
        newThread = threading.Thread(target=refreshDataBase, args=(self.db_file, ))
        newThread.start()
        # join with main thread
        newThread.join()

    def viewFavoriteJSON(self):

        user_text = ""
        with open("db/favorite.json") as file:
            user_text = file.read()

        # create ethe new text editor
        self.viewEditor = QTextEdit()
        self.viewEditor.setMinimumSize(QSize(1000, 800))
        self.viewEditor.setText(user_text)
        self.viewEditor.setTextColor(QColor(0, 0, 255))
        self.viewEditor.setFont(QFont('Hack', 15))
        self.viewEditor.setReadOnly(True)

        self.viewEditor.setStyleSheet("""
                                    QTextEdit {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 20), stop : 1 rgb(0, 0, 100))}""")

        self.viewEditor.show()

    def closeEvent(self, event) -> None:

        # ask from the user
        message = QMessageBox(self)
        message.setWindowTitle("Close Dialog")
        message.setText("Are you sure to Close!")
        message.setIcon(QMessageBox.Icon.Warning)
        message.setObjectName("closeMessage")
        message.setStandardButtons(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        message = message.exec_()

        if message == QMessageBox.StandardButton.Yes:
            # delete th temporary files from the system
            for i in os.listdir("db/temp"):
                try:
                    os.removedirs(i)
                except FileNotFoundError:
                    print(f"cannot find the file...")
                except OSError:
                    print("Cannot delete the file because OS error")
                except PermissionError:
                    print("Not permissiom to delete file")
                except:
                    print("Cannot find the reason for delete the file")

            try:
                shutil.rmtree("db/temp")
            except:
                print("Cannot delete the temp folder...")

            self.close()
        else:
            event.ignore()


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
