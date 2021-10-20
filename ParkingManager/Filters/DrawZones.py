import cv2
import numpy as np
import Models.Image as Im
from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtGui, QtWidgets


class DrawZones:
    """
    Filtro que permite elegir específicamente zonas de una imagen para delimitar un estacionamiento
    """

    image: Im
    ui: Ui

    def __init__(self, image: Im, ui: Ui, row: int, col: int, widget_id: int):

        self.image = image
        self.ui = ui
        self.draw_widget(row, col, widget_id)

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
        dz_lbl_draw_zone.setStyleSheet("background: rgb(0, 255, 0);\n"
                                                "border: 1px solid black;")
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

        self.ui.gridLayout.addWidget(frame, row, col, 1, 1)

        _translate = QtCore.QCoreApplication.translate

        dz_grb_draw_zones.setTitle(_translate("MainWindow", "Dibujar zonas"))
        dz_btn_draw_zone.setText(_translate("MainWindow", "Dibujar"))
        dz_btn_clean.setText(_translate("MainWindow", "Limpiar"))
        dz_btn_view_zone.setText(_translate("MainWindow", "Ver"))
        dz_btn_delete.setText(_translate("MainWindow", "Eliminar"))

        # Conexiones
        dz_btn_draw_zone.clicked.connect(self.load_image)
        dz_btn_view_zone.clicked.connect(self.view_zones)
        dz_btn_clean.clicked.connect(self.clean_zones)

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
                # Muestra el contorno
                cv2.imshow('Dibujando imagen...', self.image.image)
    
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
