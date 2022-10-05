import sys
import numpy as np
import random
from QTGraphicInterfaces.Stats import Ui_StatsWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

# Comunicaciones
from Integration.ParkingApi import ParkingApi as api


class Stats(QtWidgets.QMainWindow):

    def __init__(self, main_context, parking_id):

        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """
        super(Stats, self).__init__()
        self.ui = Ui_StatsWindow()
        self.ui.setupUi(self)
        self.api = api()
        self.parking_id = parking_id
        self.main_context = main_context

        self.ui.txb_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.btn_query.clicked.connect(lambda callback: self.plot_stat(self.ui.cbx_statistics.currentIndex(), self.ui.txb_date.date()))

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.ui.plot_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.ui.plot_frame.setLayout(layout)

    def plot_stat(self, stat_id, date):

        if stat_id == 0:
            data = self.get_occupations(date.toString("yyyy-MM-dd'"))

            x_axis = []
            y_axis = []

            for d in data:
                x_axis.append(d["Hora"])
                y_axis.append(d["Ocupaciones"])

            print(y_axis)

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.bar(x_axis, y_axis)
            self.canvas.draw()

    def get_occupations(self, date):
        return self.api.get_occupations(self.parking_id, date)








