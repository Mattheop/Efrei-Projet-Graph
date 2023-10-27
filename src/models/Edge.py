from models.Vertex import Vertex


class Edge:
    """
    Classe représentant une arête entre deux sommets.
    """
    sommet1: Vertex
    sommet2: Vertex
    distance: int

    def __init__(self, sommet1: Vertex, sommet2: Vertex, distance: int) -> None:
        """
        Constructeur de la classe Edge.
        :param sommet1: Sommet 1 de l'arête
        :param sommet2: Sommet 2 de l'arête
        :param distance: Poids de l'arête, représentant la distance entre les deux sommets
        """
        self.sommet1 = sommet1
        self.sommet2 = sommet2
        self.distance = distance

    def __str__(self) -> str:
        """
        :rtype: string
        :return: Représentation de l'arête sous forme de string
        """
        return str(self.sommet1.nom) + "<->" + str(self.sommet2.nom) + "(" + str(self.distance) + "m)"
