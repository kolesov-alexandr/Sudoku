# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start_window_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        Form.resize(644, 391)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(180, 100, 281, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logInButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.logInButton.setFont(font)
        self.logInButton.setObjectName("logInButton")
        self.verticalLayout.addWidget(self.logInButton)
        self.registrationButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.registrationButton.setFont(font)
        self.registrationButton.setObjectName("registrationButton")
        self.verticalLayout.addWidget(self.registrationButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Судоку"))
        self.logInButton.setText(_translate("Form", "ВХОД"))
        self.registrationButton.setText(_translate("Form", "РЕГИСТРАЦИЯ"))
