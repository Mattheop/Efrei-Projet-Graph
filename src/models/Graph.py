from models.Vertex import Vertex


class Graph:
    """
    Classe représentant un graphe.
    """
    vertices: dict[int, Vertex]

    def __init__(self) -> None:
        self.vertices = {}

    def add_vertex(self, vertex: Vertex) -> None:
        """
        Ajoute un sommet au graphe.
        :param vertex: Sommet à ajouter
        """

        self.vertices[vertex.num] = vertex

    def is_connected(self) -> bool:
        """
        Vérifie si le graphe est connexe.
        :rtype: boolean
        :return: True si le graphe est connexe, False sinon
        """

        visited = set()
        start = list(self.vertices.values())[0]
        self.dfs(start, visited)

        return len(visited) == len(self.vertices)

    def dfs(self, start: Vertex, visited: set[int]) -> None:
        """
        Parcours en profondeur du graphe utilisant la récursivité.
        À la fin de l'exécution, le set visited contient tous les sommets visités.
        :param start: Sommet de départs restant à visiter
        :param visited: Sommets déjà visités
        """
        visited.add(start.num)
        for edge in start.edges:
            neighbour = edge.sommet1 if edge.sommet1.num != start.num else edge.sommet2
            if neighbour.num not in visited:
                self.dfs(neighbour, visited)

    @classmethod
    def build(cls, vertex: dict[int, Vertex]):
        aGraph = cls()

        for i in vertex.values():
            aGraph.add_vertex(i)

        return aGraph
