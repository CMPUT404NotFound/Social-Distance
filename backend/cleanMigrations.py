import os
import shutil


def cleanUp():
    '''
    run this to delete all current migrations and make an initial migration for each app.
    '''
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    from django.core.management import execute_from_command_line

    needMigrations = ["author", "comment", "Followers", "globalSetting", "inbox", "likes", "nodes", "posts"]
    managerPath = os.path.abspath("manage.py")

    for item in needMigrations:
        migrationDir = os.path.join(item, "migrations")
        if os.path.isdir(item) and os.path.isdir(migrationDir):
            shutil.rmtree(migrationDir)

    for item in needMigrations:
        print(f"making migrations for {item}...")
        execute_from_command_line(["manage.py", "makemigrations", item])

    print("making migrations again....")
    execute_from_command_line(
        [
            "manage.py",
            "makemigrations",
        ]
    )
    print("migrating....")
    execute_from_command_line(["manage.py", "migrate"])


if __name__ == "__main__":
    cleanUp()
