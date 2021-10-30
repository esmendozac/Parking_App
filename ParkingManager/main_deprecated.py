from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from QTGraphicInterfaces.MainInterface import Ui_Form
from Models.Image import Image as Im
from Filters.DrawZones import DrawZones as Saf

import sys
import cv2
import numpy as np


class MainWindow(QtWidgets.QMainWindow):

    # region Attributes
    image = None
    # endregion

    # region Functions
    def __init__(self):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """

        super(MainWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Señal de apertura de filedialog
        self.ui.btn_load_image.clicked.connect(self.open_file)

        self.ui.btn_dibujar_zona.clicked.connect(self.load_image)
        self.ui.btn_ver_zonas.clicked.connect(self.view_zones)
        self.ui.btn_limpiar_zonas.clicked.connect(self.clean_zones)

        self.ui.btn_capturar_color.clicked.connect(self.capture_lines_color)
        self.ui.sld_tolerancia_linea.valueChanged.connect(self.sld_tolerancia_linea_evt)

        # Zona de delimitación
        self.ui.btn_dibujar_zona.setDisabled(True)
        self.ui.btn_limpiar_zonas.setDisabled(True)
        self.ui.btn_ver_zonas.setDisabled(True)

        # Zona de captura de color
        self.ui.btn_capturar_color.setDisabled(True)

    def open_file(self):
        """
        Abre una imagen del sistema de archivos
        :return:
        """

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Imágenes png (*.png)", options=options)

        if file_name:
            # Almacena label
            self.ui.lbl_load_image.setText(file_name)
            # Crea la imagen
            self.image = Im(file_name)
            # Habilita el botón de dibujar
            self.ui.btn_dibujar_zona.setDisabled(False)
            self.ui.btn_capturar_color.setDisabled(False)

        else:
            self.ui.lbl_load_image.setText("...")

    def draw_points_callback(self, event, x, y, flags, param):
        """
        Callback para eventos mouse encargado de gestionar el dibujo de contornos
        :param event:
        :param x:
        :param y:
        :param flags:
        :param param:
        :return:
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Cada punto dibujado es una coordenada almacenada y dibujada
            self.image.add_limit_coordinate(x, y, is_last=False)
            cv2.circle(self.image.image, (x, y), 3, (0, 255, 0), -1)
            # Actualiza la imagen mostrada
            cv2.imshow('Dibujando imagen...', self.image.image)

        # control + click añade una nueva zona delimitada
        elif event == cv2.EVENT_MBUTTONDBLCLK:

            # Crea una zona delimitada
            if len(self.image.limits[-1]) > 3:
                # Extrae los contornos
                contours = np.array([self.image.limits[-1]])
                # Cierra el contorno
                self.image.add_close_last_limit()
                # Crear una mascara genérica del mismo tamaño de la imagen
                mask = np.zeros(shape=(self.image.image.shape[:2]), dtype=np.uint8)
                # Itera por los contornos y crea la mascara
                mask = cv2.drawContours(mask, contours, -1, 255, -1)
                # Almacena la mascara en la imagen
                self.image.masks.append(mask)
                # Dibuja el contorno en la imagen original
                cv2.drawContours(self.image.image, contours, -1, (0, 255, 0), 2)
                # Habilita el botón de visualización de resultados s
                self.ui.btn_ver_zonas.setDisabled(False)
                self.ui.btn_limpiar_zonas.setDisabled(False)
                # Muestra el contorno
                cv2.imshow('Dibujando imagen...', self.image.image)

    def load_image(self):
        """
        Carga imagen del sistema de archivos
        :return:
        """
        try:
            cv2.imshow('Dibujando imagen...', self.image.image)
            # Callback de eventos de mouse
            cv2.setMouseCallback('Dibujando imagen...', self.draw_points_callback)
        except:
            ex = "No se puede cargar la imagen " + self.image.path
            raise Exception(ex)

    def view_zones(self):
        """
        Permite ver zonas, extrae mascaras concatenadas y realiza operación and con la imagen original
        :return:
        """
        mask = self.image.get_all_masks_limits()

        # Genera la capa filtrada con la mascara adecuada
        image_limits = cv2.bitwise_and(self.image.get_original(), self.image.get_original(), mask=mask)
        cv2.imshow('Zonas delimitadas', image_limits)

    def clean_zones(self):
        """
        Limpieza de las zonas en el objeto imagen y en la interfaz gráfica
        :return:
        """
        # Limpieza interna de la imagen
        self.image.clean_zones()
        # Visualiza imagen de nuevo
        cv2.imshow('Dibujando imagen...', self.image.image)

    def capture_lines_color(self):
        # Visualiza la imagen para capturar el color
        cv2.imshow('Capturando color de linea...', self.image.image)

        cv2.setMouseCallback('Capturando color de linea...', self.capture_lines_color_callback)

    def capture_lines_color_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Extrae valores de pixel de la imagen
            r, g, b, h, s, v = self.image.get_pixel_values(x, y)
            # Visualiza el color extraído en el label
            self.ui.lbl_color_linea.setStyleSheet(f"background: rgb({r}, {g}, {b} );\n""border: 1px solid black;")
            # Cambia espacio de color
            hsv = cv2.cvtColor(self.image.image, cv2.COLOR_BGR2HSV)
            # Lee la tolerancia del slider
            tolerance = int(self.ui.sld_tolerancia_linea.value())
            # Calcula la mascara
            mask = Im.calculate_hsv_mask(hsv, h, s, v, tolerance)
            # AND entre las dos mascaras
            res_hsv = cv2.bitwise_and(self.image.image, self.image.image, mask=mask)
            # Filtro de color de lineas
            cv2.imshow('Filtro de color de lineas aplicado...', res_hsv)

    def sld_tolerancia_linea_evt(self):
        # Actualiza el valor en el label de referencia
        self.ui.lbl_tolerancia_linea.setText(str(self.ui.sld_tolerancia_linea.value()) + " %")
    # endregion


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())
