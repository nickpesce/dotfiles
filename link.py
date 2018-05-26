import json
import os
import sys

LOCATIONS_FILE_NAME = '.locations.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_FILES_DIR = ".old"

def link_all():
    for config_dir in iter_valid_dirs():
        link(config_dir)

def link(config_dir):
    if not os.path.isdir(config_dir):
        return print("{} is not a directory".format(config_dir))
    locations_file_path = os.path.join(ROOT_DIR, config_dir, LOCATIONS_FILE_NAME);
    for(source, dest) in iter_files(locations_file_path):
        if os.path.islink(dest):
            print("{} already linked".format(dest))
        else:
            backup(dest, config_dir, source)
            dest_dir = os.path.dirname(dest)
            ensure_dir(dest_dir)
            source_path = os.path.join(ROOT_DIR, config_dir, source)  
            os.symlink(source_path, dest)
            print("ln -s {} {}".format(source_path, dest))

def iter_valid_dirs():
    for dir_ in os.listdir():
        if os.path.isdir(dir_) and not dir_.startswith('.'):
            yield dir_

def iter_files(locations_path):
    """Iterates through (src, dest) as RELATIVE sources and ABSOLUTE destinations
    specified by the locations file."""
    if not os.path.isfile(locations_path):
        return print("{} does not exist!".format(locations_path))
    with open(locations_path) as locations_file:
        locations = json.load(locations_file)
        for config_file in locations:
            source = config_file
            dest = os.path.expanduser(locations[config_file])
            yield (source, dest)

def ensure_dir(dir_):
    if not os.path.isdir(dir_):
        os.makedirs(dir_)

def backup(path, config_dir, config_file):
    if os.path.exists(path):
        backup_dir = os.path.join(ROOT_DIR, OLD_FILES_DIR, config_dir)
        ensure_dir(backup_dir)
        backup_path = os.path.join(backup_dir, config_file)
        os.rename(path, backup_path)
        print("Old {} moved to {}".format(config_file, backup_path));

if __name__ == '__main__':
    if len(sys.argv) == 1:
        link_all()
    else:
        for config_dir in sys.argv[1:]:
            link(config_dir)
