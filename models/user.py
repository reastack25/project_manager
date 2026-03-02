import json
from utils.file import get_data_path

class User:
    id_counter = 1  

    def __init__(self, name, email=None, user_id=None):
        self.user_id = user_id or User.id_counter
        if not user_id:
            User.id_counter = max(User.id_counter, self.user_id + 1)
        self.name = name
        self.email = email  
        self._projects = []  

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value and '@' not in value:
            raise ValueError("Invalid email ")
        self._email = value

    def add_project(self, project_id):
        if project_id not in self._projects:
            self._projects.append(project_id)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'projects': self._projects
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data['name'], data.get('email'), data['user_id'])
        user._projects = data.get('projects', [])
        return user

    def __repr__(self):
        return f"User(id={self.user_id}, name={self.name})"

   
    _all_users = {}

    @classmethod
    def load_all(cls):
        path = get_data_path('users.json')
        try:
            with open(path, 'r') as f:
                users_data = json.load(f)
            cls._all_users = {uid: cls.from_dict(u) for uid, u in users_data.items()}
            if cls._all_users:
                cls.id_counter = max(int(uid) for uid in cls._all_users) + 1
        except FileNotFoundError:
            cls._all_users = {}
        except json.JSONDecodeError:
            print(" users.json corrupted. ")
            cls._all_users = {}

    @classmethod
    def save_all(cls):
        path = get_data_path('users.json')
        users_dict = {str(u.user_id): u.to_dict() for u in cls._all_users.values()}
        with open(path, 'w') as f:
            json.dump(users_dict, f, indent=2)

    @classmethod
    def add(cls, user):
        cls._all_users[str(user.user_id)] = user
        cls.save_all()

    @classmethod
    def find_by_name(cls, name):
        for u in cls._all_users.values():
            if u.name.lower() == name.lower():
                return u
        return None

    @classmethod
    def get_all(cls):
        return list(cls._all_users.values())