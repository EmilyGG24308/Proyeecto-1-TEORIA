import sys

from shunting_yard import a_postfix
from thompson import construir_afn
from subconjuntos import construir_afd
from minimizacion import minimizar_afd

sys.stdout.reconfigure(encoding="utf-8")  # para poder imprimir el simbolo epsilon 


def main():
    with open("input.txt", encoding="utf-8") as f:
        for linea in f:
            regex = linea.strip()
            if not regex:
                continue
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


if __name__ == "__main__":
    main()
