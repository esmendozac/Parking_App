from QTGraphicInterfaces.MainMenu import Ui_MainWindow as menu
from PyQt5 import QtCore, QtGui, QtWidgets
# Ventanas
from Windows.Editor import Editor

import sys


class MainMenu(QtWidgets.QMainWindow):

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """
        super(MainMenu, self).__init__()
        self.ui = menu()
        self.ui.setupUi(self)

        # Conexiones
        self.ui.cfg_btn_create.clicked.connect(self.open_creator)

    @staticmethod
    def open_creator():
        app_editor = Editor()
        app_editor.show()


app = QtWidgets.QApplication([])
application = MainMenu()
application.show()
sys.exit(app.exec())