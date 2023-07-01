![Logo](https://imgur.com/YL4RHxX.png)

# Web Crawler Buscador de Marcas

## Índice

1) <a href="https://github.com/vivascarlosandres/crawler_buscador_marcas/tree/main#objetivo">Objetivo</a>
2) <a href="https://github.com/vivascarlosandres/crawler_buscador_marcas/tree/main#requerimientos-funcionales">Requerimientos funcionales</a>
3) <a href="https://github.com/vivascarlosandres/crawler_buscador_marcas/tree/main#instalación">Instalación</a>
4) <a href="https://github.com/vivascarlosandres/crawler_buscador_marcas/tree/main#configuración-de-variables">Configuración de variables</a>
5) <a href="https://github.com/vivascarlosandres/crawler_buscador_marcas/tree/main#ejecución-del-código">Ejecución del código</a>
6) <a href="https://github.com/vivascarlosandres/crawler_buscador_marcas/tree/main#explicación-del-proceso-de-desarrollo-del-código">Explicación del proceso de desarrollo del código</a>

## Objetivo

Desarrollar un web crawler para un sitio que funciona como buscador de marcas: https://ion.inapi.cl/Marca/BuscarMarca.aspx

## Requerimientos funcionales

El crawler deberá cumplir con lo siguiente:

1. Tomar como entrada una lista de números de registro para la búsqueda e iterar sobre la misma. Por ejemplo: ['1236216', '1236222', '1236223', '1236224',
'1236226', '1236227', '1236275', '1236319', '1236450', '1236470', '1236472',
'1236471', '1236482']
2. Ingresar el número de registro en el cuadro de búsqueda del sitio web.
3. Obtener los datos del registro de la sección "Instancias Administrativas".
4. Guardar en formato JSON, los siguientes datos extraídos para cada registro:

- "Observada_de_Fondo": Si en cualquiera de los valores de la columna "Descripción" contiene el texto "Resolución de observaciones de fondo de marca" se guarda la variable con el valor TRUE sino FALSE.
- "Fecha_Observada_Fondo": Si la variable "Observada_de_Fondo" es TRUE, se debe extraer la fecha de la fila donde se encontró el texto "Resolución de observaciones de fondo de marca".
- Variable "Apelaciones": Si cualquiera de los valores de la columna "Descripción" contiene el texto "Recurso de apelación" se guarda la variable con el valor TRUE sino FALSE.
- "IPT": Si cualquiera de los valores de la columna "Descripción" contiene el texto "IPT o "IPTV" se guarda la variable con el valor TRUE sino FALSE.

## Instalación

Pre-requisitos:
- Python 3.11.3: https://www.python.org/downloads/release/python-3113/
- Pip (packet manager para Python): https://pip.pypa.io/en/stable/installation/
- Requests: pip install requests
- Pandas: pip install pandas
- Clonar el proyecto:
```bash
  git clone https://github.com/vivascarlosandres/crawler_buscador_marcas.git
```

## Configuración de variables
Se deben configurar las variables internas del código según las necesidades. Estas variables se encuentran en la sección de "Configuración" del código:

- numeros_registro = Lista de números de registro para la búsqueda.
- output_file = Nombre y ubicación del archivo JSON de salida.
- use_proxy = True / False
- proxies = Si 'use_proxy = True', se deben configurar los proxies correspondientes.
- num_threads = Número de hilos de ejecución concurrente.

## Ejecución del código
Una vez que las bibliotecas estén instaladas y las variables configuradas, se puede ejecutar el código:
```bash
  python buscador.py
```
Se obtendrá el archivo en formato JSON con los resultados de la búsqueda.

## Explicación del proceso de desarrollo del código

1. Importación de módulos:
```bash
import json
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
```
En esta sección, se importan los módulos necesarios para el funcionamiento del programa. El módulo **'json'** se utiliza para trabajar con datos en formato JSON, **'requests'** se utiliza para realizar solicitudes HTTP, **'pandas'** se utiliza para manipular y analizar datos en forma de DataFrame, y **'ThreadPoolExecutor'** y **'as_completed'** se utilizan para realizar tareas en paralelo.

2. Definición de la clase 'BuscarMarcas':
```bash
class BuscarMarcas:
    def __init__(self, url1, url2, use_proxy=False, proxies=None, num_threads=5, output_file="resultados.json"):
        self.url1 = url1
        self.url2 = url2
        self.use_proxy = use_proxy
        self.proxies = proxies
        self.num_threads = num_threads
        self.output_file = output_file
```
En esta sección, se define la clase BuscarMarcas, que encapsula la funcionalidad para buscar marcas en un sitio web. La clase tiene un método constructor **'__init__()**' que inicializa los atributos de la clase, como las URL de búsqueda, el uso de proxy, los proxies, el número de hilos de ejecución y el archivo de salida JSON.

3. Definición del método 'process_numero_registro()':
```bash
def process_numero_registro(self, numero):
    resultado = {}

    payload = {
        "Hash": "",
        "IDW": "",
        "LastNumSol": 0,
        "param1": "",
        "param10": "",
        "param11": "",
        "param12": "",
        "param13": "",
        "param14": "",
        "param15": "",
        "param16": "",
        "param17": "1",
        "param2": numero,
        "param3": "",
        "param4": "",
        "param5": "",
        "param6": "",
        "param7": "",
        "param8": "",
        "param9": "",
        "responseCaptcha": "este texto no se validará"
    }
```
Este método se encarga de procesar un número de registro específico. Recibe un número de registro como entrada y crea un diccionario vacío llamado **'resultado'** para almacenar los datos resultantes de la búsqueda. También se define un diccionario llamado **'payload'** que contiene los parámetros necesarios para realizar la solicitud HTTP.

4. Inicio de la sesión de requests:
```bash
with requests.session() as s:
```
Se utiliza un bloque **'with'** para crear y gestionar una sesión de requests. Esto garantiza que los recursos de red se limpien adecuadamente después de su uso.

5. Configuración de proxies (si se utilizan):
```bash
if self.use_proxy and self.proxies:
    s.proxies = self.proxies
```
Esta sección verifica si se debe utilizar un proxy y si se han proporcionado proxies personalizados. Si es así, se configura el objeto de sesión **'s'** con los proxies proporcionados.

6. Realización de la solicitud de POST para buscar marcas:
```bash
data = json.loads(s.post(self.url1, json=payload).json()['d'])
```
Aquí se realiza una solicitud POST utilizando la sesión de requests. Se envía la URL de búsqueda **'self.url1'** y los datos **'payload'** en formato JSON. La respuesta se convierte en un diccionario Python utilizando **'json.loads()'**.

7. Procesamiento de los datos de las marcas encontradas:
```bash
for m in data['Marcas']:
    payload = {
        "Hash": data['Hash'],
        "IDW": "",
        "numeroSolicitud": m['id']
    }
    data = json.loads(s.post(self.url2, json=payload).json()['d'])
    df = pd.DataFrame(data['Marca']['Instancias'])

    if any('Resolución de observaciones de fondo de marca' in desc for desc in df['EstadoDescripcion']):
        observada_de_fondo = True
        fecha_observada_fondo = df.loc[df['EstadoDescripcion'].str.contains('Resolución de observaciones de fondo de marca'), 'Fecha'].values[0]
    if any('Recurso de apelación' in desc for desc in df['EstadoDescripcion']):
        apelaciones = True
    if any('IPT' in desc or 'IPTV' in desc for desc in df['EstadoDescripcion']):
        ipt = True
```
En esta sección se itera sobre las marcas encontradas en los datos recibidos de la primera solicitud. Para cada marca, se realiza una segunda solicitud POST utilizando la URL **'self.url2'** y se obtienen los datos adicionales. Luego, se crea un DataFrame de pandas (**'df'**) utilizando los datos de las instancias de la marca. Se verifican diferentes condiciones en los datos para establecer los valores de las variables **'observada_de_fondo', 'fecha_observada_fondo', 'apelaciones' e 'ipt'**.

8. Almacenamiento de los resultados en el diccionario 'resultado':
```bash
resultado["Numero de Registro"] = numero
resultado["Observada de Fondo"] = observada_de_fondo
resultado["Fecha Observada de Fondo"] = fecha_observada_fondo
resultado["Apelaciones"] = apelaciones
resultado["IPT"] = ipt
```
Los resultados de la búsqueda se almacenan en el diccionario **'resultado'** utilizando claves específicas.

9. Manejo de errores y excepciones:
```bash
except (requests.RequestException, json.JSONDecodeError) as e:
    # Manejo de errores de solicitud HTTP o decodificación JSON
    print(f"Error al procesar el número de registro {numero}: {str(e)}")
    return None
except (KeyError, IndexError) as e:
    # Manejo de errores de acceso a datos en el DataFrame
    print(f"Error al acceder a los datos para el número de registro {numero}: {str(e)}")
    return None
```
Se utilizan bloques **'try-except'** para manejar posibles errores y excepciones que puedan ocurrir durante la ejecución del código. Si se produce un error, se imprime un mensaje de error específico y se devuelve **'None'** para indicar un resultado no válido.

10. Retorno del diccionario 'resultado':
```bash
return resultado
```
El método **'process_numero_registro()'** devuelve el diccionario **'resultado'** que contiene los resultados de la búsqueda para un número de registro específico.

11. Definición del método 'crawl_registros()':
```bash
def crawl_registros(self, numeros_registro):
    print("Iniciando obtención de datos...")
    resultados_totales = []
    with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
        futures = [executor.submit(self.process_numero_registro, numero) for numero in numeros_registro]
        for future in as_completed(futures):
            resultado = future.result()
            if resultado is not None:
                resultados_totales.append(resultado)

    with open(self.output_file, "w") as file:
        json.dump(resultados_totales, file)

    print("Los resultados se han guardado en '{}'.".format(self.output_file))
```
Este método se encarga de realizar la búsqueda de marcas para una lista de números de registro. Utiliza la programación en paralelo para mejorar la eficiencia del proceso. Se crea una instancia de **'ThreadPoolExecutor'** con un número máximo de hilos de ejecución (**'self.num_threads'**). Luego, se ejecuta el método **'process_numero_registro()'** para cada número de registro en la lista utilizando **'executor.submit()'**. Los resultados válidos se agregan a la lista **'resultados_totales'**. Finalmente, los resultados se guardan en un archivo JSON especificado por **'self.output_file'**.

12. Configuración y ejecución del crawler:
```bash
url1 = 'https://ion.inapi.cl/Marca/BuscarMarca.aspx/FindMarcas'
url2 = 'https://ion.inapi.cl/Marca/BuscarMarca.aspx/FindMarcaByNumeroSolicitud'
numeros_registro = ['1236216', '1236222', '1236223', '1236224', '1236226', '1236227', '1236275', '1236319', '1236450', '1236470', '1236472', '1236471', '1236482']
output_file = "resultados.json"  # Nombre y ubicación del archivo JSON de salida

# Proxies (si se utilizan)
use_proxy = False  # Configurar como True si se desea utilizar proxies
proxies = {
    'http': 'http://your-proxy-url',
    'https': 'https://your-proxy-url'
}  # Configurar los proxies correspondientes si se utilizan

# Paralelismo
num_threads = 10  # Número de hilos de ejecución concurrentes

# Crear una instancia del crawler
crawler = BuscarMarcas(url1, url2, use_proxy, proxies, num_threads, output_file)

# Ejecutar el crawler
crawler.crawl_registros(numeros_registro)
```
En esta sección se configuran las variables necesarias, como las URL de búsqueda, la lista de números de registro, el archivo de salida y la configuración de proxies y paralelismo. Luego se crea una instancia de la clase **'BuscarMarcas'** con los parámetros correspondientes y se ejecuta el método **'crawl_registros()'** para iniciar la búsqueda y guardar los resultados.
