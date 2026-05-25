import heapq
import time

def k_esimo_mas_grande(nums, k):
    inicio = time.perf_counter()
    min_heap = nums[:k]
    heapq.heapify(min_heap)

    for i in range(k, len(nums)):
        if nums[i] > min_heap[0]:
            heapq.heapreplace(min_heap, nums[i])

    resultado = min_heap[0]

    fin = time.perf_counter()

    return resultado, fin - inicio

# Datos de prueba
nums = [3, 2, 1, 5, 6, 4]
k = 2

res, duracion = k_esimo_mas_grande(nums, k)

print(f"Arreglo: {nums}")
print(f"El {k}-ésimo número más grande es: {res}")
print(f"Tiempo de ejecución: {duracion:.8f} segundos")