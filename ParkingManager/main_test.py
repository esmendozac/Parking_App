from PyQt5 import QtWidgets
from QTGraphicInterfaces.DynamicMainInterface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from Models.Picture import Picture as Pic
from Filters.Filter import FilterTypes, Filter
from Filters.FactoryFilters import FactoryFilter as Ff

import sys


class MainWindow(QtWidgets.QMainWindow):
    # region Attributes
    picture = None
    filters: Filter = []

    # endregion

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Asignaciones iniciales
        self.ui.btn_draw_zones.setDisabled(True)
        self.ui.btn_color_lines.setDisabled(True)
        # Conexiones
        self.ui.btn_load_image.clicked.connect(self.open_image)
        self.ui.btn_draw_zones.clicked.connect(lambda callback: self.create_filter(FilterTypes.DrawZones))
        self.ui.btn_color_lines.clicked.connect(lambda callback: self.create_filter(FilterTypes.ColorLines))

    def open_image(self):
        """
        Abre una imagen del sistema de archivos
        :return:
        """

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Imágenes png (*.png)", options=options)

        if file_name:
            self.ui.lbl_load_image.setText(file_name)
            self.picture = Pic(file_name)
            # Asignaciones
            self.ui.btn_draw_zones.setDisabled(False)
            self.ui.btn_color_lines.setDisabled(False)

    def create_filter(self, filter_id: FilterTypes):
        """
        Retorna una instancia de filtro nueva según se indique como parámetro.
        :param filter_id:
        :return:
        """
        widget_id = len(self.filters)
        row = len(self.filters)
        col = 0

        factory = Ff(self.picture, self.ui)
        self.filters.append(factory.create_filter(filter_id, row, col, widget_id))


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())
