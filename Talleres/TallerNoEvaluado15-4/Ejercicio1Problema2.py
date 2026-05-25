import heapq
import time
from collections import Counter


data_original = [3, 100, 20, 2, 80, 1, 30, 20, 1, 3, 200, 3] * 1000

data_heap2 = list(data_original)
heapq.heapify(data_heap2)
conteos = Counter(data_heap2)

inicio_p2_heap = time.perf_counter()
repetidos = {num: veces for num, veces in conteos.items() if veces > 1}
ordenados_p2_heap = []
while data_heap2:
    ordenados_p2_heap.append(heapq.heappop(data_heap2))
fin_p2_heap = time.perf_counter()


data_lin = list(data_original)
inicio_p2_lin = time.perf_counter()
# Encontrar repetidos de forma lineal
conteos_lin = Counter(data_lin)
repetidos_lin = {num: veces for num, veces in conteos_lin.items() if veces > 1}
# Ordenar
ordenados_p2_lin = sorted(data_lin)
fin_p2_lin = time.perf_counter()

print(f"\n--- RESULTADOS PROBLEMA 2 ---")
print(f"lista convertida en heap: {data_original}")
print(f"lista convertida en heap (sorted metod): {data_lin}")
print(f"repetidos y frecuencia {repetidos}")
print(f"repetidos y frecuencia (sort) {repetidos}")
print(f"Tiempo Heap:   {fin_p2_heap - inicio_p2_heap:.8f} seg")
print(f"Tiempo Sort ed:  {fin_p2_lin - inicio_p2_lin:.8f} seg")