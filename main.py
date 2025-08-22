import tkinter as tk
from tkinter import messagebox
import datetime
import os

root = tk.Tk()
root.title("TO-DO LIST MANAGER")
root.geometry("400x650")
root.configure(bg="white")


tasks = []


def update_listbox():
    lb_tasks.delete(0, "end")
    for i, task in enumerate(tasks, start=1):
        status = "[X]" if task["done"] else "[ ]"
        due = f" (Due: {task['due']})" if task["due"] else ""
        priority = f" (Priority: {task['priority']})" if task["priority"] else ""
        lb_tasks.insert("end", f"{i}. {status} {task['desc']}{priority}{due}")

def add_task():
    desc = txt_input.get().strip()
    if desc:
        tasks.append({"desc": desc, "done": False, "priority": None, "due": None})
        update_listbox()
        lbl_display.config(text=f"Task added: {desc}", fg="green")
        txt_input.delete(0, "end")
    else:
        lbl_display.config(text="Please enter a task description!", fg="red")

def complete_task():
    try:
        index = int(txt_input.get()) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            update_listbox()
            lbl_display.config(text=f"Task marked complete: {tasks[index]['desc']}", fg="blue")
            txt_input.delete(0, "end")
        else:
            lbl_display.config(text="Invalid task number!", fg="red")
    except:
        lbl_display.config(text="Enter a valid task number!", fg="red")

def remove_task():
    try:
        index = int(txt_input.get()) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            update_listbox()
            lbl_display.config(text=f"Task removed: {removed['desc']}", fg="red")
            txt_input.delete(0, "end")
        else:
            lbl_display.config(text="Invalid task number!", fg="red")
    except:
        lbl_display.config(text="Enter a valid task number!", fg="red")

def view_sorted():
    # Sort by due date if set, else keep original order
    tasks.sort(key=lambda x: x["due"] if x["due"] else "9999-12-31")
    update_listbox()
    lbl_display.config(text="Tasks sorted by due date.", fg="purple")

def save_list():
    with open("tasks.txt", "w") as f:
        for task in tasks:
            status = "[X]" if task["done"] else "[ ]"
            due = f" (Due: {task['due']})" if task["due"] else ""
            priority = f" (Priority: {task['priority']})" if task["priority"] else ""
            f.write(f"{status} {task['desc']}{priority}{due}\n")
    lbl_display.config(text="Task list saved to tasks.txt", fg="brown")

def add_priority():
    try:
        index = int(txt_input.get().split(",")[0]) - 1
        priority_value = txt_input.get().split(",")[1].strip()
        if 0 <= index < len(tasks):
            tasks[index]["priority"] = priority_value
            update_listbox()
            lbl_display.config(text=f"Priority set: {priority_value}", fg="orange")
            txt_input.delete(0, "end")
        else:
            lbl_display.config(text="Invalid task number!", fg="red")
    except:
        lbl_display.config(text="Format: task_number, priority_text", fg="red")

def add_due_date():
    try:
        index = int(txt_input.get().split(",")[0]) - 1
        due_date = txt_input.get().split(",")[1].strip()  # Expect YYYY-MM-DD
        datetime.datetime.strptime(due_date, "%Y-%m-%d")  # validate date
        if 0 <= index < len(tasks):
            tasks[index]["due"] = due_date
            update_listbox()
            lbl_display.config(text=f"Due date set: {due_date}", fg="darkgreen")
            txt_input.delete(0, "end")
        else:
            lbl_display.config(text="Invalid task number!", fg="red")
    except:
        lbl_display.config(text="Format: task_number, YYYY-MM-DD", fg="red")

def exit_app():
    root.destroy()

#gui
lbl_title = tk.Label(root, text="To-Do List Manager", font=("Arial", 16, "bold"), bg="white")
lbl_title.pack(pady=10)

lbl_display = tk.Label(root, text="", font=("Arial", 10), bg="white", fg="red")
lbl_display.pack(pady=5)

txt_input = tk.Entry(root, width=30, font=("Arial", 12))
txt_input.pack(pady=5)

# Buttons
btn_add_task = tk.Button(root, text="1. Add a Task", width=30, bg="white", fg="green", command=add_task)
btn_add_task.pack(pady=5)

btn_complete_task = tk.Button(root, text="2. Complete a Task (Enter task number)", width=30, bg="white", fg="blue", command=complete_task)
btn_complete_task.pack(pady=5)

btn_view_sorted = tk.Button(root, text="3. View Sorted To-Do List", width=30, bg="white", fg="purple", command=view_sorted)
btn_view_sorted.pack(pady=5)

btn_remove_task = tk.Button(root, text="4. Remove a Task (Enter task number)", width=30, bg="white", fg="red", command=remove_task)
btn_remove_task.pack(pady=5)

btn_save_list = tk.Button(root, text="5. Save Task List to File", width=30, bg="white", fg="brown", command=save_list)
btn_save_list.pack(pady=5)

btn_add_priority = tk.Button(root, text="6. Add Priority (task_number,priority)", width=30, bg="white", fg="orange", command=add_priority)
btn_add_priority.pack(pady=5)

btn_add_due_date = tk.Button(root, text="7. Add Due Date (task_number,YYYY-MM-DD)", width=30, bg="white", fg="darkgreen", command=add_due_date)
btn_add_due_date.pack(pady=5)

btn_exit = tk.Button(root, text="8. Exit", width=30, bg="white", fg="black", command=exit_app)
btn_exit.pack(pady=5)

lb_tasks = tk.Listbox(root, width=45, height=15, font=("Arial", 12))
lb_tasks.pack(pady=10)


def load_tasks():
    import os
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Parse line format: [ ] description (Priority: ...) (Due: ...)
                done = "[X]" in line
                desc = line.split(" (Priority:")[0].replace("[X]","").replace("[ ]","").strip()
                priority = None
                due = None
                if "(Priority:" in line:
                    priority = line.split("(Priority:")[1].split(")")[0].strip()
                if "(Due:" in line:
                    due = line.split("(Due:")[1].split(")")[0].strip()
                tasks.append({"desc": desc, "done": done, "priority": priority, "due": due})
        update_listbox()

load_tasks()
root.mainloop()
