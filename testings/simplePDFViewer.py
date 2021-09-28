import os, sys
from PyQt5.QtWidgets import QWidget, QApplication,QHBoxLayout , QLabel, QLineEdit, QFileDialog, QVBoxLayout, QSlider, QScrollArea, QPushButton, QTextBrowser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import fitz

class PDFViewew(QWidget):
    def __init__(self):
        super(PDFViewew, self).__init__()
        self.setGeometry(0, 0, 1000, 1000)

        self.matrix = fitz.Matrix(3, 3)

        file, ok = QFileDialog.getOpenFileName(self, "pdf file", "", "PDf (*.pdf)")
        if ok:
            self.file = file
            self.doc = fitz.Document(self.file)
            page = self.doc[0]
            pix = page.get_pixmap(matrix = self.matrix)
            pix.save("pdfImage.png")

            self.html = page.get_text("html")

        # creat the line edit
        self.textEdit = QLineEdit()
        self.textEdit.returnPressed.connect(self.loadPage)

        # create the slider
        self.slider = QSlider()
        self.slider.setRange(0, 500)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.zoom)

        button = QPushButton(">")
        button.pressed.connect(self.nextPage)

        self.pageNumber = 0

        self.label = QLabel()
        self.label.resize(1000, 900)
        self.label.setPixmap(QPixmap("pdfImage.png").scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # create hte text browser
        self.browser = QTextBrowser()
        self.browser.setHtml(self.html)

        # creat ehte scrol area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(self.label)

        hbox = QHBoxLayout()
        hbox.addWidget(scrollArea)
        hbox.addWidget(self.browser)

        vbox = QVBoxLayout()
        vbox.addWidget(self.textEdit)
        vbox.addWidget(button)
        vbox.addWidget(self.slider)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.show()


    def nextPage(self):

        if self.pageNumber < self.doc.page_count:
            self.pageNumber += 1

            page = self.doc[self.pageNumber]
            pix = page.get_pixmap(matrix=self.matrix)
            pix.save("pdfImage.png")

            zoom_factor = self.slider.value() / 100
            new_w, new_h = 1000 * zoom_factor, 900 * zoom_factor

            self.label.setFixedSize(int(new_w), int(new_w))
            self.label.setPixmap(
                QPixmap("pdfImage.png").scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.browser.setHtml(page.get_text("html"))

    def zoom(self, value : float):

        zoom_factor = value / 100
        new_w, new_h = 1000 * zoom_factor, 900 * zoom_factor

        self.label.setFixedSize(int(new_w), int(new_w))
        self.label.setPixmap(QPixmap("pdfImage.png").scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def loadPage(self):

        pageNum = -1
        if self.textEdit.text().isnumeric():
            pageNum = int(self.textEdit.text())

        if pageNum <= self.doc.page_count and pageNum >= 0:
            page = self.doc[pageNum]
            pix = page.get_pixmap(matrix=self.matrix)
            pix.save("pdfImage.png")
            self.pageNumber = pageNum
            self.label.setPixmap(QPixmap("pdfImage.png").scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.browser.setHtml(page.get_text("html"))

        if (self.textEdit.text().isalpha()):
            text = self.textEdit.text()

            for i in range(self.doc.page_count):
                page = self.doc.load_page(i)
                word = page.search_for(text)

                if word != []:
                    self.pageNumber = i

                    page = self.doc[self.pageNumber]
                    pix = page.get_pixmap(matrix=self.matrix)
                    pix.save("pdfImage.png")

                    zoom_factor = self.slider.value() / 100
                    new_w, new_h = 1000 * zoom_factor, 900 * zoom_factor

                    self.label.setFixedSize(int(new_w), int(new_w))
                    self.label.setPixmap(
                        QPixmap("pdfImage.png").scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

                    self.browser.setHtml(page.get_text("html"))
                    break

if __name__ == "__main__":
    app = QApplication([])
    wondow = PDFViewew()
    app.exec_()