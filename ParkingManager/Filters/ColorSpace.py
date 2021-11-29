import cv2
import numpy as np
import copy
from QTGraphicInterfaces.MainInterface import Ui_Form as Ui
from PyQt5 import QtCore, QtWidgets
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class ColorSpace(Filter):

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

        # Tiempo de ejecución
        setattr(self.ui, f'cs_frame_{widget_id}', QtWidgets.QFrame(self.ui.scrollAreaWidgetContents))
        frame = getattr(self.ui, f'cs_frame_{widget_id}')
        frame.setMinimumSize(QtCore.QSize(400, 80))
        frame.setMaximumSize(QtCore.QSize(400, 100))
        frame.setStyleSheet("")
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName(f'cs_frame_{widget_id}')

        setattr(self.ui, f'cs_grb_color_space_{widget_id}', QtWidgets.QGroupBox(frame))
        cs_grb_color_space = getattr(self.ui, f'cs_grb_color_space_{widget_id}')
        cs_grb_color_space.setGeometry(QtCore.QRect(0, 0, 391, 101))
        cs_grb_color_space.setObjectName(f'cs_grb_color_space_{widget_id}')

        setattr(self.ui, f'cs_cbx_color_space_{widget_id}', QtWidgets.QComboBox(cs_grb_color_space))
        cs_cbx_color_space = getattr(self.ui, f'cs_cbx_color_space_{widget_id}')
        cs_cbx_color_space.setGeometry(QtCore.QRect(30, 40, 171, 22))
        cs_cbx_color_space.setObjectName(f'cs_cbx_color_space_{widget_id}')
        cs_cbx_color_space.addItem("")

        setattr(self.ui, f'cs_btn_apply_{widget_id}', QtWidgets.QPushButton(cs_grb_color_space))
        cs_btn_apply = getattr(self.ui, f'cs_btn_apply_{widget_id}')
        cs_btn_apply.setGeometry(QtCore.QRect(210, 40, 71, 23))
        cs_btn_apply.setObjectName(f'cs_btn_apply_{widget_id}')

        setattr(self.ui, f'cs_btn_view_{widget_id}', QtWidgets.QPushButton(cs_grb_color_space))
        cs_btn_view = getattr(self.ui, f'cs_btn_view_{widget_id}')
        cs_btn_view.setGeometry(QtCore.QRect(290, 40, 71, 23))
        cs_btn_view.setObjectName(f'cs_btn_view_{widget_id}')

        self.ui.gridLayout.addWidget(frame, row, col, 1, 1)

        _translate = QtCore.QCoreApplication.translate

        cs_grb_color_space.setTitle(_translate("MainWindow", "Cambiar espacio de color"))
        cs_cbx_color_space.setItemText(0, _translate("MainWindow", "COLOR_BGR2GRAY"))
        cs_btn_apply.setText(_translate("MainWindow", "Aplicar"))
        cs_btn_view.setText(_translate("MainWindow", "Ver"))

        cs_btn_view.clicked.connect(self.view_result)
        cs_btn_apply.clicked.connect(self.get_picture_filtered)

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)

    def clean(self):
        pass

    def get_picture_filtered(self):
        picture = Pic()
        picture.create_picture_from_content(cv2.cvtColor(self.picture, cv2.COLOR_BGR2GRAY))

        # Genera la capa filtrada con la mascara adecuada
        return picture

    def view_result(self):
        """
        Visualiza el resultado del filtro
        :return:
        """
        cv2.imshow(f'{self.widget_id}_Espacio de color', self.get_picture_filtered().content)

        # Bloquea edición del filtro
        # getattr(self.ui, f'dz_btn_draw_zone_{self.widget_id}').setDisabled(True)
        # getattr(self.ui, f'dz_cbx_executed_{self.widget_id}').setCheckState(QtCore.Qt.Checked)
        # self.is_done = True
        # self.set_ext_btn_state(True)

