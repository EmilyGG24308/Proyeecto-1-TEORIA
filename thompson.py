class AFN:
    def __init__(self):
        self.transiciones = {}  # estado -> lista de (simbolo_o_None, estado_destino). None = epsilon
        self.inicio = None
        self.aceptacion = None
        self.num_estados = 0

    def nuevo_estado(self):
        estado = self.num_estados
        self.num_estados += 1
        self.transiciones[estado] = []
        return estado

    def agregar_transicion(self, origen, simbolo, destino):
        self.transiciones[origen].append((simbolo, destino))

    def imprimir(self):
        print(f"Estados: {self.num_estados} (0 a {self.num_estados - 1})")
        print(f"Estado inicial: {self.inicio}")
        print(f"Estado de aceptacion: {self.aceptacion}")
        print("Transiciones:")
        for origen, lista in self.transiciones.items():
            for simbolo, destino in lista:
                etiqueta = simbolo if simbolo is not None else "ε"
                print(f"  {origen} --{etiqueta}--> {destino}")


def construir_afn(postfix):
    """Construye un AFN a partir de una expresion en postfix, usando el
    algoritmo de Thompson. Devuelve un objeto AFN."""
    afn = AFN()
    pila = []  # pila de fragmentos: cada uno es (estado_inicio, estado_aceptacion)

    for token in postfix:
        if token == '.':
            i2, a2 = pila.pop()
            i1, a1 = pila.pop()
            afn.agregar_transicion(a1, None, i2)
            pila.append((i1, a2))

        elif token == '|':
            i2, a2 = pila.pop()
            i1, a1 = pila.pop()
            s0 = afn.nuevo_estado()
            sf = afn.nuevo_estado()
            afn.agregar_transicion(s0, None, i1)
            afn.agregar_transicion(s0, None, i2)
            afn.agregar_transicion(a1, None, sf)
            afn.agregar_transicion(a2, None, sf)
            pila.append((s0, sf))

        elif token == '*':
            i1, a1 = pila.pop()
            s0 = afn.nuevo_estado()
            sf = afn.nuevo_estado()
            afn.agregar_transicion(s0, None, i1)
            afn.agregar_transicion(s0, None, sf)
            afn.agregar_transicion(a1, None, i1)
            afn.agregar_transicion(a1, None, sf)
            pila.append((s0, sf))

        else:  # simbolo del alfabeto
            i1 = afn.nuevo_estado()
            a1 = afn.nuevo_estado()
            afn.agregar_transicion(i1, token, a1)
            pila.append((i1, a1))

    afn.inicio, afn.aceptacion = pila.pop()
    return afn
