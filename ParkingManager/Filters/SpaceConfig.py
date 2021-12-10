import cv2
import numpy as np
import copy
import math
from enum import Enum
from Models import Utils

from QTGraphicInterfaces.DynamicMainInterfaceForm import Ui_MainWindow as Ui
from PyQt5 import QtCore, QtWidgets, QtGui
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class SpaceConfig:
    """
    Filtro que permite elegir específicamente zonas de una imagen para delimitar un estacionamiento
    """

    def __init__(self, picture: Pic, ui: Ui, row: int, col: int, widget_id: int, initial_picture):

        print("Constructor de config")
        # Imagen original
        self.initial_picture = initial_picture
        self._original_picture = None
        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.widget_id = widget_id
        self.draw_widget(row, col, widget_id)
        self.view_mask()

    def draw_widget(self, row: int, col: int, widget_id: int):
        """
        Renderiza el widget del filtro en la pantallaS
        :param row:
        :param col:
        :param widget_id:
        :return:
        """

        setattr(self.ui, f'ce_group_{widget_id}', QtWidgets.QGroupBox(self.ui.scrollAreaWidgetContents))
        ce_group = getattr(self.ui, f'ce_group_{widget_id}')
        ce_group.setMinimumSize(QtCore.QSize(0, 90))
        ce_group.setObjectName(f'ce_group_{widget_id}')

        setattr(self.ui, f'ce_btn_clear_{widget_id}', QtWidgets.QPushButton(ce_group))
        ce_btn_clear = getattr(self.ui, f'ce_btn_clear_{widget_id}')
        ce_btn_clear.setGeometry(QtCore.QRect(300, 30, 40, 40))
        ce_btn_clear.setMinimumSize(QtCore.QSize(40, 40))
        ce_btn_clear.setMaximumSize(QtCore.QSize(40, 40))
        ce_btn_clear.setText("")
        icon_ce_btn_clear = QtGui.QIcon()
        icon_ce_btn_clear.addPixmap(QtGui.QPixmap("icons/limpiar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ce_btn_clear.setIcon(icon_ce_btn_clear)
        ce_btn_clear.setIconSize(QtCore.QSize(32, 32))
        ce_btn_clear.setObjectName(f'ce_btn_clear_{widget_id}')

        setattr(self.ui, f'ce_btn_start_{widget_id}', QtWidgets.QPushButton(ce_group))
        ce_btn_start = getattr(self.ui, f'ce_btn_start_{widget_id}')
        ce_btn_start.setGeometry(QtCore.QRect(10, 30, 40, 40))
        ce_btn_start.setMinimumSize(QtCore.QSize(40, 40))
        ce_btn_start.setMaximumSize(QtCore.QSize(40, 40))
        ce_btn_start.setText("")
        icon_ce_btn_start = QtGui.QIcon()
        icon_ce_btn_start.addPixmap(QtGui.QPixmap("icons/iniciar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ce_btn_start.setIcon(icon_ce_btn_start)
        ce_btn_start.setIconSize(QtCore.QSize(32, 32))
        ce_btn_start.setObjectName(f'ce_btn_start_{widget_id}')

        setattr(self.ui, f'ce_btn_delete_{widget_id}', QtWidgets.QPushButton(ce_group))
        ce_btn_delete = getattr(self.ui, f'ce_btn_delete_{widget_id}')
        ce_btn_delete.setGeometry(QtCore.QRect(340, 30, 40, 40))
        ce_btn_delete.setMinimumSize(QtCore.QSize(40, 40))
        ce_btn_delete.setMaximumSize(QtCore.QSize(40, 40))
        ce_btn_delete.setText("")
        icon_ce_btn_delete = QtGui.QIcon()
        icon_ce_btn_delete.addPixmap(QtGui.QPixmap("icons/eliminar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ce_btn_delete.setIcon(icon_ce_btn_delete)
        ce_btn_delete.setIconSize(QtCore.QSize(32, 32))
        ce_btn_delete.setObjectName(f'ce_btn_delete_{widget_id}')

        setattr(self.ui, f'ce_btn_view_{widget_id}', QtWidgets.QPushButton(ce_group))
        ce_btn_view = getattr(self.ui, f'ce_btn_view_{widget_id}')
        ce_btn_view.setGeometry(QtCore.QRect(260, 30, 40, 40))
        ce_btn_view.setMinimumSize(QtCore.QSize(40, 40))
        ce_btn_view.setMaximumSize(QtCore.QSize(40, 40))
        ce_btn_view.setText("")
        icon_ce_btn_view = QtGui.QIcon()
        icon_ce_btn_view.addPixmap(QtGui.QPixmap("icons/ver.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ce_btn_view.setIcon(icon_ce_btn_view)
        ce_btn_view.setIconSize(QtCore.QSize(32, 32))
        ce_btn_view.setObjectName(f'ce_btn_view_{widget_id}')

        _translate = QtCore.QCoreApplication.translate

        ce_group.setTitle(_translate("MainWindow", "Configuración de espacios"))
        ce_btn_clear.setToolTip(_translate("MainWindow", "<html><head/><body><p>Limpiar</p></body></html>"))
        ce_btn_view.setToolTip(_translate("MainWindow", "<html><head/><body><p>Ver imagen</p></body></html>"))
        ce_btn_delete.setToolTip(_translate("MainWindow", "<html><head/><body><p>Limpiar</p></body></html>"))
        ce_btn_start.setToolTip(_translate("MainWindow", "<html><head/><body><p>Dibujar coordenadas</p></body></html>"))

        self.ui.formLayout.setWidget(widget_id, QtWidgets.QFormLayout.FieldRole, ce_group)

    def view_mask(self):
        cv2.imshow(f'{self.widget_id}_Configuración de espacios', self.initial_picture.content)

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)
