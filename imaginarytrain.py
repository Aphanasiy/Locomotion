from graph import Graph, Edge
from units import Train, graph_rules



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
        print("iAllowed:", allowed)
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
