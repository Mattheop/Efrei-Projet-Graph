import re

from models.Edge import Edge
from models.Vertex import Vertex


class EdgeReader:
    """
    Classe permettant de lire les arêtes d'un graphe depuis un fichier.
    """
    REGEX_PATTERN = r'E (\d+) (\d+) (\d+)'

    def __init__(self, file_path: str) -> None:
        """
        Constructeur de la classe EdgeReader.
        :param file_path: Chemin vers le fichier contenant les arêtes
        """
        self.file_path = file_path

    def read(self, sommets: dict[int, Vertex]) -> None:
        """
        Lit les arêtes du graphe depuis le fichier.
        Et mets à jour les sommets concernés dans le dictionnaire sommets.
        :param sommets: Dictionnaire des sommets du graphe à mettre à jour
        """
        with open(self.file_path, "r") as file:
            for line in file:
                line_match = re.match(self.REGEX_PATTERN, line)
                if line_match:
                    numero_sommet1 = int(line_match.group(1))
                    numero_sommet2 = int(line_match.group(2))
                    distance = int(line_match.group(3))

                    if numero_sommet1 not in sommets or numero_sommet2 not in sommets:
                        print(f"Sommet {numero_sommet1} ou {numero_sommet2} non trouvé")
                        continue

                    # on récupère les sommets correspondants
                    sommet1 = sommets[numero_sommet1]
                    sommet2 = sommets[numero_sommet2]

                    # on crée l'arête
                    edge = Edge(sommet1, sommet2, distance)

                    # on ajoute l'arête aux sommets correspondants
                    sommet1.edges.append(edge)
                    sommet2.edges.append(edge)