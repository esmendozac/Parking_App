import cv2
import numpy as np
import copy
from enum import Enum
from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtWidgets, QtGui
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class ColorActions(Enum):
    PickColor = 0


class Color(Filter):

    def __init__(self, picture, ui: Ui, row: int, col: int, widget_id: int):

        # Imagen original
        self._original_picture = None
        # Indica que el filtro fué finalizado
        self.is_done = False
        # Para extraer el color
        self.color = {'r': 255, 'g': 255, 'b': 255}
        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.draw_widget(row, col, widget_id)
        self.widget_id = widget_id
        self.mask = []

    def draw_widget_1(self, row: int, col: int, widget_id: int):
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

        ls_lbl_line_color.setStyleSheet(f"background: rgb({self.color['r']}, {self.color['g']}, {self.color['b']} );\n"
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

    def draw_widget(self, row: int, col: int, widget_id: int):

        setattr(self.ui, f'ml_frame_{widget_id}', QtWidgets.QFrame(self.ui.scrollAreaWidgetContents))
        ml_frame = getattr(self.ui, f'ml_frame_{widget_id}')
        ml_frame.setEnabled(True)
        ml_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        ml_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        ml_frame.setObjectName(f'ml_frame_{widget_id}')

        setattr(self.ui, f'ml_group_{widget_id}', QtWidgets.QGroupBox(ml_frame))
        ml_group = getattr(self.ui, f'ml_group_{widget_id}')
        ml_group.setGeometry(QtCore.QRect(10, 130, 391, 211))
        ml_group.setObjectName(f'ml_group_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_h_min_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_color_h_min = getattr(self.ui, f'ml_lbl_color_h_min_{widget_id}')
        ml_lbl_color_h_min.setGeometry(QtCore.QRect(110, 110, 31, 16))
        ml_lbl_color_h_min.setObjectName(f'ml_lbl_color_h_min_{widget_id}')

        setattr(self.ui, f'ml_sld_color_s_min_{widget_id}', QtWidgets.QSlider(ml_group))
        ml_sld_color_s_min = getattr(self.ui, f'ml_sld_color_s_min_{widget_id}')
        ml_sld_color_s_min.setGeometry(QtCore.QRect(40, 130, 161, 22))
        ml_sld_color_s_min.setMinimum(0)
        ml_sld_color_s_min.setMaximum(255)
        ml_sld_color_s_min.setPageStep(1)
        ml_sld_color_s_min.setSliderPosition(11)
        ml_sld_color_s_min.setTracking(False)
        ml_sld_color_s_min.setOrientation(QtCore.Qt.Horizontal)
        ml_sld_color_s_min.setObjectName(f'ml_sld_color_s_min_{widget_id}')

        setattr(self.ui, f'ml_sld_color_v_min_{widget_id}', QtWidgets.QSlider(ml_group))
        ml_sld_color_v_min = getattr(self.ui, f'ml_sld_color_v_min_{widget_id}')
        ml_sld_color_v_min.setGeometry(QtCore.QRect(40, 170, 161, 22))
        ml_sld_color_v_min.setMinimum(0)
        ml_sld_color_v_min.setMaximum(255)
        ml_sld_color_v_min.setPageStep(1)
        ml_sld_color_v_min.setSliderPosition(11)
        ml_sld_color_v_min.setTracking(False)
        ml_sld_color_v_min.setOrientation(QtCore.Qt.Horizontal)
        ml_sld_color_v_min.setObjectName(f'ml_sld_color_v_min_{widget_id}')

        setattr(self.ui, f'ml_sld_color_s_max_{widget_id}', QtWidgets.QSlider(ml_group))
        ml_sld_color_s_max = getattr(self.ui, f'ml_sld_color_s_max_{widget_id}')
        ml_sld_color_s_max.setGeometry(QtCore.QRect(220, 130, 161, 22))
        ml_sld_color_s_max.setMinimum(0)
        ml_sld_color_s_max.setMaximum(255)
        ml_sld_color_s_max.setPageStep(1)
        ml_sld_color_s_max.setSliderPosition(11)
        ml_sld_color_s_max.setTracking(False)
        ml_sld_color_s_max.setOrientation(QtCore.Qt.Horizontal)
        ml_sld_color_s_max.setObjectName(f'ml_sld_color_s_max_{widget_id}')

        setattr(self.ui, f'ml_sld_color_v_max_{widget_id}', QtWidgets.QSlider(ml_group))
        ml_sld_color_v_max = getattr(self.ui, f'ml_sld_color_v_max_{widget_id}')
        ml_sld_color_v_max.setGeometry(QtCore.QRect(220, 170, 161, 22))
        ml_sld_color_v_max.setMinimum(0)
        ml_sld_color_v_max.setMaximum(255)
        ml_sld_color_v_max.setPageStep(1)
        ml_sld_color_v_max.setSliderPosition(11)
        ml_sld_color_v_max.setTracking(False)
        ml_sld_color_v_max.setOrientation(QtCore.Qt.Horizontal)
        ml_sld_color_v_max.setObjectName(f'ml_sld_color_v_max_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_h_max_{widget_id}',QtWidgets.QLabel(ml_group))
        ml_lbl_color_h_max = getattr(self.ui, f'ml_lbl_color_h_max_{widget_id}')
        ml_lbl_color_h_max.setGeometry(QtCore.QRect(290, 110, 31, 16))
        ml_lbl_color_h_max.setObjectName(f'ml_lbl_color_h_max_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_s_min_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_color_s_min = getattr(self.ui, f'ml_lbl_color_s_min_{widget_id}')
        ml_lbl_color_s_min.setGeometry(QtCore.QRect(110, 150, 31, 16))
        ml_lbl_color_s_min.setObjectName(f'ml_lbl_color_s_min_{widget_id}')

        setattr(self.ui, f'ml_lbl_s_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_s = getattr(self.ui, f'ml_lbl_s_{widget_id}')
        ml_lbl_s.setGeometry(QtCore.QRect(10, 130, 31, 16))
        ml_lbl_s.setObjectName(f'ml_lbl_s_{widget_id}')

        setattr(self.ui, f'ml_lbl_v_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_v = getattr(self.ui, f'ml_lbl_v_{widget_id}')
        ml_lbl_v.setGeometry(QtCore.QRect(10, 170, 31, 16))
        ml_lbl_v.setObjectName(f'ml_lbl_v_{widget_id}')

        setattr(self.ui, f'ml_lbl_h_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_h = getattr(self.ui, f'ml_lbl_h_{widget_id}')
        ml_lbl_h.setGeometry(QtCore.QRect(10, 90, 31, 16))
        ml_lbl_h.setObjectName(f'ml_lbl_h_{widget_id}')

        setattr(self.ui, f'ml_sld_color_h_min_{widget_id}', QtWidgets.QSlider(ml_group))
        ml_sld_color_h_min = getattr(self.ui, f'ml_sld_color_h_min_{widget_id}')
        ml_sld_color_h_min.setGeometry(QtCore.QRect(40, 90, 161, 22))
        ml_sld_color_h_min.setMinimum(0)
        ml_sld_color_h_min.setMaximum(179)
        ml_sld_color_h_min.setPageStep(1)
        ml_sld_color_h_min.setSliderPosition(90)
        ml_sld_color_h_min.setTracking(False)
        ml_sld_color_h_min.setOrientation(QtCore.Qt.Horizontal)
        ml_sld_color_h_min.setObjectName(f'ml_sld_color_h_min_{widget_id}')

        setattr(self.ui, f'ml_sld_color_h_max_{widget_id}', QtWidgets.QSlider(ml_group))
        ml_sld_color_h_max = getattr(self.ui, f'ml_sld_color_h_max_{widget_id}')
        ml_sld_color_h_max.setGeometry(QtCore.QRect(220, 90, 161, 22))
        ml_sld_color_h_max.setMinimum(0)
        ml_sld_color_h_max.setMaximum(179)
        ml_sld_color_h_max.setPageStep(1)
        ml_sld_color_h_max.setSliderPosition(90)
        ml_sld_color_h_max.setTracking(False)
        ml_sld_color_h_max.setOrientation(QtCore.Qt.Horizontal)
        ml_sld_color_h_max.setObjectName(f'ml_sld_color_h_max_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_v_min_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_color_v_min = getattr(self.ui, f'ml_lbl_color_v_min_{widget_id}')
        ml_lbl_color_v_min.setGeometry(QtCore.QRect(110, 190, 31, 16))
        ml_lbl_color_v_min.setObjectName(f'ml_lbl_color_v_min_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_s_max_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_color_s_max = getattr(self.ui, f'ml_lbl_color_s_max_{widget_id}')
        ml_lbl_color_s_max.setGeometry(QtCore.QRect(290, 150, 31, 16))
        ml_lbl_color_s_max.setObjectName(f'ml_lbl_color_s_max_{widget_id}')

        setattr(self.ui, f'ml_btn_color_{widget_id}', QtWidgets.QPushButton(ml_group))
        ml_btn_color = getattr(self.ui, f'ml_btn_color_{widget_id}')
        ml_btn_color.setGeometry(QtCore.QRect(10, 20, 40, 40))
        ml_btn_color.setMinimumSize(QtCore.QSize(40, 40))
        ml_btn_color.setMaximumSize(QtCore.QSize(40, 40))
        ml_btn_color.setStyleSheet("border-color: rgb(255, 85, 0);")
        ml_btn_color.setText("")
        icon_ml_btn_color = QtGui.QIcon()
        icon_ml_btn_color.addPixmap(QtGui.QPixmap("icons/color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ml_btn_color.setIcon(icon_ml_btn_color)
        ml_btn_color.setIconSize(QtCore.QSize(32, 32))
        ml_btn_color.setObjectName(f'ml_btn_color_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_{widget_id}',QtWidgets.QLabel(ml_group))
        ml_lbl_color = getattr(self.ui, f'ml_lbl_color_{widget_id}')
        ml_lbl_color.setGeometry(QtCore.QRect(50, 20, 38, 38))
        ml_lbl_color.setMinimumSize(QtCore.QSize(38, 38))
        ml_lbl_color.setMaximumSize(QtCore.QSize(38, 38))
        ml_lbl_color.setAutoFillBackground(False)
        ml_lbl_color.setStyleSheet("background: rgb(255, 255, 255);\n"
                                        "border: 1px solid gray;")
        ml_lbl_color.setText("")
        ml_lbl_color.setObjectName(f'ml_lbl_color_{widget_id}')

        setattr(self.ui, f'ml_btn_view_{widget_id}', QtWidgets.QPushButton(ml_group))
        ml_btn_view = getattr(self.ui, f'ml_btn_view_{widget_id}')
        ml_btn_view.setGeometry(QtCore.QRect(260, 20, 40, 40))
        ml_btn_view.setMinimumSize(QtCore.QSize(40, 40))
        ml_btn_view.setMaximumSize(QtCore.QSize(40, 40))
        ml_btn_view.setStyleSheet("border-color: rgb(255, 85, 0);")
        ml_btn_view.setText("")
        icon_ml_btn_view = QtGui.QIcon()
        icon_ml_btn_view.addPixmap(QtGui.QPixmap("icons/ver.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ml_btn_view.setIcon(icon_ml_btn_view)
        ml_btn_view.setIconSize(QtCore.QSize(32, 32))
        ml_btn_view.setObjectName(f'ml_btn_view_{widget_id}')

        setattr(self.ui, f'ml_btn_clear_{widget_id}', QtWidgets.QPushButton(ml_group))
        ml_btn_clear = getattr(self.ui, f'ml_btn_clear_{widget_id}')
        ml_btn_clear.setGeometry(QtCore.QRect(300, 20, 40, 40))
        ml_btn_clear.setMinimumSize(QtCore.QSize(40, 40))
        ml_btn_clear.setMaximumSize(QtCore.QSize(40, 40))
        ml_btn_clear.setText("")
        icon_ml_btn_clear = QtGui.QIcon()
        icon_ml_btn_clear.addPixmap(QtGui.QPixmap("icons/limpiar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ml_btn_clear.setIcon(icon_ml_btn_clear)
        ml_btn_clear.setIconSize(QtCore.QSize(32, 32))
        ml_btn_clear.setObjectName(f'ml_btn_clear_{widget_id}')

        setattr(self.ui, f'ml_lbl_min_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_min = getattr(self.ui, f'ml_lbl_min_{widget_id}')
        ml_lbl_min.setGeometry(QtCore.QRect(40, 70, 31, 16))
        ml_lbl_min.setObjectName(f'ml_lbl_min_{widget_id}')

        setattr(self.ui, f'ml_lbl_max_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_max = getattr(self.ui, f'ml_lbl_max_{widget_id}')
        ml_lbl_max.setGeometry(QtCore.QRect(220, 70, 31, 16))
        ml_lbl_max.setObjectName(f'ml_lbl_max_{widget_id}')

        setattr(self.ui, f'ml_btn_delete_{widget_id}', QtWidgets.QPushButton(ml_group))
        ml_btn_delete = getattr(self.ui, f'ml_btn_delete_{widget_id}')
        ml_btn_delete.setGeometry(QtCore.QRect(340, 20, 40, 40))
        ml_btn_delete.setMinimumSize(QtCore.QSize(40, 40))
        ml_btn_delete.setMaximumSize(QtCore.QSize(40, 40))
        ml_btn_delete.setText("")
        icon_ml_btn_delete = QtGui.QIcon()
        icon_ml_btn_delete.addPixmap(QtGui.QPixmap("icons/eliminar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ml_btn_delete.setIcon(icon_ml_btn_delete)
        ml_btn_delete.setIconSize(QtCore.QSize(32, 32))
        ml_btn_delete.setObjectName(f'ml_btn_delete_{widget_id}')

        setattr(self.ui, f'ml_lbl_color_v_max_{widget_id}', QtWidgets.QLabel(ml_group))
        ml_lbl_color_v_max = getattr(self.ui, f'ml_lbl_color_v_max_{widget_id}')
        ml_lbl_color_v_max.setGeometry(QtCore.QRect(290, 190, 31, 16))
        ml_lbl_color_v_max.setObjectName(f'ml_lbl_color_v_max_{widget_id}')

        _translate = QtCore.QCoreApplication.translate
        ml_group.setTitle(_translate("MainWindow", "Mascara de lineas"))
        ml_lbl_color_h_min.setText(_translate("MainWindow", "11 %"))
        ml_lbl_color_h_max.setText(_translate("MainWindow", "11 %"))
        ml_lbl_color_s_min.setText(_translate("MainWindow", "11 %"))
        ml_lbl_s.setText(_translate("MainWindow", "S"))
        ml_lbl_v.setText(_translate("MainWindow", "V"))
        ml_lbl_h.setText(_translate("MainWindow", "H"))
        ml_lbl_color_v_min.setText(_translate("MainWindow", "11 %"))
        ml_lbl_color_s_max.setText(_translate("MainWindow", "11 %"))
        ml_btn_color.setToolTip(_translate("MainWindow", "<html><head/><body><p>Dibujar linea</p></body></html>"))
        ml_btn_color.setWhatsThis(
            _translate("MainWindow", "<html><head/><body><p>Dibujar linea</p></body></html>"))
        ml_btn_view.setToolTip(_translate("MainWindow", "<html><head/><body><p>Dibujar linea</p></body></html>"))
        ml_btn_view.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Dibujar linea</p></body></html>"))
        ml_btn_clear.setToolTip(_translate("MainWindow", "<html><head/><body><p>Limpiar</p></body></html>"))
        ml_lbl_min.setText(_translate("MainWindow", "Min"))
        ml_lbl_max.setText(_translate("MainWindow", "Max"))
        ml_btn_delete.setToolTip(_translate("MainWindow", "<html><head/><body><p>Limpiar</p></body></html>"))
        ml_lbl_color_v_max.setText(_translate("MainWindow", "11 %"))

        self.ui.gridLayout.addWidget(ml_frame, row, col, 1, 1)

        # Conexiones
        ml_btn_color.clicked.connect(lambda callback: self.capture_lines_color())

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

    def calculate_hsv_mask(self, image_hsv, h, s, v, tolerance):
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

        # Asigna valores a los sliders
        ml_sld_color_h_max = getattr(self.ui, f'ml_sld_color_h_max_{self.widget_id}')
        ml_sld_color_h_max.setValue(h_high)
        ml_sld_color_h_min = getattr(self.ui, f'ml_sld_color_h_min_{self.widget_id}')
        ml_sld_color_h_min.setValue(h_low)
        ml_lbl_color_h_max = getattr(self.ui, f'ml_lbl_color_h_max_{self.widget_id}')
        ml_lbl_color_h_max.setText(str(h_high))
        ml_lbl_color_h_min = getattr(self.ui, f'ml_lbl_color_h_min_{self.widget_id}')
        ml_lbl_color_h_min.setText(str(h_low))

        ml_sld_color_s_max = getattr(self.ui, f'ml_sld_color_s_max_{self.widget_id}')
        ml_sld_color_s_max.setValue(s_high)
        ml_sld_color_s_min = getattr(self.ui, f'ml_sld_color_s_min_{self.widget_id}')
        ml_sld_color_s_min.setValue(s_low)
        ml_lbl_color_s_max = getattr(self.ui, f'ml_lbl_color_s_max_{self.widget_id}')
        ml_lbl_color_s_max.setText(str(s_high))
        ml_lbl_color_s_min = getattr(self.ui, f'ml_lbl_color_s_min_{self.widget_id}')
        ml_lbl_color_s_min.setText(str(s_low))

        ml_sld_color_v_max = getattr(self.ui, f'ml_sld_color_v_max_{self.widget_id}')
        ml_sld_color_v_max.setValue(v_high)
        ml_sld_color_v_min = getattr(self.ui, f'ml_sld_color_v_min_{self.widget_id}')
        ml_sld_color_v_min.setValue(v_low)
        ml_lbl_color_v_max = getattr(self.ui, f'ml_lbl_color_v_max_{self.widget_id}')
        ml_lbl_color_v_max.setText(str(v_high))
        ml_lbl_color_v_min = getattr(self.ui, f'ml_lbl_color_v_min_{self.widget_id}')
        ml_lbl_color_v_min.setText(str(v_low))

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
            # Actualiza el color
            self.color['r'] = r
            self.color['g'] = g
            self.color['b'] = b
            # Visualiza el color extraído en el label
            ml_lbl_color = getattr(self.ui, f'ml_lbl_color_{self.widget_id}')
            ml_lbl_color.setStyleSheet(f"background: rgb({r}, {g}, {b} );\n""border: 1px solid black;")
            # Cambia espacio de color
            hsv = cv2.cvtColor(self.picture, cv2.COLOR_BGR2HSV)
            # Lee la tolerancia del slider
            # ls_sld_line_tolerance = getattr(self.ui, f'ls_sld_line_tolerance_{self.widget_id}')
            # tolerance = int(ls_sld_line_tolerance.value())
            tolerance = 10
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

    def get_selected_color(self):
        """
        Para obtener el color rgb seleccionado
        :return:
        """
        return self.color

