from PyQt5 import QtWidgets
from QTGraphicInterfaces.DynamicMainInterfaceForm import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from Models.Picture import Picture as Pic
from Filters.Filter import FilterTypes, Filter
from Filters.FactoryFilters import FactoryFilter as Ff
from Filters.Delimite import Delimite as De

import sys
import copy


class MainWindow(QtWidgets.QMainWindow):
    # region Attributes
    picture = None
    filters: Filter = []
    coordinates = []

    # endregion

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """

        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Asignaciones iniciales
        self.disable_all_buttons(True)
        self._original_picture = None

        # Conexiones
        self.ui.btn_load_image.clicked.connect(self.open_image)
        self.ui.btn_delimite.clicked.connect(lambda callback: self.create_filter(FilterTypes.Delimite))
        self.ui.btn_transformation.clicked.connect(lambda callback: self.create_filter(FilterTypes.Transformation))
        self.ui.btn_color.clicked.connect(lambda callback: self.create_filter(FilterTypes.Color))
        self.ui.btn_perspective.clicked.connect(lambda callback: self.create_filter(FilterTypes.PerspectiveTransformation))
        self.ui.btn_search.clicked.connect(lambda callback: self.create_filter(FilterTypes.SpaceConfig))
        # self.ui.btn_color_space.clicked.connect(lambda callback: self.create_filter(FilterTypes.ColorSpace))
        # self.ui.btn_delimite_area.clicked.connect(lambda callback: self.create_filter(FilterTypes.DelimiteArea))

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
            self.picture = Pic()
            self.picture.create_picture_from_path(file_name)

            # Almacena imagen inicial
            self.set_original_picture(self.picture)

            # Asignaciones
            self.disable_all_buttons(False)

    def create_filter(self, filter_id: FilterTypes):
        """
        Retorna una instancia de filtro nueva según se indique como parámetro.
        :param filter_id:
        :return:
        """
        widget_id = len(self.filters)
        row = len(self.filters)
        col = 0

        last_filter = None

        # Busca filtro que tenga coordenadas y las extrae
        for f in self.filters:
            if isinstance(f, De):
                self.coordinates.append(f.get_coordinates())

        if len(self.filters) == 0:
            factory = Ff(self.picture, self.ui)
        else:
            last_filter = self.filters[-1]
            factory = Ff(last_filter.get_picture_filtered(), self.ui)

        self.filters.append(factory.create_filter(filter_id, row, col, widget_id, last_filter, self.coordinates, self.get_original_picture()))

    def disable_all_buttons(self, state: bool):
        """
        Habilita o deshabilita todos los botones
        :param state:
        :return:
        """
        self.ui.btn_delimite.setDisabled(state)
        self.ui.btn_color.setDisabled(state)
        self.ui.btn_transformation.setDisabled(state)
        self.ui.btn_search.setDisabled(state)
        self.ui.btn_perspective.setDisabled(state)

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())
