import json
import datetime
from Bussiness.Models.DefinedSpace import DefinedSpace as DefinedSpace


class Lote:

    def __init__(self, name, nit, email, identifier, token):
        self.IdLote = None
        self.Nombre = name
        self.Nit = nit
        self.Email = email
        self.Identificador = identifier
        self.Token = token
        self.EspaciosDelimitados: list = []

    def add_defined_space(self, defined_space: DefinedSpace):
        """
        Agrega un espacio delimitado a la calibración
        :param defined_space:
        :return:
        """
        self.EspaciosDelimitados.append(defined_space)

    def get_dict(self):

        dict = {
            "IdLote": self.IdLote,
            "Nombre": self.Nombre,
            "Nit": self.Nit,
            "Email": self.Email,
            "Identificador": self.Identificador,
            "Token": self.Token,
            "EspaciosDelimitados": []
        }

        for ds in self.EspaciosDelimitados:
            dict["EspaciosDelimitados"].append(ds.__dict__)

        return dict

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
