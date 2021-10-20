# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTGraphicInterfaces/DynamicMainInterface.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(851, 691)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gbr_load_image = QtWidgets.QGroupBox(self.centralwidget)
        self.gbr_load_image.setGeometry(QtCore.QRect(10, 10, 831, 71))
        self.gbr_load_image.setObjectName("gbr_load_image")
        self.btn_load_image = QtWidgets.QPushButton(self.gbr_load_image)
        self.btn_load_image.setGeometry(QtCore.QRect(10, 30, 151, 23))
        self.btn_load_image.setObjectName("btn_load_image")
        self.lbl_load_image = QtWidgets.QLabel(self.gbr_load_image)
        self.lbl_load_image.setGeometry(QtCore.QRect(170, 30, 601, 21))
        self.lbl_load_image.setObjectName("lbl_load_image")
        self.scrollArea_filters = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_filters.setGeometry(QtCore.QRect(10, 200, 421, 461))
        self.scrollArea_filters.setWidgetResizable(True)
        self.scrollArea_filters.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea_filters.setObjectName("scrollArea_filters")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 419, 459))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_filters.setWidget(self.scrollAreaWidgetContents)
        self.gbr_add_filter = QtWidgets.QGroupBox(self.centralwidget)
        self.gbr_add_filter.setGeometry(QtCore.QRect(10, 90, 831, 71))
        self.gbr_add_filter.setCheckable(False)
        self.gbr_add_filter.setObjectName("gbr_add_filter")
        self.btn_draw_zones = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_draw_zones.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.btn_draw_zones.setObjectName("btn_draw_zones")
        self.btn_color_lines = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_color_lines.setGeometry(QtCore.QRect(90, 20, 75, 23))
        self.btn_color_lines.setObjectName("btn_color_lines")
        self.lbl_filters = QtWidgets.QLabel(self.centralwidget)
        self.lbl_filters.setGeometry(QtCore.QRect(200, 170, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_filters.setFont(font)
        self.lbl_filters.setObjectName("lbl_filters")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.gbr_load_image.setTitle(_translate("MainWindow", "Carga de imagen"))
        self.btn_load_image.setText(_translate("MainWindow", "Cargar imagen"))
        self.lbl_load_image.setText(_translate("MainWindow", "..."))
        self.gbr_add_filter.setTitle(_translate("MainWindow", "Agregar filtros"))
        self.btn_draw_zones.setText(_translate("MainWindow", "Dibujar zonas"))
        self.btn_color_lines.setText(_translate("MainWindow", "Color lineas"))
        self.lbl_filters.setText(_translate("MainWindow", "Filtros"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
