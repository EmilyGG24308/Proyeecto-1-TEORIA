from shunting_yard import a_postfix


def main():
    with open("input.txt", encoding="utf-8") as f:
        for linea in f:
            regex = linea.strip()
            if not regex:
                continue
            postfix = a_postfix(regex)
            print(f"Infix:   {regex}")
            print(f"Postfix: {postfix}")
            print()


if __name__ == "__main__":
    main()
