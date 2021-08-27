import os, shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QDialogButtonBox, QTextEdit, QCheckBox, QFileDialog)
from PyQt5.Qt import Qt, QSize, QFont
from PyQt5.QtGui import QColor
from style_sheet import dark_style_sheet_for_widgets

class newCollectionDialog(QDialog):

    default_image = "images/sys_images/coll_img1.png"

    def __init__(self, parent = None):
        super(newCollectionDialog, self).__init__(parent=parent)
        self.initializeUI()

    def initializeUI(self):

        self.setWindowTitle("New Collection Dialog")
        self.setFixedSize(QSize(600, 600))
        self.setModal(True)

        self.setUpWidget()
        self.setStyleSheet(dark_style_sheet_for_widgets)

        self.show()

    def setUpWidget(self):

        # create the title ,description and image path entry
        self.titleEdit = QLineEdit()
        self.titleEdit.resize(250, 40)
        self.titleEdit.setObjectName("titleEdit")
        self.titleEdit.setFont(QFont("verdana", 13))
        self.titleEdit.setTextMargins(10, 5, 10, 5)

        self.descriptionEdit = QTextEdit()
        self.descriptionEdit.resize(250, 100)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.descriptionEdit.setFont(QFont('verdana', 12))

        self.checkImage = QCheckBox("use Default Image")
        self.checkImage.setObjectName("defaultImageCheckBox")
        self.checkImage.setChecked(True)
        self.checkImage.stateChanged.connect(self.setButtonState)

        self.imageDirEdit = QLineEdit()
        self.imageDirEdit.resize(150, 70)
        self.imageDirEdit.setObjectName("imageDirEdit")
        self.imageDirEdit.setReadOnly(True)

        # crate the image choose button
        self.imageChooseButton = QPushButton("Choose")
        self.imageChooseButton.setFixedSize(QSize(100, 40))
        self.imageChooseButton.setEnabled(False)
        self.imageChooseButton.pressed.connect(self.chooseImagePath)

        # create the h box for pack the image items
        hBox = QHBoxLayout()
        hBox.addWidget(self.imageDirEdit)
        hBox.addWidget(self.imageChooseButton)

        # create the button box
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # create the form layout
        form_lyt = QFormLayout()
        form_lyt.addRow("Title", self.titleEdit)
        form_lyt.addRow("Description", self.descriptionEdit)
        form_lyt.addWidget(self.checkImage)
        form_lyt.addRow("Image", hBox)
        form_lyt.addWidget(buttonBox)

        self.setLayout(form_lyt)

    def setButtonState(self, state):

        if state:
            self.imageChooseButton.setEnabled(False)
        else:
            self.imageChooseButton.setEnabled(True)


    def chooseImagePath(self):

        file_path , ok = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG files(*.png) ;; JPEG Files(*.jpg)")

        if ok:
            self.imageDirEdit.setText(file_path)

    def accept(self) -> None:

        # check of the all of required filed is complete
        if (self.titleEdit.text() != ""):
            if (self.checkImage.isChecked()):
                # create the dictionary
                self.info_dict = {
                            "title" : self.titleEdit.text(),
                            "description" : self.descriptionEdit.toPlainText(),
                            "image_dir" : self.default_image
                }

            else:
                if (self.imageDirEdit.text() != ""):
                    # copy the image to images folder
                    new_dir = os.path.join("images", os.path.split(self.imageDirEdit.text())[1])
                    shutil.copyfile(self.imageDirEdit.text() , new_dir)
                    self.info_dict = {
                            "title" : self.titleEdit.text(),
                            "description" : self.descriptionEdit.toPlainText(),
                            "image_dir" : new_dir
                    }


        super().accept()

if __name__ == "__main__":
    app = QApplication([])
    window = newCollectionDialog(None)
    app.exec_()