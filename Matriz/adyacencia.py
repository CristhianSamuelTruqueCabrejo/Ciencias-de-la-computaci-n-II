# Matriz/adyacencia.py  
import matplotlib.pyplot as plt
import networkx as nx

def crear_grafo_desde_matriz(matriz, dirigido=False):
    """
    Crea un grafo (dirigido o no dirigido) a partir de una matriz de adyacencia.
    
    Parámetros:
        matriz (list of list): matriz de adyacencia (0s y 1s)
        dirigido (bool): True para grafo dirigido, False para no dirigido
        
    Retorna:
        G (networkx.Graph o networkx.DiGraph): grafo construido
    """
    G = nx.DiGraph() if dirigido else nx.Graph()
    n = len(matriz)

    # Añadir nodos
    for i in range(n):
        G.add_node(i)

    # Añadir aristas
    for i in range(n):
        for j in range(n):
            if matriz[i][j] == 1:
                G.add_edge(i, j)

    return G

def mostrar_grafo(G, titulo="Representación del Grafo"):
    """
    Muestra el grafo usando Matplotlib.
    
    Parámetros:
        G (networkx.Graph o networkx.DiGraph): grafo a visualizar
        titulo (str): título de la visualización
    """
    pos = nx.spring_layout(G)
    dirigido = G.is_directed()

    nx.draw(G, pos, with_labels=True, node_color='lightgreen', edge_color='gray', 
            node_size=1500, font_size=12, arrows=dirigido, arrowstyle='->', arrowsize=20)
    
    plt.title(titulo)
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    matriz_adyacencia = [
    [0, 1, 0, 0, 1],  # Nodo 0 → Nodo 1 y Nodo 4
    [0, 0, 1, 0, 0],  # Nodo 1 → Nodo 2
    [1, 0, 0, 1, 0],  # Nodo 2 → Nodo 0 y Nodo 3
    [0, 0, 0, 0, 1],  # Nodo 3 → Nodo 4
    [0, 0, 0, 0, 0]   # Nodo 4 → sin salidas
]

    es_dirigido = True  # Cambia a False si quieres grafo no dirigido
    grafo = crear_grafo_desde_matriz(matriz_adyacencia, dirigido=es_dirigido)
    mostrar_grafo(grafo, titulo="Grafo Dirigido" if es_dirigido else "Grafo No Dirigido")
