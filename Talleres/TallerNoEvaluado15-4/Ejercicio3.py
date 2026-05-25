import heapq
import time

def obtener_top_k_productos(productos, k):
    inicio = time.perf_counter()
    min_heap = []
    for nombre, puntaje in productos:

        if len(min_heap) < k:
            heapq.heappush(min_heap, (puntaje, nombre))
        else:

            if puntaje > min_heap[0][0]:
                heapq.heapreplace(min_heap, (puntaje, nombre))

    resultado = [nombre for puntaje, nombre in sorted(min_heap, reverse=True)]

    fin = time.perf_counter()

    return resultado, fin - inicio

# Datos de prueba
productos = [("Laptop", 95), ("Mouse", 80), ("Teclado", 85)]
k = 2

res, duracion = obtener_top_k_productos(productos, k)

print(f"Productos evaluados: {productos}")
print(f"Top-{k} productos: {res}")
print(f"Tiempo de ejecución: {duracion:.8f} segundos")