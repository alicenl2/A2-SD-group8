import json

class TaskManager:
    """Class to manage tasks."""

    def __init__(self, task_file='list_of_tasks.json'):
        """Initialize the TaskManager with a list of tasks."""
        self.task_file = task_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from a JSON file."""
        try:
            with open(self.task_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        """Save tasks to a JSON file."""
        with open(self.task_file, 'w') as file:
            json.dump(self.tasks, file, indent=4)

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
            1: 'To be started',
            2: 'In progress',
            3: 'Finished'
        }
        while True:
            try:
                status_choice = int(input("Please choose the status of the task:\n1. To be started\n2. In progress\n3. Finished\n"))
                if status_choice in status_options:
                    return status_options[status_choice]
                else:
                    print("Please enter a valid option (1, 2, or 3).")
            except ValueError:
                print("Please enter a valid integer (1, 2, or 3).")

    def add_task(self):
        """Add a new task."""
        task = self.get_user_input()
        self.tasks.append(task)
        self.save_tasks()
        print("Task added successfully!")

    def display_tasks(self):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks available.")
            return

        for index, task in enumerate(self.tasks, start=1):
            print(f"\nTask {index}:")
            print(f"Name: {task['task_name']}")
            print(f"Due Date: {task['task_due_date']}")
            print(f"Description: {task['task_description']}")
            print(f"Priority Level: {task['priority_level']}")
            print(f"Status: {task['status']}")

    def edit_task(self):
        """Edit an existing task."""
        self.display_tasks()
        try:
            task_number = int(input("Enter the task number you want to edit: "))
            task = self.tasks[task_number - 1]
        except (ValueError, IndexError):
            print("Invalid task number.")
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
        self.display_tasks()
        try:
            task_number = int(input("Enter the task number you want to delete: "))
            self.tasks.pop(task_number - 1)
            self.save_tasks()
            print("Task deleted successfully!")
        except (ValueError, IndexError):
            print("Invalid task number.")
            return

    def view_statistics(self):
        """Display statistics about tasks."""
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task['status'] == 'Finished'])
        print(f"Total tasks: {total_tasks}")
        print(f"Completed tasks: {completed_tasks}")

def main():
    task_manager = TaskManager()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Display Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Show Statistics")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            task_manager.add_task()
        elif choice == '2':
            task_manager.display_tasks()
        elif choice == '3':
            task_manager.edit_task()
        elif choice == '4':
            task_manager.delete_task()
        elif choice == '5':
            task_manager.view_statistics()
        elif choice == '6':
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

