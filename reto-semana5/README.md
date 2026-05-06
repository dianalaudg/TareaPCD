# Reto Semana 5 - Perfilador de Datasets CSV

## Descripción

Este proyecto implementa un perfilador simple de datasets en formato CSV utilizando únicamente la biblioteca estándar de Python.

El programa analiza automáticamente las columnas de un archivo CSV e infiere información relevante como:

- Tipo de dato inferido
- Cantidad de valores nulos
- Porcentaje de valores nulos
- Cantidad de valores únicos
- Porcentaje de valores únicos
- Ejemplo de valor encontrado

El resultado del análisis se genera en un nuevo archivo CSV.

---

## Estructura del Proyecto

```text
reto-semana5/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── ventas.csv
│   ├── empleados.csv
│   └── sensores.csv
│
└── outputs/
    ├── perfil_ventas.csv
    ├── perfil_empleados.csv
    └── perfil_sensores.csv

## INSTALACIÓN 
git clone <https://github.com/dianalaudg/TareaPCD.git>

## ENTRAR AL PROYECTO 
## BASH
cd reto-semana5

## COMO EJECUTAR PROGRAMA
#DATASET DE VENTAS
python main.py --input data/ventas.csv --output outputs/perfil_ventas.csv

#DATASET DE EMPLEADOS 

python main.py --input data/empleados.csv --output outputs/perfil_empleados.csv

##DATASET DE SENSORES

python main.py --input data/sensores.csv --output outputs/perfil_sensores.csv

##TIPOS DETECTADOS

El sistema puede inferir los siguientes tipos:
-Numericos
-Fecha
-Booleano
-Texto

##Funcionalidades

-Lectura de archivos csv
-Perfilado automatico de columnas
-Detección de valores nulos
-Inferencia de tipos de datos
-Generación de reportes csv
-Manejo basico de errores

## Autor 
De la Luz García Diana Laura
