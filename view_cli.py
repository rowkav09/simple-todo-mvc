from djn import todolist, controller
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk


class ViewGUI:
    def __init__(self, todo, controller_obj: controller.Controller):
        self.todolist = todo
        self.controller = controller_obj
        
        self.root = tk.Tk()
        self.root.title("To-Do List")
        self.root.geometry("500x600")
        self.root.configure(background="sky blue")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="My To-Do List",highlightcolor='black', font=("Arial", 16, "bold"),background="sky blue")
        title_label.pack(pady=10)
        
        # Task listbox with scrollbar
        frame = tk.Frame(self.root)
        frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 10))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Task", command=self.add_task_dialog).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Flip State", command=self.flip).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Remove", command=self.remove_task).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Sweep", command=self.sweep_tasks).grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        tk.Button(button_frame, text="Quit", command=self.quit).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        self.refresh_tasks()
    
    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        all_tasks = self.todolist.get_all_tasks()
        for t in all_tasks:
            status = "(done)" if t.done else ""
            self.task_listbox.insert(tk.END, f"{t.id:4} - {t.text} {status}")
    
    def add_task_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Task")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="Task text:").pack(pady=5)
        text_entry = tk.Entry(dialog, width=30)
        text_entry.pack(pady=5)
        
        var_done = tk.BooleanVar()
        tk.Checkbutton(dialog, text="Mark as done", variable=var_done).pack(pady=5)

        def save_task():
            text = text_entry.get()
            if text.strip():
                self.controller.add_task(text, var_done.get())
                self.refresh_tasks()
                dialog.destroy()
            else:
                messagebox.showwarning("Warning", "Please enter task text")

        dialog.bind('<Return>', save_task())

        tk.Button(dialog, text="Add", command=save_task,).pack(pady=10)


    
    def get_selected_task_id(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task")
            return None
        
        task_text = self.task_listbox.get(selection[0])
        task_id = int(task_text.split("-")[0].strip())
        return task_id
    
    def flip(self):
        task_id = self.get_selected_task_id()
        if task_id and self.controller.check_valid(task_id):
            self.controller.set_flip(task_id)
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Invalid task")
    
    
    def remove_task(self):
        task_id = self.get_selected_task_id()
        if task_id and self.controller.check_valid(task_id):
            self.controller.remove_task(task_id)
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Invalid task")
    
    def sweep_tasks(self):
        self.controller.sweep()
        self.refresh_tasks()
    
    def quit(self):
        self.root.quit()
    
    def start(self):
        self.root.mainloop()


if __name__ == "__main__":
    thetodolist = todolist.ToDoList()
    thecontroller = controller.Controller(thetodolist)
    view = ViewGUI(thetodolist, thecontroller)
    view.start()

