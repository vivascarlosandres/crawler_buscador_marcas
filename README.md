![Logo](https://imgur.com/YL4RHxX.png)

# Web Crawler Buscador de Marcas

## Índice

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

