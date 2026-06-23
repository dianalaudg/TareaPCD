# Reto Semana 6: Validador de Códigos con Expresiones Regulares

**Programación para Ciencia de Datos — IPN | Febrero-Julio 2026**

---

## Descripción  

Sistema automático que valida códigos de productos, envíos, empleados y facturas de una empresa de logística usando expresiones regulares en Python.

El programa lee códigos desde `stdin` (uno por línea) y escribe el resultado en formato CSV a `stdout`.

---

## Formatos Soportados

| Tipo       | Formato                     | Ejemplo válido           |
|------------|-----------------------------|--------------------------|
| Producto   | `AAA-NNNN-PP`               | `TEC-0001-MX`            |
| Envío      | `ENV-YYYY-MM-DD-NNNNNN`     | `ENV-2024-03-15-001234`  |
| Empleado   | `EMP-DEP-NNNN`              | `EMP-VEN-1234`           |
| Factura    | `FAC-S-NNNNNN`              | `FAC-A-123456`           |

---

## Requisitos

- Python 3.6 o superior
- No requiere librerías externas

---

## Uso

### Linux / Mac

```bash
python main.py < codigos.txt
```

### Windows (PowerShell)

```powershell
Get-Content codigos.txt | python main.py
```

### Windows (CMD)

```cmd
type codigos.txt | python main.py
```

---

## Ejemplo

**Entrada (`codigos.txt`):**
```
TEC-0001-MX
tec-0001-MX
ENV-2024-03-15-001234
EMP-VEN-1234
FAC-A-123456
XXX-1234
```

**Salida:**
```
codigo,tipo,valido
TEC-0001-MX,producto,VALIDO
tec-0001-MX,producto,INVALIDO
ENV-2024-03-15-001234,envio,VALIDO
EMP-VEN-1234,empleado,VALIDO
FAC-A-123456,factura,VALIDO
XXX-1234,desconocido,INVALIDO
```

---

## Comparar con salida esperada

```bash
python main.py < tests/codigos.txt > mi_salida.txt
diff mi_salida.txt tests/salida_esperada.txt
```

Si no hay diferencias, ¡la solución es correcta!

---

## Estructura del Repositorio

```
reto-semana-06/
├── README.md
├── main.py
├── .gitignore
└── tests/
    ├── codigos.txt
    └── salida_esperada.txt
```

---

