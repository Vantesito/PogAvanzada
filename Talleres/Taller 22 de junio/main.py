"""
main.py
=======
Interfaz de seleccion. Permite elegir:
  - el escenario (grafo o laberinto),
  - el algoritmo (BFS, DFS, UCS, A*),
  - el nodo/posicion inicial y objetivo,
y muestra el orden de visita, el camino, el costo y la visualizacion.

Uso interactivo:        python main.py
Uso por linea de comando:
  python main.py --escenario laberinto --algoritmo A* --inicio 0,0 --objetivo 9,9
  python main.py --escenario grafo --algoritmo UCS --inicio A --objetivo G
  python main.py --comparar laberinto      (ejecuta los 4 y genera la figura)
"""

import argparse
import os
from algoritmos import ALGORITMOS
from grafo import (ProblemaGrafo, desde_csv_lista, coordenadas_desde_csv)
from laberinto import ProblemaLaberinto, desde_csv, ascii_laberinto
import visualizacion as vis

AQUI = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(AQUI, "figuras")
os.makedirs(FIG, exist_ok=True)


# --------------------------------------------------------------------------- #
#  Construccion de cada escenario                                             #
# --------------------------------------------------------------------------- #
def construir_grafo(inicio="A", objetivo="G"):
    ady = desde_csv_lista(os.path.join(AQUI, "grafo_lista.csv"))
    coords = coordenadas_desde_csv(os.path.join(AQUI, "grafo_coords.csv"))
    return ProblemaGrafo(ady, inicio, objetivo, coordenadas=coords)


def construir_laberinto(inicio=(0, 0), objetivo=(9, 9)):
    matriz = desde_csv(os.path.join(AQUI, "laberinto.csv"))
    return ProblemaLaberinto(matriz, inicio, objetivo)


# --------------------------------------------------------------------------- #
#  Ejecucion y reporte                                                        #
# --------------------------------------------------------------------------- #
def ejecutar(prob, tipo, algoritmo, mostrar_ascii=True):
    res = ALGORITMOS[algoritmo](prob)
    print(f"\n=== {algoritmo} sobre {tipo} ===")
    if not res.exito:
        print("No se encontro camino al objetivo.")
    else:
        print("Orden de visita :", " -> ".join(map(str, res.visitados)))
        print("Camino final    :", " -> ".join(map(str, res.camino)))
        print(f"Pasos           : {res.longitud_camino - 1}")
        print(f"Costo total     : {vis._fmt(res.costo)}")
    print(f"Nodos visitados : {len(res.visitados)}")
    print(f"Frontera maxima : {res.frontera_max}")
    if tipo == "laberinto" and mostrar_ascii:
        print("\nMapa (S inicio, G meta, * camino, o visitado, # barrera):")
        print(ascii_laberinto(prob, res))
    return res


def comparar_todos(tipo, inicio=None, objetivo=None):
    if tipo == "laberinto":
        prob = construir_laberinto(*(inicio, objetivo) if inicio else ())
    else:
        prob = construir_grafo(*(inicio, objetivo) if inicio else ())
    resultados = {}
    for nombre in ("BFS", "DFS", "UCS", "A*"):
        resultados[nombre] = ejecutar(prob, tipo, nombre, mostrar_ascii=False)
    ruta = os.path.join(FIG, f"comparacion_{tipo}.png")
    vis.comparar(prob, resultados, tipo, ruta)
    print(f"\nFigura comparativa guardada en: {ruta}")
    return prob, resultados


# --------------------------------------------------------------------------- #
#  CLI                                                                         #
# --------------------------------------------------------------------------- #
def _parse_pos(texto):
    f, c = texto.split(",")
    return (int(f), int(c))


def menu_interactivo():
    print("Escenario:  1) Grafo   2) Laberinto")
    tipo = "grafo" if input("> ").strip() != "2" else "laberinto"
    print("Algoritmo:  BFS / DFS / UCS / A*")
    algoritmo = input("> ").strip().upper().replace("ESTRELLA", "*")
    if algoritmo not in ALGORITMOS:
        algoritmo = "BFS"
    if tipo == "grafo":
        inicio = input("Nodo inicial [A]: ").strip() or "A"
        objetivo = input("Nodo objetivo [G]: ").strip() or "G"
        prob = construir_grafo(inicio, objetivo)
        res = ejecutar(prob, tipo, algoritmo)
        vis.visualizar_grafo(prob, res, titulo=algoritmo,
                             ruta_salida=os.path.join(FIG, "interactivo_grafo.png"))
    else:
        inicio = _parse_pos(input("Inicio fila,col [0,0]: ").strip() or "0,0")
        objetivo = _parse_pos(input("Objetivo fila,col [9,9]: ").strip() or "9,9")
        prob = construir_laberinto(inicio, objetivo)
        res = ejecutar(prob, tipo, algoritmo)
        vis.visualizar_laberinto(prob, res, titulo=algoritmo,
                                 ruta_salida=os.path.join(FIG, "interactivo_laberinto.png"))


def main():
    ap = argparse.ArgumentParser(description="Algoritmos de busqueda: BFS, DFS, UCS, A*")
    ap.add_argument("--escenario", choices=["grafo", "laberinto"])
    ap.add_argument("--algoritmo", choices=list(ALGORITMOS))
    ap.add_argument("--inicio")
    ap.add_argument("--objetivo")
    ap.add_argument("--comparar", choices=["grafo", "laberinto"])
    args = ap.parse_args()

    if args.comparar:
        comparar_todos(args.comparar)
        return
    if not args.escenario or not args.algoritmo:
        menu_interactivo()
        return

    if args.escenario == "grafo":
        prob = construir_grafo(args.inicio or "A", args.objetivo or "G")
        res = ejecutar(prob, "grafo", args.algoritmo)
        vis.visualizar_grafo(prob, res, titulo=args.algoritmo,
                             ruta_salida=os.path.join(FIG, "salida_grafo.png"))
    else:
        ini = _parse_pos(args.inicio) if args.inicio else (0, 0)
        obj = _parse_pos(args.objetivo) if args.objetivo else (9, 9)
        prob = construir_laberinto(ini, obj)
        res = ejecutar(prob, "laberinto", args.algoritmo)
        vis.visualizar_laberinto(prob, res, titulo=args.algoritmo,
                                 ruta_salida=os.path.join(FIG, "salida_laberinto.png"))


if __name__ == "__main__":
    main()
