from algorithms.bellman_ford import bellman_ford, bellman_ford_find_path
from display.display_bellman import display_guidage
from models.Graph import Graph
from reader.EdgeReader import EdgeReader
from reader.VertexReader import VertexReader


def main():
    NUM_START = 163
    NUM_TARGET = 179

    sommet_reader = VertexReader("../data/metro.txt")
    edge_reader = EdgeReader("../data/metro.txt")

    sommets = sommet_reader.read()
    edge_reader.read(sommets)

    filtered_sommets = {k: v for k, v in sommets.items() if v.ligne_metro == "7" or v.ligne_metro == "5" or v.ligne_metro == "8"}
    graph = Graph.build(filtered_sommets)

    bellman_ford_result = bellman_ford(graph, filtered_sommets[NUM_START])
    bellman_ford_find_path_result = bellman_ford_find_path(filtered_sommets[NUM_TARGET], bellman_ford_result)
    print("Chemin le plus court de {} ligne {} à {} ligne {}".format(filtered_sommets[NUM_START].nom,
                                                                     filtered_sommets[NUM_START].ligne_metro,
                                                                     filtered_sommets[NUM_TARGET].nom,
                                                                     filtered_sommets[NUM_TARGET].ligne_metro))

    display_guidage(bellman_ford_find_path_result)


if __name__ == "__main__":
    main()
