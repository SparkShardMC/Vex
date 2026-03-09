from updater import check_for_updates
from installer import install_game
from os_detector import get_os

def start_launcher():

    system = get_os()
    print("Operating System:", system)

    update = check_for_updates()

    if update:
        print("Update available")
        install_game(system)
    else:
        print("Vex is up to date")

if __name__ == "__main__":
    start_launcher()
