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
        MainWindow.resize(441, 801)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gbr_load_image = QtWidgets.QGroupBox(self.centralwidget)
        self.gbr_load_image.setGeometry(QtCore.QRect(10, 10, 421, 91))
        self.gbr_load_image.setObjectName("gbr_load_image")
        self.btn_load_image = QtWidgets.QPushButton(self.gbr_load_image)
        self.btn_load_image.setGeometry(QtCore.QRect(10, 20, 401, 23))
        self.btn_load_image.setObjectName("btn_load_image")
        self.lbl_load_image = QtWidgets.QLabel(self.gbr_load_image)
        self.lbl_load_image.setGeometry(QtCore.QRect(10, 50, 391, 31))
        self.lbl_load_image.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_load_image.setObjectName("lbl_load_image")
        self.scrollArea_filters = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_filters.setGeometry(QtCore.QRect(10, 170, 421, 601))
        self.scrollArea_filters.setWidgetResizable(True)
        self.scrollArea_filters.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scrollArea_filters.setObjectName("scrollArea_filters")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 419, 599))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea_filters.setWidget(self.scrollAreaWidgetContents)
        self.gbr_add_filter = QtWidgets.QGroupBox(self.centralwidget)
        self.gbr_add_filter.setGeometry(QtCore.QRect(10, 110, 421, 51))
        self.gbr_add_filter.setCheckable(False)
        self.gbr_add_filter.setObjectName("gbr_add_filter")
        self.btn_delimite = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_delimite.setGeometry(QtCore.QRect(40, 20, 71, 23))
        self.btn_delimite.setObjectName("btn_delimite")
        self.btn_color = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_color.setGeometry(QtCore.QRect(110, 20, 71, 23))
        self.btn_color.setObjectName("btn_color")
        self.btn_transformation = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_transformation.setGeometry(QtCore.QRect(180, 20, 71, 23))
        self.btn_transformation.setObjectName("btn_transformation")
        self.btn_perspective = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_perspective.setGeometry(QtCore.QRect(250, 20, 71, 23))
        self.btn_perspective.setObjectName("btn_perspective")
        self.btn_search = QtWidgets.QPushButton(self.gbr_add_filter)
        self.btn_search.setGeometry(QtCore.QRect(320, 20, 71, 23))
        self.btn_search.setObjectName("btn_search")
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
        self.btn_delimite.setText(_translate("MainWindow", "Delimitar "))
        self.btn_color.setText(_translate("MainWindow", "Color"))
        self.btn_transformation.setText(_translate("MainWindow", "Transf. libre"))
        self.btn_perspective.setText(_translate("MainWindow", "Perspectiva"))
        self.btn_search.setText(_translate("MainWindow", "Busqueda"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
