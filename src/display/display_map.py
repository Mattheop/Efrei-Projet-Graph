import io

from models.Graph import Graph
import numpy as np
from matplotlib import image as mpimg, pyplot as plt

from utils import paris_ligne_couleur


def graph_to_map_stream(graph: Graph) -> io.BytesIO:
    """
    Permet de générer une image de la carte du metro de Paris avec les sommets et les arrêtes
    provenant du graph passé en paramètre
    :param graph: Graph à représenter
    :return: BytesIO Stream, do not forget to close it.
    """

    stream_result = io.BytesIO()

    carte = mpimg.imread("../data/metrof_r.png")
    carte = np.flipud(carte)
    dimensions_carte = [0, 987, 0, 952]

    plt.figure(figsize=(15, 15), dpi=100)
    plt.axis('off')
    plt.imshow(carte, extent=dimensions_carte, aspect='equal', zorder=0, alpha=0.25)
    ax = plt.gca()
    ax.invert_yaxis()

    x = []
    y = []

    for sommet in graph.vertices.values():
        x.append(sommet.x)
        y.append(sommet.y)

    # link with red line the sommets
    for sommet in graph.vertices.values():
        for voisin in sommet.edges:
            # on vérifie si les deux sommets sont bien dans le graph
            # sinon, c'est que l'autre sommet n'est pas dans le graph
            # et donc on ne trace pas l'arrête
            if voisin.sommet1.num not in graph.vertices or voisin.sommet2.num not in graph.vertices:
                continue

            ligne = sommet.ligne_metro
            couleur = paris_ligne_couleur(ligne)
            plt.plot([voisin.sommet1.x, voisin.sommet2.x], [voisin.sommet1.y, voisin.sommet2.y], color=couleur,
                     linewidth=2)

    # Afficher les sommets comme des points sur la carte
    plt.scatter(x, y, marker='o', color='black', label='Sommets', zorder=2)

    # save to file to debug
    plt.savefig(stream_result, format="png", dpi=100, bbox_inches='tight', pad_inches=0, transparent=True)
    stream_result.seek(0)

    plt.close()

    return stream_result
