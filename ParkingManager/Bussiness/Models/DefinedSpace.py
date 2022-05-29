import json
import numpy as np
from math import dist


class DefinedSpace:

    def __init__(self, coordinates: list, enabled: bool, space_type: str, index: int):

        #  Procesa las coordenadas
        if len(coordinates) == 4:

            s = DefinedSpace.sort_coordinates(coordinates[0][0], coordinates[1][0], coordinates[2][0], coordinates[3][0])
            self.Coord1 = str(s[0])
            self.Coord2 = str(s[1])
            self.Coord3 = str(s[2])
            self.Coord4 = str(s[3])

            # self.Coord1 = str(coordinates[0][0])
            # self.Coord2 = str(coordinates[1][0])
            # self.Coord3 = str(coordinates[2][0])
            # self.Coord4 = str(coordinates[3][0])
        self.indice = index
        self.IdEspacioDelimitado: int = 0
        self.Habilitado: bool = enabled
        self.Tipo: str = space_type
        self.IdCalibracion: int = 0

    @staticmethod
    def sort_coordinates_old(coord_a, coord_b, coord_c, coord_d):
        """
        Ordenar coordenadas en el espacio absoluto
        :param coord_a:
        :param coord_b:
        :param coord_c:
        :param coord_d:
        :return:
        """
        work_list = [coord_a.tolist(), coord_b.tolist(), coord_c.tolist(), coord_d.tolist()]
        final_work_list = []

        for wl in work_list:
            # Quita el wl de la lista
            partial_work_list_2nd = [pwl for pwl in work_list if pwl != wl]
            # Duplicador para generar todos los casos posibles
            for pwl2 in partial_work_list_2nd:
                partial_work_list_3rd = [pwl3 for pwl3 in partial_work_list_2nd if pwl3 != pwl2]

                first = [wl, pwl2, partial_work_list_3rd[0], partial_work_list_3rd[1]]
                second = [wl, pwl2, partial_work_list_3rd[1], partial_work_list_3rd[0]]

                final_work_list.append(first)
                final_work_list.append(second)

        # Comprobación de reglas de coordenadas
        for i in final_work_list:
            # Reglas de elección
            if i[0][0] < i[1][0] and i[0][1] < i[3][1]:
                if i[1][0] > i[0][0] and i[1][1] < i[2][1]:
                    if i[2][0] > i[3][0] and i[2][1] > i[1][1]:
                        if i[3][0] < i[2][0] and i[3][1] > i[0][1]:
                            # Regla de orientación cruzada
                            if i[1][1] < i[3][1] and i[0][1] < i[2][1]:
                                return np.array(i)

    @staticmethod
    def sort_coordinates(coord_a, coord_b, coord_c, coord_d):
        """
        Ordenar coordenadas en el espacio absoluto
        :param coord_a:
        :param coord_b:
        :param coord_c:
        :param coord_d:
        :return:
        """
        work_list = [coord_a.tolist(), coord_b.tolist(), coord_c.tolist(), coord_d.tolist()]
        final_work_list = []

        for wl in work_list:
            # Quita el wl de la lista
            partial_work_list_2nd = [pwl for pwl in work_list if pwl != wl]
            # Duplicador para generar todos los casos posibles
            for pwl2 in partial_work_list_2nd:
                partial_work_list_3rd = [pwl3 for pwl3 in partial_work_list_2nd if pwl3 != pwl2]

                first = [wl, pwl2, partial_work_list_3rd[0], partial_work_list_3rd[1]]
                second = [wl, pwl2, partial_work_list_3rd[1], partial_work_list_3rd[0]]

                final_work_list.append(first)
                final_work_list.append(second)

        sorted_list = []

        # Comprobación de reglas de coordenadas
        for i in final_work_list:
            # Reglas de elección
            if i[0][0] < i[1][0] and i[0][1] < i[3][1]:
                if i[1][0] > i[0][0] and i[1][1] < i[2][1]:
                    if i[2][0] > i[3][0] and i[2][1] > i[1][1]:
                        if i[3][0] < i[2][0] and i[3][1] > i[0][1]:
                            # Regla de orientación cruzada
                            if i[1][1] < i[3][1] and i[0][1] < i[2][1]:

                                sorted_list = np.array(i)

                                p1 = i[0]
                                p2 = i[1]
                                p3 = i[3]
                                p4 = i[2]

                                # Verificación de orientación

                                # Horizontales
                                dp1p2 = dist(p1, p2)
                                dp3p4 = dist(p3, p4)
                                dw = int((dp1p2 + dp3p4) / 2)

                                # Verticales
                                dp1p3 = dist(p1, p3)
                                dp2p4 = dist(p2, p4)
                                dh = int((dp1p3 + dp2p4) / 2)

                                if dw > dh:
                                    sorted_list = np.array([p2, p4, p3, p1])

        return sorted_list

    def serialize(self):
        return json.dumps(self, default=lambda o: o.__dict__,  sort_keys=True, indent=4)
