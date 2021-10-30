import cv2
import numpy as np
import copy
from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtWidgets
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class Color(Filter):

    def __init__(self, picture, ui: Ui, row: int, col: int, widget_id: int):

        # Imagen original
        self._original_picture = None
        # Indica que el filtro fué finalizado
        self.is_done = False
        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.draw_widget(row, col, widget_id)
        self.widget_id = widget_id
        self.mask = []

    def draw_widget(self, row: int, col: int, widget_id: int):
        """
        Renderiza el widget del filtro en la pantalla
        :param row:
        :param col:
        :param widget_id:
        :return:
        """

        setattr(self.ui, f'ls_frame_{widget_id}', QtWidgets.QFrame(self.ui.scrollAreaWidgetContents))
        frame = getattr(self.ui, f'ls_frame_{widget_id}')
        frame.setMinimumSize(QtCore.QSize(400, 80))
        frame.setMaximumSize(QtCore.QSize(400, 100))
        frame.setStyleSheet("")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName(f'ls_frame_{widget_id}')

        setattr(self.ui, f'ls_grb_lines_{widget_id}', QtWidgets.QGroupBox(frame))
        ls_grb_lines = getattr(self.ui, f'ls_grb_lines_{widget_id}')
        ls_grb_lines.setGeometry(QtCore.QRect(0, 0, 391, 100))
        ls_grb_lines.setObjectName(f'ls_grb_lines_{widget_id}')

        setattr(self.ui, f'ls_lbl_line_color_{widget_id}', QtWidgets.QLabel(ls_grb_lines))
        ls_lbl_line_color = getattr(self.ui, f'ls_lbl_line_color_{widget_id}')
        ls_lbl_line_color.setGeometry(QtCore.QRect(10, 30, 16, 21))
        ls_lbl_line_color.setAutoFillBackground(False)
        ls_lbl_line_color.setStyleSheet("background: rgb(255, 255, 255 );\n"
                                             "border: 1px solid black;")
        ls_lbl_line_color.setText("")
        ls_lbl_line_color.setObjectName(f'ls_lbl_line_color_{widget_id}')

        setattr(self.ui, f'ls_btn_capture_color_{widget_id}', QtWidgets.QPushButton(ls_grb_lines))
        ls_btn_capture_color = getattr(self.ui, f'ls_btn_capture_color_{widget_id}')
        ls_btn_capture_color.setGeometry(QtCore.QRect(30, 30, 71, 23))
        ls_btn_capture_color.setObjectName(f'ls_btn_capture_color_{widget_id}')

        setattr(self.ui, f'ls_btn_apply_color_{widget_id}', QtWidgets.QPushButton(ls_grb_lines))
        ls_btn_apply_color = getattr(self.ui, f'ls_btn_apply_color_{widget_id}')
        ls_btn_apply_color.setGeometry(QtCore.QRect(30, 60, 71, 23))
        ls_btn_apply_color.setObjectName(f'ls_btn_apply_color_{widget_id}')

        setattr(self.ui, f'ls_sld_line_tolerance_{widget_id}', QtWidgets.QSlider(ls_grb_lines))
        ls_sld_line_tolerance = getattr(self.ui, f'ls_sld_line_tolerance_{widget_id}')
        ls_sld_line_tolerance.setGeometry(QtCore.QRect(110, 30, 161, 22))
        ls_sld_line_tolerance.setMinimum(5)
        ls_sld_line_tolerance.setMaximum(30)
        ls_sld_line_tolerance.setPageStep(1)
        ls_sld_line_tolerance.setSliderPosition(11)
        ls_sld_line_tolerance.setTracking(False)
        ls_sld_line_tolerance.setOrientation(QtCore.Qt.Horizontal)
        ls_sld_line_tolerance.setObjectName(f'ls_sld_line_tolerance_{widget_id}')

        setattr(self.ui, f'ls_lbl_line_tolerance_{widget_id}',QtWidgets.QLabel(ls_grb_lines))
        ls_lbl_line_tolerance = getattr(self.ui, f'ls_lbl_line_tolerance_{widget_id}')
        ls_lbl_line_tolerance.setGeometry(QtCore.QRect(180, 60, 31, 16))
        ls_lbl_line_tolerance.setObjectName(f'ls_sld_line_tolerance_{widget_id}')

        setattr(self.ui, f'ls_btn_delete_{widget_id}', QtWidgets.QPushButton(ls_grb_lines))
        ls_btn_delete = getattr(self.ui, f'ls_btn_delete_{widget_id}')
        ls_btn_delete.setGeometry(QtCore.QRect(280, 30, 61, 23))
        ls_btn_delete.setObjectName(f'ls_btn_delete_{widget_id}')

        self.ui.gridLayout.addWidget(frame, row, col, 1, 1)

        _translate = QtCore.QCoreApplication.translate

        ls_grb_lines.setTitle(_translate("MainWindow", "Selección de color lineas"))
        ls_btn_capture_color.setText(_translate("MainWindow", "Capturar"))
        ls_btn_apply_color.setText(_translate("MainWindow", "Aplicar"))
        ls_lbl_line_tolerance.setText(_translate("MainWindow", "11 %"))
        ls_btn_delete.setText(_translate("MainWindow", "Eliminar"))

        # Conexiones

        ls_btn_capture_color.clicked.connect(self.capture_lines_color)
        ls_sld_line_tolerance.valueChanged.connect(self.sld_tolerancia_linea_evt)

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)

    def capture_lines_color(self):
        try:
            cv2.imshow(f'{self.widget_id}_Capturando color de linea...', self.picture)
            # Callback de eventos de mouse
            cv2.setMouseCallback(f'{self.widget_id}_Capturando color de linea...', self.capture_lines_color_callback)
        except Exception as ex:
            raise Exception(ex)

    def get_pixel_values(self, x, y):
        """
            Extrae valores RGB y HSV de una imagen especificada para una coordenada
        """
        # Extrae canales de forma independiente
        b_ex, g_ex, r_ex = self.picture[:, :, 0], self.picture[:, :, 1], self.picture[:, :, 2]

        r_val = r_ex[y][x]
        g_val = g_ex[y][x]
        b_val = b_ex[y][x]

        # Conforma imagen rgb de 1px * 1px
        rgb = np.array([[[r_val, g_val, b_val]]])
        # Convierte el espacio de color H: 0 -> 179, S: 0 -> 255, V: -> 0 -> 255
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        # Extrae valores pixel a pixel
        h_val = hsv[0][0][0]
        s_val = hsv[0][0][1]
        v_val = hsv[0][0][2]

        return r_val, g_val, b_val, h_val, s_val, v_val

    @staticmethod
    def calculate_hsv_mask(image_hsv, h, s, v, tolerance):
        """
        Calcula la mascara hsv de un color especifico con la tolerancia especifica
        :param image_hsv:
        :param h:
        :param s:
        :param v:
        :param tolerance:
        :return:
        """
        # Calcula el delta porcentual
        h_percent = int(180 * tolerance / 100)
        s_percent = int(255 * tolerance / 100)
        v_percent = int(255 * tolerance / 100)

        # Establece limites
        h_high = h + h_percent
        h_low = h - h_percent
        s_high = Color.__prevent_saturation(s + s_percent, 0, 255)
        s_low = Color.__prevent_saturation(s - s_percent, 0, 255)
        v_high = Color.__prevent_saturation(v + v_percent, 0, 255)
        v_low = Color.__prevent_saturation(v - v_percent, 0, 255)

        # Para el caso particular de la h (circular en grados:)
        if h_low < 0:
            h_low = 180 - h_low

        if h_high > 179:
            h_high = h_high - 180

        mask = None

        if h_low <= h_high:
            # Conforma los arrays de los limites
            limit_1_low = np.array([h_low, s_low, v_low])
            limit_1_high = np.array([h_high, s_high, v_high])

            # Aplica los límites de los filtros para el color
            mask = cv2.inRange(image_hsv, limit_1_low, limit_1_high)

        else:
            limit_1_low = np.array([h_low, s_low, v_low])
            limit_1_high = np.array([179, s_high, v_high])

            limit_2_low = np.array([0, s_low, v_low])
            limit_2_high = np.array([h_high, s_high, v_high])

            # Aplica los límites de los filtros para el color
            mask1 = cv2.inRange(image_hsv, limit_1_low, limit_1_high)
            mask2 = cv2.inRange(image_hsv, limit_2_low, limit_2_high)
            # Unifica mascaras
            mask = cv2.add(mask1, mask2)

        return mask

    @staticmethod
    def __prevent_saturation(value, low_limit, high_limit):
        """
        Previene la sobre o sub saturación de un valor estableciendo un rango
        :param value:
        :param low_limit:
        :param high_limit:
        :return:
        """
        result = 0

        if value > high_limit:
            result = high_limit
        elif value < low_limit:
            result = low_limit
        else:
            result = value

        return result

    def capture_lines_color_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Extrae valores de pixel de la imagen
            r, g, b, h, s, v = self.get_pixel_values(x, y)
            # Visualiza el color extraído en el label
            ls_lbl_line_color = getattr(self.ui, f'ls_lbl_line_color_{self.widget_id}')
            ls_lbl_line_color.setStyleSheet(f"background: rgb({r}, {g}, {b} );\n""border: 1px solid black;")
            # Cambia espacio de color
            hsv = cv2.cvtColor(self.picture, cv2.COLOR_BGR2HSV)
            # Lee la tolerancia del slider
            ls_sld_line_tolerance = getattr(self.ui, f'ls_sld_line_tolerance_{self.widget_id}')
            tolerance = int(ls_sld_line_tolerance.value())
            # Calcula la mascara
            self.mask = self.calculate_hsv_mask(hsv, h, s, v, tolerance)
            # AND entre las dos mascaras
            res_hsv = cv2.bitwise_and(self.picture, self.picture, mask=self.mask)
            # Filtro de color de lineas
            cv2.imshow('Filtro de color de lineas aplicado...', res_hsv)

    def sld_tolerancia_linea_evt(self):
        # Actualiza el valor en el label de referencia
        ls_lbl_line_tolerance = getattr(self.ui, f'ls_lbl_line_tolerance_{self.widget_id}')
        ls_sld_line_tolerance = getattr(self.ui, f'ls_sld_line_tolerance_{self.widget_id}')
        ls_lbl_line_tolerance.setText(str(ls_sld_line_tolerance.value()) + " %")

    def clean(self):
        pass

    def get_picture_filtered(self):

        picture = Pic()
        picture.create_picture_from_content(cv2.bitwise_and(self.picture, self.picture, mask=self.mask))

        # Genera la capa filtrada con la mascara adecuada
        return picture
