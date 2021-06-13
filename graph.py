import render
from dictionary import Color



class Graph: 
    edges = {}
    def __init__(self, n, m):
        pass

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

    def get_edges_by_block(self, x, y):
        return [self.get((x, y, z)) for z in self.edges[(x, y)]]

    def render(self, sc):
        for e in self.get_edges():
            e.render(sc)
        for e in self.get_edges():
            e.render(sc, edge=False, unit=True)



class Edge:
    pos = (None, None, None)
    unit = None
    reserved = False
    platform = None
    def __init__(self, pos, platform=None):
        self.pos = pos
        self.platform = platform


    def render(self, sc, edge=True, unit=False):
        if edge:
            color = Color.PATH_BASE if not self.reserved else Color.PATH_RESERVED
            render.edge(sc, self, color)
            render.draw_platform(sc, *self.pos[:2], self.platform)
        if unit and self.unit is not None:
            render.unit(sc, self.unit)    

    def __repr__(self):
        return f"Edge(pos: {self.pos} | unit: {self.unit})"

    def is_reserved(self): return self.reserved