class Task:
    cmd = ""
    params = []
    id = 0
    callback = None
    callback_params = []
    def __init__(self, taskline):
        cmd, *other = taskline.split()
        self.cmd = cmd
        Task.id += 1
        self.id = Task.id
        self.params = other
        print(cmd, other)
    def __repr__(self):
        return f"<{self.id} comand - [{self.cmd} {' '.join(self.params)}]>"
    def start(self, callback = (lambda: False), *callback_params):
        self.callback = callback
        self.callback_params = callback_params
    def is_ended(self) -> bool:
        #print(f"Calling back task {self.id}: {self.callback(*self.callback_params)}")
        return self.callback(*self.callback_params)



class Scenario:
    depended_from_task = []
    task_status = []
    tasks = []
    
    waiting_tasks = set()
    ready_tasks = set()
    processing_tasks = set()


    def __init__(self, fin):
        tasklist = fin.readlines()
        self.depended_from_task = [[] for i in range(len(tasklist) + 1)]
        self.task_status = [None for i in range(len(tasklist) + 1)]
        self.tasks = [None for i in range(len(tasklist) + 1)]
        for i, t in enumerate(tasklist, 1):
            comand, dependencies = t.split('|')
            comand = comand.strip()
            dependencies = list(map(int, dependencies.split()))
            task = Task(comand)
            self.tasks[i] = task
            for j in dependencies:
                self.depended_from_task[j].append(i)
            self.task_status[i] = len(dependencies)

        for i in range(1, len(self.task_status)):
            if self.task_status[i] == 0:
                self.waiting_tasks.add(i)
    
    def __repr__(self):
        output = []
        for i in range(1, len(self.tasks)):
            output.append("<<<")
            output.append(f"   Task: {self.tasks[i]},")
            output.append(f"   Status: {self.task_status[i]},")
            output.append(f"   Dependents: {self.depended_from_task[i]}")
            output.append(">>>")

        output.append(f"Waiting: {self.waiting_tasks}")
        output.append(f"Processing: {self.processing_tasks}")
        output.append(f"Ready: {self.ready_tasks}")

        return '\n'.join(output)

    def start_task(self, i, callback, *params):
        self.waiting_tasks.remove(i)
        self.processing_tasks.add(i)
        self.tasks[i].start(callback, *params)

    def end_task(self, i):
        self.processing_tasks.remove(i)
        self.ready_tasks.add(i)
        for d in self.depended_from_task[i]:
            self.task_status[d] -= 1
            if (self.task_status[d] == 0):
                self.waiting_tasks.add(d)

    def get_waiting_tasks(self):
        return [self.tasks[i] for i in self.waiting_tasks]
    def process(self):
        #print(self.task_status)
        for w in set(self.processing_tasks):
            if self.tasks[w].is_ended():
                self.end_task(w)

