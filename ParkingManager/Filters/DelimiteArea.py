import cv2
import numpy as np
import copy
from enum import Enum
from Models import Utils

from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtWidgets, QtGui
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class DActions(Enum):
    Line = 0,
    Coordinates = 1,
    Eraser = 2,
    ColorPick = 3


class DelimiteArea(Filter):
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
        # Acción por defecto
        self.action = None
        # Ultimo evento de mouse
        self.last_mouse_event = None

        # Hereda color de una capa externa
        if color_selected is not None:
            self.color = color_selected

        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.draw_widget(row, col, widget_id)
        self.widget_id = widget_id

        self.open_image()

        # Lineas
        self.line_coordinates = [None, None]

    def draw_widget(self, row: int, col: int, widget_id: int):
        """
        Renderiza el widget del filtro en la pantalla
        :param row:
        :param col:
        :param widget_id:
        :return:
        """

        setattr(self.ui, f'da_frame_{widget_id}', QtWidgets.QFrame(self.ui.scrollAreaWidgetContents))
        frame = getattr(self.ui, f'da_frame_{widget_id}')
        frame.setMinimumSize(QtCore.QSize(400, 80))
        frame.setMaximumSize(QtCore.QSize(400, 100))
        frame.setStyleSheet("")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName(f'da_frame_{widget_id}')

        setattr(self.ui, f'da_grb_draw_zones_{widget_id}', QtWidgets.QGroupBox(frame))
        da_grb_draw_zones = getattr(self.ui, f'da_grb_draw_zones_{widget_id}')
        da_grb_draw_zones.setGeometry(QtCore.QRect(0, 0, 391, 101))
        da_grb_draw_zones.setObjectName(f'da_grb_draw_zones_{widget_id}')

        setattr(self.ui, f'da_lbl_color_{widget_id}', QtWidgets.QLabel(da_grb_draw_zones))
        da_lbl_color = getattr(self.ui, f'da_lbl_color_{widget_id}')
        da_lbl_color.setGeometry(QtCore.QRect(170, 30, 40, 40))
        da_lbl_color.setMinimumSize(QtCore.QSize(40, 40))
        da_lbl_color.setMaximumSize(QtCore.QSize(40, 40))
        da_lbl_color.setAutoFillBackground(False)
        da_lbl_color.setStyleSheet(f"background: rgb({self.color['r']}, {self.color['g']}, "
                                   f"{self.color['b']});\n""border: 1px solid gray;")
        da_lbl_color.setText("")
        da_lbl_color.setObjectName(f'da_lbl_color_{widget_id}')

        setattr(self.ui, f'da_btn_clean_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_clean = getattr(self.ui, f'da_btn_clean_{widget_id}')
        da_btn_clean.setGeometry(QtCore.QRect(300, 30, 40, 40))
        da_btn_clean.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_clean.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_clean.setText("")
        icon_btn_clean = QtGui.QIcon()
        icon_btn_clean.addPixmap(QtGui.QPixmap("icons/limpiar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_clean.setIcon(icon_btn_clean)
        da_btn_clean.setIconSize(QtCore.QSize(32, 32))
        da_btn_clean.setObjectName(f'da_btn_clean_{widget_id}')

        setattr(self.ui, f'da_btn_delete_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_delete = getattr(self.ui, f'da_btn_delete_{widget_id}')
        da_btn_delete.setGeometry(QtCore.QRect(340, 30, 40, 40))
        da_btn_delete.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_delete.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_delete.setText("")
        icon_da_btn_delete = QtGui.QIcon()
        icon_da_btn_delete.addPixmap(QtGui.QPixmap("icons/eliminar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_delete.setIcon(icon_da_btn_delete)
        da_btn_delete.setIconSize(QtCore.QSize(32, 32))
        da_btn_delete.setObjectName(f'da_btn_delete_{widget_id}')

        setattr(self.ui, f'da_btn_coordinates_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_coordinates = getattr(self.ui, f'da_btn_coordinates_{widget_id}')
        da_btn_coordinates.setGeometry(QtCore.QRect(50, 30, 40, 40))
        da_btn_coordinates.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_coordinates.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_coordinates.setStyleSheet("border-color: rgb(255, 85, 0);")
        da_btn_coordinates.setText("")
        icon_da_btn_coordinates = QtGui.QIcon()
        icon_da_btn_coordinates.addPixmap(QtGui.QPixmap("icons/coordenadas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_coordinates.setIcon(icon_da_btn_coordinates)
        da_btn_coordinates.setIconSize(QtCore.QSize(36, 36))
        da_btn_coordinates.setObjectName(f'da_btn_coordinates_{widget_id}')

        setattr(self.ui, f'da_cbx_executed_{widget_id}', QtWidgets.QCheckBox(da_grb_draw_zones))
        da_cbx_executed = getattr(self.ui, f'da_cbx_executed_{widget_id}')
        da_cbx_executed.setGeometry(QtCore.QRect(260, 80, 70, 17))
        da_cbx_executed.setObjectName(f'da_cbx_executed_{widget_id}')

        setattr(self.ui, f'da_btn_lines_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_lines = getattr(self.ui, f'da_btn_lines_{widget_id}')
        da_btn_lines.setGeometry(QtCore.QRect(10, 30, 40, 40))
        da_btn_lines.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_lines.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_lines.setStyleSheet("border-color: rgb(255, 85, 0);")
        da_btn_lines.setText("")
        icon_da_btn_lines = QtGui.QIcon()
        icon_da_btn_lines.addPixmap(QtGui.QPixmap("icons/lineas.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_lines.setIcon(icon_da_btn_lines)
        da_btn_lines.setIconSize(QtCore.QSize(32, 32))
        da_btn_lines.setObjectName(f'da_btn_lines_{widget_id}')

        setattr(self.ui, f'da_btn_eraser_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_eraser = getattr(self.ui, f'da_btn_eraser_{widget_id}')
        da_btn_eraser.setGeometry(QtCore.QRect(90, 30, 40, 40))
        da_btn_eraser.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_eraser.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_eraser.setStyleSheet("border-color: rgb(255, 85, 0);")
        da_btn_eraser.setText("")
        icon_da_btn_eraser = QtGui.QIcon()
        icon_da_btn_eraser.addPixmap(QtGui.QPixmap("icons/borrador.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_eraser.setIcon(icon_da_btn_eraser)
        da_btn_eraser.setIconSize(QtCore.QSize(36, 36))
        da_btn_eraser.setObjectName(f'da_btn_eraser_{widget_id}')

        setattr(self.ui, f'da_btn_color_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_color = getattr(self.ui, f'da_btn_color_{widget_id}')
        da_btn_color.setGeometry(QtCore.QRect(130, 30, 40, 40))
        da_btn_color.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_color.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_color.setStyleSheet("border-color: rgb(255, 85, 0);")
        da_btn_color.setText("")
        icon_btn_color = QtGui.QIcon()
        icon_btn_color.addPixmap(QtGui.QPixmap("icons/color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_color.setIcon(icon_btn_color)
        da_btn_color.setIconSize(QtCore.QSize(32, 32))
        da_btn_color.setObjectName(f'da_btn_color_{widget_id}')

        setattr(self.ui, f'da_btn_view_{widget_id}', QtWidgets.QPushButton(da_grb_draw_zones))
        da_btn_view = getattr(self.ui, f'da_btn_view_{widget_id}')
        da_btn_view.setGeometry(QtCore.QRect(260, 30, 40, 40))
        da_btn_view.setMinimumSize(QtCore.QSize(40, 40))
        da_btn_view.setMaximumSize(QtCore.QSize(40, 40))
        da_btn_view.setText("")
        icon_da_btn_view = QtGui.QIcon()
        icon_da_btn_view.addPixmap(QtGui.QPixmap("icons/ver.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        da_btn_view.setIcon(icon_da_btn_view)
        da_btn_view.setIconSize(QtCore.QSize(32, 32))
        da_btn_view.setObjectName(f'da_btn_view_{widget_id}')

        self.ui.gridLayout.addWidget(frame, row, col, 1, 1)

        _translate = QtCore.QCoreApplication.translate

        da_grb_draw_zones.setTitle(_translate("MainWindow", "Delimitación de areas"))
        da_cbx_executed.setText(_translate("MainWindow", "Ejecutado"))

        # Conexiones
        da_btn_view.clicked.connect(self.open_image)

        da_btn_lines.clicked.connect(lambda callback: self.set_action_button(DActions.Line))
        da_btn_coordinates.clicked.connect(lambda callback: self.set_action_button(DActions.Coordinates))
        da_btn_eraser.clicked.connect(lambda callback: self.set_action_button(DActions.Eraser))
        da_btn_color.clicked.connect(lambda callback: self.set_action_button(DActions.ColorPick))

        # dz_btn_draw_zone.clicked.connect(self.draw_zone)
        # dz_btn_view_zone.clicked.connect(self.view_zones)
        # dz_btn_clean.clicked.connect(self.clean)
        #
        # # Valores iniciales
        # dz_cbx_executed.setDisabled(True)
        #
        # self.set_ext_btn_state(False)

    def open_image(self):
        """
        Abre la imagen lista para dibujar
        :return:
        """
        try:
            cv2.imshow(f'{self.widget_id}_Dibujando imagen...', self.picture)
            # Callback de eventos de mouse
            cv2.setMouseCallback(f'{self.widget_id}_Dibujando imagen...', self.mouse_callback)
        except Exception as ex:
            raise Exception(ex)

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

    def mouse_callback(self, event, x, y, flags, param):
        """
        Callback para eventos mouse encargado de gestionar el dibujo de formas
        :param event:
        :param x:
        :param y:
        :param flags:
        :param param:
        :return:
        """
        # Dependiendo de la action:
        if self.action == DActions.Line:

            # Inicia el ciclo y almacena el valor
            if event == cv2.EVENT_LBUTTONDOWN:
                self.last_mouse_event = cv2.EVENT_LBUTTONDOWN
                self.line_coordinates[0] = [x, y]

            # Previo un down click dibuja
            elif event == cv2.EVENT_MOUSEMOVE and self.last_mouse_event == cv2.EVENT_LBUTTONDOWN:

                # Saca una copia de la imagen
                picture = copy.deepcopy(self.picture)

                cv2.line(picture, (self.line_coordinates[0][0], self.line_coordinates[0][1]), (x, y),
                         (int(self.color['b']), int(self.color['g']), int(self.color['r'])), 3)
                cv2.imshow(f'{self.widget_id}_Dibujando imagen...', picture)

            # Libera el last event y el drag
            elif event == cv2.EVENT_LBUTTONUP:
                self.last_mouse_event = None
                cv2.line(self.picture, (self.line_coordinates[0][0], self.line_coordinates[0][1]), (x, y),
                         (int(self.color['b']), int(self.color['g']), int(self.color['r'])), 3)
                cv2.imshow(f'{self.widget_id}_Dibujando imagen...', self.picture)
                self.line_coordinates = [None, None]

        elif self.action == DActions.Coordinates:
            if event == cv2.EVENT_LBUTTONDOWN:
                # Cada punto dibujado es una coordenada almacenada y dibujada
                self.add_limit_coordinate(x, y, is_last=False)
                cv2.circle(self.picture, (x, y), 3, (int(self.color['b']), int(self.color['g']),int(self.color['r'])),
                           -1)
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
                                     (int(self.color['b']), int(self.color['g']),int(self.color['r'])), 2)
                    # Muestra el contorno
                    cv2.imshow(f'{self.widget_id}_Dibujando imagen...', self.picture)
        elif self.action == DActions.Eraser:
            pass
        elif self.action == DActions.ColorPick:
            if event == cv2.EVENT_LBUTTONDBLCLK:
                # Extrae valores de pixel de la imagen
                r, g, b, h, s, v = Utils.Utils.get_pixel_values(self.picture, x, y)
                print(r, g, b)

                # Actualiza el color
                self.color['r'] = r
                self.color['g'] = g
                self.color['b'] = b
                # Visualiza el color extraído en el label
                da_lbl_color = getattr(self.ui, f'da_lbl_color_{self.widget_id}')
                da_lbl_color.setStyleSheet(f"background: rgb({self.color['r']}, {self.color['g']}, "
                                           f"{self.color['b']});\n""border: 1px solid gray;")
        else:
            pass

    def set_action_button(self, action):
        """
        Setter del atributo acción usado en callbacks
        :param action:
        :return:
        """
        self.action = action

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
