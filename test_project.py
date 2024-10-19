import pytest
import os
import csv
from tkinter import Tk
from project import Task, save_tasks_to_csv, load_tasks_from_csv, add_tag_to_task, GridApp

@pytest.fixture
def sample_tasks():
    """Fixture to provide sample tasks."""
    return [
        Task("Task 1", 3, False, "home"),
        Task("Task 2", 2, True, "work"),
        Task("Task 3", 1, False, "school")
    ]

@pytest.fixture
def temp_csv_file(tmp_path):
    """Fixture to provide a temporary CSV file path."""
    return tmp_path / "tasks.csv"

def test_save_tasks_to_csv(sample_tasks, temp_csv_file):
    """Test saving tasks to a CSV file."""
    save_tasks_to_csv(sample_tasks, temp_csv_file)

    with open(temp_csv_file, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Assert that the header is correct
    assert rows[0] == ["Name", "Priority", "Completed", "Tags"]
    
    # Assert that the tasks are correctly saved
    assert rows[1] == ["Task 1", "3", "False", "home"]
    assert rows[2] == ["Task 2", "2", "True", "work"]
    assert rows[3] == ["Task 3", "1", "False", "school"]

def test_load_tasks_from_csv(sample_tasks, temp_csv_file):
    """Test loading tasks from a CSV file."""
    save_tasks_to_csv(sample_tasks, temp_csv_file)
    loaded_tasks = load_tasks_from_csv(temp_csv_file)

    # Assert that the loaded tasks match the original tasks
    assert len(loaded_tasks) == len(sample_tasks)
    for original, loaded in zip(sample_tasks, loaded_tasks):
        assert original.name == loaded.name
        assert original.priority == loaded.priority
        assert original.completed == loaded.completed
        assert original.tags == loaded.tags

def test_add_tag_to_task(sample_tasks):
    """Test adding a tag to a task."""
    root = Tk()
    app = GridApp(root, 5, 4, 800, 600)
    app.tasks = sample_tasks
    app.selected_task = sample_tasks[0]
    
    add_tag_to_task(app)

    # Assuming a new tag "new_tag" was added in the dialog
    assert app.selected_task.tags == "new_tag"

    # Clean up the Tkinter instance
    root.destroy()

if __name__ == "__main__":
    pytest.main()
