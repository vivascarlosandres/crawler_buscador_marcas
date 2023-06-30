import json
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuración
numeros_registro = ['1236216', '1236222', '1236223', '1236224', '1236226', '1236227', '1236275', '1236319', '1236450', '1236470', '1236472', '1236471', '1236482']
use_proxy = False  # Configurar como True si se desea utilizar proxies
num_threads = 5  # Número de hilos de ejecución concurrentes
output_file = "resultados.json"  # Nombre y ubicación del archivo JSON de salida

# URL y proxies (si se utilizan)
url1 = 'https://ion.inapi.cl/Marca/BuscarMarca.aspx/FindMarcas'
url2 = 'https://ion.inapi.cl/Marca/BuscarMarca.aspx/FindMarcaByNumeroSolicitud'
proxies = {
    'http': 'http://your-proxy-url',
    'https': 'https://your-proxy-url'
}  # Configurar los proxies correspondientes si se utilizan

# Función para procesar un número de registro
def process_numero_registro(numero):
    resultado = {}

    payload = {
        "Hash": "",
        "IDW": "",
        "LastNumSol": 0,
        "param1": "",
        "param2": numero,
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
        if use_proxy:
            s.proxies = proxies

        data = json.loads(s.post(url1, json=payload).json()['d'])

        observada_de_fondo = False
        fecha_observada_fondo = None
        apelaciones = False
        ipt = False

        for m in data['Marcas']:
            payload = {
                "Hash": data['Hash'],
                "IDW": "",
                "numeroSolicitud": m['id']
            }
            data = json.loads(s.post(url2, json=payload).json()['d'])
            df = pd.DataFrame(data['Marca']['Instancias'])

            if any('Resolución de observaciones de fondo de marca' in desc for desc in df['EstadoDescripcion']):
                observada_de_fondo = True
                fecha_observada_fondo = df.loc[df['EstadoDescripcion'].str.contains('Resolución de observaciones de fondo de marca'), 'Fecha'].values[0]
            if any('Recurso de apelación' in desc for desc in df['EstadoDescripcion']):
                apelaciones = True
            if any('IPT' in desc or 'IPTV' in desc for desc in df['EstadoDescripcion']):
                ipt = True

        resultado["Numero de Registro"] = numero
        resultado["Observada de Fondo"] = observada_de_fondo
        resultado["Fecha Observada de Fondo"] = fecha_observada_fondo
        resultado["Apelaciones"] = apelaciones
        resultado["IPT"] = ipt

    return resultado

# Procesamiento en paralelo
resultados_totales = []
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(process_numero_registro, numero) for numero in numeros_registro]
    for future in as_completed(futures):
        resultado = future.result()
        resultados_totales.append(resultado)

# Guardar los resultados en un archivo JSON
with open(output_file, "w") as file:
    json.dump(resultados_totales, file)

print("Los resultados se han guardado en '{}'.".format(output_file))
