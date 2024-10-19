# SimpleTask
#### Video Demo:  <URL HERE>
#### Description:

SimpleTask is a straightforward task management application developed using Python and Tkinter. It allows users to manage daily tasks by adding, prioritizing, completing, and tagging tasks through an intuitive interface.

## Features
**Add Tasks**: Users can add new tasks and assign them a priority.

**Task Priority**: Assign tasks one of three priority levels: Low, Medium, or High. These are visually represented by the colors green, yellow, and red, respectively.

**Complete Tasks:** Mark tasks as completed, which will then appear with a strikethrough and faded color.

**Tag Tasks:** Attach tags to tasks for better categorization and organization.

**Context Menu:** Right-clicking a task opens a menu with options to change its priority, delete it, or add tags.

**Persistent Storage:** Tasks are saved and loaded from a CSV file, ensuring data persistence across sessions.

## How It Works
### Adding a Task
To add a task, enter the task name in the input field, select a priority from the dropdown menu, and click the "Add Task" button. The task is displayed in the task list with its priority color.

### Displaying Tasks
Tasks are displayed in a prioritized order. The task display updates whenever a task is added, edited, or marked as completed, reflecting the current state of the task list.

### Marking Tasks as Completed
Each task has a checkbox. Checking it marks the task as completed, applying a strikethrough and saving the status to the CSV file.

### Changing Task Priority
Right-clicking a task opens a context menu with options to change its priority to Low, Medium, or High. Changing the priority updates the task and resorts the list accordingly.

### Deleting Tasks
The context menu also allows deleting a task. When deleted, the task is removed from the list, and the CSV file is updated.

### Adding Tags to Tasks
Tags can be added via the context menu. Selecting "Add Tag" prompts a dialog box for entering a tag, which is then displayed next to the task name.

## Code Structure and Implementation
### Task Class
The `Task` class defines the structure of a task, including its name, priority, completion status, and tags. By overriding the `__lt__` method, tasks can be sorted based on their priority, with higher-priority tasks appearing first in the list. This sorting functionality is crucial for maintaining an organized task list where users can easily see their most important tasks.

### GridApp Class
The `GridApp` class is the main class that sets up the user interface and handles interactions. It initializes the main window and creates input fields, buttons, and the task display area. The class manages the loading and saving of tasks to and from the CSV file. The interface is designed using Tkinter's grid layout manager to ensure a responsive design that adjusts as the window is resized.

### CSV Functions
Two key functions handle the persistence of task data:
- `save_tasks_to_csv`: This function saves the current list of tasks to a CSV file, ensuring that the data is preserved between sessions. Each task's name, priority, completion status, and tags are written to the file.
- `load_tasks_from_csv`: This function loads tasks from the CSV file when the application starts, populating the task list with previously saved tasks. It reads each row from the CSV file, creates a `Task` object for each one, and adds it to the list.

### Context Menu
The context menu is an essential feature that enhances the user experience by providing quick access to common actions. When a task is right-clicked, the context menu appears, offering options to change the task's priority, delete the task, or add tags. This menu is dynamically generated and linked to the selected task, ensuring that the actions are applied correctly.

### Task Display
Tasks are displayed in a frame using Tkinter's grid layout. Each task is represented by a label showing the task name and tags, and a checkbox indicating completion status. The priority of each task is visually indicated using colored dots next to the task name. When tasks are added, edited, or completed, the display is refreshed to reflect these changes. This dynamic updating ensures that the user always sees the most current state of their task list.

### Summary
SimpleTask is a user-friendly task management application designed to help users organize their daily tasks efficiently. By leveraging Python and Tkinter, it offers a clean and responsive interface with features such as task prioritization, completion tracking, tagging, and persistent storage. The application’s code structure ensures maintainability and extensibility, making it a robust solution for personal task management.

### Enjoy managing your tasks with SimpleTask!