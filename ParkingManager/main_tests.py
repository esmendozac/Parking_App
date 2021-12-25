from Integration.IntegrationApi import IntegrationApi as IntegrationApi
from Bussiness.Communication.Communication import Communication as Communication
import json

# http = IntegrationApi()
#
# # http.set_header('Authorization', "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJJZFVzdWFyaW8iOjIwMTAsIklkZW50aWZpY2FjaW9uIjoiMzA0NDk1NzI1MiIsIkZlY2hhVmVuY2ltaWVudG8iOiIyNS0xMi0yMDIxIDE2OjQwOjU3In0.6TMpcIGIV-7ufvehnEnj01Pvp0XvS5FU8oVV3j5sYso")
#
# try:
#     # x = http.get('dummy')
#     x = http.post('autenticar', {"identificacion": "3044957252", "contrasena": "bcd456"})
#     print(x)
#
# except Exception as ex:
#     print(ex)

com = Communication()

try:
    com.authenticate_user("3044957252", "bcd456")
    com.get_user("1009")
    # x = http.post('autenticar', {"identificacion": "3044957252", "contrasena": "bcd456"})
    # print(x)

except Exception as ex:
    print(ex)




