import render
from dictionary import Color



class Graph: 
    edges = {}
    def __init__(self, m, n):

    # def up(self, j, i): return i + (2 * self.m + 1) * j    
    # def left(self, j, i): return i + (2 * self.m + 1) * j + self.m    
    # def right(self, j, i): return i + (2 * self.m + 1) * j + self.m + 1    
    # def down(self, j, i): return i + (2 * self.m + 1) * (j + 1)
    
    def add(self, e):
        x, y, rail_id = e.pos
        # A, B = None, None
        # if (rail_id == 1):
        #     A, B = self. left(x, y), self.right(x, y)
        # if (rail_id == 2):
        #     A, B = self.   up(x, y), self. down(x, y)
        # if (rail_id == 3):
        #     A, B = self.   up(x, y), self.right(x, y)
        # if (rail_id == 4):
        #     A, B = self.right(x, y), self. down(x, y)
        # if (rail_id == 5):
        #     A, B = self. down(x, y), self. left(x, y)
        # if (rail_id == 6):
        #     A, B = self. left(x, y), self.   up(x, y)

        # self.g[A].add((B, e))
        # self.g[B].add((A, e))
        if (x, y) not in self.edges:
            self.edges[(x, y)] = {}
        self.edges[(x, y)][rail_id] = e

    def get(self, pos):
        x, y, z = pos
        if ((x, y) in self.edges and z in self.edges[(x, y)]):
            return self.edges[(x, y)][z]
        return None

    def get_edges(self):
        for blocks in self.edges:
            for z, e in self.edges[blocks].items():
                yield e

    def render(self, sc):
        for e in self.get_edges():
            e.render(sc)
        for e in self.get_edges():
            e.render(sc, edge=False, unit=True)



class Edge:
    pos = (None, None, None)
    color = Color.GREEN
    unit = None
    def __init__(self, pos):
        self.pos = pos


    def render(self, sc, edge=True, unit=False):
        if edge:
            render.edge(sc, self)
        if unit and self.unit is not None:
            render.unit(sc, self.unit)    

    def __repr__(self):
        return f"Edge(pos: {self.pos} | unit: {self.unit})"