import json
import cv2
import copy
from enum import Enum
import sys

from PyQt5 import QtWidgets
from QTGraphicInterfaces.TransactionsInterface import Ui_TransactionInterface
from PyQt5 import QtCore, QtGui, QtWidgets


# Comunicaciones
from Integration.ParkingApi import ParkingApi as api


class Transaction(QtWidgets.QMainWindow):

    def __init__(self, main_context, parking_id):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """
        super(Transaction, self).__init__()
        self.ui = Ui_TransactionInterface()
        self.ui.setupUi(self)
        self.api = api()
        self.main_context = main_context

