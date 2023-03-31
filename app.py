import os
from folders import steam_libraries


def set_high_priority_update_behavior(appmanifest_file_path):
    with open(appmanifest_file_path, "r+") as f:
        lines = f.readlines()

        if len(lines) <= 19:
            # The appmanifest is missing.
            return False

        lines[19] = '\t"AutoUpdateBehavior"\t\t"2"\n'
        f.seek(0)
        f.writelines(lines)
        f.truncate()
        return True

# Get a list of appmanifest file paths in the given libraries.
def get_appmanifest_files(libraries):
    appmanifest_files = []

    for library in libraries:
        files_list = os.listdir(library)
        
        for file in files_list:
            if file.startswith("appmanifest"):
                appmanifest_files.append(os.path.join(library, file))

    return appmanifest_files


if __name__ == "__main__":
    appmanifest_files = get_appmanifest_files(steam_libraries)
    updated_files = []

    for file_path in appmanifest_files:
        if set_high_priority_update_behavior(file_path):
            updated_files.append(file_path)

    if updated_files:
        print("The following games have been set to update with high priority:")
        for file_path in updated_files:
            with open(file_path, "r") as f:
                game_name = f.readlines()[5].split("\"")[3]
                print(game_name)
    else:
        print("No games were updated.")

    input("Press Enter to continue...")