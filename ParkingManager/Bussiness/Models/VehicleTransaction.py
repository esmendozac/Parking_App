import json


class VehicleTransaction:

    def __init__(self):
        self.IdLote: int
        self.Placa: str
        self.Marca: str
        self.Linea: str
        self.Modelo: str
        self.Clase: str
        self.NumeroMotor: str
        self.Vin: str
        self.TipoTransaccion: str
        self.Fecha: object

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



