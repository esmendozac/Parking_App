from Filters.Filter import FilterTypes
from QTGraphicInterfaces.DynamicMainInterface import Ui_MainWindow as Ui
from Models.Picture import Picture as Pic
from Filters.DrawZones import DrawZones as Dz
from Filters.Color import Color as Col
from Filters.ColorSpace import ColorSpace as Cos
from Filters.Delimite import Delimite as De
from Filters.Transform import Transform as Tr


class FactoryFilter:
    ui: Ui
    picture: Pic

    def __init__(self, picture, ui):
        self.ui = ui
        self.picture = picture

    def create_filter(self, filter_id, row, col, widget_id, last_filter):
        """
        Construye instancias de filtros
        :param filter_id:
        :param row:
        :param col:
        :param widget_id:
        :param last_filter:
        :return:
        """
        if filter_id == FilterTypes.DrawZones:
            if last_filter is not None:
                if isinstance(last_filter, Col):
                    # Envía el color anterior para el trazado
                    color_selected = last_filter.get_selected_color()
                    return Dz(self.picture.content, self.ui, row, col, widget_id, color_selected)

                return Dz(self.picture.content, self.ui, row, col, widget_id)
            else:
                return Dz(self.picture.content, self.ui, row, col, widget_id)
        elif filter_id == FilterTypes.Color:
            return Col(self.picture.content, self.ui, row, col, widget_id)
        elif filter_id == FilterTypes.ColorSpace:
            return Cos(self.picture.content, self.ui, row, col, widget_id)
        elif filter_id == FilterTypes.DelimiteArea:
            return De(self.picture.content, self.ui, row, col, widget_id)
        elif filter_id == FilterTypes.Transformation:
            return Tr(self.picture.content, self.ui, row, col, widget_id)
        else:
            raise Exception('No se pudo crear el filtro solicitado porque no existe en la enumeración')

