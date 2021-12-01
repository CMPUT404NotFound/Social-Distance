


import os


def cleanUp():
    
    for item in os.listdir():
        if os.path.isdir(item) and os.path.isdir(migrationDir := os.path.join(item, "migrations")):
            os.removedirs(migrationDir)
        

if __name__ == "__main__":
    cleanUp()