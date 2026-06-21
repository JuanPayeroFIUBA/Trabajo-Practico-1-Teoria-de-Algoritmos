import random


def leer_dataset(path):
    with open(path, "r") as f:
        n = int(f.readline())
        D, k, b = map(int, f.readline().split())
        d = []
        for _ in range(n):
            d.append(list(map(int, f.readline().split())))

    return n, D, k, b, d
