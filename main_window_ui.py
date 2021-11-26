# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(220, 180, 371, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.gameLabel.setFont(font)
        self.gameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.gameLabel.setObjectName("gameLabel")
        self.verticalLayout.addWidget(self.gameLabel)
        self.newGameButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.newGameButton.setFont(font)
        self.newGameButton.setObjectName("newGameButton")
        self.verticalLayout.addWidget(self.newGameButton)
        self.continueGameButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.continueGameButton.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.continueGameButton.setFont(font)
        self.continueGameButton.setObjectName("continueGameButton")
        self.verticalLayout.addWidget(self.continueGameButton)
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(10, 10, 321, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameLabel.setFont(font)
        self.nameLabel.setText("")
        self.nameLabel.setObjectName("nameLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.accountMenu = QtWidgets.QMenu(self.menubar)
        self.accountMenu.setObjectName("accountMenu")
        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu.setObjectName("helpMenu")
        MainWindow.setMenuBar(self.menubar)
        self.changePasswordAction = QtWidgets.QAction(MainWindow)
        self.changePasswordAction.setObjectName("changePasswordAction")
        self.quitAccountAction = QtWidgets.QAction(MainWindow)
        self.quitAccountAction.setObjectName("quitAccountAction")
        self.deleteAccountAction = QtWidgets.QAction(MainWindow)
        self.deleteAccountAction.setObjectName("deleteAccountAction")
        self.helpAction = QtWidgets.QAction(MainWindow)
        self.helpAction.setObjectName("helpAction")
        self.accountMenu.addAction(self.changePasswordAction)
        self.accountMenu.addAction(self.quitAccountAction)
        self.accountMenu.addAction(self.deleteAccountAction)
        self.helpMenu.addAction(self.helpAction)
        self.menubar.addAction(self.accountMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Судоку"))
        self.gameLabel.setText(_translate("MainWindow", "СУДОКУ"))
        self.newGameButton.setText(_translate("MainWindow", "Новая игра"))
        self.continueGameButton.setText(_translate("MainWindow", "Продолжить игру"))
        self.accountMenu.setTitle(_translate("MainWindow", "Аккаунт"))
        self.helpMenu.setTitle(_translate("MainWindow", "О программе"))
        self.changePasswordAction.setText(_translate("MainWindow", "Изменить пароль"))
        self.changePasswordAction.setShortcut(_translate("MainWindow", "Ctrl+Shift+Q"))
        self.quitAccountAction.setText(_translate("MainWindow", "Выйти из аккаунта"))
        self.quitAccountAction.setShortcut(_translate("MainWindow", "Ctrl+Shift+X"))
        self.deleteAccountAction.setText(_translate("MainWindow", "Удалить аккаунт"))
        self.deleteAccountAction.setShortcut(_translate("MainWindow", "Ctrl+Shift+Del"))
        self.helpAction.setText(_translate("MainWindow", "О программе"))
        self.helpAction.setShortcut(_translate("MainWindow", "Shift+F1"))
