#!/usr/bin/python3

from glyphs import TERMS, NAMES, term_to_str, str_to_term
from units import *
from dictionary import Good
from graph import *

BATCH = 3


def parse_field(fin, x, y):
    field = list(map(lambda x: list(x.strip('\n')), fin.readlines((x) * y * BATCH ** 2)))
    if len(field) != y * BATCH:
        raise IOError(f"Wrong map format. Too many rows ({BATCH} * {y} != {len(field)})")
    for f in range(len(field)):
        if len(field[f]) != x * BATCH:
            raise IOError(f"Wrong map format. Too many symbols in row {f + 1} ({BATCH} * {x} != {len(field[f])})")
    def batching(field):
        batched = [[
                    [["" for i in range(BATCH)] for i in range(BATCH)] 
                    for i in range(x)]
                    for i in range(y)] 
        for i in range(y * BATCH):
            for j in range(x * BATCH):
                batched[i // BATCH][j // BATCH][i % BATCH][j % BATCH] = field[i][j]
        return batched

    bfield = batching(field)
    named_map = [["" for i in range(x)] for i in range(y)]
    for i in range(y):
        for j in range(x):
            if (term_to_str(bfield[i][j]) not in NAMES):
                raise IOError(f"Unknown block '{term_to_str(bfield[i][j])}' at")
            named_map[i][j] = NAMES[term_to_str(bfield[i][j])]
    return named_map


def graphify(named_map):
    n = len(named_map)
    m = len(named_map[0])
    
    g = Graph(n, m)

    def edges(typ, i, j):
        if typ[0] == "P":
            if typ[1] == "H":
                yield Edge((i, j, 1), platform=typ[2])
            if typ[1] == "V":
                yield Edge((i, j, 2), platform=typ[2])
        if typ[0] == "R":
            mask = int(typ[1:])
            if mask & (1 << 0) > 0: yield Edge((i, j, 1))
            if mask & (1 << 1) > 0: yield Edge((i, j, 2))
            if mask & (1 << 2) > 0: yield Edge((i, j, 3))
            if mask & (1 << 3) > 0: yield Edge((i, j, 4))
            if mask & (1 << 4) > 0: yield Edge((i, j, 5))
            if mask & (1 << 5) > 0: yield Edge((i, j, 6))
        
        return

    for j in range(n):
        for i in range(m):
            if (named_map[j][i][0] in {"R", "P"}):
                for e in edges(named_map[j][i], i, j):
                    g.add(e)
    return g


def parse_units(fin, t, graph):
    fin_wagons = fin.readlines()
    wagons = [None]  # Nones are for placeholding as IDs start with 1
    trains = [None]
    for w in fin_wagons:
        typ, x, y, z, *oth = w.strip().split()
        x, y, z = map(int, [x, y, z])
        if (typ == "L"):
            loco = Loco(graph, (x, y, z))
            wagons.append(loco)
            trains.append(Train(loco, graph))
        else:
            capacity = 5
            good_load = Good.EMPTY
            loaded = 0
            if len(oth) >= 1:
                capacity, oth = oth[0], oth[1:]
            if len(oth) >= 1:
                good_load, oth = eval(oth[0]), oth[1:]
            if len(oth) >= 1:
                loaded, oth = eval(oth[0]), oth[1:]

            wagon_type = Unit
            
            avaliable_types = {
                "P": Platform,
                "H": Hopper,
                "B": Boxcar,
                "T": Tank,
                "D": Dumpcar,
                "G": Gondola
            }
            if typ in avaliable_types:
                wagon_type = avaliable_types[typ]
                wagons.append(wagon_type(graph, (x, y, z), capacity, good_load, loaded))
            else:
                wagons.append(Unit(graph, (x, y, z)))
    return wagons, trains


def parse_scenario(file):
    fin = open(file, 'r')
    tasks = fin.readlines()



def parse_map(file):
    fin = open(file, 'r')
    x, y, t = map(int, fin.readline().split())
    named_map = parse_field(fin, x, y)
    graph = graphify(named_map)
    # buffer string
    fin.readline()
    wagons, trains = parse_units(fin, t, graph)

    return named_map, graph, wagons, trains