import time
from datetime import timedelta

from models.Edge import Edge
from models.Graph import Graph
from models.Vertex import Vertex


def copy_vertex(vertex: Vertex):
    cloned = Vertex(num=vertex.num, nom=vertex.nom, branchement=vertex.branchement, is_terminus=vertex.is_terminus,
                  ligne_metro=vertex.ligne_metro)

    cloned.x = vertex.x
    cloned.y = vertex.y

    return cloned


def prims_apcm(graph: Graph, duplicated_merge=False):
    apcm = Graph()
    already_visited = set()
    start = copy_vertex(graph.vertices[0])
    apcm.add_vertex(start)
    already_visited.add(start.num)

    total_time = 0

    while len(already_visited) != len(graph.vertices):
        selected = None
        min_distance = float('inf')

        for vertex in already_visited:
            for edge in graph.vertices[vertex].edges:
                if edge.sommet1.num not in already_visited or edge.sommet2.num not in already_visited:
                    if edge.distance < min_distance:
                        min_distance = edge.distance
                        selected = edge

        if selected:
            total_time += selected.distance
            selected_copy = Edge(sommet1=selected.sommet1, sommet2=selected.sommet2, distance=selected.distance)

            neighbour = selected.sommet1 if selected.sommet1.num not in already_visited else selected.sommet2

            neighbour_copy = copy_vertex(neighbour)

            neighbour_copy.edges.append(selected_copy)
            apcm.add_vertex(neighbour_copy)

            already_visited.add(selected.sommet1.num)
            already_visited.add(selected.sommet2.num)

            # now we need to add all station with the same name
            if duplicated_merge:
                for vertex in graph.vertices.values():
                    if vertex.nom == neighbour.nom and vertex.num not in already_visited:
                        already_visited.add(vertex.num)

    print(f"Temps total : {total_time} secondes")
    print(timedelta(seconds=total_time))
    return apcm
