from subconjuntos import AFD


def _grupo_de(particion, estado):
    """Indice del grupo que contiene 'estado', o -1 si estado es None (no hay transicion)."""
    if estado is None:
        return -1
    for i, grupo in enumerate(particion):
        if estado in grupo:
            return i
    return -1


def minimizar_afd(afd):
    """Fusiona estados equivalentes de un AFD usando el algoritmo de particion (Moore)."""
    alfabeto = sorted({simbolo for dic in afd.transiciones.values() for simbolo in dic})

    aceptacion = set(afd.aceptacion)
    no_aceptacion = set(range(afd.num_estados)) - aceptacion
    particion = [grupo for grupo in (aceptacion, no_aceptacion) if grupo]

    cambio = True
    while cambio:
        cambio = False
        nueva_particion = []
        for grupo in particion:
            subgrupos = {}
            for estado in grupo:
                firma = tuple(
                    _grupo_de(particion, afd.transiciones[estado].get(simbolo))
                    for simbolo in alfabeto
                )
                subgrupos.setdefault(firma, set()).add(estado)
            nueva_particion.extend(subgrupos.values())
            if len(subgrupos) > 1:
                cambio = True
        particion = nueva_particion

    afd_min = AFD()
    id_grupo = {}
    for grupo in particion:
        estado_nuevo = afd_min.nuevo_estado()
        for estado in grupo:
            id_grupo[estado] = estado_nuevo

    for grupo in particion:
        representante = next(iter(grupo))
        origen = id_grupo[representante]
        for simbolo, destino in afd.transiciones[representante].items():
            afd_min.agregar_transicion(origen, simbolo, id_grupo[destino])

    afd_min.inicio = id_grupo[afd.inicio]
    afd_min.aceptacion = {id_grupo[estado] for estado in afd.aceptacion}

    return afd_min
