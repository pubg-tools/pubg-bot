# Form implementation generated from reading ui file '.\ui\main.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


import datetime
import json
import logging
import os
import sys
import threading

import requests
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMainWindow

# from gameloop import gameLoop
# 引入 上层文件夹的 gameloop.py 中的 gameloop类
from gameloop import gameloop
from template.tips import Ui_Form
from template.updatelog import Up_data_log

# 生成 ..\config\config.json 文件的绝对路径
configPath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../config/config.json")
)

# 构建 config.json 的正确路径
print("configPath:", configPath)

# 读取 ../config/config.json 文件 并将变量赋值给 config
globGameloop = gameloop()
# 定义一个旧的窗体文案值
oldText = ""
oldText2 = ""

try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class ChineseLogger:
    def __init__(self, log_name, log_dir="./logs", log_level=logging.INFO):
        self.log_name = log_name
        self.log_dir = log_dir
        self.log_level = log_level
        self._setup_logging()

    def _setup_logging(self):
        # 创建日志目录
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f"{str(dt)}-{str(self.log_name)}.log"
        print(file_name)
        # 日志文件路径
        self.log_file = os.path.join(self.log_dir, file_name)

        # 创建一个logger
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(self.log_level)

        # 创建一个handler，用于写入日志文件
        file_handler = logging.FileHandler(self.log_file, "a", encoding="utf-8")
        file_handler.setLevel(self.log_level)

        # 创建一个formatter，用于设置日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # 为logger添加handler
        self.logger.addHandler(file_handler)
        file_handler.setFormatter(formatter)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self._setup_logging()
        print("info:", self.log_dir)
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def setLog_dir(self, log_dir):
        self.log_dir = log_dir


class WorkerThread(QThread):
    finished_signal = pyqtSignal(str)
    # 第二个插槽
    finished_signal_loop = pyqtSignal(str)

    def run(self, timeout=5, flaytimeout=30, imgopcv=8, saveLog=True):
        self.gameloop = globGameloop
        self.gameloop.setCllback(self.callback)
        self.gameloop.setCllback2(self.callback2)
        # 创建子线程 执行 gameLoop 方法
        self.threadItem = threading.Thread(
            target=self.gameloop.gameLoop,
            args=(timeout, flaytimeout, imgopcv * 0.1, saveLog),
        )
        self.threadItem.start()

    def callback(self, message):
        self.finished_signal.emit(message)

    def callback2(self, message):
        self.finished_signal_loop.emit(message)


class Ui_mainWindow(QMainWindow):
    def __init__(self, parent=None):
        print("进入构造方法")
        super(Ui_mainWindow, self).__init__(parent=parent)
        # pubg 状态
        self.pubgState = False
        # steam 状态
        self.steamState = False

        self.gameloop = globGameloop
        # 实例化 WorkerThread
        self.worker_thread = WorkerThread()
        # 绑定 finished_signal 信号到 showLogs 方法
        self.worker_thread.finished_signal.connect(self.setStateHooks)
        # 绑定 finished_signal_loop 信号到 showLogs 方法
        self.worker_thread.finished_signal_loop.connect(self.setStateHooks2)
        # 实例化日志模块
        self.logger = None
        self.setupUi(self)

    def setupUi(self, mainWindow):
        # 获取 ../images/avatar/head.ico 的绝对路径变量
        self.iconPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../images/avatar/head.ico")
        )
        # 获取 ../images/avatar/steam.png" 的绝对路径变量
        self.steamPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../images/avatar/steam.png")
        )
        # 获取 ../images/avatar/pubg.png" 的绝对路径变量
        self.pubgPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../images/avatar/pubg.png")
        )
        # 获取 ../images/avatar/tips.png" 的绝对路径变量
        self.tipsPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../images/avatar/tips.png")
        )
        # 获取 ../images/avatar/steam_act.png" 的绝对路径变量
        self.steamActPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../images/avatar/steam_act.png")
        )
        # 获取 ../images/avatar/pubg_act.png" 的绝对路径变量
        self.pubgActPath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../images/avatar/pubg_act.png")
        )
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(756, 267)
        font = QtGui.QFont()
        font.setPointSize(9)
        mainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(self.iconPath), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off
        )
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 171, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(20, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 40, 40))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(self.steamPath))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(68, 58, 44, 44))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(self.pubgPath))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 65, 60, 30))
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 180, 91, 21))
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QtCore.QRect(110, 180, 371, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(490, 180, 75, 20))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_7 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(210, 58, 60, 40))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(290, 58, 211, 40))
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(490, 58, 211, 40))
        self.label_11.setObjectName("label_11")
        # 添加一个label 放置到窗体右下角
        self.label_12 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(700, 210, 171, 21))
        self.label_12.setObjectName("label_12")

        self.formLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(240, 110, 201, 51))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_4.setContentsMargins(20, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_14 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        self.label_14.setObjectName("label_14")
        self.formLayout_4.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_14
        )
        self.label_15 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        self.label_15.setObjectName("label_15")
        self.formLayout_4.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_15
        )
        self.spinBox_5 = QtWidgets.QSpinBox(parent=self.formLayoutWidget_2)
        self.spinBox_5.setObjectName("spinBox_5")
        self.formLayout_4.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_5
        )
        self.checkBox = QtWidgets.QCheckBox(parent=self.formLayoutWidget_2)
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.formLayout_4.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.checkBox
        )

        self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(190, 10, 541, 41))
        self.textBrowser.setEnabled(False)
        self.textBrowser.setObjectName("textBrowser")
        self.formLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 110, 201, 51))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setContentsMargins(20, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3
        )
        self.label_4 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4
        )
        self.spinBox = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox
        )
        self.spinBox_2 = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spinBox_2
        )
        self.label_9 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(210, 110, 20, 20))
        self.label_9.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WhatsThisCursor))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap(self.tipsPath))
        self.label_9.setScaledContents(True)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(210, 140, 20, 20))
        self.label_10.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WhatsThisCursor))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap(self.tipsPath))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 115, 110, 40))
        self.pushButton_3.setObjectName("pushButton_3")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 756, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(parent=self.menubar)
        self.menu.setObjectName("menu")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.action = QtGui.QAction(parent=mainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(parent=mainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtGui.QAction(parent=mainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())

        # 给 comboBox_2 添加两个选项 简体中文 和繁体中文 默认选择简体中文
        self.comboBox_2.addItem("简体中文")
        # self.comboBox_2.addItem("繁体中文")
        self.comboBox_2.setCurrentIndex(0)
        # 禁用窗体放大缩小
        mainWindow.setFixedSize(756, 267)
        # 禁用窗体最大化
        mainWindow.setWindowFlag(QtCore.Qt.WindowType.WindowMaximizeButtonHint, False)
        # 增加窗体永久置顶
        mainWindow.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint, True)
        # 禁用窗体最小化
        mainWindow.setWindowFlag(QtCore.Qt.WindowType.WindowMinimizeButtonHint, False)

        # 给 pushButton_2 添加点击事件
        self.pushButton_2.clicked.connect(self.seachLogsPath)
        # 给 日志按钮添加点击事件
        self.action_2.triggered.connect(self.showLogs)
        # 给 更新日志按钮添加点击事件
        self.action_3.triggered.connect(self.openUpdateLog)
        # 给 刷新按钮 添加 checkSteamAndPubg 点击事件
        self.pushButton.clicked.connect(self.checkSteamAndPubg)
        # 给开始挂机按钮 添加点击事件
        self.pushButton_3.clicked.connect(self.startGameLoop)
        # 给 action 添加点击事件
        self.action.triggered.connect(self.openAbout)

        # 设置 label_9 的默认值为 5
        self.spinBox.setValue(5)
        # 设置 label_10 的默认值为 30
        self.spinBox_2.setValue(30)
        # 鼠标放到 label_9 上提示文字
        self.label_9.setToolTip("轮询延迟：每轮状态检查中间隔的时间,单位为秒")
        self.label_9.setStatusTip("轮询延迟：每轮状态检查中间隔的时间,单位为秒")
        # 鼠标放到 label_10 上提示文字
        self.label_10.setToolTip("跳伞延迟：每次上飞机时等待多久跳伞,单位为秒")
        self.label_10.setStatusTip("跳伞延迟：每次上飞机时等待多久跳伞,单位为秒")
        # 默认选中 label_15
        self.checkBox.setChecked(True)
        # 设置 spinBox_5 的默认值为 8
        self.spinBox_5.setValue(8)
        # 设置 spinBox_5 的最大值为 10 最小值为 1
        self.spinBox_5.setMaximum(10)
        self.spinBox_5.setMinimum(1)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        self.initData()

    def retranslateUi(self, mainWindow):
        # 获取配置信息
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("mainWindow", "语 言"))
        self.pushButton.setText(_translate("mainWindow", "刷新"))
        self.label_6.setText(_translate("mainWindow", "日志保存位置:"))
        self.pushButton_2.setText(_translate("mainWindow", "选择文件夹"))
        self.label_7.setText(_translate("mainWindow", "当前状态："))
        self.label_8.setText(_translate("mainWindow", "未开启"))
        self.label_11.setText(_translate("mainWindow", ""))
        # 设置主页文本
        self.label_3.setText(_translate("mainWindow", "轮 询 延 迟："))
        self.label_4.setText(_translate("mainWindow", "跳 伞 延 迟："))
        self.label_14.setText(_translate("mainWindow", "图 片 相 似 度:"))
        self.label_15.setText(_translate("mainWindow", "保 存 日 志:"))
        self.menu.setTitle(_translate("mainWindow", "关于"))
        self.action.setText(_translate("mainWindow", "关于软件"))
        self.action_2.setText(_translate("mainWindow", "日志"))
        self.action_3.setText(_translate("mainWindow", "更新日志"))
        self.pushButton_3.setText(_translate("mainWindow", "开始挂机"))
        self.label_12.setText("V 1.2.0")

    def initData(self):
        # 获取用户桌面path
        path = os.path.join(os.path.expanduser("~"), "Desktop")
        path = os.path.join(path, "logs")
        print("path:", path)
        # 设置日志保存位置
        self.lineEdit.setText(path)
        self.logger = ChineseLogger("PUBG-tools")
        self.logger.setLog_dir(path)
        self.checkSteamAndPubg()

    #     检测是否打开了 steam 和 pubg
    def checkSteamAndPubg(self):
        print("检测是否打开了 steam 和 pubg")
        # 检查是否有  名为 steam.exe 的进程
        if os.system("tasklist | findstr steam.exe") == 0:
            # 如果已经打开 steam 将 label_2 的图片 替换为 steam.png
            self.label_2.setPixmap(QtGui.QPixmap(self.steamActPath))
            self.steamState = True
            self.label_11.setText("已开启 steam")
        else:
            # 将图片替换为 steam.png
            self.label_2.setPixmap(QtGui.QPixmap(self.steamPath))
            # 将 label_7  替换为 未开启 steam
            self.label_11.setText("未开启 steam")
            self.steamState = False
        # 检查是否有  名为 TslGame.exe 的进程
        if os.system("tasklist | findstr TslGame.exe") == 0:
            # 如果已经打开 pubg 将 label_5 的图片 替换为 pubg_act.png
            self.label_5.setPixmap(QtGui.QPixmap(self.pubgActPath))
            self.pubgState = True
            self.label_11.setText("已开启 pubg")
        else:
            # 将图片替换为 pubg.png
            self.label_5.setPixmap(QtGui.QPixmap(self.pubgPath))
            # 将 label_8  替换为 未开启 PUBG
            self.label_11.setText("未开启 PUBG")
            self.pubgState = False
        pass

    # def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
    #     print("关闭窗口")
    #     self.gameloop.setState(False)
    #     pass
    # 自定义关闭函数
    def closeEvent(self, event):
        print("closeEvent")
        self.gameloop.setState(False)
        super(Ui_mainWindow, self).closeEvent(event)

    #     选择日志保存位置
    def seachLogsPath(self):
        # 弹出文件选择框
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "选择文件夹", "../")
        if path != "":
            print("有值")
            path = path + "/logs"
        else:
            print("没有值")

    #     打开日志地址
    def showLogs(self):
        print("打开日志地址")
        # 获取日志保存位置
        path = self.lineEdit.text()
        print(path)
        # 打开文件夹
        os.system(f"start explorer {path}")

    #     开始挂机
    def startGameLoop(self):
        print("游戏状态：", self.gameloop.getState())
        if self.gameloop.getState() == False:
            # 将 轮询延迟 与 跳伞延迟 传进去
            self.worker_thread.run(
                self.spinBox.value(),
                self.spinBox_2.value(),
                self.spinBox_5.value(),
                self.checkBox.isChecked(),
            )
            self.pushButton_3.setText("挂机中...")
            # 设置 label_8 的文本为 已开始
            self.label_8.setText("已开始")
        else:
            self.pushButton_3.setText("开始挂机")
            self.gameloop.setState(False)
            # 设置 label_8 的文本为 已开始
            self.label_8.setText("未开始")

    # 修改主窗体文案 hooks 1
    def setStateHooks(self, message):
        global oldText
        if message == oldText:
            self.label_8.setText(message)
        else:
            self.label_8.setText(message)
            oldText = message
        #         判断是否保存日志
        if self.checkBox.isChecked():
            self.logger.info(message)

    # 修改主窗体文案 hooks 2
    def setStateHooks2(self, message):
        global oldText2
        if message == oldText2:
            self.label_11.setText(message)
        else:
            self.label_11.setText(message)
            oldText2 = message
        #         判断是否保存日志
        if self.checkBox.isChecked():
            self.logger.info(message)

    # 打开关于软件
    def openAbout(self):
        self.about_ui = Ui_Form()
        self.about_ui.show()

    # 打开更新日志按钮
    def openUpdateLog(self):
        self.updateLog_ui = Up_data_log()
        self.updateLog_ui.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec())