from Filters.Filter import FilterTypes
from QTGraphicInterfaces.DynamicMainInterface import Ui_MainWindow as Ui
from Models.Picture import Picture as Pic
from Filters.DrawZones import DrawZones as Dz


class FactoryFilter:
    ui: Ui
    picture: Pic

    def __init__(self, picture, ui):
        self.ui = ui
        self.picture = picture

    def create_filter(self, filter_id, row, col, widget_id):
        """
        Construye instancias de filtros
        :param filter_id:
        :param row:
        :param col:
        :param widget_id:
        :return:
        """
        if filter_id == FilterTypes.DrawZones:
            return Dz(self.picture.content, self.ui, row, col, widget_id)
        else:
            raise Exception('No se pudo crear el filtro solicitado porque no existe en la enumeración')

