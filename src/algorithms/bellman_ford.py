from typing import List

from models import Graph
from models.Vertex import Vertex


def bellman_ford(graph: Graph, source: Vertex) -> dict[int, int]:
    """
    Algorithme de Bellman-Ford. Pour rappel algo one to all. Prend en charge les poids négatifs.
    Mais pas les cycles de poids négatifs.
    Source / mémo révisions :
        - https://fr.wikipedia.org/wiki/Algorithme_de_Bellman-Ford
        - https://www.youtube.com/watch?v=obWXjtg0L64 ← INCROYABLE
    :param graph: Graphe à parcourir
    :param source: Sommet de départ
    :raise Exception: Si le graphe contient un cycle de poids négatif.
    :return: Dictionnaire numéro du sommet : distance
    """
    # on commence par initialiser toutes les distances à l'infini et celle de la source à 0
    # et ceux pour tous les sommets du graphe
    distances = {vertex.num: float('inf') for vertex in graph.vertices.values()}
    distances[source.num] = 0

    # on itère sur tous les sommets - 1 pour revenir au besoin sur les sommets déjà visités utilisé en
    # cas des poids négatifs
    for _ in range(len(graph.vertices) - 1):
        # on itère sur tous les sommets
        for vertex in graph.vertices.values():
            # on itère sur tous les voisins du sommet
            for edge in vertex.edges:
                neighbour = edge.sommet1 if edge.sommet1.num != vertex.num else edge.sommet2
                # on vérifie si on a trouvé un chemin plus court
                if neighbour.num in distances and vertex.num in distances:
                    if distances[vertex.num] + edge.distance < distances[neighbour.num]:
                        # si c'est le cas, on met à jour la distance
                        distances[neighbour.num] = distances[vertex.num] + edge.distance

    # Vérification de la présence de cycles de poids négatif
    # si apres n-1 itérations, on trouve encore un chemin plus court,
    # c'est qu'il y a un cycle de poids négatif
    # Est-ce qu'on veut vraiment savoir ou non ?
    for vertex in graph.vertices.values():
        for edge in vertex.edges:
            if edge.sommet1.num in distances and edge.sommet2.num in distances:
                if distances[vertex.num] + edge.distance < distances[edge.sommet2.num]:
                    raise Exception("Le graphe contient un cycle de poids négatif.")

    return distances


def bellman_ford_find_path(target_vertex: Vertex, distances: dict[int, int]) -> List[tuple[int, Vertex]]:
    """
    Fonction permettant de retrouver le chemin le plus court entre le sommet source et le sommet cible
    avec le dictionnaire des distances de l'algorithme de Bellmanford.

    :param target_vertex: Sommet cible
    :param distances: résultat de l'algorithme de Bellman-Ford
    :return: Liste de tuples représentant le parcours (distance, sommet)
    """

    # si le sommet cible n'est pas dans le dictionnaire des distances
    # ou que cette distance est infinie, c'est qu'il n'est pas atteignable
    if target_vertex.num not in distances or distances[target_vertex.num] == float('inf'):
        return []

    path = []
    current_vertex = target_vertex

    # on boucle tant que le sommet la distance du sommet courant est différente de 0,
    # c'est-à-dire tant que le sommet courant n'est pas le sommet source
    while distances[current_vertex.num] != 0:
        # on ajoute le sommet courant au chemin (en amont ! pour avoir le chemin dans l'ordre source vers target)
        path.insert(0, (distances[current_vertex.num], current_vertex))

        # on boucle sur les arrêtes du sommet courant
        for edge in current_vertex.edges:
            # on récupère le voisin du sommet courant
            # car une arrête relie deux sommets dont le sommet courant et le voisin,
            # on souhaite donc récupérer le voisin et non le sommet courant
            neighbour = edge.sommet1 if edge.sommet1.num != current_vertex.num else edge.sommet2

            # si la distance du voisin est égale à la distance du sommet courant + le poids de l'arrête
            # c'est que le voisin est le sommet précédent dans le chemin
            if neighbour.num in distances and distances[current_vertex.num] == distances[neighbour.num] + edge.distance:
                # il devient donc le sommet courant pour la prochaine itération
                current_vertex = neighbour
                break

    # on ajoute le sommet source au chemin
    path.insert(0, (0, current_vertex))

    return path
