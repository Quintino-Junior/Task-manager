import json
from pathlib import Path
from typing import List, Dict

TASKS_PATH = Path("tasks.json")
VALID_PRIORITIES = {"high", "medium", "low"}
VALID_STATUS = {"todo", "ongoing", "done"}


class TaskManager:
    """Handles loading, saving, and manipulating tasks."""

    def __init__(self, filepath: Path = TASKS_PATH):
        self.filepath = filepath
        self.task_list = self.load()

    def load(self) -> List[Dict]:
        if not self.filepath.exists():
            return []
        try:
            return json.loads(self.filepath.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("Warning: tasks.json is corrupted. Starting with empty task list.")
            return []

    def save(self) -> None:
        self.filepath.write_text(json.dumps(self.task_list, indent=4, ensure_ascii=False), encoding="utf-8")

    def _validate_input(self, value: str, valid_set: set, label: str) -> str:
        clean_value = value.strip().lower()
        if clean_value not in valid_set:
            raise ValueError(f"{label} must be one of {', '.join(sorted(valid_set))}")
        return clean_value.capitalize()

    def add(self, task: str, priority: str = "medium", status: str = "todo") -> bool:
        if not task.strip():
            raise ValueError("Task description cannot be empty")

        # Uso da função de validação centralizada
        p = self._validate_input(priority, VALID_PRIORITIES, "Priority")
        s = self._validate_input(status, VALID_STATUS, "Status")
        
        self.task_list.append({"task": task.strip(), "priority": p, "status": s})
        self.save() # Salva a lista que já está na memória
        return True

    def delete(self, index: int) -> bool:
        if not (1 <= index <= len(self.task_list)):
            raise ValueError("Invalid task index")
        self.task_list.pop(index - 1)
        self.save()
        return True

    def edit(self, index: int, task: str = None, priority: str = None, status: str = None) -> bool:
        if not (1 <= index <= len(self.task_list)):
            raise ValueError("Invalid task index")
        
        if task is not None:
            task_text = task.strip()
            if not task_text:
                raise ValueError("Task cannot be empty")
            self.task_list[index - 1]['task'] = task_text

        # Uso da função de validação centralizada
        if priority is not None:
            p = self._validate_input(priority, VALID_PRIORITIES, "Priority")
            self.task_list[index - 1]['priority'] = p
        if status is not None:
            s = self._validate_input(status, VALID_STATUS, "Status")
            self.task_list[index - 1]['status'] = s
            
        self.save()
        return True

    def list_all(self) -> None:
        if not self.task_list:
            print("No tasks found.")
            return

        for idx, entry in enumerate(self.task_list, start=1):
            priority = entry.get('priority', 'Unknown')
            task_text = entry.get('task', 'Unknown')
            status = entry.get('status', 'Todo')
            print(f"{idx}. [{priority}] {task_text} ({status})")

    def list_by_priority(self, priority: str) -> None:
        priority_lower = priority.strip().lower()
        if priority_lower not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {', '.join(sorted(VALID_PRIORITIES))}")

        filtered_tasks = [t for t in self.task_list if t.get('priority', '').lower() == priority_lower]

        if not filtered_tasks:
            print(f"No tasks with priority '{priority}' found.")
            return

        for idx, entry in enumerate(filtered_tasks, start=1):
            task_text = entry.get('task', 'Unknown')
            status = entry.get('status', 'Todo')
            print(f"{idx}. [{priority.capitalize()}] {task_text} ({status})")
    
    def list_by_status(self, status: str) -> None:
        status_lower = status.strip().lower()
        if status_lower not in VALID_STATUS:
            raise ValueError(f"Status must be one of {', '.join(sorted(VALID_STATUS))}")

        filtered_tasks = [t for t in self.task_list if t.get('status', '').lower() == status_lower]

        if not filtered_tasks:
            print(f"No tasks with status '{status}' found.")
            return

        for idx, entry in enumerate(filtered_tasks, start=1):
            priority = entry.get('priority', 'Unknown')
            task_text = entry.get('task', 'Unknown')
            print(f"{idx}. [{priority}] {task_text} ({status.capitalize()})")

def main():
    manager = TaskManager()
    while True:
        print("\n--- Task Manager ---")
        print("1. Add task")
        print("2. List tasks")
        print("3. Edit task")
        print("4. Delete task")
        print("5. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n--- Add Task ---")
            task = input("Task: ").strip()
            priority = input("Priority (High/Medium/Low): ").strip()
            status = input("Status (Todo/Ongoing/Done) [Todo]: ").strip() or "todo"
            try:
                manager.add(task, priority, status)
                print("Task added")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            print("\n--- List Tasks ---")
            print("1. All tasks")
            print("2. By priority")
            print("3. By status")
            sub_choice = input("Choose an option: ").strip()
            if sub_choice == "1":
                print("\n--- All Tasks ---")
                manager.list_all()
            elif sub_choice == "2":
                priority = input("Priority (High/Medium/Low): ").strip()
                print(f"\n--- List tasks by Priority: {priority.capitalize()} ---")
                manager.list_by_priority(priority)
            elif sub_choice == "3":
                status = input("Status (Todo/Ongoing/Done): ").strip()
                print(f"\n--- List tasks by Status: {status.capitalize()} ---")
                manager.list_by_status(status)
            else:
                print("Invalid option.")

        elif choice == "3":
            print("\n--- Edit Task ---")
            manager.list_all()
            try:
                number = int(input("Task number to edit: ").strip())
                text = input("New task text (leave blank to keep unchanged): ").strip()
                priority = input("New priority (High/Medium/Low, leave blank to keep unchanged): ").strip()
                status = input("New status (Todo/Ongoing/Done, leave blank to keep unchanged): ").strip()
                manager.edit(number, task=text if text else None, priority=priority if priority else None, status=status if status else None)
                print("Task edited")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("\n--- Delete Task ---")
            manager.list_all()
            try:
                number = int(input("Task number to delete: ").strip())
                manager.delete(number)
                print("Task deleted")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("Goodbye")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
