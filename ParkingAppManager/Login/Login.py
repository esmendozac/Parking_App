# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login/Login.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(367, 362)
        self.login_frame = QtWidgets.QFrame(Form)
        self.login_frame.setGeometry(QtCore.QRect(10, 230, 351, 121))
        self.login_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.login_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.login_frame.setObjectName("login_frame")
        self.login_login_btn = QtWidgets.QPushButton(self.login_frame)
        self.login_login_btn.setGeometry(QtCore.QRect(140, 90, 75, 23))
        self.login_login_btn.setObjectName("login_login_btn")
        self.login_user_tbx = QtWidgets.QLineEdit(self.login_frame)
        self.login_user_tbx.setGeometry(QtCore.QRect(120, 20, 171, 20))
        self.login_user_tbx.setObjectName("login_user_tbx")
        self.login_user_lbl = QtWidgets.QLabel(self.login_frame)
        self.login_user_lbl.setGeometry(QtCore.QRect(30, 20, 47, 13))
        self.login_user_lbl.setObjectName("login_user_lbl")
        self.login_password_lbl = QtWidgets.QLabel(self.login_frame)
        self.login_password_lbl.setGeometry(QtCore.QRect(30, 50, 71, 16))
        self.login_password_lbl.setObjectName("login_password_lbl")
        self.login_password_tbx = QtWidgets.QLineEdit(self.login_frame)
        self.login_password_tbx.setGeometry(QtCore.QRect(120, 50, 171, 20))
        self.login_password_tbx.setObjectName("login_password_tbx")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.login_login_btn.setText(_translate("Form", "Iniciar"))
        self.login_user_lbl.setText(_translate("Form", "Usuario"))
        self.login_password_lbl.setText(_translate("Form", "Contraseña"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
