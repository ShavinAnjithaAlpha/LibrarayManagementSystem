import json, random
import shutil
import sqlite3
import os
import fitz

from style_sheet import style_sheet_dark_for_book
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QFormLayout, QMenu,
                             QAction, QInputDialog, QFileDialog, QPlainTextEdit, QLineEdit, QMessageBox, QSplitter, QScrollArea)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRectF, QTime, QDate
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QIcon, QPainter, QPen


class BookArea(QWidget):
    def __init__(self, book_id : str):
        super(BookArea, self).__init__()
        self.book_id = book_id
        self.dir , self.des = "", ""
        self.loadPDF()
        self.initializeUI()

        self.setStyleSheet(style_sheet_dark_for_book)

    def loadPDF(self):

        with open("db/book.json") as file:
           user_data = json.load(file)


        self.dir = user_data.get(self.book_id)["dir"]
        self.des = user_data.get(self.book_id).get("description", "")

        # set the book name attribute
        dir_split = os.path.split(self.dir)[1]
        self.bookName = os.path.splitext(dir_split)[0]

        try:
            # load the document
            self.pdf = fitz.Document(self.dir)

            # set the cover page image
            page1 = self.pdf.load_page(0)
            pix = page1.get_pixmap()
            pix.save("images/page1.png")
            self.coverImage = "images/page1.png"

        except Exception as e:
            print(e.__str__())
            print("Cannot load the pdf")

    def initializeUI(self):

        self.setGeometry(0, 0, 2000, 1000)
        self.setContentsMargins(0, 0, 0, 0)

        # create the main layout and widgets
        # create the history widget
        self.historyWidget = BookHistoryWidget(self.book_id)
        self.historyWidget.setObjectName("historyWidget")

        # create the other space widget
        otherSpace = QSplitter(Qt.Vertical)
        # create the h box for pack the widgets
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)
        hbox1.addWidget(otherSpace)
        hbox1.addWidget(self.historyWidget)

        self.setLayout(hbox1)

        # create the top layout
        self.topLyt = QGridLayout()
        # create the widget for top layout
        topWidget = QWidget()
        topWidget.setLayout(self.topLyt)

        # create the h splitter
        self.splitter = QSplitter(Qt.Horizontal)

        # create the bookmark widget
        self.bookMarkWidget = BookMarkWidget(self.book_id)
        self.bookMarkWidget.setObjectName("bookMarkWidget")

        # add to the v box
        otherSpace.addWidget(topWidget)
        otherSpace.addWidget(self.splitter)
        otherSpace.addWidget(self.bookMarkWidget)

        self.setUpTop()
        self.setUpSplitter()

    def setUpTop(self):

        # create the cover image label
        coverImageLabel = QLabel()
        coverImageLabel.setFixedSize(QSize(200, 300))
        coverImageLabel.setPixmap(QPixmap(self.coverImage).scaled(
                                            coverImageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        coverImageLabel.setObjectName("coverImage")

        # create the title label
        self.topTitleLabel = QLabel(self.bookName)
        self.topTitleLabel.setFont(QFont('verdana', 17))
        self.topTitleLabel.setWordWrap(True)
        self.topTitleLabel.setAlignment(Qt.AlignCenter)
        self.topTitleLabel.setObjectName("topTitleLabel")

        # create the open button
        openButton = QPushButton("Open")
        openButton.setObjectName("openButton")
        openButton.setFont(QFont('verdana', 16))
        openButton.pressed.connect(lambda e = self.dir : os.startfile(e) )

        # create the description label
        if self.des == "":
            self.descriptionLabel = QLabel("No Description Yet")
        else:
            self.descriptionLabel = QLabel(self.des)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setFont(QFont('verdana', 12))
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.descriptionLabel.setAlignment(Qt.AlignCenter)

        self.descriptionLabel.mousePressEvent = lambda e : self.changeDes(e)

        # pack to the grid layout
        self.topLyt.addWidget(coverImageLabel, 0, 0, 3, 1)
        self.topLyt.addWidget(self.topTitleLabel, 0, 1)
        self.topLyt.addWidget(openButton, 1, 1)
        self.topLyt.addWidget(self.descriptionLabel, 2, 1)

    def setUpSplitter(self):

        # create the three widget for splitter
        self.commentWidget = QWidget()
        self.statusWidget = QWidget()
        self.toolBoxWidget = QWidget()

        for widget in [self.commentWidget, self.statusWidget, self.toolBoxWidget]:
            widget.setContentsMargins(0, 0, 0, 0)

        self.commentWidget.setMinimumWidth(300)
        self.statusWidget.setMinimumWidth(450)
        self.statusWidget.setObjectName("bookStatusWidget")

        # set to the splitter
        self.splitter.addWidget(self.commentWidget)
        self.splitter.addWidget(self.statusWidget)
        self.splitter.addWidget(self.toolBoxWidget)

        self.setUpCommentWidget()
        self.setUpStatusWidget()

    def setUpCommentWidget(self):
        # create the title label
        titleLabel = QLabel("Comments")
        titleLabel.setFont(QFont('verdana', 12))
        titleLabel.setObjectName("commentTitleLabel")

        # create the add button
        addButton = QPushButton("+")
        addButton.setFont(QFont('verdana', 15))
        addButton.setObjectName("commentAddButton")
        addButton.pressed.connect(self.addComment)

        # create the h box for pack the widgets
        hbox1 = QHBoxLayout()
        hbox1.addWidget(titleLabel)
        hbox1.addWidget(addButton)

        # create theh comment lyt
        self.commentLyt = QVBoxLayout()
        self.commentLyt.setSpacing(10)

        # widgdet for scroll area
        scrollWidget = QWidget()
        scrollWidget.setObjectName("bookCommentWidget")
        scrollWidget.setLayout(self.commentLyt)
        # create the scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(scrollWidget)

        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.addLayout(hbox1)
        mainVBox.addWidget(scrollArea)


        self.commentWidget.setLayout(mainVBox)

        self.loadComments()

    def setUpStatusWidget(self):
        # create the title label
        titleLabel = QLabel("Book Informations")
        titleLabel.setFont(QFont('verdana', 12))
        titleLabel.setObjectName("statusTitleLabel")

        # create the vbox layout for status added
        self.statusLyt = QVBoxLayout()

        # create hte scrol area widget
        scrollWidget = QWidget()
        scrollWidget.setObjectName("pageStatusWidget")
        scrollWidget.setLayout(self.statusLyt)
        # create the scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(scrollWidget)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)



        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.addWidget(titleLabel)
        mainVBox.addWidget(scrollArea)
        mainVBox.addStretch()

        self.statusWidget.setLayout(mainVBox)
        self.fillStatus()

    def fillStatus(self):

        # create the sub title label
        label1 = QLabel("PDF Informatins")
        label1.setObjectName("PDFLabel")
        label1.setAlignment(Qt.AlignRight)
        self.statusLyt.addWidget(label1)

        pdf_metaData : dict = self.pdf.metadata
        for key , value in pdf_metaData.items():
            # create title label
            keyLabel = QLabel(f"<font color = 'blue'>{key}</font>")
            if value:
                valueLabel = QLabel(f"{value}")
            else:
                valueLabel = QLabel(f"None")
            keyLabel.setObjectName("keyLabel")
            valueLabel.setObjectName("valueLabel")

            self.statusLyt.addWidget(keyLabel)
            self.statusLyt.addWidget(valueLabel)
            self.statusLyt.addSpacing(20)

        # create the sub title label
        label2 = QLabel("System Informatins")
        label2.setObjectName("PDFLabel")
        label2.setAlignment(Qt.AlignRight)
        self.statusLyt.addWidget(label2)

    def loadComments(self):

        with open("db/book.json") as file:
            user_data = json.load(file)

        book = user_data.get(self.book_id)

        if book.get("comment", False):
            # create the comment widgets
            for item in book.get('comment'):
                # create the new comment widget and add to the widget
                commentWidget = CommentLabel(*item)
                # add to the lyt
                self.commentLyt.addWidget(commentWidget)


    def addComment(self):

        # get the comment frm the user
        text , ok  = QInputDialog.getMultiLineText(self, "Comment Dialog", "Enter the Comment : ")
        if ok:
            # create the new comment widget amd the add to the layout
            date, time = QDate.currentDate().toString("dd MMM yyyy"), QTime.currentTime().toString("hh:mm:ss A")
            commentWidget = CommentLabel(text, date, time)
            # add to the lyt
            self.commentLyt.addWidget(commentWidget)

            # update the files
            self.updateFiles(text, date ,time)

    def updateFiles(self, comment, date, time):

        with open("db/book.json") as file:
            user_data= json.load(file)

        book = user_data.get(self.book_id)

        if book.get("comment", False):
            book['comment'].append([comment, date, time])
        else:
            book['comment'] = [ [comment, date, time], ]

        # save the changes
        with open("db/book.json", "w") as file:
            json.dump(user_data, file, indent=4)

    def changeDes(self , event):

        # open the text dialog for get the user inputs
        text, ok  = QInputDialog.getMultiLineText(self, "Description Dialog", "Enter the new Description", text = self.descriptionLabel.text())

        if ok:
            # change the text of the description label
            self.descriptionLabel.setText(text)

            # update the book json file with description
            with open("db/book.json") as file:
                user_data = json.load(file)

            user_data.get(self.book_id)['description'] = text

            with open("db/book.json", "w") as file:
                json.dump(user_data, file, indent=4)

class BookHistoryWidget(QWidget):
    def __init__(self, book_id):
        super(BookHistoryWidget, self).__init__()
        self.book_id = book_id
        self.labels = []

        self.setMinimumWidth(300)
        self.setMaximumWidth(450)
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
        hbox1.addWidget(titleLabel)
        hbox1.addWidget(addButton)


        # create the scroll area for history bar
        scrollBar = QScrollArea()
        scrollBar.setWidgetResizable(True)
        scrollBar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollBar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # create the vboxo for labels
        self.pageLabelBox = QVBoxLayout()
        self.pageLabelBox.setSpacing(0)

        # create the acroll widget
        scrollWidget = QWidget()
        scrollWidget.setLayout(self.pageLabelBox)
        scrollWidget.setObjectName("historyWidget")

        scrollBar.setWidget(scrollWidget)



        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.addLayout(hbox1)
        mainVBox.addWidget(scrollBar)

        # create the base widget
        baseWidget = QWidget()
        baseWidget.setLayout(mainVBox)
        baseWidget.setObjectName("historyWidget")

        vbox = QVBoxLayout()
        vbox.addWidget(baseWidget)


        self.setLayout(vbox)

    def loadHistory(self):

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
        self.pageLabelBox.addWidget(label)
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
        hbox.addWidget(titleLabel)
        hbox.addWidget(addButton)

        # create the main v box
        self.bookmarkLyt = QVBoxLayout()
        self.bookmarkLyt.setSpacing(0)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
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
        bookmarklabel = bookMarkLabel(self.index, page, comment, date, time)
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

        vbox = QVBoxLayout()
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
    def __init__(self, i : int, page : int, comment : str, date : str, time : str):
        super(bookMarkLabel, self).__init__()
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

        pageNumberLabel = QLabel(f"at Page {self.data['page']}")
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
        hbox.addWidget(numberLabel)
        hbox.addWidget(pageNumberLabel)
        hbox.addWidget(commentLabel)
        hbox.addWidget(dateTimeLabel)

        self.setLayout(hbox)

if __name__ == "__main__":
    app = QApplication([])
    window = BookArea("gquyy")
    window.show()

    app.exec_()