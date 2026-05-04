# Analizador de Ventas

## Descripción

Este programa en Python procesa un archivo CSV de transacciones de ventas y genera un reporte consolidado por producto.

A partir de múltiples registros individuales, el sistema calcula métricas clave para cada producto, permitiendo identificar cuáles generan mayor ingreso.

---

## Funcionalidades

El programa realiza las siguientes operaciones:

- Lee datos desde stdin en formato CSV  
- Ignora líneas inválidas o mal formateadas  
- Agrupa transacciones por producto  
- Calcula:
  - Unidades vendidas
  - Ingreso total
  - Precio promedio  
- Ordena los resultados por ingreso total (descendente)  
- Genera salida en formato CSV

---

## Formato de Entrada

El programa espera un CSV con la siguiente estructura:

fecha,producto,cantidad,precio_unitario 2026-01-01,Laptop,2,15000.00 2026-01-02,Mouse,10,250.00

### Reglas:
- La primera línea es el encabezado
- Cada línea representa una transacción
- Se ignoran líneas inválidas:
  - Columnas incompletas
  - Valores no numéricos en cantidad o precio

---

## Formato de Salida

El programa imprime un CSV con el siguiente formato:

```
producto,unidades_vendidas,ingreso_total,precio_promedio
Laptop,3,44500.00,14833.33
Mouse,18,4500.00,25

##Autor

De la Luz García Diana Laura

## Cómo ejecutar el programa 
Get-Content tests/entrada.txt | python main.py > tests/salida_generada.txt
