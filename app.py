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
    "accent": "#D4AF37",
    "counter_fg": "#555555",
    "toggle_bg": "#DDDDDD",
    "toggle_fg": "#000000",
    "toggle_text": "🌙 Dark Mode"
}


def make_button(parent, text, color, text_color, command, width=120):
    # using canvas as fake button - only way to force colour on macOS
    canvas = tk.Canvas(
        parent,
        width=width,
        height=36,
        bg=color,
        highlightthickness=0,
        cursor="hand2"
    )
    # tag the text so we can update it on hover
    text_id = canvas.create_text(
        width // 2,
        18,
        text=text,
        fill=text_color,
        font=("Arial", 12, "bold"),
        tags="btn_text"
    )

    # hover and click effects
    def on_enter(e):
        canvas.configure(bg=darken(color))

    def on_leave(e):
        canvas.configure(bg=color)

    def on_click(e):
        command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)
    # also bind clicks on the text itself
    canvas.tag_bind("btn_text", "<Button-1>", on_click)

    return canvas


def darken(hex_color):
    # darken a hex color by 20% for hover effect
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = max(0, int(r * 0.8))
    g = max(0, int(g * 0.8))
    b = max(0, int(b * 0.8))
    return f"#{r:02x}{g:02x}{b:02x}"


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To Do App")
        self.root.geometry("480x720")

        # start in dark mode
        self.is_dark = True
        self.theme = DARK

        self.build_ui()
        self.load_tasks()

    def build_ui(self):
        t = self.theme

        self.root.configure(bg=t["bg"])

        # clear existing widgets when rebuilding
        for widget in self.root.winfo_children():
            widget.destroy()

        # toggle button top right using canvas
        toggle_canvas = make_button(
            self.root,
            text=t["toggle_text"],
            color=t["toggle_bg"],
            text_color=t["toggle_fg"],
            command=self.toggle_theme,
            width=130
        )
        toggle_canvas.pack(anchor="ne", padx=15, pady=10)

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
            highlightthickness=0,
            justify="center"
        )
        self.task_entry.pack(pady=10, padx=30, fill=tk.X)

        # enter key shortcut
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

        # buttons using canvas for macOS colour fix
        btn_frame = tk.Frame(self.root, bg=t["bg"])
        btn_frame.pack(pady=15)

        make_button(
            btn_frame,
            text="ADD TASK",
            color="#EEEEEE",
            text_color="#000000",
            command=self.add_task,
            width=120
        ).pack(side=tk.LEFT, padx=8)

        # delete always red - canvas forces colour on macOS
        make_button(
            btn_frame,
            text="DELETE",
            color="#E74C3C",
            text_color="#FFFFFF",
            command=self.delete_task,
            width=120
        ).pack(side=tk.LEFT, padx=8)

        make_button(
            btn_frame,
            text="✓ DONE",
            color="#D4AF37",
            text_color="#000000",
            command=self.mark_complete,
            width=120
        ).pack(side=tk.LEFT, padx=8)

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

        # task counter
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
        self.is_dark = not self.is_dark
        self.theme = DARK if self.is_dark else LIGHT
        current_tasks = list(self.tasks_list.get(0, tk.END))
        self.build_ui()
        for task in current_tasks:
            self.tasks_list.insert(tk.END, task)
        self.update_counter()

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks_list.insert(tk.END, f"• {task}")
            index = self.tasks_list.size() - 1
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