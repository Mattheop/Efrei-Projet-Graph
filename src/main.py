from datetime import timedelta

from algorithms.bellman_ford import bellman_ford, bellman_ford_find_path
from algorithms.prims import prims_apcm
from display.display_bellman import display_guidage
from models.Graph import Graph
from reader.EdgeReader import EdgeReader
from reader.VertexReader import VertexReader


def main():
    """
    Cherche le chemin le plus court entre deux sommets
    Utiliser src/main_search.py pour trouver le numéro des sommets
    Ce script permet juste de faire marcher les algorithmes
    Une version web avec src/server.py
    """
    NUM_START = int(input("Entrez le numéro du sommet de départ (Ledru Rollin = 163): "))
    NUM_TARGET = int(input("Entrez le numéro du sommet d'arrivée (Mairie d'Ivry = 179): "))

    # lecture des données
    sommet_reader = VertexReader("../data/metro.txt")
    edge_reader = EdgeReader("../data/metro.txt")
    sommets = sommet_reader.read()
    edge_reader.read(sommets)

    graph = Graph.build(sommets)

    # Verification connexité
    if not graph.is_connected():
        print("Le graphe n'est pas connexe.")
        return

    print("Le graphe est connexe.")

    # Bellman Ford
    bellman_ford_result = bellman_ford(graph, sommets[NUM_START])
    bellman_ford_find_path_result = bellman_ford_find_path(sommets[NUM_TARGET], bellman_ford_result)
    print("Chemin le plus court de {} ligne {} à {} ligne {}".format(sommets[NUM_START].nom,
                                                                     sommets[NUM_START].ligne_metro,
                                                                     sommets[NUM_TARGET].nom,
                                                                     sommets[NUM_TARGET].ligne_metro))

    display_guidage(bellman_ford_find_path_result)

    # Prims
    apcm = prims_apcm(graph)
    total = 0
    for v in apcm.vertices.values():
        for edge in v.edges:
            total += edge.distance

    print("Distance totale de l'arbre couvrant minimal: " + str(timedelta(seconds=total)))


if __name__ == "__main__":
    main()
