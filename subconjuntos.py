class AFD:
    def __init__(self):
        self.transiciones = {}  # estado -> {simbolo: estado_destino}
        self.inicio = None
        self.aceptacion = set()
        self.num_estados = 0

    def nuevo_estado(self):
        estado = self.num_estados
        self.num_estados += 1
        self.transiciones[estado] = {}
        return estado

    def agregar_transicion(self, origen, simbolo, destino):
        self.transiciones[origen][simbolo] = destino

    def imprimir(self):
        print(f"Estados: {self.num_estados} (0 a {self.num_estados - 1})")
        print(f"Estado inicial: {self.inicio}")
        print(f"Estados de aceptacion: {sorted(self.aceptacion)}")
        print("Transiciones:")
        for origen, dic in self.transiciones.items():
            for simbolo, destino in dic.items():
                print(f"  {origen} --{simbolo}--> {destino}")


def epsilon_closure(afn, estados):
    """Todos los estados del AFN alcanzables desde 'estados' usando solo epsilon-transiciones."""
    pila = list(estados)
    clausura = set(estados)
    while pila:
        estado = pila.pop()
        for simbolo, destino in afn.transiciones[estado]:
            if simbolo is None and destino not in clausura:
                clausura.add(destino)
                pila.append(destino)
    return frozenset(clausura)


def mover(afn, estados, simbolo):
    """Estados del AFN alcanzables desde 'estados' leyendo exactamente 'simbolo'."""
    destinos = set()
    for estado in estados:
        for s, destino in afn.transiciones[estado]:
            if s == simbolo:
                destinos.add(destino)
    return destinos


def obtener_alfabeto(afn):
    simbolos = set()
    for transiciones in afn.transiciones.values():
        for simbolo, _ in transiciones:
            if simbolo is not None:
                simbolos.add(simbolo)
    return simbolos


def construir_afd(afn):
    """Convierte un AFN en un AFD equivalente usando construccion de subconjuntos."""
    alfabeto = sorted(obtener_alfabeto(afn))
    afd = AFD()

    inicio_cierre = epsilon_closure(afn, {afn.inicio})
    conjuntos_vistos = {inicio_cierre: afd.nuevo_estado()}
    afd.inicio = conjuntos_vistos[inicio_cierre]
    pendientes = [inicio_cierre]

    while pendientes:
        actual = pendientes.pop()
        origen = conjuntos_vistos[actual]
        for simbolo in alfabeto:
            destino_conjunto = epsilon_closure(afn, mover(afn, actual, simbolo))
            if not destino_conjunto:
                continue
            if destino_conjunto not in conjuntos_vistos:
                conjuntos_vistos[destino_conjunto] = afd.nuevo_estado()
                pendientes.append(destino_conjunto)
            afd.agregar_transicion(origen, simbolo, conjuntos_vistos[destino_conjunto])

    for conjunto, estado in conjuntos_vistos.items():
        if afn.aceptacion in conjunto:
            afd.aceptacion.add(estado)

    return afd
