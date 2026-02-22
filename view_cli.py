import model
import controller
import shlex


class ViewCLI:
    def __init__(self, todolist: model.ToDoList, controller: controller.Controller):
        self.todolist = todolist
        self.controller = controller
        self.running = False

        self.commands = [
            "help",
            "list",
            "add",
            "remove",
            "done",
            "undone",
            "sweep",
        ]

    def start(self):
        self.running = True

        while self.running:
            cmd, payload = self.get_command()
            self.process_command(cmd, payload)

    def stop(self):
        self.running = False

    def get_command(self):
        full_cmd = input("> ")
        payload = shlex.split(full_cmd)
        return payload[0], payload

    def process_command(self, cmd: str, payload: list):
        if cmd not in self.commands:
            raise Exception("Invalid command")

        choice = self.commands.index(cmd)

        match choice:
            case 0:
                self.show_commands()

            case 1:
                self.list_tasks()

            case 2:
                if len(payload) < 2:
                    print("Nothing to add")

                else:
                    text = str(payload[1])

                    if len(payload) > 2 and payload[2] in ["done", "Done"]:
                        status = True
                    else:
                        status = False

                    self.controller.add_task(text, status)
                    self.list_tasks()

            case 3:
                if len(payload) < 2:
                    print("Need a valid ID to remove")

                else:
                    task_id = int(payload[1])

                    if self.controller.check_valid(task_id):
                        self.controller.remove_task(task_id)

                    else:
                        print("Invalid task")
                    self.list_tasks()

            case 4:
                if len(payload) < 2:
                    print("Need a valid ID")

                else:
                    task_id = int(payload[1])

                    if self.controller.check_valid(task_id):
                        self.controller.set_done(int(task_id))
                    else:
                        print("Invalid task")
                    self.list_tasks()

            case 5:
                if len(payload) < 2:
                    print("Need a valid ID")

                else:
                    task_id = int(payload[1])

                    if self.controller.check_valid(task_id):
                        self.controller.set_undone(task_id)
                    else:
                        print("Invalid task")
                    self.list_tasks()

            case 6:
                self.controller.sweep()
                self.list_tasks()


    def show_commands(self):
        for cmd in self.commands:
            print(cmd)

    def list_tasks(self):
        all_tasks = self.todolist.get_all_tasks()

        for task in all_tasks:
            print(task)


if __name__ == "__main__":
    todolist = model.ToDoList()
    controller = controller.Controller(todolist)
    view = ViewCLI(todolist, controller)
    view.start()

