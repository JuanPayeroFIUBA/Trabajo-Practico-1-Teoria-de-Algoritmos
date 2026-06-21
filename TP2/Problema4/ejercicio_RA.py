import os
import random
from grafo import Grafo
import sets_datos as datos


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")


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
    dataset_path = os.path.join(DATASETS_DIR, "dataset4.txt")
    if not os.path.exists(dataset_path):
        print(f"Error: no se encontró el dataset en {dataset_path}")
        return

    grafo = datos.cargar_grafo_desde_archivo(dataset_path)
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


if __name__ == "__main__":
    main()
