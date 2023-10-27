# prim's algo, graph is represented as an v by v adjacency list
def prims(self):
    # used to pick minimum weight edge
    key = [self.INF for _ in range(self.V)]
    # used to store MST
    parent = [None for _ in range(self.V)]
    # pick a random vertex, ie 0
    key[0] = 0
    # create list for t/f if a node is connected to the MST
    mstSet = [False for _ in range(self.V)]
    # set the first node to the root (ie have a parent of -1)
    parent[0] = -1

    for _ in range(self.V):
        # 1) pick the minimum distance vertex from the current key
        # from the set of points not yet in the MST
        u = self.minKey(key, mstSet)
        # 2) add the new vertex to the MST
        mstSet[u] = True

        # loop through the vertices to update the ones that are still
        # not in the MST
        for v in range(self.V):
            # if the edge from the newly added vertex (v) exists,
            # the vertex hasn't been added to the MST, and
            # the new vertex's distance to the graph is greater than the distance
            # stored in the initial graph, update the "key" value to the
            # distance initially given and update the parent of
            # of the vertex (v) to the newly added vertex (u)
            if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                key[v] = self.graph[u][v]
                parent[v] = u

    self.printMST(parent)