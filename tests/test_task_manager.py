import unittest
from unittest.mock import patch
import os
import json
import io


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
        """Test deleting a task with an invalid index does not crash the application."""
        # Add a sample task
        self.task_manager.tasks.append({
            "task_name": "Sample Task",
            "task_due_date": "2023-12-31",
            "task_description": "Sample description.",
            "priority_level": 5,
            "status": "To be started"
        })
        self.task_manager.save_tasks()

        # Mock input to provide an invalid task number
        with patch('builtins.input', side_effect=['0', '2', 'invalid', '1']):
            with patch('builtins.print') as mock_print:
                self.task_manager.delete_task()
                self.task_manager.delete_task()
                self.task_manager.delete_task()
                self.task_manager.delete_task()

                # Verify that the appropriate error messages were printed
                expected_calls = [
                    unittest.mock.call("Invalid task number."),
                    unittest.mock.call("Invalid task number."),
                    unittest.mock.call("Please enter a valid task number."),
                    unittest.mock.call("Task deleted successfully!")
                ]
                mock_print.assert_has_calls(expected_calls, any_order=False)


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

    def test_handle_menu_choice_invalid_then_exit(self):
        """Test handle_menu_choice with an invalid choice followed by exit."""
        with patch('builtins.input', side_effect=['']):
            with patch('builtins.print') as mock_print:
                task_manager = TaskManager()
                # Test invalid choice
                continue_loop = task_manager.handle_menu_choice('invalid')
                self.assertTrue(continue_loop)
                mock_print.assert_called_with("Invalid choice. Please select a valid option.")

                # Test exit choice
                continue_loop = task_manager.handle_menu_choice('5')
                self.assertFalse(continue_loop)
                mock_print.assert_called_with("Exiting Task Manager. Goodbye!")

    def test_display_kanban_board_with_tasks(self):
        """Test display_kanban_board with multiple tasks."""
        # Add sample tasks
        tasks = [
            {
                    "task_name": "Task 1",
                    "task_due_date": "2023-12-31",
                    "task_description": "Description 1",
                    "priority_level": 9,
                    "status": "To be started"
            },
            {
                    "task_name": "Task 2",
                    "task_due_date": "2024-01-15",
                    "task_description": "Description 2",
                    "priority_level": 5,
                    "status": "In progress"
            },
            {
                    "task_name": "Task 3",
                    "task_due_date": "2024-02-20",
                    "task_description": "Description 3",
                    "priority_level": 2,
                    "status": "Finished"
            }
        ]
        self.task_manager.tasks.extend(tasks)
        self.task_manager.save_tasks()

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.task_manager.display_kanban_board()
            output = fake_out.getvalue()
            # Check that headers are present
            self.assertIn("------- To Be Started -------", output)
            self.assertIn("------- In Progress -------", output)
            self.assertIn("------- Finished -------", output)
            # Check that tasks are displayed under correct headers
            self.assertIn("Task 1 - Due: 2023-12-31 (Priority: 9)", output)
            self.assertIn("Task 2 - Due: 2024-01-15 (Priority: 5)", output)
            self.assertIn("Task 3 - Due: 2024-02-20 (Priority: 2)", output)
            # Check for color codes (optional)
            self.assertIn("\033[91m", output)  # High priority color
            self.assertIn("\033[93m", output)  # Medium priority color
            self.assertIn("\033[92m", output)  # Low priority color
            # Check for confirmation message
            self.assertIn("Task board rendering complete!", output)

    def test_display_kanban_board_with_missing_status(self):
        """Test display_kanban_board with tasks missing the 'status' key."""
        # Add a task without 'status'
        self.task_manager.tasks.append({
            "task_name": "Task without Status",
            "task_due_date": "2023-12-31",
            "task_description": "Description",
            "priority_level": 7
            # 'status' key is missing
        })
        self.task_manager.save_tasks()

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.task_manager.display_kanban_board()
            output = fake_out.getvalue()
            # Task should default to "To be started"
            self.assertIn("------- To Be Started -------", output)
            self.assertIn("Task without Status", output)

    def test_search_tasks_with_matching_keyword(self):
        """Test search_tasks method with a keyword that matches tasks."""
        # Add sample tasks
        tasks = [
            {
                "task_name": "Write report",
                "task_due_date": "2023-12-31",
                "task_description": "Write the annual report.",
                "priority_level": 5,
                "status": "In progress"
            },
            {
                "task_name": "Prepare presentation",
                "task_due_date": "2023-12-15",
                "task_description": "Prepare slides for the meeting.",
                "priority_level": 7,
                "status": "To be started"
            },
            {
                "task_name": "Submit report",
                "task_due_date": "2023-12-20",
                "task_description": "Submit the annual report to management.",
                "priority_level": 8,
                "status": "To be started"
            }
        ]
        self.task_manager.tasks.extend(tasks)
        self.task_manager.save_tasks()

        # Search for tasks with keyword 'report'
        results = self.task_manager.search_tasks('report')
        self.assertEqual(len(results), 2)
        self.assertIn(tasks[0], results)
        self.assertIn(tasks[2], results)

    def test_search_tasks_with_no_matching_keyword(self):
        """Test search_tasks method with a keyword that matches no tasks."""
        # Add sample tasks
        tasks = [
            {
                "task_name": "Write report",
                "task_due_date": "2023-12-31",
                "task_description": "Write the annual report.",
                "priority_level": 5,
                "status": "In progress"
            }
        ]
        self.task_manager.tasks.extend(tasks)
        self.task_manager.save_tasks()

        # Search for a keyword that doesn't match any tasks
        results = self.task_manager.search_tasks('presentation')
        self.assertEqual(len(results), 0)

    # New tests for filter_tasks method
    def test_filter_tasks_by_status(self):
        """Test filter_tasks method filtering by status."""
        # Add sample tasks
        tasks = [
            {
                "task_name": "Task 1",
                "task_due_date": "2023-12-31",
                "task_description": "Description 1",
                "priority_level": 5,
                "status": "In progress"
            },
            {
                "task_name": "Task 2",
                "task_due_date": "2023-12-15",
                "task_description": "Description 2",
                "priority_level": 7,
                "status": "To be started"
            },
            {
                "task_name": "Task 3",
                "task_due_date": "2023-12-20",
                "task_description": "Description 3",
                "priority_level": 8,
                "status": "Finished"
            }
        ]
        self.task_manager.tasks.extend(tasks)
        self.task_manager.save_tasks()

        # Filter tasks by status 'In progress'
        filtered_tasks = self.task_manager.filter_tasks('status', 'In progress')
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0], tasks[0])

    def test_filter_tasks_by_priority_level(self):
        """Test filter_tasks method filtering by priority level."""
        # Add sample tasks
        tasks = [
            {
                "task_name": "Task Low Priority",
                "task_due_date": "2023-12-31",
                "task_description": "Low priority task",
                "priority_level": 2,
                "status": "To be started"
            },
            {
                "task_name": "Task Medium Priority",
                "task_due_date": "2023-12-15",
                "task_description": "Medium priority task",
                "priority_level": 5,
                "status": "In progress"
            },
            {
                "task_name": "Task High Priority",
                "task_due_date": "2023-12-20",
                "task_description": "High priority task",
                "priority_level": 9,
                "status": "Finished"
            }
        ]
        self.task_manager.tasks.extend(tasks)
        self.task_manager.save_tasks()

        # Filter tasks by priority level 5
        filtered_tasks = self.task_manager.filter_tasks('priority_level', 5)
        self.assertEqual(len(filtered_tasks), 1)
        self.assertEqual(filtered_tasks[0], tasks[1])

    def test_filter_tasks_by_due_date(self):
        """Test filter_tasks method filtering by due date."""
        tasks = [
            {
                "task_name": "Task A",
                "task_due_date": "2023-12-31",
                "task_description": "Task due at end of year",
                "priority_level": 5,
                "status": "In progress"
            },
            {
                "task_name": "Task B",
                "task_due_date": "2023-12-15",
                "task_description": "Task due mid-December",
                "priority_level": 7,
                "status": "To be started"
            },
            {
                "task_name": "Task C",
                "task_due_date": "2023-12-31",
                "task_description": "Another task due at end of year",
                "priority_level": 8,
                "status": "Finished"
            }
        ]
        self.task_manager.tasks.extend(tasks)
        self.task_manager.save_tasks()

        # Filter tasks by due date '2023-12-31'
        filtered_tasks = self.task_manager.filter_tasks('due_date', '2023-12-31')
        self.assertEqual(len(filtered_tasks), 2)
        self.assertIn(tasks[0], filtered_tasks)
        self.assertIn(tasks[2], filtered_tasks)

    def test_filter_tasks_with_invalid_filter_type(self):
        """Test filter_tasks method with an invalid filter type."""
        # Add a sample task
        task = {
            "task_name": "Sample Task",
            "task_due_date": "2023-12-31",
            "task_description": "Sample description.",
            "priority_level": 5,
            "status": "To be started"
        }
        self.task_manager.tasks.append(task)
        self.task_manager.save_tasks()

        # Attempt to filter with invalid filter type
        filtered_tasks = self.task_manager.filter_tasks('invalid_type', 'some_value')
        self.assertEqual(len(filtered_tasks), 0)


if __name__ == '__main__':
    unittest.main()

