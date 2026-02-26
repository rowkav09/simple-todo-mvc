from dataclasses import dataclass


@dataclass
class Task:
    id: int
    text: str
    done: bool

    def get_status(self):
        return self.done

    def set_status(self, status):
        self.done = status


class ToDoList:
    def __init__(self):
        self.tasks: list[Task] = []
        self.task_id = 0

    def add_task(self, text: str, status: bool) -> Task:
        self.task_id += 1
        new_task = Task(id=self.task_id, text=text, done=status)
        self.tasks.append(new_task)
        return new_task

    def get_task(self, id: int) -> Task | None:
        return next((t for t in self.tasks if t.id == id), None)

    def set_done(self, id: int) -> Task | None:
        task = self.get_task(id)
        task.done = True
        return task

    def set_undone(self, id: int) -> Task | None:
        task = self.get_task(id)
        task.done = False
        return task

    def toggle_task(self, id: int) -> Task | None:
        """Flip the done state of the task with the given id.

        This replaces the previous pattern of having separate
        ``set_done``/``set_undone`` methods.  Clients can now simply
        call ``toggle_task`` (or ``set_flip`` on the controller) to
        invert the current state.
        """
        task = self.get_task(id)
        if task is not None:
            task.done = not task.done
        return task

    def remove_task(self, id: int) -> Task | None:
        task = self.get_task(id)
        self.tasks.remove(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        return self.tasks
