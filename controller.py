from . import todolist



class Controller:
    def __init__(self, todolist: model.ToDoList):
        self.todolist = todolist

    def get_all_tasks(self) -> list[model.Task]:
        return self.todolist.get_all_tasks()

    def add_task(self, text: str, done: bool = False):
        return self.todolist.add_task(text, done)

    def remove_task(self, id: int):
        return self.todolist.remove_task(id)

    def set_flip(self, id: int):
        # flip the state rather than always marking done; delegate to
        # the new toggle implementation in the model.
        return self.todolist.toggle_task(id)

    # ``set_undone`` is no longer used in the GUI, but we keep it for
    # backwards compatibility with any external callers that relied on
    # it.  New code should use ``set_flip`` instead.
    def set_undone(self, id: int):
        return self.todolist.set_undone(id)

    def check_valid(self, task_id):
        return task_id in [t.id for t in self.todolist.get_all_tasks()]

    def sweep(self):
        for t in self.todolist.get_all_tasks():
            if t.done:
                self.todolist.remove_task(t.id)
