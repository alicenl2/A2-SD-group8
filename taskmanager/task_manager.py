import json
import os

def display_kanban_board(tasks):
    """
    Display tasks organized by status in a Kanban board format with color coding based on priority.

    Args:
        tasks (list): A list of task dictionaries.

    Returns:
        str: Confirmation message after displaying the Kanban board.
    """
    # Organize tasks by status
    statuses = {
        "To be started": [],
        "In progress": [],
        "Finished": []
    }

    for task in tasks:
        status = task.get('status', 'To be started')
        statuses.setdefault(status, []).append(task)

    # Define color codes
    color_map = {
        1: '\033[91m',  # Red for high priority
        2: '\033[93m',  # Yellow for medium priority
        3: '\033[92m'   # Green for low priority
    }
    reset_color = '\033[0m'

    # Function to get color based on priority level
    def get_color(priority_level):
        if priority_level >= 8:
            return color_map[1]  # High priority
        elif 4 <= priority_level <= 7:
            return color_map[2]  # Medium priority
        else:
            return color_map[3]  # Low priority

    # Function to display tasks under each status with color coding
    def display_tasks(task_list, header):
        print(f"\n------- {header} -------")
        for task in task_list:
            task_name = task.get('task_name', 'Unnamed Task')
            due_date = task.get('task_due_date', 'No Due Date')
            priority_level = int(task.get('priority_level', 5))
            color = get_color(priority_level)
            print(f"{color}{task_name} - Due: {due_date} (Priority: {priority_level}){reset_color}")

    # Display tasks under each status
    display_tasks(statuses["To be started"], "To Be Started")
    display_tasks(statuses["In progress"], "In Progress")
    display_tasks(statuses["Finished"], "Finished")

    print("\nTask board rendering complete!")

    return "Kanban board displayed successfully with color coding."


class TaskManager:
    """Class to manage tasks."""

    def __init__(self, task_file='list_of_tasks.json'):
        """Initialize the TaskManager with a list of tasks."""
        self.task_file = task_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        if not os.path.exists(self.task_file):
            return []
        try:
            with open(self.task_file, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, TypeError):
            print("Error: Task file is corrupted. Starting with an empty task list.")
            return []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        try:
            with open(self.task_file, 'w') as file:
                json.dump(self.tasks, file, indent=4)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def get_user_input(self):
        """Collect task details from the user."""
        task_name = input("What's the task you need to do? ").strip()
        task_due_date = input("When is it due? ").strip()
        task_description = input("Please enter a description of your task if you want to: ").strip()

        # Get priority level
        priority_level = self.get_priority_level()

        # Get status
        status = self.get_status()

        return {
            "task_name": task_name,
            "task_due_date": task_due_date,
            "task_description": task_description,
            "priority_level": priority_level,
            "status": status
        }

    def get_priority_level(self):
        """Get priority level from the user."""
        while True:
            try:
                priority_level = int(input("On a scale of 1 to 10, what's its priority level? (10 being the most important): "))
                if 1 <= priority_level <= 10:
                    return priority_level
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid integer between 1 and 10.")

    def get_status(self):
        """Get task status from the user."""
        status_options = {
            '1': 'To be started',
            '2': 'In progress',
            '3': 'Finished'
        }
        while True:
            status_choice = input("Please choose the status of the task:\n1. To be started\n2. In progress\n3. Finished\n").strip()
            if status_choice in status_options:
                return status_options[status_choice]
            else:
                print("Please enter a valid option (1, 2, or 3).")

    def add_task(self):
        """Add a new task."""
        task = self.get_user_input()
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully!")

    def display_tasks(self, tasks=None):
        """Display tasks."""
        if tasks is None:
            tasks = self.tasks

        if not tasks:
            print("No tasks available.")
            return

        for index, task in enumerate(tasks, start=1):
            print(f"\nTask {index}:")
            print(f"Name: {task.get('task_name', 'N/A')}")
            print(f"Due Date: {task.get('task_due_date', 'N/A')}")
            print(f"Description: {task.get('task_description', 'N/A')}")
            print(f"Priority Level: {task.get('priority_level', 'N/A')}")
            print(f"Status: {task.get('status', 'N/A')}")

    def edit_task(self):
        """Edit an existing task."""
        if not self.tasks:
            print("No tasks to edit.")
            return

        self.display_tasks()
        try:
            task_number = int(input("Enter the task number you want to edit: "))
            if 1 <= task_number <= len(self.tasks):
                task = self.tasks[task_number - 1]
            else:
                print("Invalid task number.")
                return
        except ValueError:
            print("Please enter a valid task number.")
            return

        print("Enter new values (leave blank to keep current value):")
        task_name = input(f"Task Name [{task['task_name']}]: ").strip() or task['task_name']
        task_due_date = input(f"Due Date [{task['task_due_date']}]: ").strip() or task['task_due_date']
        task_description = input(f"Description [{task['task_description']}]: ").strip() or task['task_description']

        # Validate priority level
        while True:
            priority_level_input = input(f"Priority Level [{task['priority_level']}]: ").strip()
            if priority_level_input == '':
                priority_level = task['priority_level']
                break
            try:
                priority_level = int(priority_level_input)
                if 1 <= priority_level <= 10:
                    break
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid integer between 1 and 10.")

        # Validate status
        status_options = {
            '1': 'To be started',
            '2': 'In progress',
            '3': 'Finished'
        }
        while True:
            status_input = input(f"Status [{task['status']}]: ").strip()
            if status_input == '':
                status = task['status']
                break
            elif status_input in status_options:
                status = status_options[status_input]
                break
            else:
                print("Please enter a valid option (1, 2, or 3).")

        # Update the task
        task.update({
            "task_name": task_name,
            "task_due_date": task_due_date,
            "task_description": task_description,
            "priority_level": priority_level,
            "status": status
        })
        self.save_tasks()
        print("Task updated successfully!")

    def delete_task(self):
        """Delete an existing task."""
        if not self.tasks:
            print("No tasks to delete.")
            return

        self.display_tasks()
        try:
            task_number = int(input("Enter the task number you want to delete: "))
            if 1 <= task_number <= len(self.tasks):
                self.tasks.pop(task_number - 1)
                self.save_tasks()
                print("Task deleted successfully!")
            else:
                print("Invalid task number.")
        except ValueError:
            print("Please enter a valid task number.")

    def view_statistics(self):
        """Display statistics about tasks."""
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task['status'] == 'Finished'])
        print(f"Total tasks: {total_tasks}")
        print(f"Completed tasks: {completed_tasks}")

    def display_kanban_board(self):
        """Display tasks in a Kanban board format."""
        display_kanban_board(self.tasks)

    def search_tasks(self, keyword):
        """Search tasks by keyword."""
        results = [
            task for task in self.tasks
            if keyword.lower() in task['task_name'].lower() or
               keyword.lower() in task['task_description'].lower()
        ]
        return results

    def filter_tasks(self, filter_type, value):
        """Filter tasks based on filter_type and value."""
        if filter_type == 'status':
            return [task for task in self.tasks if task['status'] == value]
        elif filter_type == 'priority_level':
            return [task for task in self.tasks if task['priority_level'] == value]
        elif filter_type == 'due_date':
            return [task for task in self.tasks if task['task_due_date'] == value]
        else:
            return []

    def search_tasks_menu(self):
        """Menu for searching tasks."""
        keyword = input("Enter keyword to search: ").strip()
        results = self.search_tasks(keyword)
        if results:
            print(f"Found {len(results)} task(s) matching '{keyword}':")
            self.display_tasks(results)
        else:
            print(f"No tasks found matching '{keyword}'.")

    def filter_tasks_menu(self):
        """Menu for filtering tasks."""
        print("Filter by:")
        print("1. Status")
        print("2. Priority Level")
        print("3. Due Date")
        filter_choice = input("Choose a filter option: ").strip()
        if filter_choice == '1':
            status_options = {
                '1': 'To be started',
                '2': 'In progress',
                '3': 'Finished'
            }
            status_choice = input("Select status:\n1. To be started\n2. In progress\n3. Finished\n").strip()
            value = status_options.get(status_choice)
            if value:
                filtered_tasks = self.filter_tasks('status', value)
                self.display_tasks(filtered_tasks)
            else:
                print("Invalid status option.")
        elif filter_choice == '2':
            try:
                priority_level = int(input("Enter priority level (1-10): ").strip())
                if 1 <= priority_level <= 10:
                    filtered_tasks = self.filter_tasks('priority_level', priority_level)
                    self.display_tasks(filtered_tasks)
                else:
                    print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid integer.")
        elif filter_choice == '3':
            due_date = input("Enter due date (format flexible, e.g., YYYY-MM-DD): ").strip()
            filtered_tasks = self.filter_tasks('due_date', due_date)
            self.display_tasks(filtered_tasks)
        else:
            print("Invalid filter option.")

    def handle_menu_choice(self, choice):
        """Handle a single menu choice."""
        if choice == '1':
            self.add_task()
        elif choice == '2':
            self.display_kanban_board()
        elif choice == '3':
            self.edit_task()
        elif choice == '4':
            self.delete_task()
        elif choice == '5':
            self.search_tasks_menu()
        elif choice == '6':
            self.filter_tasks_menu()
        elif choice == '7':
            print("Exiting Task Manager. Goodbye!")
            return False  # Signal to exit the loop
        else:
            print("Invalid choice. Please select a valid option.")
        return True  # Continue the loop

def main():
    task_manager = TaskManager()

    continue_loop = True
    while continue_loop:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Display Kanban Board")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Filter Tasks")
        print("7. Exit")

        choice = input("Choose an option: ").strip()
        continue_loop = task_manager.handle_menu_choice(choice)

if __name__ == "__main__":
    main()
