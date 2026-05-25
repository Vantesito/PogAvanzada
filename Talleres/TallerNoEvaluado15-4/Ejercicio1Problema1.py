import heapq
import time

data_original = [3, 100, 20, 2, 80, 1]

data_heap = list(data_original)
heapq.heapify(data_heap)

inicio_heap = time.perf_counter()
ordenados_heap = []
while data_heap:
    ordenados_heap.append(heapq.heappop(data_heap))
fin_heap = time.perf_counter()


data_sorted = list(data_original)
inicio_sort = time.perf_counter()
ordenados_sort = sorted(data_sorted)
fin_sort = time.perf_counter()

print(f"--- RESULTADOS PROBLEMA 1 ---")
print(f"lista convertida en heap: {data_heap}")
print(f"lista convertida en heap (sorted): {data_sorted}")
print(f"lista ordenada de menor a mayor: {ordenados_heap}")
print(f"lista ordenada de menor a mayor: {ordenados_sort}")
print(f"Tiempo Heap (pop manual): {fin_heap - inicio_heap:.8f} seg")
print(f"Tiempo sorted():          {fin_sort - inicio_sort:.8f} seg")