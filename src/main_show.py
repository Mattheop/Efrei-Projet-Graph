import numpy as np
from matplotlib import image as mpimg, pyplot as plt

from algorithms.prims import prims_apcm
from models.Graph import Graph
from reader.EdgeReader import EdgeReader
from reader.PositionReader import PositionReader
from reader.VertexReader import VertexReader
from utils import paris_ligne_couleur


def main():
    sommet_reader = VertexReader("../data/metro.txt")
    edge_reader = EdgeReader("../data/metro.txt")
    position_reader = PositionReader("../data/pospoints.txt")

    sommets = sommet_reader.read()
    edge_reader.read(sommets)
    position_reader.read(sommets)

    filtered_sommets = sommets
    graph_main = Graph.build(filtered_sommets)
    graph = prims_apcm(graph_main)


    carte = mpimg.imread("../data/metrof_r.png")
    carte = np.flipud(carte)
    dimensions_carte = [0, 987, 0, 952]

    # Créer le graphique avec l'image de fond
    plt.figure(figsize=(15, 15), dpi=200)
    plt.imshow(carte, extent=dimensions_carte, aspect='equal', zorder=0, alpha=0.5)
    ax = plt.gca()
    ax.invert_yaxis()

    x = []
    y = []

    for sommet in graph.vertices.values():
        x.append(sommet.x)
        y.append(sommet.y)

    # Afficher les sommets comme des points sur la carte
    plt.scatter(x, y, marker='o', color='black', label='Sommets')

    # link with red line the sommets
    for sommet in graph.vertices.values():
        for voisin in sommet.edges:
            ligne = sommet.ligne_metro
            couleur = paris_ligne_couleur(ligne)
            plt.plot([voisin.sommet1.x, voisin.sommet2.x], [voisin.sommet1.y, voisin.sommet2.y], color=couleur, linewidth=2)
    plt.savefig("test.png")

    plt.show()

if __name__ == "__main__":
    main()
