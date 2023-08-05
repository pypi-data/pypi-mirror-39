import os
import shutil

def test_root():
    return ".test"

def init_test_folder():
    put_folder(test_root())

def remove_test_folder():
    remove(test_root())

def remove_temp_folder():
    remove(test_root())
    
def compose_dir(parent, name):
    return os.path.join(parent or os.getcwd(), name)

def remove(dir):
    shutil.rmtree(dir)

def put_folder(name, parent = None):
    def create(dir):
        os.makedirs(dir)
        return dir
    return create(compose_dir(parent, name)) \
        if not os.path.exists(compose_dir(parent, name)) \
                       else compose_dir(parent, name)

def put_file(name, parent = None, content = None):
    with open(compose_dir(parent, name), 'w') as file:
                       file.write(content)
    return compose_dir(parent, name)

def write_file(filepath, content = None):
    with open(filepath, 'w') as file:
        file.write(content)
    return filepath
def remove_file_if_exists(path):
    if os.path.exists(path):
        os.remove(path)
    return path

def create_folder_if_not_exists(filepath):
    def create_folder(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    create_folder(os.path.split(filepath)[0])
    
    return filepath
