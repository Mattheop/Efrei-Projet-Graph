from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from algorithms.bellman_ford import bellman_ford, bellman_ford_find_path
from algorithms.prims import prims_apcm
from display.display_bellman import json_guidage, map_guidage
from display.display_map import graph_to_map_stream
from models.Graph import Graph
from reader.EdgeReader import EdgeReader
from reader.PositionReader import PositionReader
from reader.VertexReader import VertexReader

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to localhost
)

vertex_reader = VertexReader("../data/metro.txt")
edge_reader = EdgeReader("../data/metro.txt")
position_reader = PositionReader("../data/pospoints.txt")

vertices = vertex_reader.read()
edge_reader.read(vertices)
position_reader.read(vertices)

graph = Graph.build(vertices)

vertices_dict = [{'id': k, 'name': v.nom, 'ligne': v.ligne_metro, 'x': v.x, 'y': v.y} for k, v in vertices.items()]


@app.get("/api/vertices")
async def get_vertices():
    return vertices_dict


@app.get("/api/bellmanford/{start}/{end}")
async def get_bellmanford(start: int, end: int):
    bellman_ford_result = bellman_ford(graph, vertices[start])
    bellman_ford_path_result = bellman_ford_find_path(vertices[end], bellman_ford_result)
    return json_guidage(vertices_dict, bellman_ford_path_result)


@app.get("/api/bellmanford/map/{start}/{end}")
async def get_map(start: int, end: int, background_tasks: BackgroundTasks):
    bellman_ford_result = bellman_ford(graph, vertices[start])
    bellman_ford_path_result = bellman_ford_find_path(vertices[end], bellman_ford_result)

    image_stream = map_guidage(bellman_ford_path_result)
    background_tasks.add_task(image_stream.close)

    return Response(content=image_stream.getvalue(), media_type="image/png")


@app.get("/api/prims/map")
async def get_prims_map(background_tasks: BackgroundTasks, duplicated_merge: bool = False):
    apcm = prims_apcm(graph, duplicated_merge)
    image_stream = graph_to_map_stream(apcm)
    background_tasks.add_task(image_stream.close)

    return Response(content=image_stream.getvalue(), media_type="image/png")


app.mount("/", StaticFiles(directory="web", html=True), name="static")
