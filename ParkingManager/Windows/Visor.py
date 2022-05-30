# from threading import Thread
# import time
# import cv2
# import numpy as np
# import json
# import re
# from math import dist
# from keras.applications.imagenet_utils import preprocess_input, decode_predictions
# from keras.models import load_model
# from datetime import datetime
# import copy
#
# # Constantes
# OBS_CAMERA_ADDR = 1
# OBS_CAMERA_WIDTH = 1920
# OBS_CAMERA_HEIGHT = 1080
# PRED_IMAGE_SIZE = 224
# AREA_MINIMA = 50
# CLASES = ['DISCAPACITADO', 'LIBRE', 'OCUPADO']
# # CLASES = ['LIBRE','OCUPADO']
# MODEL = "C:/Users/R5 3400/Desktop/Generador imagenes/6DSOriginalDatosVariadosIV3.h5"
# MODEL = "C:/Users/R5 3400/Desktop/Generador imagenes/18CDSClean14OriginalDatosVariados.h5"
# # MODEL = "C:/Users/R5 3400/Desktop/Generador imagenes/22DSDosClases_Seg.h5"
#
# JSON_FILE = 'C:/Users/R5 3400/Desktop/Generador imagenes/14.json'
#
# evalua_modelo_flag: bool = False
#
#
# def clean_coordinates(coord):
#     return re.sub("[^\w\s]", "", coord)
#
#
# def load_json(file: str):
#     # JSON file
#     f = open(file, "r")
#     data = json.loads(f.read())
#     f.close()
#
#     return data
#
#
# def generate_numpy_coordinates(json_data: dict):
#     spaces = json_data['EspacioDelimitadoes']
#
#     for s in spaces:
#         coord1 = np.fromstring(clean_coordinates(s["Coord1"]), dtype=int, sep='  ')
#         coord2 = np.fromstring(clean_coordinates(s["Coord2"]), dtype=int, sep='  ')
#         coord3 = np.fromstring(clean_coordinates(s["Coord3"]), dtype=int, sep='  ')
#         coord4 = np.fromstring(clean_coordinates(s["Coord4"]), dtype=int, sep='  ')
#
#         s["NumpyCoords"] = [coord1, coord2, coord3, coord4]
#
#     return json_data
#
#
# def generate_mask(data):
#     mask = np.zeros(shape=(1080, 1920), dtype=np.uint8)
#
#     for space in data["EspacioDelimitadoes"]:
#         c = space["NumpyCoords"]
#         # Arma el contorno para dibujarlo
#         contour = [
#             np.array([[c[0][0], c[0][1]], [c[1][0], c[1][1]], [c[2][0], c[2][1]], [c[3][0], c[3][1]]], dtype=np.int32)]
#
#         cv2.drawContours(image=mask, contours=contour, thickness=cv2.FILLED, color=(255), lineType=cv2.LINE_AA,
#                          contourIdx=-1)
#
#     return mask
#
#     global evalua_modelo
#
#     while True:
#         time.sleep(5)
#         now = datetime.now()
#         print("now =", now)
#
#
# def timer_evaluar_modelo():
#     while True:
#         time.sleep(1)
#
#         if evalua_modelo_flag:
#             print(f'Evaluada: {evalua_modelo_flag}')
#
#             # General
#             height, width = frame.shape[:2]
#
#             # Transf perspectiva
#             h = 400
#             w = 200
#
#             if isinstance(frame, (np.ndarray, np.generic)):
#
#                 for space in data["EspacioDelimitadoes"]:
#                     c = space["NumpyCoords"]
#
#                     pts1 = np.float32([[c[0][0], c[0][1]], [c[1][0], c[1][1]], [c[3][0], c[3][1]], [c[2][0], c[2][1]]])
#                     pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
#
#                     p1 = (c[0][0], c[0][1])
#                     p2 = (c[1][0], c[1][1])
#                     p3 = (c[3][0], c[3][1])
#                     p4 = (c[2][0], c[2][1])
#
#                     # Coordinates
#                     cv2.circle(clean_frame, p1, 3, (255, 0, 0), 2)
#                     cv2.circle(clean_frame, p2, 3, (0, 255, 0), 2)
#                     cv2.circle(clean_frame, p3, 3, (0, 0, 255), 2)
#                     cv2.circle(clean_frame, p4, 3, (255, 255, 255), 2)
#
#                     # Horizontales
#                     dp1p2 = dist(p1, p2)
#                     dp3p4 = dist(p3, p4)
#                     dw = int((dp1p2 + dp3p4) / 2)
#
#                     # Verticales
#                     dp1p3 = dist(p1, p3)
#                     dp2p4 = dist(p2, p4)
#                     dh = int((dp1p3 + dp2p4) / 2)
#
#                     # h = dh
#                     # w = dw
#
#                     # pts2 = np.float32([[0, 0],[w, 0],[0, h],[w, h]])
#
#                     m = cv2.getPerspectiveTransform(pts1, pts2)
#
#                     space["WarpedImage"] = cv2.warpPerspective(clean_frame, m, (w, h))
#
#                     # current date and time
#                     now = datetime.now()
#
#                     timestamp = datetime.timestamp(now)
#                     cv2.imwrite(f'F:\Dataset\ImagenesPrueba\{timestamp}.png', space["WarpedImage"])
#
#                     # predecir clase asociada
#                     image_for_model = cv2.resize(space["WarpedImage"], (PRED_IMAGE_SIZE, PRED_IMAGE_SIZE),
#                                                  interpolation=cv2.INTER_AREA)
#
#                     xt = np.asarray(image_for_model)
#                     xt = np.expand_dims(xt, axis=0)
#                     preds = modelo.predict(xt)
#                     space["label"] = CLASES[np.argmax(preds)]
#
#                     # Arma el contorno para dibujarlo
#                     space["contour"] = [
#                         np.array([[c[0][0], c[0][1]], [c[1][0], c[1][1]], [c[2][0], c[2][1]], [c[3][0], c[3][1]]],
#                                  dtype=np.int32)]
#
#                     # now = datetime.now()
#         # print("now =", now)
#
#
# modelo = load_model(MODEL)
#
# # Captura de video
# cap = cv2.VideoCapture(OBS_CAMERA_ADDR)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, OBS_CAMERA_WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, OBS_CAMERA_HEIGHT)
#
# # Carga información de coordenadas json
# json_data = load_json(JSON_FILE)
# data = generate_numpy_coordinates(json_data)
# mask = generate_mask(data)
#
# # Sustracción de fondo
# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# # fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
#
# Thread(target=timer_evaluar_modelo).start()
#
# while cap.isOpened():
#
#     global frame, clean_frame
#
#     ret, frame = cap.read()
#
#     clean_frame = copy.deepcopy(frame)
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # Dibujamos un rectángulo en frame, para señalar el estado
#     # del área en análisis (movimiento detectado o no detectado)
#     cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
#     color = (0, 255, 0)
#     texto_estado = "Estado: No se ha detectado movimiento"
#     # Especificamos los puntos extremos del área a analizar
#     area_pts = np.array([[240, 150], [1120, 150], [620, frame.shape[0]], [50, frame.shape[0]]])
#
#     # Con ayuda de una imagen auxiliar, determinamos el área
#     # sobre la cual actuará el detector de movimiento
#     image_area = cv2.bitwise_and(gray, gray, mask=mask)
#
#     # Obtendremos la imagen binaria donde la región en blanco representa
#     # la existencia de movimiento
#     fgmask = fgbg.apply(image_area)
#     fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
#     fgmask = cv2.dilate(fgmask, None, iterations=4)
#
#     cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
#
#     # Activador de la evaluación
#     detecciones = list(map(lambda c: cv2.contourArea(c) > AREA_MINIMA, cnts))
#
#     # Genera bandera de evaluación
#     if len(detecciones) > 0:
#         evalua_modelo_flag = True
#     else:
#         evalua_modelo_flag = False
#
#     for cnt in cnts:
#         if cv2.contourArea(cnt) > 50:
#             x, y, w, h = cv2.boundingRect(cnt)
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             texto_estado = "Estado: Alerta Movimiento Detectado!"
#             color = (0, 0, 255)
#             evalua_modelo = True
#
#     for space in data["EspacioDelimitadoes"]:
#
#         if "label" in space:
#             if space["label"] == 'LIBRE':
#                 cv2.drawContours(image=frame, contours=space["contour"], thickness=2, color=(0, 255, 0),
#                                  lineType=cv2.LINE_AA, contourIdx=-1)
#             elif space["label"] == 'OCUPADO':
#                 cv2.drawContours(image=frame, contours=space["contour"], thickness=2, color=(0, 0, 255),
#                                  lineType=cv2.LINE_AA, contourIdx=-1)
#             elif space["label"] == 'DISCAPACITADO':
#                 cv2.drawContours(image=frame, contours=space["contour"], thickness=2, color=(255, 0, 0),
#                                  lineType=cv2.LINE_AA, contourIdx=-1)
#
#                 # cv2.drawContours(frame, [area_pts], -1, color, 2)
#     cv2.putText(frame, texto_estado, (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
#     # cv2.imshow('fgmask', fgmask)
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(1) == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()