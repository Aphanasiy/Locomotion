from graph import Graph, Edge
from units import Train, graph_rules

from dictionary import Color


class Path():
    path_container = []
    graph = None
    rcolors = (None, None)
    def __init__(self, graph, path, reserved_colors = (Color.RED, Color.RED)):
        self.graph = graph
        self.path_container = path
        self.rcolors = reserved_colors
        self.render()
    def render(self):
        #print(*self.path_container, sep='\n')
        for p in self.path_container:
            a, b = p[0]
            self.graph.get(a).color = self.rcolors[0]
            self.graph.get(b).color = self.rcolors[1]
    def next(self, iteration=True):
        if (len(self.path_container) == 0):
            return None
        if iteration:
            nxt = self.path_container.pop()
            self.graph.get(nxt[0][0]).color = Color.GREEN
            self.graph.get(nxt[0][1]).color = Color.GREEN
            self.render()
        else:
            nxt = self.path_container[-1]
        return nxt

    def __repr__(self):
        return "Path:\n" + "\n".join(f"    {a, b}" for a, b in self.path_container)



class FindPath:
    img_train = None
    dest = None
    graph = None
    stopcond = None #  head / tail
    def __init__(self, train, graph, where_unit_supposed_to_be_pos, side="head"):
        self.img_train = ImaginaryTrain(train, graph)
        self.dest = where_unit_supposed_to_be_pos
        self.graph = graph
        self.stopcond = side
    def gen_path(self, find_all=False, mode="BFS"):
        if mode == "BFS":
            history, ans = self.bfs(find_all)
        if len(ans) == 0:
            return None
        else:

            pth = [(ans[0].get_snake_pos(), 0)]
            while history[pth[-1][0]][0] is not (None, None, None):
                pth.append(history[pth[-1][0]])
                #print("uf:", pth[-1])
            spath = []
            shift = 0
            for ends, drct in pth[::-1]:
                spath.append((ends, shift))
                shift = drct
            return Path(self.graph, spath[:0:-1])
    def bfs(self, find_all):
        history = {self.img_train.get_snake_pos() : ((None, None, None), 1)}
        queue = [self.img_train] 
        next_level = []
        ans = []
        found = False
        trainside = 0 if self.stopcond == "head" else 1
        while queue != [] and not found:
            for q in queue:
                #print(q, found, q.get_snake_pos()[0], self.dest)
                if q.get_snake_pos()[trainside] == self.dest:  
                    ans.append(q)
                    if not find_all: found = True
                allhead, alltail = q.allowed_moves()
                for nx_gen, fif in ([(q.move(am, forward=True), 1) for am in allhead] + [(q.move(am, forward=False), -1) for am in alltail]):
                    if nx_gen.get_snake_pos() not in history:
                        history[nx_gen.get_snake_pos()] = (q.get_snake_pos(), fif)
                        #print("++")
                        next_level.append(nx_gen)
            queue = next_level
            next_level = []
            #print(">>>", len(queue))

        return history, ans


class ImaginaryTrain:
    snake = []
    graph = None
    init_pos = None
    gen = 0

    def __init__(self, train, graph):
        self.graph = graph
        if isinstance(train, Train):
            self.snake = [u.edge.pos for u in ([train.head] + train.wagons)]
        elif isinstance(train, ImaginaryTrain):
            self.snake = train.snake
            self.gen = train.gen + 1

    def __repr__(self):
        return f"<ImTrain: head/tail {self.snake[0], self.snake[-1]} | gen {self.gen}>"

    def allowed_moves(self):
        def fdeny(unit_pos):
            def filtering(allowed):
                return allowed[:2] != unit_pos[:2]
            return filtering

        allowed_head = graph_rules(self.snake[0], self.graph, mode="move")
        allowed_tail = set()
        if len(self.snake) > 1:
            allowed_tail = graph_rules(self.snake[-1], self.graph, mode="move")
        if len(self.snake) > 1:
            deny = lambda unit: (lambda allowed: allowed[:2] != unit.edge.pos[:2])
            allowed_head = set(filter(fdeny(self.snake[1]) , allowed_head))
            allowed_tail = set(filter(fdeny(self.snake[-2]), allowed_tail))
        allowed = allowed_head | allowed_tail
        #print("iAllowed:", allowed)
        return allowed_head, allowed_tail

    def move(self, to_pos, forward=None):
        moved_train = ImaginaryTrain(self, self.graph)
        if (forward == True):
            moved_train.snake = [to_pos] + moved_train.snake[:-1]
        if (forward == False):
            moved_train.snake = moved_train.snake[1:] + [to_pos]
        return moved_train

    def get_snake_pos(self):
        return (self.snake[0], self.snake[-1])
