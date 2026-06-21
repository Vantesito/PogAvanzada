"""
grafo.py
========
Escenario 1: busqueda en grafos / arboles.

El grafo se puede definir de tres formas:
  1. En el codigo, pasando un diccionario de adyacencia.
  2. Desde un CSV como LISTA de aristas:  origen,destino,costo
  3. Desde un CSV como MATRIZ de adyacencia (0 = sin arista, >0 = costo).

Opcionalmente se cargan coordenadas (x,y) de cada nodo para que A* use una
heuristica de distancia euclidiana; si no hay coordenadas, h(n)=0 y A* se
comporta como UCS.
"""

import csv
import math
from algoritmos import Problema


class ProblemaGrafo(Problema):
    def __init__(self, adyacencia, inicio, objetivo,
                 coordenadas=None, dirigido=False):
        """
        adyacencia : dict  nodo -> lista de (vecino, costo)
        inicio, objetivo : nombres de nodo
        coordenadas: dict  nodo -> (x, y)  (opcional, para heuristica de A*)
        dirigido   : si False, cada arista se anade en ambos sentidos
        """
        self.ady = {n: list(v) for n, v in adyacencia.items()}
        if not dirigido:
            for n, vecinos in adyacencia.items():
                for vecino, costo in vecinos:
                    self.ady.setdefault(vecino, [])
                    if not any(x == n for x, _ in self.ady[vecino]):
                        self.ady[vecino].append((n, costo))
        for n in list(self.ady):
            self.ady[n].sort()
        self.inicio = inicio
        self.objetivo = objetivo
        self.coordenadas = coordenadas or {}

    # ---- interfaz Problema ----
    def estado_inicial(self):
        return self.inicio

    def es_objetivo(self, estado):
        return estado == self.objetivo

    def vecinos(self, estado):
        return self.ady.get(estado, [])

    def heuristica(self, estado):
        if estado in self.coordenadas and self.objetivo in self.coordenadas:
            x1, y1 = self.coordenadas[estado]
            x2, y2 = self.coordenadas[self.objetivo]
            return math.hypot(x1 - x2, y1 - y2)
        return 0


# --------------------------------------------------------------------------- #
#  Lectores de CSV                                                            #
# --------------------------------------------------------------------------- #
def desde_csv_lista(ruta):
    """Lee un CSV de aristas con cabecera: origen,destino,costo
    Devuelve un diccionario de adyacencia."""
    ady = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        cabecera = next(lector)
        for fila in lector:
            if not fila or all(c.strip() == "" for c in fila):
                continue
            origen, destino = fila[0].strip(), fila[1].strip()
            costo = float(fila[2]) if len(fila) > 2 and fila[2].strip() else 1.0
            costo = int(costo) if costo == int(costo) else costo
            ady.setdefault(origen, []).append((destino, costo))
            ady.setdefault(destino, [])
    return ady


def desde_csv_matriz(ruta):
    """Lee un CSV de matriz de adyacencia. La primera fila y la primera
    columna son las etiquetas de los nodos. Un valor 0 significa 'sin arista'."""
    with open(ruta, newline="", encoding="utf-8") as f:
        filas = [fila for fila in csv.reader(f) if fila]
    etiquetas = [c.strip() for c in filas[0][1:]]
    ady = {e: [] for e in etiquetas}
    for fila in filas[1:]:
        origen = fila[0].strip()
        for j, valor in enumerate(fila[1:]):
            valor = valor.strip()
            if valor and float(valor) != 0:
                costo = float(valor)
                costo = int(costo) if costo == int(costo) else costo
                ady[origen].append((etiquetas[j], costo))
    return ady


def coordenadas_desde_csv(ruta):
    """Lee un CSV de coordenadas con cabecera: nodo,x,y"""
    coords = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)
        for fila in lector:
            if fila:
                coords[fila[0].strip()] = (float(fila[1]), float(fila[2]))
    return coords
