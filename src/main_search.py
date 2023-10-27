from algorithms.bellman_ford import bellman_ford, bellman_ford_find_path
from display.display_bellman import display_guidage
from models.Graph import Graph
from reader.EdgeReader import EdgeReader
from reader.VertexReader import VertexReader


def main():
    sommet_reader = VertexReader("../data/metro.txt")
    edge_reader = EdgeReader("../data/metro.txt")

    sommets = sommet_reader.read()
    edge_reader.read(sommets)

    ligne_input = input("Entrez la ligne de métro: ")
    filtered_sommets = {k: v for k, v in sommets.items() if v.ligne_metro == ligne_input}

    for sommet in filtered_sommets.values():
        print(sommet)

    name_input = input("Entrez le nom de la station: ")
    for sommet in filtered_sommets.values():
        if name_input.lower() in sommet.nom.lower():
            print(sommet)


if __name__ == "__main__":
    main()
