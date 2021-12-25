import json


class DefinedSpace:

    def __init__(self, coordinates: list, enabled: bool, space_type: str):

        #  Procesa las coordenadas
        if len(coordinates) == 4:
            self.Coord1 = str(coordinates[0][0])
            self.Coord2 = str(coordinates[1][0])
            self.Coord3 = str(coordinates[2][0])
            self.Coord4 = str(coordinates[3][0])

        self.IdEspacioDelimitado: int = 0
        self.Habilitado: bool = enabled
        self.Tipo: str = space_type
        self.IdCalibracion: int = 0

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
