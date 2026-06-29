import tkinter as tk

root = tk.TK()
root.title("To Do App")
root.geometry("450x650")
root.configure(bg="#000000")

tk.label(root, text="Tasks", font=("Arial", 22, "bold"),
         bg="#000000", fg="#D4AF37").pack(pady=25)

task_entry = tk.Entry(root, font=("Arial", 18), bg="#EEEEEE",
                        fg="#000000", borderwidth=0, justify="center")
task_Entry.pack(pady=10, padx=30, fill=tk.X)


# listbox to show all tasks
tasks_list = tk.Listbox(root, font=("Arial", 14), bg="#111111",
                        fg="#FFFFFF", selecrbackground= "#D4AF37",
                        selectforeground="#000000", borderwidth=0)
tasks_list.pack(fill=tk.BOTH, expamd=True, padx=30, pady=20)

root.mainloop()
