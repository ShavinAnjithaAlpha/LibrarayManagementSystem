from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QStatusBar,  QWidget ,QAction,QToolBar,QDesktopWidget ,
    QApplication, QMainWindow, QLabel ,QProgressBar, QLineEdit, QPushButton, QHBoxLayout)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette,QColor
from book_space_widgets import BookHistoryWidget, CommentLabel


class PDFViewer(QMainWindow):
    def __init__(self, file, book_id):
        super(PDFViewer, self).__init__()
        # load the pdf file
        self.pdf_file = file
        self.book_id = book_id
        self.initializeUI()

    def initializeUI(self):

        self.setWindowTitle(self.pdf_file)
        # create the tool bar and statu sbar and the web view widget
        self.setUpToolBar()
        self.setUpWebView()

        # create the statu sbar for window
        self.status_bar  = QStatusBar()
        self.setStatusBar(self.status_bar)

        desktop = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, desktop.width(), desktop.height())

        self.show()

    def setUpToolBar(self):

        # create the new toll bar for main window
        self.toolBar = QToolBar()
        self.toolBar.setWindowTitle("PDf Viewer Tool Bar")
        self.setIconSize(QSize(30, 30))
        self.addToolBar(self.toolBar)

        # create the actions for this
        exitAction = QAction("Exit", self)
        exitAction.triggered.connect(self.close)



        self.toolBar.addAction(exitAction)

    def setUpWebView(self):

        # create the web view for this
        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(QWebEngineSettings.PdfViewerEnabled, True)
        self.webView.settings().setAttribute(QWebEngineSettings.ScrollAnimatorEnabled, True)
        self.webView.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        # create the book history widget
        self.historyWidget = BookHistoryWidget(self.book_id)

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.addWidget(self.webView)
        hbox.addWidget(self.historyWidget)
        # create the main widget
        central_widget = QWidget()
        central_widget.setLayout(hbox)

        self.setCentralWidget(central_widget)

        if self.pdf_file:
            # create the url
            url = QUrl(self.pdf_file)
            # load to the web view
            self.webView.load(url)

            # create the status bar progess widgets
            self.loading_pg = QProgressBar()
            self.loading_pg.setVisible(False)
            self.loading_label = QLabel()
            self.loading_label.setVisible(False)

            self.webView.loadProgress.connect(self.updateLoading)

    def updateLoading(self, value : int):

        if value < 100:
            # set the values
            self.loading_pg.setVisible(True)
            self.loading_pg.setValue(value)
            self.loading_pg.setMaximum(100)

            self.loading_label.setVisible(True)
            self.loading_label.setText(f"loading : {value}%")
            # add to the status bar
            self.status_bar.addWidget(self.loading_pg)
            self.status_bar.addWidget(self.loading_label)
        else:
            self.status_bar.removeWidget(self.loading_pg)
            self.status_bar.removeWidget(self.loading_label)

if __name__ == "__main__":
    app = QApplication([])

    window = PDFViewer()

    app.exec_()