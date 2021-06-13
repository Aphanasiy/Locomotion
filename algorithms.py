from graph import Graph, Edge
from units import Train, graph_rules

from dictionary import Color


class Path():
    path_container = []
    graph = None
    rcolors = (None, None)
    final_point = None
    train = None
    def __init__(self, graph, path_container,
                 final_point=(None, None, None), # point@(x, y, z), head/tail, safe/unsafe
                 reserved_colors = (Color.PATH_RESERVED, Color.PATH_RESERVED)):
        self.graph = graph
        self.rcolors = reserved_colors
        self.path_container = path_container
        self.render()
        self.final_point = final_point
    def render(self):
        #print(*self.path_container, sep='\n')
        is_reserved = False
        i = len(self.path_container)
        for i in range(len(self.path_container) - 1, -1, -1):
            a, b = self.path_container[i][0]
            direction = self.path_container[i][1]
            print(a, b)
            is_reserved = any(map(lambda x: x.reserved,
                                  (self.graph.get_edges_by_block(*a[:2]) if direction ==  1 else []) + \
                                  (self.graph.get_edges_by_block(*b[:2]) if direction == -1 else [])))    
            if is_reserved: break
        print("-|-|-", i, len(self.path_container))
        for p in self.path_container[i + is_reserved * 2:]:
            a, b = p[0]
            self.graph.get(a).reserved = True
            self.graph.get(b).reserved = True
    def next(self, iteration=True):
        if (len(self.path_container) == 0):
            return None, None
        nxt = self.path_container[-1]
        nxt1, nxt2 = nxt[0]
        direction = nxt[1]
        if (direction ==  1 and not self.graph.get(nxt1).reserved or 
            direction == -1 and not self.graph.get(nxt2).reserved):
            self.render()
            if (direction ==  1 and not self.graph.get(nxt1).reserved or 
                direction == -1 and not self.graph.get(nxt2).reserved):
                return False, None
        if iteration:
            nxt = self.path_container.pop()
            self.render()
        return True, nxt
    def __repr__(self):
        return "Path:\n" + "\n".join(f"    {a, b}" for a, b in self.path_container)
    def regenerate_path(self, train, mode="BFS"):
        return FindPath(train, self.graph, self.final_point[0], 
                                      side=self.final_point[1], 
                                      safe=self.final_point[2]).gen_path(mode=mode)
    def clear(self):
        i = -1
        while (i >= -len(self.path_container)):
            print(i)
            a, b = self.path_container[i][0]
            print(a, b)
            if self.graph.get(a).reserved or self.graph.get(b).reserved:
                self.graph.get(a).reserved = False
                self.graph.get(b).reserved = False
            else:
                break
            i -= 1


 
class FindPath:
    img_train = None
    dest = None
    graph = None
    stopcond = None #  head / tail
    safe = False
    def __init__(self, train, graph, where_unit_supposed_to_be_pos, side="head", safe=False):
        self.img_train = ImaginaryTrain(train, graph)
        self.dest = where_unit_supposed_to_be_pos
        self.graph = graph
        self.stopcond = side
        self.safe = safe
    def gen_path(self, find_all=False, mode="BFS"):
        if mode == "BFS":
            history, ans = self.bfs(find_all, safe_mode=self.safe)
        if len(ans) == 0:
            return None
        else:

            pth = [(ans[0].get_snake_pos(), 0)]
            while history[pth[-1][0]][0] != (None, None, None):
                pth.append(history[pth[-1][0]])
                #print("uf:", pth[-1])
            spath = []
            shift = 0
            for ends, drct in pth[::-1]:
                spath.append((ends, shift))
                shift = drct
            final_point = (self.dest, self.stopcond, self.safe)
            return Path(self.graph, spath[:0:-1], final_point=final_point)
    def bfs(self, find_all, safe_mode=False):
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
                for nx_gen, fif in ([(q.move(am, forward=True, safe_mode=safe_mode), 1) for am in allhead] + [(q.move(am, forward=False), -1) for am in alltail]):
                    if nx_gen is None:
                        continue
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

    def move(self, to_pos, forward=None, safe_mode=False):
        moved_train = ImaginaryTrain(self, self.graph)
        if safe_mode and self.graph.get(to_pos).reserved:
            return None
        if (forward == True):
            moved_train.snake = [to_pos] + moved_train.snake[:-1]
        if (forward == False):
            moved_train.snake = moved_train.snake[1:] + [to_pos]
        return moved_train

    def get_snake_pos(self):
        return (self.snake[0], self.snake[-1])
