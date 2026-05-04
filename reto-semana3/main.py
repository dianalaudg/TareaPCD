import sys

def main():
    # Diccionario para agrupar por producto
    productos = {}

    primera_linea = True

    # Leer todas las líneas desde stdin
    for linea in sys.stdin:
        linea = linea.strip()

        # Saltar encabezado
        if primera_linea:
            primera_linea = False
            continue

        # Saltar líneas vacías
        if not linea:
            continue

        # Parsear línea
        partes = linea.split(",")
        if len(partes) != 4:
            continue  # Ignorar líneas inválidas

        fecha = partes[0]
        producto = partes[1]

        # Convertir cantidad y precio (con manejo de errores)
        try:
            cantidad = int(partes[2])
            precio = float(partes[3])
        except ValueError:
            continue  # Ignorar si no son números válidos

        # Crear entrada si no existe (EVITA KeyError)
        if producto not in productos:
            productos[producto] = {
                "unidades": 0,
                "ingreso": 0.0
            }

        # Acumular valores
        productos[producto]["unidades"] += cantidad
        productos[producto]["ingreso"] += cantidad * precio

    # Calcular precio promedio (EVITA división por cero)
    for prod in productos:
        unidades = productos[prod]["unidades"]
        ingreso = productos[prod]["ingreso"]
        productos[prod]["promedio"] = ingreso / unidades if unidades > 0 else 0

    # Ordenar por ingreso descendente (CORRECTO)
    productos_ordenados = sorted(
        productos.items(),
        key=lambda x: x[1]["ingreso"],
        reverse=True
    )

    # Imprimir salida CSV (FORMATO EXACTO)
    print("producto,unidades_vendidas,ingreso_total,precio_promedio")
    for nombre, datos in productos_ordenados:
        print(f"{nombre},{datos['unidades']},{datos['ingreso']:.2f},{datos['promedio']:.2f}")


if __name__ == "__main__":
    main()