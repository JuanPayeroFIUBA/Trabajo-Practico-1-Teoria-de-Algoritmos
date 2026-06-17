import random


def generar_dataset(n, D, k, b, seed=42, filename="dataset.txt"):

    random.seed(seed)

    d = []

    for i in range(n):
        fila = []
        for j in range(n):

            if i == j:
                fila.append(0)
            else:
                fila.append(random.randint(1, 10))

        d.append(fila)

    with open(filename, "w") as f:
        f.write(f"{n}\n")
        f.write(f"{D} {k} {b}\n")

        for fila in d:
            f.write(" ".join(map(str, fila)) + "\n")

    return d


def leer_dataset(path):

    with open(path, "r") as f:

        n = int(f.readline())
        D, k, b = map(int, f.readline().split())

        d = []

        for _ in range(n):
            d.append(list(map(int, f.readline().split())))

    return n, D, k, b, d
