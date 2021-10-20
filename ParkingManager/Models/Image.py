import cv2
import numpy as np
import copy


class Image:
    # region Public attributes
    # Ruta de la imagen en el disco físico
    path = ""
    # Array de la imagen bgr recién cargada
    image = []
    # Coordenadas de limites útiles en la imagen
    limits = [[]]
    # Mascaras de limites
    masks = []
    # endregion

    # region Private attributes
    # Copia original de la imagen
    __image_original = []
    # endregion

    # region Functions
    def __init__(self, path):
        """
        :param path: Path de la imagen cargada
        """
        self.path = path
        try:
            self.image = cv2.imread(path)
            self.__image_original = cv2.imread(path)
        except:
            ex = "No se puede cargar la imagen " + self.image.path
            raise Exception(ex)

    def get_original(self):

        """
        Obtiene una copia de la imagen original cargada en memoria
        :return: image
        """

        return copy.copy(self.__image_original)

    def add_limit_coordinate(self, x, y, is_last):

        """
        Añade grupos de coordenadas a los límites definidos en la imagen
        :param x: coordenada x
        :param y: coordenada y
        :param is_last: si la coordenada cierra la figura se debe indicar
        :return: void
        """
        # Extrae el indice para insertar los registros
        index = len(self.limits) - 1
        # Añade las coordenadas en los límites
        self.limits[index].append([x, y])

    def add_close_last_limit(self):

        """
        Cierra la ultima coordenada
        :return:
        """

        self.limits.append([])

    def get_all_masks_limits(self):

        """
        Retorna todas las mascaras unificadas para concatenar con la imagen real
        :return: mask
        """
        # Crear una mascara genérica del mismo tamaño de la imagen
        mask = np.zeros(shape=(self.image.shape[:2]), dtype=np.uint8)

        # Itera y concatena las mascaras
        for m in self.masks:
            mask = cv2.bitwise_or(m, mask)

        return mask

    def clean_zones(self):
        self.limits = [[]]
        self.masks = []
        self.image = self.get_original()

    def get_pixel_values(self, x, y):
        """
            Extrae valores RGB y HSV de una imagen especificada para una coordenada
        """
        # Extrae canales de forma independiente
        b_ex, g_ex, r_ex = self.image[:, :, 0], self.image[:, :, 1], self.image[:, :, 2]

        r_val = r_ex[y][x]
        g_val = g_ex[y][x]
        b_val = b_ex[y][x]

        # Conforma imagen rgb de 1px * 1px
        rgb = np.array([[[r_val, g_val, b_val]]])
        # Convierte el espacio de color H: 0 -> 179, S: 0 -> 255, V: -> 0 -> 255
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        # Extrae valores pixel a pixel
        h_val = hsv[0][0][0]
        s_val = hsv[0][0][1]
        v_val = hsv[0][0][2]

        return r_val, g_val, b_val, h_val, s_val, v_val

    @staticmethod
    def calculate_hsv_mask(image_hsv, h, s, v, tolerance):
        """
        Calcula la mascara hsv de un color especifico con la tolerancia especifica
        :param image_hsv:
        :param h:
        :param s:
        :param v:
        :param tolerance:
        :return:
        """
        # Calcula el delta porcentual
        h_percent = int(180 * tolerance / 100)
        s_percent = int(255 * tolerance / 100)
        v_percent = int(255 * tolerance / 100)

        # Establece limites
        h_high = h + h_percent
        h_low = h - h_percent
        s_high = Image.__prevent_saturation(s + s_percent, 0, 255)
        s_low = Image.__prevent_saturation(s - s_percent, 0, 255)
        v_high = Image.__prevent_saturation(v + v_percent, 0, 255)
        v_low = Image.__prevent_saturation(v - v_percent, 0, 255)

        # Para el caso particular de la h (circular en grados:)
        if h_low < 0:
            h_low = 180 - h_low

        if h_high > 179:
            h_high = h_high - 180

        mask = None

        if h_low <= h_high:
            # Conforma los arrays de los limites
            limit_1_low = np.array([h_low, s_low, v_low])
            limit_1_high = np.array([h_high, s_high, v_high])

            # Aplica los límites de los filtros para el color
            mask = cv2.inRange(image_hsv, limit_1_low, limit_1_high)

        else:
            limit_1_low = np.array([h_low, s_low, v_low])
            limit_1_high = np.array([179, s_high, v_high])

            limit_2_low = np.array([0, s_low, v_low])
            limit_2_high = np.array([h_high, s_high, v_high])

            # Aplica los límites de los filtros para el color
            mask1 = cv2.inRange(image_hsv, limit_1_low, limit_1_high)
            mask2 = cv2.inRange(image_hsv, limit_2_low, limit_2_high)
            # Unifica mascaras
            mask = cv2.add(mask1, mask2)

        return mask

    @staticmethod
    def __prevent_saturation(value, low_limit, high_limit):
        """
        Previene la sobre o sub saturación de un valor estableciendo un rango
        :param value:
        :param low_limit:
        :param high_limit:
        :return:
        """
        result = 0

        if value > high_limit:
            result = high_limit
        elif value < low_limit:
            result = low_limit
        else:
            result = value

        return result

    # endregion
