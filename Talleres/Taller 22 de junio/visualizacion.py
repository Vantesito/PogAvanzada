"""
visualizacion.py
================
Visualizacion grafica con matplotlib para los dos escenarios.

  visualizar_laberinto : barreras, celdas visitadas, camino final, inicio y meta.
  visualizar_grafo     : nodos visitados y camino resaltado sobre el grafo.
"""

import matplotlib
matplotlib.use("Agg")          # backend sin ventana, para guardar figuras
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np


# --------------------------------------------------------------------------- #
#  Laberinto                                                                  #
# --------------------------------------------------------------------------- #
def visualizar_laberinto(prob, resultado, titulo="", ruta_salida=None, ax=None):
    """Pinta el laberinto:
         - negro  : barrera
         - blanco : libre
         - celeste: celda visitada (expandida)
         - naranja: camino final
         - verde  : inicio    - rojo : objetivo
    """
    filas, cols = prob.filas, prob.cols
    # 0 libre, 1 barrera, 2 visitado, 3 camino, 4 inicio, 5 objetivo
    grid = np.array([[1 if prob.matriz[f][c] == 1 else 0
                      for c in range(cols)] for f in range(filas)], dtype=float)

    for estado in resultado.visitados:
        f, c = estado
        if grid[f, c] == 0:
            grid[f, c] = 2
    if resultado.camino:
        for f, c in resultado.camino:
            grid[f, c] = 3
    sf, sc = prob.inicio
    gf, gc = prob.objetivo
    grid[sf, sc] = 4
    grid[gf, gc] = 5

    colores = ["white", "black", "#9ecae1", "#fd8d3c", "#31a354", "#de2d26"]
    cmap = matplotlib.colors.ListedColormap(colores)
    norm = matplotlib.colors.BoundaryNorm(range(len(colores) + 1), cmap.N)

    creado = ax is None
    if creado:
        fig, ax = plt.subplots(figsize=(cols * 0.45 + 2, filas * 0.45 + 1.5))

    ax.imshow(grid, cmap=cmap, norm=norm)
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, filas, 1), minor=True)
    ax.grid(which="minor", color="#cccccc", linewidth=0.5)
    ax.set_xticks([]); ax.set_yticks([])

    sub = "sin solucion" if not resultado.exito else (
        f"pasos={resultado.longitud_camino - 1}  costo={_fmt(resultado.costo)}  "
        f"visitados={len(resultado.visitados)}")
    ax.set_title(f"{titulo}\n{sub}", fontsize=10)

    if creado:
        leyenda = [
            Patch(facecolor="#31a354", label="Inicio"),
            Patch(facecolor="#de2d26", label="Objetivo"),
            Patch(facecolor="#9ecae1", label="Visitado"),
            Patch(facecolor="#fd8d3c", label="Camino"),
            Patch(facecolor="black", label="Barrera"),
        ]
        ax.legend(handles=leyenda, loc="upper left",
                  bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
        fig.tight_layout()
        if ruta_salida:
            fig.savefig(ruta_salida, dpi=120, bbox_inches="tight")
            plt.close(fig)
    return ax


# --------------------------------------------------------------------------- #
#  Grafo                                                                       #
# --------------------------------------------------------------------------- #
def visualizar_grafo(prob, resultado, titulo="", ruta_salida=None, ax=None):
    """Dibuja el grafo con networkx; resalta nodos visitados y el camino."""
    import networkx as nx

    G = nx.Graph()
    for nodo, vecinos in prob.ady.items():
        G.add_node(nodo)
        for vecino, costo in vecinos:
            G.add_edge(nodo, vecino, weight=costo)

    if prob.coordenadas:
        pos = {n: prob.coordenadas.get(n, (0, 0)) for n in G.nodes}
    else:
        pos = nx.spring_layout(G, seed=42)

    creado = ax is None
    if creado:
        fig, ax = plt.subplots(figsize=(8, 6))

    visitados = set(resultado.visitados)
    camino = resultado.camino or []
    aristas_camino = set(zip(camino, camino[1:]))

    colores_nodo = []
    for n in G.nodes:
        if n == prob.inicio:
            colores_nodo.append("#31a354")
        elif n == prob.objetivo:
            colores_nodo.append("#de2d26")
        elif n in set(camino):
            colores_nodo.append("#fd8d3c")
        elif n in visitados:
            colores_nodo.append("#9ecae1")
        else:
            colores_nodo.append("#eeeeee")

    colores_arista, anchos = [], []
    for u, v in G.edges:
        if (u, v) in aristas_camino or (v, u) in aristas_camino:
            colores_arista.append("#fd8d3c"); anchos.append(3.0)
        else:
            colores_arista.append("#bbbbbb"); anchos.append(1.0)

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=colores_arista, width=anchos)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colores_nodo,
                           edgecolors="#333333", node_size=700)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight="bold")
    etiquetas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, ax=ax, font_size=8)

    sub = "sin solucion" if not resultado.exito else (
        f"camino={' -> '.join(map(str, camino))}   costo={_fmt(resultado.costo)}   "
        f"visitados={len(resultado.visitados)}")
    ax.set_title(f"{titulo}\n{sub}", fontsize=10)
    ax.axis("off")

    if creado:
        fig.tight_layout()
        if ruta_salida:
            fig.savefig(ruta_salida, dpi=120, bbox_inches="tight")
            plt.close(fig)
    return ax


def _fmt(x):
    if x is None:
        return "-"
    return str(int(x)) if float(x) == int(x) else f"{x:.2f}"


# --------------------------------------------------------------------------- #
#  Comparativa: 4 algoritmos en una sola figura                               #
# --------------------------------------------------------------------------- #
def comparar(prob, resultados, tipo, ruta_salida):
    """resultados: dict nombre_algoritmo -> Resultado. tipo: 'laberinto'|'grafo'"""
    fig, axes = plt.subplots(2, 2, figsize=(13, 11))
    dibujar = visualizar_laberinto if tipo == "laberinto" else visualizar_grafo
    for ax, (nombre, res) in zip(axes.flat, resultados.items()):
        dibujar(prob, res, titulo=nombre, ax=ax)
    fig.suptitle(f"Comparacion de algoritmos sobre {tipo}", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(ruta_salida, dpi=120, bbox_inches="tight")
    plt.close(fig)
