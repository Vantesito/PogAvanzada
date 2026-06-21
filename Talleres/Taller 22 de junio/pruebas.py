"""
pruebas.py
==========
Pruebas automaticas que verifican propiedades clave de cada algoritmo.
Ejecutar con:  python pruebas.py
"""

from algoritmos import bfs, dfs, ucs, a_estrella
from grafo import ProblemaGrafo, desde_csv_lista, desde_csv_matriz, coordenadas_desde_csv
from laberinto import ProblemaLaberinto, desde_csv
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ok = 0
fallos = 0


def verificar(cond, descripcion):
    global ok, fallos
    if cond:
        ok += 1
        print(f"  [OK]   {descripcion}")
    else:
        fallos += 1
        print(f"  [FALLO]{descripcion}")


print("== Grafo (lista de adyacencia) ==")
ady = desde_csv_lista(os.path.join(AQUI, "grafo_lista.csv"))
coords = coordenadas_desde_csv(os.path.join(AQUI, "grafo_coords.csv"))
g = ProblemaGrafo(ady, "A", "G", coordenadas=coords)

r_bfs, r_dfs, r_ucs, r_astar = bfs(g), dfs(g), ucs(g), a_estrella(g)
verificar(r_bfs.exito and r_bfs.camino[0] == "A" and r_bfs.camino[-1] == "G",
          "BFS llega de A a G")
verificar(r_ucs.costo == 7, f"UCS encuentra el costo minimo (=7, obtuvo {r_ucs.costo})")
verificar(r_astar.costo == 7, f"A* encuentra el costo minimo (=7, obtuvo {r_astar.costo})")
verificar(r_astar.costo == r_ucs.costo, "A* y UCS coinciden en costo optimo")
verificar(len(r_astar.visitados) <= len(r_ucs.visitados),
          "A* no expande mas nodos que UCS")
verificar((r_bfs.longitud_camino - 1) <= (r_ucs.longitud_camino - 1),
          "BFS usa el menor numero de pasos")

print("\n== Grafo (matriz de adyacencia) ==")
ady_m = desde_csv_matriz(os.path.join(AQUI, "grafo_matriz.csv"))
g2 = ProblemaGrafo(ady_m, "A", "G")
r2 = ucs(g2)
verificar(r2.exito and r2.camino[-1] == "G", "UCS sobre matriz llega a G")

print("\n== Laberinto ==")
matriz = desde_csv(os.path.join(AQUI, "laberinto.csv"))
lab = ProblemaLaberinto(matriz, (0, 0), (9, 9))
b, d, u, a = bfs(lab), dfs(lab), ucs(lab), a_estrella(lab)
verificar(b.exito, "BFS encuentra salida del laberinto")
verificar(b.costo == u.costo == a.costo,
          f"BFS=UCS=A* mismo costo optimo ({b.costo},{u.costo},{a.costo})")
verificar(len(a.visitados) <= len(u.visitados),
          f"A* expande <= que UCS ({len(a.visitados)} vs {len(u.visitados)})")
verificar(a.camino[0] == (0, 0) and a.camino[-1] == (9, 9),
          "A* respeta inicio y objetivo")

print("\n== Caso sin solucion ==")
encerrado = [[0, 1, 0], [1, 1, 0], [0, 0, 0]]
lab2 = ProblemaLaberinto(encerrado, (0, 0), (0, 2))
verificar(not bfs(lab2).exito, "BFS reporta correctamente que no hay camino")

print(f"\nResumen: {ok} correctas, {fallos} fallidas")
