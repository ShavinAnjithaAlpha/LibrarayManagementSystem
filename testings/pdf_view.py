from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView



class PDF(QWebView):
    def __init__(self):
        super(PDF, self).__init__()
        self.setGeometry(0, 0, 1200, 900)
        self.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        # open the pdf file
        file, ok = QFileDialog.getOpenFileName(self, "PDF dialog", "", "PDF Files (*.pdf)")
        if ok:
            url = QUrl(file).toLocalFile()
            print(url)

            self.load(url)

        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = PDF()

    app.exec_()