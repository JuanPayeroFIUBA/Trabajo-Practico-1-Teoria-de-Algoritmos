import random
import time
import math
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# ─────────────────────────────────────────────────────────────
# Algoritmos
# ─────────────────────────────────────────────────────────────

def greedy_original(A, B):
    S, T = [], 0
    for a in A:
        if T + a <= B:
            S.append(a)
            T += a
    return S, T


def greedy_aprox(A, B):
    A_ord = sorted(A, reverse=True)
    S, T = [], 0
    for a in A_ord:
        if T + a <= B:
            S.append(a)
            T += a
    return S, T


def optimo_dp(A, B):
    dp = [False] * (B + 1)
    dp[0] = True
    for a in A:
        if a <= B:
            for v in range(B, a - 1, -1):
                if dp[v - a]:
                    dp[v] = True
    for v in range(B, -1, -1):
        if dp[v]:
            return v
    return 0


# ─────────────────────────────────────────────────────────────
# Datasets
# ─────────────────────────────────────────────────────────────

def generar_dataset(n, B, seed=None):
    if seed is not None:
        random.seed(seed)
    return [random.randint(1, B) for _ in range(n)]


def guardar_dataset(path, A, B, suma_aprox=None):
    with open(path, 'w') as f:
        f.write(f"B={B}\n")
        f.write("A=" + ",".join(map(str, A)) + "\n")
        if suma_aprox is not None:
            f.write(f"suma_aprox={suma_aprox}\n")


def cargar_dataset(path):
    A, B = [], None
    with open(path) as f:
        for line in f:
            k, v = line.strip().split("=", 1)
            if k == "B":
                B = int(v)
            elif k == "A":
                A = list(map(int, v.split(",")))
    return A, B


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    os.makedirs("datasets", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # Seguimiento con datasets reducidos
    TRACE_SETS = [
        ([9, 3, 5], 13),
        ([1, 10], 10),
        ([7, 5, 4, 3], 10),
        ([6, 5, 5, 4], 11),
    ]
    print(f"{'A':<25} {'B':>5}  {'greedy_orig':>12}  {'greedy_aprox':>13}  {'OPT':>6}  {'ratio':>7}")
    print("-" * 72)
    for A_t, B_t in TRACE_SETS:
        _, t_orig = greedy_original(A_t, B_t)
        _, t_ap = greedy_aprox(A_t, B_t)
        opt = optimo_dp(A_t, B_t)
        print(f"{str(A_t):<25} {B_t:>5}  {t_orig:>12}  {t_ap:>13}  {opt:>6}  {t_ap/opt:.3f}")
    print()

    # Experimentos de tiempo
    TAMANIOS = [100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    B_exp = 10_000
    TIEMPOS_PATH = "results/tiempos.csv"

    # Si ya existe el archivo de tiempos, lo carga en lugar de re-medir
    if os.path.exists(TIEMPOS_PATH):
        tiempos = []
        with open(TIEMPOS_PATH) as f:
            next(f)  # encabezado
            for line in f:
                tiempos.append(float(line.split(",")[1]))
        print("(Tiempos cargados desde archivo. Usar --remedir para recalcular.)")
    else:
        tiempos = []
        print(f"{'n':>8}  {'tiempo (s)':>12}  {'suma_aprox':>12}  {'OPT':>8}  {'ratio':>7}  {'garantia':>9}")
        print("-" * 68)

        with open(TIEMPOS_PATH, 'w') as f:
            f.write("n,tiempo,suma_aprox\n")
            for n in TAMANIOS:
                A = generar_dataset(n, B_exp, seed=2024 + n)
                path = f"datasets/dataset_n{n}.txt"

                inicio = time.perf_counter()
                _, T_a = greedy_aprox(A, B_exp)
                t = time.perf_counter() - inicio
                tiempos.append(t)

                guardar_dataset(path, A, B_exp, suma_aprox=T_a)
                f.write(f"{n},{t},{T_a}\n")

                if n <= 2000:
                    opt = optimo_dp(A, B_exp)
                    ratio = T_a / opt if opt > 0 else 1.0
                    cumple = "si" if T_a >= opt / 2 else "NO"
                    print(f"{n:>8}  {t:>12.6f}  {T_a:>12}  {opt:>8}  {ratio:>7.4f}  {cumple:>9}")
                else:
                    print(f"{n:>8}  {t:>12.6f}  {T_a:>12}  {'---':>8}  {'---':>7}  {'---':>9}")

    # Gráficos
    nlogn = [n * math.log(n) for n in TAMANIOS]
    escala = tiempos[-1] / nlogn[-1]
    teorico = [escala * v for v in nlogn]
    norm = [t / (n * math.log(n)) for t, n in zip(tiempos, TAMANIOS)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(TAMANIOS, tiempos, 'bo-', label='Tiempo medido', markersize=5)
    axes[0].plot(TAMANIOS, teorico, 'r--', label='O(n log n) teórico')
    axes[0].set_xlabel('n (tamaño de A)')
    axes[0].set_ylabel('Tiempo (s)')
    axes[0].set_title('Tiempo de ejecución')
    axes[0].legend()
    axes[0].grid(True, alpha=0.4)

    axes[1].plot(TAMANIOS, norm, 'go-', markersize=5)
    axes[1].axhline(y=sum(norm) / len(norm), color='r', linestyle='--',
                    label='Constante promedio')
    axes[1].set_xlabel('n')
    axes[1].set_ylabel('t / (n·log n)')
    axes[1].set_title('Tiempo normalizado')
    axes[1].legend()
    axes[1].grid(True, alpha=0.4)

    plt.suptitle('Problema 3 — Greedy Ordenado Descendente', fontsize=13)
    plt.tight_layout()
    plt.savefig('results/tiempos_problema3.png', dpi=150)
    print(f"\nGráfico guardado en results/tiempos_problema3.png")


if __name__ == "__main__":
    main()
