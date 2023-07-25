import requests
from abc import ABC, abstractmethod
import csv

class DataReader(ABC):
    @abstractmethod
    def read_data(self, filename):
        pass

class CSVReader(DataReader):
    def read_data(self, filename):
        with open(filename) as file:
            csv_data = csv.reader(file)
            next(csv_data)
            next(csv_data)
            next(csv_data)

            loans = []
            for loan in csv_data:
                loan_id = loan[0]
                client_full_name = loan[2] + " " + loan[3] + " " + loan[4]
                aval_full_name = loan[408] + " " + loan[409] + " " + loan[410]
                week = int(loan[15])
                year = int(loan[16])
                balance = loan[404].strip()
                loans.append([loan_id, client_full_name, week, year, aval_full_name, balance])

        return loans

def consumir_endpoint_post(url, login, password, db):
    try:
        # Crear el objeto JSON con el payload para el método POST
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": "",
            "params": {
                "login": login,
                "password": password,
                "db": db
            }
        }

        # Realizar la solicitud POST y guardar las cookies en la sesión
        session = requests.Session()
        response = session.post(url, json=payload)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Error: {response.status_code} - {response.text}")

        return session  # Devolver la sesión con las cookies

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None


def consumir_endpoint_get(url, prestamo_id, session):
    try:
        # Crear el objeto JSON con el parámetro prestamoId variable
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "prestamoId": prestamo_id
            }
        }

        # Realizar la solicitud GET con la sesión que contiene las cookies de autenticación
        response = session.get(url, json=payload)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            data = response.json()
            code = data['result']['code'] 
            if code != 400:
                print(code)
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")


# URL del endpoint POST que deseas consumir
url_del_endpoint_post = "https://xmsdev.terio.xyz/web/session/authenticate"

# URL del endpoint GET que deseas consumir
url_del_endpoint_get = "https://xmsdev.terio.xyz/api/v1/prestamo"

# Valores para el payload del método POST
login = "sahidalejandroo@gmail.com"
password = "noqA3qL9pMhSgs"
db = "xpress_testing"

# Llamar a la función para consumir el endpoint POST y guardar las cookies en la sesión
session = consumir_endpoint_post(url_del_endpoint_post, login, password, db)

# Si la sesión se ha creado correctamente (cookies recibidas), llamar a la función para consumir el endpoint GET
if session is not None:

    csv_reader = CSVReader()
    data = csv_reader.read_data("BD DINERO XPRESS 2023. CRUDA SEMANA 27 CSV.csv")

    i = 0
    for dat in data:
        # Valor de la variable prestamoId que deseas pasar en la solicitud GET
        prestamo_id_variable = dat[0]
        consumir_endpoint_get(url_del_endpoint_get, prestamo_id_variable, session)
        """i = i + 1
        if i > 5: 
            break"""
