import random
import string
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


# Algoritmo propuesto de PD
def min_palindromos(cadena):
    n = len(cadena)
    if n == 0:
        return 0

    esPal = [[False] * n for _ in range(n)]
    C = [0] * n

    for i in range(n):
        esPal[i][i] = True

    for L in range(2, n + 1):
        for j in range(n - L + 1):
            i = j + L - 1
            if L == 2:
                esPal[j][i] = cadena[j] == cadena[i]
            else:
                esPal[j][i] = cadena[j] == cadena[i] and esPal[j + 1][i - 1]

    for i in range(n):
        if esPal[0][i]:
            C[i] = 1
        else:
            C[i] = n + 1
            for j in range(i + 1):
                if esPal[j][i]:
                    if C[j - 1] + 1 < C[i]:
                        C[i] = C[j - 1] + 1
    return C[-1]


# Generacion de datos de prueba y grafico
random.seed(42)


def generar_datos(longitud):
    return "".join(random.choices(string.ascii_uppercase, k=longitud))


tamanio_cadena = [
    10,
    50,
    100,
    250,
    500,
    750,
    1000,
    1300,
    1600,
    2000,
    2500,
    3000,
    3600,
    4200,
    4800,
    5500,
]
tiempos_medidos = []

print("RESULTADOs")
for n in tamanio_cadena:
    data = generar_datos(n)

    inicio = time.perf_counter()
    resultado = min_palindromos(data)
    fin = time.perf_counter()

    tiempo_transcurrido = fin - inicio
    tiempos_medidos.append(tiempo_transcurrido)

    print(
        f"N: {n:4d} | Tamaño del palíndromo mas largo: {resultado:4d}  | Tiempo: {tiempo_transcurrido:.6f} segundos"
    )


def curva_teorica(x, a, b, c):
    return a * x**2 + b * x + c


x_data = np.array(tamanio_cadena)
y_data = np.array(tiempos_medidos)

popt, _ = curve_fit(curva_teorica, x_data, y_data)

x_fit = np.linspace(min(tamanio_cadena), max(tamanio_cadena), 100)
y_fit = curva_teorica(x_fit, *popt)

plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, "bo-", label="Tiempos medidos (Empírico)")

plt.plot(x_fit, y_fit, "r--", label="Ajuste Teórico O(n²)")

plt.title("Análisis de Complejidad")
plt.xlabel("Longitud de la cadena (n)")
plt.ylabel("Tiempo de ejecución (segundos)")
plt.legend()
plt.grid(True)
plt.show()
