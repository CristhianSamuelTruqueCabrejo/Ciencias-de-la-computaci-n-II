import heapq
from collections import deque, defaultdict

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w
    
    def __lt__(self, other):
        return self.w < other.w

def main():
    import sys
    input = sys.stdin.read().split('\n')
    ptr = 0
    N = int(input[ptr])
    ptr += 1
    
    for _ in range(N):
        while ptr < len(input) and input[ptr].strip() == '':
            ptr += 1
        if ptr >= len(input):
            break
            
        x, y = map(int, input[ptr].split())
        ptr += 1
        
        # Leer el laberinto
        maze = []
        vertices = []
        g = []
        imap = {}
        top = 0
        
        for i in range(y):
            while ptr < len(input) and input[ptr].strip() == '':
                ptr += 1
            if ptr >= len(input):
                s = ''
            else:
                s = input[ptr].rstrip('\n')
                ptr += 1
            
            row = []
            for j in range(len(s)):
                c = s[j]
                row.append(c)
                if c == 'A' or c == 'S':
                    g.append((i, j))
                    imap[(i, j)] = top
                    top += 1
                    vertices.append((i, j))
                elif c == ' ':
                    g.append((i, j))
                    imap[(i, j)] = top
                    top += 1
            maze.append(row)
        
        V = len(g)
        adj = [[] for _ in range(V)]
        
        # Construir lista de adyacencia
        for ii in range(V):
            i, j = g[ii]
            if j-1 >= 0 and maze[i][j-1] != '#':
                adj[ii].append(imap[(i, j-1)])
            if j+1 < x and maze[i][j+1] != '#':
                adj[ii].append(imap[(i, j+1)])
            if i-1 >= 0 and maze[i-1][j] != '#':
                adj[ii].append(imap[(i-1, j)])
            if i+1 < y and maze[i+1][j] != '#':
                adj[ii].append(imap[(i+1, j)])
        
        INF = 10000
        dist = [[INF]*V for _ in range(V)]
        
        # Dijkstra para cada vértice importante
        VV = len(vertices)
        for ss in range(VV):
            s = imap[vertices[ss]]
            dist[s][s] = 0
            heap = []
            heapq.heappush(heap, (0, s))
            
            while heap:
                current_dist, u = heapq.heappop(heap)
                if current_dist > dist[s][u]:
                    continue
                
                for v in adj[u]:
                    if dist[s][u] + 1 < dist[s][v]:
                        dist[s][v] = dist[s][u] + 1
                        heapq.heappush(heap, (dist[s][v], v))
        
        # Construir grafo para MST
        gg = [[] for _ in range(VV)]
        for i in range(VV):
            for j in range(i+1, VV):
                ii = imap[vertices[i]]
                jj = imap[vertices[j]]
                weight = dist[ii][jj]
                gg[i].append(Edge(i, j, weight))
                gg[j].append(Edge(j, i, weight))
        
        # Algoritmo de Prim para MST
        marked = [False] * VV
        sum_mst = 0
        heap = []
        marked[0] = True
        
        for edge in gg[0]:
            heapq.heappush(heap, edge)
        
        mst_edges = 0
        while mst_edges < VV-1 and heap:
            e = heapq.heappop(heap)
            u, v, w = e.u, e.v, e.w
            
            if marked[u] and marked[v]:
                continue
            
            if marked[u]:
                marked[v] = True
                for edge in gg[v]:
                    heapq.heappush(heap, edge)
            elif marked[v]:
                marked[u] = True
                for edge in gg[u]:
                    heapq.heappush(heap, edge)
            
            sum_mst += w
            mst_edges += 1
        
        print(sum_mst)

if __name__ == "__main__":
    main()