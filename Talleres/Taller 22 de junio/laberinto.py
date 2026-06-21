"""
laberinto.py
============
Escenario 2: busqueda en laberintos representados por una matriz.

  0 = celda libre (transitable)
  1 = barrera (no transitable)

El estado es una tupla (fila, columna). Por defecto el movimiento es en 4
direcciones (arriba, abajo, izquierda, derecha) con costo 1 por paso. Se puede
activar movimiento en 8 direcciones (diagonales con costo sqrt(2)).

La heuristica recomendada para A* es la distancia Manhattan al objetivo, que es
admisible para movimiento en 4 direcciones con costo unitario.
"""

import csv
import math
from algoritmos import Problema


class ProblemaLaberinto(Problema):
    def __init__(self, matriz, inicio, objetivo, diagonales=False):
        """
        matriz   : lista de listas con 0 (libre) y 1 (barrera)
        inicio   : (fila, columna) de partida
        objetivo : (fila, columna) meta
        diagonales : permite 8 movimientos si es True
        """
        self.matriz = matriz
        self.filas = len(matriz)
        self.cols = len(matriz[0]) if matriz else 0
        self.inicio = tuple(inicio)
        self.objetivo = tuple(objetivo)
        self.diagonales = diagonales
        self._validar()

        if diagonales:
            self.movimientos = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1),
                                (-1, -1, math.sqrt(2)), (-1, 1, math.sqrt(2)),
                                (1, -1, math.sqrt(2)), (1, 1, math.sqrt(2))]
        else:
            self.movimientos = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1)]

    def _validar(self):
        for p in (self.inicio, self.objetivo):
            f, c = p
            if not (0 <= f < self.filas and 0 <= c < self.cols):
                raise ValueError(f"La posicion {p} esta fuera del laberinto.")
            if self.matriz[f][c] == 1:
                raise ValueError(f"La posicion {p} cae sobre una barrera.")

    def libre(self, f, c):
        return 0 <= f < self.filas and 0 <= c < self.cols and self.matriz[f][c] == 0

    # ---- interfaz Problema ----
    def estado_inicial(self):
        return self.inicio

    def es_objetivo(self, estado):
        return estado == self.objetivo

    def vecinos(self, estado):
        f, c = estado
        salida = []
        for df, dc, costo in self.movimientos:
            nf, nc = f + df, c + dc
            if self.libre(nf, nc):
                salida.append(((nf, nc), costo))
        return salida

    def heuristica(self, estado):
        """Distancia Manhattan al objetivo (admisible en movimiento de 4 dir.)."""
        f, c = estado
        of, oc = self.objetivo
        return abs(f - of) + abs(c - oc)


def desde_csv(ruta):
    """Lee un laberinto desde un CSV de 0 y 1 (sin cabecera)."""
    matriz = []
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.reader(f):
            if fila and any(c.strip() != "" for c in fila):
                matriz.append([int(float(c)) for c in fila if c.strip() != ""])
    return matriz


def ascii_laberinto(prob, resultado=None):
    """Representacion textual del laberinto y, si se pasa, del recorrido.
       # barrera   . libre   S inicio   G objetivo   * camino   o visitado"""
    visitados = set(resultado.visitados) if resultado else set()
    camino = set(resultado.camino) if (resultado and resultado.camino) else set()
    lineas = []
    for f in range(prob.filas):
        fila = []
        for c in range(prob.cols):
            p = (f, c)
            if prob.matriz[f][c] == 1:
                fila.append("#")
            elif p == prob.inicio:
                fila.append("S")
            elif p == prob.objetivo:
                fila.append("G")
            elif p in camino:
                fila.append("*")
            elif p in visitados:
                fila.append("o")
            else:
                fila.append(".")
        lineas.append(" ".join(fila))
    return "\n".join(lineas)
