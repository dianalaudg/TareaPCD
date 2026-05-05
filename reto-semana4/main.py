from models.producto import Producto
from utils.validators import validar_producto
from utils.io import leer_inventario, escribir_reporte

ARCHIVO_INVENTARIO = "data/inventario.csv"
ARCHIVO_REPORTE = "outputs/reporte_inventario.csv"


def crear_productos(datos_raw):
    productos = []

    for datos in datos_raw:
        es_valido, error = validar_producto(
            datos.get("sku"),
            datos.get("nombre"),
            datos.get("categoria"),
            datos.get("precio"),
            datos.get("stock"),
            datos.get("stock_minimo")
        )

        if not es_valido:
            print(f"[IGNORADO] {error}")
            continue

        producto = Producto(
            datos["sku"],
            datos["nombre"],
            datos["categoria"],
            float(datos["precio"]),
            int(datos["stock"]),
            int(datos["stock_minimo"])
        )

        productos.append(producto)

    return productos


def main():
    print("=" * 50)
    print("SISTEMA DE INVENTARIO - REPORTE DE REORDEN")
    print("=" * 50)

    datos_raw = leer_inventario(ARCHIVO_INVENTARIO)
    productos = crear_productos(datos_raw)

    necesitan = [p for p in productos if p.necesita_reorden()]
    necesitan.sort(key=lambda p: p.unidades_faltantes(), reverse=True)

    print("\nPRODUCTOS QUE NECESITAN REORDEN:")
    for p in necesitan:
        print(p)

    escribir_reporte(necesitan, ARCHIVO_REPORTE)

    print(f"\nReporte generado en: {ARCHIVO_REPORTE}")


if __name__ == "__main__":
    main()