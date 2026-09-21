import os
import shutil

import graphviz


def _asegurar_graphviz_en_path():
    """Si 'dot' no esta en el PATH de esta terminal, lo busca en su carpeta
    de instalacion habitual en Windows y lo agrega para esta ejecucion."""
    if shutil.which("dot"):
        return
    posibles_rutas = [r"C:\Program Files\Graphviz\bin", r"C:\Program Files (x86)\Graphviz\bin"]
    for ruta in posibles_rutas:
        if os.path.isdir(ruta):
            os.environ["PATH"] += os.pathsep + ruta
            return


_asegurar_graphviz_en_path()


def _nuevo_grafo():
    return graphviz.Digraph(format="png", graph_attr={"rankdir": "LR"})


def _agregar_estados_e_inicio(grafo, num_estados, aceptacion, inicio):
    for estado in range(num_estados):
        forma = "doublecircle" if estado in aceptacion else "circle"
        grafo.node(str(estado), shape=forma)
    grafo.node("inicio_punto", shape="point")
    grafo.edge("inicio_punto", str(inicio))


def _agregar_transiciones(grafo, etiquetas_por_arista):
    """etiquetas_por_arista: dict {(origen, destino): [lista de etiquetas]}"""
    for (origen, destino), etiquetas in etiquetas_por_arista.items():
        grafo.edge(str(origen), str(destino), label=",".join(etiquetas))


def graficar_afn(afn, ruta_salida):
    grafo = _nuevo_grafo()
    _agregar_estados_e_inicio(grafo, afn.num_estados, {afn.aceptacion}, afn.inicio)

    etiquetas_por_arista = {}
    for origen, transiciones in afn.transiciones.items():
        for simbolo, destino in transiciones:
            etiqueta = simbolo if simbolo is not None else "ε"
            etiquetas_por_arista.setdefault((origen, destino), []).append(etiqueta)

    _agregar_transiciones(grafo, etiquetas_por_arista)
    grafo.render(ruta_salida, cleanup=True)


def graficar_afd(afd, ruta_salida):
    grafo = _nuevo_grafo()
    _agregar_estados_e_inicio(grafo, afd.num_estados, afd.aceptacion, afd.inicio)

    etiquetas_por_arista = {}
    for origen, transiciones in afd.transiciones.items():
        for simbolo, destino in transiciones.items():
            etiquetas_por_arista.setdefault((origen, destino), []).append(simbolo)

    _agregar_transiciones(grafo, etiquetas_por_arista)
    grafo.render(ruta_salida, cleanup=True)
