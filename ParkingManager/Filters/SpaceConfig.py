import cv2
import numpy as np
import copy
import math
from enum import Enum


from QTGraphicInterfaces.DynamicMainInterfaceForm import Ui_MainWindow as Ui
from PyQt5 import QtCore, QtWidgets, QtGui
from Filters.Filter import Filter
from Models.Picture import Picture as Pic
from Models.Utils import Utils as Ut

# Negocio
from Bussiness.Models.Calibration import Calibration as Calibration
from Bussiness.Models.DefinedSpace import DefinedSpace as DefinedSpace


# noinspection SpellCheckingInspection
class SpaceConfig:
    """
    Filtro que permite elegir específicamente zonas de una imagen para delimitar un estacionamiento
    """

    def __init__(self, picture: Pic, ui: Ui, row: int, col: int, widget_id: int):

        # Creación de la calibración
        self.calibration = Calibration(1, 1, True)

        self._original_picture = None
        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.widget_id = widget_id
        self.draw_widget(row, col, widget_id)
        self.generate_spaces()

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
        ce_btn_start.clicked.connect(lambda callback: self.generate_spaces())

    def generate_spaces(self):

        try:
            # Extrae la imagen inicial
            initial_image = Ut.get_original_image_content()

            # Binariza la mascara
            original_bw = cv2.cvtColor(self.picture, cv2.COLOR_BGR2GRAY)
            _, original_bin = cv2.threshold(original_bw, 100, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(original_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            # Dibuja el rectangulo:
            for c in contours:
                epsilon = 0.01 * cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon, True)

                cv2.drawContours(initial_image, [approx], -1, (0, 0, 255), cv2.FILLED)

                print(f'Puntos: {len(approx)}, approx: {str(approx[0][0])}')
                ds = DefinedSpace(approx, True, "Normal space")
                self.calibration.add_defined_space(ds)

            cv2.imshow(f'{self.widget_id}_Espacios delimitados...', initial_image)
            cv2.imshow(f'{self.widget_id}_Mascara...', original_bin)

            print(self.calibration.serialize())

        except Exception as ex:
            raise Exception(ex)

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)
