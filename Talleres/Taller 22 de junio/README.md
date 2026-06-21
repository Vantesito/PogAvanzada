# Algoritmos de Búsqueda: BFS, DFS, UCS y A\*

Implementación y visualización de cuatro algoritmos de búsqueda sobre dos
escenarios: **grafos/árboles** y **laberintos** (matrices). Un mismo código de
búsqueda se reutiliza para ambos escenarios gracias a una interfaz de problema común.

## Estructura

| Archivo | Contenido |
|---|---|
| `algoritmos.py` | BFS, DFS, UCS y A\* sobre la interfaz `Problema` |
| `grafo.py` | Escenario grafo + lectura de CSV (lista y matriz de adyacencia) |
| `laberinto.py` | Escenario laberinto (matriz 0/1) + heurística Manhattan |
| `visualizacion.py` | Gráficos con matplotlib / networkx |
| `main.py` | Interfaz de selección (menú interactivo y línea de comandos) |
| `pruebas.py` | Pruebas automáticas que verifican la corrección |
| `informe.docx` | Informe con decisiones de diseño y comparación |
| `grafo_lista.csv`, `grafo_matriz.csv`, `grafo_coords.csv` | Grafo de prueba |
| `laberinto.csv` | Laberinto 10x10 de prueba |
| `figuras/` | Capturas de ejecución (comparativas e individuales) |

## Requisitos

```bash
pip install matplotlib networkx
```

## Uso

```bash
# Comparar los 4 algoritmos y generar la figura comparativa
python main.py --comparar laberinto
python main.py --comparar grafo

# Ejecutar un algoritmo concreto
python main.py --escenario laberinto --algoritmo "A*" --inicio 0,0 --objetivo 9,9
python main.py --escenario grafo --algoritmo UCS --inicio A --objetivo G

# Menú interactivo
python main.py

# Pruebas automáticas
python pruebas.py
```

## Convenciones del laberinto

`0` = celda libre, `1` = barrera. Posición = `(fila, columna)`. Movimiento en
4 direcciones con costo 1 (opción de 8 direcciones con diagonales de costo √2).

## Formatos de CSV del grafo

- **Lista de aristas:** cabecera `origen,destino,costo` y una fila por arista.
- **Matriz de adyacencia:** primera fila y columna con etiquetas; `0` = sin arista.
- **Coordenadas (opcional):** `nodo,x,y`, usadas por A\* para la heurística euclidiana.

## Resumen de resultados

**Laberinto 10x10** (todos hallan costo 18): A\* visita 33 nodos frente a 43 de
BFS/UCS gracias a la heurística Manhattan.

**Grafo ponderado** (A→G): BFS/DFS hallan `A-C-E-G` (costo 9, 3 saltos) pero no
es el más barato; UCS/A\* hallan `A-B-C-D-E-G` (costo 7). A\* expande un nodo menos.
