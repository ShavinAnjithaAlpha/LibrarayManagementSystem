from style_sheet import dark_style_sheet_for_widgets, dark_style_sheet_for_Collection
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLabel , QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit)
from PyQt5.Qt import Qt, QFont, QSize, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QPixmap

# create the collection widget
class collectionWidget(QWidget):


    def __init__(self, title, description, image_dir, path):
        super(collectionWidget, self).__init__()
        self.title = title
        self.description = description
        self.image_dir = image_dir
        self.path = path

        # create the container base widget
        self.baseWidget = QWidget(self)
        self.baseWidget.setObjectName("collectionBaseWidget")
        # create the v boc for pack the base widget
        v_box = QVBoxLayout()
        v_box.addWidget(self.baseWidget)
        self.setLayout(v_box)

        self.setStyleSheet(dark_style_sheet_for_Collection)

        # create the title , description and image labels
        self.titleLabel = QLabel(self.title)
        self.titleLabel.setFont(QFont('verdana', 18))
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        self.titleLabel.setObjectName("collectionTitleLabel")

        self.descriptionLabel = QLabel(self.description)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setFont(QFont("Hack", 11))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setObjectName("collectionDescriptionLabel")

        if self.description == "":
            self.descriptionLabel.setText("No Description yet")

        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(QSize(180, 200))
        self.imageLabel.setPixmap(
            QPixmap(self.image_dir).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))


class boxCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path):
        super(boxCollectionWidget, self).__init__(title, description, image_dir, path)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumSize(QSize(300, 250))
        self.setMaximumSize(QSize(500, 350))

        # create the grid layout for pack the items
        self.gridLyt  = QGridLayout()

        self.gridLyt.addWidget(self.titleLabel, 0, 0, 1, 2)
        self.gridLyt.addWidget(self.imageLabel, 1, 0, 1, 1)
        self.gridLyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)

        self.baseWidget.setLayout(self.gridLyt)


class listCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path):
        super(listCollectionWidget, self).__init__(title, description, image_dir, path)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumHeight(200)
        self.setMaximumHeight(350)

        self.titleLabel.setFont(QFont("verdana", 22))

        # create the grid lyt for pack items
        self.grid_lyt = QGridLayout()
        self.grid_lyt.addWidget(self.titleLabel, 0, 1, 1, 1)
        self.grid_lyt.addWidget(self.imageLabel, 0, 0, 2, 1)
        self.grid_lyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)

        self.baseWidget.setLayout(self.grid_lyt)


class switchButton(QWidget):

    # defined the new signal
    switchSignal = pyqtSignal()

    def __init__(self, textLeft, textRight, key1, key2):
        super(switchButton, self).__init__()
        self.textLeft , self.textRight = textLeft, textRight
        self.keys = {textLeft : key1,
                     textRight : key2}
        self.initializeUI()

        self.setStyleSheet(dark_style_sheet_for_widgets)

    def initializeUI(self):

        self.setContentsMargins(0, 0, 0, 0)
        # create the two buttons
        self.buttonLeft = QPushButton(self.textLeft)
        self.buttonLeft.setObjectName("switchButtonLeft")
        self.buttonLeft.setCheckable(True)
        self.buttonLeft.setChecked(True)

        self.buttonRight = QPushButton(self.textRight)
        self.buttonRight.setObjectName("switchButtonRight")
        self.buttonRight.setCheckable(True)
        self.buttonRight.setChecked(False)

        # set the button slots
        self.buttonLeft.clicked.connect(lambda a, e = "left" : self.setButtonState(e, a))
        self.buttonRight.clicked.connect(lambda a, e = "right" : self.setButtonState(e, a))

        # create the h box
        h_box = QHBoxLayout()
        h_box.setSpacing(0)
        h_box.addWidget(self.buttonLeft)
        h_box.addWidget(self.buttonRight)

        self.setLayout(h_box)


    def setButtonState(self, button , state):

        if button == "left":
            self.buttonLeft.setChecked(True)
            self.buttonRight.setChecked(False)
        elif button == "right":
            self.buttonRight.setChecked(True)
            self.buttonLeft.setChecked(False)

        # fire the signal
        self.switchSignal.emit()

    def getState(self):

        if self.buttonLeft.isChecked():
            return self.keys.get(self.buttonLeft.text())
        else:
            return self.keys.get(self.buttonRight.text())

if __name__ == "__main__":
    app = QApplication([])
    window = listCollectionWidget("Science", "this is the science section for get the some knowledges.....", "images/sys_images/coll_img1.jpg", "0/1/2")
    window.show()
    app.exec_()

