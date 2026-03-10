import sys

# Filtrar caracteres (quedarse solo con digitos, punto y signo negativo)
def limpiar(texto):
    caracteres_validos = '0123456789.-'
    resultado = ''
    for char in texto:
        if char in caracteres_validos:
            resultado += char
    return resultado

# Convertir string a numero y truncar
def convertir_a_entero(texto):
    """Convierte texto a entero, truncando decimales."""
    if not texto:  # Si esta vacio
        return 0
    try:
        numero = float(texto)  # Primero a float
        return int(numero)     # Luego truncar a int
    except ValueError:
        return 0  # Si no se puede convertir, es 0

def procesar_linea(linea):
    """
    Procesa una linea completa: separa por comas, 
    limpia espacios y suma los valores procesados.
    """
    linea = linea.strip()
    if not linea:
        return 0
    
    # Separar por comas
    valores = linea.split(',')
    
    # Quitar espacios de cada elemento y procesar
    suma_total = 0
    for v in valores:
        v_sin_espacios = v.strip()
        v_limpio = limpiar(v_sin_espacios)
        suma_total += convertir_a_entero(v_limpio)
        
    return suma_total

def main():
    """
    Lee de stdin linea por linea (Opcion 1 del profesor)
    """
    for linea in sys.stdin:
        resultado = procesar_linea(linea)
        print(resultado)

if __name__ == "__main__":
    main()
    