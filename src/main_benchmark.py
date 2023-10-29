import time

from algorithms.bellman_ford import bellman_ford, bellman_ford_find_path
from algorithms.dijkstra import dijkstra
from algorithms.prims import prims_apcm
from models.Graph import Graph
from reader.EdgeReader import EdgeReader
from reader.VertexReader import VertexReader


def main():
    NUM_START = 163
    NUM_TARGET = 179
    TIMES = 100

    sommet_reader = VertexReader("../data/metro.txt")
    edge_reader = EdgeReader("../data/metro.txt")

    sommets = sommet_reader.read()
    edge_reader.read(sommets)

    graph = Graph.build(sommets)

    # is_connected
    delta = []
    for i in range(TIMES):
        start_time = time.perf_counter_ns()
        graph.is_connected()
        end_time = time.perf_counter_ns()
        delta.append((end_time - start_time) / 1000000)

    print("Moyenne en ms is_connected: " + str(sum(delta) / len(delta)))
    print(delta)

    # Bellman Ford
    delta = []
    delta2 = []
    for i in range(TIMES):
        start_time = time.perf_counter_ns()
        result = bellman_ford(graph, graph.vertices[NUM_START])
        end_time = time.perf_counter_ns()
        delta.append((end_time - start_time) / 1000000)
        bellman_ford_find_path(graph.vertices[NUM_TARGET], result)
        end_time = time.perf_counter_ns()
        delta2.append((end_time - start_time) / 1000000)

    print("Moyenne en ms Bellman Ford Etape 1: " + str(sum(delta) / len(delta)))
    print("Moyenne en ms Bellman Ford Total: " + str(sum(delta2) / len(delta2)))

    print(delta)

    # dijkstra
    delta = []
    for i in range(TIMES):
        start_time = time.perf_counter_ns()
        dijkstra(graph, graph.vertices[NUM_START], graph.vertices[NUM_TARGET])
        end_time = time.perf_counter_ns()
        delta.append((end_time - start_time) / 1000000)

    print("Moyenne en ms Dijkstra: " + str(sum(delta) / len(delta)))
    print(delta)

    # prims
    delta = []
    for i in range(TIMES):
        start_time = time.perf_counter_ns()
        prims_apcm(graph)
        end_time = time.perf_counter_ns()
        delta.append((end_time - start_time) / 1000000)

    print("Moyenne en ms Prim: " + str(sum(delta) / len(delta)))
    print(delta)


if __name__ == "__main__":
    main()
