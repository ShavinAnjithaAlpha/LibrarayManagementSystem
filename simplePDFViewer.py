import os, sys
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar, QApplication, QHBoxLayout, QLabel, QLineEdit, QFileDialog, \
    QVBoxLayout, QSlider, QScrollArea, QPushButton, QTextBrowser, QDesktopWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont, QKeyEvent, QPalette, QColor
import fitz

class PDFViewew(QMainWindow):
    def __init__(self, file_name : str  = None , pageNumber : int = 0):
        super(PDFViewew, self).__init__()
        desktop_geo = QDesktopWidget().screenGeometry()
        self.setGeometry(desktop_geo)
        self.setWindowTitle(f"{file_name} : with Libraray Managment System")

        self.matrix = fitz.Matrix(3, 3)

        self.file = file_name
        self.pageNumber = pageNumber

        self.doc = fitz.Document(self.file)
        page = self.doc[self.pageNumber]
        pix = page.get_pixmap(matrix = self.matrix)

        self.page_image = "db/pdfImage.png"
        pix.save(self.page_image)

        # create the tool bar
        self.toolBar = QToolBar()
        self.toolBar.setIconSize(QSize(50, 50))
        self.addToolBar(self.toolBar)

        # create the line edit
        self.textEdit = QLineEdit()
        self.textEdit.setTextMargins(10, 10, 10, 10)
        self.textEdit.setMaximumSize(QSize(200, 30))
        self.textEdit.setFont(QFont('verdana', 15))
        self.textEdit.addAction(QAction("Search"), QLineEdit.LeadingPosition)
        self.textEdit.returnPressed.connect(self.loadPage)

        # create the slider
        self.slider = QSlider()
        # self.slider.addAction()
        self.slider.setRange(0, 500)
        self.slider.setMaximumHeight(250)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.zoom)

        up_button = QAction(QIcon("images/sys_images/up_arrow.png"), "Next",self)
        up_button.triggered.connect(self.nextPage)

        down_button = QAction(QIcon("images/sys_images/down_arraow.png"), "Back", self)
        down_button.triggered.connect(self.backPage)

        # self.pageNumber = 0

        self.label_width = 1500
        self.label_height = 1200

        self.label = QLabel()
        self.label.resize(self.label_width, self.label_height)
        self.label.setPixmap(QPixmap(self.page_image).scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


        # creat ehte scrol area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.label)

        self.setCentralWidget(scrollArea)

        self.textEdit.setFocus()
        # add the tool ba actions
        self.toolBar.setContentsMargins(10, 10, 10, 10)

        self.toolBar.addAction(down_button)
        self.toolBar.addAction(up_button)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(QLabel("Page Number"))
        self.toolBar.addWidget(self.textEdit)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(QLabel("Zoom"))
        self.toolBar.addWidget(self.slider)
        self.toolBar.addSeparator()
        self.show()


    def nextPage(self):

        if self.pageNumber < self.doc.page_count:
            self.pageNumber += 1

            page = self.doc[self.pageNumber]
            pix = page.get_pixmap(matrix=self.matrix)
            pix.save(self.page_image)

            zoom_factor = self.slider.value() / 100
            new_w, new_h = self.label_width * zoom_factor, self.label_height * zoom_factor

            self.label.setFixedSize(int(new_w), int(new_w))
            self.label.setPixmap(
                QPixmap(self.page_image).scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # self.textEdit.setText(self.pageNumber)
            # self.browser.setHtml(page.get_text("html"))

    def backPage(self):

        if self.pageNumber > 0:
            self.pageNumber -= 1

            page = self.doc[self.pageNumber]
            pix = page.get_pixmap(matrix=self.matrix)
            pix.save(self.page_image)

            zoom_factor = self.slider.value() / 100
            new_w, new_h = self.label_width * zoom_factor, self.label_height * zoom_factor

            self.label.setFixedSize(int(new_w), int(new_w))
            self.label.setPixmap(
                QPixmap(self.page_image).scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.textEdit.setText(self.pageNumber)
            # self.browser.setHtml(page.get_text("html"))

    def keyPressEvent(self, event : QKeyEvent) -> None:

        if (event.key() == Qt.Key_Plus):
            # zoom the page
            self.slider.setValue(self.slider.value() + 40)
        elif (event.key() == Qt.Key_Minus):
            if (self.slider.value() > 40):
                self.slider.setValue(self.slider.value() - 40)

        elif (event.key() == Qt.Key_Right):
            self.nextPage()
        elif (event.key() == Qt.Key_Left):
            self.backPage()

    def zoom(self, value : float):

        zoom_factor = value / 100
        new_w, new_h = self.label_width * zoom_factor, self.label_height * zoom_factor

        self.label.setFixedSize(int(new_w), int(new_w))
        self.label.setPixmap(QPixmap(self.page_image).scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def loadPage(self):

        pageNum = -1
        if self.textEdit.text().isnumeric():
            pageNum = int(self.textEdit.text())

        if pageNum <= self.doc.page_count and pageNum >= 0:
            page = self.doc[pageNum]
            pix = page.get_pixmap(matrix=self.matrix)
            pix.save(self.page_image)
            self.pageNumber = pageNum
            self.label.setPixmap(QPixmap(self.page_image).scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            # self.browser.setHtml(page.get_text("html"))

        if (self.textEdit.text().isalpha()):
            text = self.textEdit.text()

            for i in range(self.doc.page_count):
                page = self.doc.load_page(i)
                word = page.search_for(text)

                if word != []:
                    self.pageNumber = i

                    page = self.doc[self.pageNumber]
                    pix = page.get_pixmap(matrix=self.matrix)
                    pix.save(self.page_image)

                    zoom_factor = self.slider.value() / 100
                    new_w, new_h = self.label_width * zoom_factor, self.label_height * zoom_factor

                    self.label.setFixedSize(int(new_w), int(new_w))
                    self.label.setPixmap(
                        QPixmap(self.page_image).scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

                    # self.browser.setHtml(page.get_text("html"))
                    break

if __name__ == "__main__":
    app = QApplication([])
    wondow = PDFViewew()

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

    app.exec_()