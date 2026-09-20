def main():
    with open("input.txt", encoding="utf-8") as f:
        for linea in f:
            regex = linea.strip()
            if not regex:
                continue
            print(f"Expresion leida: {regex}")


if __name__ == "__main__":
    main()
