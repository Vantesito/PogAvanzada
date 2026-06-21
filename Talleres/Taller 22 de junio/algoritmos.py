"""
algoritmos.py
=============
Implementacion de los cuatro algoritmos de busqueda (BFS, DFS, UCS y A*)
sobre una interfaz de problema unificada. Esto permite reutilizar exactamente
el mismo codigo de busqueda tanto para grafos/arboles como para laberintos:
basta con que cada escenario provea el metodo `vecinos`, la prueba de objetivo
y (para A*) una heuristica.

Cada algoritmo devuelve un objeto Resultado con:
  - camino        : lista de estados desde inicio hasta objetivo (o None)
  - costo         : costo acumulado del camino (suma de costos de arista)
  - visitados     : lista de estados en el ORDEN en que fueron expandidos
  - frontera_max  : tamano maximo que alcanzo la frontera (uso de memoria)
"""

from collections import deque
import heapq
import itertools


class Problema:
    """Interfaz que deben implementar grafos y laberintos.

    Metodos esperados:
      estado_inicial            -> estado de partida
      es_objetivo(estado)       -> bool
      vecinos(estado)           -> lista de tuplas (estado_vecino, costo_arista)
      heuristica(estado)        -> estimacion (>=0) del costo restante al objetivo
    """

    def estado_inicial(self):
        raise NotImplementedError

    def es_objetivo(self, estado):
        raise NotImplementedError

    def vecinos(self, estado):
        raise NotImplementedError

    def heuristica(self, estado):
        return 0  # por defecto (admisible): convierte A* en UCS


class Resultado:
    def __init__(self, camino, costo, visitados, frontera_max):
        self.camino = camino
        self.costo = costo
        self.visitados = visitados
        self.frontera_max = frontera_max

    @property
    def exito(self):
        return self.camino is not None

    @property
    def longitud_camino(self):
        return len(self.camino) if self.camino else 0

    def __repr__(self):
        if not self.exito:
            return f"<Resultado SIN SOLUCION  visitados={len(self.visitados)}>"
        return (f"<Resultado exito  pasos={self.longitud_camino - 1}  "
                f"costo={self.costo}  visitados={len(self.visitados)}  "
                f"frontera_max={self.frontera_max}>")


def _reconstruir(padres, objetivo):
    """Reconstruye el camino siguiendo el diccionario de padres hacia atras."""
    camino = [objetivo]
    while padres[objetivo] is not None:
        objetivo = padres[objetivo]
        camino.append(objetivo)
    camino.reverse()
    return camino


def _costo_camino(problema, camino):
    """Suma los costos de arista a lo largo del camino encontrado."""
    total = 0
    for a, b in zip(camino, camino[1:]):
        for vecino, costo in problema.vecinos(a):
            if vecino == b:
                total += costo
                break
    return total


# --------------------------------------------------------------------------- #
#  BFS - Breadth First Search (busqueda en anchura, por niveles)              #
# --------------------------------------------------------------------------- #
def bfs(problema):
    """Explora por niveles usando una cola FIFO. Garantiza el camino con
    MENOR NUMERO DE PASOS (optimo solo si todas las aristas cuestan lo mismo)."""
    inicio = problema.estado_inicial()
    if problema.es_objetivo(inicio):
        return Resultado([inicio], 0, [inicio], 1)

    frontera = deque([inicio])
    padres = {inicio: None}
    visitados = []
    frontera_max = 1

    while frontera:
        frontera_max = max(frontera_max, len(frontera))
        estado = frontera.popleft()
        visitados.append(estado)

        if problema.es_objetivo(estado):
            camino = _reconstruir(padres, estado)
            return Resultado(camino, _costo_camino(problema, camino),
                             visitados, frontera_max)

        for vecino, _ in problema.vecinos(estado):
            if vecino not in padres:
                padres[vecino] = estado
                frontera.append(vecino)

    return Resultado(None, None, visitados, frontera_max)


# --------------------------------------------------------------------------- #
#  DFS - Depth First Search (busqueda en profundidad)                         #
# --------------------------------------------------------------------------- #
def dfs(problema):
    """Explora en profundidad usando una pila LIFO. NO garantiza el camino
    mas corto ni el de menor costo; sirve para ver el contraste de recorrido."""
    inicio = problema.estado_inicial()
    frontera = [inicio]          # pila
    padres = {inicio: None}
    visitados = []
    expandidos = set()
    frontera_max = 1

    while frontera:
        frontera_max = max(frontera_max, len(frontera))
        estado = frontera.pop()
        if estado in expandidos:
            continue
        expandidos.add(estado)
        visitados.append(estado)

        if problema.es_objetivo(estado):
            camino = _reconstruir(padres, estado)
            return Resultado(camino, _costo_camino(problema, camino),
                             visitados, frontera_max)

        # Se invierten los vecinos para que el primero listado se expanda antes.
        for vecino, _ in reversed(problema.vecinos(estado)):
            if vecino not in expandidos:
                padres.setdefault(vecino, estado)
                frontera.append(vecino)

    return Resultado(None, None, visitados, frontera_max)


# --------------------------------------------------------------------------- #
#  UCS - Uniform Cost Search (Dijkstra con objetivo)                          #
# --------------------------------------------------------------------------- #
def ucs(problema):
    """Cola de prioridad ordenada por el costo acumulado g(n). Encuentra el
    camino de MENOR COSTO total cuando los costos son no negativos."""
    inicio = problema.estado_inicial()
    contador = itertools.count()          # desempata para evitar comparar estados
    frontera = [(0, next(contador), inicio)]
    g = {inicio: 0}
    padres = {inicio: None}
    visitados = []
    expandidos = set()
    frontera_max = 1

    while frontera:
        frontera_max = max(frontera_max, len(frontera))
        costo, _, estado = heapq.heappop(frontera)
        if estado in expandidos:
            continue
        expandidos.add(estado)
        visitados.append(estado)

        if problema.es_objetivo(estado):
            camino = _reconstruir(padres, estado)
            return Resultado(camino, costo, visitados, frontera_max)

        for vecino, paso in problema.vecinos(estado):
            nuevo = costo + paso
            if vecino not in g or nuevo < g[vecino]:
                g[vecino] = nuevo
                padres[vecino] = estado
                heapq.heappush(frontera, (nuevo, next(contador), vecino))

    return Resultado(None, None, visitados, frontera_max)


# --------------------------------------------------------------------------- #
#  A* - A estrella : f(n) = g(n) + h(n)                                        #
# --------------------------------------------------------------------------- #
def a_estrella(problema):
    """Cola de prioridad ordenada por f(n) = g(n) + h(n). Con una heuristica
    admisible (p.ej. distancia Manhattan en laberintos) encuentra el camino
    OPTIMO expandiendo menos nodos que UCS."""
    inicio = problema.estado_inicial()
    contador = itertools.count()
    g = {inicio: 0}
    f0 = problema.heuristica(inicio)
    frontera = [(f0, next(contador), inicio)]
    padres = {inicio: None}
    visitados = []
    expandidos = set()
    frontera_max = 1

    while frontera:
        frontera_max = max(frontera_max, len(frontera))
        _, _, estado = heapq.heappop(frontera)
        if estado in expandidos:
            continue
        expandidos.add(estado)
        visitados.append(estado)

        if problema.es_objetivo(estado):
            camino = _reconstruir(padres, estado)
            return Resultado(camino, g[estado], visitados, frontera_max)

        for vecino, paso in problema.vecinos(estado):
            nuevo = g[estado] + paso
            if vecino not in g or nuevo < g[vecino]:
                g[vecino] = nuevo
                padres[vecino] = estado
                f = nuevo + problema.heuristica(vecino)
                heapq.heappush(frontera, (f, next(contador), vecino))

    return Resultado(None, None, visitados, frontera_max)


# Tabla de acceso por nombre, util para la interfaz de seleccion.
ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "A*": a_estrella,
}
