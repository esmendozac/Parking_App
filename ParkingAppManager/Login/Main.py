from Login.Login import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """

        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


        # Conexiones
        # self.ui.btn_load_image.clicked.connect(self.open_image)
        # self.ui.btn_delimite.clicked.connect(lambda callback: self.create_filter(FilterTypes.Delimite))
        # self.ui.btn_transformation.clicked.connect(lambda callback: self.create_filter(FilterTypes.Transformation))
        # self.ui.btn_color.clicked.connect(lambda callback: self.create_filter(FilterTypes.Color))
        # self.ui.btn_perspective.clicked.connect(lambda callback: self.create_filter(FilterTypes.PerspectiveTransformation))
        # self.ui.btn_search.clicked.connect(lambda callback: self.create_filter(FilterTypes.SpaceConfig))
        # self.ui.btn_color_space.clicked.connect(lambda callback: self.create_filter(FilterTypes.ColorSpace))
        # self.ui.btn_delimite_area.clicked.connect(lambda callback: self.create_filter(FilterTypes.DelimiteArea))

def run():
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
