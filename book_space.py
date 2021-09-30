import json, random
import os
import fitz

from style_sheet import style_sheet_dark_for_book
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout,
                             QInputDialog, QSplitter, QScrollArea, QDesktopWidget)
from PyQt5.QtCore import Qt, QSize, QTime, QDate
from PyQt5.QtGui import QFont, QPixmap, QPalette, QColor
from pdf_view import PDFViewer
from book_space_widgets import BookHistoryWidget, BookMarkWidget, CommentLabel, bookMarkLabel

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

        self.setWindowTitle(f"{self.bookName}")
        self.setGeometry(QDesktopWidget().geometry())
        self.setContentsMargins(0, 0, 0, 0)

        # create the main layout and widgets
        # create the history widget
        self.historyWidget = BookHistoryWidget(self.book_id)
        self.historyWidget.setContentsMargins(0, 0, 0, 0)
        # self.historyWidget.setObjectName("historyWidget")

        # create the other space widget
        otherSpace = QSplitter(Qt.Vertical)
        otherSpace.setContentsMargins(0, 0, 0, 0)
        # create the h box for pack the widgets
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)
        hbox1.setContentsMargins(0, 0, 0, 0)
        hbox1.addWidget(otherSpace)
        hbox1.addWidget(self.historyWidget)

        self.setLayout(hbox1)

        # create the top layout
        self.topLyt = QGridLayout()
        # create the widget for top layout
        topWidget = QWidget()
        topWidget.setContentsMargins(0, 0, 0, 0)
        topWidget.setLayout(self.topLyt)

        # create the h splitter
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        # create the bookmark widget
        self.bookMarkWidget = BookMarkWidget(self.book_id)
        #self.bookMarkWidget.setObjectName("bookmarkWidget")
        self.bookMarkWidget.setContentsMargins(0, 0, 0, 0)

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
        # openButton.pressed.connect(lambda e = self.dir : os.startfile(e) )
        openButton.pressed.connect(self.openPDF)

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
        self.setUpToolBoxWidget()

    def setUpToolBoxWidget(self):

        # create the title label
        titleLabel = QLabel("Tool Box")
        titleLabel.setObjectName("commentTitleLabel")
        titleLabel.setFont(QFont('verdana', 15))

        # create the vbox for this
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(titleLabel)
        vbox.addStretch()

        self.toolBoxWidget.setLayout(vbox)

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
        hbox1.setContentsMargins(0, 0, 0, 0)
        hbox1.addWidget(titleLabel)
        hbox1.addWidget(addButton)

        # create theh comment lyt
        self.commentLyt = QVBoxLayout()
        self.commentLyt.setSpacing(10)

        # widgdet for scroll area
        scrollWidget = QWidget()
        scrollWidget.setContentsMargins(0, 0, 0, 0)
        scrollWidget.setObjectName("bookCommentWidget")
        scrollWidget.setLayout(self.commentLyt)
        # create the scroll area
        scrollArea = QScrollArea()
        scrollArea.setContentsMargins(0, 0, 0, 0)
        scrollArea.setWidgetResizable(True)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(scrollWidget)

        # create the main v box layout
        mainVBox = QVBoxLayout()
        mainVBox.setSpacing(0)
        mainVBox.setContentsMargins(0, 0, 0, 0)
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
        mainVBox.setContentsMargins(0, 0, 0, 0)
        mainVBox.addWidget(titleLabel)
        mainVBox.addWidget(scrollArea)
        mainVBox.addStretch()

        self.statusWidget.setLayout(mainVBox)
        self.fillStatus()

    def fillStatus(self):

        # create the sub title label
        label1 = QLabel("PDF Informatins")
        label1.setObjectName("PDFLabel")
        label1.setObjectName("pdfLabel")
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


    def openPDF(self):

        with open("db/book.json") as file:
            data = json.load(file)

            book_path = data.get(self.book_id).get("dir")

        # open the PDF document with the custom widget
        self.pdfView = PDFViewer(book_path, self.book_id)











if __name__ == "__main__":
    app = QApplication([])

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

    window = BookArea("gquyy")
    window.show()

    app.exec_()