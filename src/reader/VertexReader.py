import re

from models.Vertex import Vertex


class VertexReader:
    """
    Classe permettant de lire les sommets d'un graphe depuis un fichier.
    """
    REGEX_PATTERN = r'V (\d+) (.*?);(.*?) ;(True|False) (\d+)'.replace(" ", r"\s*")

    def __init__(self, file_path: str) -> None:
        """
        Constructeur de la classe VertexReader.
        :param file_path: Chemin vers le fichier contenant les sommets
        """
        self.file_path = file_path
        self.debug = False

    def read(self) -> dict[int, Vertex]:
        """
        Lit le fichier et retourne une liste de sommets
        On rappelle un exemple de ligne du fichier :
        V num_sommet nom_sommet ;numéro_ligne ;si_terminus branchement
        V 0000 Abbesses ;12 ;False 0
        :return: La liste des Sommet(s)
        """

        sommets = {}
        with open(self.file_path, "r") as file:
            for line in file:
                match = re.match(self.REGEX_PATTERN, line)
                if match:
                    num = int(match.group(1))
                    nom = match.group(2).strip()
                    ligne_metro = match.group(3).strip()
                    is_terminus = match.group(4).strip() == "True"
                    branchement = int(match.group(5))

                    sommets[num] = Vertex(num, nom, ligne_metro, is_terminus, branchement)
                else:
                    if line.startswith("V") and self.debug:
                        print(f"La ligne {line} n'a pas été reconnue")

        return sommets
