from grafo import Grafo


def cargar_grafo_desde_archivo(ruta_archivo) -> Grafo:

    grafo = Grafo(dirigido=False)

    with open(ruta_archivo, "r") as f:
        lineas = f.read().splitlines()

    num_vertices = int(lineas[0].strip())
    for v in range(num_vertices):
        grafo.agregar_vertice(v)

    for linea in lineas[1:]:
        if linea.strip():
            u, v = map(int, linea.strip().split(","))
            grafo.agregar_arista(u, v)

    return grafo
