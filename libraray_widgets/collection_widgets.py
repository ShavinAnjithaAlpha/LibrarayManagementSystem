import json, sqlite3, os, shutil
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QMenu ,QAction, QVBoxLayout, QGridLayout,
                             QFileDialog, QMessageBox, QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QRectF
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter, QColor, QPen, QKeyEvent
# import the styles
from style_sheet import dark_style_sheet_for_Collection

db_file = "db/data.db"
favorite_file = "db/favorite.json"
collection_file = "db/collection.json"
collection_track_file = "db/collection_tracking.json"
book_file = "db/book.json"


class collectionWidget(QWidget):

    # defined the new signal for change the favorite widgets of the model
    favoriteSignal = pyqtSignal(list)
    statusSignal = pyqtSignal(str)

    def __init__(self, title, description, image_dir, path, pw, id):
        super(collectionWidget, self).__init__()
        self.title = title
        self.description = description
        self.image_dir = image_dir
        self.path = path
        self.collection_id = id
        self.pw = pw


        self.setStatusTip(f"Collection : {title}")
        self.setUpToolTip()

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
        self.imageLabel.setFixedSize(QSize(180, 170))
        self.imageLabel.setPixmap(
            QPixmap(self.image_dir).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

        # create the favorite button
        self.addFavoriteButton = QPushButton()
        self.addFavoriteButton.setObjectName("favoriteButton")
        self.addFavoriteButton.setIconSize(QSize(30, 30))
        self.addFavoriteButton.clicked.connect(self.changeFavoriteState)
        self.addFavoriteButton.setCheckable(True)
        self.setState()

        # create the loack button
        self.lockbutton  = QLabel()
        if self.pw != "":
            self.lockbutton.setPixmap(QPixmap("images/sys_images/lock.png").scaled(QSize(25, 25), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # create the button create the role
        self.roleButton = QPushButton(">")
        self.hideButton = QPushButton("<")

        # create the menu button
        self.menuButton = QPushButton()
        self.menuButton.setObjectName("menuButton")

        self.setUpMenu()

    def setUpMenu(self):

        # create the menu
        self.menu = QMenu(self)

        # create the action
        self.changeTitleAction = QAction("Change Title", self)
        self.changeTitleAction.triggered.connect(self.changeTitle)
        self.changeTitleAction.setToolTip("Change the Collection title you want")
        self.changeTitleAction.setIcon(QIcon("images/sys_images/renameIcon2.png"))

        self.changeDesAction = QAction("Change Description", self)
        self.changeDesAction.triggered.connect(self.changeDescription)
        self.changeDesAction.setToolTip("Change the Collection Description you want")
        self.changeDesAction.setIcon(QIcon("images/sys_images/changeDesIcon2.png"))

        self.changeImageAction = QAction("Change Cover Image", self)
        self.changeImageAction.triggered.connect(self.changeImage)
        self.changeImageAction.setToolTip("Change the Collection Cover Image you want")
        self.changeImageAction.setIcon(QIcon("images/sys_images/imageIcon.png"))

        self.changePasswordAction = QAction("Change Password", self)
        self.changePasswordAction.setToolTip("Change the collection passowrd or enter the new password")
        self.changePasswordAction.triggered.connect(self.changePassword)
        self.changePasswordAction.setIcon(QIcon("images/sys_images/lockIcon.png"))

        self.statusAction = QAction("Infomations", self)
        self.statusAction.triggered.connect(self.fireStatus)
        self.statusAction.setToolTip("More About the Collection")
        self.statusAction.setIcon(QIcon("images/sys_images/infoIcon.png"))

        # create the delete action
        self.deleteActon = QAction("Delete", self)
        self.deleteActon.setToolTip("Delete the all of the data about the collection")
        self.deleteActon.triggered.connect(self.delete)

        # add to the menu
        self.menu.addAction(self.changeTitleAction)
        self.menu.addAction(self.changeDesAction)
        self.menu.addAction(self.changeImageAction)
        self.menu.addAction(self.changePasswordAction)
        self.menu.addSeparator()
        self.menu.addAction(self.deleteActon)
        self.menu.addAction(self.statusAction)

        self.menuButton.setMenu(self.menu)

    def keyPressEvent(self, event : QKeyEvent) -> None:

        if event.key() == Qt.Key_Delete:
            self.delete()

    def fireStatus(self):

        self.statusSignal.emit(self.collection_id)

    def changePassword(self):

        check = False
        subCheck = False
        # get the new password from the text box
        if self.pw != "":
            # reconfirm the password
            pw , ok = QInputDialog.getText(self, "Password Prompt", "Enter the Password : ", echo=QLineEdit.Password)
            if ok and pw == self.pw:
                subCheck = True
            else:
                QMessageBox.warning(self, "Warning", "Password You Entered is Wrong! Please Enter Correct Password")

        else:
            subCheck = True

        # get the new pw from the user
        if subCheck:
            # get the new pw from the user
            new_pw, ok2 = QInputDialog.getText(self, "New Password Dialog", "Enter the New Password : ", echo=QLineEdit.Password)
            if ok2:
                # confirm the password from the user
                confirm_pw, ok3 = QInputDialog.getText(self, "Confirm Password Dialog", "Confirm the Password : ", echo=QLineEdit.Password)
                if ok3 and confirm_pw == new_pw:
                    check = True
                else:
                    QMessageBox.warning(self, "Warning", "Confirm Password is not correct...Please Enter the Correct Password")


        if check:
            # change the password from the data base and current widget
            self.pw = new_pw
            # create the connection to the data base
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()

            cursor.execute(
                f" UPDATE collection_table SET pw = '{self.pw}' WHERE collection_id = '{self.collection_id}'  ")
            # save the changes
            connection.commit()
            connection.close()

    def changeImage(self):

        # open the file dialog and change the image dir
        file, ok = QFileDialog.getOpenFileName(self, "Open the Cover Image", "", "JPG Files(*.jpg);; PNG Files(*.png)")
        if ok:

            # change the image dir to relative path
            new_path = os.path.join("images", os.path.split(file)[1])
            shutil.copyfile(file ,new_path)

            # save the changes
            user_data = {}
            with open(collection_file, "r") as file:
                user_data = json.load(file)

            user_data.get(self.collection_id)["image_dir"] = new_path

            with open(collection_file, "w") as file:
                json.dump(user_data, file, indent=4)

            # change the image
            self.imageLabel.setPixmap(QPixmap(new_path).scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.FastTransformation))
            self.image_dir = new_path

    def changeTitle(self):

        text, ok = QInputDialog.getText(self, "Title Changed Dialog", "Enter the new title : ")

        if ok:
            # change the data base file title
            user_data = {}
            with open(collection_file) as file:
                user_data = json.load(file)

            user_data.get(self.collection_id)['title'] = text
            with open(collection_file, "w") as file:
                json.dump(user_data, file, indent=4)

            # change the favorites json file
            with open(favorite_file) as file:
                user_data = json.load(file)

            for item in user_data:
                if item["id"] == self.collection_id and item['type'] == "collection":
                    item["title"] = text

            with open(favorite_file, "w") as file:
                json.dump(user_data, file, indent=4)
            # end of the update the json files


            # update the database file
            connection = sqlite3.connect(db_file)
            cursor = connection.cursor()

            cursor.execute(f"UPDATE collection_table SET name = '{text}' WHERE collection_id = '{self.collection_id}'  ")
            connection.commit()

            # close the connection
            connection.close()

            # change the widget title
            self.titleLabel.setText(text)
            self.title = text

    def changeDescription(self):

        # prompt the text dialog for get the new description
        text, ok = QInputDialog.getMultiLineText(self, "New Description Dialog", "Description : ", text=self.description)
        if ok:
            # change the collection json file
            user_data = {}
            with open(collection_file, "r") as file:
                user_data = json.load(file)

            # find the code and change the description
            user_data.get(self.collection_id)["description"] = text
            # save the changes
            with open(collection_file, "w") as file:
                json.dump(user_data, file, indent=4)

            # change hte curren widget description
            self.descriptionLabel.setText(text)
            self.description = text

    def setIcon(self):

        if self.addFavoriteButton.isChecked():
            self.addFavoriteButton.setIcon(QIcon("images/sys_images/fillStar.png"))
        else:
            self.addFavoriteButton.setIcon(QIcon("images/sys_images/nonFillStar.png"))

    def setState(self):

        # open th json file
        user_data = []
        with open(favorite_file, "r") as file:
            user_data =json.load(file)

        for item in user_data:
            if item["path"]  == self.path and item["type"] == "collection":
                self.addFavoriteButton.setChecked(True)
                self.addFavoriteButton.setIcon(QIcon("images/sys_images/fillStar.png"))
                return None
        self.addFavoriteButton.setChecked(False)
        self.addFavoriteButton.setIcon(QIcon("images/sys_images/nonFillStar.png"))

    def changeFavoriteState(self, state):

        # get the id for this
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute(f""" SELECT collection_id FROM collection_table WHERE path = '{self.path}' """)
        data = cursor.fetchall()

        id = data[0][0]
        connection.close()

        # add to the favorite
        # open the json file
        user_data = []
        with open(favorite_file, "r") as file:
            user_data = json.load(file)

        if state:

            user_data.append({
                "type" : "collection",
                "id" : id,
                "title" : self.title,
                "path" : self.path
            })

            # fire hte favorite signal
            self.favoriteSignal.emit([self.title, self.path, id, True, "collection"])

        else:
            # select the correct item and clear it
            for item in user_data:
                if item["path"] == self.path:
                    user_data.remove(item)
            # fire the signal
            self.favoriteSignal.emit([self.title, self.path, id, False, "collection"])

        # save the updated user_data
        with open(favorite_file, "w") as file:
            json.dump(user_data, file, indent=4)
        self.setIcon()

    def delete(self):

        check = True
        if self.pw != "":
            text, ok = QInputDialog.getText(self, "Password Dialog", "Type the Password : ", echo=QLineEdit.Password)
            if ok:
                if text != self.pw:
                    check = False
                    QMessageBox.warning(self, 'Password warning', "Wrong Password , Please Try again!")
            else:
                check = False

        message = QMessageBox.StandardButton.No
        if check:
            message = QMessageBox.warning(self, "Delete Message", f"Are you sure to Delete Collection {self.title} ?",
                                                        QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)

        if message == QMessageBox.StandardButton.Yes:
            # remove the data from the data base and all of the json files
            connect = sqlite3.connect(db_file)
            cursor = connect.cursor()

            cursor.execute(f"DELETE FROM collection_table WHERE collection_id = '{self.collection_id}' ")

            # remove the all of the book from the book table
            cursor.execute("SELECT path, book_id FROM book_table " )
            books = cursor.fetchall()

            with open(book_file) as file:
                book_data = json.load(file)

            removed_books = [i[1] for i in books if i[0].startswith(self.path)]
            for i in removed_books:
                try:
                    cursor.execute(f"DELETE FROM book_table WHERE book_id = '{i}' ")
                    book_data.pop(i)
                except:
                    pass

            with open(book_file, 'w') as file:
                json.dump(book_data, file, indent=4)

            connect.commit()
            connect.close()
            del book_data
            del removed_books
            del books

            # remove the colelction json file info
            coll_data  : dict = {}
            with open(collection_file) as file:
                coll_data = json.load(file)

            coll_data.pop(self.collection_id)

            with open(collection_file, "w") as file:
                json.dump(coll_data, file, indent=4)
            del coll_data

            # remove from the favorite jsn file
            if self.addFavoriteButton.isChecked():
                # remove from the favorite json file
                fav_data = []
                with open(favorite_file) as file:
                    fav_data = json.load(file)

                for i in fav_data:
                    if i['type'] == 'collection' and i['id'] == self.collection_id:
                        fav_data.remove(i)
                        break
                with open(favorite_file, 'w') as file:
                    json.dump(fav_data, file, indent=4)


            # finally delete the widget
            self.deleteLater()
            print("[INFO] successfully delete the collection...")

    def setUpToolTip(self):

        # calculate the data
        connect = sqlite3.connect(db_file)
        cursor = connect.cursor()

        cursor.execute(f"SELECT path FROM collection_table")
        data = [item[0] for item in cursor.fetchall()]

        cursor.execute(f"SELECT path FROM book_table")
        book_data = [item[0] for item in cursor.fetchall()]

        connect.close()

        total1 = 0
        total2 = 0
        for i in data:
            if i.startswith(self.path):
                total2 += 1
                if (len(i.split("/")) - len(i.split(self.path)) == 1):
                    total1 += 1

        total3 = 0
        total4 = 0
        for i in book_data:
            if i.startswith(self.path):
                total4 += 1
                if (len(i.split("/")) - len(i.split(self.path)) == 1):
                    total3 += 1

        self.setToolTip(f"""Collections : <font color = 'blue'>{total1}</font>
                            \nTotal Collections : <font color = 'blue'> {total2}</font>
                            \nBooks : <font color = 'blue' >{total3}</font>
                            \nTotal Books : <font color = 'blue' >{total4}</font>""")


class boxCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path, pw ,id):
        super(boxCollectionWidget, self).__init__(title, description, image_dir, path, pw, id)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(700, 400))

        # set the word wrap option to title label
        self.titleLabel.setWordWrap(True)
        # create the grid layout for pack the items
        self.gridLyt  = QGridLayout()

        self.gridLyt.addWidget(self.titleLabel, 0, 0, 1, 2)
        self.gridLyt.addWidget(self.imageLabel, 1, 0, 1, 1)
        self.gridLyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)
        self.gridLyt.addWidget(self.addFavoriteButton, 0, 3)
        self.gridLyt.addWidget(self.menuButton, 0, 2)
        self.gridLyt.addWidget(self.lockbutton, 1, 3)



        self.baseWidget.setLayout(self.gridLyt)


class listCollectionWidget(collectionWidget):
    def __init__(self, title, description, image_dir, path, pw, id):
        super(listCollectionWidget, self).__init__(title, description, image_dir, path, pw, id)
        self.initializeUI()

    def initializeUI(self):

        self.setMinimumHeight(150)
        #self.setMaximumHeight(220)

        self.titleLabel.setFont(QFont("verdana", 22))

        # create the grid lyt for pack items
        self.grid_lyt = QGridLayout()
        self.grid_lyt.addWidget(self.titleLabel, 0, 1, 1, 1)
        self.grid_lyt.addWidget(self.imageLabel, 0, 0, 2, 1)
        self.grid_lyt.addWidget(self.descriptionLabel, 1, 1, 1, 1)
        self.grid_lyt.addWidget(self.addFavoriteButton, 0, 3)
        self.grid_lyt.addWidget(self.menuButton, 0, 2)
        self.grid_lyt.addWidget(self.lockbutton, 1, 3)
        self.grid_lyt.addWidget(self.roleButton, 0, 4)
        self.grid_lyt.addWidget(self.hideButton, 0, 4)

        self.hideButton.hide()

        self.roleButton.pressed.connect(self.openRole)
        self.hideButton.pressed.connect(self.removeRole)



        self.roleButton.setObjectName("collection_role_button")
        self.hideButton.setObjectName("collection_role_button")

        # create the vbox
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.grid_lyt)

        self.baseWidget.setLayout(self.vbox)

    def openRole(self):
        # create the new collectionRole object
        self.role = CollectionRoll(self.collection_id)
        self.vbox.addWidget(self.role)
        self.vbox.addStretch(1)

        self.hideButton.show()
        self.roleButton.hide()

    def removeRole(self):
        self.role.deleteLater()
        self.roleButton.show()
        self.hideButton.hide()



class CollectionRoll(QWidget):
    def __init__(self, collection_code: str):
        super(CollectionRoll, self).__init__()
        self.collection_id = collection_code

        self.data = []
        self.n = 0
        self.t = 50

        self.l = 50
        self.color = [QColor(0, 70, 130), QColor(0, 50, 100)]

        self.loadData()
        self.initializeUI()

    def loadData(self):

        # load the data base datas
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute(f" SELECT path, name FROM collection_table ")
        data = cursor.fetchall()

        cursor.execute(f" SELECT path FROM collection_table WHERE collection_id = '{self.collection_id}' ")
        main_path = cursor.fetchall()[0][0]

        connection.close()


        # filter the data
        filter_data = []

        for item in data:
            if item[0].startswith(main_path) and (len(item[0].split("/")) - len(main_path.split("/"))) == 1:
                filter_data.append(item[1])

        self.data = filter_data
        self.n = len(self.data)

    def initializeUI(self):

        self.setMinimumHeight(self.t * self.n)

    def paintEvent(self, event):

       # crete the painter object
        painter = QPainter(self)

        # defined the widget drawing parameters
        width = painter.device().width()
        height = painter.device().height()

        try:
            t = self.t

            painter.setFont(QFont('verdana', 14))
            # create the collection box
            for i in range(0, self.n):
                painter.setPen(QColor(0, 0, 0))
                painter.setBrush(self.color[i%2])
                painter.drawRect(0, i * t, self.l, t)

                painter.setPen(QPen(QColor(255, 255, 255), 1))
                painter.drawText(QRectF(0, i * t, self.l, t), Qt.AlignCenter, f"{i+1}")

                painter.setPen(QColor(0, 0, 0))
                painter.drawRect(self.l, i * t, (width - self.l), t)
                painter.setPen(QPen(QColor(255, 255, 255), 1))
                painter.drawText(QRectF(self.l + 10, i * t, (width - self.l), t), Qt.AlignVCenter, self.data[i])

        except:
            pass

        painter.end()