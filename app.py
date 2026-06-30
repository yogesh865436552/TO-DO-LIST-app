import tkinter as tk
from tkinter import messagebox

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do App")
        self.root.geometry("450x650")
        self.root.configure(bg="#000000")

        tk.Label(root, text="TASKS", font=("Arial", 22, "bold"),
                 bg="#000000", fg="#D4AF37").pack(pady=25)

        self.task_entry = tk.Entry(root, font=("Arial", 18), bg="#EEEEEE",
                                   fg="#000000", borderwidth=0, justify="center")
        self.task_entry.pack(pady=10, padx=30, fill=tk.X)

        btn_frame = tk.Frame(root, bg="#000000")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="ADD TASK", command=self.add_task,
                  font=("Arial", 12, "bold"), bg="#EEEEEE", fg="#000000",
                  width=12).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="DELETE", command=self.delete_task,
                  font=("Arial", 12, "bold"), bg="#000000", fg="#FFFFFF",
                  width=12).pack(side=tk.LEFT, padx=10)

        self.tasks_list = tk.Listbox(root, font=("Arial", 14), bg="#111111",
                                     fg="#FFFFFF", selectbackground="#D4AF37",
                                     selectforeground="#000000", borderwidth=0)
        self.tasks_list.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks_list.insert(tk.END, f"• {task}")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Alert", "Entry cannot be empty.")

    def delete_task(self):
        try:
            index = self.tasks_list.curselection()[0]
            self.tasks_list.delete(index)
        except IndexError:
            messagebox.showwarning("Alert", "Please select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
