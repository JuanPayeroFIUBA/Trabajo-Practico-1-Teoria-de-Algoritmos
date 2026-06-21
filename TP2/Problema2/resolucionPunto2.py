import glob
import os
import time
from matplotlib import pyplot as plt
import clasesFlujo as aux
import generadorDeDatasets as gen


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
RESULTADOS_DIR = os.path.join(BASE_DIR, "resultados")


def medir_tiempos():
    files = sorted(glob.glob(os.path.join(DATASETS_DIR, "*.txt")))
    if not files:
        print("No se encontraron datasets en:", DATASETS_DIR)
        return [], []

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
    if not n_values:
        print("No hay datos para graficar.")
        return

    teorica = curva_teorica(n_values)
    escala = max(tiempos) / max(teorica)
    teorica = [t * escala for t in teorica]

    plt.plot(n_values, tiempos, marker="o", label="Tiempo real")
    plt.plot(n_values, teorica, linestyle="--", label="O(n^5) teórico")
    plt.xlabel("Tamaño del problema (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación tiempo real vs complejidad teórica")
    plt.legend()

    os.makedirs(RESULTADOS_DIR, exist_ok=True)
    grafico_path = os.path.join(RESULTADOS_DIR, "tiempos_problema2.png")
    plt.savefig(grafico_path)
    print(f"Gráfico guardado en: {grafico_path}")
    plt.close()


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
    archivos = sorted(glob.glob(os.path.join(DATASETS_DIR, "*.txt")))
    if not archivos:
        print("No se encontraron datasets en:", DATASETS_DIR)
        return

    os.makedirs(RESULTADOS_DIR, exist_ok=True)

    for archivo in archivos:
        nombre = os.path.splitext(os.path.basename(archivo))[0]
        n, D, k, b, d = gen.leer_dataset(archivo)
        solucion = backups_por_flujo(d, D, b, k)

        resultado_path = os.path.join(RESULTADOS_DIR, f"resultado_{nombre}.txt")
        with open(resultado_path, "w") as f:
            if solucion is None:
                mensaje = f"Dataset: {nombre}\nNo existe solución\n"
                print(mensaje)
                f.write(mensaje)
                continue

            f.write(f"Dataset: {nombre}\n")
            f.write(f"Parametros: n={n}, D={D}, k={k}, b={b}\n\n")
            f.write("Backups encontrados:\n")
            for i, backups in enumerate(solucion):
                f.write(f"Antena {i}: {backups}\n")

            f.write("\nCantidad de veces que cada antena aparece como backup:\n")
            usos = [0] * n
            for backups in solucion:
                for a in backups:
                    usos[a] += 1

            for i, c in enumerate(usos):
                f.write(f"Antena {i}: {c} veces\n")

        print(f"Resultado guardado en: {resultado_path}")

    graficar()


if __name__ == "__main__":
    main()
