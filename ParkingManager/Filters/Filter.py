import abc
from enum import Enum
from abc import ABC, abstractmethod, abstractproperty


class FilterTypes(Enum):

    DrawZones = 0
    Color = 1
    ColorSpace = 2,
    DelimiteArea = 3,
    Transformation = 4,
    PerspectiveTransformation = 5


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

    @abstractmethod
    def clean(self):
        pass
