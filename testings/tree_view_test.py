import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.Qt import QStandardItemModel, QStandardItem, Qt
from PyQt5.QtGui import QFont, QColor, QIcon, QImage

class standard_item(QStandardItem):
    def __init__(self, text = "" , font = "verdena", bold = False, color = QColor(0, 0, 0)):
        super(standard_item, self).__init__()

        font = QFont(font, 12)
        font.setBold(bold)

        self.setText(text)
        self.setForeground(color)
        self.setFont(font)


        image = QIcon("images/sys_images/close.png")

        self.setData(image, Qt.DecorationRole)

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setWindowTitle("Tree View")
        # create the tree view
        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(True)

        # create the tree model
        model = QStandardItemModel()
        rootNode = model.invisibleRootItem()

        # create the items of the mdodel
        amricaModel = standard_item("America", bold=True)
        srilanka_item = standard_item("sri Lanka", bold=True)

        # create the new list
        names = ["california", "andreas", "new york", "amstardam", "hamstardam"]

        items = []
        for i in names:
            # create the items
            item = standard_item(i)
            items.append(item)

        amricaModel.appendRows(items)

        rootNode.appendRow(amricaModel)
        rootNode.appendRow(srilanka_item)

        self.tree_view.setModel(model)
        self.setCentralWidget(self.tree_view)

        self.tree_view.doubleClicked.connect(self.getDate)
        self.tree_view.expandAll()
        self.resize(500, 600)
        self.show()

    def getDate(self, value):
        print(value.data())
        print(value.row())
        print(value.column())

if __name__ == "__main__":
    app = QApplication([])

    app.setStyle("Fusion")
    styles_sheet = """
                        QTreeView {background-color : black;
                        border: none;
                        color  :white}
                        
                        QTreeView::item {color : white;
                                        background-color : rgb(240, 60, 5);
                                        border : none;
                                        padding : 3px;}
                                        
                        QTreeView::item:hover {background-color : rgb(200, 60, 6);
                                            }
                                            
                        QTreeView::item:pressed {background-color : red}"""

    # app.setStyleSheet(styles_sheet)

    window = window()
    app.exec_()
