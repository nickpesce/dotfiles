import json
import os

LOCATION_FILE_NAME = '.locations.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_FILES_DIR = ".old"

def link():
    for config_dir in iter_valid_dirs():
        location_file_path = os.path.join(ROOT_DIR, config_dir, LOCATION_FILE_NAME);
        with open(location_file_path) as location_file:
            data = json.load(location_file)
            for config_file in data:
                source = os.path.join(ROOT_DIR, config_dir, config_file)
                dest = os.path.expanduser(data[config_file])
                if os.path.islink(dest):
                    print("{} already linked".format(dest))
                else:
                    backup(dest, config_dir, config_file)
                    dest_dir = os.path.dirname(dest)
                    ensure_dir(dest_dir)
                    os.symlink(source, dest)
                    print("ln -s {} {}".format(source, dest))

def iter_valid_dirs():
    for dir_ in os.listdir():
        if os.path.isdir(dir_) and not dir_.startswith('.'):
            yield dir_

def ensure_dir(dir_):
    if not os.path.isdir(dir_):
        os.makedirs(dir_)

def backup(file_path, config_dir, config_file):
    if os.path.isfile(file_path):
        backup_dir = os.path.join(ROOT_DIR, OLD_FILES_DIR, config_dir)
        ensure_dir(backup_dir)
        backup_path = os.path.join(backup_dir, config_file)
        os.rename(dest, backup_path)
        print("Old {} moved to {}".format(config_file, backup_path));

if __name__ == '__main__':
    link()
