from subconjuntos import epsilon_closure, mover


def simular_afn(afn, cadena):
    """True si 'cadena' pertenece al lenguaje reconocido por el AFN."""
    actuales = epsilon_closure(afn, {afn.inicio})
    for simbolo in cadena:
        actuales = epsilon_closure(afn, mover(afn, actuales, simbolo))
        if not actuales:
            return False
    return afn.aceptacion in actuales


def simular_afd(afd, cadena):
    """True si 'cadena' pertenece al lenguaje reconocido por el AFD."""
    estado = afd.inicio
    for simbolo in cadena:
        estado = afd.transiciones[estado].get(simbolo)
        if estado is None:
            return False
    return estado in afd.aceptacion
