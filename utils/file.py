import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_data_path(filename):
    ensure_data_dir()
    return os.path.join(DATA_DIR, filename)