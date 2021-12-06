import cv2
import numpy as np
import copy
import math
from enum import Enum
from Models import Utils

from QTGraphicInterfaces.DynamicMainInterfaceForm import Ui_MainWindow as Ui
from PyQt5 import QtCore, QtWidgets, QtGui
from Filters.Filter import Filter
from Models.Picture import Picture as Pic


class TPerspective:
    """
    Filtro que permite elegir específicamente zonas de una imagen para delimitar un estacionamiento
    """

    def __init__(self, picture: Pic, ui: Ui, row: int, col: int, widget_id: int, coordinates):

        # Imagen original
        self._original_picture = None
        self.coordinates = coordinates
        self.set_original_picture(picture)
        self.picture = self.get_original_picture()
        self.ui = ui
        self.widget_id = widget_id
        self.draw_widget(row, col, widget_id)

        # Parámetros funcionales
        self.tp_height = 500
        self.tp_width = 1200
        self.vertical_degrees = 25
        self.horizontal_degrees = 5

    def draw_widget(self, row: int, col: int, widget_id: int):
        """
        Renderiza el widget del filtro en la pantallaS
        :param row:
        :param col:
        :param widget_id:
        :return:
        """

        setattr(self.ui, f'tp_group_{widget_id}', QtWidgets.QGroupBox(self.ui.scrollAreaWidgetContents))
        tp_group = getattr(self.ui, f'tp_group_{widget_id}')
        tp_group.setMinimumSize(QtCore.QSize(0, 90))
        tp_group.setObjectName(f'tp_group_{widget_id}')

        setattr(self.ui, f'tp_btn_start_{widget_id}', QtWidgets.QPushButton(tp_group))
        tp_btn_start = getattr(self.ui, f'tp_btn_start_{widget_id}')
        tp_btn_start.setGeometry(QtCore.QRect(10, 30, 40, 40))
        tp_btn_start.setMinimumSize(QtCore.QSize(40, 40))
        tp_btn_start.setMaximumSize(QtCore.QSize(40, 40))
        tp_btn_start.setStyleSheet("border-color: rgb(255, 85, 0);")
        tp_btn_start.setText("")
        icon_tp_btn_start = QtGui.QIcon()
        icon_tp_btn_start.addPixmap(QtGui.QPixmap("icons/iniciar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        tp_btn_start.setIcon(icon_tp_btn_start)
        tp_btn_start.setIconSize(QtCore.QSize(36, 36))
        tp_btn_start.setObjectName(f'tp_btn_start_{widget_id}')

        _translate = QtCore.QCoreApplication.translate
        tp_group.setTitle(_translate("MainWindow", "Transformación de perspectiva"))

        self.ui.formLayout.setWidget(widget_id, QtWidgets.QFormLayout.FieldRole, tp_group)

        # Conexiones
        tp_btn_start.clicked.connect(lambda callback: self.execute_perspective_transform())

    def get_lines(self, transformed, tolerance):

        # Aplica algoritmos de detección de bordes
        image_canny = cv2.Canny(transformed, 0, 100, 0)
        lines = cv2.HoughLines(image_canny, 1, np.pi / 180, tolerance)

        verticals = []
        horizontals = []

        if lines is not None:

            max_size = max([self.tp_height, self.tp_width])

            for l in lines:
                for rho, theta in l:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + max_size * (-b))
                    y1 = int(y0 + max_size * (a))
                    x2 = int(x0 - max_size * (-b))
                    y2 = int(y0 - max_size * (a))

                    angle = theta * 180 / np.pi
                    magnitude = abs(int(rho))

                    # Vertical lines
                    if (((360 - self.vertical_degrees) < angle and angle < self.vertical_degrees)) or (
                    ((-1 * self.vertical_degrees) < angle and angle < self.vertical_degrees)) or (
                    ((180 - self.vertical_degrees) < angle and angle < 180 + self.vertical_degrees)):

                        if rho < 0:
                            theta = theta - np.pi
                            rho = -1 * rho

                        cv2.line(transformed, (x1, y1), (x2, y2), (0, 0, 255), 1)
                        verticals.append({'angle': angle, 'magnitude': magnitude, 'rho': rho, 'theta': theta})

                        # Horizontal lines
                    elif (((90 - self.horizontal_degrees) < angle and angle < (90 + self.horizontal_degrees))) or (
                    ((270 - self.horizontal_degrees) < angle and angle < (270 + self.horizontal_degrees))):

                        cv2.line(transformed, (x1, y1), (x2, y2), (255, 0, 255), 1)
                        horizontals.append({'angle': angle, 'magnitude': magnitude, 'rho': rho, 'theta': theta})

                    verticals = sorted(verticals, key=lambda i: i['magnitude'])
                    horizontals = sorted(horizontals, key=lambda i: i['magnitude'])

        return verticals, horizontals

    def execute_perspective_transform(self):

        # coordinates = np.float32([[[[798, 361], [1176, 355], [1203, 396], [771, 404]], [[654, 465], [1273, 457], [1357, 539], [572, 543]],
        #   [[670, 545], [1356, 539], [1470, 654], [585, 670]], [[338, 787], [1600, 769], [1844, 1005], [134, 1012]]]])

        cont = 0

        for c in self.coordinates[0]:

            tc = np.float32([c[0], c[1], c[3], c[2]])

            print(f"{cont}_Coordenadas inyectadas: {tc}")

            if TPerspective.is_horizontal(tc):
                perspective_zone = np.float32([[0, 0], [self.tp_width, 0], [0, self.tp_height], [self.tp_width, self.tp_height]])
                m = cv2.getPerspectiveTransform(tc, perspective_zone)
                transformed = cv2.warpPerspective(self.picture, m, (self.tp_width, self.tp_height))
                _, binary = cv2.threshold(transformed, 200, 255, cv2.THRESH_BINARY)
            else:
                perspective_zone = np.float32([[0, 0], [self.tp_height, 0], [0, self.tp_width], [self.tp_height, self.tp_width]])
                m = cv2.getPerspectiveTransform(tc, perspective_zone)
                transformed_no_rotated = cv2.warpPerspective(self.picture, m, (self.tp_height, self.tp_width))
                transformed = np.rot90(transformed_no_rotated, k=1)
                transformed = transformed.copy()
                _, binary = cv2.threshold(transformed, 200, 255, cv2.THRESH_BINARY)

            cont += 1

            verticals, horizontals = self.get_lines(transformed, 120)

            verticals_filtered = self.get_classified_lines_by_rho(verticals, 20, transformed, False)
            horizontals_filtered = self.get_classified_lines_by_rho(horizontals, 15, transformed, True)
            cv2.imshow(f'{cont}_Pruebas perspectiva', transformed)

            # verticals_filtered = self.filter_bad_distances(verticals_filtered, 0.5, 0.9, transformed)

    def get_classified_lines_by_rho(self, lines: list, tolerance: int, image, is_horizontal: bool):

        clusters = []
        final = []
        base = [lines[0]]
        max_size = max([self.tp_height, self.tp_width])

        for i in range(1, len(lines)):

            d = abs(lines[i]["magnitude"] - lines[i - 1]["magnitude"])

            if d < tolerance:
                base.append(lines[i])
            else:
                clusters.append(base)
                base = [lines[i]]

                # Punto final
            if i == len(lines) - 1:
                clusters.append(base)

        if is_horizontal:
            clusters = filter(lambda c: (len(c) > 5), clusters)

        # Calculate mean
        for c in clusters:

            rho = 0
            theta = 0

            for l in c:

                if is_horizontal:
                    rho += l['rho']
                    theta += l['theta']
                else:

                    radianes_vertical = self.vertical_degrees * np.pi / 180

                    if (np.pi - radianes_vertical) < theta and theta < (radianes_vertical + np.pi):
                        l['rho'] = -1 * l['rho']
                        l['theta'] = l['theta'] - np.pi
                    elif (2 * np.pi - radianes_vertical) < theta and theta < radianes_vertical:
                        l['theta'] = l['theta'] - (2 * np.pi)

                    rho += l['rho']
                    theta += l['theta']

            rho = rho / len(c)
            theta = theta / len(c)

            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + max_size * (-b))
            y1 = int(y0 + max_size * (a))
            x2 = int(x0 - max_size * (-b))
            y2 = int(y0 - max_size * (a))

            # Calcula la linea equivalente
            final.append({'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2, 'rho': rho, 'theta': theta})
            cv2.line(image,(x1,y1),(x2,y2),(255,125,125),15)

        return final

    def filter_bad_distances(self, clusters: list, percent_1: float, percent_2: float, image):

        distances_1 = []

        for i in range(len(clusters) - 1):
            distances_1.append(abs(clusters[i]['rho'] - clusters[i + 1]['rho']))

        median_1 = np.median(distances_1)

        bad_distances_1 = [d[0] for d in enumerate(distances_1) if d[1] < (percent_1 * median_1)]
        filtered_clusters_1 = [c[1] for c in enumerate(clusters) if c[0] not in bad_distances_1]

        distances_2 = []
        for i in range(len(filtered_clusters_1) - 1):
            distances_2.append(abs(filtered_clusters_1[i]['rho'] - filtered_clusters_1[i + 1]['rho']))

        median_2 = np.median(distances_2)

        clustes_distances = []

        for i in range(len(clusters)):

            # First
            if i == 0:
                d_left = median_2 * percent_2 + 1
                d_right = abs(clusters[i]['rho'] - clusters[i + 1]['rho'])
            # Last
            elif i == len(clusters) - 1:
                d_left = abs(clusters[i]['rho'] - clusters[i - 1]['rho'])
                d_right = median_2 * percent_2 + 1
            else:
                d_left = abs(clusters[i]['rho'] - clusters[i - 1]['rho'])
                d_right = abs(clusters[i]['rho'] - clusters[i + 1]['rho'])

            clustes_distances.append({'rho': clusters[i]['rho'], 'd_left': d_left, 'd_right': d_right})

        clustes_distances_filtered = [c for c in clustes_distances if
                                      c['d_right'] < (percent_2 * median_2) and c['d_left'] < (percent_2 * median_2)]
        clusters_to_return = []

        for cl in clusters:
            if cl['rho'] not in [cl['rho'] for cl in clustes_distances_filtered]:
                clusters_to_return.append(cl)
                cv2.line(image, (cl['x1'], cl['y1']), (cl['x2'], cl['y2']), (255, 125, 125), 15)

        return clusters_to_return

    def set_original_picture(self, picture):
        self._original_picture = copy.deepcopy(picture)

    def get_original_picture(self):
        return copy.deepcopy(self._original_picture)

    @staticmethod
    def is_horizontal(coordinates):
        """
        :param coordinates:
        :return:
        """
        # Segmento 1 - 3
        d_x = abs(coordinates[0][0] - coordinates[2][0])
        d_y = abs(coordinates[0][1] - coordinates[2][1])
        s_13 = math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2))

        # Segmento 2 -4
        d_x = abs(coordinates[1][0] - coordinates[3][0])
        d_y = abs(coordinates[1][1] - coordinates[3][1])
        s_24 = math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2))

        # Segmento 1 - 2
        d_x = abs(coordinates[0][0] - coordinates[1][0])
        d_y = abs(coordinates[0][1] - coordinates[1][1])
        s_12 = math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2))

        # Segmento 3 - 4
        d_x = abs(coordinates[2][0] - coordinates[3][0])
        d_y = abs(coordinates[2][1] - coordinates[3][1])
        s_34 = math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2))

        # Medias
        hor = (s_12 + s_34) / 2
        ver = (s_13 + s_24) / 2

        if hor >= ver:
            return True
        else:
            return False


