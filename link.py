import json
import os

LOCATION_FILE_NAME = '.locations.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OLD_FILES_DIR = ".old"

for config_dir in os.listdir():
    if (not os.path.isdir(config_dir)) or config_dir.startswith('.'):
        continue;
    with open(os.path.join(ROOT_DIR, config_dir, LOCATION_FILE_NAME)) as location_file:
        data = json.load(location_file)
        for config_file in data:
            #ln -s config_file
            source = os.path.join(ROOT_DIR, config_dir, config_file)
            dest = os.path.expanduser(data[config_file])
            if os.path.islink(dest):
                print("{} already linked".format(dest))
            else:
                if os.path.isfile(dest):
                    backup_dir = os.path.join(ROOT_DIR, OLD_FILES_DIR, config_dir)
                    if not os.path.isdir(backup_dir):
                    	os.makedirs(backup_dir)
                    backup_path = os.path.join(backup_dir, config_file)
                    os.rename(dest, backup_path)
                    print("Old {} moved to {}".format(config_file, backup_path));
                print("ln -s {} {}".format(source, dest))
                os.symlink(source, dest)
