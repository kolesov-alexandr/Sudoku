import Leaders

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.leadersButton.clicked.connect(self.leaders)

    def initUI(self, args):
        self.previous = args[0]
        self.difficulty = args[1]
        self.number = args[2]
        self.resize(600, 470)
        self.setWindowTitle("Поздравляем!")
        self.setWindowModality(Qt.ApplicationModal)
        self.imageLabel = QLabel("", self)
        self.imageLabel.setPixmap(QPixmap("images/winner.jpg"))
        self.leadersButton = QPushButton("Перейти к таблице лидеров", self)
        self.leadersButton.setFont(QFont("MS Shell Dlg 2", 10))
        self.leadersButton.move(10, 430)

    def leaders(self):
        self.leaders_window = Leaders.MyWidget(self, self.difficulty, self.number)
        self.leaders_window.show()

    def closeEvent(self, event):
        self.previous.close()
