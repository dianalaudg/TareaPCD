# Sistema de Inventario Modular

Este proyecto implementa un sistema de inventario para una tienda de tecnología.

## Funcionalidades

- Leer inventario desde un archivo CSV
- Validar datos de productos
- Ignorar registros inválidos
- Detectar productos con stock bajo
- Generar reporte de reorden

## Estructura

- `models/` → Clases del dominio (Producto)
- `utils/` → Validaciones y manejo de archivos
- `data/` → Archivo CSV de entrada
- `outputs/` → Reporte generado
- `main.py` → Programa principal

## Ejecución

```bash
python main.py