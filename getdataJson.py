import requests
import json

logion = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "login": "sahidalejandroo@gmail.com",
                "password": "noqA3qL9pMhSgs",
                "db": "xpress_testing"
            }
    }


header = [{"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache"}]
url = "https://xmsdev.terio.xyz/web/session/authenticate"
url_import = "https://xmsdev.terio.xyz/api/v1/import/create"
url_esta = "https://xmsdev.terio.xyz//api/v1/prestamo"


response = requests.post(url, data=json.dumps(logion), headers=header[0])
r = json.loads(response.text)
cookies = response.cookies
c = cookies.values()
cookie = c[0]
header = [{"Content-Type": "application/json", "Accept": "application/json", "Catch-Control": "no-cache",
               "Set-Cookie": "session_id=%s" % (c[0]) }]

with open('prestamos_odoo_activo.json') as f:
    data = json.load(f)
    cont = 0
    list = []

    contador = 0
    for item in data:
        cont = cont + 1
        get_id = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "prestamoId": item['prestamoId']
            }
        }
        print(item['prestamoId'])
        response_import = requests.get(url_esta, data=json.dumps(get_id), headers=response.headers, cookies=cookies)
        prestamo = json.loads(response_import.text)
        print(prestamo)
        if prestamo['result']['code'] == 200:
            list.append(prestamo['result']['data'][0])
        # Convertir la lista en formato JSON con indentación
        contador = contador + 1
        if contador > 200: break

    json_lista = json.dumps(list, indent=4)
    # Guardar la lista en un archivo de texto
    with open('prestamos_semana28.json', 'w') as archivo:
         archivo.write(json_lista)