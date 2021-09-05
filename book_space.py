import json
import shutil
import sqlite3
import os

from style_sheet import style_sheet_dark_for_book
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy, QFormLayout, QMenu,
                             QAction, QInputDialog, QFileDialog, QPlainTextEdit, QLineEdit, QMessageBox, QSplitter)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRectF, QTime, QDate
from PyQt5.QtGui import QFont, QColor, QPixmap, QImage, QIcon, QPainter, QPen


class BookArea(QWidget):
    def __init__(self, collection_id : str):
        super(BookArea, self).__init__()
        self.collection_id = collection_id
        self.initializeUI()

        self.setStyleSheet(style_sheet_dark_for_book)

    def initializeUI(self):

        self.setMinimumWidth(600)
        self.setContentsMargins(0, 0, 0, 0)

        # create the main layout and widgets
        # create the history widget
        self.historyWidget = BookHistoryWidget()
        self.historyWidget.setObjectName("historyWidget")

        # create the other space widget
        otherSpace = QVBoxLayout()
        otherSpace.setSpacing(0)
        # create the h box for pack the widgets
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)
        hbox1.addLayout(otherSpace)
        hbox1.addWidget(self.historyWidget)

        self.setLayout(hbox1)

        # create the top layout
        self.topLyt = QGridLayout()
        # create the h splitter
        self.splitter = QSplitter(Qt.Horizontal)

        # create the bookmark widget
        self.bookMarkWidget = BookMarkWidget()
        self.bookMarkWidget.setObjectName("bookMarkWidget")

        # add to the v box
        otherSpace.addLayout(self.topLyt)
        otherSpace.addWidget(self.splitter)
        otherSpace.addWidget(self.bookMarkWidget)

        self.setUpTop()
        self.setUpSplitter()

    def setUpTop(self):

        # create the cover image label
        coverImageLabel = QLabel()
        coverImageLabel.setFixedSize(QSize(200, 300))
        coverImageLabel.setPixmap(QPixmap("images/iphone-12-2160x3840-black-abstract-apple-october-2020-event-4k-23079.jpg").scaled(
                                            coverImageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        coverImageLabel.setObjectName("coverImage")

        # create the title label
        self.topTitleLabel = QLabel("Shavin Anjitha Chandrawansha")
        self.topTitleLabel.setFont(QFont('verdana', 17))
        self.topTitleLabel.setWordWrap(True)
        self.topTitleLabel.setAlignment(Qt.AlignCenter)
        self.topTitleLabel.setObjectName("topTitleLabel")

        # create the open button
        openButton = QPushButton("Open")
        openButton.setObjectName("openButton")
        openButton.setFont(QFont('verdana', 16))

        # create the descriptioon label
        descriptionLabel = QLabel("No Description Yet")
        descriptionLabel.setWordWrap(True)
        descriptionLabel.setFont(QFont('verdana', 12))
        descriptionLabel.setObjectName("descriptionLabel")
        descriptionLabel.setAlignment(Qt.AlignCenter)

        # pack to the grid layout
        self.topLyt.addWidget(coverImageLabel, 0, 0, 3, 1)
        self.topLyt.addWidget(self.topTitleLabel, 0, 1)
        self.topLyt.addWidget(openButton, 1, 1)
        self.topLyt.addWidget(descriptionLabel, 2, 1)

    def setUpSplitter(self):

        # create theh three widget for splitter
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

        # create the h box for pack the widgets
        hbox1 = QHBoxLayout()
        hbox1.addWidget(titleLabel)
        hbox1.addWidget(addButton)

        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.addLayout(hbox1)
        mainVBox.addStretch()

        self.commentWidget.setLayout(mainVBox)

    def setUpStatusWidget(self):
        # create the title label
        titleLabel = QLabel("Book Informations")
        titleLabel.setFont(QFont('verdana', 12))
        titleLabel.setObjectName("statusTitleLabel")

        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.addWidget(titleLabel)
        mainVBox.addStretch()

        self.statusWidget.setLayout(mainVBox)



class BookHistoryWidget(QWidget):
    def __init__(self):
        super(BookHistoryWidget, self).__init__()
        self.setMinimumWidth(300)
        self.initializeUI()

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

        # create the vboxo for labels
        self.pageLabelBox = QVBoxLayout()
        self.pageLabelBox.setSpacing(0)


        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.addLayout(hbox1)
        mainVBox.addLayout(self.pageLabelBox)
        mainVBox.addStretch()

        self.setLayout(mainVBox)

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
                label = pageHistoryLabel(pageNumber, comment, date ,time)
                # add to the vbox
                self.pageLabelBox.addWidget(label)



class BookMarkWidget(QWidget):
    def __init__(self):
        super(BookMarkWidget, self).__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumHeight(300)

        # create the lbel
        label = QLabel("BookMark Label")

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.setSpacing(0)

        self.setLayout(vbox)


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



if __name__ == "__main__":
    app = QApplication([])
    window = BookArea("shdjds6d5")
    window.show()

    app.exec_()