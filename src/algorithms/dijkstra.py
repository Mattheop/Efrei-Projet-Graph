from typing import List

from models.Graph import Graph
from models.Vertex import Vertex


def dijkstra(graph: Graph, start: Vertex, end: Vertex) -> List[Vertex] or None:
    # Créez un dictionnaire pour stocker les distances minimales.
    distances = {vertex.num: float('inf') for vertex in graph.vertices.values()}
    distances[start.num] = 0

    # Créez un dictionnaire pour stocker les prédécesseurs des sommets.
    predecessors = {}

    # Créez un ensemble pour stocker les sommets non encore visités.
    unvisited_vertices = set(graph.vertices.values())

    while unvisited_vertices:
        # Trouvez le sommet non visité le plus proche.
        current_vertex = min(unvisited_vertices, key=lambda vertex: distances[vertex.num])

        # Parcourez tous les voisins du sommet courant.
        for edge in current_vertex.edges:
            neighbour = edge.sommet1 if edge.sommet1.num != current_vertex.num else edge.sommet2

            # Si le voisin n'a pas encore été visité, calculez la distance
            # entre le sommet courant et le voisin.
            if neighbour in unvisited_vertices:
                distance = distances[current_vertex.num] + edge.distance

                # Si la distance est plus courte que la distance stockée,
                # mettez à jour la distance et le prédécesseur.
                if distance < distances[neighbour.num]:
                    distances[neighbour.num] = distance
                    predecessors[neighbour.num] = current_vertex

        # Marquez le sommet courant comme visité et supprimez-le de l'ensemble.
        unvisited_vertices.remove(current_vertex)

    # Générer le chemin
    path = []
    while end.num != start.num:
        path.insert(0, (distances[end.num], end))
        end = predecessors[end.num]
    path.insert(0, (distances[start.num], start))

    return path
