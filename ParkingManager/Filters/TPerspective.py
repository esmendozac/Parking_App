import cv2
import numpy as np
import copy
from enum import Enum
from Models import Utils

from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtWidgets, QtGui
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class TPerspective:
    """
    Filtro que permite elegir específicamente zonas de una imagen para delimitar un estacionamiento
    """
    ui: Ui

    def __init__(self, picture: Pic, ui: Ui, row: int, col: int, widget_id: int, coordinates):
        print(f"Construyó: ")

        # Imagen original
        self._original_picture = None
        self.coordinates = coordinates
        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.widget_id = widget_id
        self.draw_widget(row, col, widget_id)

    def draw_widget(self, row: int, col: int, widget_id: int):
        """
        Renderiza el widget del filtro en la pantalla
        :param row:
        :param col:
        :param widget_id:
        :return:
        """

        setattr(self.ui, f'tp_frame_{widget_id}', QtWidgets.QFrame(self.ui.scrollAreaWidgetContents))
        tp_frame = getattr(self.ui, f'tp_frame_{widget_id}')
        tp_frame.setEnabled(True)
        tp_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        tp_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        tp_frame.setObjectName(f'tp_frame_{widget_id}')

        setattr(self.ui, f'tp_group_{widget_id}', QtWidgets.QGroupBox(tp_frame))
        tp_group = getattr(self.ui, f'tp_group_{widget_id}')
        tp_group.setGeometry(QtCore.QRect(10, 10, 391, 81))
        tp_group.setObjectName(f'tp_group_{widget_id}')

        setattr(self.ui, f'tp_btn_start_{widget_id}', QtWidgets.QPushButton(self.tp_group))
        tp_btn_start = getattr(self.ui, f'tp_btn_start_{widget_id}')
        tp_btn_start.setGeometry(QtCore.QRect(10, 30, 40, 40))
        tp_btn_start.setMinimumSize(QtCore.QSize(40, 40))
        tp_btn_start.setMaximumSize(QtCore.QSize(40, 40))
        tp_btn_start.setStyleSheet("border-color: rgb(255, 85, 0);")
        tp_btn_start.setText("")
        icon_tp_btn_start = QtGui.QIcon()
        icon_tp_btn_start.addPixmap(QtGui.QPixmap("icons/iniciar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        tp_btn_start.setIcon(icon_tp_btn_start)
        tp_btn_start.setIconSize(QtCore.QSize(36, 36))
        tp_btn_start.setObjectName(f'tp_btn_start_{widget_id}')

        _translate = QtCore.QCoreApplication.translate
        tp_group.setTitle(_translate("MainWindow", "Transformación de perspectiva"))
        # tp_btn_clear.setToolTip(_translate("MainWindow", "<html><head/><body><p>Limpiar</p></body></html>"))
        # tp_btn_start.setToolTip(_translate("MainWindow", "<html><head/><body><p>Dibujar coordenadas</p></body></html>"))
        # tp_btn_view.setToolTip(_translate("MainWindow", "<html><head/><body><p>Ver imagen</p></body></html>"))
        # tp_btn_delete.setToolTip(_translate("MainWindow", "<html><head/><body><p>Limpiar</p></body></html>"))

        self.ui.gridLayout.addWidget(tp_frame, row, col, 1, 1)

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)
