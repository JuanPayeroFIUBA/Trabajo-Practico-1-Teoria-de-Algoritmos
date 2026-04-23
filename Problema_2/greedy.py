def main():
    n = int(input("INGRESE EL NUMERO DE VERTICES: "))
    print()

    # 40-60: creo las estructuras de datos. La matriz de adyacencia
    cost = []
    for i in range(n + 1):
        fila = []
        for j in range(n + 1):
            fila.append(0)
        cost.append(fila)
    dist = [0] * (n + 1)  # Guarda la distacia minima acumulada de cada nodo
    sol = [0] * (n + 1)  # Marcador para determinar que nodos fueron visitados

    print("INGRESE EL CUADRO DE COSTOS (INGRESE 0,0 PARA TERMINAR)\n")

    # 100 - 130: Cargo los datos al grafo
    while True:
        linea = input("EL EJE (A,B): ")
        a, b = map(int, linea.split(","))
        if a == 0:
            break
        costo_eje = int(input("COSTO DEL EJE: "))
        cost[a][b] = costo_eje

    # 140-180: Agrego peso infinito(15000) a las aristas que no existen
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if cost[i][j] == 0:
                cost[i][j] = 15000

    # 190-230: Hacer el grafo no dirigido, para implementar dikstra
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            cost[i][j] = cost[j][i]

    # Bucle principal de ejecución
    while True:
        v = int(input("INGRESE EL VERTICE DE SALIDA: "))

        # Limpiar estados
        for i in range(1, n + 1):
            dist[i] = cost[v][i]
            sol[i] = 0

        dijkstra(n, v, cost, dist, sol)

        print("SALIDA", "LLEGADA", "DISTANCIA")

        for i in range(1, n + 1):
            if dist[i] < 15000:
                print(f"{v}\t {i}\t {dist[i]}")

        res = input("OTRA VEZ? (SI/NO): ").strip().upper()
        if res == "NO":
            break

        for i in range(1, n + 1):
            sol[i] = 0
            dist[i] = 0


# 1000-1120: algoritmo dijktra
def dijkstra(n, v, cost, dist, sol):
    sol[v] = 1
    dist[v] = 0
    for i in range(1, n):
        u_val = 15000
        u = -1

        for j in range(1, n + 1):
            if dist[j] <= u_val and sol[j] == 0:
                u_val = dist[j]
                u = j

        if u != -1:
            sol[u] = 1
            for j in range(1, n + 1):
                if dist[j] >= (dist[u] + cost[u][j]):
                    dist[j] = dist[u] + cost[u][j]


if __name__ == "__main__":
    main()
