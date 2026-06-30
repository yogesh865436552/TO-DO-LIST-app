import tkinter as tk

root = tk.TK()
root.title("To Do App")
root.geometry("450x650")
root.configure(bg="#000000")

tk.label(root, text="Tasks", font=("Arial", 22, "bold"),
         bg="#000000", fg="#D4AF37").pack(pady=25)

task_entry = tk.Entry(root, font=("Arial", 18), bg="#EEEEEE",
                        fg="#000000", borderwidth=0, justify="center")
task_entry.pack(pady=10, padx=30, fill=tk.X)

# add and delete buttons side by side
btn_frame = tk.Frame(root, bg="#000000")
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="ADD TASK", font=("Arial", 12, "bold"),
          bg="#EEEEEE", fg="#000000", width=12).pack(side=tk.LEFT, padx=10)

tk.Button(btn_frame, text="DELETE", font=("Arial", 12,"bold"),
          bg="#EEEEEE", fg="#FFFFFF", width=12).pack(side=tk.LEFT, padx=10)

tasks_list = tk.Listbox(root, font=("Arial", 14), bg="#111111",
                        fg="#FFFFFF", selecrbackground= "#D4AF37",
                        selectforeground="#000000", borderwidth=0)
tasks_list.pack(fill=tk.BOTH, expamd=True, padx=30, pady=20)

root.mainloop()
