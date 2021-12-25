import json
import datetime
from Bussiness.Models.DefinedSpace import DefinedSpace as DefinedSpace


class Calibration:

    def __init__(self, user_id: int, lot_id: int, enabled: bool):
        self.IdCalibracion: int = 0
        self.IdUsuario: int = user_id
        self.IdLote: int = lot_id
        self.Habilitada: bool = enabled
        self.EspacioDelimitadoes: list = []

    def add_defined_space(self, defined_space: DefinedSpace):
        """
        Agrega un espacio delimitado a la calibración
        :param defined_space:
        :return:
        """
        defined_space.IdCalibracion = self.IdCalibracion
        self.EspacioDelimitadoes.append(defined_space)

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
