import heapq
import time

def mezclar_k_listas(listas):

    inicio = time.perf_counter()

    min_heap = []
    resultado = []

    # Insertamos el primer elemento de cada lista en el heap
    # Guardamos una tupla: (valor, índice_de_la_lista, índice_del_elemento)
    for i in range(len(listas)):
        if listas[i]: # Verificamos que la lista no esté vacía
            heapq.heappush(min_heap, (listas[i][0], i, 0))


    while min_heap:
        valor, lista_idx, elemento_idx = heapq.heappop(min_heap)
        resultado.append(valor)

        # Si la lista de la que salió el elemento tiene más números,
        # insertamos el siguiente en el heap
        if elemento_idx + 1 < len(listas[lista_idx]):
            siguiente_valor = listas[lista_idx][elemento_idx + 1]
            heapq.heappush(min_heap, (siguiente_valor, lista_idx, elemento_idx + 1))


    fin = time.perf_counter()

    return resultado, fin - inicio


listas_entrada = [[1, 4, 5], [1, 3, 4], [2, 6]]

res, duracion = mezclar_k_listas(listas_entrada)

print(f"Entrada: {listas_entrada}")
print(f"Salida mezclada: {res}")
print(f"Tiempo de ejecución: {duracion:.8f} segundos")