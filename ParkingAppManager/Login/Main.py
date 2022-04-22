import MainMenu.Main
from Login.Login import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class LoginWindow(QtWidgets.QMainWindow):

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """

        super(LoginWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.login_login_btn.clicked.connect(lambda callback: self.log_in())

        # Conexiones
        # self.ui.btn_load_image.clicked.connect(self.open_image)
        # self.ui.btn_delimite.clicked.connect(lambda callback: self.create_filter(FilterTypes.Delimite))
        # self.ui.btn_transformation.clicked.connect(lambda callback: self.create_filter(FilterTypes.Transformation))
        # self.ui.btn_color.clicked.connect(lambda callback: self.create_filter(FilterTypes.Color))
        # self.ui.btn_perspective.clicked.connect(lambda callback: self.create_filter(FilterTypes.PerspectiveTransformation))

        # self.ui.btn_color_space.clicked.connect(lambda callback: self.create_filter(FilterTypes.ColorSpace))
        # self.ui.btn_delimite_area.clicked.connect(lambda callback: self.create_filter(FilterTypes.DelimiteArea))
    def log_in(self):
        user = self.ui.login_user_tbx.text()
        password = self.ui.login_password_tbx.text()

        menu = MainMenu.Main.MainWindow()

        menu.show()

        # Cierra ventana
        #self.hide()
