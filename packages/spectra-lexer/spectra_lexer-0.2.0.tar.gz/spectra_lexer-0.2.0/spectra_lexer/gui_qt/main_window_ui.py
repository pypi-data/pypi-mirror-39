# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra_lexer\gui_qt\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/spectra_lexer/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.w_central = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_central.sizePolicy().hasHeightForWidth())
        self.w_central.setSizePolicy(sizePolicy)
        self.w_central.setMinimumSize(QtCore.QSize(0, 0))
        self.w_central.setObjectName("w_central")
        self.layout_main = QtWidgets.QHBoxLayout(self.w_central)
        self.layout_main.setObjectName("layout_main")
        self.w_main = MainWidget(self.w_central)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_main.sizePolicy().hasHeightForWidth())
        self.w_main.setSizePolicy(sizePolicy)
        self.w_main.setObjectName("w_main")
        self.layout_main.addWidget(self.w_main)
        MainWindow.setCentralWidget(self.w_central)
        self.m_menu = QtWidgets.QMenuBar(MainWindow)
        self.m_menu.setGeometry(QtCore.QRect(0, 0, 550, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.m_menu.setFont(font)
        self.m_menu.setObjectName("m_menu")
        self.m_file = QtWidgets.QMenu(self.m_menu)
        self.m_file.setObjectName("m_file")
        MainWindow.setMenuBar(self.m_menu)
        self.m_file_load = QtWidgets.QAction(MainWindow)
        self.m_file_load.setObjectName("m_file_load")
        self.m_file_exit = QtWidgets.QAction(MainWindow)
        self.m_file_exit.setObjectName("m_file_exit")
        self.m_file.addAction(self.m_file_load)
        self.m_file.addAction(self.m_file_exit)
        self.m_menu.addAction(self.m_file.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spectra Lexer"))
        self.m_file.setTitle(_translate("MainWindow", "File"))
        self.m_file_load.setText(_translate("MainWindow", "Load Dictionary..."))
        self.m_file_exit.setText(_translate("MainWindow", "Exit"))

from spectra_lexer.gui_qt.main_widget import MainWidget
from . import resources_rc
