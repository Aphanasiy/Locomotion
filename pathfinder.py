from graph import Graph, Edge
from units import Train, graph_rules




class FindPath:
    img_train = None
    dest = None

    def __init__(self, train, where_head_supposed_to_be_pos):
        self.img_train = ImaginaryTrain(train)
        self.dest = where_head_supposed_to_be_pos

    def gen_path(self, mode):
        if mode == "BFS":
            bfs()


    def bfs():
        (x = 0)



class ImaginaryTrain:
    train = None
    snake = []
    graph = None
    init_pos = None

    def __init__(self, train, graph):
        self.train = train
        self.graph = graph
        if isinstance(train, Train):
            self.snake = [u.edge.pos for u in ([train.head] + train.wagons)]
        elif isinstance(train, ImaginaryTrain):
            self.snake = train.snake

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
        print(allowed)
        return allowed_head, allowed_tail

    def move(self, to_pos, forward=None):
        moved_train = ImaginaryTrain(self)
        if (forward == True):
            moved_train.snake = [to_pos] + moved_train.snake[:-1]
        if (forward == False):
            moved_train.snake = moved_train.snake[1:] + [to_pos]
        return moved_train