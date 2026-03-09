import os
import yaml
import platform
import subprocess

# Detect OS
current_os = platform.system().lower()  # 'windows' or 'darwin' for mac

# Load config
with open("../config/electron_config.yml", "r") as f:
    config = yaml.safe_load(f)

if current_os.startswith("win"):
    cfg = config["windows"]
elif current_os.startswith("darwin"):
    cfg = config["mac"]
else:
    raise Exception("Unsupported OS for packaging")

output_name = cfg["output_name"]
icon = cfg["icon"]
build_dir = cfg["build_dir"]
source_dir = config["source_dir"]

# Ensure build directory exists
os.makedirs(build_dir, exist_ok=True)

# Command to package with Electron
cmd = [
    "npx", "electron-packager", source_dir, "Vex",
    "--overwrite",
    f"--out={build_dir}",
    f"--icon={icon}",
]

if current_os.startswith("win"):
    cmd.append("--platform=win32")
elif current_os.startswith("darwin"):
    cmd.append("--platform=darwin")

print("Packaging VEX with Electron...")
subprocess.run(cmd)
print(f"Packaged {output_name} in {build_dir}")
