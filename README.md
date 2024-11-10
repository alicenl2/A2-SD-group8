# Task Manager Application
## Overview
The Task Manager Application is a command-line tool designed to help users manage their tasks efficiently. It allows users to add, view, edit, delete, search, and filter tasks. The application also provides a Kanban board view with color-coded priorities to visualize task statuses.

Version v1.02 includes several new features and improvements, enhancing the user experience and functionality.

## Features (Up to v1.02)
- Add Tasks: Create new tasks with details such as name, due date, description, priority level, and status.
- Display Tasks:
  - Kanban Board: Visualize tasks organized by status with color-coded priority levels.
- Edit Tasks: Modify existing tasks to update information or correct mistakes.
- Delete Tasks: Remove tasks that are completed or no longer needed.
- Search Tasks: Search for tasks by keywords in the task name or description.
- Filter Tasks: Filter tasks based on status, priority level, or due date.
- Improved Input Validation: Enhanced error handling and input validation for a smoother user experience.
- Color Coding and Task Categorization: Tasks are color-coded based on priority in the Kanban board view.

## Installation
### Prerequisites
  Python 3.6 or higher installed on your system.

**Clone the Repository**
```bash
  git clone https://github.com/alicenl2/A2-SD-group8.git
  cd A2-SD-group8
 ```

**No External Dependencies**: Version v1.02 does not require any external Python packages. It utilizes Python's built-in libraries and ANSI escape codes for color formatting.

**Note for Windows Users**: The color codes used in the Kanban board may not display correctly in the default Command Prompt. Consider using a terminal that supports ANSI escape codes or installing the colorama package.

## Usage
Run the application from the command line:

```bash
python task_manager.py
```

## Main Menu
Upon running the application, you will see the following menu options:
```markdown
Task Manager Menu:
1. Add Task
2. Display Kanban Board
3. Edit Task
4. Delete Task
5. Search Tasks
6. Filter Tasks
7. Exit
```
### Adding a Task
Select Option 1: Type 1 and press Enter.

Enter Task Details:
- Task Name: Provide a descriptive name.
- Due Date: Specify the due date (format flexible, e.g., YYYY-MM-DD).
- Description: Optionally, add more details.
- Priority Level: Enter a number from 1 (lowest) to 10 (highest).
- Status: Choose from:
1. To be started
2. In progress 
3. Finished
- Confirmation: The task will be added and saved.

### Displaying TasksOption 2: Display Kanban Board
Visualizes tasks organized by status: "To Be Started," "In Progress," and "Finished."
Tasks are color-coded based on priority:
- High Priority (8-10): Red
- Medium Priority (4-7): Yellow
- Low Priority (1-3): Green

### Editing a Task
Select Option 3: Type 3 and press Enter.
Choose Task: Enter the task number you wish to edit.

For each prompt, enter new information or press Enter to keep the current value.

Confirmation: The task will be updated and saved.

### Deleting a Task
Select Option 4: Type 4 and press Enter.
Choose Task: Enter the task number you wish to delete.

Confirmation: The task will be removed from the list.

### Searching Tasks
Select Option 5: Type 5 and press Enter.

Enter Keyword: Input the keyword to search for in task names and descriptions.

View Results: The application will display tasks matching the keyword.

### Filtering Tasks
Select Option 6: Type 6 and press Enter.

Choose Filter Type:
1. Filter by Status
2. Filter by Priority Level
3. Filter by Due Date

Enter Filter Value:

Status:
1. To be started
2. In progress
3. Finished

Priority Level: Enter a number between 1 and 10.

Due Date: Enter the due date (consistent with the format used when adding tasks).

View Filtered Tasks: The application will display tasks matching the filter criteria.

### Exiting the Application
Select Option 7: Type 7 and press Enter to exit.

## Known Issues in v1.02
Input Validation: While improved, some inputs may still not be thoroughly validated.
Terminal Compatibility: ANSI color codes may not display correctly on all terminals, especially on Windows CMD.

## Future Improvements
Planned enhancements for upcoming versions:

- Cross-Platform Color Support: Implement libraries like colorama for better color handling on Windows.
- Enhanced Date Handling: Incorporate date validation and formatting.
- Recurring Tasks: Allow users to set tasks that recur at specified intervals.
- User Authentication: Implement user accounts for personalized task management.
- Graphical User Interface (GUI): Develop a GUI version of the application for improved usability.

## Testing
The application includes a suite of unit tests to ensure functionality and reliability. Tests cover:

- Adding, editing, and deleting tasks.
- Searching and filtering tasks.
- Displaying tasks and the Kanban board.
- Input validation and error handling.

To run the tests:
```bash
python -m unittest discover tests
```

Thank you for using the Task Manager Application! Your feedback is appreciated and will help improve future versions.