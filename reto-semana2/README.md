# Clasificador de Temperaturas

Este programa procesa un archivo CSV desde la entrada estándar (stdin), convierte temperaturas a Celsius y las clasifica según su valor.

## Descripción

Cada línea de entrada contiene:
ciudad,temperatura,unidad

El programa:
- Convierte temperaturas en Fahrenheit a Celsius
- Clasifica la temperatura
- Ignora líneas inválidas

## Cómo ejecutar

En terminal:

```bash
python main.py < entrada.txt

# EJEMPLO DE ENTRADA 
ciudad,temperatura,unidad
CDMX,22,C
Nueva York,50,F
Moscu,-10,C
Miami,95,F

# EJEMPLO DE SALIDA

ciudad,temperatura_celsius,clasificacion
CDMX,22.0,Templado
Nueva York,10.0,Frio
Moscu,-10.0,Congelante
Miami,35.0,Calido

 Clasificación

* < 0 → Congelante
* 0 a 15 → Frio
* 16 a 25 → Templado
* 26 a 35 → Calido
* 35 → Extremo

 Consideraciones

* Se ignoran líneas vacías
* Se ignoran valores no numéricos
* Se ignoran unidades inválidas
* Se manejan espacios extra
* La salida tiene 1 decimal

AUTOR

De la Luz García Diana Laura

## EJECUTAR EL PROGRAMA
Get-Content tests/entrada.txt | python main.py | Out-File -Encoding ascii tests/salida.txt