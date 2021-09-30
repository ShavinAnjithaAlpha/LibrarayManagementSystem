import os, sys, json, sqlite3
import time

from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QPushButton, QRadioButton, QTextEdit, QCheckBox, QGridLayout, QScrollArea)
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtGui import QColor, QFont, QPixmap
from style_sheet import dark_theme_for_task

class TaskAndReminderOpen(QWidget):
    def __init__(self):
        super(TaskAndReminderOpen, self).__init__()
        self.setFixedSize(QSize(300, 50))

        # create the h box for pack the widgets
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        # create the task widget
        self.taskWidget  = taskWidget(self)

        newTaskButton = QPushButton("New Task")
        newTaskButton.pressed.connect(self.taskWidget.addTask)
        newTaskButton.setObjectName("navButton")

        newReminderButton = QPushButton("New Reminder")
        newReminderButton.pressed.connect(self.taskWidget.addReminder)
        newReminderButton.setObjectName("navButton")

        openButton = QPushButton(">")
        openButton.pressed.connect(self.openView)
        openButton.setObjectName("openButton")

        hbox.addWidget(newReminderButton)
        hbox.addWidget(newTaskButton)
        hbox.addWidget(openButton)

        self.setLayout(hbox)
        self.setStyleSheet(dark_theme_for_task)

    def openView(self):

        if self.taskWidget.isHidden():
            self.taskWidget.show()
        else:
            self.taskWidget.hide()

    def closeEvent(self, event) -> None:
        self.taskWidget.deleteLater()
        self.close()

class taskWidget(QWidget):
    def __init__(self, parent  = None):
        super(taskWidget, self).__init__()
        #self.left = left
        self.parent = parent
        self.initializeUI()
        self.setStyleSheet(dark_theme_for_task)

    def initializeUI(self):

        # set the main settings
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("mainWidget")
        #self.setGeometry(QRect(self.parent.mapToGlobal(self.parent.rect().bottomLeft()), QSize(400, 800)))
        self.setGeometry(QRect(self.parent.mapToParent(self.parent.rect().bottomLeft()), QSize(550, 500)))
        self.setMaximumHeight(600)
        #self.setFixedWidth(400)
        #self.setFixedHeight(800)

        # create the title labels
        imageLabel = QLabel("Hi Shavin Anjitha")
        imageLabel.setObjectName("imageLabel")
        imageLabel.setFont(QFont('Hack', 35))
        imageLabel.setFixedSize(QSize(self.width(), 300))
        imageLabel.setContentsMargins(0, 0, 0, 0)
        # imageLabel.setPixmap(QPixmap("images/sys_images/taskProfile.jpg").scaled(imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # create the two scroll area for task and reminders
        remindersScrollArea = QScrollArea()
        remindersScrollArea.setWidgetResizable(True)
        remindersScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        remindersScrollArea.setContentsMargins(0, 0, 0, 0)
        remindersScrollArea.setMinimumHeight(200)

        taskScrollArea = QScrollArea()
        taskScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        taskScrollArea.setWidgetResizable(True)
        taskScrollArea.setContentsMargins(0, 0, 0, 0)
        taskScrollArea.setMinimumHeight(200)

        # create the task and reminder widgets
        self.taskWidget = QWidget()
        self.taskWidget.setContentsMargins(0, 0, 0, 0)
        self.taskWidget.setObjectName("taskWidget")

        self.reminderWidget = QWidget()
        self.reminderWidget.setContentsMargins(15, 15, 15, 15)
        self.reminderWidget.setObjectName("reminderWidget")

        # create the layout and set the scroll bar widgets
        remindersScrollArea.setWidget(self.reminderWidget)
        taskScrollArea.setWidget(self.taskWidget)

        vbox = QVBoxLayout()
        vbox.addWidget(imageLabel)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        # setup the widgets
        self.setUpTaskWidget()
        self.setUpReminderWidget()

        vbox.addWidget(remindersScrollArea)
        vbox.addWidget(taskScrollArea)
        self.setLayout(vbox)



    def setUpTaskWidget(self):

        # create the grid view for this
        self.taskGrid = QVBoxLayout()
        self.taskGrid.setSpacing(10)
        self.taskGrid.setContentsMargins(0, 0, 0, 0)
        self.taskGrid.addWidget(QLabel())
        self.taskGrid.addStretch()

        # load the tasks from the
        self.loadTasks()

        if self.tasks_data != []:
            for task in self.tasks_data:
                radio = QRadioButton(task)
                radio.setObjectName("radioButton")
                radio.pressed.connect(lambda e = radio : self.completeTask(e))
                self.taskGrid.insertWidget(0, radio)
        else:
            self.noneLabel2 = QLabel("No Task Yet")
            self.noneLabel2.setContentsMargins(100, 100, 100, 100)
            self.taskGrid.insertWidget(0, self.noneLabel2)

        self.taskWidget.setLayout(self.taskGrid)

    def completeTask(self, radio : QRadioButton):

        data = []
        with open("db/task.json") as file:
            data = json.load(file)
        data.remove(radio.text())

        with open("db/task.json", "w") as file:
            json.dump(data, file, indent=4)

        # delete the radion button
        radio.setChecked(True)
        time.sleep(0.5)
        radio.deleteLater()

    def addTask(self):

        if (self.isHidden()):
            self.show()
        try:
            self.noneLabel2.deleteLater()
        except:
            pass

        self.taskEdit = QLineEdit()
        self.taskEdit.setObjectName("newEdit")
        self.taskEdit.resize(200, 40)
        self.taskEdit.setTextMargins(10, 10, 10, 10)
        self.taskEdit.setFocus()
        self.taskEdit.returnPressed.connect(self.saveTask)

        self.taskGrid.insertWidget(0, self.taskEdit)

    def saveTask(self):

        text = self.taskEdit.text()

        if os.path.exists("db/task.json"):
            data = []
            with open("db/task.json") as file:
                data = json.load(file)

            data.append(text)
            with open("db/task.json", "w") as file:
                json.dump(data, file, indent=4)

        else:
            data = [text, ]
            with open("db/task.json", "w") as file:
                json.dump(data, file, indent=4)

        # create the new label
        label = QRadioButton(text)
        label.setObjectName("radioButton")

        self.taskEdit.deleteLater()
        self.taskGrid.insertWidget(0, label)

    def setUpReminderWidget(self):

        # create the clear button
        claerButton = QPushButton("Clear")
        claerButton.pressed.connect(self.clearReminders)

        # create the grid layout for this
        self.reminderGrid = QVBoxLayout()
        self.reminderGrid.setSpacing(20)
        self.reminderGrid.setContentsMargins(0, 0, 0, 0)
        self.reminderGrid.addWidget(QLabel())
        self.reminderGrid.addStretch()
        self.reminderGrid.addWidget(claerButton, alignment=Qt.AlignRight)

        # load the reminders
        self.loadReminders()

        if self.reminder_data != []:
            for reminder in self.reminder_data:
                label_new = QLabel(reminder)
                label_new.setObjectName("reminderLabel")
                #label_new.setPixmap(QPixmap("images/sys_images/fillStar.png").scaled(QSize(40, 40), Qt.KeepAspectRatio, Qt.FastTransformation))
                self.reminderGrid.insertWidget(0, label_new)
        else:
            self.noneLabel = QLabel("Nothing to Preview")
            self.noneLabel.setContentsMargins(100, 100, 100, 100)
            self.reminderGrid.insertWidget(0, self.noneLabel)

        self.reminderWidget.setLayout(self.reminderGrid)

    def addReminder(self):

        if (self.isHidden()):
            self.show()

        # show the line edit for user
        self.reminderEdit  = QLineEdit()
        self.reminderEdit.setObjectName("newEdit")
        self.reminderEdit.resize(200, 40)
        self.reminderEdit.setTextMargins(10, 10, 10, 10)
        self.reminderEdit.returnPressed.connect(self.saveReminder)

        self.reminderGrid.insertWidget(0, self.reminderEdit)

    def saveReminder(self):

        try:
            self.noneLabel.deleteLater()
        except:
            pass

        text = self.reminderEdit.text()

        if os.path.exists("db/reminder.json"):
            data = []
            with open("db/reminder.json") as file:
                data = json.load(file)

            data.append(text)
            with open("db/reminder.json", "w") as file:
                json.dump(data, file, indent=4)

        else:
            data = [text, ]
            with open("db/reminder.json", "w") as file:
                json.dump(data, file, indent=4)

        # create the new label
        label = QLabel(text)
        label.setObjectName("reminderLabel")
        #label.setPixmap(QPixmap("images/sys_images/fillStar.png").scaled(QSize(40, 40), Qt.KeepAspectRatio, Qt.FastTransformation))
        self.reminderEdit.deleteLater()
        self.reminderGrid.insertWidget(0, label)

    def clearReminders(self):

        with open("db/reminder.json", "w") as file:
            json.dump([], file, indent=4)

        for i in range(self.reminderGrid.count()):
            self.reminderGrid.itemAt(i).deleteLater()

    def loadTasks(self):

        if os.path.exists("db/task.json"):
            # load the tasks
            self.tasks_data = []
            with open("db/task.json") as file:
                self.tasks_data = json.load(file)
        else:
            self.tasks_data = []


    def loadReminders(self):

        if os.path.exists("db/reminder.json"):
            # load the tasks
            self.reminder_data = []
            with open("db/reminder.json") as file:
                self.reminder_data = json.load(file)
        else:
            self.reminder_data = []


if __name__ == "__main__":
    app = QApplication([])
    window = TaskAndReminderOpen()
    window.show()

    app.exec_()