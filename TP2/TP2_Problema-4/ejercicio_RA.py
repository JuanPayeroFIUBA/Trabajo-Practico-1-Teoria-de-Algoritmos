import random
from grafo import Grafo
import sets_datos as datos


def tres_coloreo_randomizado(grafo: Grafo):
    colores = {}
    aristas_satisfechas = 0
    for v in grafo.obtener_vertices():
        colores[v] = random.randint(1, 3)

    for u, v in grafo.obtener_aristas():
        if colores[u] != colores[v]:
            aristas_satisfechas += 1

    return colores, aristas_satisfechas


def main():
    grafo = datos.cargar_grafo_desde_archivo("datasets/dataset4.txt")
    total = 0
    iteraciones = 10000

    _, satisfechas = tres_coloreo_randomizado(grafo)
    print("Satisfaccion observada en una ejecucion", satisfechas)

    for _ in range(iteraciones):

        _, satisfechas = tres_coloreo_randomizado(grafo)

        total += satisfechas

    promedio = total / iteraciones

    print("Promedio observado en", iteraciones, "iteraciones:", promedio)
    print("Esperado teórico:", (2 / 3) * len(grafo.obtener_aristas()))


main()
