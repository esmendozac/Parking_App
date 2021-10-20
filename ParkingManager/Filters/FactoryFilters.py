from Filters.Filter import Filter
from QTGraphicInterfaces.DynamicMainInterface import Ui_MainWindow as Ui
from Models.Image import Image as Im
from Filters.DrawZones import DrawZones as Dz


class FactoryFilter:
    ui: Ui
    image: Im

    def __init__(self, image, ui):
        self.ui = ui
        self.image = image

    def create_filter(self, filter_id, row, col, widget_id):
        """
        Construye instancias de filtros
        :param filter_id:
        :param row:
        :param col:
        :param widget_id:
        :return:
        """
        if filter_id == Filter.DrawZones:
            return Dz(self.image, self.ui, row, col, widget_id)
        else:
            raise

