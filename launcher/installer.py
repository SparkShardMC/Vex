import subprocess

def install_game(system):

    if system == "windows":
        subprocess.run("builds/windows/vex_installer.exe")

    elif system == "mac":
        subprocess.run("open builds/mac/vex_installer.dmg")

    else:
        print("Unsupported system")
