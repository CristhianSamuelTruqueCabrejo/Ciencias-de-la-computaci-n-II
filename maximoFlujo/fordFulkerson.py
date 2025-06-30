class Graph:
    def __init__(self, size):
        self.adj_list = [[] for _ in range(size)]  # Incidence list representation
        self.size = size
        self.vertex_data = [''] * size

    def add_edge(self, u, v, c):
        # Add forward edge with capacity
        self.adj_list[u].append({'to': v, 'capacity': c, 'flow': 0})
        # Add reverse edge with 0 capacity
        self.adj_list[v].append({'to': u, 'capacity': 0, 'flow': 0})

    def add_vertex_data(self, vertex, data):
        if 0 <= vertex < self.size:
            self.vertex_data[vertex] = data

    def dfs(self, s, t, visited=None, path=None):
        if visited is None:
            visited = [False] * self.size
        if path is None:
            path = []

        visited[s] = True
        path.append(s)

        if s == t:
            return path

        for edge in self.adj_list[s]:
            v = edge['to']
            residual = edge['capacity'] - edge['flow']
            if not visited[v] and residual > 0:
                result_path = self.dfs(v, t, visited, path.copy())
                if result_path:
                    return result_path

        return None

    def fordFulkerson(self, source, sink):
        max_flow = 0

        path = self.dfs(source, sink)
        while path:
            # Find minimum residual capacity in the path
            path_flow = float("Inf")
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                # Find the edge between u and v
                for edge in self.adj_list[u]:
                    if edge['to'] == v:
                        residual = edge['capacity'] - edge['flow']
                        path_flow = min(path_flow, residual)
                        break

            # Update flows along the path
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                # Update forward edge
                for edge in self.adj_list[u]:
                    if edge['to'] == v:
                        edge['flow'] += path_flow
                        break
                # Update reverse edge
                for edge in self.adj_list[v]:
                    if edge['to'] == u:
                        edge['flow'] -= path_flow
                        break

            max_flow += path_flow

            path_names = [self.vertex_data[node] for node in path]
            print("Path:", " -> ".join(path_names), ", Flow:", path_flow)

            path = self.dfs(source, sink)

        return max_flow


# Example usage
g = Graph(1000)
vertex_names = ['s', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 't']
for i, name in enumerate(vertex_names):
    g.add_vertex_data(i, name)

g.add_edge(0, 1, 17)  # s  -> v1, cap: 17
g.add_edge(0, 2, 14)  
g.add_edge(0, 3, 14) 
g.add_edge(0, 4, 9) 
g.add_edge(1, 2, 3)  
g.add_edge(3, 4, 5) 
g.add_edge(1, 5, 5)
g.add_edge(1, 6, 7)
g.add_edge(2, 6, 4)
g.add_edge(2, 7, 5)
g.add_edge(3, 7, 4)
g.add_edge(4, 8, 7)
g.add_edge(5, 9, 8)
g.add_edge(5, 6, 10)
g.add_edge(7, 8, 2)
g.add_edge(5, 10, 17)
g.add_edge(6, 10, 11)
g.add_edge(7, 11, 7)
g.add_edge(8, 11, 15)
g.add_edge(9, 11, 9)
g.add_edge(11, 10, 6)
g.add_edge(10, 12, 25)
g.add_edge(11, 12, 29)


source = 0; sink = 12

print("The maximum possible flow is %d " % g.fordFulkerson(source, sink))