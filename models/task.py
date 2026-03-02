import json
from utils.file import get_data_path

class Task:
    id_counter = 1

    def __init__(self, title, project_id, status='pending', assigned_to=None, task_id=None):
        self.task_id = task_id or Task.id_counter
        if not task_id:
            Task.id_counter = max(Task.id_counter, self.task_id + 1)
        self.title = title
        self.project_id = project_id
        self.status = status  
        self.assigned_to = assigned_to  

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        allowed = ['pending', 'in_progress', 'completed']
        if value not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        self._status = value

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'title': self.title,
            'project_id': self.project_id,
            'status': self.status,
            'assigned_to': self.assigned_to
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            data['title'],
            data['project_id'],
            data.get('status', 'pending'),
            data.get('assigned_to'),
            data['task_id']
        )
        return task

    def __repr__(self):
        return f"Task(id={self.task_id}, title={self.title}, status={self.status})"

    _all_tasks = {}

    @classmethod
    def load_all(cls):
        path = get_data_path('tasks.json')
        try:
            with open(path, 'r') as f:
                tasks_data = json.load(f)
            cls._all_tasks = {tid: cls.from_dict(t) for tid, t in tasks_data.items()}
            if cls._all_tasks:
                cls.id_counter = max(int(tid) for tid in cls._all_tasks) + 1
        except FileNotFoundError:
            cls._all_tasks = {}
        except json.JSONDecodeError:
            print("Warning: tasks.json corrupted. Starting fresh.")
            cls._all_tasks = {}

    @classmethod
    def save_all(cls):
        path = get_data_path('tasks.json')
        tasks_dict = {str(t.task_id): t.to_dict() for t in cls._all_tasks.values()}
        with open(path, 'w') as f:
            json.dump(tasks_dict, f, indent=2)

    @classmethod
    def add(cls, task):
        cls._all_tasks[str(task.task_id)] = task
        cls.save_all()

    @classmethod
    def find_by_id(cls, task_id):
        return cls._all_tasks.get(str(task_id))

    @classmethod
    def get_all(cls):
        return list(cls._all_tasks.values())

    @classmethod
    def get_for_project(cls, project_id):
        return [t for t in cls._all_tasks.values() if t.project_id == project_id]

    @classmethod
    def get_for_user(cls, user_id):
        return [t for t in cls._all_tasks.values() if t.assigned_to == user_id]