import json
import requests
import pandas as pd

url1 = 'https://ion.inapi.cl/Marca/BuscarMarca.aspx/FindMarcas'
url2 = 'https://ion.inapi.cl/Marca/BuscarMarca.aspx/FindMarcaByNumeroSolicitud'

payload = {
    "Hash": "",
    "IDW": "",
    "LastNumSol": 0,
    "param1": "",
    "param2": "1236222",
    "param3": "",
    "param4": "",
    "param5": "",
    "param6": "",
    "param7": "",
    "param8": "",
    "param9": "",
    "param10": "",
    "param11": "",
    "param12": "",
    "param13": "",
    "param14": "",
    "param15": "",
    "param16": "",
    "param17": "1",
    "responseCaptcha": "este texto no se validará"
}

with requests.session() as s:
    data = json.loads(s.post(url1, json=payload).json()['d'])

    data_list = [] ## Lista vacía para almacenar los datos

    for m in data['Marcas']:
        payload = {
            "Hash": data['Hash'],
            "IDW": "",
            "numeroSolicitud": m['id']
        }
        data = json.loads(s.post(url2, json=payload).json()['d'])
        df = pd.DataFrame(data['Marca']['Instancias'])
        data_list.append(df.to_dict()) ## Agregar los datos a la lista

    with open('datos.json', 'w') as file:
        json.dump(data_list, file) ## Guardar la lista en el archivo 'datos.json'
