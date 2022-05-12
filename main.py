import json
import os
import sys
import copy

def main(umm_path):
    for dirs in os.listdir(umm_path):
        # Path variable for the current mod's path
        current_path = os.path.join(umm_path, dirs)
        # Checks if the mod path is a directory
        if os.path.isdir(current_path):
            # Theoretical path to the mod's config.json
            current_path_to_json = os.path.join(current_path, "config.json")
            # Checks if the json path exists
            if os.path.isfile(current_path_to_json):
                # Opens the json and loads it into a dict
                f = open(current_path_to_json)
                mod_json: dict = json.load(f)
                # Defines the key to use for "new-dir-files"
                key = "new_dir_files" if ("new_dir_files" in mod_json) else "new-dir-files" if ("new-dir-files" in mod_json) else None
                # Returns the loop if "new-dir-files" isn't in the json
                if key == None:
                    continue
                # Copies the mod's json to iterate over it, required so that it doesn't error when we make changes to the json
                mod_json_copy = copy.deepcopy(mod_json)
                # Iterates through the "new-dir-files" dict in the json
                for dirs in mod_json_copy[key]:
                    # Sets the path index as 0 for every directory list
                    path_idx = 0
                    # Iterates through the paths in the list
                    for paths in mod_json_copy[key][dirs]:
                        # Path variable for the given added file
                        path_to_file = os.path.join(current_path, paths)
                        # Checks if the file exists, and adds to the path index if so
                        if os.path.isfile(path_to_file):
                            path_idx += 1
                        # If the file doesnt exist, remove the entry from the list
                        else:
                            del mod_json[key][dirs][path_idx]
                    # Checks if the directory list is empty
                    if mod_json[key][dirs] == []:
                        # Deletes the directory list if it is empty
                        del mod_json[key][dirs]
                f = open(current_path_to_json, "w+")
                json.dump(mod_json, f, indent=4)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print("usage: main.py <path-to-ultimate-mods>")