# Form implementation generated from reading ui file '.\ui\关于软件.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import requests
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget


class Ui_Form(QWidget):

    def __init__(self):
        super(Ui_Form, self).__init__()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(200, 20, 100, 40))
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(parent=Form)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(40, 60, 431, 121))
        self.textBrowser.setObjectName("textBrowser")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(150, 190, 200, 200))
        self.label_2.setText("")
        # self.label_2.setPixmap(QtGui.QPixmap(".\\ui\\f7d077c6d349c220f4293dac4c02799.jpg"))
        # 改为从网络地址加载图片
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        # 禁用窗体放大缩小
        Form.setFixedSize(500, 400)
        # 禁用窗体最大化
        Form.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        # 增加窗体永久置顶
        Form.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        # 禁用窗体最小化
        Form.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "关于软件"))