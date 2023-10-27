from typing import List


def triowise(target: List) -> List[tuple[List, List, List]]:
    return [(current,
             target[idx - 1] if idx >= 1 else None,
             target[idx + 1] if idx < len(target) - 1 else None) for idx, current in
            enumerate(target)]


def paris_ligne_couleur(ligne: str) -> str:
    metro_paris = {
        "1": "#FFCD00",  # Jaune
        "2": "#003CA6",  # Bleu
        "3": "#75A23D",  # Vert
        "3bis": "#75A23D",  # Vert
        "4": "#E30074",  # Rose
        "5": "#FF9700",  # Orange
        "6": "#B5A642",  # Vert
        "7": "#E30074",  # Rose
        "7bis": "#E30074",  # Rose
        "8": "#C1A470",  # Crème
        "9": "#906EAF",  # Mauve
        "10": "#D05D10",  # Rouge
        "11": "#009E49",  # Vert
        "12": "#FDCF0A",  # Dorée
        "13": "#4490A6",  # Azur
        "14": "#6E1E96"  # Violet
    }

    if ligne in metro_paris:
        return metro_paris[ligne]

    return "black"
