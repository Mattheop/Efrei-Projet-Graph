class Vertex:
    """
    Classe représentant un sommet du graphe.
    """

    num: int
    nom: str
    ligne_metro: str
    is_terminus: bool
    branchement: int
    edge: list
    x: int
    y: int

    def __init__(self, num: int, nom: str, ligne_metro: str, is_terminus: bool, branchement: int) -> None:
        """
        Constructeur de la classe Vertex.
        :param num: Numéro du sommet
        :param nom: Nom du sommet
        :param ligne_metro: Ligne de métro du sommet
        :param is_terminus: True si le sommet est un terminus, False sinon
        :param branchement: Numéro du sommet de branchement, -1 si le sommet n'est pas un branchement
        """

        self.num = num
        self.nom = nom
        self.ligne_metro = ligne_metro
        self.is_terminus = is_terminus
        self.branchement = branchement

        self.edges = []
        self.x = 0
        self.y = 0

    def __str__(self) -> str:
        """
        :rtype: string
        :return: Représentation du sommet sous forme de string
        """
        return f"Sommet {self.num} : {self.nom} (ligne {self.ligne_metro}) {self.is_terminus} {', '.join([str(edge) for edge in self.edges])}"
