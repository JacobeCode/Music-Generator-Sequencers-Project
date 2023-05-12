# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Music_Generator.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os

from PyQt5 import QtCore, QtGui, QtWidgets
from music_informations import music_informations


class Ui_MainWindow(object):
    def __init__(self):
        self.music_info = music_informations()

    def generate_music(self):
        # Multiply by 4 because of calculations on quarter-notes
        points_to_use = (self.music_info.metrum * self.music_info.tacts) * 4

        file_name = "test"
        text_file = open(file_name + ".ly", 'w')
        text_file.write(self.music_info.template + "{\n")
        text_file.write(self.music_info.number_tacts + "\n")
        text_file.write(chr(92) + "time " + str(self.music_info.metrum) + "/4 ")

        while points_to_use > 0:
            self.music_info.melody.append("f'4")
            points_to_use -= 4
        for note in self.music_info.melody:
            text_file.write(note + " ")

        # Closing file and setting proper bars
        text_file.write("\n" + chr(92) + "bar " + chr(34) + "||" + chr(34) + "}")
        text_file.close()

        os.system("lilypond --pdf " + file_name + ".ly")
        os.system(file_name + ".pdf")

    def change_metrum(self):
        if self.metrum_insert.toPlainText() == "":
            pass
        else:
            self.music_info.metrum = int(self.metrum_insert.toPlainText())
            print(str(self.music_info.metrum))

    def change_tacts(self):
        if self.tacts_insert.toPlainText() == "":
            pass
        else:
            self.music_info.tacts = int(self.tacts_insert.toPlainText())
            print(str(self.music_info.tacts))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 668)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(410, 160, 201, 301))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 480, 371, 23))
        self.progressBar.setProperty("value", 21)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.settings_tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.settings_tabs.setGeometry(QtCore.QRect(20, 150, 371, 321))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.settings_tabs.setFont(font)
        self.settings_tabs.setObjectName("settings_tabs")
        self.basic_settings = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.basic_settings.setFont(font)
        self.basic_settings.setObjectName("basic_settings")
        self.comboBox_4 = QtWidgets.QComboBox(self.basic_settings)
        self.comboBox_4.setGeometry(QtCore.QRect(40, 220, 151, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox = QtWidgets.QComboBox(self.basic_settings)
        self.comboBox.setGeometry(QtCore.QRect(20, 110, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox_2 = QtWidgets.QComboBox(self.basic_settings)
        self.comboBox_2.setGeometry(QtCore.QRect(190, 120, 141, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.basic_settings)
        self.comboBox_3.setGeometry(QtCore.QRect(10, 180, 281, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.metrum_info = QtWidgets.QTextEdit(self.basic_settings)
        self.metrum_info.setGeometry(QtCore.QRect(10, 10, 221, 41))
        self.metrum_info.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.metrum_info.setLineWidth(0)
        self.metrum_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.metrum_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.metrum_info.setObjectName("metrum_info")
        self.metrum_insert = QtWidgets.QTextEdit(self.basic_settings)
        self.metrum_insert.setGeometry(QtCore.QRect(240, 10, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.metrum_insert.setFont(font)
        self.metrum_insert.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.metrum_insert.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_insert.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_insert.setObjectName("metrum_insert")
        self.metrum_div = QtWidgets.QTextEdit(self.basic_settings)
        self.metrum_div.setGeometry(QtCore.QRect(300, 10, 51, 41))
        self.metrum_div.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.metrum_div.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_div.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.metrum_div.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.metrum_div.setObjectName("metrum_div")
        self.tacts_info = QtWidgets.QTextEdit(self.basic_settings)
        self.tacts_info.setGeometry(QtCore.QRect(10, 60, 221, 41))
        self.tacts_info.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.tacts_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_info.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.tacts_info.setObjectName("tacts_info")
        self.tacts_insert = QtWidgets.QTextEdit(self.basic_settings)
        self.tacts_insert.setGeometry(QtCore.QRect(240, 60, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.tacts_insert.setFont(font)
        self.tacts_insert.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.tacts_insert.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_insert.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tacts_insert.setObjectName("tacts_insert")
        self.metrum_insert.raise_()
        self.comboBox_4.raise_()
        self.comboBox.raise_()
        self.comboBox_2.raise_()
        self.comboBox_3.raise_()
        self.metrum_info.raise_()
        self.metrum_div.raise_()
        self.tacts_info.raise_()
        self.tacts_insert.raise_()
        self.settings_tabs.addTab(self.basic_settings, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.spinBox_8 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_8.setGeometry(QtCore.QRect(50, 170, 42, 22))
        self.spinBox_8.setObjectName("spinBox_8")
        self.spinBox_22 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_22.setGeometry(QtCore.QRect(260, 80, 42, 22))
        self.spinBox_22.setObjectName("spinBox_22")
        self.spinBox_7 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_7.setGeometry(QtCore.QRect(50, 200, 42, 22))
        self.spinBox_7.setObjectName("spinBox_7")
        self.spinBox_26 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_26.setGeometry(QtCore.QRect(260, 170, 42, 22))
        self.spinBox_26.setObjectName("spinBox_26")
        self.spinBox = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox.setGeometry(QtCore.QRect(50, 20, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_20 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_20.setGeometry(QtCore.QRect(260, 50, 42, 22))
        self.spinBox_20.setObjectName("spinBox_20")
        self.spinBox_12 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_12.setGeometry(QtCore.QRect(50, 260, 42, 22))
        self.spinBox_12.setObjectName("spinBox_12")
        self.spinBox_9 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_9.setGeometry(QtCore.QRect(160, 80, 42, 22))
        self.spinBox_9.setObjectName("spinBox_9")
        self.spinBox_25 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_25.setGeometry(QtCore.QRect(160, 170, 42, 22))
        self.spinBox_25.setObjectName("spinBox_25")
        self.spinBox_13 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_13.setGeometry(QtCore.QRect(160, 230, 42, 22))
        self.spinBox_13.setObjectName("spinBox_13")
        self.spinBox_17 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_17.setGeometry(QtCore.QRect(260, 110, 42, 22))
        self.spinBox_17.setObjectName("spinBox_17")
        self.spinBox_15 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_15.setGeometry(QtCore.QRect(260, 20, 42, 22))
        self.spinBox_15.setObjectName("spinBox_15")
        self.spinBox_18 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_18.setGeometry(QtCore.QRect(160, 140, 42, 22))
        self.spinBox_18.setObjectName("spinBox_18")
        self.spinBox_5 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_5.setGeometry(QtCore.QRect(50, 230, 42, 22))
        self.spinBox_5.setObjectName("spinBox_5")
        self.spinBox_11 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_11.setGeometry(QtCore.QRect(260, 230, 42, 22))
        self.spinBox_11.setObjectName("spinBox_11")
        self.spinBox_24 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_24.setGeometry(QtCore.QRect(260, 260, 42, 22))
        self.spinBox_24.setObjectName("spinBox_24")
        self.spinBox_2 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_2.setGeometry(QtCore.QRect(50, 50, 42, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_21 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_21.setGeometry(QtCore.QRect(160, 200, 42, 22))
        self.spinBox_21.setObjectName("spinBox_21")
        self.spinBox_6 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_6.setGeometry(QtCore.QRect(50, 140, 42, 22))
        self.spinBox_6.setObjectName("spinBox_6")
        self.spinBox_3 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_3.setGeometry(QtCore.QRect(50, 80, 42, 22))
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_19 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_19.setGeometry(QtCore.QRect(260, 200, 42, 22))
        self.spinBox_19.setObjectName("spinBox_19")
        self.spinBox_4 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_4.setGeometry(QtCore.QRect(50, 110, 42, 22))
        self.spinBox_4.setObjectName("spinBox_4")
        self.spinBox_14 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_14.setGeometry(QtCore.QRect(160, 50, 42, 22))
        self.spinBox_14.setObjectName("spinBox_14")
        self.spinBox_10 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_10.setGeometry(QtCore.QRect(160, 110, 42, 22))
        self.spinBox_10.setObjectName("spinBox_10")
        self.spinBox_16 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_16.setGeometry(QtCore.QRect(160, 20, 42, 22))
        self.spinBox_16.setObjectName("spinBox_16")
        self.spinBox_23 = QtWidgets.QSpinBox(self.tab_2)
        self.spinBox_23.setGeometry(QtCore.QRect(260, 140, 42, 22))
        self.spinBox_23.setObjectName("spinBox_23")
        self.settings_tabs.addTab(self.tab_2, "")
        self.generate_button = QtWidgets.QPushButton(self.centralwidget)
        self.generate_button.setGeometry(QtCore.QRect(410, 480, 201, 23))
        self.generate_button.setObjectName("generate_button")
        self.command_line_window = QtWidgets.QTextEdit(self.centralwidget)
        self.command_line_window.setEnabled(True)
        self.command_line_window.setGeometry(QtCore.QRect(20, 10, 591, 131))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.command_line_window.setFont(font)
        self.command_line_window.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.command_line_window.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.command_line_window.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.command_line_window.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.command_line_window.setObjectName("command_line_window")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.settings_tabs.setCurrentIndex(0)
        self.generate_button.clicked.connect(MainWindow.generate_music)  # type: ignore
        self.metrum_insert.textChanged.connect(MainWindow.change_metrum)  # type: ignore
        self.tacts_insert.textChanged.connect(MainWindow.change_tacts)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.metrum_info.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                            "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">Here you can type in your requested metrum (in format - n/4)</span></p></body></html>"))
        self.metrum_insert.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.metrum_div.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-style:italic;\">/4</span></p></body></html>"))
        self.tacts_info.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:600; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">Here you can input your requested number of  tacts</span></p>\n"
                                           "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-style:italic;\"><br /></p></body></html>"))
        self.tacts_insert.setHtml(_translate("MainWindow",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:600; font-style:normal;\">\n"
                                             "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.basic_settings),
                                      _translate("MainWindow", "Basic_Settings"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.generate_button.setText(_translate("MainWindow", "Generate"))
        self.command_line_window.setHtml(_translate("MainWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'Times New Roman\'; font-size:12pt; font-weight:600; font-style:italic;\">\n"
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\';\">Welcome in the program for basic, algorithmic music generation !</span></p></body></html>"))