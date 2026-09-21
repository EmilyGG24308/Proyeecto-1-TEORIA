import os
import sys

from shunting_yard import a_postfix
from thompson import construir_afn
from subconjuntos import construir_afd
from minimizacion import minimizar_afd
from simulacion import simular_afn, simular_afd
from graficar import graficar_afn, graficar_afd

sys.stdout.reconfigure(encoding="utf-8")  # para poder imprimir el simbolo epsilon

CARPETA_SALIDA = "output"


def procesar_regex(regex, w, indice):
    postfix = a_postfix(regex)
    print(f"Infix:   {regex}")
    print(f"Postfix: {postfix}")

    afn = construir_afn(postfix)
    afn.imprimir()
    print()

    afd = construir_afd(afn)
    print("AFD (por construccion de subconjuntos):")
    afd.imprimir()
    print()

    afd_min = minimizar_afd(afd)
    print("AFD minimizado:")
    afd_min.imprimir()
    print()

    base = os.path.join(CARPETA_SALIDA, f"regex_{indice}")
    graficar_afn(afn, f"{base}_afn")
    graficar_afd(afd, f"{base}_afd")
    graficar_afd(afd_min, f"{base}_afd_min")
    print(f"Imagenes guardadas en {base}_afn.png / _afd.png / _afd_min.png")
    print()

    r_afn = "si" if simular_afn(afn, w) else "no"
    r_afd = "si" if simular_afd(afd, w) else "no"
    r_min = "si" if simular_afd(afd_min, w) else "no"
    print(f'Cadena w = "{w}"')
    print(f"  Pertenece a L(r) segun AFN:         {r_afn}")
    print(f"  Pertenece a L(r) segun AFD:         {r_afd}")
    print(f"  Pertenece a L(r) segun AFD minimo:  {r_min}")


def main():
    w = sys.argv[1] if len(sys.argv) > 1 else input("Ingrese la cadena w a evaluar: ").strip()

    try:
        with open("input.txt", encoding="utf-8") as f:
            lineas = f.readlines()
    except FileNotFoundError:
        print("Error: no se encontro el archivo input.txt")
        return

    os.makedirs(CARPETA_SALIDA, exist_ok=True)

    for num_linea, linea in enumerate(lineas, start=1):
        regex = linea.strip()
        if not regex:
            continue
        print("=" * 50)
        try:
            procesar_regex(regex, w, num_linea)
        except Exception as error:
            print(f"[Linea {num_linea}] Error procesando '{regex}': {error}")
        print()


if __name__ == "__main__":
    main()
