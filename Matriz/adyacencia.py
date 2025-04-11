import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class GrafoVisual:
    def __init__(self, matriz_adyacencia):
        """
        Inicializa el grafo con una matriz de adyacencia.
        :param matriz_adyacencia: Matriz cuadrada (lista de listas o numpy array).
        """
        self.matriz = np.array(matriz_adyacencia)
        self.num_nodos = len(self.matriz)
        self.grafo = nx.Graph()  # Grafo no dirigido (para dirigido, usa nx.DiGraph)

        # Añadir nodos y aristas al grafo de networkx
        for i in range(self.num_nodos):
            self.grafo.add_node(i)
            for j in range(i, self.num_nodos):  # Evita duplicados en no dirigido
                if self.matriz[i][j] == 1:
                    self.grafo.add_edge(i, j)

    def dibujar_grafo(self, layout='spring', titulo="Grafo a partir de matriz de adyacencia"):
        """
        Dibuja el grafo usando matplotlib.
        :param layout: 'spring' (default), 'circular', 'random', etc.
        :param titulo: Título del gráfico.
        """
        # Seleccionar disposición de los nodos
        if layout == 'spring':
            pos = nx.spring_layout(self.grafo)
        elif layout == 'circular':
            pos = nx.circular_layout(self.grafo)
        else:
            pos = nx.random_layout(self.grafo)

        # Dibujar el grafo
        plt.figure(figsize=(8, 6))
        nx.draw_networkx(
            self.grafo,
            pos,
            with_labels=True,
            node_color='skyblue',
            node_size=800,
            font_size=12,
            font_weight='bold',
            edge_color='gray'
        )
        plt.title(titulo)
        plt.axis('off')
        plt.show()

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Matriz de adyacencia (ejemplo: grafo no dirigido)
    matriz_ejemplo = [
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
    ]

    # Crear y dibujar el grafo
    grafo_visual = GrafoVisual(matriz_ejemplo)
    grafo_visual.dibujar_grafo(layout='circular', titulo="Grafo de ejemplo (no dirigido)")