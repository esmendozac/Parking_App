from QTGraphicInterfaces.MainMenu import Ui_MainWindow as menu
from PyQt5 import QtCore, QtGui, QtWidgets
# Ventanas
from Windows.Editor import Editor
from Windows.VisorClass import Visor

# Comunicación
from Integration.ParkingApi import ParkingApi
import sys


class MainMenu(QtWidgets.QMainWindow):

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """
        super(MainMenu, self).__init__()
        self.ui = menu()
        self.ui.setupUi(self)
        self.api = ParkingApi()

        # Conexiones
        self.ui.cfg_btn_create.clicked.connect(self.open_creator)
        self.ui.op_btn_start.clicked.connect(self.load_parking)

    @staticmethod
    def open_creator():
        app_editor = Editor()
        app_editor.show()

    def load_parking(self):

        # Lectura del Id
        parking_id = int(self.ui.op_txb_id.text())
        data = self.api.get_parking(parking_id)

        # Instancia del visor
        app_visor = Visor(data)


app = QtWidgets.QApplication([])
application = MainMenu()
application.show()
sys.exit(app.exec())