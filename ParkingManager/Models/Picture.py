import cv2


class Picture:

    path = None
    content = []

    # region Functions
    def __init__(self, path):
        """
        Lee la imagen y la carga en memoria
        :param path: Path de la imagen cargada
        """
        self.path = path
        try:
            self.content = cv2.imread(path)
        except Exception as ex:
            raise Exception(ex)
