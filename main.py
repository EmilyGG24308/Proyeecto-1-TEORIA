import sys

from shunting_yard import a_postfix
from thompson import construir_afn

sys.stdout.reconfigure(encoding="utf-8")  # para poder imprimir el simbolo epsilon (ε) en Windows


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


if __name__ == "__main__":
    main()
