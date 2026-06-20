import glob
import time
from matplotlib import pyplot as plt
import clasesFlujo as aux
import generadorDeDatasets as gen


def medir_tiempos():
    files = sorted(glob.glob("datasets/*.txt"))
    tamanios = []
    tiempos = []
    for file in files:
        n, D, k, b, d = gen.leer_dataset(file)
        start = time.perf_counter()
        backups_por_flujo(d, D, b, k)
        end = time.perf_counter()
        tiempo = end - start
        print(f"{file} -> n={n}, tiempo={tiempo:.6f}s")
        tamanios.append(n)
        tiempos.append(tiempo)

    return tamanios, tiempos


def curva_teorica(n_values):
    return [n**5 for n in n_values]


def graficar():
    n_values, tiempos = medir_tiempos()
    teorica = curva_teorica(n_values)
    escala = max(tiempos) / max(teorica)
    teorica = [t * escala for t in teorica]

    plt.plot(n_values, tiempos, marker="o", label="Tiempo real")
    plt.plot(n_values, teorica, linestyle="--", label="O(n^5) teórico")
    plt.xlabel("Tamaño del problema (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación tiempo real vs complejidad teórica")
    plt.legend()
    plt.show()


def backups_por_flujo(d, D, b, k):
    n = len(d)
    S = 0
    IZQ = 1
    DER = IZQ + n
    T = DER + n
    mf = aux.MaxFlow(T + 1)

    for i in range(n):
        mf.add_vertice(S, IZQ + i, k)

    for i in range(n):
        for j in range(n):

            if i == j:
                continue

            if d[i][j] < D:
                mf.add_vertice(IZQ + i, DER + j, 1)

    for j in range(n):
        mf.add_vertice(DER + j, T, b)

    flujo = mf.edmonds_karp(S, T)

    if flujo != n * k:
        return None

    backups = [[] for _ in range(n)]

    for i in range(n):
        u = IZQ + i

        for e in mf.graph[u]:
            if DER <= e.hacia < DER + n and e.flujo == 1:
                backups[i].append(e.hacia - DER)

    return backups


def main():
    archivos = glob.glob("datasets/*.txt")
    for archivo in archivos:

        n, D, k, b, d = gen.leer_dataset(archivo)
        solucion = backups_por_flujo(d, D, b, k)
        if solucion is None:
            print("No existe solución")
            continue

        print("Backups encontrados:\n")
        for i, backups in enumerate(solucion):
            print(f"Antena {i}: {backups}")

        print("\nCantidad de veces que cada antena aparece como backup:")
        usos = [0] * n
        for backups in solucion:
            for a in backups:
                usos[a] += 1

        for i, c in enumerate(usos):
            print(f"Antena {i}: {c} veces")

    graficar()


main()
