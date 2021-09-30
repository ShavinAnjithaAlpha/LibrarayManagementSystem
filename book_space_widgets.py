import json, random
import os
import fitz

from style_sheet import style_sheet_dark_for_book
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout,
                             QInputDialog, QSplitter, QScrollArea, QDesktopWidget)
from PyQt5.QtCore import Qt, QSize, QTime, QDate
from PyQt5.QtGui import QFont, QPixmap
from simplePDFViewer import PDFViewew

class BookHistoryWidget(QWidget):
    def __init__(self, book_id):
        super(BookHistoryWidget, self).__init__()
        self.book_id = book_id
        self.labels = []

        self.setMinimumWidth(300)
        self.setMaximumWidth(450)
        self.setMinimumHeight(800)
        self.setContentsMargins(0, 0, 0, 0)

        self.initializeUI()
        self.loadHistory()

    def initializeUI(self):

        # create the title label
        titleLabel = QLabel("Page History")
        titleLabel.setFont(QFont('verdana', 12))
        titleLabel.setObjectName("pageTitleLabel")

        # create the add button
        addButton = QPushButton("+")
        addButton.setFont(QFont('verdana', 15))
        addButton.setObjectName("pageAddButton")
        addButton.pressed.connect(self.addPage)

        # create the h box for pack the widgets
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)
        hbox1.setContentsMargins(0, 0, 0, 0)
        hbox1.addWidget(titleLabel)
        hbox1.addWidget(addButton)


        # create the scroll area for history bar
        scrollBar = QScrollArea()
        scrollBar.setMinimumHeight(self.height())
        scrollBar.setWidgetResizable(True)
        scrollBar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollBar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # create the vbox for labels
        self.pageLabelBox = QVBoxLayout()
        self.pageLabelBox.setSpacing(0)
        self.pageLabelBox.setContentsMargins(0, 0, 0, 0)

        # create the scroll widget
        scrollWidget = QWidget()
        scrollWidget.setContentsMargins(0, 0, 0, 0)
        scrollWidget.setLayout(self.pageLabelBox)
        # scrollWidget.setObjectName("historyWidget2")

        scrollBar.setWidget(scrollWidget)
        scrollBar.setContentsMargins(0, 0, 0, 0)



        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.setContentsMargins(0, 0, 0, 0)
        mainVBox.addLayout(hbox1)
        mainVBox.addWidget(scrollBar)

        # create the base widget
        baseWidget = QWidget()
        baseWidget.setContentsMargins(0, 0, 0, 0)
        baseWidget.setLayout(mainVBox)
        #baseWidget.setObjectName("historyWidget")

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(baseWidget)


        self.setLayout(vbox)
        self.setStyleSheet(style_sheet_dark_for_book)

    def loadHistory(self):

        self.pageLabelBox.insertWidget(0, QLabel())
        self.pageLabelBox.addStretch()

        with open("db/book.json") as file:
            user_data = json.load(file)

        book = user_data.get(self.book_id)

        if book.get("history", False):
            # create the new history labels
            for item in book['history']:
                # create the new widget and add to the widget
                self.addLabel(*item)

    def addPage(self):

        # get the paeg number from the user
        pageNumber, ok = QInputDialog.getInt(self, "Page Number Dialog", "Enter the Page Number you last read : ")
        if ok:
            # ask the comment from the user
            comment, ok2 = QInputDialog.getMultiLineText(self, "Comment Dialog", "Enter the Comment About Page : ")
            if ok2:
                # create the new page widget and add to history widget
                # get the current time and date
                date, time = QDate.currentDate().toString("dd MMM yyyy") , QTime.currentTime().toString("hh:mm:ss A")
                # create the label
                self.addLabel(pageNumber, comment, date, time)
                self.updateFile(pageNumber, comment, date, time)

    def addLabel(self, page, comment, date, time):

        label = pageHistoryLabel(page, comment, date, time)
        self.labels.append(label)
        # add to the vbox
        self.pageLabelBox.insertWidget(0, label)
        # update the file

    def updateFile(self, page, comment, date, time):

        with open("db/book.json") as file:
            user_data = json.load(file)

        book = user_data.get(self.book_id)

        if book.get("history", False):
            book['history'].append([page, comment, date, time])
        else:
            book['history'] = [ [page, comment, date, time],  ]


        # save the changes
        with open("db/book.json", "w") as file:
            json.dump(user_data, file, indent=4)


class BookMarkWidget(QWidget):
    def __init__(self, book_id : str):
        super(BookMarkWidget, self).__init__()

        self.index = 1
        self.bookmarkLabels = []
        self.book_id = book_id

        self.initializeUI()
        self.loadBookmarks()

    def initializeUI(self):
        self.setMinimumHeight(300)
        self.setObjectName("bookmarkWidget")

        # create the top title layout
        titleLabel = QLabel("Your Book BookMarks")
        titleLabel.setFont(QFont('verdana', 13))
        titleLabel.setObjectName("bookmarkTitleLabel")

        # create the add button
        addButton = QPushButton("+")
        addButton.setFont(QFont('verdana', 15))
        addButton.setObjectName("bookmarkAddButton")
        addButton.pressed.connect(self.addBookMark)

        # create the h box
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(titleLabel)
        hbox.addWidget(addButton)

        # create the main v box
        self.bookmarkLyt = QVBoxLayout()
        self.bookmarkLyt.setSpacing(0)
        self.bookmarkLyt.setContentsMargins(0, 0, 0, 0)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(self.bookmarkLyt)
        vbox.addStretch()

        self.setLayout(vbox)

    def loadBookmarks(self):

        with open("db/book.json") as file:
            user_data  = json.load(file)

        book = user_data.get(self.book_id)
        if book.get('bookmarks', False):
            # fill the widget with the bookmarks
            for mark in book["bookmarks"]:
                # create the new label
                self.addLabel(*mark)


    def addBookMark(self):

        # get the page number and comment from the user
        page, ok = QInputDialog.getInt(self, "Page Number Dialog", "Enter the Page Number")
        if ok:
            comment, ok2 = QInputDialog.getMultiLineText(self, "Comment Dialog", "Enter the Comment about the BookMark")
            if ok2:
                # set the number and page at the bookmark widget
                date , time = QDate.currentDate().toString("dd MMM yyyy"), QTime.currentTime().toString("hh:mm:ss A")
                self.addLabel(page, comment, date, time)

                # update the data base
                self.updateFile(page, comment, date, time)


    def addLabel(self, page, comment, date, time):

        # create the bookmark widget and increase the index
        bookmarklabel = bookMarkLabel(self.index, page, comment, date, time, self)
        self.index += 1
        self.bookmarkLyt.addWidget(bookmarklabel)
        # add to the bookmark list
        self.bookmarkLabels.append(bookmarklabel)


    def updateFile(self, page, comment, date ,time):

        with open("db/book.json") as file:
            user_data = json.load(file)

        # get the user data book
        book = user_data.get(self.book_id)

        # append the new bookmark to file's this book
        if book.get("bookmarks", False):
            book['bookmarks'].append([page, comment, date, time])
        else:
            book["bookmarks"] = [ [page, comment, date ,time] , ]

        # save the changes
        with open("db/book.json", "w") as file:
            json.dump(user_data, file, indent=4)

class pageHistoryLabel(QWidget):
    def __init__(self, pageNumber : int, comment : str, date, time):
        super(pageHistoryLabel, self).__init__()
        self.pageNumber = pageNumber
        self.comment = comment
        self.date = date
        self.time = time

        baseWidget = QWidget()
        baseWidget.setObjectName("pageBase")
        baseWidget.setContentsMargins(0, 0, 0, 0)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(baseWidget)

        self.setLayout(vbox)
        # create the main three labels
        # page number label
        pageLabel = QLabel(f"Page {self.pageNumber}")
        pageLabel.setObjectName("pageNumberLabel")
        pageLabel.setFont(QFont('verdana', 13))
        pageLabel.setAlignment(Qt.AlignRight)

        # create the comment label
        if self.comment != "":
            commentLabel = QLabel(self.comment)
            commentLabel.setObjectName("pageCommentLabel")
            commentLabel.setFont(QFont('verdana', 11))
            commentLabel.setWordWrap(True)

        # create the time and date label
        dateTimeLabel = QLabel(f"{self.date} at {self.time}")
        dateTimeLabel.setObjectName("pageDateTimeLabel")
        dateTimeLabel.setFont(QFont('verdana', 10))


        # create the vbox
        vbox = QVBoxLayout()
        vbox.addWidget(pageLabel)
        if self.comment != "":
            vbox.addWidget(commentLabel)
        vbox.addWidget(dateTimeLabel)

        baseWidget.setLayout(vbox)

    def sizeHint(self) -> QSize:

        font_metrix = QApplication.fontMetrics()
        # rect  = self.rect()
        rect = font_metrix.boundingRect(self.comment)
        return rect.size()

class CommentLabel(QWidget):

    colors = ["red", "blue", "rgb(50, 0, 50)", "rgb(70, 0, 100)"]

    gradients = ["QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 50), stop : 1 rgb(0, 0, 200))",
                 "QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(80, 0, 50), stop : 1 rgb(200, 0, 200))",
                 "QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(50, 0, 0), stop : 1 rgb(220, 0, 0))",
                 "QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 50, 0), stop : 1 rgb(0, 200, 0))"]

    def __init__(self, comment, date, time):
        super(CommentLabel, self).__init__()
        self.setMaximumHeight(200)
        self.comment = comment
        self.date = date
        self.time = time
        self.baseColor = random.choice(self.gradients)

        baseWidget = QWidget()
        baseWidget.setObjectName("commentLabelBase")
        styleStr = """
                            QWidget#commentLabelBase {background : %s;
                                        padding : 10px;
                                        border : none;
                                        border-radius : 20px;
                                        margin : 0px;}"""%(self.baseColor)
        baseWidget.setStyleSheet(styleStr)
        vbox = QVBoxLayout()
        vbox.addWidget(baseWidget)

        self.setLayout(vbox)
        # create the main three labels

        # create the comment label
        commentLabel = QLabel(self.comment)
        commentLabel.setObjectName("pageCommentLabel")
        commentLabel.setFont(QFont('verdana', 11))
        commentLabel.setWordWrap(True)
        # create the time and date label
        dateTimeLabel = QLabel(f"{self.date} at {self.time}")
        dateTimeLabel.setObjectName("pageDateTimeLabel")
        dateTimeLabel.setFont(QFont('verdana', 10))


        # create the vbox
        vbox = QVBoxLayout()
        vbox.addWidget(commentLabel)
        vbox.addWidget(dateTimeLabel)
        baseWidget.setLayout(vbox)

class bookMarkLabel(QWidget):
    def __init__(self, i : int, page : int, comment : str, date : str, time : str, parent = None):
        super(bookMarkLabel, self).__init__()
        self.parent = parent
        self.data = {"i" : i,
                     "page" : page,
                     "comment" : comment,
                     "date": date,
                     "time" : time}
        self.initializeUI()

    def initializeUI(self):
        self.setContentsMargins(0, 0, 0, 0)

        # create the number label
        numberLabel = QLabel(f"#{self.data['i']}")
        numberLabel.setObjectName("bookmarkIndexLabel")

        pageNumberLabel = QPushButton(f"at Page {self.data['page']}")
        pageNumberLabel.pressed.connect(self.loadPage)
        pageNumberLabel.setObjectName("bookmarkPageLabel")

        commentLabel = QLabel(self.data['comment'])
        commentLabel.setObjectName("bookmarkCommentLabel")
        commentLabel.setWordWrap(True)

        # create the date time label
        dateTimeLabel = QLabel(f"{self.data['date']} at {self.data['time']}")
        dateTimeLabel.setObjectName("bookmarkDateLabel")
        dateTimeLabel.setAlignment(Qt.AlignRight)

        for widget in [numberLabel, pageNumberLabel, commentLabel, dateTimeLabel]:
            widget.setFont(QFont('verdana', 10))
            widget.setContentsMargins(0, 0, 0, 0)

        # pack the labels
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(numberLabel)
        hbox.addWidget(pageNumberLabel)
        hbox.addWidget(commentLabel)
        hbox.addWidget(dateTimeLabel)

        self.setLayout(hbox)

    def loadPage(self):

        with open("db/book.json") as file:
            data = json.load(file)

            file = data.get(self.parent.book_id).get("dir")

        # create the pdf viewer and load the pdf
        self.pdf_viewer = PDFViewew(file , int(self.data["page"]))
