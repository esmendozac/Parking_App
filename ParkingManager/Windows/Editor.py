import json
import cv2
import copy

from PyQt5 import QtWidgets
from QTGraphicInterfaces.Editor import Ui_Editor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from Models.Picture import Picture as Pic
from Filters.Filter import FilterTypes, Filter
from Filters.FactoryFilters import FactoryFilter as Ff
from Filters.Delimite import Delimite as De
from Models.Utils import Utils as Ut


class Editor(QtWidgets.QMainWindow):
    # region Attributes
    picture = None
    filters: Filter = []
    coordinates = []

    # endregion

    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """

        super(Editor, self).__init__()
        self.ui = Ui_Editor()
        self.ui.setupUi(self)
        # Asignaciones iniciales
        self.disable_all_buttons(True)
        # Botón de almacenamiento de archivo
        self.ui.btn_save_json.setDisabled(False)
        self._original_picture = None

        # Conexiones
        self.ui.btn_load_image.clicked.connect(self.open_image)
        self.ui.btn_capture_image.clicked.connect(self.capture_image)

        self.ui.btn_delimite.clicked.connect(lambda callback: self.create_filter(FilterTypes.Delimite))
        self.ui.btn_transformation.clicked.connect(lambda callback: self.create_filter(FilterTypes.Transformation))
        self.ui.btn_color.clicked.connect(lambda callback: self.create_filter(FilterTypes.Color))
        self.ui.btn_perspective.clicked.connect(lambda callback: self.create_filter(FilterTypes.PerspectiveTransformation))
        self.ui.btn_search.clicked.connect(lambda callback: self.create_filter(FilterTypes.SpaceConfig))

    def capture_image(self):
        """
        Cargar video desde la fuente especificada
        :return:
        """
        # Constantes
        CAMERA_ADDR = int(self.ui.txb_video_source.text())
        CAMERA_WIDTH = 1920
        CAMERA_HEIGHT = 1080

        # Captura de video
        cap = cv2.VideoCapture(CAMERA_ADDR)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):

                self.picture = Pic()
                self.picture.create_picture_from_content(frame)
                # Almacena imagen inicial
                self.set_original_picture(self.picture)
                Ut.content = self.picture.content
                Ut.path = self.picture.path
                # Asignaciones
                self.disable_all_buttons(False)

                self.ui.btn_capture_image.setDisabled(True)
                self.ui.btn_load_image.setDisabled(True)
                break

        cap.release()
        cv2.destroyAllWindows()

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
            Ut.content = self.picture.content
            Ut.path = self.picture.path
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
            f.set_visible(False)

        if len(self.filters) == 0:
            factory = Ff(self.picture, self.ui)
        else:
            last_filter = self.filters[-1]

            factory = Ff(last_filter.get_picture_filtered(), self.ui)

        self.filters.append(factory.create_filter(filter_id, row, col, widget_id, last_filter, self.coordinates, self))

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
