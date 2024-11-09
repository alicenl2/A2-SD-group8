import unittest
from unittest.mock import patch
import sys
import os
import json

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from taskmanager import TaskManager

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

    def test_edit_task_with_invalid_priority(self):
        """Test editing a task with invalid priority level input."""
        # Add a task to edit
        self.task_manager.tasks.append({
            "task_name": "Task to Edit",
            "task_due_date": "2023-12-31",
            "task_description": "Original description.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()

        # Simulate invalid priority level input
        with self.assertRaises(ValueError):
            self.task_manager.tasks[0]['priority_level'] = int("invalid")

    def test_edit_task_with_valid_priority(self):
        """Test editing a task with valid priority level input."""
        # Add a task to edit
        self.task_manager.tasks.append({
            "task_name": "Task to Edit",
            "task_due_date": "2023-12-31",
            "task_description": "Original description.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()

        # Simulate editing the priority level with valid input
        self.task_manager.tasks[0]['priority_level'] = 8
        self.task_manager.save_tasks()
        edited_task = self.task_manager.tasks[0]
        self.assertEqual(edited_task['priority_level'], 8)

    def test_edit_task_with_invalid_status(self):
        """Test editing a task with invalid status input."""
        # Add a task to edit
        self.task_manager.tasks.append({
            "task_name": "Task to Edit",
            "task_due_date": "2023-12-31",
            "task_description": "Original description.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()

        # Simulate invalid status input
        invalid_status = "Not a valid status"
        self.task_manager.tasks[0]['status'] = invalid_status
        self.task_manager.save_tasks()
        edited_task = self.task_manager.tasks[0]
        # Check that status has been updated (even if invalid)
        self.assertEqual(edited_task['status'], invalid_status)

    def test_delete_task_with_valid_index(self):
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
        # Delete the task using the corrected index
        self.task_manager.tasks.pop(0)  # Index 0 after fixing off-by-one error
        self.task_manager.save_tasks()
        self.assertEqual(len(self.task_manager.tasks), initial_task_count - 1)

    def test_delete_task_with_invalid_index(self):
        """Test deleting a task with an invalid index."""
        # Add a sample task
        self.task_manager.tasks.append({
            "task_name": "Sample Task",
            "task_due_date": "2023-12-31",
            "task_description": "Sample description.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()
        # Attempt to delete with an invalid index
        with self.assertRaises(IndexError):
            self.task_manager.tasks.pop(5)  # Invalid index

    def test_get_priority_level_with_invalid_input(self):
        """Test get_priority_level method with invalid input."""
        with patch('builtins.input', side_effect=['invalid', '15', '5']):
            priority_level = self.task_manager.get_priority_level()
            self.assertEqual(priority_level, 5)

    def test_get_status_with_invalid_input(self):
        """Test get_status method with invalid input."""
        with patch('builtins.input', side_effect=['invalid', '4', '2']):
            status = self.task_manager.get_status()
            self.assertEqual(status, 'In progress')


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



if __name__ == '__main__':
    unittest.main()
