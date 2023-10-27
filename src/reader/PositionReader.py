from models.Vertex import Vertex
from reader.VertexReader import VertexReader


class PositionReader:
    """
    Classe permettant de lire les positions des sommets d'un graphe depuis un fichier.
    """

    def __init__(self, file_path: str) -> None:
        """
        Constructeur de la classe PositionReader.
        :param file_path: Chemin vers le fichier contenant les positions
        """
        self.file_path = file_path

    def read(self, sommets: dict[int, Vertex]):
        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue

                x = float(line.split(";")[0])
                y = float(line.split(";")[1])
                nom_sommet = line.split(";")[2].replace("@", " ").strip()

                sommets_numbers = [sommet.num for sommet in sommets.values() if sommet.nom == nom_sommet]

                if len(sommets_numbers) == 0:
                    print(f"Sommet {nom_sommet} non trouvé")
                    continue

                for sommet_number in sommets_numbers:
                    sommets[sommet_number].x = int(x)
                    sommets[sommet_number].y = int(y)

if __name__ == "__main__":
    sommet_reader = VertexReader("../../data/metro.txt")
    sommets = sommet_reader.read()

    position_reader = PositionReader("../../data/pospoints.txt")
    position_reader.read(sommets)