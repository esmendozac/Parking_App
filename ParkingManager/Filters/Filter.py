from enum import Enum
from abc import ABC, abstractmethod


class FilterTypes(Enum):

    DrawZones = 0
    ColorLines = 1


class Filter(ABC):

    @abstractmethod
    def get_picture_filtered(self):
        pass

    @abstractmethod
    def get_original_picture(self):
        pass

    @abstractmethod
    def set_original_picture(self, picture):
        pass

    @abstractmethod
    def draw_widget(self, row: int, col: int, widget_id: int):
        pass