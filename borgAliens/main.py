import sys
from collections import deque

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        fx = self.find(x)
        fy = self.find(y)
        if fx != fy:
            self.parent[fy] = fx

def compute_distances(maze, nodes, pos_to_idx, y_size, x_size):
    n_nodes = len(nodes)
    distance = [[0] * n_nodes for _ in range(n_nodes)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for i in range(n_nodes):
        start_row, start_col = nodes[i]
        visited = [[False] * x_size for _ in range(y_size)]
        q = deque()
        q.append((start_row, start_col, 0))
        visited[start_row][start_col] = True
        remaining = n_nodes - 1  # Excluir el propio nodo
        
        dist_i = [float('inf')] * n_nodes
        dist_i[i] = 0
        
        if remaining == 0:
            distance[i] = dist_i
            continue
        
        while q and remaining > 0:
            row, col, d = q.popleft()
            
            for dr, dc in directions:
                nr = row + dr
                nc = col + dc
                if 0 <= nr < y_size and 0 <= nc < x_size and not visited[nr][nc] and maze[nr][nc] != '#':
                    visited[nr][nc] = True
                    new_d = d + 1
                    
                    # Verificar si esta posición es un nodo importante
                    if (nr, nc) in pos_to_idx:
                        j = pos_to_idx[(nr, nc)]
                        if new_d < dist_i[j]:
                            if j != i and dist_i[j] == float('inf'):
                                remaining -= 1
                            dist_i[j] = new_d
                            if remaining == 0:
                                break
                    q.append((nr, nc, new_d))
            if remaining == 0:
                break
        
        for j in range(n_nodes):
            distance[i][j] = dist_i[j]
    
    return distance

def main():
    input = sys.stdin.read().splitlines()
    idx = 0
    n = int(input[idx])
    idx += 1
    for _ in range(n):
        x, y = map(int, input[idx].split())
        idx += 1
        maze = []
        for _ in range(y):
            line = input[idx].strip('\n')
            maze.append(line)
            idx += 1
        
        # Recolectar nodos importantes (S y A)
        nodes = []
        for row in range(y):
            for col in range(x):
                c = maze[row][col]
                if c in ('S', 'A'):
                    nodes.append((row, col))
        
        # Mapear coordenadas a índices
        pos_to_idx = {(r, c): i for i, (r, c) in enumerate(nodes)}
        n_nodes = len(nodes)
        if n_nodes == 0:
            print(0)
            continue
        
        # Calcular matriz de distancias
        distance = compute_distances(maze, nodes, pos_to_idx, y, x)
        
        # Generar aristas
        edges = []
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                if distance[i][j] != float('inf'):
                    edges.append((distance[i][j], i, j))
        edges.sort()
        
        # Algoritmo de Kruskal para MST
        uf = UnionFind(n_nodes)
        total_cost = 0
        edges_added = 0
        for edge in edges:
            weight, u, v = edge
            if uf.find(u) != uf.find(v):
                uf.union(u, v)
                total_cost += weight
                edges_added += 1
                if edges_added == n_nodes - 1:
                    break
        
        print(total_cost)

if __name__ == "__main__":
    main()