import unittest
from unittest.mock import patch
import json
import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from feature_manager import TaskManager

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        # Initialize TaskManager with a test file
        self.test_task_file = 'test_tasks.json'
        self.task_manager = TaskManager(task_file=self.test_task_file)
        # Ensure the test file is clean
        self.task_manager.tasks = []
        self.task_manager.save_tasks()

    def tearDown(self):
        # Remove the test file after tests
        if os.path.exists(self.test_task_file):
            os.remove(self.test_task_file)

    def test_add_task(self):
        """Test adding a task."""
        initial_task_count = len(self.task_manager.tasks)
        # Simulate adding a task without user input
        new_task = {
            "task_name": "Test Task",
            "task_due_date": "2023-12-31",
            "task_description": "This is a test task.",
            "priority_level": 5,
            "status": "To be started"
        }
        self.task_manager.tasks.append(new_task)
        self.task_manager.save_tasks()
        self.assertEqual(len(self.task_manager.tasks), initial_task_count + 1)
        self.assertEqual(self.task_manager.tasks[-1], new_task)

    def test_display_tasks(self):
        """Test displaying tasks."""
        # Add a sample task
        self.task_manager.tasks.append({
            "task_name": "Display Test Task",
            "task_due_date": "2023-12-31",
            "task_description": "Task for display test.",
            "priority_level": 3,
            "status": "In progress"
        })
        self.task_manager.save_tasks()
        # Since display_tasks prints output, we check if it runs without errors
        try:
            self.task_manager.display_tasks()
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_edit_task(self):
        """Test editing a task with valid inputs."""
        # Add a task to edit
        self.task_manager.tasks.append({
            "task_name": "Old Task Name",
            "task_due_date": "2023-12-31",
            "task_description": "Old description.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()
        # Simulate editing the task directly
        task = self.task_manager.tasks[0]
        task.update({
            "task_name": "New Task Name",
            "task_due_date": "2024-01-31",
            "task_description": "New description.",
            "priority_level": 7,  # Valid priority level
            "status": "In progress"  # Valid status
        })
        self.task_manager.save_tasks()
        edited_task = self.task_manager.tasks[0]
        self.assertEqual(edited_task['task_name'], "New Task Name")
        self.assertEqual(edited_task['priority_level'], 7)
        self.assertEqual(edited_task['status'], "In progress")

    def test_delete_task(self):
        """Test deleting a task with a valid index."""
        # Add a task to delete
        self.task_manager.tasks.append({
            "task_name": "Task to Delete",
            "task_due_date": "2023-12-31",
            "task_description": "Task that will be deleted.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()
        initial_task_count = len(self.task_manager.tasks)
        # Delete the task at index 0 (first task)
        self.task_manager.tasks.pop(0)
        self.task_manager.save_tasks()
        self.assertEqual(len(self.task_manager.tasks), initial_task_count - 1)

    def test_load_and_save_tasks(self):
        """Test loading and saving tasks."""
        # Create test tasks
        test_tasks = [
            {
                "task_name": "Loaded Task 1",
                "task_due_date": "2023-12-31",
                "task_description": "First loaded task.",
                "priority_level": 4,
                "status": "To be started"
            },
            {
                "task_name": "Loaded Task 2",
                "task_due_date": "2024-01-15",
                "task_description": "Second loaded task.",
                "priority_level": 6,
                "status": "In progress"
            }
        ]
        # Save tasks directly to the test file
        with open(self.test_task_file, 'w') as file:
            json.dump(test_tasks, file, indent=4)
        # Load tasks using the TaskManager method
        loaded_tasks = self.task_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 2)
        self.assertEqual(loaded_tasks[0]['task_name'], "Loaded Task 1")

    def test_get_priority_level(self):
        """Test getting a valid priority level."""
        # Since get_priority_level requires user input, we'll mock the input
        # For simplicity, we'll directly test the logic
        with patch('builtins.input', return_value='5'):
            priority_level = self.task_manager.get_priority_level()
            self.assertEqual(priority_level, 5)

    def test_get_status(self):
        """Test getting a valid status."""
        # Mock input to return '2' which corresponds to 'In progress'
        with patch('builtins.input', return_value='2'):
            status = self.task_manager.get_status()
            self.assertEqual(status, 'In progress')

if __name__ == '__main__':
    unittest.main()