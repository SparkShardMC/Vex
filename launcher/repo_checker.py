import os
import requests
import subprocess
import yaml
import sys

GITHUB_RAW_URL = "https://raw.githubusercontent.com/SparkShardMC/Vex/main/version.yml"
LOCAL_VERSION_FILE = "../config/version.yml"

def get_remote_version():
    r = requests.get(GITHUB_RAW_URL)
    r.raise_for_status()
    return yaml.safe_load(r.text)["version"]

def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return None
    with open(LOCAL_VERSION_FILE, "r") as f:
        return yaml.safe_load(f)["version"]

def update_local_version(new_version):
    with open(LOCAL_VERSION_FILE, "w") as f:
        yaml.dump({"version": new_version}, f)

def check_for_update():
    remote_version = get_remote_version()
    local_version = get_local_version()
    if remote_version != local_version:
        print(f"New version available: {remote_version}")
        # Run packager.py to generate installer
        script_path = os.path.join(os.path.dirname(__file__), "packager.py")
        subprocess.run([sys.executable, script_path], check=True)
        update_local_version(remote_version)
        print("Update installed successfully!")
    else:
        print("You have the latest version.")

if __name__ == "__main__":
    check_for_update()
