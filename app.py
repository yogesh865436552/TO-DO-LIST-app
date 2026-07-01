import tkinter as tk
from tkinter import messagebox
from task_storage import load_tasks as load_tasks_from_file
from task_storage import save_tasks as save_tasks_to_file

# colour themes
DARK = {
    "bg": "#000000",
    "fg": "#FFFFFF",
    "entry_bg": "#EEEEEE",
    "entry_fg": "#000000",
    "list_bg": "#111111",
    "list_fg": "#FFFFFF",
    "btn_add_bg": "#EEEEEE",
    "btn_add_fg": "#000000",
    "btn_del_bg": "#E74C3C",
    "btn_del_fg": "#FFFFFF",
    "accent": "#D4AF37",
    "counter_fg": "#888888",
    "toggle_bg": "#222222",
    "toggle_fg": "#FFFFFF",
    "toggle_text": "☀️ Light Mode"
}

LIGHT = {
    "bg": "#F5F5F5",
    "fg": "#000000",
    "entry_bg": "#FFFFFF",
    "entry_fg": "#000000",
    "list_bg": "#FFFFFF",
    "list_fg": "#000000",
    "btn_add_bg": "#000000",
    "btn_add_fg": "#FFFFFF",
    "btn_del_bg": "#E74C3C",
    "btn_del_fg": "#FFFFFF",
    "accent": "#D4AF37",
    "counter_fg": "#555555",
    "toggle_bg": "#DDDDDD",
    "toggle_fg": "#000000",
    "toggle_text": "🌙 Dark Mode"
}


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do App")
        self.root.geometry("450x700")

        # start in dark mode
        self.is_dark = True
        self.theme = DARK

        self.build_ui()
        self.load_tasks()

    def build_ui(self):
        t = self.theme

        self.root.configure(bg=t["bg"])

        # clear existing widgets when rebuilding for theme switch
        for widget in self.root.winfo_children():
            widget.destroy()

        # toggle button top right
        self.toggle_btn = tk.Button(
            self.root,
            text=t["toggle_text"],
            command=self.toggle_theme,
            font=("Arial", 10),
            bg=t["toggle_bg"],
            fg=t["toggle_fg"],
            borderwidth=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.toggle_btn.pack(anchor="ne", padx=15, pady=10)

        # title
        tk.Label(
            self.root,
            text="Tasks",
            font=("Arial", 22, "bold"),
            bg=t["bg"],
            fg=t["accent"]
        ).pack(pady=10)

        # input field
        self.task_entry = tk.Entry(
            self.root,
            font=("Arial", 18),
            bg=t["entry_bg"],
            fg=t["entry_fg"],
            borderwidth=0,
            justify="center"
        )
        self.task_entry.pack(pady=10, padx=30, fill=tk.X)

        # enter key shortcut to add task
        self.task_entry.bind('<Return>', lambda e: self.add_task())

        # priority selector
        priority_frame = tk.Frame(self.root, bg=t["bg"])
        priority_frame.pack(pady=5)

        tk.Label(
            priority_frame,
            text="Priority:",
            font=("Arial", 11),
            bg=t["bg"],
            fg=t["counter_fg"]
        ).pack(side=tk.LEFT, padx=5)

        self.priority = tk.StringVar(value="normal")

        for label, color, value in [
            ("High", "#E74C3C", "high"),
            ("Medium", "#F39C12", "medium"),
            ("Low", "#27AE60", "low")
        ]:
            tk.Radiobutton(
                priority_frame,
                text=label,
                variable=self.priority,
                value=value,
                bg=t["bg"],
                fg=color,
                selectcolor=t["bg"],
                activebackground=t["bg"],
                font=("Arial", 11)
            ).pack(side=tk.LEFT, padx=5)

        # buttons
        btn_frame = tk.Frame(self.root, bg=t["bg"])
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="ADD TASK",
            command=self.add_task,
            font=("Arial", 12, "bold"),
            bg=t["btn_add_bg"],
            fg=t["btn_add_fg"],
            width=12,
            height=1,
            cursor="hand2",
            borderwidth=0
        ).pack(side=tk.LEFT, padx=10)

        # delete button always red so it's visible in both dark and light
        tk.Button(
            btn_frame,
            text="DELETE",
            command=self.delete_task,
            font=("Arial", 12, "bold"),
            bg=t["btn_del_bg"],
            fg=t["btn_del_fg"],
            width=12,
            height=1,
            cursor="hand2",
            borderwidth=0
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="✓ DONE",
            command=self.mark_complete,
            font=("Arial", 12, "bold"),
            bg=t["accent"],
            fg="#000000",
            width=12,
            height=1,
            cursor="hand2",
            borderwidth=0
        ).pack(side=tk.LEFT, padx=10)

        # task listbox
        self.tasks_list = tk.Listbox(
            self.root,
            font=("Arial", 14),
            bg=t["list_bg"],
            fg=t["list_fg"],
            selectbackground=t["accent"],
            selectforeground="#000000",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#333333"
        )
        self.tasks_list.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # task counter at bottom
        self.counter_label = tk.Label(
            self.root,
            text="0 tasks",
            font=("Arial", 11),
            bg=t["bg"],
            fg=t["counter_fg"]
        )
        self.counter_label.pack(pady=5)

        # footer
        tk.Label(
            self.root,
            text="Made by Yogesh Madhukumar 🚀",
            font=("Arial", 10),
            bg=t["bg"],
            fg=t["counter_fg"]
        ).pack(pady=5)

    def toggle_theme(self):
        # switch between dark and light
        self.is_dark = not self.is_dark
        self.theme = DARK if self.is_dark else LIGHT

        # save current tasks before rebuilding
        current_tasks = list(self.tasks_list.get(0, tk.END))

        # rebuild UI with new theme
        self.build_ui()

        # restore tasks after rebuild
        for task in current_tasks:
            self.tasks_list.insert(tk.END, task)
        self.update_counter()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks_list.insert(tk.END, f"• {task}")
            index = self.tasks_list.size() - 1
            # colour code by priority
            colors = {
                "high": "#E74C3C",
                "medium": "#F39C12",
                "low": "#27AE60"
            }
            self.tasks_list.itemconfig(
                index,
                fg=colors.get(self.priority.get(), self.theme["list_fg"])
            )
            self.task_entry.delete(0, tk.END)
            self.save_tasks()
            self.update_counter()
        else:
            messagebox.showwarning("Alert", "Entry cannot be empty.")

    def delete_task(self):
        try:
            index = self.tasks_list.curselection()[0]
            self.tasks_list.delete(index)
            self.save_tasks()
            self.update_counter()
        except IndexError:
            messagebox.showwarning("Alert", "Please select a task to delete.")

    def mark_complete(self):
        try:
            index = self.tasks_list.curselection()[0]
            task = self.tasks_list.get(index)
            # strike through effect using grey color
            if not task.startswith("✓"):
                self.tasks_list.delete(index)
                self.tasks_list.insert(index, f"✓ {task}")
                self.tasks_list.itemconfig(index, fg="#555555")
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Alert", "Please select a task to mark done.")

    def update_counter(self):
        count = self.tasks_list.size()
        self.counter_label.config(
            text=f"{count} task{'s' if count != 1 else ''}"
        )

    def save_tasks(self):
        save_tasks_to_file(self.tasks_list.get(0, tk.END))

    def load_tasks(self):
        for task in load_tasks_from_file():
            self.tasks_list.insert(tk.END, task)
        self.update_counter()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()