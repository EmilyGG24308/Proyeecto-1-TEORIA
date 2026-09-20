OPERADORES = {'|', '.', '*'}
PRECEDENCIA = {'|': 1, '.': 2, '*': 3}


def es_operando(c):
    """Un operando es cualquier simbolo del alfabeto (no operador, no parentesis)."""
    return c not in OPERADORES and c not in ('(', ')')


def insertar_concatenacion(regex):
    """Inserta el operador explicito '.' donde la concatenacion es implicita.
    Ej: 'ab' -> 'a.b' ,  '(a|b)*ab' -> '(a|b)*.a.b'
    """
    salida = []
    for i, c in enumerate(regex):
        salida.append(c)
        if i + 1 < len(regex):
            siguiente = regex[i + 1]
            puede_terminar_expr = es_operando(c) or c in (')', '*')
            puede_empezar_expr = es_operando(siguiente) or siguiente == '('
            if puede_terminar_expr and puede_empezar_expr:
                salida.append('.')
    return ''.join(salida)


def a_postfix(regex):
    """Convierte una expresion regular en notacion infix a notacion postfix."""
    regex = insertar_concatenacion(regex)
    salida = []
    pila = []
    for c in regex:
        if es_operando(c):
            salida.append(c)
        elif c == '(':
            pila.append(c)
        elif c == ')':
            while pila and pila[-1] != '(':
                salida.append(pila.pop())
            pila.pop()  # descarta el '('
        else:  # es un operador: | . *
            while pila and pila[-1] != '(' and PRECEDENCIA[pila[-1]] >= PRECEDENCIA[c]:
                salida.append(pila.pop())
            pila.append(c)
    while pila:
        salida.append(pila.pop())
    return ''.join(salida)
