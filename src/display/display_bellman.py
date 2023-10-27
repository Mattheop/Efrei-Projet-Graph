import io
from datetime import timedelta
from typing import List, Union

from display.display_map import graph_to_map_stream
from models.Graph import Graph
from models.Vertex import Vertex
from utils import triowise


def json_guidage(vertices_dict: list[dict[str, Union[str, int]]], bellman_ford_find_path_result: List[tuple[int, Vertex]]) -> List[dict]:
    result = []
    for current, previous, next in triowise(bellman_ford_find_path_result):
        if previous is None or current[1].ligne_metro != previous[1].ligne_metro:
            result.append({
                'start_duration_seconds': current[0],
                'start_duration_formatted': str(timedelta(seconds=current[0])),
                'end_duration_seconds': next[0] if next is not None else current[0],
                'end_duration_formatted': str(timedelta(seconds=next[0] if next is not None else current[0])),
                'ligne': current[1].ligne_metro,
                'next_ligne': next[1].ligne_metro if next is not None else None,
                'stations': []
            })

        result[-1]['stations'].append({
            'name': current[1].nom,
            'num': current[1].num,
            'acc_duration_seconds': current[0],
            'correspondances': [v['ligne'] for v in vertices_dict if v['name'] == current[1].nom and v['id'] != current[1].num],
        })

        result[-1]['end_duration_seconds'] = current[0]
        result[-1]['end_duration_formatted'] = str(timedelta(seconds=current[0]))
        result[-1]['next_ligne'] = next[1].ligne_metro if next is not None else None

    return result



def display_guidage(bellman_ford_find_path_result: List[tuple[int, Vertex]]) -> None:
    for current, previous, next in triowise(bellman_ford_find_path_result):
        formatted_duration = str(timedelta(seconds=current[0]))

        if previous is None:
            print(f"{formatted_duration} - Je suis à {current[1].nom} et je prend la ligne {current[1].ligne_metro}")
        elif next is None:
            print(f"{formatted_duration} - Je suis arrivé à {current[1].nom} en {current[0]} secondes")
        else:
            if previous[1].ligne_metro != current[1].ligne_metro:
                print(f"{formatted_duration} - Je change de la ligne {previous[1].ligne_metro} à {current[1].nom} pour prendre la ligne {next[1].ligne_metro}")
            else:
                print(f"{formatted_duration} - Je continue sur la ligne {current[1].ligne_metro} pour aller à {current[1].nom}")

def map_guidage(bellman_ford_find_path_result: List[tuple[int, Vertex]]) -> io.BytesIO:
    vertices = {k: v for k, v in [(sommet[1].num, sommet[1]) for sommet in bellman_ford_find_path_result]}
    graph = Graph.build(vertices)

    return graph_to_map_stream(graph)