from os import listdir, system, path
from folders import steam_libraries

if __name__ == "__main__":
    for library in steam_libraries:
        files_list = listdir(library)
        
        for file in files_list:
            if file.startswith("appmanifest"):
                # Join the steam library path and the game path
                game_path = path.join(library, file)
                with open(game_path, "r") as f:
                    # Read lines from the appmanifest file
                    line = f.readlines()
                    if len(line) > 10:
                        print("GAME FOUND:", line[5].split("\"")[3])
                        # Change the Update Behavior to High Priority (2)
                        line[19] = '\t"AutoUpdateBehavior"\t\t"2"\n'
                        # Save the changes to final file
                        with open(game_path, "w") as file:
                            file.writelines(line)
    print("\nAll installed games have been set update to high priority.\n")
    system('pause')
