import fitz
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5.QtGui import QImage

app = QApplication([])

file ,ok = QFileDialog.getOpenFileName(None, "open pdf", "", "PDF (*.pdf)")


doc = fitz.Document(file)
print(doc.metadata)
print(doc.page_count)
print(doc.get_toc())
page = doc.load_page(0)

pic = page.get_pixmap()
fmt = QImage.Format_RGBA8888 if pic.alpha else QImage.Format_RGB888
qt = QImage(pic.samples_ptr, pic.width, pic.height, fmt)


app.exec_()