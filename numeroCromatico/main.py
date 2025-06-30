def greedy_graph_coloring(adj_matrix):
    n = len(adj_matrix)
    colors = [-1] * n  # Inicializar todos los vértices sin color
    k = 0  # Número cromático

    # Orden de los vértices (puede ser orden natural o otro orden)
    vertices = range(n)

    for v in vertices:
        # Colores no disponibles para v (colores de sus vecinos)
        unavailable_colors = set()
        for u in range(n):
            if adj_matrix[v][u] == 1 and colors[u] != -1:
                unavailable_colors.add(colors[u])

        # Asignar el menor color disponible
        c = 0
        while c in unavailable_colors:
            c += 1
        colors[v] = c
        k = max(k, c + 1)  # Actualizar número cromático

    return  k

adj_matrix = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0]
]

print(f"numero cromatico: {greedy_graph_coloring(adj_matrix)}")