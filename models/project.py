import json
from utils.file import get_data_path

class Project:
    id_counter = 1

    def __init__(self, title, user_id, description=None, due_date=None, project_id=None):
        self.project_id = project_id or Project.id_counter
        if not project_id:
            Project.id_counter = max(Project.id_counter, self.project_id + 1)
        self.title = title
        self.user_id = user_id
        self.description = description
        self.due_date = due_date
        self._tasks = []  

    def add_task(self, task_id):
        if task_id not in self._tasks:
            self._tasks.append(task_id)

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'title': self.title,
            'user_id': self.user_id,
            'description': self.description,
            'due_date': self.due_date,
            'tasks': self._tasks
        }

    @classmethod
    def from_dict(cls, data):
        proj = cls(
            data['title'],
            data['user_id'],
            data.get('description'),
            data.get('due_date'),
            data['project_id']
        )
        proj._tasks = data.get('tasks', [])
        return proj

    def __repr__(self):
        return f"Project(id={self.project_id}, title={self.title})"

    _all_projects = {}

    @classmethod
    def load_all(cls):
        path = get_data_path('projects.json')
        try:
            with open(path, 'r') as f:
                projects_data = json.load(f)
            cls._all_projects = {pid: cls.from_dict(p) for pid, p in projects_data.items()}
            if cls._all_projects:
                cls.id_counter = max(int(pid) for pid in cls._all_projects) + 1
        except FileNotFoundError:
            cls._all_projects = {}
        except json.JSONDecodeError:
            print("projects.json corrupted. ")
            cls._all_projects = {}

    @classmethod
    def save_all(cls):
        path = get_data_path('projects.json')
        projects_dict = {str(p.project_id): p.to_dict() for p in cls._all_projects.values()}
        with open(path, 'w') as f:
            json.dump(projects_dict, f, indent=2)

    @classmethod
    def add(cls, project):
        cls._all_projects[str(project.project_id)] = project
        cls.save_all()

    @classmethod
    def find_by_title(cls, title):
        for p in cls._all_projects.values():
            if p.title.lower() == title.lower():
                return p
        return None

    @classmethod
    def get_all(cls):
        return list(cls._all_projects.values())

    @classmethod
    def get_for_user(cls, user_id):
        return [p for p in cls._all_projects.values() if p.user_id == user_id]