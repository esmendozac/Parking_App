import json

from Bussiness.Models import VehicleTransaction
from QTGraphicInterfaces.VehicleForm import Ui_VehicleForm
from PyQt5 import QtCore, QtGui, QtWidgets
# Comunicaciones
from Integration.ParkingApi import ParkingApi as api


class TransactionsForm(QtWidgets.QMainWindow):

    def __init__(self, transaction_context, info: VehicleTransaction, parking_id: int):

        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """
        super(TransactionsForm, self).__init__()
        self.ui = Ui_VehicleForm()
        self.ui.setupUi(self)
        self.api = api()
        self.vehicle_info = VehicleTransaction.VehicleTransaction()
        self.vehicle_info.IdLote = parking_id
        self.transaction_context = transaction_context
        self.ui.btn_ok.clicked.connect(lambda callback: self.save())

        # Parámetros iniciales
        if info is not None:

            self.vehicle_info: VehicleTransaction = info
            self.ui.txb_plate.setText(TransactionsForm.check_if_valid_param(info.Placa))
            self.ui.txb_class.setText(TransactionsForm.check_if_valid_param(info.Clase))
            self.ui.txb_brand.setText(TransactionsForm.check_if_valid_param(info.Marca))
            self.ui.txb_line.setText(TransactionsForm.check_if_valid_param(info.Linea))
            self.ui.txb_model.setText(TransactionsForm.check_if_valid_param(info.Modelo))
            self.ui.txb_color.setText(TransactionsForm.check_if_valid_param(info.Color))

    def save(self):
        self.vehicle_info.Placa = self.ui.txb_plate.text()
        self.vehicle_info.Clase = self.ui.txb_class.text()
        self.vehicle_info.Marca = self.ui.txb_brand.text()
        self.vehicle_info.Linea = self.ui.txb_line.text()
        self.vehicle_info.Modelo = self.ui.txb_model.text()
        self.vehicle_info.Color = self.ui.txb_color.text()

        self.register_transaction(self.vehicle_info)

    def register_transaction(self, data):

        resume = self.api.register_transaction(data.get_dict())
        text = \
            f"""
           -----------------------------------------------------------
               Entrada: {resume["FechaEntrada"]}
               Salida:   {resume["FechaSalida"]}
               Placa: {resume["Placa"]}
               Tarifa por fracción: ${resume["TarifaFraccion"]}
               Tarifa fija después de {resume["FraccionMinimaPrecioFijo"]} minutos : $ {resume["TarifaFija"]}
               Tiempo: {resume["Tiempo"]} minutos
               Valor: ${resume["Valor"]}
           -----------------------------------------------------------
           """
        self.transaction_context.print_transaction(text)
        self.close()

    @staticmethod
    def check_if_valid_param(value):
        if value:
            return value
        else:
            return ""