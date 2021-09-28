import fitz
from PyQt5.QtWidgets import QFileDialog, QApplication, QTextBrowser
from PyQt5.QtGui import QImage

app = QApplication([])

file ,ok = QFileDialog.getOpenFileName(None, "open pdf", "", "PDF (*.pdf)")


doc = fitz.Document(file)
print(doc.metadata)
print(doc.page_count)
print(doc.get_toc())
page = doc.load_page(0)

print(doc.load_page(100).get_images())
print(doc.load_page(100).get_links())
html = doc.load_page(443).get_text("xhtml")

with open("web.xhtml", "w") as file:
    file.writelines(html)

matrix = fitz.Matrix(3, 3)
display = doc.load_page(180).get_displaylist()
pix = display.get_pixmap(matrix = matrix)
pix.save("pixmap.png")

window = QTextBrowser()
window.setHtml(html)
window.show()


pic = page.get_pixmap()
fmt = QImage.Format_RGBA8888 if pic.alpha else QImage.Format_RGB888
qt = QImage(pic.samples_ptr, pic.width, pic.height, fmt)


app.exec_()