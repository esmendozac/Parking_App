import json
import cv2
import copy
from enum import Enum
import sys
import numpy as np
from math import dist
import pytesseract
import re


from PyQt5 import QtWidgets
from QTGraphicInterfaces.TransactionsInterface import Ui_TransactionInterface
from PyQt5 import QtCore, QtGui, QtWidgets


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
custom_config = r'--psm 6 '

# Comunicaciones
from Integration.ParkingApi import ParkingApi as api


class Transaction(QtWidgets.QMainWindow):

    def __init__(self, main_context, parking_id):
        """
            Constructor donde se inicializan parámetros de interfaz gráfica
        """
        super(Transaction, self).__init__()
        self.ui = Ui_TransactionInterface()
        self.ui.setupUi(self)
        self.api = api()
        self.main_context = main_context

        self.ui.txb_resume.setPlainText("")
        self.ui.btn_open_camera.clicked.connect(lambda callback: self.open_camera())

    def open_camera(self):

        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1290)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            ret, frame = cap.read()

            if ret:
                cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if cv2.waitKey(1) & 0xFF == ord('f'):
                self.process_card(frame)

        cap.release()
        cv2.destroyAllWindows()

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

    def process_card(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        GB = cv2.GaussianBlur(image, (15, 15), 1)
        GB = cv2.medianBlur(GB, 15)
        kernel = np.ones((10, 10), np.uint8)
        GB = cv2.morphologyEx(GB, cv2.MORPH_OPEN, kernel)
        kernelopening = np.ones((2, 2), np.uint8)
        # GB = cv2.erode(GB,kernel,iterations = 4)
        th3 = cv2.adaptiveThreshold(GB, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        th3 = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernelopening)
        erosion = cv2.erode(th3, kernelopening, iterations=3)
        th4 = cv2.morphologyEx(erosion, cv2.MORPH_GRADIENT, kernelopening)
        # closing = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((2, 2), np.uint8)
        th4 = cv2.dilate(th4, kernel, iterations=2)
        # erosion = cv2.erode(th3,kernel,iterations = 3)
        # GB = cv2.GaussianBlur(image, (5, 5), 1)
        contornos, hierachy = cv2.findContours(th3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(contornos, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        epsilon = 0.01 * cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, epsilon, True)

        coords = Transaction.sort_coordinates(aprox[0][0], aprox[1][0], aprox[2][0], aprox[3][0])

        c1 = coords[0]
        c2 = coords[1]
        c3 = coords[2]
        c4 = coords[3]

        # Transformación de perspectivas
        tc = np.float32([c4, c1, c3, c2])
        perspective_zone = np.float32([[0, 0], [800, 0], [0, 497], [800, 497]])
        m = cv2.getPerspectiveTransform(tc, perspective_zone)
        transformed = cv2.warpPerspective(frame, m, (800, 497))
        transformed = cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY)

        plate_img = transformed[141:220, 0:144]
        cv2.imshow("plate_img", plate_img)
        plate_text = pytesseract.image_to_string(plate_img, lang="spa", config=custom_config)

        cleaned_plate = re.findall('[A-Z]{3}[0-9]{3}|[A-Z]{3}[0-9]{2}[A-Z]{1}', plate_text)

        if len(cleaned_plate) >= 1:
            print(f"Plate: {cleaned_plate[0]}")
            self.ui.txb_resume.setPlainText(f"Placa: {cleaned_plate[0]}")
        else:
            print("No se obtuvo una placa válida")
            self.ui.txb_resume.setPlainText("No se obtuvo una placa válida")

        brand_img = transformed[142:217, 150:397]
        cv2.imshow("brand_img", brand_img)
        brand_text = pytesseract.image_to_string(brand_img, lang="spa", config=custom_config)
        print(f"brand_text:   {brand_text}")

        line_img = transformed[139:240, 395:585]
        cv2.imshow("line_img", line_img)
        line_text = pytesseract.image_to_string(line_img, lang="spa", config=custom_config)
        print(f"line_text:   {line_text}")

        color_img = transformed[214:265, 150:400]
        cv2.imshow("color_img", color_img)
        color_text = pytesseract.image_to_string(color_img, lang="spa", config=custom_config)
        print(f"color_text:   {color_text}")

        model_img = transformed[156:240, 672:796]
        cv2.imshow("model_img", model_img)
        model_text = pytesseract.image_to_string(model_img, lang="spa", config=custom_config)
        cleaned_model = re.findall('[0-9]{4}', model_text)

        if len(cleaned_model) >= 1:
            print(f"Model: {cleaned_model[0]}")
        else:
            print("No se obtuvo un modelo válida")

        cv2.imshow('Perspectiva', transformed)



