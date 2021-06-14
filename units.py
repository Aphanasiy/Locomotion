import render
from dictionary import Color, Good


COOLDOWN = 5


class Unit:
    graph = None
    edge = None
    id = 0
    color = Color.WHITE
    coupled = False
    def __init__(self, graph, pos):
        self.edge = graph.get(pos)
        self.edge.unit = self
        self.id = Unit.id = Unit.id + 1


    def render(self, sc):
        render.unit(sc, self)

    def move(self, new_edge):
        #print(self.edge)
        self.edge.unit = None
        self.edge = new_edge
        #print(self.edge)
        if (self.edge.unit):
            raise Exception("This edge already has an another unit")
        self.edge.unit = self

class Loco(Unit):
    coupled=True
    def __init__(self, graph, pos):
        self.color = Color.ORANGE
        super().__init__(graph, pos)
    
    def __repr__(self):
        return f"<Unit ID: {self.id} | Position: {self.edge.pos} | Locomotive>"


class Wagon(Unit):
    capacity = None
    loaded = 0
    good_loaded = Good.EMPTY
    goods = []

    def __init__(self, graph, pos, capacity, good = Good.EMPTY, loaded = 0):
        super().__init__(graph, pos)
        self.capacity = capacity
        self.good_loaded = good
        self.loaded = loaded

    def load(self, count, loading_good):
        if self.edge.platform is None:
            raise Exception("Wagon is not at the platform")
        loading_good = eval(f"Good.{loading_good}")
        if self.good_loaded != Good.EMPTY and loading_good != self.good_loaded:
            raise Exception("There's another good type already in the wagon")
        self.good_loaded = loading_good
        self.loaded += count
        if self.loaded > self.capacity:
            raise Exception("The capacity of the wagon is less than load task says")

    def unload(self, count):
        if self.edge.platform is None:
            raise Exception("Wagon is not at the platform")
        self.loaded -= count
        if (self.loaded == 0):
            self.good_loaded = Good.EMPTY
        if (self.loaded < 0):
            raise Exception("There are less goods in wagon than unload task says")

    def __repr__(self):
        return f"<Unit ID: {self.id} | Position {self.edge.pos} | {type(self).__name__} | Loaded: {self.good_loaded.value} ({self.loaded}/{self.capacity}) >"


class Platform(Wagon):
    def __init__(self, graph, pos, capacity, good=Good.EMPTY, loaded=0):
        self.color = Color.VIOLET
        super().__init__(graph, pos, capacity, good, loaded)

class  Boxcar(Wagon):    #Крытый
    def __init__(self, graph, pos, capacity, good=Good.EMPTY, loaded=0):
        self.color = Color.GREEN
        super().__init__(graph, pos, capacity, good, loaded)

class Gondola(Wagon):   #Полувагон
    def __init__(self, graph, pos, capacity, good=Good.EMPTY, loaded=0):
        self.color = Color.BLACK
        super().__init__(graph, pos, capacity, good, loaded)

class  Hopper(Wagon):    #Хоппер
    def __init__(self, graph, pos, capacity, good=Good.EMPTY, loaded=0):
        self.color = Color.PINK
        super().__init__(graph, pos, capacity, good, loaded)

class Dumpcar(Wagon):
    def __init__(self, graph, pos, capacity, good=Good.EMPTY, loaded=0):
        self.color = Color.BROWN
        super().__init__(graph, pos, capacity, good, loaded)

class    Tank(Wagon):      #Цистерна
    def __init__(self, graph, pos, capacity, good=Good.EMPTY, loaded=0):
        self.color = Color.BLUE
        super().__init__(graph, pos, capacity, good, loaded)


def graph_rules(pos, graph=None, mode="move"): #mode: move/couple
    d = set()
    pre_d = []
    x, y, z = pos
    if (z == 1):
        pre_d = [
            {(x - 1, y, 1),
             (x - 1, y, 3),
             (x - 1, y, 4)},
            {(x + 1, y, 1),
             (x + 1, y, 5),
             (x + 1, y, 6)},
        ]
    elif (z == 2):
        pre_d = [
            {(x, y - 1, 2),
             (x, y - 1, 4),
             (x, y - 1, 5)},
            {(x, y + 1, 2),
             (x, y + 1, 3),
             (x, y + 1, 6)}
        ]
    elif (z == 3):
        pre_d = [
            {(x + 1, y, 1),
             (x + 1, y, 5)},
            {(x, y - 1, 2),
             (x, y - 1, 5)}
        ]
    elif (z == 4):
        pre_d = [
            {(x + 1, y, 1),
             (x + 1, y, 6)},
            {(x, y + 1, 2),
             (x, y + 1, 6)}
        ]
    elif (z == 5):
        pre_d = [
            {(x - 1, y, 1),
             (x - 1, y, 3)},
            {(x, y + 1, 2),
             (x, y + 1, 3)}
        ]
    elif (z == 6):
        pre_d = [
            {(x - 1, y, 1),
             (x - 1, y, 4)},
            {(x, y - 1, 2),
             (x, y - 1, 4)}
        ]
    def no_units(l_rails):
        for r in l_rails:
            #print(r)
            e = graph.get(r)
            if e and e.unit:
                return False
        return True
    existing_edge = lambda x: graph.get(x)

    # Sensitive block

    if mode == "move":
        pre_d = filter(no_units, pre_d)

    for i in pre_d:
        d |= set(filter(existing_edge, i))

    if mode == "couple":
        d = set(filter(lambda e: graph.get(e).unit, d))
    return d


class Train:
    head = None
    graph = None
    wagons = []
    path = None
    id = 0
    cooldown = COOLDOWN
    previous_status = None
    def __init__(self, main_unit, graph):
        if (not isinstance(main_unit, Loco)):
            raise Exception(f"Train must be initialized with a Locomotive. It was initialized with {unit} instead.")
        self.head = main_unit
        self.id = Train.id = Train.id + 1
        self.graph = graph
        self.wagons = []

    def __repr__(self):
        r = []
        r.append(f"\nTrain T{self.id} (")
        r.append(f"L: {self.head}")
        r.extend([f"{i + 1}: {self.wagons[i]}" for i in range(len(self.wagons))])
        r.append(")")
        return '\n'.join(r)

    def allowed_moves(self):
        def fdeny(unit):
            def filtering(allowed):
                return allowed[:2] != unit.edge.pos[:2]
            return filtering

        allowed_head = graph_rules(self.head.edge.pos, self.graph, mode="move")
        allowed_tail = set()
        if self.wagons != []:
            allowed_tail = graph_rules(self.wagons[-1].edge.pos, self.graph, mode="move")
        if len(self.wagons) > 0:
            deny = lambda unit: (lambda allowed: allowed[:2] != unit.edge.pos[:2])
            allowed_head = set(filter(fdeny(self.wagons[0]), allowed_head))
            if len(self.wagons) == 1:
                allowed_tail = set(filter(fdeny(self.head), allowed_tail))
            else:
                allowed_tail = set(filter(fdeny(self.wagons[-2]), allowed_tail))
        allowed = allowed_head | allowed_tail
        #print("Allowed:", allowed)
        
        return allowed_head, allowed_tail


    def single_move(self, pos, check=True, forward=None):
        
        # Is allowed move
        if check:
            allhead, alltail = self.allowed_moves(self.graph)
            if pos not in (allhead | alltail):
                print(f"This move is not allowed: {pos} not in {allhead | alltail}")
                return
            else:
                print(f"Moving train T{self.id} to {pos}")


            if pos in allhead:
                forward = True
            else:
                forward = False                

        if forward:
            if self.wagons:
                self.wagons[-1].edge.reserved = False
            else:
                self.head.edge.reserved = False
            last_pos = self.head.edge.pos
            self.head.move(self.graph.get(pos))
            for w in self.wagons:
                pos = last_pos
                last_pos = w.edge.pos
                w.move(self.graph.get(pos))
        else:
            self.head.edge.reserved = False
            last_pos = pos
            for w in self.wagons[::-1]:
                last_pos = w.edge.pos
                w.move(self.graph.get(pos))
                pos = last_pos
            self.head.move(self.graph.get(pos))
        

    def set_path(self, path):
        if self.path is not None:
            self.path.clear()
        self.path = path
        self.previous_status = None
        print("Path setted")
        #print(self.path.path_container)

    def process(self):
        if self.path is None:
            return
        if (self.cooldown > 0):
            self.cooldown -= 1
            return
        
        allowed, next_move = self.path.next(False)
        #print(">>> ", self.id, allowed, self.previous_status)
        if allowed is None:
            self.previous_status = allowed
            self.path = None
            for u in [self.head] + self.wagons:
                u.edge.reserved = False
            return
        elif allowed:
            if (self.previous_status is not None and self.previous_status == False):
                #print("!!! !!! !!! GEN_NEW_PATH !!! !!! !!!")
                new_path = self.path.regenerate_path(self)
                if (new_path is None):
                    previous_status = False
                else:
                    self.set_path(new_path)
                    self.previous_status = allowed
                self.cooldown = 2 * COOLDOWN
                return
            _, next_move = self.path.next()
            self.cooldown = COOLDOWN
            self.previous_status = allowed
    
        else:
            self.previous_status = allowed
            self.path.render()
            self.cooldown = 2 * COOLDOWN
            return
        self.single_move(next_move[0][((next_move[1] - 1)// 2)], check=False, forward=((next_move[1] + 1) // 2))

    def couple(self, graph, unit):
        if (len(self.wagons) > 0):
            def fdeny(unit):
                def filtering(allowed):
                    return allowed[:2] != unit.edge.pos[:2]
                return filtering
            deny_unit = self.head
            if (len(self.wagons) > 1):
                deny_unit = self.wagons[-2]
            allowed = set(filter(fdeny(deny_unit), graph_rules(self.wagons[-1].edge.pos, graph, mode="couple")))

        else:
            allowed = graph_rules(self.head.edge.pos, graph, mode="couple")
        #print(allowed, [graph.get(x).unit for x in allowed])
        if (not unit in [graph.get(x).unit for x in allowed]):
            print(f"Failed to couple {unit} to {self})")
            return False
        self.wagons.append(unit)
        unit.coupled=True
        return True

    def uncouple(self, n):
        for w in self.wagons[-n:]:
            w.coupled = False
        self.wagons = self.wagons[:-n]

