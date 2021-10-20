# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QTGraphicInterfaces/MainInterface.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(892, 427)
        self.btn_load_image = QtWidgets.QPushButton(Form)
        self.btn_load_image.setGeometry(QtCore.QRect(10, 10, 151, 23))
        self.btn_load_image.setObjectName("btn_load_image")
        self.lbl_load_image = QtWidgets.QLabel(Form)
        self.lbl_load_image.setGeometry(QtCore.QRect(170, 10, 701, 21))
        self.lbl_load_image.setObjectName("lbl_load_image")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 331, 61))
        self.groupBox.setObjectName("groupBox")
        self.btn_dibujar_zona = QtWidgets.QPushButton(self.groupBox)
        self.btn_dibujar_zona.setGeometry(QtCore.QRect(30, 20, 91, 23))
        self.btn_dibujar_zona.setObjectName("btn_dibujar_zona")
        self.lbl_dibujar_zona = QtWidgets.QLabel(self.groupBox)
        self.lbl_dibujar_zona.setGeometry(QtCore.QRect(10, 20, 16, 21))
        self.lbl_dibujar_zona.setAutoFillBackground(False)
        self.lbl_dibujar_zona.setStyleSheet("background: rgb(0, 255, 0);\n"
"border: 1px solid black;")
        self.lbl_dibujar_zona.setText("")
        self.lbl_dibujar_zona.setObjectName("lbl_dibujar_zona")
        self.btn_limpiar_zonas = QtWidgets.QPushButton(self.groupBox)
        self.btn_limpiar_zonas.setGeometry(QtCore.QRect(130, 20, 91, 23))
        self.btn_limpiar_zonas.setObjectName("btn_limpiar_zonas")
        self.btn_ver_zonas = QtWidgets.QPushButton(self.groupBox)
        self.btn_ver_zonas.setGeometry(QtCore.QRect(230, 20, 91, 23))
        self.btn_ver_zonas.setObjectName("btn_ver_zonas")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 120, 331, 71))
        self.groupBox_2.setObjectName("groupBox_2")
        self.lbl_color_linea = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_color_linea.setGeometry(QtCore.QRect(10, 30, 16, 21))
        self.lbl_color_linea.setAutoFillBackground(False)
        self.lbl_color_linea.setStyleSheet("background: rgb(255, 255, 255 );\n"
"border: 1px solid black;")
        self.lbl_color_linea.setText("")
        self.lbl_color_linea.setObjectName("lbl_color_linea")
        self.btn_capturar_color = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_capturar_color.setGeometry(QtCore.QRect(30, 30, 91, 23))
        self.btn_capturar_color.setObjectName("btn_capturar_color")
        self.btn_aplicar_color_linea = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_aplicar_color_linea.setGeometry(QtCore.QRect(230, 30, 91, 23))
        self.btn_aplicar_color_linea.setObjectName("btn_aplicar_color_linea")
        self.sld_tolerancia_linea = QtWidgets.QSlider(self.groupBox_2)
        self.sld_tolerancia_linea.setGeometry(QtCore.QRect(130, 30, 91, 22))
        self.sld_tolerancia_linea.setMinimum(5)
        self.sld_tolerancia_linea.setMaximum(30)
        self.sld_tolerancia_linea.setPageStep(1)
        self.sld_tolerancia_linea.setSliderPosition(11)
        self.sld_tolerancia_linea.setTracking(False)
        self.sld_tolerancia_linea.setOrientation(QtCore.Qt.Horizontal)
        self.sld_tolerancia_linea.setObjectName("sld_tolerancia_linea")
        self.lbl_tolerancia_linea = QtWidgets.QLabel(self.groupBox_2)
        self.lbl_tolerancia_linea.setGeometry(QtCore.QRect(200, 10, 31, 16))
        self.lbl_tolerancia_linea.setObjectName("lbl_tolerancia_linea")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_load_image.setText(_translate("Form", "Cargar imagen"))
        self.lbl_load_image.setText(_translate("Form", "..."))
        self.groupBox.setTitle(_translate("Form", "Delimitacion zonas"))
        self.btn_dibujar_zona.setText(_translate("Form", "Dibujar"))
        self.btn_limpiar_zonas.setText(_translate("Form", "Limpiar"))
        self.btn_ver_zonas.setText(_translate("Form", "Ver"))
        self.groupBox_2.setTitle(_translate("Form", "Seleccion de color lineas"))
        self.btn_capturar_color.setText(_translate("Form", "Capturar"))
        self.btn_aplicar_color_linea.setText(_translate("Form", "Aplicar"))
        self.lbl_tolerancia_linea.setText(_translate("Form", "11 %"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
