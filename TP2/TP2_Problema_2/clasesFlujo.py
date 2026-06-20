from collections import deque


class Vertice:
    def __init__(self, hacia, capacidad):
        self.hacia = hacia
        self.capacidad = capacidad
        self.flujo = 0
        self.rev = None


class MaxFlow:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_vertice(self, u, v, cap):
        fwd = Vertice(v, cap)
        rev = Vertice(u, 0)

        fwd.rev = rev
        rev.rev = fwd

        self.graph[u].append(fwd)
        self.graph[v].append(rev)

    def bfs(self, s, t):
        parent = [None] * self.n
        parent[s] = (s, None)
        q = deque([s])
        while q:
            u = q.popleft()
            for e in self.graph[u]:
                residual = e.capacidad - e.flujo
                if residual > 0 and parent[e.hacia] is None:
                    parent[e.hacia] = (u, e)
                    if e.hacia == t:
                        return parent
                    q.append(e.hacia)

        return None

    def edmonds_karp(self, s, t):
        max_flujo = 0
        while True:
            parent = self.bfs(s, t)
            if parent is None:
                break
            bottleneck = float("inf")
            v = t
            while v != s:
                u, e = parent[v]
                bottleneck = min(bottleneck, e.capacidad - e.flujo)
                v = u
            v = t

            while v != s:
                u, e = parent[v]
                e.flujo += bottleneck
                e.rev.flujo -= bottleneck
                v = u

            max_flujo += bottleneck

        return max_flujo
