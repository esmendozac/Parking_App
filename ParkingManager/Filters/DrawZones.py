import cv2
import numpy as np
import copy
from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtWidgets
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class DrawZones(Filter):
    """
    Filtro que permite elegir específicamente zonas de una imagen para delimitar un estacionamiento
    """
    ui: Ui

    def __init__(self, picture: Pic, ui: Ui, row: int, col: int, widget_id: int, color_selected=None):

        # Imagen original
        self._original_picture = None
        # Coordenadas de limites útiles en la imagen
        self.limits = [[]]
        # Mascaras de limites
        self.masks = []
        # Indica que el filtro fué finalizado
        self.is_done = False
        # Hereda el color de linea de un filtro anterior
        self.color = {'r': 255, 'g': 255, 'b': 255}

        if color_selected is not None:
            self.color = color_selected

        print(self.color)

        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.draw_widget(row, col, widget_id)
        self.widget_id = widget_id

    def draw_widget(self, row: int, col: int, widget_id: int):
        """
        Renderiza el widget del filtro en la pantalla
        :param row:
        :param col:
        :param widget_id:
        :return:
        """
        # Tiempo de ejecución
        setattr(self.ui, f'dz_frame_{widget_id}', QtWidgets.QFrame(self.ui.scrollAreaWidgetContents))
        frame = getattr(self.ui, f'dz_frame_{widget_id}')
        frame.setMinimumSize(QtCore.QSize(400, 80))
        frame.setMaximumSize(QtCore.QSize(400, 100))
        frame.setStyleSheet("")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName(f'dz_frame_{widget_id}')

        setattr(self.ui, f'dz_grb_draw_zones_{widget_id}', QtWidgets.QGroupBox(frame))
        dz_grb_draw_zones = getattr(self.ui, f'dz_grb_draw_zones_{widget_id}')
        dz_grb_draw_zones.setGeometry(QtCore.QRect(0, 0, 391, 101))
        dz_grb_draw_zones.setObjectName(f'dz_grb_draw_zones_{widget_id}')

        setattr(self.ui, f'dz_btn_draw_zone_{widget_id}', QtWidgets.QPushButton(dz_grb_draw_zones))
        dz_btn_draw_zone = getattr(self.ui, f'dz_btn_draw_zone_{widget_id}')
        dz_btn_draw_zone.setGeometry(QtCore.QRect(30, 20, 91, 23))
        dz_btn_draw_zone.setObjectName(f'dz_btn_draw_zone_{widget_id}')

        setattr(self.ui, f'dz_lbl_draw_zone_{widget_id}', QtWidgets.QLabel(dz_grb_draw_zones))
        dz_lbl_draw_zone = getattr(self.ui, f'dz_lbl_draw_zone_{widget_id}')
        dz_lbl_draw_zone.setGeometry(QtCore.QRect(10, 20, 16, 21))
        dz_lbl_draw_zone.setAutoFillBackground(False)
        dz_lbl_draw_zone.setStyleSheet(f"background: rgb({self.color['r']}, {self.color['g']}, "
                                       f"{self.color['b']});\n""border: 1px solid black;")
        dz_lbl_draw_zone.setText("")
        dz_lbl_draw_zone.setObjectName(f'dz_lbl_draw_zone_{widget_id}')

        setattr(self.ui, f'dz_btn_clean_{widget_id}', QtWidgets.QPushButton(dz_grb_draw_zones))
        dz_btn_clean = getattr(self.ui, f'dz_btn_clean_{widget_id}')
        dz_btn_clean.setGeometry(QtCore.QRect(30, 50, 91, 23))
        dz_btn_clean.setObjectName(f'dz_btn_clean_{widget_id}')

        setattr(self.ui, f'dz_btn_view_zone_{widget_id}', QtWidgets.QPushButton(dz_grb_draw_zones))
        dz_btn_view_zone = getattr(self.ui, f'dz_btn_view_zone_{widget_id}')
        dz_btn_view_zone.setGeometry(QtCore.QRect(150, 20, 81, 23))
        dz_btn_view_zone.setObjectName(f'dz_btn_view_zone_{widget_id}')

        setattr(self.ui, f'dz_btn_delete_{widget_id}', QtWidgets.QPushButton(dz_grb_draw_zones))
        dz_btn_delete = getattr(self.ui, f'dz_btn_delete_{widget_id}')
        dz_btn_delete.setGeometry(QtCore.QRect(150, 50, 81, 23))
        dz_btn_delete.setObjectName(f'dz_btn_delete_{widget_id}')

        setattr(self.ui, f'dz_cbx_executed_{widget_id}', QtWidgets.QCheckBox(dz_grb_draw_zones))
        dz_cbx_executed = getattr(self.ui, f'dz_cbx_executed_{widget_id}')
        dz_cbx_executed.setGeometry(QtCore.QRect(310, 10, 70, 17))
        dz_cbx_executed.setObjectName(f'dz_cbx_executed_{widget_id}')

        self.ui.gridLayout.addWidget(frame, row, col, 1, 1)

        _translate = QtCore.QCoreApplication.translate

        dz_grb_draw_zones.setTitle(_translate("MainWindow", "Dibujar zonas"))
        dz_btn_draw_zone.setText(_translate("MainWindow", "Dibujar"))
        dz_btn_clean.setText(_translate("MainWindow", "Limpiar"))
        dz_btn_view_zone.setText(_translate("MainWindow", "Ver"))
        dz_btn_delete.setText(_translate("MainWindow", "Eliminar"))
        dz_cbx_executed.setText(_translate("MainWindow", "Ejecutado"))

        # Conexiones
        dz_btn_draw_zone.clicked.connect(self.draw_zone)
        dz_btn_view_zone.clicked.connect(self.view_zones)
        dz_btn_clean.clicked.connect(self.clean)

        # Valores iniciales
        dz_cbx_executed.setDisabled(True)

        self.set_ext_btn_state(False)

    def draw_zone(self):
        """
        Carga imagen del sistema de archivos
        :return:
        """
        try:
            cv2.imshow(f'{self.widget_id}_Dibujando imagen...', self.picture)
            # Callback de eventos de mouse
            cv2.setMouseCallback(f'{self.widget_id}_Dibujando imagen...', self.draw_points_callback)
        except Exception as ex:
            raise Exception(ex)

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
            self.add_limit_coordinate(x, y, is_last=False)
            cv2.circle(self.picture, (x, y), 3, (int(self.color['r']), int(self.color['g']), int(self.color['b'])), -1)
            # Actualiza la imagen mostrada
            cv2.imshow(f'{self.widget_id}_Dibujando imagen...', self.picture)

        # control + click añade una nueva zona delimitada
        elif event == cv2.EVENT_MBUTTONDBLCLK:

            # Crea una zona delimitada
            if len(self.limits[-1]) > 3:
                # Extrae los contornos
                contours = np.array([self.limits[-1]])
                # Cierra el contorno
                self.add_close_last_limit()
                # Crear una mascara genérica del mismo tamaño de la imagen
                mask = np.zeros(shape=(self.picture.shape[:2]), dtype=np.uint8)
                # Itera por los contornos y crea la mascara
                mask = cv2.drawContours(mask, contours, -1, 255, -1)
                # Almacena la mascara en la imagen
                self.masks.append(mask)

                # Dibuja el contorno en la imagen original
                cv2.drawContours(self.picture, contours, -1,
                                 (int(self.color['r']), int(self.color['g']), int(self.color['b'])), 2)
                # Muestra el contorno
                cv2.imshow(f'{self.widget_id}_Dibujando imagen...', self.picture)

    def view_zones(self):
        """
        Visualiza el resultado del filtro
        :return:
        """
        cv2.imshow(f'{self.widget_id}_Zonas delimitadas', self.get_picture_filtered().content)

        # Bloquea edición del filtro
        getattr(self.ui, f'dz_btn_draw_zone_{self.widget_id}').setDisabled(True)
        getattr(self.ui, f'dz_cbx_executed_{self.widget_id}').setCheckState(QtCore.Qt.Checked)
        self.is_done = True
        self.set_ext_btn_state(True)

    def clean(self):
        """
        Limpieza de las zonas en el objeto imagen y en la interfaz gráfica
        :return:
        """
        self.limits = [[]]
        self.masks = []
        self.picture = self.get_original_picture()

    def add_limit_coordinate(self, x, y, is_last):

        """
        Añade grupos de coordenadas a los límites definidos en la imagen
        :param x: coordenada x
        :param y: coordenada y
        :param is_last: si la coordenada cierra la figura se debe indicar
        :return: void
        """
        # Extrae el indice para insertar los registros
        index = len(self.limits) - 1
        # Añade las coordenadas en los límites
        self.limits[index].append([x, y])

    def get_all_masks_limits(self):

        """
        Retorna todas las mascaras unificadas para concatenar con la imagen real
        :return: mask
        """
        # Crear una mascara genérica del mismo tamaño de la imagen
        mask = np.zeros(shape=(self.picture.shape[:2]), dtype=np.uint8)

        # Itera y concatena las mascaras
        for m in self.masks:
            mask = cv2.bitwise_or(m, mask)

        return mask

    def add_close_last_limit(self):

        """
        Cierra la ultima coordenada
        :return:
        """

        self.limits.append([])

    def get_picture_filtered(self):
        """
        Genera el resultado del filtro aplicado
        :return:
        """
        mask = self.get_all_masks_limits()

        picture = Pic()
        image_with_contours = cv2.bitwise_and(self.get_original_picture(), self.get_original_picture(), mask=mask)

        for limit in filter(lambda c: len(c) > 0, self.limits):
            contours = np.array([limit])
            # Dibuja el contorno en la imagen original
            cv2.drawContours(image_with_contours, contours, -1,
                             (int(self.color['r']), int(self.color['g']), int(self.color['b'])), 2)

        picture.create_picture_from_content(image_with_contours)

        # Genera la capa filtrada con la mascara adecuada
        return picture

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)

    def empty_callback(self):
        """
        Función vacía para inhabilitar el callback
        :param self:
        :return:
        """
        pass

    def set_ext_btn_state(self, state: bool):
        """
        Permite configurar el estado de los botones que crean filtros (Lógica normal)
        :param state:
        :return:
        """
        self.ui.btn_draw_zones.setDisabled(not state)
        self.ui.btn_color_lines.setDisabled(not state)
