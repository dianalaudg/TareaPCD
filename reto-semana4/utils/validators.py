def validar_sku(sku):
    if not sku or not str(sku).strip():
        return False
    return True


def validar_precio(precio):
    try:
        precio = float(precio)
        return precio >= 0
    except:
        return False


def validar_stock(stock):
    try:
        stock = int(stock)
        return stock >= 0
    except:
        return False


def validar_producto(sku, nombre, categoria, precio, stock, stock_minimo):
    if not validar_sku(sku):
        return False, "SKU inválido"

    if not nombre or not str(nombre).strip():
        return False, "Nombre vacío"

    if not validar_precio(precio):
        return False, f"Precio inválido: {precio}"

    if not validar_stock(stock):
        return False, f"Stock inválido: {stock}"

    if not validar_stock(stock_minimo):
        return False, f"Stock mínimo inválido: {stock_minimo}"

    return True, None