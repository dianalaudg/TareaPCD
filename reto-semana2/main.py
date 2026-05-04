import sys


def fahrenheit_a_celsius(f):
    return (f - 32) * 5 / 9


def clasificar(celsius):
    if celsius < 0:
        return "Congelante"
    elif celsius <= 15:
        return "Frio"
    elif celsius <= 25:
        return "Templado"
    elif celsius <= 35:
        return "Calido"
    else:
        return "Extremo"


def main():
    print("ciudad,temperatura_celsius,clasificacion")

    primera_linea = True

    for linea in sys.stdin:
        linea = linea.strip()

        if primera_linea:
            primera_linea = False
            continue

        if not linea:
            continue

        partes = linea.split(",")

        if len(partes) != 3:
            continue

        ciudad = partes[0].strip()
        temp_str = partes[1].strip()
        unidad = partes[2].strip().upper()

        if unidad not in ["C", "F"]:
            continue

        try:
            temp = float(temp_str)
        except:
            continue

        if unidad == "F":
            celsius = fahrenheit_a_celsius(temp)
        else:
            celsius = temp

        clasificacion = clasificar(celsius)

        print(f"{ciudad},{celsius:.1f},{clasificacion}")


if __name__ == "__main__":
    main()