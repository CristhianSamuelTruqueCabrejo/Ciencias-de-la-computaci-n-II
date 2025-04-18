import heapq
from collections import defaultdict, deque

def dijkstra(graph, start, N):
    dist = [float('inf')] * N
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, cost in graph[u]:
            if dist[v] > dist[u] + cost:
                dist[v] = dist[u] + cost
                heapq.heappush(pq, (dist[v], v))
    return dist

def bfs_backtrack(rev_graph, dist, start, end):
    visited = [False] * len(dist)
    queue = deque([end])
    edges_to_remove = set()
    while queue:
        u = queue.popleft()
        if visited[u]:
            continue
        visited[u] = True
        for v, cost in rev_graph[u]:
            if dist[v] + cost == dist[u]:
                edges_to_remove.add((v, u))
                queue.append(v)
    return edges_to_remove

def solve():
    while True:
        N, M = map(int, input().split())
        if N == 0 and M == 0:
            break

        S, D = map(int, input().split())

        graph = defaultdict(list)
        rev_graph = defaultdict(list)

        for _ in range(M):
            u, v, p = map(int, input().split())
            graph[u].append((v, p))
            rev_graph[v].append((u, p))

        dist = dijkstra(graph, S, N)

        if dist[D] == float('inf'):
            print(-1)
            continue

        edges_to_remove = bfs_backtrack(rev_graph, dist, S, D)

        # Construir un nuevo grafo sin las aristas del camino más corto
        new_graph = defaultdict(list)
        for u in range(N):
            for v, p in graph[u]:
                if (u, v) not in edges_to_remove:
                    new_graph[u].append((v, p))

        new_dist = dijkstra(new_graph, S, N)
        print(new_dist[D] if new_dist[D] != float('inf') else -1)

# Ejecutar la solución
solve()
