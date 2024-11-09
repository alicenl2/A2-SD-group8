import json

class TaskManager:
  """Class to manage tasks"""

  def __init__(self, task_file='list_of_tasks.json'):
    '''Initialize the TaskManager with a list of tasks'''
    self.task_file = task_file
    self.tasks = self.load_tasks()

  def load_tasks(self):
    '''Load tasks from a JSON file'''
    try:
      with open(self.task_file, 'r') as file:
        return json.load(file)
    except FileNotFoundError:
        return []

  def save_tasks(self):
    '''Save tasks to a JSON file'''
    with open(self.task_file, 'w') as file:
      json.dump(self.tasks, file, indent=4)

  def get_user_input(self):
    '''Collect task details from user'''
    task_name = input('What is the task you need to do? ')
    task_due_date = input('When is it due? ')
    task_description = input('Please enter a description if you want to: ')

    while True:
      try:
        priority_level = int(input('On a scale of 1 to 10, what is its priority level? '))
        if 1 <= priority_level <= 10:
          break
        else:
          print('Please enter a number between 1 and 10.')
      except ValueError:
        print('Please enter a valid integer between 1 and 10.')

    while True:
      try:
        status_options = {
            1: 'To be started',
            2: 'In progress',
            3: 'Finished'
        }
        status_choice = int(input("Please choose the status of the task:\n1. To be started\n2. In progress\n3. Finished\n"))
        if status_choice in status_options:
          status = status_options[status_choice]
          break
        else:
          print("Please enter a number between 1 and 3.")
      except ValueError:
        print("Please enter a valid integer (1, 2, or 3).")

    return {
        "task_name": task_name,
        "task_due_date": task_due_date,
        "task_description": task_description,
        "priority_level": priority_level,
        "status": status
    }

  def add_task(self):
    '''Add a new task'''
    task = self.get_user_input()
    self.tasks.append(task)
    self.save_tasks()
    print('Task added successfully!')
    print(f'Current tasks: {self.tasks}')

if __name__ == "__main__":
  task_manager = TaskManager()
  task_manager.add_task()