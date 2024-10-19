import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import os

# Define constants for priority levels
PRIORITY_LOW = 1
PRIORITY_MEDIUM = 2
PRIORITY_HIGH = 3
PRIORITY_MAP = {"Low": PRIORITY_LOW, "Medium": PRIORITY_MEDIUM, "High": PRIORITY_HIGH}
PRIORITY_COLOR = ["green", "orange", "red"]

# Defining the Task class
class Task:
    def __init__(self, name, priority, completed=False, tags=""):
        self.name = name
        self.priority = priority
        self.completed = completed
        self.tags = tags

    def __lt__(self, other):
        return self.priority > other.priority
    
# Function to store data to csv file
def save_tasks_to_csv(tasks, csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Priority", "Completed", "Tags"])
        for task in tasks:
            writer.writerow([task.name, task.priority, task.completed, task.tags])

# Function to import data from csv file
def load_tasks_from_csv(csv_file):
    tasks = []
    if os.path.exists(csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                name, priority, completed, tags = row
                task = Task(name, int(priority), completed == 'True', tags)
                tasks.append(task)
    return tasks

# Function to add tags to a Task
def add_tag_to_task(app):
    if app.selected_task:
        new_tag = simpledialog.askstring("Add Tag", "Enter tag for the selected task:")
        if new_tag:
            app.selected_task.tags = new_tag
            app.display_tasks()
            save_tasks_to_csv(app.tasks, app.csv_file)

# Defining the app class
class GridApp:
    def __init__(self, root, width, height):
        # Setting its appearance
        self.root = root
        self.root.title("SimpleTask")
        self.root.iconbitmap('SimpleTask.ico')
        self.root.geometry(f"{width}x{height}")

        self.font = ("Segoe UI Light", 13)

        self.priorities = ["Low", "Medium", "High"]
        self.csv_file = "tasks.csv"

        # Create a frame to contain the grid
        self.frame = tk.Frame(root, padx=40, pady=40)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.tasks = []

        # Create the header
        self.header = tk.Label(self.frame, text="Welcome to SimpleTask!", font=("Segoe UI", 20))
        self.header.grid(row=0, column=0, columnspan=4, padx=10, pady=(5, 20), sticky="nsew")

        # Create the task input widgets
        self.task_entry = tk.Entry(self.frame, font=self.font)
        self.task_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        # Priority dropdown menu
        self.priority_var = tk.StringVar(value="Priority")
        self.priority_menu = ttk.OptionMenu(self.frame, self.priority_var, "Priority", *self.priorities)
        self.priority_menu.config(width=10, style='my.TMenubutton')
        self.priority_menu.grid(row=1, column=2, padx=(10, 10), pady=10, sticky="nsew")

        # Create the add task button
        self.add_task_button = tk.Button(self.frame, text="Add Task", command=self.add_task, width=12, font=self.font, bg="#666666", fg="white", takefocus=0)
        self.add_task_button.grid(row=1, column=3, padx=(10, 20), pady=10, sticky="nsew")

        # Create a frame to display tasks
        self.task_display_frame = tk.Frame(self.frame)
        self.task_display_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Configure grid 
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=0)

        # Ensure window expands to accommodate the frame
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Create the context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.change_priority_menu = tk.Menu(self.context_menu, tearoff=0)
        self.create_context_menu()

        self.selected_task = None

        # Load tasks from CSV file
        self.tasks = load_tasks_from_csv(self.csv_file)
        self.display_tasks()

    #Create the right-click context menu
    def create_context_menu(self):
        self.context_menu.add_cascade(label="Change Priority", menu=self.change_priority_menu)
        self.change_priority_menu.add_command(label="Low", command=lambda: self.change_priority("Low"))
        self.change_priority_menu.add_command(label="Medium", command=lambda: self.change_priority("Medium"))
        self.change_priority_menu.add_command(label="High", command=lambda: self.change_priority("High"))
        self.context_menu.add_command(label="Delete Task", command=self.delete_task)
        self.context_menu.add_command(label="Add Tag", command=lambda: add_tag_to_task(self))

    #Adds a task to the list and saves it intto the CSV file
    def add_task(self):
        task_name = self.task_entry.get()
        task_priority = self.priority_var.get()
        if task_name and task_priority in self.priorities:
            priority_value = PRIORITY_MAP[task_priority]
            task = Task(task_name, priority_value)
            self.tasks.append(task)
            self.display_tasks()
            self.task_entry.delete(0, tk.END)
            self.priority_var.set("Priority")
            save_tasks_to_csv(self.tasks, self.csv_file)
        else:
            messagebox.showwarning("Input Error", "Please enter a task and select a valid priority.")
    
    #Display tasks in the task display frame
    def display_tasks(self):
        for widget in self.task_display_frame.winfo_children():
            widget.destroy()

        self.tasks.sort()

        for i, task in enumerate(self.tasks):
            self.create_task_row(i, task)
    #Create a row in the task display frame for a given task
    def create_task_row(self, index, task):
        # Color that indicates the priority of the task
        priority_label = tk.Label(self.task_display_frame, text="⚫  ", fg=PRIORITY_COLOR[task.priority-1], font=("Segoe UI Light", 9))

        # Mark task as completed
        if task.completed:
            label_style = {"font": ("Segoe UI Light", 15, "overstrike"), "fg": "grey"}
        else:
            label_style = {"font": ("Segoe UI Light", 15)}
        
        label = tk.Label(self.task_display_frame, text=f"{task.name}   [ {task.tags} ]", borderwidth=0, relief="solid", **label_style)
        completed_var = tk.BooleanVar(value=task.completed)
        checkbox = ttk.Checkbutton(self.task_display_frame, variable=completed_var, command=lambda task=task, var=completed_var: self.update_task_completion(task, var), style='TCheckbutton', takefocus=0)

        priority_label.grid(row=index, column=0, padx=0, pady=(10, 5), sticky="w")
        label.grid(row=index, column=1, padx=0, pady=5, sticky="w")
        checkbox.grid(row=index, column=2, padx=0, pady=(10, 5), sticky="e")

        self.task_display_frame.grid_columnconfigure(0, weight=1)
        self.task_display_frame.grid_columnconfigure(2, weight=18)

        label.bind("<Button-3>", lambda event, task=task: self.show_context_menu(event, task))
    
    # Update the completion status of a task
    def update_task_completion(self, task, var):
        task.completed = var.get()
        self.display_tasks()  # Refresh task display to reflect changes
        save_tasks_to_csv(self.tasks, self.csv_file)
    
    # Show the right-click context menu
    def show_context_menu(self, event, task):
        self.selected_task = task
        self.context_menu.post(event.x_root, event.y_root)
    
    # Change the priority of the selected task
    def change_priority(self, new_priority):
        if self.selected_task:
            self.selected_task.priority = PRIORITY_MAP[new_priority]
            self.display_tasks()
            save_tasks_to_csv(self.tasks, self.csv_file)
    
    # Deletes the selected task
    def delete_task(self):
        if self.selected_task:
            self.tasks.remove(self.selected_task)
            self.selected_task = None
            self.display_tasks()
            save_tasks_to_csv(self.tasks, self.csv_file)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('my.TMenubutton', background='#666666', foreground='white', font=("Segoe UI Light", 13))
    app = GridApp(root, 800, 600)
    root.mainloop()
